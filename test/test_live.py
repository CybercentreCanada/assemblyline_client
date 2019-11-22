
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_message_list(datastore, client):
    submission_id = random_id_from_collection(datastore, "submission")
    watch_queue = client.live.setup_watch_queue(submission_id)["wq_id"]

    res = client.live.get_message_list(watch_queue)
    assert len(res) >= 1


def test_setup_watch_queue(datastore, client):
    submission_id = random_id_from_collection(datastore, "submission")
    res = client.live.setup_watch_queue(submission_id)
    assert "wq_id" in res
