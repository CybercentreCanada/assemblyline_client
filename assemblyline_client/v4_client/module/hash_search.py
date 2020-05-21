from assemblyline_client.v4_client.common.utils import api_path


class HashSearch(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, h, db=None, max_timeout=None):
        """\
Perform a hash search for the given md5, sha1 or sha256.

Required:
h       : Hash - md5, sha1 or sha256 (string)

Optional:
db          : Data sources to query (list of strings).
max_timeout : Maximum amount of time to wait for response, in seconds (float).

Note: Not all hash types are supported by all data sources.
"""
        if db is None:
            db = []

        kw = {}
        if db:
            kw['db'] = '|'.join(db)

        if max_timeout:
            kw['max_timeout'] = float(max_timeout)

        return self._connection.get(api_path('hash_search', h, **kw))

    def list_data_sources(self):
        """Return the hash search data sources available."""
        return self._connection.get(api_path('hash_search/list_data_sources'))
