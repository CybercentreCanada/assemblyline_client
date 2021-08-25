from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, api_path


class Facet(object):
    def __init__(self, connection):
        self._connection = connection

    def _do_facet(self, index, field, **kwargs):
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
        path = api_path('search', 'facet', index, field, **kwargs)
        return self._connection.get(path)

    def alert(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the alert collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('alert', field, query=query, mincount=mincount, filters=filters)

    def file(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the file collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('file', field, query=query, mincount=mincount, filters=filters)

    def heuristic(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the heuristic collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('heuristic', field, query=query, mincount=mincount, filters=filters)

    def result(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the result collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('result', field, query=query, mincount=mincount, filters=filters)

    def safelist(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the safelist collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('safelist', field, query=query, mincount=mincount, filters=filters)

    def signature(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the signature collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('signature', field, query=query, mincount=mincount, filters=filters)

    def submission(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the submission collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('submission', field, query=query, mincount=mincount, filters=filters)

    def workflow(self, field, query=None, mincount=None, filters=None):
        """\
List most frequent value for a field in the workflow collection.

Required:
field   : field to extract the facets from

Optional:
qeury    : Initial query to filter the data (default: 'id:*')
filters  : Additional lucene queries used to filter the data (list of strings)
mincount : Minimum amount of hits for the value to be returned

Returns all results.
"""
        return self._do_facet('workflow', field, query=query, mincount=mincount, filters=filters)
