from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, get_funtion_kwargs, stream_output, \
    raw_output


class Signature(object):
    def __init__(self, connection):
        self._connection = connection

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
        """
        return self._connection.post(api_path_by_module(self, **get_funtion_kwargs('data', 'self')), json=data)

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
        """
        return self._connection.post(api_path_by_module(self, **get_funtion_kwargs('data', 'self')), json=data)

    # noinspection PyUnusedLocal
    def download(self, output=None, query=None, safe=True):
        """\
Download the signatures. Defaults to all if no query is provided.

Optional:
output  : Path or file handle. (string or file-like object)
query   : lucene query (string)
safe    : Ensure signatures can be compiled. (boolean)

If output is not specified the content is returned.
"""
        path = api_path_by_module(self, **get_funtion_kwargs('output', 'self'))
        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def update_available(self, since='', sig_type='*'):
        """\
Check if updated signatures are available.

Optional:
since   : ISO 8601 date (%Y-%m-%dT%H:%M:%S). (string)
"""
        return self._connection.get(api_path_by_module(self, last_update=since, type=sig_type))


