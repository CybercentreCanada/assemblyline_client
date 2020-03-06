
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_user(datastore, client):
    user_id = random_id_from_collection(datastore, 'user')
    user_data = datastore.user.get(user_id, as_obj=False)

    res = client.user(user_id)

    assert res['name'] == user_data['name']
    assert res['uname'] == user_data['uname']
    assert 'otp_sk' not in res
    assert '2fa_enabled' in res
    assert 'security_token_enabled' in res
    assert sorted(res['security_tokens']) == sorted(list(user_data['security_tokens'].keys()))


def test_get_submission_params(datastore, client):
    user_id = random_id_from_collection(datastore, 'user')

    res = client.user.submission_params(user_id)

    assert not {'download_encoding', 'hide_raw_results'}.issubset(set(res.keys()))
    assert {'deep_scan', 'groups', 'ignore_cache', 'submitter'}.issubset(set(res.keys()))
    assert res['submitter'] == user_id
