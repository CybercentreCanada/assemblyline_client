from assemblyline_client.v4_client.common.utils import api_path_by_module, get_funtion_kwargs, stream_output, raw_output


class File(object):
    def __init__(self, connection):
        self._connection = connection

    def ascii(self, sha256):
        """\
Return an ascii representation of the file.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))

    def children(self, sha256):
        """\
Return the list of children for the file with the given sha256.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))

    # noinspection PyUnusedLocal
    def download(self, sha256, encoding=None, output=None):
        """\
Download the file with the given sha256.

Required:
sha256     : File key (string)

Optional:
format  : Encoding (string)
output  : Path or file handle (string or file-like object)

If output is not specified the content is returned.

Throws a Client exception if the file does not exist.
"""
        kw = get_funtion_kwargs('output', 'self', 'sha256')
        path = api_path_by_module(self, sha256, **kw)
        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def hex(self, sha256):
        """\
Return an hexadecimal representation of the file.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))


    def info(self, sha256):
        """\
Return info for the the file with the given sha256.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))

    def result(self, sha256, service=None):
        """\
Return all the results for the given sha256.

Required:
sha256     : File key (string)

Optional:
service : Service name (string)

If a service is specified, results are limited to that service.

Throws a Client exception if the file does not exist.
"""
        args = [service] if service else []
        return self._connection.get(api_path_by_module(self, sha256, *args))

    def score(self, sha256):
        """\
Return the latest score for the given sha256.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))

    def strings(self, sha256):
        """\
Return all strings found in the file.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))
