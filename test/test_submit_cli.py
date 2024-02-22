import os
import re
import sys

try:
    from assemblyline_client.submit import _main
    from assemblyline_client.v4_client.common.submit_utils import al_result_to_text
    from utils import random_id_from_collection
    from io import StringIO
except ImportError:
    import pytest
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_submit(datastore):
    old_stderr = sys.stderr
    sys.stderr = mystderr = StringIO()

    test_file = os.path.join(os.path.dirname(__file__), 'test_user.py')
    res = _main(['-a', '-n', '-i', '-u', 'admin', '-p', 'admin', test_file])
    stderr = mystderr.getvalue()
    assert re.match(r'Sending file .*test_user.py for analysis\.\.\.\n', stderr) is not None
    assert res == 0

    sys.stderr = old_stderr


def test_result_to_text(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission', q="file_count:[2 TO *]")
    data = client.submission.full(submission_id)
    text = "\n".join(al_result_to_text(data))
    assert len(text) != 0
    assert ":: Submission Detail ::" in text
    assert ":: Submitted files ::" in text
    assert ":: Service results ::" in text
    assert "ERR: Unknown section type" not in text
