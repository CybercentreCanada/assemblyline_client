
from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, api_path


class Grouped(object):
    def __init__(self, connection):
        self._connection = connection

    def _do_grouped(self, index, field, **kwargs):
        if index not in SEARCHABLE:
            raise ClientError("Index %s is not searchable" % index, 400)

        filters = kwargs.pop('filters', None)
        if filters is not None:
            if isinstance(filters, str):
                filters = [filters]

            filters = [('filters', fq) for fq in filters]

        kwargs = {k: v for k, v in kwargs.items() if v is not None and k != 'filters'}
        if filters is not None:
            kwargs['params_tuples'] = filters
        path = api_path('search', 'grouped', index, field, **kwargs)
        return self._connection.get(path)

    def alert(self, field, group_sort=None, limit=None, query=None, filters=None,
              offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search alert collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('alert', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def badlist(self, field, group_sort=None, limit=None, query=None, filters=None,
                offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search badlist collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('badlist', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def file(self, field, group_sort=None, limit=None, query=None, filters=None,
             offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search file collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('file', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def heuristic(self, field, group_sort=None, limit=None, query=None, filters=None,
                  offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search heuristic collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('heuristic', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def result(self, field, group_sort=None, limit=None, query=None, filters=None,
               offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search result collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('result', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def safelist(self, field, group_sort=None, limit=None, query=None, filters=None,
                 offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search safelist collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('safelist', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def signature(self, field, group_sort=None, limit=None, query=None, filters=None,
                  offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search signature collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('signature', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def submission(self, field, group_sort=None, limit=None, query=None, filters=None,
                   offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search submission collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('submission', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)

    def workflow(self, field, group_sort=None, limit=None, query=None, filters=None,
                 offset=None, rows=None, sort=None, fl=None, timeout=None):
        """\
Search workflow collection and group result to a given field

Required:
field   : Field used to group the results

Optional:
group_sort : Field used for sorting items in the groups with direction (string: ex. 'id desc')
limit      : Maximum number of items returned per group (integer)
query      : lucene query (string)
filters    : Additional lucene queries used to filter the data (list of strings)
offset     : Offset at which the query items should start (integer)
rows       : Number of records to return (integer)
sort       : Field used for sorting with direction (string: ex. 'id desc')
fl         : List of fields to return (comma separated string of fields)
timeout    : Maximum execution time in milliseconds (integer)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_grouped('workflow', field, group_sort=group_sort, limit=limit, query=query, filters=filters,
                                offset=offset, rows=rows, sort=sort, fl=fl, timeout=timeout)
