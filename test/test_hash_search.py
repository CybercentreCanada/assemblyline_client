
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_list_datasources(datastore, client):
    res = client.hash_search.list_data_sources()
    assert res == ['al', 'alert']


def test_md5_search(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    file_data = datastore.file.get(file_id)

    res = client.hash_search(file_data.md5)

    assert res['al']['items'][0]['data']['md5'] == file_data.md5


def test_sha1_search(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    file_data = datastore.file.get(file_id)

    res = client.hash_search(file_data.sha1)

    assert res['al']['items'][0]['data']['sha1'] == file_data.sha1


# noinspection PyUnusedLocal
def test_sha256_search(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.hash_search(file_id)

    assert res['al']['items'][0]['data']['sha256'] == file_id


def test_sha256_search_with_specific_db(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.hash_search(file_id, db=['al'])

    assert res['al']['items'][0]['data']['sha256'] == file_id

    alert_id = random_id_from_collection(datastore, 'alert')
    alert_data = datastore.alert.get(alert_id)
    res = client.hash_search(alert_data.file.sha256, db=['alert'], max_timeout=1)

    assert len(res['alert']['items']) != 0
