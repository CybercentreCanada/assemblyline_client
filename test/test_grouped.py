
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_alert(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    res = client.search.grouped.alert("id", query="id:{}".format(alert_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['value'] == alert_id

    res = client.search.grouped.alert("status", query="id:*", offset=1)
    assert res['total'] > 1


def test_file(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.search.grouped.file("id", query="id:{}".format(file_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]["value"] == file_id

    res = client.search.grouped.file("classification", query="id:*", limit=2, rows=5)
    assert res['total'] > 1


def test_heuristic(datastore, client):
    heuristic_id = random_id_from_collection(datastore, 'heuristic')
    res = client.search.grouped.heuristic("id", query="id:{}".format(heuristic_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['value'] == heuristic_id

    res = client.search.grouped.heuristic("name", query="id:*", sort="id desc", fl="heur_id")
    assert res['total'] > 1


def test_result(datastore, client):
    result_id = random_id_from_collection(datastore, 'result')
    res = client.search.grouped.result("id", query="id:{}".format(result_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['value'] == result_id

    res = client.search.grouped.result("response.service_name", query="id:*", fl="response.score")
    assert res['total'] > 1


def test_signature(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature')
    res = client.search.grouped.signature("id", query="id:{}".format(signature_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['value'] == signature_id

    res = client.search.grouped.signature("name", query="id:*", filters=["id:yara_CSE*", "name:*Shade*"])
    assert res['total'] == 1


def test_submission(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    res = client.search.grouped.submission("id", query="id:{}".format(submission_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['value'] == submission_id

    res = client.search.grouped.submission("params.submitter", query="id:*")
    assert res['total'] > 1


def test_workflow(datastore, client):
    workflow_id = random_id_from_collection(datastore, 'workflow')
    res = client.search.grouped.workflow("id", query="id:{}".format(workflow_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['value'] == workflow_id

    res = client.search.grouped.workflow("creator", query="id:*", offset=5)
    assert res['total'] > 1
