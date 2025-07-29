"""The models for the package `mock-event-generator`."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Upload:
    """Class containing the information required to submit a file to GraceDB."""

    message: str
    tags: set[str]
    filename: str
    delay: float


@dataclass
class GEventDescription:
    """Class containing all the information required to create a G-event."""

    id: str
    source: str
    pipeline: str
    group: str
    search: str
    offline: bool
    gpstime: float
    reporting_latency: float
    uploads: list[Upload]
    superevent: str
    far: float


@dataclass
class SEventDescription:
    """Class containing all the information required to create a S-event."""

    id: str
    source: str
    t_start: float
    t_0: float
    t_end: float
    gevent_ids: list[str]
