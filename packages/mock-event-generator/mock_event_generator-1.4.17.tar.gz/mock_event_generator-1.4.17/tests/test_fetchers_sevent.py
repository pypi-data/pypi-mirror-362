import json
from pathlib import Path
from typing import Any

import pytest
from apischema import deserialize
from pytest_mock import MockerFixture

from mock_event_generator import GEventFetcher, SEventFetcher
from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext
from mock_event_generator.models import GEventDescription, SEventDescription

SEVENT_ID = 'S220609hl'
GEVENT_IDS = {'G587365', 'G587366', 'G587369'}
SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)


def test_fetchers(mocked_gracedb: None, tmp_path: Path) -> None:
    superevent_path = tmp_path / SEVENT_ID
    fetcher = SEventFetcher.from_id(SEVENT_ID, SOURCE, tmp_path)
    fetcher.fetch()
    description_path = superevent_path / 'description.json'
    assert description_path.is_file()
    description_serialized = json.loads(description_path.read_text())
    description_sevent = deserialize(SEventDescription, description_serialized)
    assert description_sevent.id == SEVENT_ID
    assert GEVENT_IDS.issubset(description_sevent.gevent_ids)

    for graceid in GEVENT_IDS:
        gevent_path = superevent_path / graceid
        assert gevent_path.is_dir()
        description_path = gevent_path / 'description.json'
        assert description_path.is_file()
        description_serialized = json.loads(description_path.read_text())
        description_gevent = deserialize(GEventDescription, description_serialized)
        assert description_gevent.id == graceid


@pytest.mark.parametrize('exception_cls', [KeyboardInterrupt, ValueError])
def test_cleanup(
    mocker: MockerFixture,
    mocked_gracedb: None,
    tmp_path: Path,
    exception_cls: type[BaseException],
) -> None:
    mocked_rmtree = mocker.patch('shutil.rmtree')
    mocked_fetch_no_cleanup = mocker.patch(
        'mock_event_generator.SEventFetcher._fetch_no_cleanup',
        side_effect=exception_cls,
    )

    with pytest.raises(exception_cls):
        SEventFetcher.from_id(SEVENT_ID, SOURCE, tmp_path).fetch()

    mocked_fetch_no_cleanup.assert_called_once()
    mocked_rmtree.assert_called_once()


def test_cleanup_present(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_rmtree = mocker.patch('shutil.rmtree')
    (tmp_path / SEVENT_ID).mkdir()
    SEventFetcher.from_id(SEVENT_ID, SOURCE, tmp_path).fetch()
    mocked_rmtree.assert_called_once()


def test_cleanup_missing(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_rmtree = mocker.patch('shutil.rmtree')
    SEventFetcher.from_id(SEVENT_ID, SOURCE, tmp_path).fetch()
    mocked_rmtree.assert_not_called()


def test_nologs(mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path) -> None:
    mocked_filter_logs = mocker.patch(
        'mock_event_generator.GEventFetcher._filter_logs', return_value=[]
    )
    SEventFetcher.from_id(SEVENT_ID, SOURCE, tmp_path).fetch()
    assert mocked_filter_logs.call_count == len(GEVENT_IDS)
    assert [p.name for p in (tmp_path / SEVENT_ID).glob('*')] == ['description.json']


def test_discard_offline(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    original_from_id = GEventFetcher.from_id

    def new_from_id(*args: Any, **keywords: Any) -> GEventFetcher:
        fetcher = original_from_id(*args, **keywords)
        fetcher.gevent['offline'] = True
        return fetcher

    mocker.patch(
        'mock_event_generator.GEventFetcher.from_id',
        autospec=True,
        side_effect=new_from_id,
    )

    SEventFetcher.from_id(SEVENT_ID, SOURCE, tmp_path).fetch()
    assert [p.name for p in (tmp_path / SEVENT_ID).glob('*')] == ['description.json']
