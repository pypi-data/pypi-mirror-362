import json
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from mock_event_generator.cache import (
    CacheEntry,
    EventFileCache,
    GEventCacheEntry,
    SEventCacheEntry,
)
from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext

GEVENT_ID = 'G587369'
SEVENT_ID = 'S220609hl'
SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)


def test_cache_gevent_enabled_missing(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.GEventFetcher.fetch')
    cache = EventFileCache(SOURCE, False, tmp_path)
    cache.get_gevent_cache_entry(GEVENT_ID)
    mocked_download.assert_called_once()


def test_cache_gevent_enabled_present(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.GEventFetcher.fetch')
    (tmp_path / GEVENT_ID).mkdir()
    cache = EventFileCache(SOURCE, False, tmp_path)
    cache.get_gevent_cache_entry(GEVENT_ID)
    mocked_download.assert_not_called()


def test_cache_gevent_disabled_missing(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.GEventFetcher.fetch')
    cache = EventFileCache(SOURCE, True, tmp_path)
    cache.get_gevent_cache_entry(GEVENT_ID)
    mocked_download.assert_called_once()


def test_cache_gevent_disabled_present(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.GEventFetcher.fetch')
    (tmp_path / GEVENT_ID).mkdir()
    cache = EventFileCache(SOURCE, True, tmp_path)
    cache.get_gevent_cache_entry(GEVENT_ID)
    mocked_download.assert_called_once()


def test_cache_sevent_enabled_missing(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.SEventFetcher.fetch')
    cache = EventFileCache(SOURCE, False, tmp_path)
    cache.get_sevent_cache_entry(SEVENT_ID)
    mocked_download.assert_called_once()


def test_cache_sevent_enabled_present(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.SEventFetcher.fetch')
    (tmp_path / SEVENT_ID).mkdir()
    cache = EventFileCache(SOURCE, False, tmp_path)
    cache.get_sevent_cache_entry(SEVENT_ID)
    mocked_download.assert_not_called()


def test_cache_sevent_disabled_missing(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.SEventFetcher.fetch')
    cache = EventFileCache(SOURCE, True, tmp_path)
    cache.get_sevent_cache_entry(SEVENT_ID)
    mocked_download.assert_called_once()


def test_cache_sevent_disabled_present(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_download = mocker.patch('mock_event_generator.cache.SEventFetcher.fetch')
    (tmp_path / SEVENT_ID).mkdir()
    cache = EventFileCache(SOURCE, True, tmp_path)
    cache.get_sevent_cache_entry(SEVENT_ID)
    mocked_download.assert_called_once()


def test_read_json(tmp_path: Path) -> None:
    filename = 'file.json'
    value = 'abc'
    (tmp_path / filename).write_text(json.dumps(value))
    cache_entry = CacheEntry(tmp_path)
    assert cache_entry.read_json(filename) == value


def test_gevent_cache_entry_from_sevent_cache_entry(tmp_path: Path) -> None:
    sevent_cache_entry = SEventCacheEntry(tmp_path)
    gevent_cache_entry = sevent_cache_entry / GEVENT_ID
    assert isinstance(gevent_cache_entry, GEventCacheEntry)
    assert gevent_cache_entry.path == tmp_path / GEVENT_ID


def test_gevent_cache_entry_from_sevent_cache_entry_error(tmp_path: Path) -> None:
    sevent_cache_entry = SEventCacheEntry(tmp_path)
    with pytest.raises(TypeError):
        sevent_cache_entry / 3  # type: ignore[operator]
