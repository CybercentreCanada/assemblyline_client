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
    safelist_id = random_id_from_collection(datastore, 'safelist')
    safelist_obj = datastore.safelist.get(safelist_id, as_obj=False)

    res = client.safelist(safelist_id)
    assert res is not None

    assert res == safelist_obj


def test_add_file_to_safelist(datastore, client):
    sha256 = get_random_hash(64)
    safelist_file = {
        "classification": "TLP:W",
        "enabled": True,
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
             "name": "NSRL",
             "reason": [
                     "Found as test.txt on default windows 10 CD",
                     "Found as install.txt on default windows XP CD"
             ],
             "type": "external"},
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["We've seen this file many times and it leads to False positives"],
             "type": "user"}
        ],
        "type": "file"
    }

    res = client.safelist.add_update(safelist_file)
    assert res['success']
    inserted_file = datastore.safelist.get(sha256, as_obj=False)
    assert inserted_file is not None
    assert inserted_file.get('hashes', {}).get('sha256', None) == sha256


def test_add_tag_to_safelist(datastore, client):
    safelist_tag = {
        "classification": "TLP:W",
        "enabled": True,
        "sources": [
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["This is a known safe domain"],
             "type": "user"}
        ],
        "tag": {
            "type": "network.static.domain",
            "value": "google.ca"
        },
        "type": "tag"
    }
    hashed_value = f"{safelist_tag['tag']['type']}: {safelist_tag['tag']['value']}".encode('utf8')
    sha256 = hashlib.sha256(hashed_value).hexdigest()
    res = client.safelist.add_update(safelist_tag)
    assert res['success']
    inserted_tag = datastore.safelist.get(sha256, as_obj=False)
    assert inserted_tag is not None
    assert inserted_tag.get("tag", {}).get("value", None) == 'google.ca'


def test_add_multiple_to_safelist(datastore, client):
    # A safe tag
    safelist_tag = {
        "classification": "TLP:W",
        "enabled": True,
        "sources": [
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["This is a known safe domain"],
             "type": "user"}
        ],
        "tag": {
            "type": "network.static.domain",
            "value": "google.com"
        },
        "type": "tag"
    }
    tag_hashed_value = f"{safelist_tag['tag']['type']}: {safelist_tag['tag']['value']}".encode('utf8')
    tag_sha256 = hashlib.sha256(tag_hashed_value).hexdigest()

    # A safe file
    sha256 = get_random_hash(64)
    safelist_file = {
        "classification": "TLP:W",
        "enabled": True,
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
             "name": "NSRL",
             "reason": [
                     "Found as test.txt on default windows 10 CD",
                     "Found as install.txt on default windows XP CD"
             ],
             "type": "external"},
            {"classification": "TLP:W",
             "name": "admin",
             "reason": ["We've seen this file many times and it leads to False positives"],
             "type": "user"}
        ],
        "type": "file"
    }

    res = client.safelist.add_update_many([safelist_tag, safelist_file])
    assert res['success']

    # Check tag
    inserted_tag = datastore.safelist.get(tag_sha256, as_obj=False)
    assert inserted_tag is not None
    assert inserted_tag.get("tag", {}).get("value", None) == 'google.com'

    # Check File
    inserted_file = datastore.safelist.get(sha256, as_obj=False)
    assert inserted_file is not None
    assert inserted_file.get('hashes', {}).get('sha256', None) == sha256


def test_delete_from_safelist(datastore, client):
    try:
        safelist_id = random_id_from_collection(datastore, 'safelist')
        res = client.safelist.delete(safelist_id)
        assert res['success']
        assert datastore.safelist.get(safelist_id, as_obj=False) is None
    finally:
        # Make sure searches are ready for next tests
        datastore.safelist.commit()


def test_enable_disable_safelist(datastore, client):
    safelist_id = random_id_from_collection(datastore, 'safelist')
    old_safelist = datastore.safelist.get(safelist_id, as_obj=False)

    res = client.safelist.set_enabled(safelist_id, not old_safelist["enabled"])
    assert res['success']
    assert datastore.safelist.get(safelist_id, as_obj=False)["enabled"] != old_safelist["enabled"]
