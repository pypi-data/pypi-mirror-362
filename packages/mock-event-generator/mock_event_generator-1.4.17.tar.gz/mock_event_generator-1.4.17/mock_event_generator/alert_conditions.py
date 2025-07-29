"""Utility and setting of the alert conditions.

To be used (in future in gwcelery)
Implement:
- is_significant(event: dict[str, Any]) -> bool
- is_comlete(event: dict[str, Any]) -> bool
- should_publish(event: dict[str, Any]) -> bool
- keyfunc(event: dict[str, Any]) -> Any)

- get_mchirp(event: dict[str, Any]) -> float
- get_snr(event: dict[str, Any]) -> float
- get_instruments(event: dict[str, Any]) -> set
- get_instruments_in_ranking_statistic(event: dict[str, Any]) -> set

- is_skymap_required(event: dict[str, Any]) -> bool
- is_p_astro_required(event: dict[str, Any]) -> bool
- is_em_bright_required(event: dict[str, Any]) -> bool

- check_alert_dictionaies_consistency() -> bool

Use the following configuration dictionary;
- significant_alert_far_thresholds : dict[tuple[str, str, str],float]
- preliminary_alert_far_thresholds : dict[tuple[str, str, str], float]
- required_labels_to_publish : dict[tuple[str, str, str], set[str]]

"""

from typing import Any

#######################################################################
# DEFINTION OF ALERT CONDITIONS DICTIONARIES --> do me moved to config
#######################################################################

superevent_candidate_preference: dict[tuple[str, str, str], float] = {
    # CBC AllSKy searches
    ('cbc', 'mbta', 'allsky'): 6,
    ('cbc', 'gstlal', 'allsky'): 6,
    ('cbc', 'pycbc', 'allsky'): 6,
    ('cbc', 'spiir', 'allsky'): 6,
    # CBC SSM searches
    ('cbc', 'mbta', 'ssm'): 5,
    ('cbc', 'gstlal', 'ssm'): 5,
    # ML AllSky searches
    ('cbc', 'aframe', 'allsky'): 4,
    # BURST BBH searches
    ('burst', 'cwb', 'bbh'): 4,
    # BURST AllSky searches
    ('burst', 'cwb', 'allsky'): 3,
    ('burst', 'olib', 'allsky'): 3,
    # CBC EarlyWarning searches
    ('cbc', 'mbta', 'earlywarning'): 2,
    ('cbc', 'gstlal', 'earlywarning'): 2,
    ('cbc', 'pycbc', 'earlywarning'): 2,
    ('cbc', 'spiir', 'earlywarning'): 2,
    # CBC MDC gstlal
    ('cbc', 'gstlal', 'mdc'): 1,
}
"""Group-Pipeline-Search preference for individual candidates. This is
used by :meth:`gwcelery.tasks.superevents.keyfunc` to sort
candidates for the preferred event before a ranking statistic is used."""

one_day = 1 / 3600 / 24
one_month = 1 / 3600 / 24 / 30
one_year = 1 / 3600 / 24 / 365
threshold_cbc = 2 * one_day
threshold_burst = one_month / 4

trial_factor_cbc = 7.0
trial_factor_burst = 4.0
threshold_cbc_significant = one_month / trial_factor_cbc
threshold_burst_significant = one_year / trial_factor_burst

significant_alert_far_thresholds: dict[tuple[str, str, str], float] = {
    # CBC AllSKy searches
    ('cbc', 'mbta', 'allsky'): threshold_cbc_significant,
    ('cbc', 'gstlal', 'allsky'): threshold_cbc_significant,
    ('cbc', 'pycbc', 'allsky'): threshold_cbc_significant,
    ('cbc', 'spiir', 'allsky'): threshold_cbc_significant,
    # ML AllSky searches
    ('cbc', 'aframe', 'allsky'): threshold_cbc_significant,
    # CBC EarlyWarning searches
    ('cbc', 'mbta', 'earlywarning'): threshold_cbc_significant,
    ('cbc', 'gstlal', 'earlywarning'): threshold_cbc_significant,
    ('cbc', 'pycbc', 'earlywarning'): threshold_cbc_significant,
    ('cbc', 'spiir', 'earlywarning'): threshold_cbc_significant,
    # CBC SSM searches
    ('cbc', 'mbta', 'ssm'): threshold_cbc_significant,
    ('cbc', 'gstlal', 'ssm'): threshold_cbc_significant,
    # BURST BBH searches
    ('burst', 'cwb', 'bbh'): threshold_cbc_significant,
    # BURST AllSky searches
    ('burst', 'cwb', 'allsky'): threshold_burst_significant,
    ('burst', 'olib', 'allsky'): threshold_burst_significant,
    # CBC MDC gstlal
    ('cbc', 'gstlal', 'mdc'): threshold_cbc_significant,
}
"""Group-Pipeline-Search specific maximum false alarm rate to consider
sending significant alerts (the value include the trial factor).
Default values of 0.0 means no significant criteria."""

preliminary_alert_far_thresholds: dict[tuple[str, str, str], float] = {
    ('cbc', 'mbta', 'allsky'): threshold_cbc,
    ('cbc', 'gstlal', 'allsky'): threshold_cbc,
    ('cbc', 'pycbc', 'allsky'): threshold_cbc,
    ('cbc', 'spiir', 'allsky'): threshold_cbc,
    # ML AllSky searches
    ('cbc', 'aframe', 'allsky'): threshold_cbc,
    # CBC EarlyWarning searches
    ('cbc', 'mbta', 'earlywarning'): threshold_cbc_significant,
    ('cbc', 'gstlal', 'earlywarning'): threshold_cbc_significant,
    ('cbc', 'pycbc', 'earlywarning'): threshold_cbc_significant,
    ('cbc', 'spiir', 'earlywarning'): threshold_cbc_significant,
    # CBC SSM searches
    ('cbc', 'mbta', 'ssm'): threshold_burst,
    ('cbc', 'gstlal', 'ssm'): threshold_burst,
    # BURST BBH searches
    ('burst', 'cwb', 'bbh'): threshold_burst,
    # BURST AllSky searches
    ('burst', 'cwb', 'allsky'): threshold_burst,
    ('burst', 'olib', 'allsky'): threshold_burst,
    # CBC MDC gstlal
    ('cbc', 'gstlal', 'mdc'): threshold_cbc,
}
"""Group-Pipeline-Search specific maximum false alarm rate to consider
for sending less significant alerts (the value include the trial factor).
Default values of 0.0 means no public alerts."""

REQUIRED_LABELS_CBC_ALERT: set[str] = {'PASTRO_READY', 'EMBRIGHT_READY', 'SKYMAP_READY'}
REQUIRED_LABELS_BURST_ALERT: set[str] = {'SKYMAP_READY'}
"""The meaning of the labels indicate that the follwing data products are present:
 SKYMAP_READY    the file pipeline.multiorder.fits is present.
 PASTRO_READY    the file pipeline.p_astro.json is present.
 EMBRIGHT_READY  the file embright.json is present.
"""

required_labels_to_publish: dict[tuple[str, str, str], set[str]] = {
    ('cbc', 'mbta', 'allsky'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'gstlal', 'allsky'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'pycbc', 'allsky'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'spiir', 'allsky'): REQUIRED_LABELS_CBC_ALERT,
    # ML AllSky searches
    ('cbc', 'aframe', 'allsky'): REQUIRED_LABELS_CBC_ALERT,
    # CBC EarlyWarning searches
    ('cbc', 'mbta', 'earlywarning'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'gstlal', 'earlywarning'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'pycbc', 'earlywarning'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'spiir', 'earlywarning'): REQUIRED_LABELS_CBC_ALERT,
    # CBC SSM searches
    ('cbc', 'mbta', 'ssm'): REQUIRED_LABELS_CBC_ALERT,
    ('cbc', 'gstlal', 'ssm'): REQUIRED_LABELS_CBC_ALERT,
    # BURST BBH searches
    ('burst', 'cwb', 'bbh'): REQUIRED_LABELS_CBC_ALERT,
    # BURST AllSky searches
    ('burst', 'cwb', 'allsky'): REQUIRED_LABELS_BURST_ALERT,
    ('burst', 'olib', 'allsky'): REQUIRED_LABELS_BURST_ALERT,
    # CBC MDC gstlal
    ('cbc', 'gstlal', 'mdc'): REQUIRED_LABELS_CBC_ALERT,
}
"""Group-Pipeline-Search required label to have all the data products
present to generate alerts."""

#######################################################################
# END DEFINTION OF ALERT CONDITIONS DICTIONARIES
#######################################################################


def is_significant(event: dict[str, Any]) -> bool:
    """Determine whether an event should be considered a significant event.

    All of the following conditions must be true for a public alert:

    *   The event's ``offline`` flag is not set.
    *   The event's is not an injection.
    *   The event's false alarm rate is less than or equal to
        :obj:`~gwcelery.conf.alert_far_thresholds`

    or the event has been marked to generate a RAVEN alert.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_significant : bool
        :obj:`True` if the event meets the criteria for a signifincat alert.
        :obj:`False` if it does not.

    """
    ev_group = event.get('group', '').lower()
    ev_pipeline = event.get('pipeline', '').lower()
    ev_search = event.get('search', '').lower()
    ev_far = event.get('far', 0.0)
    far_threshold = preliminary_alert_far_thresholds.get(
        (ev_group, ev_pipeline, ev_search), 0.0
    )

    _is_significant = (
        (not event['offline'])
        and ('INJ' not in event['labels'])
        and (ev_far < far_threshold)
    ) or ('RAVEN_ALERT' in event['labels'])

    return _is_significant


# ---------------------------------
# From gwcelery/task/superevents.py
# ---------------------------------


def is_complete(event: dict[str, Any]) -> bool:
    """Determine if a G event is complete.

    One event is comlete when the avaluation of all
    data products complete i.e. has PASTRO_READY, SKYMAP_READY,
    EMBRIGHT_READY for CBC type alerts and the SKYMAP_READY label for the
    Burst events. Test events are not processed by low-latency infrastructure
    and are always labeled complete.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_complete : bool
        :obj:`True` if the event has all teh required data products.
        :obj:`False` if it does not.

    """
    ev_group = event['group'].lower()
    ev_pipeline = event['pipeline'].lower()
    ev_search = event['search'].lower()
    label_set = set(event['labels'])

    required_labels = required_labels_to_publish.get(
        (ev_group, ev_pipeline, ev_search), {'NEVER_COMPLETE'}
    )

    return required_labels.issubset(label_set)


def should_publish(event: dict[str, Any]) -> bool:
    """Determine whether an event should be published as a public alert.

    All of the following conditions must be true for a public alert:

    *   The event's ``offline`` flag is not set.
    *   The event's is not an injection.
    *   The event's false alarm rate is less than or equal to
        :obj:`~gwcelery.conf.alert_far_thresholds`

    or the event has been marked to generate a RAVEN alert.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    should_publish : bool
        :obj:`True` if the event meets the criteria for a public alert or
        :obj:`False` if it does not.

    """
    ev_group = event.get('group', '').lower()
    ev_pipeline = event.get('pipeline', '').lower()
    ev_search = event.get('search', '').lower()
    ev_far = event.get('far', 0.0)
    far_threshold = preliminary_alert_far_thresholds.get(
        (ev_group, ev_pipeline, ev_search), 0.0
    )

    _should_publish = (
        (not event['offline'])
        and ('INJ' not in event['labels'])
        and (ev_far < far_threshold)
    ) or ('RAVEN_ALERT' in event['labels'])

    return _should_publish


def get_mchirp(event: dict[str, Any]) -> float:
    """Get the chirp mass from the LVAlert packet.

    Different groups and pipelines store the mchirp in different fields.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    mchirp : float
        The chirp mass (only for CBC and cWB-BBH search).

    """
    group = event.get('group', '').lower()
    pipeline = event.get('pipeline', '').lower()
    if group == 'cbc':
        attribs = event['extra_attributes']['CoincInspiral']
        return float(attribs['mchirp'])
    elif pipeline == 'cwb':
        attribs = event['extra_attributes']['MultiBurst']
        mchirp = attribs.get('mchirp', 0.0)
        if mchirp is not None:
            return float(mchirp)
        else:
            return 0.0
    else:
        return 0.0


def get_snr(event: dict[str, Any]) -> float:
    """Get the SNR from the LVAlert packet.

    Different groups and pipelines store the SNR in different fields.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    snr : float
        The SNR.

    """
    group = event.get('group', '').lower()
    pipeline = event.get('pipeline', '').lower()
    if pipeline == 'aframe':
        return 0.0
    elif group == 'cbc':
        attribs = event['extra_attributes']['CoincInspiral']
        return float(attribs['snr'])
    elif pipeline == 'cwb':
        attribs = event['extra_attributes']['MultiBurst']
        return float(attribs['snr'])
    elif pipeline == 'olib':
        attribs = event['extra_attributes']['LalInferenceBurst']
        return float(attribs['omicron_snr_network'])
    elif pipeline == 'mly':
        attribs = event['extra_attributes']['MLyBurst']
        return float(attribs['SNR'])
    elif group == 'external':
        return 0.0
    else:
        raise NotImplementedError('SNR attribute not found')


def get_instruments(event: dict[str, Any]) -> set[str]:
    """Get the instruments that contributed data to an event.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    set
        The set of instruments that contributed to the event.

    """
    pipeline = event.get('pipeline', '').lower()
    if pipeline == 'aframe':
        ifos = set(event['instruments'].split(','))
    else:
        attribs = event['extra_attributes']['SingleInspiral']
        ifos = {single['ifo'] for single in attribs}
    return ifos


def get_instruments_in_ranking_statistic(event: dict[str, Any]) -> set[str]:
    """Get the instruments that contribute to the false alarm rate.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    set
        The set of instruments that contributed to the ranking statistic for
        the event.

    Notes
    -----
    The number of instruments that contributed *data* to an event is given by
    the ``instruments`` key of the GraceDB event JSON structure. However, some
    pipelines (e.g. gstlal) have a distinction between which instruments
    contributed *data* and which were considered in the *ranking* of the
    candidate. For such pipelines, we infer which pipelines contributed to the
    ranking by counting only the SingleInspiral records for which the chi
    squared field is non-empty.

    For PyCBC Live in the O3 configuration, an empty chi^2 field does not mean
    that the detector did not contribute to the ranking; in fact, *all*
    detectors listed in the SingleInspiral table contribute to the significance
    even if the chi^2 is not computed for some of them. Hence PyCBC Live is
    handled as a special case.

    """
    pipeline = event.get('pipeline', '').lower()
    if pipeline in ['aframe', 'pycbc']:
        return set(event['instruments'].split(','))
    else:
        attribs = event['extra_attributes']['SingleInspiral']
        return {single['ifo'] for single in attribs if single.get('chisq') is not None}


def keyfunc(event: dict[str, Any]) -> Any:
    """Key function for selection of the preferred event.

    Return a value suitable for identifying the preferred event. Given events
    ``a`` and ``b``, ``a`` is preferred over ``b`` if
    ``keyfunc(a) > keyfunc(b)``, else ``b`` is preferred.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`).

    Returns
    -------
    key : tuple
        The comparison key.

    Notes
    -----
    Tuples are compared lexicographically in Python: they are compared
    element-wise until an unequal pair of elements is found.

    """
    ev_group = event['group'].lower()
    ev_pipeline = event['pipeline'].lower()
    ev_search = event['search'].lower()

    group_rank = superevent_candidate_preference.get(
        (ev_group, ev_pipeline, ev_search), 0
    )

    if ev_group == 'cbc':
        n_ifos = len(get_instruments(event))
        snr_or_far_ranking = get_snr(event)
    else:
        # We don't care about the number of detectors for burst events.
        n_ifos = -1
        # Smaller FAR -> higher IFAR -> more significant.
        # Use -FAR instead of IFAR=1/FAR so that rank for FAR=0 is defined.
        snr_or_far_ranking = -event['far']

    # Conditions that determine choice of the preferred event
    # event completeness comes first
    # then, publishability criteria for significant events
    # then, publishability criteria for less-significant events
    # then, CBC group is given higher priority over Burst
    # then, prioritize more number of detectors
    # finally, use SNR (FAR) between two CBC (Burst) events
    # See https://rtd.igwn.org/projects/gwcelery/en/latest/gwcelery.tasks.superevents.html#selection-of-the-preferred-event  # noqa: E501
    return (
        is_complete(event),
        is_significant(event),
        should_publish(event),
        group_rank,
        n_ifos,
        snr_or_far_ranking,
    )


def is_skymap_required(event: dict[str, Any]) -> bool:
    """Determine if the p_astro data product should be present.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_skymap_required : bool
    """
    ev_group = event['group'].lower()
    ev_pipeline = event['pipeline'].lower()
    ev_search = event['search'].lower()

    required_labels = required_labels_to_publish.get(
        (ev_group, ev_pipeline, ev_search), set()
    )

    return 'SKYMAP_READY' in required_labels


def is_p_astro_required(event: dict[str, Any]) -> bool:
    """Determine if the p_astro data product should be present.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_p_astro_required : bool
    """
    ev_group = event['group'].lower()
    ev_pipeline = event['pipeline'].lower()
    ev_search = event['search'].lower()

    required_labels = required_labels_to_publish.get(
        (ev_group, ev_pipeline, ev_search), set()
    )

    return 'PASTRO_READY' in required_labels


def is_em_bright_required(event: dict[str, Any]) -> bool:
    """Determine if the em_bright data product should be present.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_em_bright_required : bool
    """
    ev_group = event['group'].lower()
    ev_pipeline = event['pipeline'].lower()
    ev_search = event['search'].lower()

    required_labels = required_labels_to_publish.get(
        (ev_group, ev_pipeline, ev_search), set()
    )

    return 'EMBRIGHT_READY' in required_labels


def check_alert_dictionaies_consistency() -> bool:
    """Check consistency of dictionary.

    Check that all dictioary are consisten i.e.:
    - they have the same entries
    - significant_alert_far_thresholds <= preliminary_alert_far_thresholds
    """
    if (
        set(significant_alert_far_thresholds)
        == set(preliminary_alert_far_thresholds)
        == set(required_labels_to_publish)
    ):
        # The dictionary have the same keys
        far_conditions = [
            (
                significant_alert_far_thresholds[key]
                <= preliminary_alert_far_thresholds[key]
            )
            for key in required_labels_to_publish
        ]
        # for key in required_labels_to_publish:
        #    print(key,preliminary_alert_far_thresholds[key],
        #          significant_alert_far_thresholds[key])
        return all(far_conditions)
    else:
        return False
