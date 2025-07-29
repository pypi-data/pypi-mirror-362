from __future__ import annotations

from pathlib import Path

import pytest
from freezegun import freeze_time
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from mock_event_generator.cache import EventFileCache
from mock_event_generator.cli import meg
from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext
from pytest_gracedb import PIPELINES

SEVENT_ID = 'S220609hl'
GEVENT_ID = PIPELINES['cwb'].gevent_id
SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)

runner = CliRunner()


def test_fetch_help(mocked_gracedb: None) -> None:
    result = runner.invoke(
        meg,
        [
            'fetch',
            '--help',
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert 'Fetch G-events and store them in the cache.' in result.output


@pytest.mark.parametrize('source', ['mocked', 'http://localhost', 'https://xyz'])
def test_fetch_gevent_alias(mocked_gracedb: None, source: str, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'fetch',
            GEVENT_ID,
            '--source',
            source,
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    path = tmp_path / GEVENT_ID
    assert path.is_dir()
    actual_files = {_.name for _ in path.glob('*')} - {'description.json'}
    assert actual_files
    assert actual_files <= set(PIPELINES['cwb'].files)


def test_fetch_gevent_invalid_source(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'fetch',
            GEVENT_ID,
            '--source',
            'invalid',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Invalid specifier for the GraceDB server: 'invalid'" in result.output


def test_fetch_sevent(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'fetch',
            SEVENT_ID,
            '--source',
            'mocked',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    path = tmp_path / SEVENT_ID
    assert path.is_dir()
    actual_files = {_.name for _ in path.glob('*')}
    assert 'description.json' in actual_files
    assert GEVENT_ID in actual_files


def test_fetch_invalid_event(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'fetch',
            'G12345',
            'XYZ1',
            'XYZ2',
            '--source',
            'mocked',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Invalid event identifier(s): 'XYZ1', 'XYZ2'." in result.output


@pytest.mark.xfail
def test_create_gevent(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'create',
            GEVENT_ID,
            '--target',
            'mocked',
            '--source',
            'mocked',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert (tmp_path / GEVENT_ID).is_dir()


def test_create_gevent_invalid_target(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'create',
            GEVENT_ID,
            '--target',
            'invalid',
            '--source',
            'mocked',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Invalid specifier for the GraceDB server: 'invalid'" in result.output


@pytest.mark.xfail
def test_create_sevent(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'create',
            SEVENT_ID,
            '--target',
            'mocked',
            '--source',
            'mocked',
            '--cache-path',
            str(tmp_path),
            '--max-delay',
            '0',
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert (tmp_path / SEVENT_ID).is_dir()


def test_create_invalid_event(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'create',
            'G12345',
            'S12345a',
            'XYZ1',
            'XYZ2',
            '--target',
            'mocked',
            '--source',
            'mocked',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Invalid event identifier(s): 'XYZ1', 'XYZ2'." in result.output


@pytest.mark.parametrize(
    'include_files, expected_output',
    [
        (
            False,
            '├── G587366     MBTAOnline     CBC            AllSky         1338848303.869315\n    └── G587369     CWB            Burst          BBH            1338848303.7875',
        ),
        (
            True,
            '└── G587369     CWB            Burst          BBH            1338848303.7875\n        ├── description.json',
        ),
    ],
)
@pytest.mark.xfail
def test_cache_list(
    mocked_gracedb: None, tmp_path: Path, include_files: bool, expected_output: str
) -> None:
    cache = EventFileCache(SOURCE, False, tmp_path)
    cache.get_sevent_cache_entry(SEVENT_ID)
    assert len(list(tmp_path.glob('*'))) == 1

    result = runner.invoke(
        meg,
        [
            'cache',
            'list',
            '--include-files' if include_files else '--no-include-files',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_cache_list_path_not_found(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'cache',
            'list',
            '--cache-path',
            str(tmp_path / 'invalid_path'),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert 'Cache path does not exist' in result.output


@pytest.mark.parametrize('name', ['S00000abc', 'A00000', 'G00000', 'Z00000'])
def test_cache_clean_valid(mocked_gracedb: None, tmp_path: Path, name: str) -> None:
    (tmp_path / name).mkdir()
    result = runner.invoke(
        meg,
        [
            'cache',
            'clean',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert len(list(tmp_path.glob('*'))) == 0


@pytest.mark.parametrize(
    'name, isdir',
    [
        ('G00000a', True),
        ('S00000', True),
        ('mystuff', True),
        ('otherstuff', False),
        ('G12345', False),
        ('S12345a', False),
    ],
)
def test_cache_clean_invalid(
    mocked_gracedb: None, tmp_path: Path, name: str, isdir: bool
) -> None:
    path = tmp_path / name
    if isdir:
        path.mkdir()
    else:
        path.touch()
    assert len(list(tmp_path.glob('*'))) == 1

    result = runner.invoke(
        meg,
        [
            'cache',
            'clean',
            '--cache-path',
            str(tmp_path),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert len(list(tmp_path.glob('*'))) == 1


def test_cache_clean_path_not_found(mocked_gracedb: None, tmp_path: Path) -> None:
    result = runner.invoke(
        meg,
        [
            'cache',
            'clean',
            '--cache-path',
            str(tmp_path / 'invalid_path'),
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert 'Cache path does not exist' in result.output


def test_ca_certificate(mocker: MockerFixture, tmp_path: Path) -> None:
    ca_bundle = tmp_path / 'cacert.pem'
    ca_bundle.touch()
    mocker.patch('certifi.where', return_value=str(ca_bundle))
    result = runner.invoke(
        meg,
        [
            'ca-certificate',
            'tests/data/certificate-terena-ssl-ca-3.pem',
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert ca_bundle.stat().st_size > 0


@freeze_time('3000/1/1')
def test_ca_certificate_expired(mocker: MockerFixture, tmp_path: Path) -> None:
    ca_bundle = tmp_path / 'cacert.pem'
    ca_bundle.touch()
    mocker.patch('certifi.where', return_value=str(ca_bundle))
    result = runner.invoke(
        meg,
        [
            'ca-certificate',
            'tests/data/certificate-terena-ssl-ca-3.pem',
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert 'has expired' in result.output


def test_ca_certificate_already_added(mocker: MockerFixture, tmp_path: Path) -> None:
    ca_bundle = tmp_path / 'cacert.pem'
    ca_bundle.write_text(Path('tests/data/certificate-terena-ssl-ca-3.pem').read_text())
    mocker.patch('certifi.where', return_value=str(ca_bundle))
    result = runner.invoke(
        meg,
        [
            'ca-certificate',
            'tests/data/certificate-terena-ssl-ca-3.pem',
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert 'has already been added' in result.output
