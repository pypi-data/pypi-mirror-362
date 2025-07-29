"""This module provides the functionality to access cached event cached data files."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from apischema import ValidationError, deserialize

from mock_event_generator.gracedbs import GraceDBWithContext

from .fetchers import GEventFetcher, SEventFetcher
from .models import GEventDescription, SEventDescription

__all__ = ['EventFileCache', 'GEventCacheEntry', 'SEventCacheEntry']

logger = logging.getLogger(__name__)

try:
    DEFAULT_CACHE_PATH = Path(os.environ['XDG_CACHE_HOME']) / 'mock-event-generator'
except KeyError:
    DEFAULT_CACHE_PATH = Path.home() / '.cache' / 'mock-event-generator'


@dataclass(frozen=True)
class EventFileCache:
    """Class to cache and access G-event or S-event data files.

    Attributes:
        source: The GraceDB instance name from which events are downloaded, such as
            `production` or `playground`.
        disabled: If true, bypass the cache and always download the event data files.
        cache_path: The top-level path of the cache.
    """

    source: GraceDBWithContext
    disabled: bool
    cache_path: Path = DEFAULT_CACHE_PATH

    def __post_init__(self) -> None:
        """Ensure that the cache path exists."""
        self.cache_path.mkdir(exist_ok=True, parents=True)

    def get_sevent_cache_entry(self, sevent_id: str) -> SEventCacheEntry:
        """Factory to cache and access S-event data files.

        If the data is not available in the cache, it is immediately downloaded.

        Parameters:
            sevent_id: Identifier of the S-event to be downloaded.
        """
        return SEventCacheEntry.from_id(
            sevent_id, self.source, self.disabled, self.cache_path
        )

    def get_gevent_cache_entry(self, gevent_id: str) -> GEventCacheEntry:
        """Factory to cache and access G-event data files.

        If the data is not available in the cache, it is immediately downloaded.

        Attributes:
            gevent_id: Identifier of the G-event to be downloaded.
        """
        try:
            path = next(self.cache_path.glob(f'*/{gevent_id}')).parent
        except StopIteration:
            path = self.cache_path

        return GEventCacheEntry.from_id(gevent_id, self.source, self.disabled, path)


@dataclass(frozen=True)
class CacheEntry:
    """Class to access cached data files.

    Attributes:
        path: The path to the cache entry.
    """

    path: Path

    def read_bytes(self, filename: str) -> bytes:
        return (self.path / filename).read_bytes()

    def read_json(self, filename: str) -> Any:
        return json.loads(self.read_bytes(filename))


class SEventCacheEntry(CacheEntry):
    """Class to access cached S-event data files.

    Attributes:
        path: The path to the cache entry.
    """

    @classmethod
    def from_id(
        cls,
        sevent_id: str,
        source: GraceDBWithContext,
        disabled: bool,
        cache_path: Path,
    ) -> SEventCacheEntry:
        """Factory to cache and access S-event data files.

        If the data is not available in the cache, it is downloaded.

        Parameters:
            sevent_id: Identifier of the S-event to be downloaded.
            source: The GraceDB client from which events are downloaded.
            disabled: If true, bypass the cache and always download the data files.
            cache_path: The top-level path of the cache.
        """
        sevent_path = cache_path / sevent_id
        if disabled or not sevent_path.is_dir():
            logger.info(
                f'Downloading {sevent_id} from GraceDB ('
                f'{source.meg_alias or source.meg_url})...'
            )
            SEventFetcher.from_id(sevent_id, source, sevent_path.parent).fetch()
        return SEventCacheEntry(sevent_path)

    def __truediv__(self, gevent_id: str) -> GEventCacheEntry:
        """Get a G-Event cache entry from an S-Event cache entry.

        Parameters:
            gevent_id: The G-event identifier.

        Example:
            >>> cache_entry = SEventCacheEntry(DEFAULT_CACHE_PATH / 'S00001')
            >>> cache_entry / 'G00001'
            GEventCacheEntry(
                path=PosixPath('/home/user/.cache/mock_event_generator/S00001/G00001')
            )
        """
        if not isinstance(gevent_id, str):
            return NotImplemented
        return GEventCacheEntry(self.path / gevent_id)

    def get_description(self) -> SEventDescription:
        """Return the serialized description of the S-event."""
        serialized_description = self.read_json('description.json')
        # Some version of mock-event-generator had the field:
        # - sevent_data
        # Here a compatibility hack.
        try:
            return deserialize(SEventDescription, serialized_description)
        except ValidationError:
            serialized_description.pop('sevent_data', None)
            return deserialize(SEventDescription, serialized_description)


class GEventCacheEntry(CacheEntry):
    """Class to access cached G-event data files.

    Attributes:
        path: The path to the cache entry.
    """

    @classmethod
    def from_id(
        cls,
        gevent_id: str,
        source: GraceDBWithContext,
        disabled: bool,
        cache_path: Path,
    ) -> GEventCacheEntry:
        """Factory to cache and access G-event data files.

        If the data is not available in the cache, it is downloaded.

        Attributes:
            gevent_id: Identifier of the G-event to be downloaded.
            source: The GraceDB client from which events are downloaded.
            disabled: If true, bypass the cache and always download the data files.
            cache_path: The top-level or associated S-event cache path.
        """
        gevent_path = cache_path / gevent_id
        if disabled or not gevent_path.is_dir():
            logger.info(
                f'Downloading {gevent_id} from GraceDB ('
                f'{source.meg_alias or source.meg_url})...'
            )
            GEventFetcher.from_id(gevent_id, source, gevent_path.parent).fetch()
        return GEventCacheEntry(gevent_path)

    def get_description(self) -> GEventDescription:
        """Return the serialized description of the G-event."""
        serialized_description = self.read_json('description.json')
        # Some version of mock-event-generator missed the fields:
        # - superevent
        # - far
        # Here a compatibility hack.
        if serialized_description.get('superevent') is None:
            serialized_description['superevent'] = ''
        if serialized_description.get('far') is None:
            serialized_description['far'] = 0.0
        return deserialize(GEventDescription, serialized_description)
