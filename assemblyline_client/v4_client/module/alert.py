from assemblyline_client.v4_client.common.utils import api_path_by_module, get_funtion_kwargs, api_path


class Alert(object):
    def __init__(self, connection):
        self._connection = connection
        self.batch = Batch(connection)

    def __call__(self, alert_id):
        """\
Return the full alert for a given alert_id.

Required:
alert_id: Alert key. (string)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.get(api_path('alert', alert_id))

    def label(self, alert_id, *labels):
        """\
Add label(s) to the alert with the given alert_id.

Required:
alert_id: Alert key (string)
*labels : One or more labels (variable argument list of strings)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.post(api_path_by_module(self, alert_id), json=labels)

    def ownership(self, alert_id):
        """\
Set the ownership of the alert with the given alert_id to the current user.

Required:
alert_id: Alert key (string)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.get(api_path_by_module(self, alert_id))

    def priority(self, alert_id, priority):
        """\
Set the priority of the alert with the given alert_id.

Required:
alert_id: Alert key (string)
priority: Priority (enum: LOW, MEDIUM, HIGH, CRITICAL)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.post(api_path_by_module(self, alert_id), json=priority)

    def status(self, alert_id, status):
        """\
Set the status of the alert with the given alert_id.

Required:
alert_id: Alert key (string)
status  : Status (enum: MALICIOUS, NON-MALICIOUS, ASSESS)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.post(api_path_by_module(self, alert_id), json=status)


# noinspection PyUnusedLocal
class Batch(object):
    def __init__(self, connection):
        self._connection = connection

    def label(self, q, labels, tc=None, tc_start=None, fq_list=None):
        """\
Add labels to alerts matching the search criteria.

Required:
q       : Query used to limit the scope of the data (string)
labels  : Labels to apply (list of strings)

Optional:
tc         : Time constraint applied to the query (string)
tc_start   : Date which the time constraint will be applied to [Default: NOW] (string)
fq_list    : List of filter queries (list of strings)
"""
        if not fq_list:
            fq_list = []

        kw = get_funtion_kwargs('self', 'fq_list', 'labels')
        path = api_path('alert/label/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.post(path, json=labels)

    def ownership(self, q, tc=None, tc_start=None, fq_list=None):
        """\
Set ownership on alerts matching the search criteria.

Required:
q       : Query used to limit the scope of the data (string)

Optional:
tc         : Time constraint applied to the query (string)
tc_start   : Date which the time constraint will be applied to [Default: NOW] (string)
fq_list    : List of filter queries (list of strings)
"""
        if not fq_list:
            fq_list = []

        kw = get_funtion_kwargs('self', 'fq_list', 'ownership')
        path = api_path('alert/ownership/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.get(path)

    def priority(self, q, priority, tc=None, tc_start=None, fq_list=None):
        """\
Set the priority on alerts matching the search criteria.

Required:
q       : Query used to limit the scope of the data (string)
priority: Priority (enum: LOW, MEDIUM, HIGH, CRITICAL)

Optional:
tc         : Time constraint applied to the query (string)
tc_start   : Date which the time constraint will be applied to [Default: NOW] (string)
fq_list    : List of filter queries (list of strings)
"""
        if not fq_list:
            fq_list = []

        kw = get_funtion_kwargs('self', 'fq_list', 'priority')
        path = api_path('alert/priority/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.post(path, json=priority)

    def status(self, q, status, tc=None, tc_start=None, fq_list=None):
        """\
Set the status on alerts matching the search criteria.

Required:
q       : Query used to limit the scope of the data (string)
status  : Status (enum: MALICIOUS, NON-MALICIOUS, ASSESS)

Optional:
tc         : Time constraint applied to the query (string)
tc_start   : Date which the time constraint will be applied to [Default: NOW] (string)
fq_list    : List of filter queries (list of strings)
"""
        if not fq_list:
            fq_list = []

        kw = get_funtion_kwargs('self', 'fq_list', 'status')
        path = api_path('alert/status/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.post(path, json=status)
