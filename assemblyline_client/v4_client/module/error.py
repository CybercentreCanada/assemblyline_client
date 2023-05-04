from assemblyline_client.v4_client.common.utils import api_path_by_module, api_path


class Error(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, error_key):
        """\
Get the error details for a given error key

Required:
error_key:  Error key to get the details for (string)

Throws a Client exception if the error does not exist.
"""
        return self._connection.get(api_path('error', error_key))

    def list(self, query=None, offset=0, rows=10, sort=None, use_archive=False, track_total_hits=None):
        """\
List all errors in the system (per page)

Required:
offset            : Offset at which we start giving errors
query             : Query to apply to the error list
rows              : Number of errors to return
sort              : Sort order
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)
"""
        kw = {
            'offset': offset,
            'query': query,
            'rows': rows,
            'sort': sort
        }
        if use_archive:
            kw['use_archive'] = ''
        if track_total_hits:
            kw['track_total_hits'] = track_total_hits
        return self._connection.get(api_path_by_module(self, **kw))
