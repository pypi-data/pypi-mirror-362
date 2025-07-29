"""Utility to analize S-events.

Implement:
- AnalizeLogsSuperEvents(LOGS,t0)
- AnalizePipelinesSEvents(sev,gevs,log)
"""

import re
from datetime import datetime
from typing import Any

import numpy as np
from astropy.time import Time


def _convert_created(timestr: str) -> datetime:
    return datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S UTC')


def AnalizeLogsSuperEvents(
    LOGS: list[Any], t0: float = 0.0
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Analize the logs of a supervent to find out labels and alerts.

    Returns:
    - history_properties: list of (time-t0 , object)
       'initial'  : Event that create the super-event
       'added'    : Hystory of added event
       'prefered' : Hystory of prefered event changes
       'labels'   : History of the applyed labels
       'rlabels'  : History of the removes labels
    - history_alerts: list of (time-t0, kind ,filename, version)
       'xml'      : alerts as VO event
       'avro'     : alerts as avro over kafka to SCiMMA
       'json'     : alerts as json over kafka to GCN
       'txt'      : alerts as email text
    - history_dataproducts: list of (time-t0, kind ,filename, version)
       'multiorder' : multiorder skymap (*.multiorder.fits)
       'p_astro'    : p_astro data (*.pastro.json)
       'em_bright'  : em_bright data (*em_bright.json)
       'gwskynet'   : gwskynet annotation ()
       # Auxiliary data products (not in alerts)
       'posterior'  : Bilby posterior sample
       'flatten'    : flattened skymap (*.fits.gz)
    """
    history_properties: dict[str, Any] = dict()
    history_alerts: dict[str, Any] = dict()
    history_dataproducts: dict[str, Any] = dict()

    comment_match = {
        'initial': re.compile('Superevent created.*preferred_event=(\\S*)'),
        'added': re.compile('Added event: (\\S*)'),
        'prefered': re.compile('.*preferred_event: \\S\\d* -> (\\S\\d*).*'),
        'lables': re.compile(
            'Added label: (\\S*)|.*label (\\S*) applied', flags=re.DOTALL
        ),
        'rlables': re.compile('.*label (\\S*) removed.*', flags=re.DOTALL),
        'gcn_received': re.compile('Tagged message (\\d*): gcn_received'),
    }
    comments = [log['comment'] for log in LOGS]
    for kind in comment_match:
        history_properties[kind] = []
        for idx, comment in enumerate(comments):
            regout = comment_match[kind].match(comment)
            if regout:
                alert = ''
                for matchvalue in regout.groups():
                    if matchvalue is not None:
                        alert = matchvalue
                alerttime = Time(_convert_created(LOGS[idx]['created'])).gps - t0
                history_properties[kind].append([alerttime, alert, idx])
    # Join 'initial' to 'prefered' and 'added' history
    for history_event in ['added', 'prefered']:
        history_properties[history_event] = (
            history_properties['initial'] + history_properties[history_event]
        )
    # get and assoced the messagge associated to the tag history
    for history_tag in ['gcn_received']:
        for index, record in enumerate(history_properties[history_tag]):
            log_index = int(record[1]) - 1
            new_values = 'Tag[{:3}]:{:10}  ({},{})'.format(
                record[1],
                history_tag,
                LOGS[log_index]['filename'],
                LOGS[log_index]['file_version'],
            )
            history_properties[history_tag][index][1] = new_values
    alert_match = {
        'xml': re.compile('.*-\\d*-(\\S*).xml'),
        'json': re.compile('\\S\\d\\d\\d\\d\\d\\d\\S*-(\\S*).json'),
        'avro': re.compile('.*-(\\S*).avro'),
        'txt': re.compile('.*-\\d*-(\\S*).txt'),
    }
    fnames = [log['filename'] for log in LOGS]
    for kind in alert_match:
        history_alerts[kind] = []
        for idx, fname in enumerate(fnames):
            regout = alert_match[kind].match(fname)
            if regout:
                alert = regout.group(1)
                alerttime = Time(_convert_created(LOGS[idx]['created'])).gps - t0
                history_alerts[kind].append(
                    [
                        alerttime,
                        alert.lower(),
                        LOGS[idx]['filename'],
                        LOGS[idx]['file_version'],
                        idx,
                    ]
                )

    dataproducts_match = {
        'multiorder': re.compile('.*multiorder.fits'),
        'p_astro': re.compile('.*p_astro.json'),
        'em_bright': re.compile('.*em_bright.json'),
        'gwskynet': re.compile('.*gwskynet.json'),
        # Auxiliary data products (not in alerts)
        'posterior': re.compile('.*posterior_samples.hdf5'),
        'flatten': re.compile('.*fits.gz'),
        'png_p_astro': re.compile('.*p_astro.png'),
        'png_em_bright': re.compile('.*em_bright.png'),
    }
    fnames = [log['filename'] for log in LOGS]
    for kind in dataproducts_match:
        history_dataproducts[kind] = []
        for idx, fname in enumerate(fnames):
            regout = dataproducts_match[kind].match(fnames[idx])
            if regout:
                creation_time = Time(_convert_created(LOGS[idx]['created'])).gps - t0
                history_dataproducts[kind].append(
                    [
                        creation_time,
                        LOGS[idx]['filename'],
                        LOGS[idx]['file_version'],
                        LOGS[idx]['comment'],
                        idx,
                    ]
                )
        # print('KIND --- {}'.format(kind))
        # for data in alerts_properties[kind]:
        #    print(data)

    return history_properties, history_alerts, history_dataproducts


def AnalizePipelinesSEvents(
    sev: dict[str, Any], gevs: dict[str, Any], log: bool = False
) -> tuple[dict[tuple[Any, Any], Any], dict[tuple[Any, Any], Any]]:
    """Analize the the kind of events in a supervent.

    Returns two group dictionary with entry (pipeline,search) containing
    - group_events : the list of G-events in the group
    - group_fars   : the list of FAR of the G-events in the group.
    """
    gw_events = sev['gw_events']
    events_data = [gevs[evid] for evid in gw_events]
    events_far = np.array([ev['far'] for ev in events_data])
    # events_group = np.array([ev['group'] for ev in events_data])
    events_pipeline = np.array([ev['pipeline'] for ev in events_data])
    events_search = np.array([ev['search'] for ev in events_data])
    searches = set(events_search)
    pipelines = set(events_pipeline)
    group_events: dict[tuple[Any, Any], Any] = {}
    group_fars: dict[tuple[Any, Any], Any] = {}
    for search in searches:
        for pipeline in pipelines:
            count = np.where((events_search == search) * (events_pipeline == pipeline))[
                0
            ]
            if len(count) > 0:
                group_events[(pipeline, search)] = list(
                    np.array(sev['gw_events'])[count]
                )
                group_fars[(pipeline, search)] = events_far[count]

    if log:
        print(
            'sev {:10}  FAR {:.4}  #ev={}'.format(
                sev['superevent_id'], sev['far'], len(gw_events)
            )
        )
        print(f'  min FAR {np.min(events_far):6.4} max FAR {np.max(events_far):6.4}')
        for evset in group_events:
            count = group_events[evset]
            print(
                '  --- {:8} {:8} #{:2}  min FAR {:6.4} - {}'.format(
                    evset[0],
                    evset[1],
                    len(count),
                    np.min(group_fars[evset]),
                    group_fars[evset],
                )
            )
    return group_events, group_fars
