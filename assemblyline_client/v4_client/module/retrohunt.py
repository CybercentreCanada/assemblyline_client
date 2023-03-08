from json import dumps

from assemblyline_client.v4_client.common.utils import api_path


class Retrohunt(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, query_code):
        """
        Return status of the query with the given code.

        Required:
        query_code: Identifier for query. (string)

        Throws a Client exception if the query does not exist.
        """
        return self._connection.get(api_path('retrohunt', query_code))

    def start(self, yara_signature, archive_only, description, classification):
        """
        Start a new retrohunt query.

        Required:
        yara_signature: yara signature to search with. (string)
        archive_only: Should the search only be run on archived files. (bool)
        description: Textual description of this search. (string)
        classification: Classification level for the search. (string)

        Throws a Client execption if any parameters are not accepted.
        """

        data = dumps({
            'yara_signature': yara_signature,
            'archive_only': archive_only,
            'description': description,
            'classification': classification
        })

        return self._connection.post(api_path('retrohunt'), data=data)
