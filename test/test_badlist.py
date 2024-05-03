import hashlib

try:
    from utils import random_id_from_collection
    from assemblyline.odm.randomizer import get_random_hash
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_check_hash(datastore, client):
    badlist_id = random_id_from_collection(datastore, 'badlist')
    badlist_obj = datastore.badlist.get(badlist_id, as_obj=False)

    res = client.badlist(badlist_id)
    assert res is not None

    assert res == badlist_obj


def test_check_ssdeep(datastore, client):
    badlist_obj = datastore.badlist.search('hashes.ssdeep:*', fl="*", rows=1, as_obj=False)['items'][0]

    res = client.badlist.ssdeep(badlist_obj['hashes']['ssdeep'])
    assert res is not None

    assert res[0] == badlist_obj


def test_check_tlsh(datastore, client):
    badlist_obj = datastore.badlist.search('hashes.tlsh:*', fl="*", rows=1, as_obj=False)['items'][0]

    res = client.badlist.tlsh(badlist_obj['hashes']['tlsh'])
    assert res is not None

    assert res[0] == badlist_obj


def test_add_file_to_badlist(datastore, client):
    sha256 = get_random_hash(64)
    badlist_file = {
        "classification": "TLP:W",
        "enabled": True,
        "attribution": {"actor": "SPAMMER"},
        "file": {
            "name": ["file.txt"],
            "size": 12345,
            "type": "document/text"},
        "hashes": {
            "md5": get_random_hash(32),
            "sha1": get_random_hash(40),
            "sha256": sha256,
        },
        "sources": [
            {"classification": "TLP:W",
             "name": "SPAM",
             "reason": [
                     "It's spam",
                     "This is clearly spam"
             ],
             "type": "external"},
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["Yup clearly spam"],
             "type": "user"}
        ],
        "type": "file"
    }

    res = client.badlist.add_update(badlist_file)
    assert res['success']
    inserted_file = datastore.badlist.get(sha256, as_obj=False)
    assert inserted_file is not None
    assert inserted_file.get('hashes', {}).get('sha256', None) == sha256


def test_add_tag_to_badlist(datastore, client):
    badlist_tag = {
        "classification": "TLP:W",
        "enabled": True,
        "sources": [
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["This is a known bad domain"],
             "type": "user"}
        ],
        "tag": {
            "type": "network.static.domain",
            "value": "bad.ca"
        },
        "type": "tag"
    }
    hashed_value = f"{badlist_tag['tag']['type']}: {badlist_tag['tag']['value']}".encode('utf8')
    sha256 = hashlib.sha256(hashed_value).hexdigest()
    res = client.badlist.add_update(badlist_tag)
    assert res['success']
    inserted_tag = datastore.badlist.get(sha256, as_obj=False)
    assert inserted_tag is not None
    assert inserted_tag.get("tag", {}).get("value", None) == 'bad.ca'


def test_add_multiple_to_badlist(datastore, client):
    # A bad tag
    badlist_tag = {
        "classification": "TLP:W",
        "enabled": True,
        "sources": [
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["This is a known bad domain"],
             "type": "user"}
        ],
        "tag": {
            "type": "network.static.domain",
            "value": "bad2.ca"
        },
        "type": "tag"
    }
    tag_hashed_value = f"{badlist_tag['tag']['type']}: {badlist_tag['tag']['value']}".encode('utf8')
    tag_sha256 = hashlib.sha256(tag_hashed_value).hexdigest()

    # A bad file
    sha256 = get_random_hash(64)
    badlist_file = {
        "classification": "TLP:W",
        "enabled": True,
        "attribution": {"actor": "MULTI"},
        "file": {
            "name": ["file2.txt"],
            "size": 123456,
            "type": "document/text"},
        "hashes": {
            "md5": get_random_hash(32),
            "sha1": get_random_hash(40),
            "sha256": sha256,
        },
        "sources": [
            {"classification": "TLP:W",
             "name": "SPAM",
             "reason": [
                     "It's spam",
                     "This is clearly spam"
             ],
             "type": "external"},
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["Yup clearly spam"],
             "type": "user"}
        ],
        "type": "file"
    }

    res = client.badlist.add_update_many([badlist_tag, badlist_file])
    assert res['success']

    # Check tag
    inserted_tag = datastore.badlist.get(tag_sha256, as_obj=False)
    assert inserted_tag is not None
    assert inserted_tag.get("tag", {}).get("value", None) == 'bad2.ca'

    # Check File
    inserted_file = datastore.badlist.get(sha256, as_obj=False)
    assert inserted_file is not None
    assert inserted_file.get('hashes', {}).get('sha256', None) == sha256


def test_delete_from_badlist(datastore, client):
    badlist_id = random_id_from_collection(datastore, 'badlist')
    res = client.badlist.delete(badlist_id)
    assert res['success']
    assert datastore.badlist.get(badlist_id, as_obj=False) is None


def test_enable_disable_badlist(datastore, client):
    old_badlist = None
    while not old_badlist:
        badlist_id = random_id_from_collection(datastore, 'badlist')
        old_badlist = datastore.badlist.get(badlist_id, as_obj=False)

    res = client.badlist.set_enabled(badlist_id, not old_badlist["enabled"])
    assert res['success']
    assert datastore.badlist.get(badlist_id, as_obj=False)["enabled"] != old_badlist["enabled"]
