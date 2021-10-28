import tempfile

from io import BytesIO

try:
    from assemblyline.common import forge
    from assemblyline.common.uid import get_random_id
    from assemblyline.odm.models.submission import Submission
    from assemblyline.odm.randomizer import random_model_obj, get_random_phrase
    from assemblyline.remote.datatypes.queues.named import NamedQueue

    from utils import random_id_from_collection

    config = forge.get_config()

except (ImportError, SyntaxError):
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_message(datastore, client):
    notification_queue = get_random_id()
    queue = NamedQueue("nq-%s" % notification_queue,
                       host=config.core.redis.persistent.host,
                       port=config.core.redis.persistent.port)
    queue.delete()
    msg = random_model_obj(Submission).as_primitives()
    queue.push(msg)

    res = client.ingest.get_message(notification_queue)
    assert isinstance(res, dict)
    assert 'sid' in res
    assert 'results' in res
    assert res == msg


def test_get_message_list(datastore, client):
    notification_queue = get_random_id()
    queue = NamedQueue("nq-%s" % notification_queue,
                       host=config.core.redis.persistent.host,
                       port=config.core.redis.persistent.port)
    queue.delete()
    msg_0 = random_model_obj(Submission).as_primitives()
    queue.push(msg_0)
    msg_1 = random_model_obj(Submission).as_primitives()
    queue.push(msg_1)

    res = client.ingest.get_message_list(notification_queue)
    assert len(res) == 2
    assert res[0] == msg_0
    assert res[1] == msg_1


def test_ingest_content(datastore, client):
    content = get_random_phrase(wmin=15, wmax=50).encode()
    res = client.ingest(content=content, fname=get_random_id())
    assert res.get('ingest_id', None) is not None


def test_submit_fh(datastore, client):
    content = get_random_phrase(wmin=15, wmax=50).encode()
    fname = "test_ingest_{}.txt".format(get_random_id())
    with tempfile.TemporaryFile() as test_file:
        test_file.write(content + b"FILE_HANDLE")
        res = client.submit(fh=test_file, fname=fname)
    assert res.get('ingest_id', None) is not None


def test_submit_bio(datastore, client):
    bio = BytesIO()
    bio.write(get_random_phrase(wmin=15, wmax=50).encode() + b"BIO")
    fname = "test_ingest_{}.txt".format(get_random_id())
    res = client.submit(fh=bio, fname=fname)
    assert res.get('ingest_id', None) is not None


def test_ingest_path(datastore, client):
    content = get_random_phrase(wmin=15, wmax=50).encode()
    test_path = "/tmp/test_ingest_{}".format(get_random_id())
    with open(test_path, 'wb') as test_file:
        test_file.write(content + b"PATH")

    res = client.ingest(alert=True, path=test_path, params={'service_spec': {"extract": {"password": "test"}}})
    assert res.get('ingest_id', None) is not None


def test_ingest_sha(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.ingest(alert=True, sha256=file_id, metadata={"file_id": get_random_id(), "comment": "test"},
                        nq=get_random_id(), nt=100)
    assert res.get('ingest_id', None) is not None


def test_ingest_url(datastore, client):
    url = 'https://www.cyber.gc.ca/en/theme-gcwu-fegc/assets/wmms.svg'
    res = client.ingest(url=url, params={"deep_scan": True, "ignore_cache": True, "priority": 100})
    assert res.get('ingest_id', None) is not None
