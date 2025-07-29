"""Classes for G-event and S-event validation."""

from __future__ import annotations

import io
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import astropy
import astropy.coordinates
import matplotlib.pyplot as plt  # type: ignore[attr-defined]
import mocpy
import numpy as np
from astropy.time import Time
from matplotlib import colormaps  # type: ignore[attr-defined]
from requests import HTTPError

from .alert_conditions import (
    get_mchirp,
    get_snr,
    is_complete,
    is_significant,
    should_publish,
)
from .analize_utils import AnalizeLogsSuperEvents, AnalizePipelinesSEvents
from .cache import GEventCacheEntry, SEventCacheEntry
from .exceptions import MEGValidationFailed
from .gracedbs import GraceDBWithContext

# import astropy_healpix
# import healpy
# import mocpy


logger = logging.getLogger(__name__)

# Files and Labels that should be present for MDC test event checklist

FILES_CHECKLIST_MDC = [
    'bayestar.multiorder.fits',
    'bayestar.fits.gz',
    'bayestar.png',
    'bayestar.volume.png',
    'bayestar.html',
    '{}.p_astro.json',
    '{}.p_astro.png',
    'em_bright.json',
    'em_bright.png',
]

LABELS_CHECKLIST_MDC = [
    'EMBRIGHT_READY',
    'GCN_PRELIM_SENT',
    'PASTRO_READY',
    'SKYMAP_READY',
    'DQR_REQUEST',
]

ADV_LABELS = ['ADVNO', 'ADVOK', 'ADVREQ']


class SEventValidator(SEventCacheEntry):
    """Class used to validate a cached S-event."""

    datetime_format = '%Y-%m-%d %H:%M:%S %Z'
    cmap = colormaps['tab10']
    data_template = {'found': False, 'time': 'never', 'latency': 9999.0}
    loginfo = True

    # --------------------------------------------------------------------------
    # -  self.labels_dictMDC      : Labels check from MDC label checklist
    # -  self.files_dictMDC       : File checks from MDC files checklist
    # -  self.history_properties  : [kind][ [latency,description,log] ....]
    # -  self.history_alerts      : [kind][ [latency,type,file,vers,log#] ....]
    # -  self.history_dataproducts: [kind][ [latency,file,vers,comment,log#] ...]
    # -  self.dataproducts        : (binary) of dataproductw [kind]['filename,vers']
    # -  self.dataalerts          : (binary) of alerts       [kind]['filename,vers']
    # -  self.datalocalizations   : (binary) of events localizations [GEV]
    # -  self.filelocalizations   : Filename of events localizations [GEV]
    # --------------------------------------------------------------------------
    history_properties: dict[str, Any]
    history_alerts: dict[str, Any]
    history_dataproducts: dict[str, Any]
    dataproducts: dict[str, Any]
    dataalerts: dict[str, Any]
    datalocalizations: dict[str, Any]
    filelocalizations: dict[str, str]

    @classmethod
    def from_sevent_id(
        cls,
        sevent_id: str,
        source: GraceDBWithContext,
        disabled: bool,
        cache_path: Path,
    ) -> SEventValidator:
        """Init from S-event id.

        Fetches S-event and returns a validator instance.

        Parameters:
            sevent_id: The S-event GraceDB identifier.
            source: The GraceDB instance name from which events are downloaded,
                such as `production` or `playground`.
            disabled: If true, bypass the cache and always download the event
                data files.
            cache_path: The top-level path of the cache.
        """
        SEventCacheEntry.from_id(sevent_id, source, disabled, cache_path)

        return SEventValidator(cache_path / sevent_id)

    @classmethod
    def from_gevent_id(
        cls,
        gevent_id: str,
        source: GraceDBWithContext,
        disabled: bool,
        cache_path: Path,
    ) -> SEventValidator:
        """Init from G-event id.

        Fetches G-event info, queries for S-events in the corresponding
        search and returns a validator instance for the S-event associated to
        the input G-event.

        Parameters:
            gevent_id: The G-event GraceDB identifier.
            source: The GraceDB instance name from which events are downloaded,
                such as `production` or `playground`.
            disabled: If true, bypass the cache and always download the event
                data files.
            cache_path: The top-level path of the cache.

        Raises:
            RuntimeError: When the input G-event does not have ans associated
                S-event.
        """
        gevent_data = GEventCacheEntry.from_id(
            gevent_id, source, disabled, cache_path
        ).get_description()
        sevent_id = gevent_data.superevent
        if sevent_id != '':
            logger.info(f'Validating parent S-event {sevent_id} of G-event {gevent_id}')
            return SEventValidator.from_sevent_id(
                sevent_id, source, disabled, cache_path
            )
        else:
            err_str = (
                f'G-event {gevent_id} do not belong to an S-event. Validation Failed'
            )
            logger.info(err_str)
            raise MEGValidationFailed(err_str)

    def _get_labels(self) -> dict[str, Any]:
        """Load labels info into a dictionary."""
        logs = self.sevent_data['labels']
        labels_dictMDC = {
            key: self.data_template.copy() for key in LABELS_CHECKLIST_MDC + ADV_LABELS
        }
        for row in logs:
            labelname = row['name']
            log_time = datetime.strptime(row['created'], self.datetime_format)
            # logger.info(f'Label {labelname} created {str(log_time)}')
            if labelname in LABELS_CHECKLIST_MDC + ADV_LABELS:
                labels_dictMDC[labelname]['found'] = True
                labels_dictMDC[labelname]['time'] = str(log_time)
                labels_dictMDC[labelname]['latency'] = [(Time(log_time).gps - self.t_0)]

        return labels_dictMDC

    def _get_files(self) -> dict[str, Any]:
        """Load files info into a dictionary."""
        logs = self.sevent_data['logs']['log']
        files_dictMDC: dict[str, dict[str, Any]]
        files_dictMDC = {
            key.format(self.pipeline): self.data_template.copy()
            for key in FILES_CHECKLIST_MDC
        }
        for filename in files_dictMDC:
            files_dictMDC[filename]['latency'] = []
        for row in logs:
            filename = row['filename']
            log_time = datetime.strptime(row['created'], self.datetime_format)
            if filename:
                pass
                # logger.info(f'File {filename} created {str(log_time)}')
            if filename in files_dictMDC:
                files_dictMDC[filename]['found'] = True
                files_dictMDC[filename]['time'] = str(log_time)
                files_dictMDC[filename]['latency'].append(Time(log_time).gps - self.t_0)

        return files_dictMDC

    def _get_file_dataproduct_ev(
        self, filename: str, ev: str, filename_path: Path
    ) -> bytes:
        """Get content of a files from the mag cache.

        If the data do not exist retive them from GraceDB.

        Parameters:
            ev: The event GraceDB identifier.
            filename: The name of the file to download
            filename_path: The path to the cached file.
        """
        if filename_path.exists():
            filename_data = filename_path.read_bytes()
            return filename_data

        # Check if the cache directory is present. Create if not.
        if filename_path.parents[1].exists() and not filename_path.parents[0].exists():
            logger.info(
                f'Base dir exist {str(filename_path.parents[1])} creating subdir'
            )
            filename_path.parents[0].mkdir(parents=True, exist_ok=True)

        # Download data from GraceDB, save in the meg cache and ruturn values.
        source = GraceDBWithContext.meg_from_alias_or_url(self.get_description().source)
        try:
            response = source.files(ev, filename)
            logger.info(f'Event {ev}: File {filename!r} found!')
            filename_data = response.read()
        except HTTPError as exc:
            if exc.response.status != 404:  # type: ignore[attr-defined,union-attr]
                raise exc
            logger.info(f'Event {ev}: File {filename!r} not found!')
            raise ValueError(f'Event {ev}: File {filename!r} not found.')
        try:
            filename_path.write_bytes(filename_data)
        except FileNotFoundError:
            logger.info(f'Data can not be saved to {str(filename_data)}')

        return filename_data

    def _get_sevent_history_data(self) -> None:
        """Create history entry in the SEventValidator class.

        Expect: [defined by _get_sevent_history(self)]
        -  self.history_properties  : [kind][ [latency,description,log] ....]
        -  self.history_alerts      : [kind][ [latency,type,file,vers,log#] ....]
        -  self.history_dataproducts: [kind][ [latency,file,vers,comment,log#] ...]
        Return:
        -  self.dataproducts        : (binary) of dataproductw [kind]['filename,vers']
        -  self.dataalerts          : (binary) of alerts       [kind]['filename,vers']
        -  self.datalocalizations   : (binary) of events localizations [GEV]
        -  self.filelocalizations   : fileename of events localizations [GEV]
        """
        # GET DATA PRODUCTS
        self.dataproducts = dict()
        for dataproduct in self.history_dataproducts:
            self.dataproducts[dataproduct] = dict()
            dataproducts = self.history_dataproducts[dataproduct]
            for elem in dataproducts:
                filename = elem[1] + ',' + str(elem[2])
                filename_path = self.path / filename
                filename_data = self._get_file_dataproduct_ev(
                    filename, self.sevent_id, filename_path
                )
                self.dataproducts[dataproduct][filename] = filename_data

        # GET DATA ALERTS
        self.dataalerts = dict()
        for dataproduct in self.history_alerts:
            self.dataalerts[dataproduct] = dict()
            dataproducts = self.history_alerts[dataproduct]
            for elem in dataproducts:
                filename_alert = elem[2] + ',' + str(elem[3])
                filename_path = self.path / filename_alert
                filename_data = self._get_file_dataproduct_ev(
                    filename_alert, self.sevent_id, filename_path
                )
                self.dataalerts[dataproduct][filename_alert] = filename_data

        # GET EVENTS LOCALIZATIONS
        self.datalocalizations = dict()
        self.filelocalizations = dict()
        for gev_id in self.sevent_data['sevent']['gw_events']:
            data_event = self.sevent_data['gevents'][gev_id]
            group_event = data_event['group'].lower()
            pipeline_event = data_event['pipeline'].lower()
            labels_event = data_event['labels']
            try:
                if group_event == 'cbc' and 'SKYMAP_READY' in labels_event:
                    localization = 'bayestar.multiorder.fits,0'
                    filename_path = self.path / gev_id / localization
                    filename_data = self._get_file_dataproduct_ev(
                        localization, gev_id, filename_path
                    )
                elif group_event == 'burst' and 'SKYMAP_READY' in labels_event:
                    localization = pipeline_event + '.multiorder.fits,0'
                    filename_path = self.path / gev_id / localization
                    filename_data = self._get_file_dataproduct_ev(
                        localization, gev_id, filename_path
                    )
                else:
                    filename_data = b''
            except ValueError:
                logger.info(f'Event {gev_id}: is invalid! File {localization} missing.')
                filename_data = b''
            self.datalocalizations[gev_id] = filename_data
            self.filelocalizations[gev_id] = str(filename_path)

    def _get_sevent_history(self) -> None:
        """Create history entry in the SEventValidator class.

        Return:
        -  self.labels_dictMDC      : to be removed used for MDC checklist
        -  self.files_dictMDC       : to be removed used for MDC checklist
        -  self.history_properties  : [kind][ [latency,description,log] ....]
        -  self.history_alerts      : [kind][ [latency,type,file,vers,log#] ....]
        -  self.history_dataproducts: [kind][ [latency,file,vers,comment,log#] ...]
        """
        # Get list of files and label in MDC checklist
        self.labels_dictMDC = self._get_labels()
        self.files_dictMDC = self._get_files()

        # Get history of S-event
        history_data = AnalizeLogsSuperEvents(self.sevent_data['logs']['log'], self.t_0)
        self.history_properties = history_data[0]
        self.history_alerts = history_data[1]
        self.history_dataproducts = history_data[2]
        # Get properties G-events and groups
        self.group_events, self.group_fars = AnalizePipelinesSEvents(
            self.sevent_data['sevent'], self.sevent_data['gevents'], log=False
        )

    def validate(self, save_plot_to: Path | None) -> None:
        """Superevent validation method.

        Get S-event description, recover labels and file info,
        validate and produce a plot.

        Raises:
            RuntimeError: When the validation fails.
        """
        self.source = GraceDBWithContext.meg_from_alias_or_url(
            self.get_description().source
        )
        self.id = self.get_description().id
        self.t_start = self.get_description().t_start
        self.t_0 = self.get_description().t_0
        self.t_end = self.get_description().t_end
        self.gevent_ids = self.get_description().gevent_ids
        logger.info(
            'Validating {} from graceDB {} in {}'.format(
                self.id, str(self.get_description().source), str(self.path)
            )
        )
        validation_data_filename = self.path / str(self.id + '_validation_data.json')
        if validation_data_filename.exists():
            logger.info(
                f'Getting validation S-event data from {str(validation_data_filename)}'
            )
            with open(validation_data_filename) as stream:
                sevent_data = json.load(stream)
        else:
            sevent = self.source.superevent(self.id).json()
            full_logs = self.source.logs(self.id).json()
            full_labels = self.source.labels(self.id).json()
            gevent_data = {
                id: self.source.event(id).json() for id in sevent['gw_events']
            }
            # Download gevents logs
            for gid in gevent_data:
                gevent_data[gid]['logs'] = self.source.logs(gid).json()
            # Construct the full sevent_data dictionary
            sevent_data = {
                'sevent': sevent,
                'logs': full_logs,
                'labels': full_labels['labels'],
                'gevents': gevent_data,
            }
            with open(validation_data_filename, 'w') as stream:
                json.dump(sevent_data, stream, indent=4)
            logger.info(
                f'Validation S-event data saved to {str(validation_data_filename)}'
            )

        self.sevent_data = sevent_data
        self.sevent_id = self.sevent_data['sevent']['superevent_id']
        self.sub_time = datetime.strptime(
            self.sevent_data['sevent']['created'], self.datetime_format
        )
        logger.info(
            'Validating {} submitted {} from graceDB {}'.format(
                self.id, str(self.sub_time), str(self.get_description().source)
            )
        )

        # GET SEVENT MAIN PRODUCTS
        self.sev_values = self.sevent_data['sevent']
        self.gev_values = self.sevent_data['sevent']['preferred_event_data']
        self.group = self.gev_values['group'].lower()
        self.pipeline = self.gev_values['pipeline'].lower()
        self.search = self.gev_values['search'].lower()
        self.superevent_id = self.sev_values['superevent_id']
        self.is_significant = is_significant(self.gev_values)
        self.is_earlywaring = 'EARLY_WARNING' in self.sevent_data['sevent']['labels']
        self.is_raven = 'RAVEN_ALERT' in self.sevent_data['sevent']['labels']
        self.is_cbc = (
            'cbc' == self.sevent_data['sevent']['preferred_event_data']['group'].lower()
        )
        self.is_mdc = (
            'mdc'
            == self.sevent_data['sevent']['preferred_event_data']['search'].lower()
        )
        self.should_publish = should_publish(self.gev_values)

        logger.info(f'Event {self.sevent_id} is_significant is {self.is_significant}')
        logger.info(f'Event {self.sevent_id} should_publish is {self.should_publish}')
        logger.info(f'Event {self.sevent_id} is cbc {self.is_cbc}')
        logger.info(f'Event {self.sevent_id} is mdc {self.is_mdc}')
        logger.info(f'Event {self.sevent_id} is EARLY_WARNING {self.is_earlywaring}')
        logger.info(f'Event {self.sevent_id} is RAVEN {self.is_raven}')

        # Get SEVENT history and data
        self._get_sevent_history()
        self._get_sevent_history_data()

        # #################################
        # Perform validation checks
        # #################################

        validation_tests: list[str] = []

        # TEST G-events completness
        current_validation = self._validate_g_events()
        if len(current_validation) > 0:
            validation_tests = validation_tests + current_validation
        else:
            logger.info('G-events completness validation OK.')

        # TESTs advocate action are requested
        if self.is_significant:
            current_validation = self._validate_advocate()
            if len(current_validation) > 0:
                validation_tests = validation_tests + current_validation
            else:
                logger.info(f'S-event {self.sevent_id} advocate validation OK.')

        # Checks that apply to CBC Alerts (From the MDC checklist)
        if self.is_significant and self.is_cbc and not self.is_earlywaring:
            current_validation = self._validate_labels() + self._validate_files()
            if len(current_validation) > 0:
                validation_tests = validation_tests + current_validation
            else:
                logger.info(f'S-event {self.sevent_id} MDC-CBC checklist OK.')
        else:
            logger.info(f'S-event {self.sevent_id} MDC-CBC checks not performed.')

        # Check the number of alerts.
        current_validation = self._validate_number_of_alerts()
        if len(current_validation) > 0:
            validation_tests = validation_tests + current_validation
        else:
            logger.info(f'S-event {self.sevent_id} has the expected # of alerts.')

        # -------------------------------------
        # Ouput infos to the appropriate files
        # -------------------------------------
        if not save_plot_to:
            save_plot_to = self.path

        if self.loginfo:
            self._save_analize_sev_history(save_plot_to)
            self._save_data(save_plot_to)
            self._plot(save_plot_to)

        if len(validation_tests) > 0:
            n_failed_test = len(validation_tests)
            logger.info(
                f'Validation of S-event {self.sevent_id} failed {n_failed_test} tests:'
            )
            err_str = f'Validation failed for S-event {self.sevent_id}\n'
            for i, validation_test in enumerate(validation_tests):
                logger.info(f'[{i:2}] {validation_test}')
                err_str = err_str + validation_test + '\n'
            raise MEGValidationFailed(err_str)
        else:
            logger.info(f'S-event {self.sevent_id} verified validation tests!')

    def _validate_g_events(self) -> list[str]:
        """Validate that all required G_events are complete."""
        current_validation = []
        for gev_id in self.sevent_data['sevent']['gw_events']:
            data_event = self.sevent_data['gevents'][gev_id]
            if not is_complete(data_event):
                current_validation.append(
                    'GEV: {} ({}-{}) is not complete.'.format(
                        gev_id, data_event['pipeline'], data_event['search']
                    )
                )
        return current_validation

    def _validate_number_of_alerts(self) -> list[str]:
        """Check that we have the correct number of alerts.

        Checks:
        - [0] should publish false (no preliminary alert)
        - [1] should publish and not early_warning (at least two preliminary)
        - [2] early_warnig (at least one earlywarning)
        - [3] advok at least one initial
        - [4] advno at least one retraction

        Return:
          validation : [] (empty list) if all tests are ok.
                       otherwise list of str descibing the failed checks.
        """

        def _count_alert(kind: str, alert_type: str = 'preliminary') -> int:
            count_prelimary_alerts = 0
            for alert in self.history_alerts[kind]:
                if alert[1] == alert_type:
                    count_prelimary_alerts += 1
            return count_prelimary_alerts

        def _count_label_applied(label_name: str) -> int:
            count_label_applied = 0
            for alert in self.history_properties['label']:
                if alert[1] == label_name:
                    count_label_applied += 1
            return count_label_applied

        validation: list[str] = []
        # - [0] should publish false (no preliminary alert)
        if (not self.should_publish) and _count_alert('xml', 'preliminary') > 0:
            validation = validation + [
                '{} XML preliminary alerts and should_publish is False.'.format(
                    _count_alert('xml', 'preliminary')
                )
            ]
        # - [1] should publish and not early_warning: at least two preliminary.
        if (
            self.should_publish
            and (not self.is_earlywaring)
            and _count_alert('xml', 'preliminary') < 2
        ):
            validation = validation + [
                'Number of XML preliminary alert is {} (less than two).'.format(
                    _count_alert('xml', 'preliminary')
                )
            ]

        # - [2] early_warnig: at least one earlywarning.
        if self.is_earlywaring and _count_alert('xml', 'earlywarning') == 0:
            validation = validation + ['Missing EarlyWarning alert']
        return validation

        # - [3] advok applied: at least one initial.
        if _count_label_applied('ADVOK') > 0 and _count_alert('xml', 'initial') == 0:
            validation = validation + [
                'ADVOK has been applied and Initial alert is missing'
            ]

        # - [4] advno applied: at least one retraction.
        if _count_label_applied('ADVNO') > 0 and _count_alert('xml', 'retraction') == 0:
            validation = validation + [
                'ADVNO has been applied and Retraction alert is missing'
            ]

        return validation

    def _validate_labels(self) -> list[str]:
        """Check is all labels in LABELS_CHECKLIST_MDC are applied.

        Return:
          validation : [] (empty list) if all tests are ok.
                       otherwise list of str descibing the failed checks.
        """
        validation: list[str] = []
        for key in LABELS_CHECKLIST_MDC:
            if not self.labels_dictMDC[key]['found']:
                validation.append(f'Missing labels: {key}')
        return validation

    def _validate_advocate(self) -> list[str]:
        """Check if an advocate label (either ADVOK, ADVNO or ADV_REQ) is present.

        Return:
          validation : [] (empty list) if all tests are ok.
                       otherwise list of str descibing the failed checks.
        """
        adv_created = [self.labels_dictMDC[key]['found'] for key in ADV_LABELS]
        if any(adv_created):
            validation = []
        else:
            validation = [f'Missing ADV label (either one of {ADV_LABELS}).']
        return validation

    def _validate_files(self) -> list[str]:
        """Check is all file prescribed by matching FILES_CHECKLIST_MDC are present.

        Return:
          validation : [] (empty list) if all tests are ok.
                       otherwise list of str descibing the failed checks.
        """
        validation: list[str] = []
        for key in self.files_dictMDC:
            if not self.files_dictMDC[key]['found']:
                validation.append(f'FILES_CHECKLIST_MDC: Missing File:{key}')
        return validation

    def _save_data(self, outdir: Path) -> None:
        """Saves latency data to json files..

        Parameters:
            outdir: Output directory.
        """
        data_dict = {
            'sub_time': str(self.sub_time),
            'labels_dictMDC': self.labels_dictMDC,
            'files_dictMDC': self.files_dictMDC,
            'superevent_id': self.sevent_id,
            't_0': self.t_0,
            'history_properties': self.history_properties,
            'history_alerts': self.history_alerts,
            'history_dataproducts': self.history_dataproducts,
            'sevent_data': self.sevent_data,
        }
        filename = outdir / ('%s_latency_data.json' % str(self.sevent_id))
        try:
            with open(filename, 'w') as stream:
                json.dump(data_dict, stream, indent=4)
            logger.info(f'Data saved to {str(filename)}')
        except FileNotFoundError:
            logger.info(f'Data can not be saved to {str(filename)}')

    def _plot(self, outdir: Path) -> None:
        """Plots timeline of label and filename creation.

        Parameters:
            outdir: Output directory.
        """
        self._init_figure()
        self._add_entries_to_plot(self.axes[0], self.labels_dictMDC)
        self._add_entries_to_plot(self.axes[1], self.files_dictMDC)
        self._add_history_alert_to_plot(self.axes[2], self.history_alerts)
        self._add_history_properties_to_plot(self.axes[3], self.history_properties)

        # x_span = (
        #    self.axes[0].get_xlim()[1]  # type: ignore[attr-defined]
        #    - self.axes[0].get_xlim()[0]  # type: ignore[attr-defined]
        # )  # type: ignore[attr-defined]
        # self.axes[0].set_xlim(  # type: ignore[attr-defined]
        #    self.axes[0].get_xlim()[0],  # type: ignore[attr-defined]
        #    self.axes[0].get_xlim()[1] + 0.2 * x_span,  # type: ignore[attr-defined]
        # )
        textstr = ''
        for key in ['superevent_id', 'category', 'submitter', 'created', 't_0']:
            textstr += '{}: {}\n'.format(key, self.sevent_data['sevent'][key])
        self.axes[1].text(  # type: ignore[attr-defined]
            0.70,
            0.05,
            textstr[:-2],
            fontsize=10,
            transform=self.axes[0].transAxes,  # type: ignore[attr-defined]
            va='bottom',
            ha='left',
            bbox={'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.6},
        )

        plt.tight_layout()  # type: ignore[attr-defined]
        plt.subplots_adjust(hspace=0)

        filename = outdir / ('%s_latency_plot.pdf' % str(self.sevent_id))
        try:
            plt.savefig(filename)
            logger.info(f'Plot saved to {str(filename)}')
        except FileNotFoundError:
            logger.info(f'Plot can not be saved to {str(filename)}')

    def _init_figure(self) -> None:
        """Init matplotlib objects."""
        plt.rc('font', size=10)  # type: ignore[attr-defined]
        self.fig = plt.figure(figsize=(10, 8))
        self.axes = []

        self.axes.append(self.fig.add_subplot(4, 1, 1))
        self.axes[0].grid(ls='--')  # type: ignore[call-arg]
        self.axes[0].set_ylim(0, 1)
        self.axes[0].set_xscale(  # type: ignore[attr-defined]
            'symlog', linthresh=60, base=60 * 60
        )
        self.axes[0].set_xticks([-10, 0, 10, 30, 60, 300, 60 * 60, 3600 * 24])
        self.axes[0].set_xticklabels(
            ['-10s', '0', '10s', '30s', '1min', '6min', '1h', '1day']
        )
        self.axes[0].tick_params(  # type: ignore[attr-defined]
            axis='both', labelbottom=False, left=False, labelleft=False
        )

        self.axes.append(
            self.fig.add_subplot(4, 1, 2, sharex=self.axes[0], sharey=self.axes[0])
        )
        self.axes[1].grid(ls='--')  # type: ignore[call-arg]
        self.axes[1].tick_params(  # type: ignore[attr-defined]
            axis='both', left=False, labelleft=False
        )
        self.axes.append(
            self.fig.add_subplot(4, 1, 3, sharex=self.axes[0], sharey=self.axes[0])
        )
        self.axes[2].grid(ls='--')  # type: ignore[call-arg]
        self.axes[2].tick_params(  # type: ignore[attr-defined]
            axis='both', left=False, labelleft=False
        )
        self.axes[2].set_xlabel(r'Seconds since t$_0$')
        self.axes.append(
            self.fig.add_subplot(4, 1, 4, sharex=self.axes[0], sharey=self.axes[0])
        )
        self.axes[3].grid(ls='--')  # type: ignore[call-arg]
        self.axes[3].tick_params(  # type: ignore[attr-defined]
            axis='both', left=False, labelleft=False
        )
        self.axes[3].set_xlabel(r'Seconds since t$_0$')

    def _add_history_alert_to_plot(
        self, ax: plt.Axes, history_alerts: dict[str, Any]
    ) -> None:
        """Adds alert history to a plot.

        Parameters:
            ax: instance of matplotlib Axes
            entries: dict as returned by AnalizeLogsSuperEvents(...)[1]
        """
        alerts_types = list(history_alerts)
        alert_colors = {
            'earlywarning': 'g',
            'preliminary': 'b',
            'initial': 'k',
            'retraction': 'r',
            'update': 'g',
        }
        for i, alerts_type in enumerate(alerts_types):
            ax.text(  # type: ignore[attr-defined]
                0, i * 0.2 + 0.2, f'alert type {alerts_type}'
            )
            for alerts_data in history_alerts[alerts_type]:
                item_latency = alerts_data[0]
                ax.plot(
                    [item_latency, item_latency],
                    [0, 1],
                    color=alert_colors[alerts_data[1]],
                )
                ax.plot(
                    item_latency,
                    i * 0.2 + 0.2,
                    marker='o',
                    color=alert_colors[alerts_data[1]],
                )
                ax.text(  # type: ignore[attr-defined]
                    item_latency,
                    i * 0.2 + 0.2,
                    f'  ({alerts_data[0]:4.1f})',
                    color=alert_colors[alerts_data[1]],
                    horizontalalignment='left',
                )

    def _add_history_properties_to_plot(
        self, ax: plt.Axes, history_properities: dict[str, Any]
    ) -> None:
        """Adds alert history to a plot.

        Parameters:
            ax: instance of matplotlib Axes
            entries: dict as returned by AnalizeLogsSuperEvents(...)[1]
        """
        colors = ['black', 'blue', 'magenta', 'red', 'orange', 'green']
        colors = colors + colors
        properties = ['lables', 'gcn_received', 'rlables']
        for i, properity in enumerate(properties):
            y_loc = i / len(properties) * 0.9 + 0.05
            for item_latency, item_description, _ in history_properities[properity]:
                ax.plot(
                    [item_latency, item_latency],
                    [0, y_loc],
                    color=colors[i],
                )
                ax.plot(
                    [item_latency],
                    [y_loc],
                    marker='o',
                    color=colors[i],
                )
                if i == 0 or i == 2:
                    show_text = f'{item_description} ({item_latency:4.1f})'
                else:
                    show_text = properity
                ax.text(  # type: ignore[attr-defined]
                    item_latency,
                    y_loc,
                    f'  ({item_latency:4.1f})',
                    color=colors[i],
                    horizontalalignment='left',
                )
                ax.text(  # type: ignore[attr-defined]
                    item_latency,
                    y_loc + 0.05,
                    show_text,
                    color=colors[i],
                    rotation=90,
                    fontsize=6,
                    horizontalalignment='center',
                    verticalalignment='bottom',
                )

    def _add_entries_to_plot(self, ax: plt.Axes, entries: dict[str, Any]) -> None:
        """Adds entries to a plot.

        Parameters:
            ax: instance of matplotlib Axes
            entries: dict as returned by self._get_labels() or self._get_files()
        """
        i = 0
        colors = ['black', 'blue', 'magenta', 'red', 'orange', 'green']
        colors = colors + colors
        for key, item in entries.items():
            y_loc = i / len(entries.keys()) * 0.9 + 0.05
            if item['found']:
                for item_latency in item['latency']:
                    # ax.axvline(
                    # item_latency, ls='-', color=colors[i]
                    # )  # type: ignore[call-arg]
                    ax.plot(
                        [item_latency, item_latency],
                        [0, 1],
                        color=colors[i],
                    )
                    ax.plot(
                        [item_latency],
                        [y_loc],
                        marker='o',
                        color=colors[i],
                    )
                    ax.text(  # type: ignore[attr-defined]
                        item_latency,
                        y_loc,
                        f'({item_latency:4.1f})  ',
                        color='black',
                        horizontalalignment='right',
                        verticalalignment='bottom',
                        fontsize=6,
                    )
                ax.plot(
                    [item['latency'][0], item['latency'][-1] + 15],
                    [y_loc, y_loc],
                    color=colors[i],
                )
                ax.text(  # type: ignore[attr-defined]
                    item['latency'][-1] + 17, y_loc, key, color=colors[i]
                )
            i += 1

    def _save_analize_sev_history(self, outdir: Path) -> None:
        """Saves the dump of AnalizeLogsSuperEvents and AnalizePipelinesSEvents.

        Parameters:
            outdir: Output directory.
        """
        filename = outdir / ('%s_analize_sev_history.txt' % str(self.sevent_id))

        dump_log_lines = []

        # -------------------------------
        # Ouput data event
        # -------------------------------
        # -------------------------------
        # Ouput log LABELS
        # -------------------------------
        dump_log_lines.append(
            '  ================== S-event        ============================'
        )

        dump_log_lines.append(
            '   superevent_id: {}'.format(self.sev_values['superevent_id'])
        )
        dump_log_lines.append('      preferd_id: {}'.format(self.gev_values['graceid']))
        dump_log_lines.append('           group: {}'.format(self.gev_values['group']))
        dump_log_lines.append(
            '        pipeline: {}'.format(self.gev_values['pipeline'])
        )
        dump_log_lines.append(f'  is_significant: {self.is_significant}')
        dump_log_lines.append(f'  should_publish: {self.should_publish}')

        # -------------------------------
        # Ouput log upload events
        # -------------------------------
        for history_index in ['added', 'prefered']:
            data_upload_events = self.history_properties[history_index]
            dump_log_lines.append(
                f'  ===== {history_index:8} EVENT HISTORY ================='
            )
            for data_upload_event in data_upload_events:
                id_event = data_upload_event[1]
                try:
                    data_event = self.sevent_data['gevents'][id_event]
                    snr_event = get_snr(data_event)
                    mchirp_event = get_mchirp(data_event)
                except KeyError:
                    data_event = {
                        'group': '--',
                        'pipeline': '--',
                        'search': '--',
                        'far': 0.0,
                    }
                    snr_event = 0.0
                    mchirp_event = 0.0
                    credible90 = 0.0

                # Should use the localization data in the field
                # --- self.datalocalizations[id_event]
                # print(id_event,self.filelocalizations[id_event] )
                # print(id_event,len(self.datalocalizations[id_event]))
                if len(self.datalocalizations.get(id_event, '')) > 0:
                    filepath = self.filelocalizations[id_event]
                    moc90 = mocpy.MOC.from_multiordermap_fits_file(
                        filepath, cumul_to=0.9
                    )
                    credible90 = moc90.sky_fraction
                    skymap_fits = astropy.io.fits.open(filepath)
                    LOGBCI = skymap_fits[1].header.get('LOGBCI', 0.0)
                    # import astropy_healpix as ah
                    # import astropy.units as u
                    # max_order = skymap_fits[1].header["MOCORDER"]
                    # data = skymap_fits[1].data
                    # uniq = data["UNIQ"]
                    # probdensity = data["PROBDENSITY"]
                    # level, ipix = ah.uniq_to_level_ipix(uniq)
                    # area = ah.nside_to_pixel_area(
                    #          ah.level_to_nside(level)).to_value(u.steradian)
                    # prob = probdensity * area
                    # moc90 = MOC.from_valued_healpix_cells(
                    #               uniq, prob, max_order, cumul_to=0.9)
                else:
                    credible90 = 0.0
                    LOGBCI = 0.0
                dump_log_lines.append(
                    ' {:8.1f}s ({:5.1f}s)  {:10} FAR={:8.3g} SNR={:5.2f} mchirp={:5.2f}'
                    ' sky90%= {:8.3f} deg2 LOGBCI={:5.2f} {}'.format(
                        data_upload_event[0],
                        data_event.get('reporting_latency', 0.0),
                        id_event,
                        data_event['far'],
                        snr_event,
                        mchirp_event,
                        credible90 * (360**2) / np.pi,
                        LOGBCI,
                        str((data_event['pipeline'], data_event['search'])),
                    )
                )
        # -------------------------------
        # Ouput log LABELS and tags
        # -------------------------------

        dump_log_lines.append(
            '  ==================  HISTORY ============================='
        )
        for kind in ['lables', 'rlables', 'gcn_received']:
            dump_log_lines.append(f'  ******** Property: {kind:15}  *******')
            data_lables = self.history_properties[kind]
            for data_lable in data_lables:
                dump_log_lines.append('  {:8.1f}s {:30} - log({})'.format(*data_lable))

        # -------------------------------
        # Ouput log G-events and groups
        # -------------------------------
        dump_log_lines.append(
            '  ==================     EVENTS TYPE   ============================'
        )
        for group_event in self.group_events:
            dump_log_lines.append(
                '  -- {:25} FAR={:8.3} : {}'.format(
                    str((group_event[0], group_event[1])),
                    np.min(self.group_fars[group_event]),
                    self.group_events[group_event],
                )
            )

        # -------------------------------
        # Ouput alert History
        # -------------------------------
        dump_log_lines.append(
            '  ==================    ALERT HISTORY    ============================'
        )
        for alert_kind in self.history_alerts:
            dump_log_lines.append(f'  KIND {alert_kind}')
            for alert in self.history_alerts[alert_kind]:
                dump_log_lines.append(
                    '{:10.1f}s {:15} {:36} - log({})'.format(
                        alert[0], alert[1], alert[2] + ',' + str(alert[3]), alert[4]
                    )
                )

        # -------------------------------
        # Ouput Data Product  History
        # -------------------------------
        dump_log_lines.append(
            '  ==================    DATA PRODUCTS HISTORY     ==================='
        )
        for alert_kind in self.history_dataproducts:
            dump_log_lines.append(f'  KIND {alert_kind}')
            for dataproduct in self.history_dataproducts[alert_kind]:
                dump_log_lines.append(
                    '{:10.1f}s file= {:30} ...{} - log({})'.format(
                        dataproduct[0],
                        dataproduct[1] + ',' + str(dataproduct[2]),
                        dataproduct[3][-12:],
                        dataproduct[4],
                    )
                )

        # -------------------------------
        # Ouput Data Product
        # -------------------------------
        dump_log_lines.append(
            '  ==================    DATA PRODUCTS  =============================='
        )
        dump_log_lines.append(f'  {list(self.dataproducts)}')
        for dataproduct in ['p_astro', 'em_bright', 'gwskynet']:
            dump_log_lines.append(f'  [{dataproduct}]')
            dataproducts = self.dataproducts[dataproduct]
            for data_filename in dataproducts:
                data_json = json.loads(dataproducts[data_filename])
                prop_keys = list(data_json)
                prop_keys.sort()
                out_string = ''
                for prop in prop_keys:
                    out_value = data_json[prop]
                    try:
                        out_string = f'{prop}={out_value:9.4g} ' + out_string
                    except ValueError:
                        out_string = out_string + f'{prop}={out_value}'
                dump_log_lines.append(f'  -- {data_filename:35} {out_string}')
        for dataproduct in ['multiorder']:
            dump_log_lines.append(f'  [{dataproduct}]')
            dataproducts = self.dataproducts[dataproduct]
            for data_filename in dataproducts:
                fitscontent = dataproducts[data_filename]
                moc90 = mocpy.MOC.from_multiordermap_fits_file(
                    self.path / data_filename, cumul_to=0.9
                )
                try:
                    skymap_fits = astropy.io.fits.open(io.BytesIO(fitscontent))
                    LOGBCI = skymap_fits[1].header['LOGBCI']
                except KeyError:
                    LOGBCI = 0
                dump_log_lines.append(
                    '  -- {:35} size={} sky90%={:7.5f} LOGBCI={:5.2f}'.format(
                        data_filename,
                        len(fitscontent),
                        moc90.sky_fraction,
                        LOGBCI,
                    )
                )

        dump_log_lines.append(
            '  ==================================================================='
        )
        if self.loginfo:
            for line in dump_log_lines:
                logger.info(line)

        try:
            with open(filename, 'w') as stream:
                stream.writelines(line + '\n' for line in dump_log_lines)
            logger.info(f'History saved to {str(filename)}')
        except FileNotFoundError:
            logger.info(f'History can not be saved to {str(filename)}')
