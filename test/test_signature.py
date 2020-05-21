import random

import pytest

from copy import deepcopy

from assemblyline_client import ClientError

try:
    from assemblyline.common.isotime import now_as_iso
    from assemblyline.common.uid import get_random_id
    from assemblyline.odm.random_data import random_model_obj
    from assemblyline.odm.models.signature import Signature

    from utils import random_id_from_collection
except ImportError:
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_add_update(datastore, client):
    random_sig = random_model_obj(Signature, as_json=True)

    res = client.signature.add_update(random_sig)
    assert res['success']
    datastore.signature.commit()

    # This signature should fail
    random_sig_fail = deepcopy(random_sig)
    random_sig_fail['signature_id'] = "FAIL"

    with pytest.raises(ClientError):
        client.signature.add_update(random_sig_fail)
        datastore.signature.commit()

    res = client.signature.add_update(random_sig_fail, dedup_name=False)
    assert res['success']


# noinspection PyUnusedLocal
def test_add_update_many(datastore, client):
    # Insert a dummy signature
    source = "source"
    s_type = "type"
    sig_list = []
    for x in range(10):
        data = random_model_obj(Signature).as_primitives(hidden_fields=True)
        data['status'] = "DEPLOYED"
        data['source'] = source
        data['type'] = s_type
        sig_list.append(data)

    res = client.signature.add_update_many(source, s_type, sig_list)
    assert res == {'errors': False, 'success': 10, 'skipped': []}

    # Test the signature data
    datastore.signature.commit()
    data = Signature(random.choice(sig_list)).as_primitives()
    key = "%s_%s_%s" % (data['type'], data['source'], data['signature_id'])
    added_sig = datastore.signature.get(key, as_obj=False)
    assert data == added_sig

    # This signature should fail
    random_sig_fail = deepcopy(data)
    random_sig_fail['signature_id'] = "FAIL"
    res = client.signature.add_update_many(source, s_type, [random_sig_fail])
    assert res['success'] == 0
    random_key = "%s_%s_%s" % (random_sig_fail['type'], random_sig_fail['source'], random_sig_fail['signature_id'])
    assert random_key in res['skipped']

    # Does not fail if we don't dedup names
    res = client.signature.add_update_many(source, s_type, [random_sig_fail], dedup_name=False)
    assert res['success'] == 1


def test_get_signature(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature')

    signature_data = datastore.signature.get(signature_id, as_obj=False)

    res = client.signature(signature_id)
    assert res == signature_data


def test_download_file_handle(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature', q="type:yara")
    query = "id:{}".format(signature_id)
    output = "/tmp/sigs_{}_obj".format(get_random_id())
    res = client.signature.download(query=query, output=open(output, 'wb'))
    assert res

    found = False

    with open(output, 'rb') as fh:
        if b"yara/sample_rules.yar" in fh.read():
            found = True

    if not found:
        pytest.fail("This is not the signature file that we were expecting.")


def test_download_path(datastore, client):
    query = "id:*"
    output = "/tmp/sigs_{}".format(get_random_id())
    res = client.signature.download(output=output, query=query)
    assert res

    has_yara_samples = False
    has_suricata_samples = False

    with open(output, 'rb') as fh:
        for l in fh:
            if b"yara/sample_rules.yar" in l:
                has_yara_samples = True
            if b"suricata/sample_suricata.rules" in l:
                has_suricata_samples = True

            if has_suricata_samples and has_suricata_samples:
                break

    if not has_yara_samples and not has_suricata_samples:
        pytest.fail("This is not the signature file that we were expecting.")


def test_download_raw(datastore, client):
    query = "id:*"
    res = client.signature.download(query=query)

    assert res[:2] == b"PK"
    assert b"yara/sample_rules.yar" in res
    assert b"suricata/sample_suricata.rules" in res


def test_stats(datastore, client):
    res = client.signature.stats()
    assert len(res) == datastore.signature.search('id:*')['total']


def test_update_available(datastore, client):
    res = client.signature.update_available()
    assert res['update_available']


def test_update_available_past(datastore, client):
    check_date = now_as_iso(-24 * 60 * 60)
    res = client.signature.update_available(since=check_date)
    assert res['update_available']


def test_update_available_future(datastore, client):
    check_date = now_as_iso(24 * 60 * 60)
    res = client.signature.update_available(since=check_date)
    assert not res['update_available']
