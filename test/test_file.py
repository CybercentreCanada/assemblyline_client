import hashlib
import os

try:
    import cart
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_children(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission', q="file_count:[2 TO *]")
    submission_data = datastore.submission.get(submission_id)
    file_id = submission_data.files[0].sha256

    res = client.file.children(file_id)
    assert len(res) >= 1


def test_ascii(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')

    res = client.file.ascii(file_id)
    assert len(res) >= 1


def test_hex(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')

    res = client.file.hex(file_id)['content']
    assert res.startswith('00000000:')


def test_strings(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')

    res = client.file.strings(file_id)
    assert len(res) >= 1


# noinspection PyUnusedLocal
def test_download_to_obj(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.file.download(file_id)

    assert res[:4] == b"CART"


# noinspection PyUnusedLocal
def test_download_to_obj_raw(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.file.download(file_id, encoding="raw")

    assert hashlib.sha256(res).hexdigest() == file_id


# noinspection PyUnusedLocal
def test_download_to_obj_zip(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.file.download(file_id, encoding="zip")

    assert res[:2] == b"PK"


# noinspection PyUnusedLocal
def test_download_to_file(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    download_output = "/tmp/download_{}".format(file_id)
    try:
        client.file.download(file_id, output=download_output)

        assert open(download_output, 'rb').read(4) == b"CART"
        metadata = cart.get_metadata_only(download_output)
        assert file_id == metadata['sha256']
    finally:
        os.unlink(download_output)


# noinspection PyUnusedLocal
def test_download_to_file_handle(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    download_output = "/tmp/download_{}_fobj".format(file_id)
    try:
        client.file.download(file_id, output=open(download_output, "wb"))

        assert open(download_output, 'rb').read(4) == b"CART"
    finally:
        os.unlink(download_output)

# noinspection PyUnusedLocal
def test_delete_from_filestore(datastore, filestore, client):
    file_id = random_id_from_collection(datastore, 'file')

    # Delete file from filestore only
    # Shouldn't affect the related document in the datastore
    assert filestore.exists(file_id)
    assert client.file.delete_from_filestore(file_id)['success']
    assert not filestore.exists(file_id) and datastore.file.exists(file_id)


# noinspection PyUnusedLocal
def test_info(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.file.info(file_id)

    assert res['sha256'] == file_id


# noinspection PyUnusedLocal
def test_result(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.file.result(file_id)

    assert res['file_info']['sha256'] == file_id


# noinspection PyUnusedLocal
def test_result_for_service(datastore, client):
    result_id = random_id_from_collection(datastore, 'result')
    file_id, service_name, _ = result_id.split('.', 2)
    res = client.file.result(file_id, service=service_name)

    assert res['file_info']['sha256'] == file_id
    assert res['results'][0]['response']['service_name'] == service_name


# noinspection PyUnusedLocal
def test_score(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.file.score(file_id)

    assert res['file_info']['sha256'] == file_id
    for k in res['result_keys']:
        assert k[:64] == file_id
