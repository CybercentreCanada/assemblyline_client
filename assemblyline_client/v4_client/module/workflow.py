from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module


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
        return self._connection.get(api_path('workflow', workflow_id))

    def labels(self):
        """\
Return the list of potential labels for the workflows
"""
        return self._connection.get(api_path_by_module(self))
