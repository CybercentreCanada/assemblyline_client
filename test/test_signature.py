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


def test_get_signature(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature')

    signature_data = datastore.signature.get(signature_id, as_obj=False)

    res = client.signature(signature_id)
    assert res == signature_data


def test_download_file_handle(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature')
    query = "id:{}".format(signature_id)
    output = "/tmp/sigs_{}_obj".format(get_random_id())
    res = client.signature.download(query=query, output=open(output, 'wb'), safe=False)
    assert res

    has_yara_samples = False
    has_suricata_samples = False

    with open(output, 'rb') as fh:
        for l in fh:
            if signature_id.startswith('yara') and b"yara/sample_rules.yar" in l:
                has_yara_samples = True
                break
            elif signature_id.startswith('suricata') and b"suricata/sample_suricata.rules" in l:
                has_suricata_samples = True
                break

    if not has_yara_samples and not has_suricata_samples:
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
