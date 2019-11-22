from json import dumps

from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module


class Submission(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, sid):
        """\
Return the submission record for the given sid.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path('submission', sid))

    def delete(self, sid):
        """\
Delete the submission and related records for the given sid.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.delete(api_path('submission', sid))

    def file(self, sid, sha256, results=None, errors=None):
        """\
Return all errors and results for a file as part of a specific submission.

Required:
sid     : Submission ID. (string)
sha256     : File key. (string)

Optional:
resuls  : Also include results with the given result keys. (list of strings)
errors  : Also include errors with the given error keys. (list of strings)

Throws a Client exception if the submission and/or file does not exist.
"""
        kw = {}
        if errors:
            kw['extra_error_keys'] = errors
        if results:
            kw['extra_result_keys'] = results

        path = api_path('submission', sid, 'file', sha256)
        if kw:
            return self._connection.post(path, data=dumps(kw))
        else:
            return self._connection.get(path)

    def full(self, sid):
        """\
Return the full result for the given submission.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))

    def is_completed(self, sid):
        """\
Check if the submission with the given sid is completed.

Required:
sid     : Submission ID. (string)

Returns True/False.

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))

    def summary(self, sid):
        """\
Return the executive summary for the submission with the given sid.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))

    def tree(self, sid):
        """\
Return the file hierarchy for the submission with the given sid.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))


class Live(object):
    def __init__(self, connection):
        self._connection = connection

    def get_message_list(self, wq):
        """\
Return messages from the given watch queue.

Required:
wq      : Watch queue name. (string)

Throws a Client exception if the watch queue does not exist.
"""
        return self._connection.get(api_path_by_module(self, wq))

    def setup_watch_queue(self, sid):
        """\
Set up a watch queue for the submission with the given sid.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))
