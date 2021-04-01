from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, \
    get_function_kwargs, stream_output, raw_output


class Signature(object):
    def __init__(self, connection):
        self._connection = connection
        self.sources = Sources(connection)

    def __call__(self, signature_id):
        """\
Return the signature with the given ID and revision.

Required:
signature_id     : Signature ID including

Throws a Client exception if the signature does not exist.
"""
        return self._connection.get(api_path('signature', signature_id))

    # noinspection PyUnusedLocal
    def add_update(self, data, dedup_name=True):
        """\
Add or update a signature.

Required:
Data block:
{
 "name": "sig_name",           # Signature name
 "type": "yara",               # One of yara, suricata or tagcheck
 "data": "rule sample {...}",  # Data of the rule to be added
 "source": "yara_signatures"   # Source from where the signature has been gathered
}

Optional:
dedup_name : Should we check if the signature already exist before inserting it (default: True)

Returns:
{
 "success": True,
 "signature_id": <ID of the saved signature>
}
        """
        return self._connection.post(api_path_by_module(self, **get_function_kwargs('data', 'self')), json=data)

    # noinspection PyUnusedLocal
    def add_update_many(self, source, sig_type, data, dedup_name=True):
        """\
Add or update multiple signatures.

Required:
source     : Source of the signature
sig_type   : Type of signature
data       : List of signatures

Data block example:
[                                # List of signatures to update
    {
     "name": "sig_name",           # Signature name
     "type": "yara",               # One of yara, suricata or tagcheck
     "data": "rule sample {...}",  # Data of the rule to be added
     "source": "yara_signatures"   # Source from where the signature has been gathered
    },
    ...
]

Optional:
dedup_name : Should we check if the signatures already exist before inserting it (default: True)

Returns:
{
 "success": 23,       # Number of successful inserts
 "errors": [],        # List of signature that failed
 "skipped": [],       # List of skipped signatures, they already exist
}
        """
        return self._connection.post(api_path_by_module(self, **get_function_kwargs('data', 'self')), json=data)

    def change_status(self, signature_id, status):
        """\
Change the status of a signature

Required:
signature_id     : ID of the signature to change the status
status           : New status for the signature (DEPLOYED, NOISY, DISABLED, TESTING, STAGING)

Throws a Client exception if the signature does not exist or the status is invalid.
"""
        return self._connection.get(api_path_by_module(self, signature_id, status))

    def delete(self, signature_id):
        """\
Delete a signature based off its ID

Required:
signature_id     : ID of the signature to be deleted

Throws a Client exception if the signature does not exist.
"""
        return self._connection.delete(api_path('signature', signature_id))

    # noinspection PyUnusedLocal
    def download(self, output=None, query=None):
        """\
Download the signatures. Defaults to all if no query is provided.

Optional:
output  : Path or file handle. (string or file-like object)
query   : lucene query (string)

If output is not specified the content is returned.
"""
        path = api_path_by_module(self, **get_function_kwargs('output', 'self'))
        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def stats(self):
        """\
Gather statistics about all the signatures in the system.

"""
        return self._connection.get(api_path('signature/stats'))

    def update_available(self, since='', sig_type='*'):
        """\
Check if updated signatures are available.

Optional:
since   : ISO 8601 date (%Y-%m-%dT%H:%M:%S). (string)
"""
        return self._connection.get(api_path_by_module(self, last_update=since, type=sig_type))


class Sources(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self):
        """\
Get all signature sources.
"""
        return self._connection.get(api_path('signature', 'sources'))

    def add(self, service, new_source):
        """\
Add a signature source for a given service

Required:
service      : Service to which we want to add the source to
source_data  : Data of the signature source
"""
        return self._connection.put(api_path('signature', 'sources', service), json=new_source)

    def delete(self, service, name):
        """\
Delete a signature source by name for a given service

Required:
service      : Service to which we want to delete the source from
name         : Name of the source you want to remove
"""
        return self._connection.delete(api_path('signature', 'sources', service, name))

    def update(self, service, name, source_data):
        """\
Update a signature source by name for a given service

Required:
service      : Service to which we want to update the signature source from
name         : Name of the signature source you want to update
source_data  : Data of the signature source
"""
        return self._connection.post(api_path('signature', 'sources', service, name), json=source_data)
