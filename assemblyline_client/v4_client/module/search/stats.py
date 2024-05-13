from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, api_path


class Stats(object):
    def __init__(self, connection):
        self._connection = connection

    def _do_stats(self, index, field, **kwargs):
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
        path = api_path('search', 'stats', index, field, **kwargs)
        return self._connection.get(path)

    def alert(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the alert collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('alert', field, query=query, filters=filters, timeout=timeout)

    def badlist(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the badlist collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('badlist', field, query=query, filters=filters, timeout=timeout)

    def file(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the file collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('file', field, query=query, filters=filters, timeout=timeout)

    def result(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the result collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('result', field, query=query, filters=filters, timeout=timeout)

    def safelist(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the safelist collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('safelist', field, query=query, filters=filters, timeout=timeout)

    def signature(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the signature collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('signature', field, query=query, filters=filters, timeout=timeout)

    def submission(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the submission collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('submission', field, query=query, filters=filters, timeout=timeout)

    def workflow(self, field, query=None, filters=None, timeout=None):
        """\
Generates statistics about the distribution of an integer field of the workflow collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
timeout  : Maximum execution time in milliseconds (integer)

Returns statistics about the field.
"""
        return self._do_stats('workflow', field, query=query, filters=filters, timeout=timeout)
