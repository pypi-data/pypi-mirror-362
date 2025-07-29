import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext

SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.PLAYGROUND)

# include the tests directory in the path so that we can import tests from it
sys.path.insert(0, str(Path(__file__).parents[1]))


@pytest.fixture
def mocked_gracedb(mocker: MockerFixture) -> Iterator[None]:
    mocker.patch('tests.test_fetchers_gevent.SOURCE', SOURCE)
    mocker.patch('tests.test_fetchers_sevent.SOURCE', SOURCE)
    yield
