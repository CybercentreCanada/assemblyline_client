
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
    res = client.search.facet.alert('al.ip', "id:{}".format(alert_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_file(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    res = client.search.facet.file('type', "id:{}".format(file_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_heuristic(datastore, client):
    heuristic_id = random_id_from_collection(datastore, 'heuristic')
    res = client.search.facet.heuristic('filetype', "id:{}".format(heuristic_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_result(datastore, client):
    result_id = random_id_from_collection(datastore, 'result')
    res = client.search.facet.result('response.service_name', "id:{}".format(result_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_signature(datastore, client):
    signature_id = random_id_from_collection(datastore, 'signature')
    res = client.search.facet.signature('status', "id:{}".format(signature_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_submission(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    res = client.search.facet.submission('params.submitter', "id:{}".format(submission_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_workflow(datastore, client):
    workflow_id = random_id_from_collection(datastore, 'workflow')
    res = client.search.facet.workflow('name', "id:{}".format(workflow_id), mincount=1)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1
