
import pytest

try:
    from assemblyline_client.v4_client.common.utils import ClientError
    from utils import random_id_from_collection
except ImportError:
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    alert_data = datastore.alert.get(alert_id, as_obj=False)
    res = client.alert(alert_id)
    assert res['alert_id'] == alert_id
    assert alert_data == res


def test_label(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    res = client.alert.label(alert_id, "L1", "L2")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "L1" in alert_data.label
    assert "L2" in alert_data.label

    res = client.alert.label(alert_id, "L3")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "L3" in alert_data.label


def test_owner(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    alert_data = datastore.alert.get(alert_id)
    if alert_data.owner is None:
        res = client.alert.ownership(alert_id)
        assert res['success']
    else:
        with pytest.raises(ClientError):
            client.alert.ownership(alert_id)

        alert_data.owner = None
        datastore.alert.save(alert_id, alert_data)

        res = client.alert.ownership(alert_id)
        assert res['success']


def test_priority(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    res = client.alert.priority(alert_id, "HIGH")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "HIGH" in alert_data.priority


def test_status(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    res = client.alert.status(alert_id, "ASSESS")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "ASSESS" in alert_data.status
