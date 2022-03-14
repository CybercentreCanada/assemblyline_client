import json

from assemblyline_client.v4_client.common.utils import api_path


class Replay(object):
    def __init__(self, connection):
        self._connection = connection

    def request(self, index, doc_id):
        """\
Request an alert or a submission to be transfered to another system

Required:
index   : Type of document to be transfered (alert or submission)
doc_id  : ID of the document to transfer

Throws a Client exception if you don't have access to the alert or submission.
"""
        return self._connection.get(api_path('replay', index, doc_id))

    def set_complete(self, index, doc_id):
        """\
Mark an alert or submission successfully transfered to another system

Required:
index   : Type of document transfered (alert or submission)
doc_id  : ID of the document transfered

Throws a Client exception if you don't have access to the alert or submission.
"""
        return self._connection.post(api_path('replay', index, doc_id))

    def set_bulk_pending(self, index, query, filter_queries, max_docs):
        """\
Set the replay pending state on alert or submissions maching the queries

Required:
index           : Type of document transfered (alert or submission)
query           : Query that the alert/submission must match
filter_queries  : Additional filter queries that the alert/submission must match
max_docs        : Maximum number of documents that can be modified by the operation

Throws a Client exception if you there are syntax errors in your search queries.
"""
        return self._connection.post(
            api_path('replay', 'pending'),
            data=json.dumps(dict(index=index, query=query, filter_queries=filter_queries, max_docs=max_docs))
        )
