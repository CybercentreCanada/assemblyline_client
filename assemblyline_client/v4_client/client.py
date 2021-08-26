

from assemblyline_client.v4_client.common.utils import walk_api_path
from assemblyline_client.v4_client.module.alert import Alert
from assemblyline_client.v4_client.module.bundle import Bundle
from assemblyline_client.v4_client.module.error import Error
from assemblyline_client.v4_client.module.file import File
from assemblyline_client.v4_client.module.hash_search import HashSearch
from assemblyline_client.v4_client.module.help import Help
from assemblyline_client.v4_client.module.heuristics import Heuristics
from assemblyline_client.v4_client.module.ingest import Ingest
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
        self.bundle = Bundle(self._connection)
        self.error = Error(self._connection)
        self.file = File(self._connection)
        self.hash_search = HashSearch(self._connection)
        self.help = Help(self._connection)
        self.heuristics = Heuristics(self._connection)
        self.ingest = Ingest(self._connection)
        self.live = Live(self._connection)
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
