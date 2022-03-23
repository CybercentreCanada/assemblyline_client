import os

from json import dumps

from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, get_function_kwargs, ClientError
from assemblyline_client.v4_client.common.submit_utils import get_file_handler


class Submit(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, fh=None, path=None, content=None, url=None, sha256=None, fname=None, params=None, metadata=None):
        """\
Submit a file to be dispatched.

Required (one of)
fh      : Opened file handle to a file to scan
content : Content of the file to scan (byte array)
path    : Path/name of file. (string)
sha256  : Sha256 of the file to scan (string)
url     : Url to scan (string)

Optional
fname   : Name of the file to scan
metadata   : Metadata to include with submission. (dict)
params  : Additional submission parameters. (dict)

If content is provided, the path is used as metadata only.
"""
        rmpath = None
        try:
            if content:
                fh = get_file_handler(content, fname)

            files = {}
            if fh:
                if fname is None:
                    if hasattr(fh, 'name'):
                        fname = fh.name
                    else:
                        raise ClientError('Could not guess the file name, please provide an fname parameter', 400)
                fh.seek(0)
                files = {'bin': (fname, fh)}
                request = {
                    'name': fname,
                }
            elif path:
                if os.path.exists(path):
                    files = {'bin': open(path, 'rb')}
                else:
                    raise ClientError('File does not exist "%s"' % path, 400)

                request = {
                    'name': fname or os.path.basename(path)
                }
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
                data = {'json': dumps(request)}
                headers = {'content-type': None}
            else:
                data = dumps(request)
                headers = None

            return self._connection.post(api_path('submit'), data=data, files=files, headers=headers)
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
