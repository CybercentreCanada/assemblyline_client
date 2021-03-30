
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_error(datastore, client):
    error_id = random_id_from_collection(datastore, 'error')
    error_data = datastore.error.get(error_id, as_obj=False)

    res = client.error(error_id)
    assert res == error_data


def test_list_error(datastore, client):
    error_id = random_id_from_collection(datastore, 'error')

    res = client.error.list(rows=1000)
    assert error_id in [x['id'] for x in res['items']]
