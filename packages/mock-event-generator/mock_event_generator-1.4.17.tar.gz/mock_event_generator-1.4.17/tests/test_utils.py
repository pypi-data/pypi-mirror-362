import pytest

from mock_event_generator.utils import is_any_event, is_gevent, is_superevent


@pytest.mark.parametrize('id', ['G12345', 'M12345', 'T12345'])
def test_is_gevent(id: str) -> None:
    assert is_gevent(id)


@pytest.mark.parametrize('id', ['S12345a', 'G123', 'G12345a', 'S12345', 'MS12345'])
def test_is_not_gevent(id: str) -> None:
    assert not is_gevent(id)


@pytest.mark.parametrize('id', ['MS12345a', 'S12345a'])
def test_is_superevent(id: str) -> None:
    assert is_superevent(id)


@pytest.mark.parametrize(
    'id', ['G12345', 'S123a', 'MS123a', 'S00000', 'M12345a', 'G12345a']
)
def test_is_not_superevent(id: str) -> None:
    assert not is_superevent(id)


@pytest.mark.parametrize('id', ['G12345', 'M12345', 'T12345', 'MS12345a', 'S12345a'])
def test_is_any_event(id: str) -> None:
    assert is_any_event(id)


@pytest.mark.parametrize(
    'id',
    [
        'G123',
        'G12345a',
        'S12345',
        'MS12345',
        'S123a',
        'MS123a',
        'S00000',
        'M12345a',
        'G12345a',
    ],
)
def test_is_not_anyevent(id: str) -> None:
    assert not is_any_event(id)
