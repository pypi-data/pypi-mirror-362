"""Classes for downloading and caching GraceDB G-events and S-Events."""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from tempfile import mkdtemp
from typing import Any, cast

import urllib3
from apischema import serialize
from requests import HTTPError

from .exceptions import MEGIgnoreEventError
from .gracedbs import GraceDBAlias, GraceDBWithContext
from .models import GEventDescription, SEventDescription, Upload

__all__ = [
    'GEventFetcher',
    'SEventFetcher',
]

logger = logging.getLogger(__name__)

DEFAULT_SOURCE_GRACEDB = GraceDBAlias.PRODUCTION
EMFOLLOW_REGEX = re.compile(
    r'(Log File Created|Coinc Table Created|.* created by GraceDbPlotter)$'
)


@dataclass
class GEventFetcher:
    """Class to fetch and store files associated to a G-event.

    Attributes:
        gevent: The G-event, as returned by GraceDB.
        path: The directory where the event files will be stored.
        gracedb: The GraceDB client instance used for the queries.
    """

    gevent: dict[str, Any]
    source: GraceDBWithContext
    path: Path

    @property
    def id(self) -> str:
        """Returns the G-event GraceDB identifier."""
        return cast(str, self.gevent['graceid'])

    @classmethod
    def from_id(
        cls,
        gevent_id: str,
        source: GraceDBWithContext,
        path: Path,
    ) -> GEventFetcher:
        """The GEventFetcher factory.

        Return the GEventFetcher associated to an event id.

        Parameters:
            gevent_id: The G-event GraceDB identifier.
            source: The GraceDB client from which events are downloaded.
            path: The directory where the event files will be stored.
        """
        gevent = source.event(gevent_id).json()
        return GEventFetcher(gevent, source, path)

    def fetch(self) -> None:
        """Download all the information required to re-create the event.

        The files are first written in a temporary directory, and this directory
        is renamed into the G-event identifier only upon success, in order to avoid
        dealing with incomplete downloads.
        """
        self.path.mkdir(exist_ok=True)
        tmp_path = Path(mkdtemp(dir=self.path))
        try:
            self._fetch_no_cleanup(tmp_path)

            target = self.path / self.id
            if target.exists():
                shutil.rmtree(target)
            os.rename(tmp_path, target)
        except BaseException:
            shutil.rmtree(tmp_path)
            raise

    def _fetch_no_cleanup(self, tmp_path: Path) -> None:
        description = self._get_description()
        self._store_description(description, tmp_path)
        filenames = [_.filename for _ in description.uploads]
        self._store_files(tmp_path, filenames)

    def _get_description(self) -> GEventDescription:
        description = GEventDescription(
            id=self.id,
            source=self.source.meg_alias or self.source.meg_url,
            pipeline=self.gevent['pipeline'],
            group=self.gevent['group'],
            search=self.gevent['search'],
            offline=self.gevent['offline'],
            gpstime=self.gevent['gpstime'],
            reporting_latency=self.gevent['reporting_latency'],
            uploads=self._get_uploads(),
            superevent=self.gevent['superevent'] if self.gevent['superevent'] else '',
            far=self.gevent['far'],
        )
        return description

    def _store_description(self, description: GEventDescription, path: Path) -> None:
        """Cache the G-event description as a json file.

        This file contains all the information to re-create an event.
        """
        description_path = path / 'description.json'
        description_path.write_text(json.dumps(serialize(description), indent=4))

    def _get_uploads(self) -> list[Upload]:
        full_logs = self._get_logs()
        logs = self._filter_logs(full_logs)
        if not logs:
            raise MEGIgnoreEventError(
                f'No pipeline logs for the event {self.id!r}:\n'
                f'{chr(13).join(str(_) for _ in full_logs)}'
            )
        t0 = self._convert_created(logs[0]['created'])
        return [self._get_upload(log, t0) for log in logs]

    def _get_upload(self, log: dict[str, Any], t0: datetime) -> Upload:
        delay = (self._convert_created(log['created']) - t0).total_seconds()
        # check uploads sanity (show a message if delay > 60s)
        if delay > 60:
            logger.info(
                f'--> Delay for "{log["filename"]},{log["file_version"]}"'
                f' is {delay}.'
            )
        upload = Upload(
            message=log['comment'],
            tags=log['tag_names'],
            filename=f'{log["filename"]},{log["file_version"]}',
            delay=delay,
        )
        return upload

    def _get_logs(self) -> list[dict[str, Any]]:
        """Return the event logs."""
        response = self.source.logs(self.id)
        response.raise_for_status()
        response_logs = response.json()
        if response_logs['links']['first'] != response_logs['links']['last']:
            raise NotImplementedError('Logs are paginated.')
        logs: list[dict[str, Any]] = response_logs['log']
        return logs

    def _filter_logs(self, logs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter out logs not issued by the pipeline.

        The discarded logs are those:
        - with no file
        - not issued by the pipeline
        - issued by 'emfollow' except for the first upload
        - with a comment such as 'Log File Created', 'Coinc Table Created' or
            '... created by GraceDbPlotter'.

        Parameters:
            logs: The list of logs associated to the current event as returned by
                GraceDB.
        """
        filtered_logs = [
            _
            for _ in logs
            if _['file']
            and _['issuer'] == self.gevent['submitter']
            and not (_['issuer'] == 'emfollow' and _['N'] > 1)
            and not EMFOLLOW_REGEX.match(_['comment'])
        ]
        return filtered_logs

    @staticmethod
    def _convert_created(dt: str) -> datetime:
        """Convert the log's field 'created' into a datetime.

        Parameters:
            dt: The time string, as returned by GraceDB.

        Example:
            >>> GEventFetcher._convert_created('2020-02-25 06:04:45 UTC')
            datetime.datetime(2020, 2, 25, 5, 4, 45, tzinfo=datetime.timezone.utc)
        """
        return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S UTC').astimezone(timezone.utc)

    def _store_files(self, path: Path, filenames: list[str]) -> None:
        """Fetch and cache the event's files required to re-generate it.

        Parameters:
            path: The path of the directory where the files will be stored.
            filenames: The file names to be downloaded and stored.
        """
        for filename in filenames:
            self._store_file(path, filename)

    def _store_file(self, path: Path, filename: str) -> None:
        """Fetch and cache an event file.

        Parameters:
            path: The path of the directory where the file will be stored.
            filename: The file name to be downloaded and stored.

        Raises:
            ValueError: When the file does not exist for the current event.
        """
        try:
            response = self.source.files(self.id, filename)
        except HTTPError as exc:
            if exc.response.status != 404:  # type: ignore[attr-defined,union-attr]
                raise
            if filename.endswith('.gz'):
                self._store_file(path, filename[:-3])
                return
            raise ValueError(f'G-event {self.id}: File {filename!r} not found.')

        assert isinstance(response, urllib3.response.HTTPResponse)
        (path / filename).write_bytes(response.read())


@dataclass
class SEventFetcher:
    """Class to fetch and store files associated to a super event.

    Attributes:
        sevent: The S-event, as returned by GraceDB.
        path: The directory where the event files will be stored.
        gracedb: The GraceDB client instance used for the queries.
    """

    sevent: dict[str, Any]
    source: GraceDBWithContext
    path: Path

    @property
    def id(self) -> str:
        """Returns the S-event GraceDB identifier."""
        return cast(str, self.sevent['superevent_id'])

    @classmethod
    def from_id(
        cls,
        sevent_id: str,
        source: GraceDBWithContext,
        path: Path,
    ) -> SEventFetcher:
        """The SEventFetcher factory.

        Return the SEventFetcher associated to a super event id.

        Parameters:
            sevent_id: The S-event GraceDB identifier.
            source: The GraceDB client from which events are downloaded.
            path: The directory where the event files will be stored.
        """
        sevent = source.superevent(sevent_id).json()
        return SEventFetcher(sevent, source, path)

    def fetch(self) -> None:
        """Download all the information required to re-create the super-event.

        The files are first written in a temporary directory, and this directory
        is renamed into the G-event identifier only upon success, in order to avoid
        dealing with incomplete downloads.
        """
        self.path.mkdir(exist_ok=True)
        tmp_path = Path(mkdtemp(dir=self.path))
        try:
            self._fetch_no_cleanup(tmp_path)

            target = self.path / self.id
            if target.exists():
                shutil.rmtree(target)
            os.rename(tmp_path, target)
        except BaseException:
            shutil.rmtree(tmp_path)
            raise

    def _fetch_no_cleanup(self, tmp_path: Path) -> None:
        description = self._get_description()
        valid_ids = []
        for gevent_id in description.gevent_ids:
            fetcher = GEventFetcher.from_id(gevent_id, self.source, tmp_path)
            if fetcher.gevent['offline']:
                continue
            logger.info(f'Downloading {gevent_id}...')
            try:
                fetcher.fetch()
            except MEGIgnoreEventError as exc:
                logger.warning(f'Aborting {gevent_id}: {exc}')
                continue
            valid_ids.append(gevent_id)

        description.gevent_ids = valid_ids
        self._store_description(description, tmp_path)

    def _get_description(self) -> SEventDescription:
        # full_logs = self.source.logs(self.id).json()
        # full_labels = self.source.labels(self.id).json()
        # gevent_data = {id: self.source.event(id).json() for id in gevent_ids}
        gevent_ids = self.sevent['gw_events']
        description = SEventDescription(
            id=self.id,
            source=self.source.meg_alias or self.source.meg_url,
            t_start=self.sevent['t_start'],
            t_0=self.sevent['t_0'],
            t_end=self.sevent['t_end'],
            gevent_ids=gevent_ids,
            # sevent_data={
            #    'sevent': self.sevent,
            #    'logs': full_logs,
            #    'labels': full_labels['labels'],
            #    'gevents': gevent_data,
            # },
        )
        return description

    def _store_description(self, description: SEventDescription, path: Path) -> None:
        """Cache the description as a JSON file."""
        description_path = path / 'description.json'
        description_path.write_text(json.dumps(serialize(description), indent=4))
