from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module


class User(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, username):
        """\
Return the settings for the given username.

Required:
username: User key. (string).

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path('user', username))

    def submission_params(self, username):
        """\
Return the submission parameters for the given username.

Required:
username: User key. (string).

Throws a Client exception if the submission does not exist.
"""
        return self._connection.get(api_path_by_module(self, username))
