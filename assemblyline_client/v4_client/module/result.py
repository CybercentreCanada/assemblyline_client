from json import dumps

from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, get_function_kwargs


class Result(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, key):
        """\
Return the result with the given key.

Required:
key     : Result key.

Throws a Client exception if the error does not exist.
"""
        return self._connection.get(api_path('result', key))

    def error(self, key):
        """\
Return the error with the given key.

Required:
key     : Error key.

Throws a Client exception if the error does not exist.
"""
        return self._connection.get(api_path_by_module(self, key))

    # noinspection PyUnusedLocal
    def multiple(self, error=None, result=None):
        """\
Get multiple result and error keys at the same time.

Optional:
error   : List of error keys. (list of strings).
result  : List of result keys. (list of strings).
"""
        if result is None:
            result = []
        if error is None:
            error = []
        data = dumps(get_function_kwargs('self'))
        return self._connection.post(api_path('result', 'multiple_keys'), data=data)
