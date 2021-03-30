
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_workflow(datastore, client):
    workflow_id = random_id_from_collection(datastore, 'workflow')
    workflow_data = datastore.workflow.get(workflow_id, as_obj=False)

    res = client.workflow(workflow_id)

    assert res == workflow_data


def test_label_list(datastore, client):
    workflow_id = random_id_from_collection(datastore, 'workflow')
    workflow_data = datastore.workflow.get(workflow_id, as_obj=False)
    res = client.workflow.labels()

    assert isinstance(res, list)
    for label in workflow_data['labels']:
        assert label in res
