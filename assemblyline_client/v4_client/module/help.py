from assemblyline_client.v4_client.common.utils import api_path_by_module


class Help(object):
    def __init__(self, connection):
        self._connection = connection

    def classification_definition(self):
        """\
Return the current system classification definition
"""
        return self._connection.get(api_path_by_module(self))

    def configuration(self):
        """\
Return the current system configuration:
    * Max file size
    * Max number of embedded files
    * Extraction's max depth
    * and many others...
"""
        return self._connection.get(api_path_by_module(self))

    def constants(self):
        """\
Return the current system configuration constants which include:
    * Priorities
    * File types
    * Service tag types
    * Service tag contexts
"""
        return self._connection.get(api_path_by_module(self))

    def tos(self):
        """\
Return the current system terms of service
"""
        return self._connection.get(api_path_by_module(self))
