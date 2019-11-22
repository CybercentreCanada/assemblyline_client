from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, api_path


class Stats(object):
    def __init__(self, connection):
        self._connection = connection

    def _do_stats(self, bucket, field, **kwargs):
        if bucket not in SEARCHABLE:
            raise ClientError("Bucket %s is not searchable" % bucket, 400)

        filters = kwargs.pop('filters', None)
        if filters is not None:
            if isinstance(filters, str):
                filters = [filters]

            filters = [('filters', fq) for fq in filters]

        kwargs = {k: v for k, v in kwargs.items() if v is not None and k != 'filters'}
        if filters is not None:
            kwargs['params_tuples'] = filters
        path = api_path('search', 'stats', bucket, field, **kwargs)
        return self._connection.get(path)

    def alert(self, field, query=None, filters=None):
        """\
Generates statistics about the distribution of an integer field of the alert collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)

Returns statistics about the field.
"""
        return self._do_stats('alert', field, query=query, filters=filters)

    def file(self, field, query=None, filters=None):
        """\
Generates statistics about the distribution of an integer field of the file collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)

Returns statistics about the field.
"""
        return self._do_stats('file', field, query=query, filters=filters)

    def result(self, field, query=None, filters=None):
        """\
Generates statistics about the distribution of an integer field of the result collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)

Returns statistics about the field.
"""
        return self._do_stats('result', field, query=query, filters=filters)

    def signature(self, field, query=None, filters=None):
        """\
Generates statistics about the distribution of an integer field of the signature collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)

Returns statistics about the field.
"""
        return self._do_stats('signature', field, query=query, filters=filters)

    def submission(self, field, query=None, filters=None):
        """\
Generates statistics about the distribution of an integer field of the submission collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)

Returns statistics about the field.
"""
        return self._do_stats('submission', field, query=query, filters=filters)

    def workflow(self, field, query=None, filters=None):
        """\
Generates statistics about the distribution of an integer field of the workflow collection.

Required:
field   : field to create the stats on (only work on number fields)

Optional:
query    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)

Returns statistics about the field.
"""
        return self._do_stats('workflow', field, query=query, filters=filters)
