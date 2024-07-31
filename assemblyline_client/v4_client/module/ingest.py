import os

from json import dumps

from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, ClientError
from assemblyline_client.v4_client.common.submit_utils import get_file_handler


class Ingest(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, fh=None, path=None, content=None, url=None, sha256=None, fname=None, params=None, metadata=None,
                 alert=False, nq=None, nt=None, ingest_type='AL_CLIENT', submission_profile=None):
        """\
Submit a file to the ingestion queue.

Required (one of)
fh      : Opened file handle to a file to scan
content : Content of the file to scan (byte array)
path    : Path/name of file (string)
sha256  : Sha256 of the file to scan (string)
url     : Url to scan (string)

Optional
alert      : Create an alert if score above alert threshold. (boolean)
fname      : Name of the file to scan (string)
metadata   : Metadata to include with submission. (dict)
nq         : Notification queue name. (string)
nt         : Notification threshold. (int)
params     : Additional submission parameters. (dict)
ingest_type: Ingestion type, one word to describe how the data is ingested. Default: AL_CLIENT (string)
submission_profile    : Submission profile name

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
                files = {'bin': fh}
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

            request.update({
                'metadata': {},
                'type': ingest_type,
            })

            if alert:
                request['generate_alert'] = bool(alert)
            if metadata:
                request['metadata'].update(metadata)
            if nq:
                request['notification_queue'] = nq
            if nt:
                request['notification_threshold'] = int(nt)
            if params:
                request['params'] = params
            if submission_profile:
                request['submission_profile'] = submission_profile
            if files:
                data = {'json': dumps(request)}
                headers = {'content-type': None}
            else:
                data = dumps(request)
                headers = None

            return self._connection.post(api_path('ingest'), data=data, files=files, headers=headers)
        finally:
            if rmpath:
                try:
                    os.unlink(rmpath)
                except OSError:
                    pass

    def get_message(self, nq):
        """\
Return a single message from the given notification queue.

Required:
nq      : Notification queue name. (string)

Throws a Client exception if the watch queue does not exist.
"""
        return self._connection.get(api_path_by_module(self, nq))

    def get_message_list(self, nq, page_size=None):
        """\
Return all messages from the given notification queue.

Required:
nq          : Notification queue name. (string)

Optional:
page_size   : Number of messages to get back from queue. (int)

Throws a Client exception if the watch queue does not exist.
"""
        kw = {}
        if page_size:
            kw['page_size'] = int(page_size)
        return self._connection.get(api_path_by_module(self, nq, **kw))
