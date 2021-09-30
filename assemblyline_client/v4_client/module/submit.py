import os
import tempfile
from json import dumps
from requests_toolbelt.multipart.encoder import MultipartEncoder

from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, get_function_kwargs, ClientError


class Submit(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, openfile=None, path=None, content=None, url=None, sha256=None, fname=None, params=None, metadata=None):
        """\
Submit a file to be dispatched.

Required (one of)
openfile: A file-like object that has already been opened for reading.
content : Content of the file to scan
path    : Path/name of file. (string)
sha256  : Sha256 of the file to scan
url     : Url to scan

Optional
fname   : Name of the file to scan
metadata   : Metadata to include with submission. (dict)
params  : Additional submission parameters. (dict)

If content is provided, the path is used as metadata only.
"""
        rmpath = None
        try:
            if content:
                fd, path = tempfile.mkstemp()
                rmpath = path
                with os.fdopen(fd, 'wb') as fh:
                    if isinstance(content, str):
                        content = content.encode()
                    fh.write(content)

            files = {}
            if openfile:
                if fname is None:
                    raise ClientError(
                        'fname must be provided when openfile is given', 400
                    )
                files = {'bin': (fname, openfile)}
                request = {
                    'name': fname,
                }
            elif path:
                if os.path.exists(path):
                    request = {
                        'name': fname or os.path.basename(path)
                    }
                    files = {'bin': (request['name'], open(path, 'rb'))}
                else:
                    raise ClientError('File does not exist "%s"' % path, 400)
            elif url:
                request = {
                    'url': url,
                    'name': fname or os.path.basename(url).split("?")[0],
                }
            elif sha256:
                request = {
                    'sha256': sha256,
                    'name': fname or sha256,
                }
            else:
                raise ClientError('You need to provide at least content, a path, a url or a sha256', 400)

            if params:
                request['params'] = params

            if metadata:
                request['metadata'] = metadata

            if files:
                fields = {'json': dumps(request)}
                fields.update(files)
                data = MultipartEncoder(fields)
                headers = {'content-type': data.content_type}
            else:
                data = dumps(request)
                headers = None

            return self._connection.post(api_path('submit'), data=data, headers=headers)
        finally:
            if rmpath:
                try:
                    os.unlink(rmpath)
                except OSError:
                    pass

    # noinspection PyUnusedLocal
    def dynamic(self, sha256, copy_sid=None, name=None):
        """\
Resubmit a file for dynamic analysis

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        kw = get_function_kwargs('self', 'sha256')
        return self._connection.get(api_path_by_module(self, sha256, **kw))

    def resubmit(self, sid):
        """\
Resubmit a file for analysis with the exact same parameters.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))
