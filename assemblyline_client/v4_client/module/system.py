from json import dumps

from assemblyline_client.v4_client.common.utils import api_path


class System(object):
    def __init__(self, connection):
        self._connection = connection

    def clear_system_message(self):
        """\
Clear the current system message
"""
        return self._connection.delete(api_path('system', 'system_message'))

    def get_system_message(self):
        """\
Get the current system message
"""
        return self._connection.get(api_path('system', 'system_message'))

    def set_system_message(self, message_object):
        """\
Set the current system message

Required:
message_object: A system message data block

Example data block:
{
  "title": "Message title",
  "severity": "info",
  "message": "This is a test message"
}
"""
        return self._connection.put(api_path('system', 'system_message'), data=dumps(message_object))

    def get_tag_safelist(self):
        """\
Get the current tag_safelist.yml file
"""
        return self._connection.get(api_path('system', 'tag_safelist'))

    def set_tag_safelist(self, yaml_file):
        """\
Set the current tag_safelist.yml file

Required:
yaml_file: New tag_safelist.yml file
"""
        return self._connection.put(api_path('system', 'tag_safelist'), data=dumps(yaml_file))
