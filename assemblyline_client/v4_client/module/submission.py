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

    def list(self, user=None, group=None, fq=None, rows=10, offset=0):
        """\
List all submissions of a given group or user.

Required:
sid        : Submission ID. (string)

Optional:
user       : user to get the submissions from
group      : groups to get the submissions from
offset     : Offset at which we start giving submissions
rows       : Number of submissions to return
fq         : Query to filter to the submission list
"""
        kw = {
            'rows': rows,
            'offset': offset
        }

        if fq:
            kw['query'] = fq

        if user:
            return self._connection.get(api_path_by_module(self, 'user', user, **kw))
        if group:
            return self._connection.get(api_path_by_module(self, 'group', group, **kw))
        return self._connection.get(api_path_by_module(self, 'group', 'ALL', **kw))

    def report(self, sid):
        """\
Create a report for a submission based on its ID.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))

    def set_verdict(self, sid, verdict):
        """\
Set the verdict of a submission based on its ID.

Required:
sid       : Submission ID. (string)
verdict   : Verdict that the user thinks the submission is (malicious, non_malicious)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.put(api_path('submission', 'verdict', sid, verdict))

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

    def get_message(self, wq):
        """\
Get a message from the given watch queue.

Required:
wq      : Watch queue name. (string)

Throws a Client exception if the watch queue does not exist.
"""
        return self._connection.get(api_path_by_module(self, wq))

    def get_message_list(self, wq):
        """\
Return all current messages from the given watch queue.

Required:
wq      : Watch queue name. (string)

Throws a Client exception if the watch queue does not exist.
"""
        return self._connection.get(api_path_by_module(self, wq))

    def outstanding_services(self, sid):
        """\
List outstanding services and the number of files each
of them still have to process.

Required:
sid:   Submission ID (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))

    def setup_watch_queue(self, sid):
        """\
Set up a watch queue for the submission with the given sid.

Required:
sid     : Submission ID. (string)

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, sid))
