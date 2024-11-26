from assemblyline_client.v4_client.module.file import File
from assemblyline_client.v4_client.module.alert import Alert
from assemblyline_client.v4_client.module.result import Result
from assemblyline_client.v4_client.module.badlist import Badlist
from assemblyline_client.v4_client.module.safelist import Safelist
from assemblyline_client.v4_client.module.signature import Signature
from assemblyline_client.v4_client.module.submission import Submission
from assemblyline_client.v4_client.module.workflow import Workflow
# AL client wrapper to allow direct assemblyline_client actions from queries

class BaseWrapper(dict):
    def __init__(self, connection, data):
        self.connection = connection
        super().__init__(data)

    def run(self):
        print("function ran")


class FileWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.file = File(connection)
        super().__init__(connection, data)

    def download(self):
        return self.file.download(self['sha256'])

    def delete_from_filestore(self):
        return self.file.delete_from_filestore(self['sha256'])

    def hex(self, bytes_only=False, length=None):
        return self.file.hex(self['sha256'], bytes_only, length)

    def info(self):
        return self.file.info(self['sha256'])

    def result(self):
        return self.file.result(self['sha256'])

    def score(self):
        return self.file.score(self['sha256'])

    def strings(self):
        return self.file.strings(self['sha256'])

    def children(self):
        return self.file.children(self['sha256'])

    def ascii(self):
        return self.file.ascii(self['sha256'])


class AlertWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.alert = Alert(connection)
        super().__init__(connection, data) 

    def __call__(self):
        return self.alert(self['id'])

    def grouped(self, field, fq=[], q=None, tc_start=None, tc=None, no_delay=False, offset=0, rows=10,
                use_archive=False, track_total_hits=None):
        return self.alert.grouped(field, fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay, offset=offset, rows=rows, use_archive=use_archive, track_total_hits=track_total_hits)


    def label(self, *labels):
        return self.alert.label(self['id'], *labels)

    def labels(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        return self.alert.labels(fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay)


    def list(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False, offset=0, rows=10,
             use_archive=False, track_total_hits=None):
        return self.alert.list(fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay, offset=offset, rows=rows, use_archive=use_archive, track_total_hits=track_total_hits)

    def ownership(self):
        return self.alert.ownership(self['id'])

    def priority(self, priority):
        return self.alert.priority(self['id'], priority)

    def priorities(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        return self.alert.priorities(fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay)

    def related(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        return self.alert.related(fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay)

    def remove_label(self, *labels):
        return self.alert.remove_label(self['id'], *labels)

    def statistics(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        return self.alert.statistics(fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay)

    def status(self, status):
        return self.alert.status(self['id'], status)

    def statuses(self, fq=[], q=None, tc_start=None, tc=None, no_delay=False):
        return self.alert.statuses(fq=fq, q=q, tc_start=tc_start, tc=tc, no_delay=no_delay)

    def verdict(self, verdict):
        return self.alert.verdict(self['id'], verdict)


class BadlistWrapper(BaseWrapper):
    
    def __init__(self, connection, data):
        self.badlist = Badlist(connection)
        super().__init__(connection, data)

    def __call__(self, qhash):
        return self.badlist(qhash)

    def add_update(self, badlist_object):
        return self.badlist.add_update(badlist_object)

    def add_update_many(self, list_of_badlist_object):
        return self.badlist.add_update_many(list_of_badlist_object)

    def delete(self):
        return self.badlist.delete(self['id'])

    def set_enabled(self, enabled):
        return self.badlist.set_enabled(self['id'], enabled)

    def ssdeep(self):
        return self.badlist.ssdeep(self['hashes']['ssdeep'])

    def tlsh(self):
        return self.badlist.tlsh(self['hashes']['tlsh'])


class HeuristicWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.heuristic = Heuristic(connection)
        super().__init__(connection, data)

    def __call__(self):
        return self.heuristic(self['id'])

    def stats(self):
        return self.heuristic.stats()


class ResultWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.result = Result(connection)
        super().__init__(connection, data)

    def __call__(self):
        return self.result(self['id'])

    def error(self):
        return self.result.error(self['id'])

    def multiple(self, error=None, result=None):
        return self.result.multiple(error, result)


class SafelistWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.safelist = Safelist(connection)
        super().__init__(connection, data)

    def __call__(self):
        return self.safelist(self['id'])

    def add_update(self, safelist_object):
        return self.safelist.add_update(safelist_object)

    def add_update_many(self, list_of_safelist_object):
        return self.safelist.add_update_many(list_of_safelist_object)

    def delete(self):
        return self.safelist.delete(self['id'])

    def set_enabled(self, enabled):
        return self.safelist.set_enabled(self['id'],enabled)


class SignatureWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.signature = Signature(connection)
        super().__init__(connection, data)

    def __call__(self):
        return self.signature(self['id'])

    def add_update(self, data, dedup_name=True):
        return self.signature.add_update(data, dedup_name=dedup_name)

    def add_update_many(self, source, sig_type, data, dedup_name=True):
        return self.signature.add_update_many(source, sig_type, data, dedup_name=dedup_name)

    def change_status(self, status):
        return self.signature.change_status(self['id'], status)

    def clear_status(self):
        return self.signature.clear_status(self['id'])

    def delete(self):
        return self.signature.delete(self['id'])

    def download(self, output=None, query=None):
        return self.signature.download(output=output, query=query)

    def stats(self):
        return self.signature.stats()

    def update_available(self, since='', sig_type='*'):
        return self.signature.update_available(since=since, sig_type=sig_type)


class SubmissionWrapper(BaseWrapper):

    def __init__(self, connection, data):
        self.submission = Submission(connection)
        super().__init__(connection, data)

    def __call__(self):
        return self.submission(self['sid'])

    def delete(self):
        return self.submission.delete(self['sid'])

    def file(self, sha256, results=None, errors=None):
        return self.submission.file(self['sid'], sha256, results=results, errors=errors)

    def full(self):
        return self.submission.full(self['sid'])

    def is_completed(self):
        return self.submission.is_completed(self['sid'])

    def list(self, user=None, group=None, fq=None, rows=10, offset=0, use_archive=False, track_total_hits=None):
        return self.submission.list(user=user, group=group, fq=fq, rows=rows, offset=offset, use_archive=use_archive, track_total_hits=track_total_hits)

    def report(self):
        return self.submission.report(self['sid'])

    def set_verdict(self, verdict):
        return self.submission.set_verdict(self['sid'], verdict)

    def summary(self):
        return self.submission.summary(self['sid'])

    def tree(self):
        return self.submission.tree(self['sid'])


class WorkflowWrapper(BaseWrapper):
 
    def __init__(self, connection, data):
        self.workflow = Workflow(connection)
        super().__init__(connection, data)

    def __call__(self):
        return self.workflow(self['workflow_id'])

    def add(self, workflow):
        return self.workflow.add(workflow)

    def delete(self):
        return self.workflow.delete(self['workflow_id'])

    def labels(self):
        return self.workflow.labels()

    def list(self, query="*:*", rows=10, offset=0):
        return self.workflow.list(query=query, rows=rows, offset=offset)

    def update(self, workflow):
        return self.workflow.update(self['workflow_id'], workflow)
