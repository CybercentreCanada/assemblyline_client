import json
from typing import List, Union
from assemblyline_client.v4_client.common.utils import api_path, raw_output, stream_output


class Ontology(object):
    def __init__(self, connection):
        self._connection = connection

    def alert(
            self,
            alert_id: str,
            sha256s: Union[List[str], str] = [],
            services: Union[List[str], str] = [],
            output=None):
        """\
WARNING:
    This APIs output is considered stable but the ontology model itself is still in its
    alpha state. Do not use the results of this API in a production system just yet.

Get all ontology records for a given alert

Required:
alert_id     : Alert ID to get ontology records for (string)

Optional:
sha256s       : Single or list of sha256 to get ontology records for (strings - default: all)
services      : Single or list of services to get ontology records for (strings - Default: all)
output        : Output stream that will receive the raw data of
                the API instead of json loading every record (file handle or BytesIO)

Throws a Client exception if the alert or submission does not exist.
"""
        params_tuples = []
        if isinstance(sha256s, str):
            # Assume the user wanted a single sha256 and did not use a list
            params_tuples.extend([('sha256', sha256s)])
        else:
            params_tuples.extend([('sha256', x) for x in sha256s])

        if isinstance(services, str):
            # Assume the user wanted a single service and did not use a list
            params_tuples.extend([('service', services)])
        else:
            params_tuples.extend([('service', x) for x in services])

        kw = {}
        if params_tuples:
            kw['params_tuples'] = params_tuples

        if output:
            return self._connection.download(api_path('ontology', 'alert', alert_id, **kw), stream_output(output))

        data = self._connection.download(api_path('ontology', 'alert', alert_id, **kw), raw_output)
        return [json.loads(line) for line in data.splitlines()]

    def file(self, sha256: str, services: Union[List[str], str] = [], all: bool = False, output=None):
        """\
WARNING:
    This APIs output is considered stable but the ontology model itself is still in its
    alpha state. Do not use the results of this API in a production system just yet.

Get all ontology records for a given file

Required:
sha256     : SHA256 hash to get ontology records for (string)

Optional:
services     : Single or list of services to get ontology records for (strings - default: all)
all          : If there are multiple version of the ontology records, get them all (bool)
output       : Output stream that will receive the raw data of
                the API instead of json loading every record (file handle or BytesIO)

Throws a Client exception if the file does not exist.
"""
        kw = {}
        if all:
            kw['all'] = ''
        if services:
            if isinstance(services, str):
                # Assume the user wanted a single service and did not use a list
                kw['params_tuples'] = [('service', services)]
            else:
                kw['params_tuples'] = [('service', x) for x in services]

        if output:
            return self._connection.download(api_path('ontology', 'file', sha256, **kw), stream_output(output))

        data = self._connection.download(api_path('ontology', 'file', sha256, **kw), raw_output)
        return [json.loads(line) for line in data.splitlines()]

    def submission(
            self,
            sid: str,
            sha256s: Union[List[str], str] = [],
            services: Union[List[str], str] = [],
            output=None):
        """\
WARNING:
    This APIs output is considered stable but the ontology model itself is still in its
    alpha state. Do not use the results of this API in a production system just yet.

Get all ontology records for a given submission

Required:
sid     : Submission ID to get ontology records for (string)

Optional:
sha256s       : Single or list of sha256 to get ontology records for (Default: all)
services      : Single or list of services to get ontology records for (Default: all)
output        : Output stream that will receive the raw data of
                the API instead of json loading every record (file handle or BytesIO)

Throws a Client exception if the submission does not exist.
"""
        params_tuples = []

        if isinstance(sha256s, str):
            # Assume the user wanted a single sha256 and did not use a list
            params_tuples.extend([('sha256', sha256s)])
        else:
            params_tuples.extend([('sha256', x) for x in sha256s])

        if isinstance(services, str):
            # Assume the user wanted a single service and did not use a list
            params_tuples.extend([('service', services)])
        else:
            params_tuples.extend([('service', x) for x in services])

        kw = {}
        if params_tuples:
            kw['params_tuples'] = params_tuples

        if output:
            return self._connection.download(api_path('ontology', 'submission', sid, **kw), stream_output(output))

        data = self._connection.download(api_path('ontology', 'submission', sid, **kw), raw_output)
        return [json.loads(line) for line in data.splitlines()]
