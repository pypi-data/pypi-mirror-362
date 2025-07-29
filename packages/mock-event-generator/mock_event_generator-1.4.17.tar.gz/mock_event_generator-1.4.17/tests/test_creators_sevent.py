from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from astropy.time import Time
from pytest_mock import MockerFixture
from trio.testing import MockClock

from mock_event_generator.cache import EventFileCache
from mock_event_generator.creators import (
    PIPELINE_GEVENT_CREATOR_CLASSES,
    CWBEventCreator,
    SEventCreator,
)
from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext

SEVENT_ID = 'S220609hl'
SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)
TARGET = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)


@pytest.fixture
def cache(mocked_gracedb: None, tmp_path: Path) -> Iterator[EventFileCache]:
    yield EventFileCache(SOURCE, False, tmp_path)


@pytest.mark.xfail
@pytest.mark.parametrize('group', [None, 'Test'])
@pytest.mark.parametrize('search', [None, 'MDC'])
async def test_create_sevent(
    cache: EventFileCache,
    group: str | None,
    search: str | None,
    autojump_clock: MockClock,
) -> None:
    creator = SEventCreator.from_id(SEVENT_ID, SOURCE, cache)
    actual_gevents = await creator.create(group, search, Time.now().gps)
    sevent_cache_entry = cache.get_sevent_cache_entry(SEVENT_ID)
    gevent_ids = sevent_cache_entry.get_description().gevent_ids
    for gevent_id, actual_gevent in zip(gevent_ids, actual_gevents):
        description = (sevent_cache_entry / gevent_id).get_description()
        expected_group = group or description.group
        expected_search = search or description.search
        assert actual_gevent['group'] == expected_group
        assert actual_gevent['search'] == expected_search


async def test_create_sevent_unknown_pipeline(
    mocker: MockerFixture, caplog: pytest.LogCaptureFixture, cache: EventFileCache
) -> None:
    mocker.patch.dict(PIPELINE_GEVENT_CREATOR_CLASSES, clear=True)
    creator = SEventCreator.from_id(SEVENT_ID, SOURCE, cache)
    await creator.create(None, None, Time.now().gps)
    assert 'Cannot re-create G-event' in caplog.text


@pytest.mark.xfail
async def test_create_sevent_only_one_gevent(
    mocker: MockerFixture, cache: EventFileCache
) -> None:
    mocker.patch.dict(
        PIPELINE_GEVENT_CREATOR_CLASSES, {'CWB': CWBEventCreator}, clear=True
    )
    creator = SEventCreator.from_id(SEVENT_ID, SOURCE, cache)
    gevents = await creator.create(None, None, Time.now().gps, max_delay=1)
    assert len(gevents) == 1


async def test_create_sevent_single_upload() -> None:
    max_delay = 2.0
    assert SEventCreator._get_shrink_factors({'Z12345': [0]}, max_delay) == (0.0, 1.0)
