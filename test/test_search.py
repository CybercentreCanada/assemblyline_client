
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
    res = client.search.alert("id:{}".format(alert_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == alert_id

    res = client.search.alert("id:*", offset=5)
    assert res['total'] > 1


def test_file(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.search.file("id:{}".format(file_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]["id"] == file_id

    res = client.search.file("id:*", rows=5)
    assert res['total'] > 1


def test_heuristic(datastore, client):
    heuristic_id = random_id_from_collection(datastore, 'heuristic')
    res = client.search.heuristic("id:{}".format(heuristic_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == heuristic_id

    res = client.search.heuristic("id:*", sort="id desc", fl="heur_id")
    assert res['total'] > 1


def test_result(datastore, client):
    result_id = random_id_from_collection(datastore, 'result')
    res = client.search.result("id:{}".format(result_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == result_id

    res = client.search.result("id:*", fl="response.score")
    assert res['total'] > 1


def test_signature(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature')
    res = client.search.signature("id:{}".format(signature_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == signature_id

    res = client.search.signature("id:*", filters=["id:yara_YAR_SAMPLE_CSE*", "name:*Shade*"])
    assert res['total'] == 1


def test_submission(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    res = client.search.submission("id:{}".format(submission_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == submission_id

    res = client.search.submission("id:*")
    assert res['total'] > 1


def test_safelist(datastore, client):
    safelist_id = random_id_from_collection(datastore, 'safelist')
    res = client.search.safelist("id:{}".format(safelist_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == safelist_id

    res = client.search.safelist("id:*")
    assert res['total'] > 1


def test_workflow(datastore, client):
    workflow_id = random_id_from_collection(datastore, 'workflow')
    res = client.search.workflow("id:{}".format(workflow_id), fl="id")
    assert res['total'] == 1
    assert res['items'][0]['id'] == workflow_id

    res = client.search.workflow("id:*", offset=5)
    assert res['total'] > 1
