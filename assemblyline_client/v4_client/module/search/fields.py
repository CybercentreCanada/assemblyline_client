from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, api_path


class Fields(object):
    def __init__(self, connection):
        self._connection = connection

    def _do_fields(self, index):
        if index not in SEARCHABLE:
            raise ClientError("Index %s is not searchable" % index, 400)

        path = api_path('search', 'fields', index)
        return self._connection.get(path)

    def alert(self):
        """\
List all fields details for the alert collection.
"""
        return self._do_fields('alert')

    def badlist(self):
        """\
List all fields details for the badlist collection.
"""
        return self._do_fields('badlist')

    def file(self):
        """\
List all fields details for the file collection.
"""
        return self._do_fields('file')

    def heuristic(self):
        """\
List all fields details for the heuristic collection.
"""
        return self._do_fields('heuristic')

    def result(self):
        """\
List all fields details for the result collection.
"""
        return self._do_fields('result')

    def safelist(self):
        """\
List all fields details for the safelist collection.
"""
        return self._do_fields('safelist')

    def signature(self):
        """\
List all fields details for the signature collection.
"""
        return self._do_fields('signature')

    def submission(self):
        """\
List all fields details for the submission collection.
"""
        return self._do_fields('submission')

    def workflow(self):
        """\
List all fields details for the workflow collection.
"""
        return self._do_fields('workflow')
