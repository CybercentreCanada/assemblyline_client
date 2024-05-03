
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_label(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')

    res = client.alert.batch.label('alert_id:{}'.format(alert_id), ["B1", "B2"], fq_list=["id:*", "label:*"])
    assert res['success'] == 1

    alert_data = datastore.alert.get(alert_id)
    assert "B1" in alert_data.label
    assert "B2" in alert_data.label


def test_owner(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')

    # Make sure the batch query has something to do
    alert_data = datastore.alert.get(alert_id)
    alert_data.owner = None
    datastore.alert.save(alert_id, alert_data)
    datastore.alert.commit()

    res = client.alert.batch.ownership('alert_id:{}'.format(alert_id), fq_list=["id:*", "label:*"])
    assert res['success'] == 1

    alert_data = datastore.alert.get(alert_id)
    assert alert_data.owner == 'admin'


def test_priority(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')

    res = client.alert.batch.priority('alert_id:{}'.format(alert_id), "HIGH", fq_list=["id:*", "label:*"])
    assert res['success'] == 1

    alert_data = datastore.alert.get(alert_id)
    assert "HIGH" in alert_data.priority


def test_remove_label(datastore, client):
    import random
    alert_id = random_id_from_collection(datastore, 'alert')
    alert = datastore.alert.get(alert_id)
    labels_to_remove = []
    while not labels_to_remove:
        labels_to_remove = [label for label in alert.label if random.randint(0, 1) == 1]

    res = client.alert.batch.remove_label('alert_id:{}'.format(alert_id), labels_to_remove, fq_list=["id:*", "label:*"])
    assert res['success'] == 1

    alert_data = datastore.alert.get(alert_id)
    assert all([label not in alert_data.label for label in labels_to_remove])


def test_status(datastore, client):
    has_labels = False
    while not has_labels:
        alert_id = random_id_from_collection(datastore, 'alert')
        alert = datastore.alert.get(alert_id)
        has_labels = len(alert.label) != 0

    res = client.alert.batch.status('alert_id:{}'.format(alert_id), "ASSESS", fq_list=["id:*", "label:*"])
    assert res['success'] == 1

    alert_data = datastore.alert.get(alert_id)
    assert "ASSESS" in alert_data.status
