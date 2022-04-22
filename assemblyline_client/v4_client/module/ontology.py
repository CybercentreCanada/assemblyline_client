import json

from assemblyline_client.v4_client.common.utils import api_path, raw_output


class Ontology(object):
    def __init__(self, connection):
        self._connection = connection

    def alert(self, alert_id):
        """\
Get all ontology records for a given alert

Required:
alert_id     : Alert ID to get ontology records for (string)

Throws a Client exception if the alert or submission does not exist.
"""
        data = self._connection.download(api_path('ontology', 'alert',  alert_id), raw_output)
        return [
            json.loads(line) for line in data.splitlines()
        ]

    def file(self, sha256):
        """\
Get all ontology records for a given file

Required:
sha256     : SHA256 hash to get ontology records for (string)

Throws a Client exception if the file does not exist.
"""
        data = self._connection.download(api_path('ontology', 'file',  sha256), raw_output)
        return [
            json.loads(line) for line in data.splitlines()
        ]

    def submission(self, sid):
        """\
Get all ontology records for a given submission

Required:
sid     : Submission ID to get ontology records for (string)

Throws a Client exception if the submission does not exist.
"""
        data = self._connection.download(api_path('ontology', 'submission',  sid), raw_output)
        return [
            json.loads(line) for line in data.splitlines()
        ]
