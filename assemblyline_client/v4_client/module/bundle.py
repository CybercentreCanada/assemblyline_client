import os

from assemblyline_client.v4_client.common.utils import api_path, stream_output, raw_output


class Bundle(object):
    def __init__(self, connection):
        self._connection = connection

    def create(self, sid, output=None):
        """\
Creates a bundle containing the submission results and the associated files

Required:
sid    : Submission ID (string)

Optional:
output  : Path or file handle. (string or file-like object)

If output is not specified the content is returned by the function
"""
        path = api_path('bundle', sid)

        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def import_bundle(self, bundle, min_classification=None):
        """\
Import a submission bundle into the system

Required:
bundle              : bundle to import (string, bytes or file_handle)

Optional:
min_classification  : Minimum classification at which the bundle is imported. (string)

Returns {'success': True/False } depending if it was imported or not
"""
        if isinstance(bundle, str):
            if len(bundle) <= 1024 and os.path.exists(bundle):
                with open(bundle, 'rb') as f:
                    contents = f.read()
            else:
                contents = bundle
        elif "read" in dir(bundle):
            contents = bundle.read()
        else:
            raise TypeError("Invalid bundle")

        kw = {}
        if min_classification:
            kw['min_classification'] = min_classification

        return self._connection.post(api_path('bundle', **kw), data=contents)
