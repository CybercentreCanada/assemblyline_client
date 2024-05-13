import threading
import time

from assemblyline_client.v4_client.common.utils import SEARCHABLE, ClientError, INVALID_STREAM_SEARCH_PARAMS


class Stream(object):
    def __init__(self, connection, do_search):
        self._connection = connection
        self._do_search = do_search
        self._page_size = 100
        self._max_yield_cache = 100

    def _auto_fill(self, items, lock, index, query, **kwargs):
        done = False
        while not done:
            skip = False
            with lock:
                if len(items) > self._max_yield_cache:
                    skip = True

            if skip:
                time.sleep(0.01)
                continue

            j = self._do_search(index, query, **kwargs)

            # Replace cursorMark.
            kwargs['deep_paging_id'] = j.get('next_deep_paging_id', '*')

            with lock:
                items.extend(j['items'])

            done = self._page_size - len(j['items'])

    def _do_stream(self, index, query, **kwargs):
        if index not in SEARCHABLE:
            raise ClientError("Index %s is not searchable" % index, 400)

        for arg in list(kwargs.keys()):
            if arg in INVALID_STREAM_SEARCH_PARAMS:
                raise ClientError(
                    "The following parameters cannot be used with stream search: %s" %
                    ", ".join(INVALID_STREAM_SEARCH_PARAMS), 400
                )

        kwargs.update({
            'rows': str(self._page_size),
            'deep_paging_id': '*'
        })

        yield_done = False
        items = []
        lock = threading.Lock()
        sf_t = threading.Thread(target=self._auto_fill, args=[items, lock, index, query], kwargs=kwargs)
        sf_t.setDaemon(True)
        sf_t.start()
        while not yield_done:
            try:
                with lock:
                    item = items.pop(0)

                yield item
            except IndexError:
                if not sf_t.is_alive() and len(items) == 0:
                    yield_done = True
                time.sleep(0.01)

    def alert(self, query, filters=None, fl=None):
        """\
Get all alerts from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('alert', query, filters=filters, fl=fl)

    def badlist(self, query, filters=None, fl=None):
        """\
Get all badlists from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('badlist', query, filters=filters, fl=fl)

    def file(self, query, filters=None, fl=None):
        """\
Get all files from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('file', query, filters=filters, fl=fl)

    def heuristic(self, query, filters=None, fl=None):
        """\
Get all heuristics from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('heuristic', query, filters=filters, fl=fl)

    def result(self, query, filters=None, fl=None):
        """\
Get all results from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('result', query, filters=filters, fl=fl)

    def signature(self, query, filters=None, fl=None):
        """\
Get all signatures from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('signature', query, filters=filters, fl=fl)

    def safelist(self, query, filters=None, fl=None):
        """\
Get all safelists from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('safelist', query, filters=filters, fl=fl)

    def submission(self, query, filters=None, fl=None):
        """\
Get all submissions from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('submission', query, filters=filters, fl=fl)

    def workflow(self, query, filters=None, fl=None):
        """\
Get all workflow from a lucene query.

Required:
query   : lucene query (string)

Optional:
filters : Additional lucene queries used to filter the data (list of strings)
fl      : List of fields to return (comma separated string of fields)

Returns a generator that transparently and efficiently pages through results.
"""
        return self._do_stream('workflow', query, filters=filters, fl=fl)
