
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_result(datastore, client):
    result_id = random_id_from_collection(datastore, 'result')
    res = client.result(result_id)
    ds_res = datastore.result.get(result_id, as_obj=False)
    assert res['response'] == ds_res['response']
    assert res['sha256'] == ds_res['sha256']
    assert res['sha256'] == result_id[:64]


def test_get_result_error(datastore, client):
    error_id = random_id_from_collection(datastore, 'error')
    res = client.result.error(error_id)
    assert res == datastore.error.get(error_id, as_obj=False)


def test_get_multiple_error(datastore, client):
    m_results = []
    m_errors = []
    for _ in range(5):
        m_results.append(random_id_from_collection(datastore, 'result'))
    for _ in range(2):
        m_errors.append(random_id_from_collection(datastore, 'error'))

    m_results = list(set(m_results))
    m_errors = list(set(m_errors))

    res = client.result.multiple(error=m_errors, result=m_results)
    assert sorted(list(res['error'].keys())) == sorted(m_errors)
    assert sorted(list(res['result'].keys())) == sorted(m_results)

    ds_result = datastore.get_multiple_results(m_results)
    for res_key in m_results:
        assert res['result'][res_key]['response'] == ds_result[res_key]['response']
        assert res['result'][res_key]['sha256'] == ds_result[res_key]['sha256']
        assert res['result'][res_key]['sha256'] == res_key[:64]

    assert res['error'] == datastore.error.multiget(m_errors, as_dictionary=True, as_obj=False)
