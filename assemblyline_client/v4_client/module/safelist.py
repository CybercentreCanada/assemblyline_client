from json import dumps

from assemblyline_client.v4_client.common.utils import api_path


class Safelist(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, qhash):
        """\
Check if a hash exists in the safelist

Required:
qhash     : Hash to check in the safelist (string)
"""
        return self._connection.get(api_path('safelist', qhash))

    def add_update(self, safelist_object):
        """\
Add a hash in the safelist if it does not exist or update its list of sources if it does

Required:
safelist_object     : A dictionary containing the safelist details

Throws a Client exception if the safelist object is invalid.
"""
        return self._connection.put(api_path('safelist'), data=dumps(safelist_object))

    def delete(self, safelist_id):
        """\
Delete the safelist object using it's ID.

The safelist ID is one of the following:
    - One of the hash of the file in order of importance (SHA256 -> SHA1 -> MD5)
    - SHA256 hash of the tag type and value concatenated

Required:
safelist_id     : ID of the safelist object (string)

Throws a Client exception if the safelist does not exist.
"""
        return self._connection.delete(api_path('safelist', safelist_id))

    def set_enabled(self, safelist_id, enabled):
        """\
Set the enabled status of a safelist object using it's ID.

The safelist ID is one of the following:
    - One of the hash of the file in order of importance (SHA256 -> SHA1 -> MD5)
    - SHA256 hash of the tag type and value concatenated

Required:
safelist_id     : ID of the safelist object (string)
enabled         : True/False value (boolean)

Throws a Client exception if the safelist does not exist.
"""
        return self._connection.put(api_path('safelist', 'enable', safelist_id), data=dumps(enabled))
