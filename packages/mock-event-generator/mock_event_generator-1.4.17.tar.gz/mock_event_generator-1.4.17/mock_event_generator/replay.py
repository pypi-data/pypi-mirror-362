"""Utilities for generating replay events."""

import itertools
import math
from collections.abc import Iterator
from typing import Any, Optional

from astropy.time import Time

from .gracedbs import GraceDBWithContext
from .models import SEventDescription


def calculate_offset(start: int, end: int, t_reference: float) -> float:
    """Calculate the replay offset based off of a reference time.

    Parameters:
        start: start time (GPS) of the replay.
        end: end time (GPS) of the replay.
        t_reference: reference time to calculate the offset for.

    Returns:
        The replay offset.
    """
    duration = end - start

    # determine offset needed for replay
    num_replays = math.floor((t_reference - start) / duration)
    return num_replays * duration


def gracedb_iso(gps: float) -> str:
    """Convert a gps time to ISO format, compatible with GraceDB queries.

    Parameters:
        the gps time in seconds

    Returns:
        the time in the format YYYY-MM-DD HH:MM:SS
    """
    return str((Time(gps, format='gps').iso)[:19])


def replay_superevents(
    client: GraceDBWithContext, start: int, end: int
) -> Iterator[SEventDescription]:
    """Generate a continuous replay of superevents.

    This will query GraceDB for the times in question and yield
    results from the superevent query. The replay will cycle
    continuously.

    Parameters:
        client: the GraceDB client to query from.
        start: start time (GPS) of the replay.
        end: end time (GPS) of the replay.

    Yields:
        Superevent descriptions.
    """
    now = Time.now().gps
    offset = calculate_offset(start, end, now)

    # make two queries:
    #  1. from 'now' to end of replay
    #  2. from start of replay to 'now'
    to_end = client.superevents(
        query=f't_0: {now - offset} .. {end}',
        orderby='t_0',
    )
    from_start = client.superevents(
        query=f't_0: {start} .. {now - offset}',
        orderby='t_0',
    )

    # stitch the results of these two queries
    # to generate a continuous replay
    for sevent in itertools.cycle(itertools.chain(to_end, from_start)):
        yield SEventDescription(
            id=sevent['superevent_id'],
            source=client.meg_alias or client.meg_url,
            t_start=sevent['t_start'],
            t_0=sevent['t_0'],
            t_end=sevent['t_end'],
            gevent_ids=sevent['gw_events'],
        )


def replay_gevents(
    client: GraceDBWithContext,
    pipeline: Optional[str],
    search: Optional[str],
    start: int,
    end: int,
) -> Iterator[dict[str, Any]]:
    """Generate a continuous replay of events.

    This will query GraceDB for the times in question and yield
    results from the event query. The replay will cycle
    continuously.

    Parameters:
        client: the GraceDB client to query from.
        pipeline: the search pipeline to be replayed (None->All).
        search: the search to be replayed  (None->All).
        start: start time (GPS) of the replay.
        end: end time (GPS) of the replay.

    Yields:
        Superevent descriptions.
    """
    now = Time.now().gps
    offset = calculate_offset(start, end, now)

    filter = ''
    if pipeline is not None:
        filter = filter + f'pipeline: {pipeline} '
    if search is not None:
        filter = filter + f'search: {search} '
    # make two queries:
    #  1. from 'now' to end of replay
    #  2. from start of replay to 'now'
    to_end = client.events(
        query=filter + f'created: {gracedb_iso(now - offset)} .. {gracedb_iso(end)}',
        orderby='created',
    )
    from_start = client.events(
        query=filter + f'created: {gracedb_iso(start)} .. {gracedb_iso(now - offset)}',
        orderby='created',
    )

    # stitch the results of these two queries
    # to generate a continuous replay
    yield from itertools.cycle(itertools.chain(to_end, from_start))
