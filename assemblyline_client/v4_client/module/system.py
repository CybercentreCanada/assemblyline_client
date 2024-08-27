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

    def get_classification_aliases(self):
        """\
Get the current display aliases for the classification engine
"""
        return self._connection.get(api_path('system', 'classification_aliases'))

    def set_classification_aliases(self, aliases):
        """\
Save display aliases for the classification engine

Required:
aliases: A dictionary of alias name and short_names for a given classifications strings

Example data block:
{
  "ORG_000000": {"name": "Communication Security Establishment",
                 "short_name": "CSE"},
  "ORG_000001": {"name": "Canadian Center for Cyber Security",
                 "short_name": "CCCS"},
  ...
}
"""
        return self._connection.put(api_path('system', 'classification_aliases'), data=dumps(aliases))

    def get_metadata_suggestions(self, key=None):
        """\
Get the current metadata suggestions

Optional:
key: Get only the suggestions values for the given key
"""
        kw = {}
        if key:
            kw['key'] = key
        return self._connection.get(api_path('system', 'metadata_suggestions', **kw))

    def set_metadata_suggestions(self, suggestions, key=None):
        """\
Set the metadata suggestions

Required:
aliases: A dictionary with a list of suggestions for each key or
         A list of suggestion if used on a specific key

Example data block:
{
  "key_1": ["a", "b", "c"],
  "key_2": ["d", "e", "f"],
}

or

["a", "b", "c"]  # If use with a key
"""
        kw = {}
        if key:
            kw['key'] = key
        return self._connection.put(api_path('system', 'metadata_suggestions', **kw), data=dumps(suggestions))
