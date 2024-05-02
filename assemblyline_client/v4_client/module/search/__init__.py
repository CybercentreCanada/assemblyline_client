import json

from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, api_path
from assemblyline_client.v4_client.module.search.facet import Facet
from assemblyline_client.v4_client.module.search.fields import Fields
from assemblyline_client.v4_client.module.search.grouped import Grouped
from assemblyline_client.v4_client.module.search.histogram import Histogram
from assemblyline_client.v4_client.module.search.stats import Stats
from assemblyline_client.v4_client.module.search.stream import Stream


class Search(object):
    def __init__(self, connection):
        self._connection = connection
        self.facet = Facet(connection)
        self.fields = Fields(connection)
        self.grouped = Grouped(connection)
        self.histogram = Histogram(connection)
        self.stats = Stats(connection)
        self.stream = Stream(connection, self._do_search)

    def _do_search(self, index, query, use_archive=False, track_total_hits=None, **kwargs):
        if index not in SEARCHABLE:
            raise ClientError("Index %s is not searchable" % index, 400)

        filters = kwargs.pop('filters', None)
        if filters is not None:
            if isinstance(filters, str):
                filters = [filters]

            kwargs['filters'] = filters

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs['query'] = query
        if use_archive:
            kwargs['use_archive'] = ''
        if track_total_hits:
            kwargs['track_total_hits'] = track_total_hits
        path = api_path('search', index)
        return self._connection.post(path, data=json.dumps(kwargs))

    def alert(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
              use_archive=False, track_total_hits=None):
        """\
Search alerts with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('alert', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def badlist(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
                use_archive=False, track_total_hits=None):
        """\
Search badlists with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('badlist', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def file(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
             use_archive=False, track_total_hits=None):
        """\
Search files with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('file', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def heuristic(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
                  use_archive=False, track_total_hits=None):
        """\
Search heuristics with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('heuristic', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def result(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
               use_archive=False, track_total_hits=None):
        """\
Search results with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('result', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def safelist(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
                 use_archive=False, track_total_hits=None):
        """\
Search safelist with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('safelist', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def signature(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
                  use_archive=False, track_total_hits=None):
        """\
Search signatures with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('signature', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def submission(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
                   use_archive=False, track_total_hits=None):
        """\
Search submissions with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('submission', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)

    def workflow(self, query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None,
                 use_archive=False, track_total_hits=None):
        """\
Search workflow with a lucene query.

Required:
query   : lucene query (string)

Optional:
filters           : Additional lucene queries used to filter the data (list of strings)
fl                : List of fields to return (comma separated string of fields)
offset            : Offset at which the query items should start (integer)
rows              : Number of records to return (integer)
sort              : Field used for sorting with direction (string: ex. 'id desc')
timeout           : Maximum execution time in milliseconds (integer)
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)

Returns all results.
"""
        return self._do_search('workflow', query, filters=filters, fl=fl, offset=offset,
                               rows=rows, sort=sort, timeout=timeout,
                               use_archive=use_archive, track_total_hits=track_total_hits)
