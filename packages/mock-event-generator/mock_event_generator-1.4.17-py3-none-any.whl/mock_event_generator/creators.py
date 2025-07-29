"""Classes for creating G-events in GraceDB."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from io import BytesIO
from typing import Any

# --------------------------------------
# Deprecated: ligo.lw --> igwn_ligolw
# https://git.ligo.org/emfollow/gwcelery/-/merge_requests/1636/diffs
#
import igwn_ligolw
import igwn_ligolw.lsctables
import igwn_ligolw.utils

# import igwn_ligolw.array
# import igwn_ligolw.param
# import igwn_ligolw.table
import trio
from astropy.time import Time
from igwn_ligolw.ligolw import Document, LIGOLWContentHandler
from lxml import etree
from lxml.etree import _Element, _ElementTree
from requests import HTTPError

from ligo.skymap.util import ilwd

from .cache import EventFileCache, GEventCacheEntry, SEventCacheEntry
from .gracedbs import GraceDBWithContext
from .models import GEventDescription, SEventDescription, Upload
from .utils import split_filename

IS_FITS_REGEX = re.compile(r'\.fits(\.gz)?$')

logger = logging.getLogger(__name__)


@ilwd.use_in
class ContentHandler(LIGOLWContentHandler):  # type: ignore[misc]
    """Class for parsing LIGO Light Weight documents with a SAX2-compliant parser.

    Old-style row IDs are converted on the fly.
    """


@dataclass
class SEventCreator:
    """Creator of the G-events that belong to a given S-event in GraceDB.

    It creates G-events mostly identitical to the G-events belonging to the original
    S-event. The only G-event fields that can be modified are:
        - the time reference, which is translated to the current time.
        - `group` the analysis group which identified the candidate.
        - `search` the type of search of the analysis pipeline.

    Attributes:
        sevent: The original S-event description.
        target: The GraceDB client where the G-events will be created.
        cache_entry: The cache entry, which stores the original G-event' data files.
    """

    sevent: SEventDescription
    target: GraceDBWithContext
    cache_entry: SEventCacheEntry

    @classmethod
    def from_id(
        cls, sevent_id: str, target: GraceDBWithContext, cache: EventFileCache
    ) -> SEventCreator:
        """Factory to create the G-events that belong to a given S-event.

        Parameters:
            sevent_id: Identifier of the S-event to be downloaded.
            target: The GraceDB client where the G-events will be created.
            cache: The event data file cache.
        """
        cache_entry = cache.get_sevent_cache_entry(sevent_id)
        sevent = cache_entry.get_description()
        return SEventCreator(sevent, target, cache_entry)

    async def create(
        self,
        group: str | None,
        search: str | None,
        sevent_time: float,
        max_delay: float | None = None,
    ) -> list[dict[str, Any]]:
        """Time-translate and create G-events.

        Time-translate all the G-events belonging to the original S-event and create
        them in GraceDB.

        Parameters:
            group: The analysis group which identified the candidate. If None, the
                original group is used.
            search: The type of search of the analysis pipeline. If None, the
                original search type is used.
            sevent_time: The new intrinsic S-event time (GPS time).
            max_delay: If not None, maximum lapse of time between the creation
                of the first G-Event and the last upload. If None, the original
                time sequencing of the uploads is reproduced.
        Returns:
            The list of newly created G-events, each represented as a dictionary.
        """
        creators = self._get_creators()
        if not creators:
            logger.warning('No events have been created.')
            return []

        async def func(
            creator: GEventCreator, event_time: float, request_delay: float
        ) -> None:
            id = creator.gevent.id
            gevents_out[id] = await creator.create(
                group, search, event_time, request_delay
            )

        gevents_in = [_.gevent for _ in creators]

        # A BUG WAS INTRUDUCE WHEN EARLY_WARNING EVENT ARE PRESENT
        # THAT NEED TO BE FIXED
        now = Time.now().gps
        logger.info(
            f'Replay of {self.sevent.id} using provided '
            f'gps time {sevent_time} (now()={now})'
        )

        # time of the G_event       => self.sevent.t_0,
        # creation time of G-events ==> self._get_original_creation_times(gevents_in)
        upload_delays = self._get_upload_delays(gevents_in, self.sevent.t_0, max_delay)
        extra_delay = -min([min(upload_delays[_][0] for _ in upload_delays), 0.0])
        if extra_delay > 0.0:
            logger.info('Applying an extra delay: some uploads have negative latency')

        gevents_out: dict[str, dict[str, Any]] = {}
        async with trio.open_nursery() as nursery:
            for creator in creators:
                creation_delay = upload_delays[creator.gevent.id][0] + extra_delay
                event_time = sevent_time + (creator.gevent.gpstime - self.sevent.t_0)
                logger.info(
                    f'G-event {creator.gevent.id} with '
                    f'delay of {creation_delay:.2f}s '
                    f'({creator.gevent.reporting_latency:.2f})'
                )
                nursery.start_soon(func, creator, event_time, creation_delay)

        return list(gevents_out.values())

    def _get_creators(self) -> list[GEventCreator]:
        creators: list[GEventCreator] = []
        for gevent_id in self.sevent.gevent_ids:
            cache_entry = self.cache_entry / gevent_id
            gevent = cache_entry.get_description()
            creator_cls = PIPELINE_GEVENT_CREATOR_CLASSES.get(gevent.pipeline)
            if creator_cls is None:
                logger.warning(
                    f'Cannot re-create G-event {gevent_id!r} from unknown pipeline '
                    f'{gevent.pipeline!r}.'
                )
                continue
            creator = creator_cls(gevent, self.target, cache_entry)
            creators.append(creator)
        return creators

    def _get_upload_delays(
        self, gevents: list[GEventDescription], reftime: float, max_delay: float | None
    ) -> dict[str, list[float]]:
        original_delays = self._get_original_upload_delays(gevents, reftime)
        _max_delay, _shrink_factor = self._get_shrink_factors(
            original_delays, max_delay
        )

        def _shrink(delay: float) -> float:
            if delay < 0.5 * _max_delay:
                return delay
            else:
                # <-  0.5 * _max_delay + _shrink_factor * (delay-0.5 * _max_delay)
                return _shrink_factor * delay + (1 - _shrink_factor) * 0.5 * _max_delay

        return {
            id: [_shrink(_) for _ in delays] for id, delays in original_delays.items()
        }

    #################################################################################

    def _get_original_upload_delays(
        self, gevents: list[GEventDescription], reftime: float
    ) -> dict[str, list[float]]:
        creation_times = self._get_original_creation_times(gevents)
        upload_delays = {
            gevent.id: [
                upload.delay + creation_time - reftime
                for upload in filter_uploads_unless(gevent.uploads, False)
            ]
            for gevent, creation_time in zip(gevents, creation_times)
        }
        return upload_delays

    def _get_original_creation_times(
        self, gevents: list[GEventDescription]
    ) -> list[float]:
        return [_.gpstime + _.reporting_latency for _ in gevents]

    @staticmethod
    def _get_shrink_factors(
        upload_delays: dict[str, list[float]], max_delay: float | None
    ) -> tuple[float, float]:
        _shrink_factor: float = 1.0
        _max_delay: float = 0.0
        actual_max_delay = max(delays[0] for delays in upload_delays.values())
        actual_max_delay2 = max(delays[-1] for delays in upload_delays.values())
        if (max_delay is None) or (actual_max_delay < max_delay):
            logger.info(
                f'The uploads to GraceDB will take {actual_max_delay:.2f}s, like the '
                f'original schedule. (full {actual_max_delay2:.2f}s)'
            )
            _max_delay = actual_max_delay
            _shrink_factor = 1.0
            return (_max_delay, _shrink_factor)
        else:
            _max_delay = max_delay

        logger.info(
            f'The uploads to GraceDB will take {max_delay:.2f}s, w.r.t the '
            f'original schedule of {actual_max_delay:.2f}s.'
        )
        if actual_max_delay == 0:
            _shrink_factor = 1.0
        else:
            _shrink_factor = (0.5 * _max_delay) / (actual_max_delay - 0.5 * _max_delay)

        return (_max_delay, _shrink_factor)


@dataclass
class GEventCreator:
    """Creator of G-events in GraceDB.

    It creates G-events mostly identitical to the specified input G-event. The only
    G-event fields that are / can be modified are:
        - the time reference, which is translated to the current time.
        - `group` the analysis group which identified the candidate.
        - `search` the type of search of the analysis pipeline.

    Attributes:
        gevent: The original G-event description.
        target: The GraceDB client where the G-event will be created.
        cache_entry: The cache entry, which stores the original G-event data files.
    """

    gevent: GEventDescription
    target: GraceDBWithContext
    cache_entry: GEventCacheEntry

    @classmethod
    def from_id(
        cls, gevent_id: str, target: GraceDBWithContext, cache: EventFileCache
    ) -> GEventCreator:
        """Factory to create G-events.

        Parameters:
            gevent_id: Identifier of the G-event to be downloaded.
            target: The GraceDB client where the G-event will be created.
            cache: The event data file cache.
        """
        cache_entry = cache.get_gevent_cache_entry(gevent_id)
        gevent = cache_entry.get_description()
        creator_cls = PIPELINE_GEVENT_CREATOR_CLASSES.get(gevent.pipeline)
        if creator_cls is None:
            raise NotImplementedError(
                f'Cannot re-create G-event {gevent_id!r} from unknown pipeline '
                f'{gevent.pipeline!r}.'
            )
        return creator_cls(gevent, target, cache_entry)

    async def create(
        self,
        group: str | None,
        search: str | None,
        event_time: float,
        delay: float = 0,
        max_delay: float | None = None,
        include_all_files: bool = False,
        extra_labels: list[str] | None = None,
    ) -> dict[str, Any]:
        """Time-translate the original G-event and re-generate it in GraceDB.

        Parameters:
            group: The analysis group which identified the candidate. If None, the
                original group is used.
            search: The type of search of the analysis pipeline. If None, the
                original search type is used.
            event_time: The new intrinsic event time (GPS time).
            delay: Delay to be waited for before sending the creation request to
                GraceDB (in seconds).
            max_delay: max delay in the replay of the additional uploads
            include_all_files: False (True will replay all the uploads)
            extra_lables: List of extra labels to be applied (default: [])
        Returns:
            The newly created G-event, as a dictionary.
        """
        await trio.sleep(delay)

        if group is None:
            group = self.gevent.group
        if search is None:
            search = self.gevent.search

        created_event = await self._upload_initial_data(
            group, search, event_time, extra_labels
        )
        event_id = created_event['graceid']

        # ------------------------------------------
        # await wait for the upload to comlete
        # So we have to reduce the wait accordingly
        # ------------------------------------------
        total_delay = 0.0
        if max_delay is None:
            max_delay = 3600
        for upload in filter_uploads_unless(self.gevent.uploads, include_all_files)[1:]:
            new_delay = upload.delay if upload.delay < max_delay else max_delay
            if new_delay >= total_delay:
                new_delay = new_delay - total_delay
            upload1 = Upload(upload.message, upload.tags, upload.filename, new_delay)
            logger.info(f'Now {total_delay} required {upload.delay} -> {upload1.delay}')
            total_delay = total_delay + new_delay
            await self._upload_additional_data(event_id, upload1, max_delay)

        return created_event

    async def _upload_initial_data(
        self,
        group: str,
        search: str,
        event_time: float,
        extra_labels: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Upload the initial data and create and event.

        Parameters:
            group: The analysis group which identified the candidate. If None, the
                original group is used.
            search: The type of search of the analysis pipeline. If None, the
                original search type is used.
            extra_lables: List of extra labels to be applied (default: [])
        """
        initial_upload = self.gevent.uploads[0]
        initial_filename, _ = split_filename(initial_upload.filename)
        filecontents = self._read_upload(initial_upload)
        delta_time = event_time - self.gevent.gpstime
        # If the request event time is zero, use the original event time
        if event_time == 0.0:
            delta_time = 0.0
        shifted_filecontents = self._shift_original_data(filecontents, delta_time)

        if extra_labels is None:
            apply_extra_labels = (
                ['MOCK', 'EARLY_WARNING'] if search == 'EarlyWarning' else 'MOCK'
            )
        elif len(extra_labels) < 1:
            apply_extra_labels = (
                ['MOCK', 'EARLY_WARNING'] if search == 'EarlyWarning' else 'MOCK'
            )
        else:
            apply_extra_labels = extra_labels
        try:
            created_event: dict[str, Any] = self.target.create_event(
                pipeline=self.gevent.pipeline,
                group=group,
                search=search,
                offline=self.gevent.offline,
                filename=initial_filename,
                filecontents=shifted_filecontents,
                labels=apply_extra_labels,
            ).json()
        except HTTPError as exc:
            logger.error(exc.response.text)
            raise

        try:
            descr = 'source ' + self.gevent.source + ' id:' + self.gevent.id
            self.target.write_log(
                created_event['graceid'],
                message=f'Event create by the mock event generator from {descr}',
                tag_name='meg',
            )
        except HTTPError as exc:
            logger.error(exc.response.text)
            raise

        self._report_creation(created_event)
        return created_event

    def _read_upload(self, upload: Upload) -> bytes:
        return self.cache_entry.read_bytes(upload.filename)

    def _shift_original_data(self, filecontents: bytes, delta_time: float) -> bytes:
        raise NotImplementedError

    def _report_creation(self, created_gevent: dict[str, Any]) -> None:
        id = f'{self.gevent.id} -> {created_gevent["graceid"]}  {self.gevent.pipeline}'
        group = created_gevent['group']
        if group != self.gevent.group:
            group = f'{self.gevent.group} -> {group}'
        search = created_gevent['search']
        if search != self.gevent.search:
            search = f'{self.gevent.search} -> {search}'
        event_time = created_gevent['gpstime']
        logger.info(f'Created {id:31}{group:15}{search:15}{event_time}')

    async def _upload_additional_data(
        self, event_id: str, upload: Upload, max_delay: float | None
    ) -> None:
        """Upload a file to GraceDB."""
        filename, version = split_filename(upload.filename)

        # Uploads with a maximum delay is not set
        logger.info(f'--> Delay requested for "{upload.filename}" is {upload.delay}.')
        if max_delay is None:
            await trio.sleep(upload.delay)
        elif upload.delay < max_delay:
            await trio.sleep(upload.delay)
        else:
            logger.info(
                f'--> Delay for "{upload.filename}"'
                f' is {upload.delay}. Set delay to {max_delay}'
            )
            await trio.sleep(max_delay)

        if 'p_astro.json' in filename:
            label = 'PASTRO_READY'
        elif 'sky_loc' in upload.tags and IS_FITS_REGEX.search(filename):
            label = 'SKYMAP_READY'
        else:
            label = None

        try:
            self.target.write_log(
                event_id,
                filename=filename,
                filecontents=self._read_upload(upload),
                message=upload.message,
                tag_name=upload.tags,
                label=label,
            )
        except HTTPError as exc:
            logger.error(exc.response.text)
            raise
        logger.info(f'Uploaded file for event {event_id}: {upload.filename}')


class MLyEventCreator(GEventCreator):
    """Creator of G-event for the MLy pipeline."""

    @staticmethod
    def _shift_original_data(raw_content: bytes, delta_time: float) -> bytes:
        data = json.loads(raw_content)
        data['gpstime'] = data['gpstime'] + delta_time
        new_content = json.dumps(data)
        return new_content.encode()


class oLIBEventCreator(GEventCreator):
    """Creator of G-event for the oLIB pipeline."""

    @staticmethod
    def _shift_original_data(raw_content: bytes, delta_time: float) -> bytes:
        data = json.loads(raw_content)
        data['gpstime'] = data['gpstime'] + delta_time
        new_content = json.dumps(data)
        return new_content.encode()


class CWBEventCreator(GEventCreator):
    """Creator of G-event for the cWB pipeline."""

    ORIGINAL_DATA_REGEX = re.compile(
        r'(?<=(^start:|^time: |^stop: ))( +(\d+\.\d*))+', re.MULTILINE
    )
    ORIGINAL_DATA_REGEX2 = re.compile(
        r'(?<=(^event_time:))( +(\d+\.\d*))+', re.MULTILINE
    )
    ORIGINAL_DATA_REGEX3 = re.compile(r'(?<=(^segment:))( +(\d+\.\d*))+', re.MULTILINE)
    ORIGINAL_DATA_LINE_REGEX = re.compile(r'\d+\.\d*')

    @staticmethod
    def _shift_original_data(raw_content: bytes, delta_time: float) -> bytes:
        def time_repl(match: re.Match[str]) -> str:
            new_time = float(match.group(0)) + delta_time
            return f'{new_time:.4f}'

        def line_repl(match: re.Match[str]) -> str:
            new_line, nsub = CWBEventCreator.ORIGINAL_DATA_LINE_REGEX.subn(
                time_repl, match.group(0)
            )
            if nsub < 1:
                raise ValueError(
                    f'Could not extract the event times. Has the format changed?\n'
                    f'{content}'
                )
            return new_line

        content = raw_content.decode()
        new_content, nsub = CWBEventCreator.ORIGINAL_DATA_REGEX.subn(line_repl, content)
        if nsub != 3:
            raise ValueError(
                f'Could not extract the event times. Has the format changed?\n{content}'
            )
        new_content, nsub = CWBEventCreator.ORIGINAL_DATA_REGEX2.subn(
            line_repl, new_content
        )
        new_content, nsub = CWBEventCreator.ORIGINAL_DATA_REGEX3.subn(
            line_repl, new_content
        )
        return new_content.encode()


class AframeEventCreator(GEventCreator):
    """Creator of G-event for the Aframe pipeline."""

    @staticmethod
    def _shift_original_data(raw_content: bytes, delta_time: float) -> bytes:
        data = json.loads(raw_content)
        data['gpstime'] = data['gpstime'] + delta_time
        new_content = json.dumps(data)
        return new_content.encode()


class CBCEventCreator(GEventCreator):
    """Creator of G-event for the CBC pipelines."""

    @staticmethod
    def _shift_original_data(raw_data: bytes, delta_time: float) -> bytes:
        buffer = BytesIO(raw_data)
        xmldoc: Document = igwn_ligolw.utils.load_fileobj(
            buffer, contenthandler=ContentHandler
        )

        CBCEventCreator._shift_original_document(xmldoc, delta_time)

        buffer = BytesIO()
        igwn_ligolw.utils.write_fileobj(xmldoc, buffer)
        return buffer.getvalue()

    @staticmethod
    def _shift_original_document(xmldoc: Document, delta_time: float) -> None:
        coinc_inspiral_table = igwn_ligolw.lsctables.CoincInspiralTable.get_table(
            xmldoc
        )
        for row in coinc_inspiral_table:
            row.end += delta_time

        sngl_inspiral_table = igwn_ligolw.lsctables.SnglInspiralTable.get_table(xmldoc)
        for row in sngl_inspiral_table:
            row.end += delta_time

        arrays = xmldoc.getElementsByTagName('LIGO_LW')
        for array in arrays:
            if not hasattr(array, 'Name'):
                continue
            if array.Name == 'COMPLEX8TimeSeries':
                array.childNodes[0].pcdata += delta_time


def etree_find(root: _ElementTree, path: str) -> _Element:
    """Returns an element in an xml document, or raise an error if not found.

    Parameters:
        root: The xml document.
        path: The specification path to the element.

    Raises:
        ValueError: When the element specified by the path is not specified in document.
    """
    element = root.find(path)
    if element is None:
        raise ValueError(f'No element specified by {path!r} in the xml document.')
    return element


class ExternalEventCreator(GEventCreator):
    """Creator of G-event for External group pipelines."""

    @staticmethod
    def _shift_original_data(raw_data: bytes, delta_time: float) -> bytes:
        buffer = BytesIO(raw_data)
        root = etree.parse(buffer)
        ExternalEventCreator._shift_original_document(root, delta_time)
        return etree.tostring(root, xml_declaration=True, pretty_print=True)

    @staticmethod
    def _shift_original_document(root: _ElementTree, delta_time: float) -> None:
        for tag in [
            './Who/Date',
            './WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime',  # noqa: E501
        ]:
            element = etree_find(root, tag)
            original_gps_time = Time(element.text, format='isot').gps
            new_gps_time = original_gps_time + delta_time
            new_isot_time = Time(new_gps_time, format='gps', scale='utc').isot
            element.text = str(new_isot_time)


def filter_uploads_unless(
    uploads: list[Upload], include_all_files: bool
) -> list[Upload]:
    """Optionally remove uploads of lesser importance.

    This function optionally filters out the uploads of PNG files or files without one
    of the tags: 'p_astro', 'psd' and 'sky_loc'. The initial upload is always included.

    Parameters:
        uploads: The event uploads.
        include_all_files: If true, the filtering is not performed, otherwise the
            filtering is performed.
    """
    if include_all_files:
        return uploads
    return filter_uploads(uploads)


def filter_uploads(uploads: list[Upload]) -> list[Upload]:
    """Remove uploads of lesser importance.

    This function filter out all the PNG files
    and do not filters out uploads:
    - with one of the tags: 'em_bright', 'p_astro' and 'sky_loc'.
    - if the file name contains the string 'p_astro.json'
    The initial upload is always included.

    Parameters:
        uploads: The event uploads.
    """
    required_tags = {'em_bright', 'p_astro', 'sky_loc'}
    new_uploads = [uploads[0]]

    for upload in uploads[1:]:
        filename, _ = split_filename(upload.filename)
        if filename.endswith('.png'):
            continue
        elif upload.tags & required_tags:
            pass
        elif 'p_astro.json' in filename:
            pass
        elif filename == 'amplfi.posterior_samples.hdf5':
            pass
        else:
            continue
        new_uploads.append(upload)

    return new_uploads


PIPELINE_GEVENT_CREATOR_CLASSES = {
    # CBC pipelines
    'gstlal': CBCEventCreator,
    'MBTA': CBCEventCreator,
    'MBTAOnline': CBCEventCreator,
    'pycbc': CBCEventCreator,
    'spiir': CBCEventCreator,
    'PyGRB': CBCEventCreator,
    'aframe': AframeEventCreator,
    # Burst pipelines
    'CWB': CWBEventCreator,
    'oLIB': oLIBEventCreator,
    'MLy': MLyEventCreator,
    # 'MLy': MLyEventCreator,
    # External events pipelines Group=External
    'Fermi': ExternalEventCreator,
    'Swift': ExternalEventCreator,
    'SNEWS': ExternalEventCreator,
    'INTEGRAL': ExternalEventCreator,
    'AGILE': ExternalEventCreator,
}
