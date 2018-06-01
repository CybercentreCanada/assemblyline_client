"""
A mock of the assemblyline server for testing the client.

Very simple and uses the built in HTTPServer.

- Accepts all logins
- Always returns the same submission id
- Stores data from logins and submissions
- Runs in process
"""
from __future__ import print_function

import threading
import os.path
import time
import json
import ssl

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random

try:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer


def load_async_key(key_def, use_pkcs=False):
    key = RSA.importKey(key_def)

    if use_pkcs:
        Random.atfork()
        return PKCS1_v1_5.new(key)

    return key


class AllowReuseHTTPServer(HTTPServer):
    allow_reuse_address = True


class AssemblylineHandler(BaseHTTPRequestHandler):
    """A mostly stateless request handler that logs some request data back to the server."""

    def get_body(self):
        try:
            content_len = int(self.headers.getheader('content-length', 0))
        except AttributeError:
            content_len = int(self.headers.get('content-length', 0))
        return json.loads(self.rfile.read(content_len))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.post_json(self.get_body())).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.get_json()).encode('utf-8'))

    def get_json(self):
        path = self.path
        self.server.data.gets.append(path)
        if path.endswith('/api/v3/auth/init/'):
            return {'api_response': self.server.data.certificate}
        elif path.endswith('/api/v3/auth/login/'):
            self.server.data.logins.append(self.get_body())
            return {'api_response': {'session_duration': 600}}
        elif path.endswith('/api/'):
            return {'api_response': ['v3']}
        elif '/api/v3/live/setup_watch_queue/' in path:
            return {'api_response': {'wq_id': 'test_wq_id'}}
        elif '/api/v3/live/get_message_list/test_wq_id' in path:
            return {'api_response': [{'type': 'stop'}]}
        elif '/api/v3/submission/is_completed/' in path:
            return {'api_response': True}
        elif '/api/v3/submission/full/' in path:
            return {'api_response': {'missing_result_keys': []}}

        print('get', path)
        return {'api_response': {}}

    def post_json(self, body):
        path = self.path
        if path.endswith('/api/v3/submit/'):
            self.server.data.submits.append(body)
            return {
                'api_response': {
                    'submission': {
                        'sid': 'sidsidsid'
                    }
                }
            }

        print('post', path)
        print(body)
        return {
            'api_response': {}
        }

    def log_message(self, format, *args):
        self.server.data.logs.append((format, args))


class Server:
    """A HTTP server that serves as a stand in for Assemblyline in unit tests."""

    def __init__(self, port=0):
        # By default use port zero so the OS chooses a free port for us
        # tests can get the actual port by reading it after the server starts.
        self.port = port
        self.handler = AssemblylineHandler
        self.thread = None
        self.server = None

        srcdir = os.path.abspath(os.path.dirname(__file__))
        self.cert_path = os.path.join(srcdir, 'test.cert')
        self.key_path = os.path.join(srcdir, 'test.key')
        self.certificate = open(self.cert_path).read()
        self.private_key = load_async_key(open(self.key_path).read(), True)

        self.submits = []
        self.gets = []
        self.logins = []
        self.logs = []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def _start(self):
        self.server = AllowReuseHTTPServer(('localhost', self.port), self.handler)
        self.server.data = self
        self.server.socket = ssl.wrap_socket(self.server.socket, server_side=True,
                                             keyfile=self.key_path, certfile=self.cert_path)
        self.server.serve_forever()

    def start(self):
        self.thread = threading.Thread(target=self._start)
        self.thread.daemon = True
        self.thread.start()
        while self.server is None:
            time.sleep(0.5)
        time.sleep(0.5)
        self.port = self.server.server_port
        self.address = 'https://localhost:{}'.format(self.server.server_port)

    def stop(self):
        self.server.shutdown()
        self.thread.join()

    def got_like(self, part_path):
        for url in self.gets:
            if part_path in url:
                return True
        return False
