import json

from assemblyline_client.v4_client.common.utils import api_path, raw_output


class Ontology(object):
    def __init__(self, connection):
        self._connection = connection

    def alert(self, alert_id, sha256s=[], services=[]):
        """\
Get all ontology records for a given alert

Required:
alert_id     : Alert ID to get ontology records for (string)

Optional:
sha256s       : List of sha256 to get ontology records for (strings - default: all)
services      : List of services to get ontology records for (strings - Default: all)

Throws a Client exception if the alert or submission does not exist.
"""
        params_tuples = []
        params_tuples.extend([('sha256', x) for x in sha256s])
        params_tuples.extend([('service', x) for x in services])

        kw = {}
        if params_tuples:
            kw['params_tuples'] = params_tuples

        data = self._connection.download(api_path('ontology', 'alert',  alert_id, **kw), raw_output)
        return [
            json.loads(line) for line in data.splitlines()
        ]

    def file(self, sha256, services=[], all=False):
        """\
Get all ontology records for a given file

Required:
sha256     : SHA256 hash to get ontology records for (string)

Optional:
services      : List of services to get ontology records for (strings - default: all)
all          : If there are multiple version of the ontology records, get them all (bool)

Throws a Client exception if the file does not exist.
"""
        kw = {}
        if all:
            kw['all'] = ''
        if services:
            kw['params_tuples'] = [('service', x) for x in services]

        data = self._connection.download(api_path('ontology', 'file',  sha256, **kw), raw_output)
        return [
            json.loads(line) for line in data.splitlines()
        ]

    def submission(self, sid, sha256s=[], services=[]):
        """\
Get all ontology records for a given submission

Required:
sid     : Submission ID to get ontology records for (string)

Optional:
sha256s       : List of sha256 to get ontology records for (Default: all)
services      : List of services to get ontology records for (Default: all)

Throws a Client exception if the submission does not exist.
"""
        params_tuples = []
        params_tuples.extend([('sha256', x) for x in sha256s])
        params_tuples.extend([('service', x) for x in services])

        kw = {}
        if params_tuples:
            kw['params_tuples'] = params_tuples

        data = self._connection.download(api_path('ontology', 'submission',  sid, **kw), raw_output)
        return [
            json.loads(line) for line in data.splitlines()
        ]
