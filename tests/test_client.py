
import assemblyline_client
import mocks

import mock
from base64 import b64decode


def test_bad_cert():
    """Make sure that the client detects that the test cert is self signed."""
    with mocks.Server() as server:
        try:
            assemblyline_client.Client(server.address)
            assert False
        except assemblyline_client.ClientError as ce:
            assert 'CERTIFICATE_VERIFY_FAILED' in str(ce)


def test_noauth():
    """The test server should let us login with no authentication."""
    with mocks.Server() as server:
        assemblyline_client.Client(server.address, verify=False)
        assert len(server.logins) == 1


def test_noauth_submit(mocker):
    """Submit a file and ensure that the same file is unpacked."""
    with mocks.Server() as server:

        client = assemblyline_client.Client(server.address, verify=False)
        submits = server.submits

        # Submit a file with contents
        client.submit(path='readme.txt', contents=b'abc123')
        assert len(submits) == 1
        assert b64decode(submits[0]['binary']) == b'abc123'
        assert submits[0]['name'] == 'readme.txt'
        submits.pop()

        # Submit a file from a file
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('assemblyline_client.open', mock.mock_open(read_data=b'abc123'), create=True)
        client.submit(path='readme.txt')
        assert len(submits) == 1
        assert b64decode(submits[0]['binary']) == b'abc123'
        assert submits[0]['name'] == 'readme.txt'
        submits.pop()


def test_encrypt_password_auth():
    """Send an encryped password and decrypt it."""
    with mocks.Server() as server:
        assemblyline_client.Client(server.address, verify=False, auth=('username', 'password'))
        assert len(server.logins) == 1
        assert server.logins[0]['user'] == 'username'
        assert server.logins[0]['password'] != 'password'
        assert server.private_key.decrypt(b64decode(server.logins[0]['password']), 'ERROR') == b'password'


def test_encrypt_apikey_auth():
    """Send an encryped apikey and decrypt it."""
    with mocks.Server() as server:
        assemblyline_client.Client(server.address, verify=False, apikey=('username', 'ANAPIKEY'))
        assert len(server.logins) == 1
        assert server.logins[0]['user'] == 'username'
        assert server.logins[0]['apikey'] != 'ANAPIKEY'
        assert server.private_key.decrypt(b64decode(server.logins[0]['apikey']), 'ERROR') == b'ANAPIKEY'
