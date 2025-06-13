try:
    from assemblyline.odm.random_data import random_model_obj
    from assemblyline.odm.models.workflow import Workflow

    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys

    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_add(datastore, client):
    new_workflow = random_model_obj(Workflow, as_json=True)
    res = client.workflow.add(new_workflow)
    assert res["success"]

    saved_workflow = datastore.workflow.get(res["workflow_id"], as_obj=False)
    assert saved_workflow is not None
    assert saved_workflow["query"] == new_workflow["query"]


def test_delete(datastore, client):
    workflow_id = random_id_from_collection(datastore, "workflow")
    res = client.workflow.delete(workflow_id)
    assert res["success"]

    datastore.workflow.commit()

    assert datastore.workflow.get(workflow_id) is None


def test_get(datastore, client):
    workflow_id = random_id_from_collection(datastore, "workflow")
    workflow_data = datastore.workflow.get(workflow_id, as_obj=False)

    res = client.workflow(workflow_id)

    assert res == workflow_data


def test_run(datastore, client):

    # setting up workflow to run on any alert
    workflow_id = random_id_from_collection(datastore, "workflow")
    workflow_data = datastore.workflow.get(workflow_id, as_obj=False)
    workflow_data["query"] = "*"
    datastore.workflow.save(workflow_id, workflow_data)
    datastore.workflow.commit()

    # success should be true to run workflow
    res = client.workflow.run(workflow_id)
    datastore.alert.commit()
    assert res["success"]

    assert datastore.alert.search(f'events.entity_id:"{workflow_id}"', rows=1)["total"]


def test_label_list(datastore, client):
    workflow_id = random_id_from_collection(datastore, "workflow")
    workflow_data = datastore.workflow.get(workflow_id, as_obj=False)
    res = client.workflow.labels()

    assert isinstance(res, list)
    for label in workflow_data["labels"]:
        assert label in res


def test_list(datastore, client):
    res = client.workflow.list()
    assert res["total"] == datastore.workflow.search("*:*", rows=0)["total"]


def test_update(datastore, client):
    new_query = "NEW TEST QUERY"
    workflow_id = random_id_from_collection(datastore, "workflow")
    updated_data = datastore.workflow.get(workflow_id, as_obj=False)
    updated_data["query"] = new_query

    res = client.workflow.update(workflow_id, updated_data)
    assert res["success"]
    assert datastore.workflow.get(workflow_id, as_obj=False)["query"] == new_query
