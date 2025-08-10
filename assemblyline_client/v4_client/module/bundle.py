import os

from assemblyline_client.v4_client.common.utils import api_path, stream_output, raw_output


class Bundle(object):
    def __init__(self, connection):
        self._connection = connection

    def create(self, sid, output=None, use_alert=False):
        """\
Creates a bundle containing the submission results and the associated files

Required:
sid    : Submission ID (string)

Optional:
output     : Path or file handle. (string or file-like object)
use_alert  : The ID provided is an alert ID and will be used for bundle creation. (bool)

If output is not specified the content is returned by the function
"""
        path = api_path('bundle', sid, use_alert='' if use_alert else None)

        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def import_bundle(
        self,
        bundle,
        min_classification=None,
        rescan_services=None,
        exist_ok=False,
        allow_incomplete=False,
        complete_queue=None,
        reclassification=None,
        to_ingest=False,
    ):
        """\
Import a submission bundle into the system

Required:
bundle              : bundle to import (string, bytes or file_handle)

Optional:
allow_incomplete    : allow importing incomplete submission. (bool)
exist_ok            : Do not throw an exception if the submission already exists (bool)
min_classification  : Minimum classification at which the bundle is imported. (string)
rescan_services     : List of services to rescan after import. (Comma seperated strings)

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
        if exist_ok:
            kw['exist_ok'] = ''
        if min_classification:
            kw['min_classification'] = min_classification
        if rescan_services:
            kw['rescan_services'] = ','.join(rescan_services)
        if allow_incomplete:
            kw['allow_incomplete'] = ''
        if reclassification:
            kw["reclassification"] = reclassification
        if to_ingest:
            kw["to_ingest"] = to_ingest

        return self._connection.post(api_path('bundle', **kw), data=contents)
