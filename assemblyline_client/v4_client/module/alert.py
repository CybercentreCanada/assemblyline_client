from assemblyline_client.v4_client.common.utils import api_path_by_module, get_function_kwargs, api_path


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

    def grouped(self, field, fq=[], q=None, tc_start=None, tc=None, no_delay=False, offset=0, rows=10,
                use_archive=False, track_total_hits=None):
        """\
List all alert grouped by a given field

Required:
field:    Field to group the alerts by

Optional:
fq                : Post filter queries (you can have multiple of these)
q                 : Query to apply to the alert list
no_delay          : Do not delay alerts
offset            : Offset at which we start giving alerts
rows              : Number of alerts to return
tc_start          : Time offset at which we start the time constraint
tc                : Time constraint applied to the API
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'offset': offset,
            'params_tuples': params_tuples,
            'q': q,
            'rows': rows,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = True
        if use_archive:
            kw['use_archive'] = ''
        if track_total_hits:
            kw['track_total_hits'] = track_total_hits

        return self._connection.get(api_path_by_module(self, field, **kw))

    def label(self, alert_id, *labels):
        """\
Add label(s) to the alert with the given alert_id.

Required:
alert_id: Alert key (string)
*labels : One or more labels (variable argument list of strings)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.post(api_path_by_module(self, alert_id), json=labels)

    def labels(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        """\
Find the different labels matching the query.

Optional:
fq      : Post filter queries (you can have multiple of these)
q       : Query to apply to the alert list
tc_start: Time offset at which we start the time constraint
tc      : Time constraint applied to the API
no_delay: Do not delay alerts
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'params_tuples': params_tuples,
            'q': q,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = True

        return self._connection.get(api_path_by_module(self, **kw))

    def list(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False, offset=0, rows=10,
             use_archive=False, track_total_hits=None):
        """\
List all alerts in the system (per page)

Optional:
fq                : Post filter queries (you can have multiple of these)
q                 : Query to apply to the alert list
no_delay          : Do not delay alerts
offset            : Offset at which we start giving alerts
rows              : Number of alerts to return
tc_start          : Time offset at which we start the time constraint
tc                : Time constraint applied to the API
use_archive       : Also query the archive
track_total_hits  : Number of hits to track (default: 10k)
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'offset': offset,
            'params_tuples': params_tuples,
            'q': q,
            'rows': rows,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = ''
        if use_archive:
            kw['use_archive'] = ''
        if track_total_hits:
            kw['track_total_hits'] = track_total_hits

        return self._connection.get(api_path_by_module(self, **kw))

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

    def priorities(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        """\
Find the different priorities matching the query.

Optional:
fq      : Post filter queries (you can have multiple of these)
q       : Query to apply to the alert list
tc_start: Time offset at which we start the time constraint
tc      : Time constraint applied to the API
no_delay: Do not delay alerts
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'params_tuples': params_tuples,
            'q': q,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = True

        return self._connection.get(api_path_by_module(self, **kw))

    def related(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        """\
Return the list of all IDs related to the currently selected query.

Optional:
fq      : Post filter queries (you can have multiple of these)
q       : Query to apply to the alert list
tc_start: Time offset at which we start the time constraint
tc      : Time constraint applied to the API
no_delay: Do not delay alerts
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'params_tuples': params_tuples,
            'q': q,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = True

        return self._connection.get(api_path_by_module(self, **kw))

    def remove_label(self, alert_id, *labels):
        """\
Remove label(s) from the alert with the given alert_id.

Required:
alert_id: Alert key (string)
*labels : One or more labels (variable argument list of strings)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.delete(api_path(f'alert/label/{alert_id}'), json=labels)

    def statistics(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        """\
Find the different statistics for the alerts matching the query.

Optional:
fq      : Post filter queries (you can have multiple of these)
q       : Query to apply to the alert list
tc_start: Time offset at which we start the time constraint
tc      : Time constraint applied to the API
no_delay: Do not delay alerts
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'params_tuples': params_tuples,
            'q': q,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = True

        return self._connection.get(api_path_by_module(self, **kw))

    def status(self, alert_id, status):
        """\
Set the status of the alert with the given alert_id.

Required:
alert_id: Alert key (string)
status  : Status (enum: MALICIOUS, NON-MALICIOUS, ASSESS)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.post(api_path_by_module(self, alert_id), json=status)

    def statuses(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        """\
Find the different statuses matching the query.

Optional:
fq      : Post filter queries (you can have multiple of these)
q       : Query to apply to the alert list
tc_start: Time offset at which we start the time constraint
tc      : Time constraint applied to the API
no_delay: Do not delay alerts
"""
        params_tuples = [('fq', x) for x in fq]
        kw = {
            'params_tuples': params_tuples,
            'q': q,
            'tc_start': tc_start,
            'tc': tc
        }
        if no_delay:
            kw['no_delay'] = True

        return self._connection.get(api_path_by_module(self, **kw))

    def verdict(self, alert_id, verdict):
        """\
Set the verdict of the alert with the given alert_id.

Required:
alert_id: Alert key (string)
verdict : Verdict (enum: malicious, non_malicious)

Throws a Client exception if the alert does not exist.
"""
        return self._connection.put(api_path_by_module(self, alert_id, verdict))


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

        kw = get_function_kwargs('self', 'fq_list', 'labels')
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

        kw = get_function_kwargs('self', 'fq_list', 'ownership')
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

        kw = get_function_kwargs('self', 'fq_list', 'priority')
        path = api_path('alert/priority/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.post(path, json=priority)

    def remove_label(self, q, labels, tc=None, tc_start=None, fq_list=None):
        """\
Remove labels from alerts matching the search criteria.

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

        kw = get_function_kwargs('self', 'fq_list', 'labels')
        path = api_path('alert/label/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.delete(path, json=labels)

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

        kw = get_function_kwargs('self', 'fq_list', 'status')
        path = api_path('alert/status/batch', params_tuples=[('fq', fq) for fq in fq_list], **kw)

        return self._connection.post(path, json=status)
