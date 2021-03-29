
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


def test_grouped(datastore, client):
    res = client.alert.grouped('file.sha256', q='alert_id:*', no_delay=True)

    assert 'counted_total' in res
    assert 'items' in res
    assert 'offset' in res
    assert 'rows' in res
    assert 'total' in res
    assert 'tc_start' in res

    assert res['total'] >= len(res['items'])
    assert len(res['items']) <= res['rows']


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


def test_labels(datastore, client):
    res = client.alert.labels(no_delay=True)
    assert isinstance(res, dict)
    for v in res.values():
        assert isinstance(v, int)


def test_list(datastore, client):
    res = client.alert.list(no_delay=True)

    assert 'items' in res
    assert 'offset' in res
    assert 'rows' in res
    assert 'total' in res

    assert res['total'] >= len(res['items'])
    assert len(res['items']) <= res['rows']


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


def test_priorities(datastore, client):
    res = client.alert.priorities(no_delay=True)
    assert isinstance(res, dict)
    for k, v in res.items():
        assert k in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        assert isinstance(v, int)


def test_related(datastore, client):
    res = client.alert.related(q='alert_id:*')
    assert isinstance(res, list)
    for v in res:
        assert isinstance(v, str)


def test_statistics(datastore, client):
    res = client.alert.statistics(no_delay=True)
    assert isinstance(res, dict)
    for field, stats in res.items():
        assert isinstance(field, str)
        for (value, count) in stats.items():
            assert isinstance(value, str)
            assert isinstance(count, int)


def test_status(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    res = client.alert.status(alert_id, "ASSESS")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "ASSESS" in alert_data.status


def test_statuses(datastore, client):
    res = client.alert.statuses(no_delay=True)
    assert isinstance(res, dict)
    for k, v in res.items():
        assert k in ['ASSESS', 'MALICIOUS', 'NON-MALICIOUS', 'TRIAGE']
        assert isinstance(v, int)


def test_verdict(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')

    # Set alert malicious
    res = client.alert.verdict(alert_id, "malicious")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "admin" in alert_data.verdict.malicious

    # Set alert non-malicious
    res = client.alert.verdict(alert_id, "non_malicious")
    assert res['success']
    alert_data = datastore.alert.get(alert_id)
    assert "admin" in alert_data.verdict.non_malicious
