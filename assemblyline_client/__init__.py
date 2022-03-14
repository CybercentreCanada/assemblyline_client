import json
from base64 import b64encode

import pkg_resources
import requests
import time
import warnings

from assemblyline_client.v4_client.common.utils import ClientError

from assemblyline_client.v3_client import Client as Client3
from assemblyline_client.v4_client.client import Client as Client4


try:
    __version__ = pkg_resources.get_distribution('assemblyline_client').version
except pkg_resources.DistributionNotFound:
    __version__ = "4.0.0.dev0"

RETRY_FOREVER = 0
SUPPORTED_APIS = {'v3', 'v4'}


def convert_api_output(response):
    return response.json()['api_response']


# This is done for backward compatibility only you are encourage to use get_client function instead
def Client(*args, **kwargs):
    warnings.warn("Object assemblyline_client.Client is deprecated. Use get_client() function instead.")
    return get_client(*args, **kwargs)


def get_client(server, auth=None, cert=None, debug=lambda x: None, headers=None, retries=RETRY_FOREVER,
               silence_requests_warnings=True, apikey=None, verify=True, timeout=None):
    connection = Connection(server, auth, cert, debug, headers, retries,
                            silence_requests_warnings, apikey, verify, timeout)
    if connection.is_v4:
        return Client4(connection)
    else:
        return Client3(connection)


class Connection(object):
    def __init__(  # pylint: disable=R0913
        self, server, auth, cert, debug, headers, retries,
        silence_warnings, apikey, verify, timeout
    ):
        self.auth = auth
        self.apikey = apikey
        self.debug = debug
        self.is_v4 = False
        self.max_retries = retries
        self.server = server
        self.silence_warnings = silence_warnings
        self.verify = verify
        self.default_timeout = timeout

        session = requests.Session()

        session.headers.update({'content-type': 'application/json'})
        session.verify = verify

        if cert:
            session.cert = cert
        if headers:
            session.headers.update(headers)

        self.session = session

        try:
            auth_session_detail = self._authenticate()
        except requests.exceptions.SSLError as ssle:
            raise ClientError("Client could not connect to the server "
                              "due to the following SSLError: %s" % ssle, 495)

        session.timeout = auth_session_detail['session_duration']

        r = self.request(self.session.get, 'api/', convert_api_output)
        if not isinstance(r, list) or not set(r).intersection(SUPPORTED_APIS):
            raise ClientError("Supported APIS (%s) are not available" % SUPPORTED_APIS, 400)

    def _load_public_encryption_key(self):
        public_key = self.request(self.session.get, "api/v3/auth/init/", convert_api_output)

        if not public_key:
            return None

        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5

        key = RSA.importKey(public_key)
        return PKCS1_v1_5.new(key)

    def _authenticate(self):
        try:
            public_key = self._load_public_encryption_key()
            self.is_v4 = False
        except ClientError as ce:
            public_key = None
            if ce.status_code == 404:
                self.is_v4 = True
            else:
                raise

        if self.is_v4:
            if self.apikey and len(self.apikey) == 2:
                auth = {
                    'user': self.apikey[0],
                    'apikey': self.apikey[1]
                }
            elif self.auth and len(self.auth) == 2:
                auth = {
                    'user': self.auth[0],
                    'password': self.auth[1]
                }
            else:
                auth = {}
            return self.request(self.session.get, "api/v4/auth/login/", convert_api_output, data=json.dumps(auth))
        else:
            if self.apikey and len(self.apikey) == 2:
                if public_key:
                    key = b64encode(public_key.encrypt(self.apikey[1].encode("UTF-8")))
                    if isinstance(key, bytes) and not isinstance(key, str):
                        key = key.decode("UTF-8")
                else:
                    key = self.apikey[1]
                auth = {
                    'user': self.apikey[0],
                    'apikey': key
                }
            elif self.auth and len(self.auth) == 2:
                if public_key:
                    pw = b64encode(public_key.encrypt(self.auth[1].encode("UTF-8")))
                    if isinstance(pw, bytes) and not isinstance(pw, str):
                        pw = pw.decode("UTF-8")
                else:
                    pw = self.auth[1]
                auth = {
                    'user': self.auth[0],
                    'password': pw
                }
            else:
                auth = {}
            return self.request(self.session.get, "api/v3/auth/login/", convert_api_output, data=json.dumps(auth))

    def delete(self, path, **kw):
        return self.request(self.session.delete, path, convert_api_output, **kw)

    def download(self, path, process, **kw):
        return self.request(self.session.get, path, process, **kw)

    def get(self, path, **kw):
        return self.request(self.session.get, path, convert_api_output, **kw)

    def post(self, path, **kw):
        return self.request(self.session.post, path, convert_api_output, **kw)

    def put(self, path, **kw):
        return self.request(self.session.put, path, convert_api_output, **kw)

    def request(self, func, path, process, **kw):
        self.debug(path)

        # Apply default timeout parameter if not passed elsewhere
        kw.setdefault('timeout', self.default_timeout)

        retries = 0
        with warnings.catch_warnings():
            if self.silence_warnings:
                warnings.simplefilter('ignore')
            while self.max_retries < 1 or retries <= self.max_retries:
                if retries:
                    time.sleep(min(2, 2 ** (retries - 7)))
                    stream = kw.get('files', {}).get('bin', None)
                    if stream and 'seek' in dir(stream):
                        stream.seek(0)

                try:
                    response = func('/'.join((self.server, path)), **kw)
                    if 'XSRF-TOKEN' in response.cookies:
                        self.session.headers.update({'X-XSRF-TOKEN': response.cookies['XSRF-TOKEN']})
                    if response.ok:
                        return process(response)
                    elif response.status_code == 401:
                        try:
                            resp_data = response.json()
                            if resp_data["api_error_message"] in ["Session rejected",
                                                                  "Session not found",
                                                                  "Session expired",
                                                                  "Invalid source IP for this session",
                                                                  "Invalid user agent for this session"]:
                                self._authenticate()
                            else:
                                raise ClientError(resp_data["api_error_message"], response.status_code,
                                                  api_version=resp_data["api_server_version"],
                                                  api_response=resp_data["api_response"])
                        except Exception as e:
                            if isinstance(e, ClientError):
                                raise

                            raise ClientError(response.content, response.status_code)

                    elif response.status_code not in (502, 503, 504):
                        try:
                            resp_data = response.json()
                            raise ClientError(resp_data["api_error_message"], response.status_code,
                                              api_version=resp_data["api_server_version"],
                                              api_response=resp_data["api_response"])
                        except Exception as e:
                            if isinstance(e, ClientError):
                                raise

                            raise ClientError(response.content, response.status_code)
                except (requests.exceptions.SSLError, requests.exceptions.ProxyError):
                    raise
                except requests.exceptions.ConnectionError:
                    pass
                except OSError as e:
                    if "Connection aborted" not in str(e):
                        raise

                retries += 1

            raise ClientError("Max retry reached, could not perform the request.")
