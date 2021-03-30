import pytest

try:
    from assemblyline_client.v4_client.common.utils import ClientError
    from utils import random_id_from_collection
except ImportError:
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_message(datastore, client):
    submission_id = random_id_from_collection(datastore, "submission")
    with pytest.raises(ClientError):
        client.live.setup_watch_queue(submission_id)["wq_id"]

    res = client.live.get_message('DOES_NOT_EXIST')
    assert res['msg'] is None
    assert res['type'] == 'timeout'


def test_get_message_list(datastore, client):
    submission_id = random_id_from_collection(datastore, "submission")
    with pytest.raises(ClientError):
        client.live.setup_watch_queue(submission_id)["wq_id"]

    res = client.live.get_message_list('DOES_NOT_EXIST')
    assert len(res) == 0


def test_outstanding_services(datastore, client):
    submission_id = random_id_from_collection(datastore, "submission")
    res = client.live.outstanding_services(submission_id)
    assert res == {}


def test_setup_watch_queue(datastore, client):
    submission_id = random_id_from_collection(datastore, "submission")
    with pytest.raises(ClientError):
        client.live.setup_watch_queue(submission_id)
