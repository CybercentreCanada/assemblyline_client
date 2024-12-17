from assemblyline_client.v4_client.module.alert import Alert
from assemblyline_client.v4_client.module.badlist import Badlist
from assemblyline_client.v4_client.module.file import File
from assemblyline_client.v4_client.module.heuristics import Heuristics
from assemblyline_client.v4_client.module.result import Result
from assemblyline_client.v4_client.module.safelist import Safelist
from assemblyline_client.v4_client.module.signature import Signature
from assemblyline_client.v4_client.module.submission import Submission
from assemblyline_client.v4_client.module.workflow import Workflow

wrapper_search = None


def wrapper_function(inner_func, args=[]):
    """
Decorator for wrapper functions to provide docstrings for documentation.

Required:
inner_func: Function that is being wrapped (.ie function called inside of a wrapper function)
args: List of required arguments to not remove from an inner function's docstring

Sets the __doc__ attribute of the decorated function to the modified __doc__ of the inner function.
    """

    def decorator(func):
        hits = ['Required:', 'Optional:']
        clear = False
        docstring = []
        for line in inner_func.__doc__.splitlines():
            if line in hits:
                if len(args) != 0:
                    docstring.append(line)
                clear = True
            if line == '':
                clear = False
            if not clear or line.split(":")[0].strip() in args:
                docstring.append(line)
        func.__doc__ = "\n".join(docstring)
        return func

    return decorator


class BaseWrapper(dict):
    def __init__(self, search, data):
        self.search = search
        super().__init__(data)


class FileWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.file = File(search._connection)
        super().__init__(search, data)

    @wrapper_function(File.download)
    def download(self, *args, **kwargs):
        return self.file.download(self['sha256'], *args, **kwargs)

    @wrapper_function(File.delete_from_filestore)
    def delete_from_filestore(self, *args, **kwargs):
        return self.file.delete_from_filestore(self['sha256'], *args, **kwargs)

    @wrapper_function(File.hex)
    def hex(self, *args, **kwargs):
        return self.file.hex(self['sha256'], *args, **kwargs)

    @wrapper_function(File.info)
    def info(self, *args, **kwargs):
        return self.file.info(self['sha256'], *args, **kwargs)

    @wrapper_function(File.result)
    def result(self, *args, **kwargs):
        return self.file.result(self['sha256'], *args, **kwargs)

    @wrapper_function(File.score)
    def score(self, *args, **kwargs):
        return self.file.score(self['sha256'], *args, **kwargs)

    @wrapper_function(File.strings)
    def strings(self, *args, **kwargs):
        return self.file.strings(self['sha256'], *args, **kwargs)

    @wrapper_function(File.children)
    def children(self, *args, **kawrgs):
        return self.file.children(self['sha256'], *args, **kwargs)

    @wrapper_function(File.ascii)
    def ascii(self, *args, **kwargs):
        return self.file.ascii(self['sha256'], *args, **kwargs)

    def get_submissions(self):
        """\
Get the submissions from a file.

Returns a list of SubmissionWrapper.
"""
        return self.search.submission(self['sha256'])['items']

    def get_results(self):
        """\
Get the results of a file.

Returns a list of ResultWrapper.
"""
        return self.search.result(f"sha256:{self['sha256']}")['items']

    def get_extracted_files(self):
        """\
Get extracted files from a file. This searches for all results related to a sha256.

Returns a list of FileWrapper.
"""
        try:
            extracted_files = [result()['response']['extracted']
                               for result in self.get_results()]

            query = ""
            for files in extracted_files:
                if len(files) == 0:
                    continue
                for idx, file in enumerate(files):
                    if idx + 1 == len(files):
                        query += f"{file['sha256']}"
                        continue
                    query += f"{file['sha256']} OR "
            return self.search.file(query)['items']

        except KeyError:
            return []


class AlertWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.alert = Alert(search._connection)
        super().__init__(search, data)

    @wrapper_function(Alert.__call__)
    def __call__(self):
        return self.alert(self['id'])

    @wrapper_function(Alert.label, ["*labels"])
    def label(self, *args, **kwargs):
        return self.alert.label(self['id'], *args, **kwargs)

    @wrapper_function(Alert.ownership)
    def ownership(self):
        return self.alert.ownership(self['id'])

    @wrapper_function(Alert.priority, ["priority"])
    def priority(self, *args, **kwargs):
        return self.alert.priority(self['id'], *args, **kwargs)

    @wrapper_function(Alert.remove_label, ["*labels"])
    def remove_label(self, *args, **kwargs):
        return self.alert.remove_label(self['id'], *args, **kwargs)

    @wrapper_function(Alert.status, ["status"])
    def status(self, *args, **kwargs):
        return self.alert.status(self['id'], *args, **kwargs)

    @wrapper_function(Alert.verdict, ["verdict"])
    def verdict(self, *args, **kwargs):
        return self.alert.verdict(self['id'], *args, **kwargs)


class BadlistWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.badlist = Badlist(search._connection)
        super().__init__(search, data)

    @wrapper_function(Badlist.__call__)
    def __call__(self, *args, **kwargs):
        return self.badlist(*args, **kwargs)

    @wrapper_function(Badlist.delete)
    def delete(self, *args, **kwargs):
        return self.badlist.delete(self['id'], *args, **kwargs)

    @wrapper_function(Badlist.set_enabled, ["enabled"])
    def set_enabled(self, *args, **kwargs):
        return self.badlist.set_enabled(self['id'], *args, **kwargs)


class HeuristicWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.heuristic = Heuristics(search._connection)
        super().__init__(search, data)

    @wrapper_function(Heuristics.__call__)
    def __call__(self):
        return self.heuristic(self['id'])


class ResultWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.result = Result(search._connection)
        super().__init__(search, data)

    @wrapper_function(Result.__call__)
    def __call__(self):
        return self.result(self['id'])

    @wrapper_function(Result.error)
    def error(self, *args, **kwargs):
        return self.result.error(self['id'], *args, **kwargs)


class SafelistWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.safelist = Safelist(search._connection)
        super().__init__(search, data)

    @wrapper_function(Safelist.__call__)
    def __call__(self):
        return self.safelist(self['id'])

    @wrapper_function(Safelist.delete)
    def delete(self, *args, **kwargs):
        return self.safelist.delete(self['id'], *args, **kwargs)

    @wrapper_function(Safelist.set_enabled, ["enabled"])
    def set_enabled(self, *args, **kwargs):
        return self.safelist.set_enabled(self['id'], *args, **kwargs)


class SignatureWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.signature = Signature(search._connection)
        super().__init__(search, data)

    @wrapper_function(Signature.__call__)
    def __call__(self):
        return self.signature(self['id'])

    @wrapper_function(Signature.change_status, ["status"])
    def change_status(self, *args, **kwargs):
        return self.signature.change_status(self['id'], *args, **kwargs)

    @wrapper_function(Signature.clear_status)
    def clear_status(self, *args, **kwargs):
        return self.signature.clear_status(self['id'], *args, **kwargs)

    @wrapper_function(Signature.delete)
    def delete(self, *args, **kwargs):
        return self.signature.delete(self['id'], *args, **kwargs)


class SubmissionWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.submission = Submission(search._connection)
        super().__init__(search, data)

    @wrapper_function(Submission.__call__)
    def __call__(self):
        return self.submission(self['sid'])

    @wrapper_function(Submission.delete)
    def delete(self, *args, **kwargs):
        return self.submission.delete(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.file, ["sha256"])
    def file(self, *args, **kwargs):
        return self.submission.file(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.full)
    def full(self, *args, **kwargs):
        return self.submission.full(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.is_completed)
    def is_completed(self, *args, **kwargs):
        return self.submission.is_completed(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.report)
    def report(self, *args, **kwargs):
        return self.submission.report(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.set_verdict, ["verdict"])
    def set_verdict(self, *args, **kwargs):
        return self.submission.set_verdict(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.summary)
    def summary(self, *args, **kwargs):
        return self.submission.summary(self['sid'], *args, **kwargs)

    @wrapper_function(Submission.tree)
    def tree(self, *args, **kwargs):
        return self.submission.tree(self['sid'], *args, **kwargs)

    def get_files(self):
        """\
Get the list of files that were originally submitted

Returns a list of FileWrapper
"""
        try:
            submission_files = self.full()['files']
            query = ""
            for idx, file in enumerate(submission_files):
                if idx + 1 == len(submission_files):
                    query += f"{file['sha256']}"
                    continue
                query += f"{file['sha256']} OR "

            return self.search.file(query)['items']
        except KeyError:
            return []


class WorkflowWrapper(BaseWrapper):

    def __init__(self, search, data):
        self.workflow = Workflow(search._connection)
        super().__init__(search, data)

    @wrapper_function(Workflow.__call__)
    def __call__(self):
        return self.workflow(self['workflow_id'])

    @wrapper_function(Workflow.delete)
    def delete(self):
        return self.workflow.delete(self['workflow_id'])

    @wrapper_function(Workflow.update, ["workflow"])
    def update(self, *args, **kwargs):
        return self.workflow.update(self['workflow_id'], *args, **kwargs)


wrapper_map = {
    'file': FileWrapper,
    'alert': AlertWrapper,
    'badlist': BadlistWrapper,
    'heuristic': HeuristicWrapper,
    'result': ResultWrapper,
    'safelist': SafelistWrapper,
    'signature': SignatureWrapper,
    'submission': SubmissionWrapper,
    'workflow': WorkflowWrapper
}
