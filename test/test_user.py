import random

import pytest
from assemblyline_client.v4_client.common.utils import ClientError

from assemblyline.odm.models.user_settings import (
    DEFAULT_SUBMISSION_PROFILE_SETTINGS,
    DEFAULT_USER_PROFILE_SETTINGS,
)

try:
    from utils import random_id_from_collection

    from assemblyline.odm.models.user import User
    from assemblyline.odm.models.user_favorites import Favorite
    from assemblyline.odm.random_data import random_model_obj
except ImportError:
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_add(datastore, client):
    user_id = 'to_be_added'

    user_data = random_model_obj(User).as_primitives()
    user_data['email'] = user_data['email']
    user_data['uname'] = user_id

    assert datastore.user.get(user_id, as_obj=False) is None

    res = client.user.add(user_id, user_data)
    assert res['success']

    assert datastore.user.get(user_id, as_obj=False) == user_data


def test_avatar(datastore, client):
    # Test adding avatar (1x1 white gif)
    new_avatar = "data:image/gif;base64,R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
    res = client.user.avatar.update('admin', new_avatar)
    assert res['success']

    # Test getting the our own avatar
    avatar = client.user.avatar('admin')
    assert avatar == new_avatar

    # As an admin, test adding another user's avatar
    res = client.user.avatar.update('user', new_avatar)
    assert res['success']


def test_favorites(datastore, client):
    possible_fav_types = {'alert', 'error', 'search', 'signature', 'submission'}
    user_id = random_id_from_collection(datastore, 'user')

    # Test getting favorites
    favorites = client.user.favorites(user_id)
    assert possible_fav_types.issubset(set(favorites.keys()))

    # Test adding favorites
    fav_type = random.choice(list(possible_fav_types))
    new_fav = random_model_obj(Favorite, as_json=True)
    res = client.user.favorites.add(user_id, fav_type, new_fav)
    assert res['success']

    # Test if favorite was added
    found = False
    for fav in datastore.user_favorites.get(user_id, as_obj=False)[fav_type]:
        if fav['name'] == new_fav['name'] and fav['query'] == new_fav['query']:
            found = True
            break
    assert found

    # Test delete favorite
    client.user.favorites.delete(user_id, fav_type, new_fav['name'])
    assert res['success']

    # Test if favorite was deleted
    found = False
    for fav in datastore.user_favorites.get(user_id, as_obj=False)[fav_type]:
        if fav['name'] == new_fav['name'] and fav['query'] == new_fav['query']:
            found = True
            break
    assert not found

    # Test update favorites
    new_favs = {
        'alert': [new_fav],
        'error': [new_fav],
        'search': [new_fav],
        'signature': [new_fav],
        'submission': [new_fav]
    }
    res = client.user.favorites.update(user_id, new_favs)
    assert res['success']

    # Test is favorites were really updated
    for favs in datastore.user_favorites.get(user_id, as_obj=False).values():
        assert favs[0]['name'] == new_fav['name']


def test_delete(datastore, client):
    user_id = 'to_be_deleted'
    user_data = random_model_obj(User)
    user_data['uname'] = user_id
    datastore.user.save(user_id, user_data)
    assert datastore.user.get(user_id, as_obj=False) is not None

    res = client.user.delete(user_id)
    assert res['success']

    datastore.user.commit()

    assert datastore.user.get(user_id, as_obj=False) is None


def test_get(datastore, client):
    user_id = random_id_from_collection(datastore, 'user')
    user_data = datastore.user.get(user_id, as_obj=False)

    res = client.user(user_id)

    assert res['name'] == user_data['name']
    assert res['uname'] == user_data['uname']
    assert 'otp_sk' not in res
    assert '2fa_enabled' in res
    assert 'security_token_enabled' in res
    assert sorted(res['security_tokens']) == sorted(list(user_data['security_tokens'].keys()))


def test_list(datastore, client):
    res = client.user.list()
    assert 'admin' in [x['uname'] for x in res['items']]

    res = client.user.list(query="id:admin")
    assert 'admin' in [x['uname'] for x in res['items']]
    assert res['total'] == 1


def test_settings(datastore, client):
    user_id = random_id_from_collection(datastore, 'user')

    # Test getting settings
    settings = client.user.settings(user_id)

    # Ensure general settings are present
    assert set(DEFAULT_USER_PROFILE_SETTINGS.keys()).issubset(set(settings.keys()))

    # Ensure submission settings are present under "submission_profiles"
    for submission_profile in settings['submission_profiles'].values():
        assert set(DEFAULT_SUBMISSION_PROFILE_SETTINGS.keys()).issubset(set(submission_profile.keys()))

    # Test updating settings
    new_password = "zippy"
    settings['default_zip_password'] = new_password

    res = client.user.settings.update(user_id, settings)
    assert res['success']

    # Validate changes were applied
    datastore.user_settings.commit()
    assert new_password == datastore.user_settings.get(user_id, as_obj=False)['default_zip_password']


def test_submission_params(datastore, client):
    user_id = random_id_from_collection(datastore, 'user')

    res = client.user.submission_params(user_id)

    assert not {'download_encoding', 'hide_raw_results'}.issubset(set(res.keys()))
    assert {'deep_scan', 'groups', 'ignore_cache', 'submitter'}.issubset(set(res.keys()))
    assert res['submitter'] == user_id


def test_tos(datastore, client):
    res = client.user.tos('admin')
    assert res['success']
    assert datastore.user.get('admin', as_obj=False)['agrees_with_tos'] is not None

    with pytest.raises(ClientError):
        client.user.tos('user')


def test_update(datastore, client):
    new_name = "TEST_NAME!"

    user_id = 'user'
    user_data = datastore.user.get(user_id, as_obj=False)
    assert user_data is not None

    user_data['name'] = new_name
    res = client.user.update(user_id, user_data)
    assert res['success']

    assert datastore.user.get(user_id, as_obj=False)['name'] == new_name


def test_whoami(datastore, client):
    res = client.user.whoami()
    assert {'c12nDef', 'configuration', 'username', 'indexes'}.issubset(set(res.keys()))
    assert res['username'] == 'admin'
