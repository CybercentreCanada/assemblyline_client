import json

from assemblyline_client.v4_client.common.utils import api_path


class Replay(object):
    def __init__(self, connection):
        self._connection = connection

    def get_checkpoint(self, m_type):
        """\
Get the checkpoint of a given type for processing in a worker

Required:
m_type   : Type of message to get (badlist, safelist, workflow)

Throws a Client exception if the message type is invalid.
"""
        return self._connection.get(api_path('replay', 'checkpoint', m_type))

    def get_message(self, m_type):
        """\
Get the next message of a given type for processing in a worker

Required:
m_type   : Type of message to get (alert, submission or file)

Throws a Client exception if the message type is invalid.
"""
        return self._connection.get(api_path('replay', 'queue', m_type))

    def put_checkpoint(self, m_type, checkpoint):
        """\
Set checkpoint for message type in the Replay for processing in a worker

Required:
m_type      : Type of message for checkpoint setting (badlist, safelist, workflow)
checkpoint  : Date string or "*" to set checkpoint value

Throws a Client exception if the message type or message is invalid.
"""
        return self._connection.put(
            api_path('replay', 'checkpoint', m_type),
            data=json.dumps(dict(checkpoint=checkpoint)))

    def put_message(self, m_type, message):
        """\
Put a message in the replay queues for processing in a worker

Required:
m_type   : Type of message to be transfered (alert, submission or file)
message  : Message for the worker

Throws a Client exception if the message type or message is invalid.
"""
        return self._connection.put(api_path('replay', 'queue', m_type), data=json.dumps(message))

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
