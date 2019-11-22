
from assemblyline_client.submit import _main
import mocks

import mock
from base64 import b64decode


def test_submit(mocker):
    """Call the main function for submit.py with a 'file' to submit."""
    with mocks.Server() as server:
        submits = server.submits

        # Create the fake file
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('assemblyline_client.submit.exists', return_value=True)
        mocker.patch('assemblyline_client.v3_client.open', mock.mock_open(read_data=b'abc123'), create=True)

        # Call the submit script
        _main(['-i', '-s', server.address, '-u', 'user', '-p', 'password', 'readme.txt'])

        # Did it submit the file
        assert len(submits) == 1
        assert b64decode(submits[0]['binary']) == b'abc123'
        assert submits[0]['name'] == 'readme.txt'

        # Did it request the results
        assert server.got_like('/api/v3/submission/full/')
