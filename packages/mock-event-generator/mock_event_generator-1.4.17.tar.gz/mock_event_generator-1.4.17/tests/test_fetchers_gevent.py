import json
from pathlib import Path

import pytest
from apischema import deserialize
from pytest_mock import MockerFixture
from requests import HTTPError, Response

from mock_event_generator import GEventFetcher
from mock_event_generator.exceptions import MEGIgnoreEventError
from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext
from mock_event_generator.models import GEventDescription
from pytest_gracedb import PIPELINES, Pipeline

GEVENT_ID = PIPELINES['cwb'].gevent_id
SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)


@pytest.mark.parametrize('pipeline_id, pipeline', PIPELINES.items())
def test_fetchers(
    mocked_gracedb: None, tmp_path: Path, pipeline_id: str, pipeline: Pipeline
) -> None:
    gevent_id = pipeline.gevent_id
    fetcher = GEventFetcher.from_id(gevent_id, SOURCE, tmp_path)
    fetcher.fetch()

    path = tmp_path / gevent_id
    description_path = path / 'description.json'
    assert description_path.is_file()
    description_serialized = json.loads(description_path.read_text())
    description = deserialize(GEventDescription, description_serialized)
    assert description.id == gevent_id

    expected = {
        'cwb': {
            'trigger_1338848303.7875.txt,0',
            'cWB.fits.gz,0',
        },
        'fermi': {
            'tmpykkr0kg3,0',
            'fermi_test_skymap.fits.gz,0',
            'fermi_test_skymap.fits.gz,1',
            'coincidence_far.json,2',
            'coincidence_far.json,3',
        },
        'gstlal': {
            'coinc.xml,0',
            'p_astro.json,0',
            'ranking_data.xml.gz,0',
        },
        'mbta': {
            'coinc.xml,0',
            'pastro.json,0',
            'embright.json,0',
        },
        'mly': {
            'T_1339447521.0_HLV.json,0',
        },
        'pycbc': {
            'coinc-1339452303.1486003-jnqfly.xml.gz,0',
            'coinc-1339452303.1486003-jnqfly.hdf,0',
            'coinc-1339452303.1486003-jnqfly_probs.json,0',
        },
        'spiir': {
            'H1L1V1_1339427916_398_235.xml,0',
            'psd.xml.gz,0',
        },
    }[pipeline_id]

    assert {_.name for _ in path.glob('*') if '.png,' not in _.name} - {
        'description.json'
    } == expected


@pytest.mark.parametrize('exception_cls', [KeyboardInterrupt, ValueError])
def test_cleanup(
    mocker: MockerFixture,
    mocked_gracedb: None,
    tmp_path: Path,
    exception_cls: type[BaseException],
) -> None:
    mocked_rmtree = mocker.patch('shutil.rmtree')
    mocked_fetch_no_cleanup = mocker.patch(
        'mock_event_generator.GEventFetcher._fetch_no_cleanup',
        autospec=True,
        side_effect=exception_cls,
    )

    with pytest.raises(exception_cls):
        GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path).fetch()

    mocked_fetch_no_cleanup.assert_called_once()
    mocked_rmtree.assert_called_once()


def test_cleanup_present(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_rmtree = mocker.patch('shutil.rmtree')
    (tmp_path / GEVENT_ID).mkdir()
    GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path).fetch()
    mocked_rmtree.assert_called_once()


def test_cleanup_missing(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    mocked_rmtree = mocker.patch('shutil.rmtree')
    GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path).fetch()
    mocked_rmtree.assert_not_called()


def test_nologs(mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path) -> None:
    mocked_filter_logs = mocker.patch(
        'mock_event_generator.GEventFetcher._filter_logs', return_value=[]
    )
    fetcher = GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path)
    with pytest.raises(MEGIgnoreEventError):
        fetcher.fetch()
    mocked_filter_logs.assert_called_once()


def test_store_file_http_error(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    old_raise_for_status = Response.raise_for_status

    def new_raise_for_status(response: Response) -> None:
        assert response.request.url is not None
        if '/files/' in response.request.url:
            response.status_code = 500
        old_raise_for_status(response)

    fetcher = GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path)
    mocker.patch(
        'requests.Response.raise_for_status',
        autospec=True,
        side_effect=new_raise_for_status,
    )
    with pytest.raises(HTTPError):
        fetcher.fetch()


def test_store_file_present_gz(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    fetcher = GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path)
    mocked_store_file = mocker.spy(fetcher, '_store_file')
    filename = PIPELINES['cwb'].files[0]
    fetcher._store_file(tmp_path, filename + '.gz')
    assert mocked_store_file.call_count == 2
    mocked_store_file.assert_called_with(tmp_path, filename)


def test_store_file_missing_gz(
    mocker: MockerFixture, mocked_gracedb: None, tmp_path: Path
) -> None:
    fetcher = GEventFetcher.from_id(GEVENT_ID, SOURCE, tmp_path)
    mocked_store_file = mocker.spy(fetcher, '_store_file')
    with pytest.raises(ValueError):
        fetcher._store_file(tmp_path, 'xxx.gz')
    assert mocked_store_file.call_count == 2
    mocked_store_file.assert_called_with(tmp_path, 'xxx')
