from assemblyline_client.v4_client.common.utils import (
    api_path,
    api_path_by_module,
    get_function_kwargs,
    raw_output,
    stream_output,
)


class File(object):
    def __init__(self, connection):
        self._connection = connection

    def ai_summary(self, sha256) -> str:
        """\
Return an AI generated summary for the file with the given sha256.
Required:
sha256     : File key (string)
Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path('file/ai', sha256))['content']

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

    def code_summary(self, sha256) -> str:
        """\
Return a code summary for the file with the given sha256.
Required:
sha256     : File key (string)
Throws a Client exception if the file does not exist.
"""
        return self._connection.get(api_path_by_module(self, sha256))['content']

    # noinspection PyUnusedLocal
    def download(self, sha256, encoding=None, sid=None, output=None, password=None):
        """\
Download the file with the given sha256.

Required:
sha256     : File key (string)

Optional:
encoding : Which file encoding do you want for the file (string)
output   : Path or file handle (string or file-like object)
sid      : ID of the submission the download is for
           If carted the file will inherit the submission metadata (string)

If output is not specified the content is returned.

Throws a Client exception if the file does not exist.
"""
        kw = get_function_kwargs('output', 'sid', 'sha256')
        path = api_path_by_module(self, sha256, **kw)
        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def delete_from_filestore(self, sha256):
        """\
Delete a file from the filestore without deleting the file record

Required:
sha256     : A resource locator for the file (sha256)

Throws a Client exception if the file does not exist or if you don't have the rights to delete the file.
"""
        return self._connection.delete(api_path('file/filestore', sha256))

    def hex(self, sha256, bytes_only=False, length=None):
        """\
Return an hexadecimal representation of the file.

Required:
sha256     : File key (string)

Throws a Client exception if the file does not exist.
"""
        kw = {}
        if bytes_only:
            kw['bytes_only'] = ''
        if length:
            kw['length'] = length

        return self._connection.get(api_path_by_module(self, sha256, **kw))

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
