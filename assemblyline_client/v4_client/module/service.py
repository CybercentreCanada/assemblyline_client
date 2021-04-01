from assemblyline_client.v4_client.common.utils import api_path, api_path_by_module, raw_output, stream_output


class Service(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, service_name, version=None):
        """\
Load the configuration for a given service

Required:
service_name:   Name of the service to get the info

Optional:
version     :   Specific version of the service to get

Throws a Client exception if the service does not exist.
"""
        kw = {}
        if version:
            kw['version'] = version
        return self._connection.get(api_path('service', service_name, **kw))

    def add(self, data):
        """\
Add a service using its yaml manifest

Required:
data  : service_manifest.yml content
"""
        return self._connection.put(api_path('service'), data=data)

    def backup(self, output=None):
        """\
Create a backup of the current system configuration

Optional:
output   : Path or file handle (string or file-like object)
"""
        path = api_path_by_module(self)
        if output:
            return self._connection.download(path, stream_output(output))
        return self._connection.download(path, raw_output)

    def constants(self, output=None):
        """\
Get global service constants.
"""
        return self._connection.get(api_path_by_module(self))

    def delete(self, service_name):
        """\
Remove a service from the system

Required:
service_name:   Name of the service to delete

Throws a Client exception if the service does not exist.
"""
        return self._connection.delete(api_path('service', service_name))

    def list(self):
        """\
List all service configurations of the system.
"""
        return self._connection.get(api_path('service', 'all'))

    def restore(self, data):
        """\
Restore an old backup of the system configuration

Required:
data   :  Backup yaml data
"""
        return self._connection.put(api_path('service', 'restore'), data=data)

    def set(self, service_name, service_data):
        """\
Calculate the delta between the original service config and
the posted service config then saves that delta as the current
service delta.

Required:
service_name     : Name of the service to change the configuration
service_data     : New configuration for the service
"""
        return self._connection.post(api_path('service', service_name), json=service_data)

    def update(self, name, image, tag, username=None, password=None):
        """\
Update a given service

Required:
name      : Name of the service to update
image     : Full path to the container image including tag
tag       : Tag to update the service to

Optional:
username  : Username to log into the docker registry
password  : Password to log into the docker registry
"""
        data = {
            'name': name,
            'update_data': {
                'name': name,
                'image': image,
                'latest_tag': tag
            }
        }

        if username and password:
            data['update_data']['auth'] = {
                'username': username,
                'password': password
            }

        return self._connection.put(api_path_by_module(self), json=data)

    def updates(self):
        """\
Check for potential updates for the given services.
"""
        return self._connection.get(api_path_by_module(self))

    def versions(self, service_name):
        """\
List the different versions of a service stored in the system

Required:
service_name:   Name of the service to get the versions for

Throws a Client exception if the service does not exist.
"""
        return self._connection.get(api_path_by_module(self, service_name))
