from json import dumps

from assemblyline_client.v4_client.common.utils import api_path


class Badlist(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, qhash):
        """\
Check if a hash exists in the badlist

Required:
qhash     : Hash to check in the badlist (string)
"""
        return self._connection.get(api_path('badlist', qhash))

    def add_update(self, badlist_object):
        """\
Add a hash in the badlist if it does not exist or update its list of sources if it does

Required:
badlist_object     : A dictionary containing the badlist details

Throws a Client exception if the badlist object is invalid.
"""
        return self._connection.put(api_path('badlist'), data=dumps(badlist_object))

    def add_update_many(self, list_of_badlist_object):
        """\
Add a list of hashes in the badlist if it does not exist or update its list of sources if it does

Required:
list_of_badlist_object     : A list of dictionary containing the badlist details

Throws a Client exception if the badlist object is invalid.
"""
        return self._connection.put(api_path('badlist', 'add_update_many'), data=dumps(list_of_badlist_object))

    def delete(self, badlist_id):
        """\
Delete the badlist object using it's ID.

The badlist ID is one of the following:
    - One of the hash of the file in order of importance (SHA256 -> SHA1 -> MD5)
    - SHA256 hash of the tag type and value concatenated

Required:
badlist_id     : ID of the badlist object (string)

Throws a Client exception if the badlist does not exist.
"""
        return self._connection.delete(api_path('badlist', badlist_id))

    def set_enabled(self, badlist_id, enabled):
        """\
Set the enabled status of a badlist object using it's ID.

The badlist ID is one of the following:
    - One of the hash of the file in order of importance (SHA256 -> SHA1 -> MD5)
    - SHA256 hash of the tag type and value concatenated

Required:
badlist_id     : ID of the badlist object (string)
enabled         : True/False value (boolean)

Throws a Client exception if the badlist does not exist.
"""
        return self._connection.put(api_path('badlist', 'enable', badlist_id), data=dumps(enabled))

    def ssdeep(self, qhash):
        """\
Check if a file exists with a similar ssdeep.

Required:
qhash     : Hash to check in the badlist (string)

Returns:
[ List of files matching the SSDeep hash ]
"""
        return self._connection.get(api_path('badlist', 'ssdeep', qhash))

    def tlsh(self, qhash):
        """\
Check if a file exists with a similar TLSH.

Required:
qhash     : Hash to check in the badlist (string)

Returns:
[ List of files matching the TLSH hash ]
"""
        return self._connection.get(api_path('badlist', 'tlsh', qhash))
