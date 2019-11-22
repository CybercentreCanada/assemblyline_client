from assemblyline_client.v4_client.common.utils import api_path


class Heuristics(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, heuristic_id):
        """\
Get a specific heuristic's details from the system.

Required:
heuristic_id: (string) ID of the heuristic.
"""
        return self._connection.get(api_path('heuristics', heuristic_id))

    def stats(self):
        """\
Gather statistics about all the heuristics in the system.

"""
        return self._connection.get(api_path('heuristics/stats'))
