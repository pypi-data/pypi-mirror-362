"""The mock_event_generator package.

This package downloads and caches existing G-Events from GraceDB and translates them
in time in order to produce new events, but with the same characteristics as the old
ones.
"""

import logging
from importlib.metadata import PackageNotFoundError, version

from .creators import GEventCreator, SEventCreator
from .fetchers import GEventFetcher, SEventFetcher

try:
    __version__ = version('mock_event_generator')
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass

__all__ = [
    'GEventCreator',
    'SEventCreator',
    'GEventFetcher',
    'SEventFetcher',
]

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)
