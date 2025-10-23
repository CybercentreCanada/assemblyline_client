
from assemblyline_client.common.classification import Classification
from assemblyline_client.v4_client.common.utils import ClientError, walk_api_path
from assemblyline_client.v4_client.module.alert import Alert
from assemblyline_client.v4_client.module.assistant import Assistant
from assemblyline_client.v4_client.module.badlist import Badlist
from assemblyline_client.v4_client.module.bundle import Bundle
from assemblyline_client.v4_client.module.error import Error
from assemblyline_client.v4_client.module.file import File
from assemblyline_client.v4_client.module.hash_search import HashSearch
from assemblyline_client.v4_client.module.help import Help
from assemblyline_client.v4_client.module.heuristics import Heuristics
from assemblyline_client.v4_client.module.ingest import Ingest
from assemblyline_client.v4_client.module.ontology import Ontology
from assemblyline_client.v4_client.module.replay import Replay
from assemblyline_client.v4_client.module.result import Result
from assemblyline_client.v4_client.module.safelist import Safelist
from assemblyline_client.v4_client.module.search import Search
from assemblyline_client.v4_client.module.service import Service
from assemblyline_client.v4_client.module.signature import Signature
from assemblyline_client.v4_client.module.socketio import SocketIO
from assemblyline_client.v4_client.module.submission import Live, Submission
from assemblyline_client.v4_client.module.submit import Submit
from assemblyline_client.v4_client.module.system import System
from assemblyline_client.v4_client.module.user import User
from assemblyline_client.v4_client.module.workflow import Workflow


class Client(object):
    def __init__(self, connection):
        self._connection = connection

        self.alert = Alert(self._connection)
        self.assistant = Assistant(self._connection)
        self.badlist = Badlist(self._connection)
        self.bundle = Bundle(self._connection)
        self.error = Error(self._connection)
        self.file = File(self._connection)
        self.hash_search = HashSearch(self._connection)
        self.help = Help(self._connection)
        self.heuristics = Heuristics(self._connection)
        self.ingest = Ingest(self._connection)
        self.live = Live(self._connection)
        self.ontology = Ontology(self._connection)
        self.replay = Replay(self._connection)
        self.result = Result(self._connection)
        self.safelist = Safelist(self._connection)
        self.search = Search(self._connection)
        self.service = Service(self._connection)
        self.signature = Signature(self._connection)
        self.socketio = SocketIO(self._connection)
        self.submission = Submission(self._connection)
        self.submit = Submit(self._connection)
        self.system = System(self._connection)
        self.user = User(self._connection)
        self.workflow = Workflow(self._connection)

        paths = []
        walk_api_path(self, [''], paths)

        self.__doc__ = 'Client provides the following methods:\n\n' + \
            '\n'.join(['\n'.join(p + ['']) for p in paths])

    def _load_quotas(self):
        try:
            resp = self.user.quotas(self._connection.current_user)
            self._connection.remaining_api_quota = resp['daily_api']
            self._connection.remaining_submission_quota = resp['daily_submission']
        except ClientError:
            pass

    @property
    def current_user(self):
        return self._connection.current_user

    def get_remaining_api_quota(self):
        if self._connection.remaining_api_quota is not None:
            return self._connection.remaining_api_quota

        self._load_quotas()
        return self._connection.remaining_api_quota

    def get_remaining_submission_quota(self):
        if self._connection.remaining_submission_quota is not None:
            return self._connection.remaining_submission_quota

        self._load_quotas()
        return self._connection.remaining_submission_quota

    def get_classification_engine(self):
        definition = self.help.classification_definition(original=True)
        return Classification(definition)

    def set_obo_token(self, token, provider=None):
        new_headers = {'authorization': f"Bearer {token}"}
        if provider:
            new_headers['x-token-provider'] = provider
        else:
            self._connection.session.headers.pop('x-token-provider', None)
        self._connection.session.headers.update(new_headers)

    def clear_obo_token(self):
        self._connection.session.headers.pop('authorization', None)
        self._connection.session.headers.pop('x-token-provider', None)
