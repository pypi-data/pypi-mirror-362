from base64 import b64decode

import pytest
import responses
from requests import Response

from mock_event_generator.gracedbs import GRACEDB_URLS, GraceDBWithContext


@pytest.mark.xfail
def test_gracedb_basic_authentication() -> None:
    call_count = 0

    def callback(resp: Response) -> Response:
        nonlocal call_count
        call_count += 1
        headers = resp.request.headers
        assert 'Authorization' in headers
        decoded = b64decode(headers['Authorization'].removeprefix('Basic '))
        assert decoded.decode() == f'{username}:{password}'
        return resp

    username = 'username'
    password = 'password'
    alias = 'mocked'
    url = GRACEDB_URLS[alias]
    client = GraceDBWithContext(alias, url, username=username, password=password)
    api = GRACEDB_URLS[alias] + '/api/'
    with responses.RequestsMock(response_callback=callback) as mock:
        mock.add(responses.GET, api)
        client.get(api)
    assert call_count == 1
