from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, get_function_kwargs


class Workflow(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, workflow_id):
        """\
Get the detail for a workflow

Required:
workflow_id: Id of the workflow (string)

Throws a Client exception if the workflow does not exist.
"""
        return self._connection.get(api_path("workflow", workflow_id))

    def add(self, workflow):
        """\
Add a workflow to the system

Required:
workflow  : data of the workflow

Throws a Client exception if the workflow information is wrong.
"""
        return self._connection.put(api_path("workflow"), json=workflow)

    def delete(self, workflow_id):
        """\
Remove the specified workflow.

Required:
workflow_id : id of the workflow

Throws a Client exception if the workflow does not exist.
"""
        return self._connection.delete(api_path("workflow", workflow_id))

    def labels(self):
        """\
Return the list of potential labels for the workflows
"""
        return self._connection.get(api_path_by_module(self))

    def list(self, query="*:*", rows=10, offset=0):
        """\
List the potential workflows (per page)

Required:
query     : query to filter the workflow
rows      : number of items returned
offset    : offset in the results to start returning data
"""
        return self._connection.get(api_path("search", "workflow", **get_function_kwargs("self")))

    def update(self, workflow_id, workflow):
        """\
Update a workflow.

Required:
workflow_id : id of the workflow
workflow    : data of the workflow

Throws a Client exception if the workflow does not exist.
"""
        return self._connection.post(api_path("workflow", workflow_id), json=workflow)

    def run(self, workflow_id):
        """\
 Run the specified workflow against all existing alerts that match the query.

Required:
workflow_id : id of the workflow

Throws a Client exception if the workflow does not exist.
"""
        return self._connection.get(api_path("workflow", workflow_id, "run"))
