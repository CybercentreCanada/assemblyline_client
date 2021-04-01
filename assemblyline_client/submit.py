#!/usr/bin/env python

import datetime
import sys
import select
import json
import io

from errno import EPIPE
from getpass import getpass
from os.path import exists, isdir, basename, join, expanduser
from os import walk
from signal import signal, SIGINT, SIG_DFL
from threading import Thread, Lock
from time import sleep

from configparser import ConfigParser

from assemblyline_client.v4_client.client import Client as Client4
from assemblyline_client import get_client, __version__ as client_version
from assemblyline_client.v4_client.common.utils import ClientError, get_random_id, get_id_from_path

ASYNC_LOCK = Lock()

__version__ = "al_submit v%s" % client_version
al_result_to_text = None


# noinspection PyCallingNonCallable
def result_to_text(data):
    if sys.version_info < (3, 0):
        results = [x.decode('utf-8') for x in al_result_to_text(data)]
    else:
        results = al_result_to_text(data)
    return "\n".join(results)


def get_details_from_key(key):
    file_hash = key[:64]
    key = key[65:]
    name = key[:key.index(".")]

    return file_hash, name


def compute_results(client, sid, output, verbose, name, options):
    if verbose:
        sys.stderr.write("\tAll messages received, fetching results...\n")

    final_results = client.submission.full(sid)
    if output:
        write_file(final_results, output, name, **options)
    else:
        write_to_sdtout(final_results, **options)


# send(client, input_file, output, verbose=verbose, **kw)
def send(client, path, output, options=None, **kw):
    if options is None:
        options = {}
    name = basename(path)
    verbose = options.get('verbose', False)

    try:
        submission = client.submit(path=path, **kw)
        sid = submission.get('sid', None) or submission.get('submission', {}).get('sid', None)
        if not sid:
            sys.stderr.write("!!ERROR!! Could not find the sid opf the submitted file.\n")
            return False

        if verbose:
            sys.stderr.write("File %s submitted for analysis [sid: %s]\n" % (name, sid))

        wq_id = client.live.setup_watch_queue(sid)['wq_id']
        if verbose:
            sys.stderr.write("\tListening for incoming results (WQ_ID: %s)\n" % wq_id)

        start_msg_received = False
        done = False
        while not done:
            msgs = client.live.get_message_list(wq_id)
            for m in msgs:
                if m['type'] == "start":
                    if verbose:
                        sys.stderr.write("\tProcessing...\n")

                    start_msg_received = True

                # Dispatcher will send a 'stop' message if it receives
                # request to start a watch queue for a file it
                # hasn't received it yet. Check completion via
                # submission.is_completed api, continue listening if not completed.
                elif m['type'] == "stop" and not start_msg_received:
                    if client.submission.is_completed(sid):
                        compute_results(client, sid, output, verbose, name, options)
                        done = True
                        break
                    else:
                        wq_id = client.live.setup_watch_queue(sid)['wq_id']
                        if verbose:
                            sys.stderr.write("\tSubmission hasn't started on the server yet (new WQ_ID: %s)\n" % wq_id)

                elif m['type'] == "stop":
                    compute_results(client, sid, output, verbose, name, options)
                    done = True
                    break
                elif m["type"] == "cachekey" or m["type"] == "cachekeyerr":
                    file_hash, srv_name = get_details_from_key(m["msg"])
                    if verbose:
                        m_type = 'ERROR' if m['type'] == 'cachekeyerr' else 'SUCCESS'
                        sys.stderr.write("\t\t[x] %s (%s) - %s\n" % (srv_name, file_hash, m_type))
                else:
                    if verbose:
                        sys.stdout.write("%s\n" % m)

            if not done:
                sleep(2)

    except ClientError as e:
        if e.status_code == 401:
            sys.stderr.write("!!ERROR!! Authentication to the server failed.\n")
        elif e.status_code == 403:
            data = json.loads(e)
            sys.stderr.write("!!ERROR!! %s\n" % data['api_error_message'])
        elif e.status_code == 400 and "File empty" in str(e):
            sys.stderr.write("!!ERROR!! Failed to submit '%s' skipped because it is empty.\n" % path)
        else:
            raise
        return False

    return True


def main():
    sys.exit(_main(sys.argv[1:]))


description_string = """Submit a file to AL using the web API and write the results to a file or to stdout.
NOTE: If file not provided, will read the file from stdin and output results to stdout."""


# noinspection PyBroadException
def _main(arguments):
    global al_result_to_text

    signal(SIGINT, SIG_DFL)
    if sys.platform.startswith("linux"):
        from signal import SIGPIPE
        signal(SIGPIPE, SIG_DFL)

    user = None
    pw = None
    cert = None
    apikey = None
    transport = "https"
    host = "localhost"
    port = 443
    kw = {}
    verify = True

    config = ConfigParser()
    config.read([expanduser("~/.al/submit.cfg")])
    for section in config.sections():
        if section == "auth":
            if 'user' in config.options('auth'):
                user = config.get('auth', 'user')
            if 'password' in config.options('auth'):
                pw = config.get('auth', 'password')
            if 'cert' in config.options('auth'):
                cert = config.get('auth', 'cert')
            if 'apikey' in config.options('auth'):
                apikey = config.get('auth', 'apikey')
            if 'insecure' in config.options('auth'):
                verify = config.get('auth', 'insecure').lower() not in ['true', 'yes']
        elif section == "server":
            if 'transport' in config.options('server'):
                transport = config.get('server', 'transport')
            if 'host' in config.options('server'):
                host = config.get('server', 'host')
            if 'port' in config.options('server'):
                port = config.get('server', 'port')
            if 'cert' in config.options('server'):
                verify = config.get('server', 'cert')

    server = "%s://%s:%s" % (transport, host, port)

    # parse the command line args
    from argparse import ArgumentParser
    parser = ArgumentParser(description=description_string)
    parser.add_argument('files', metavar='file/dir', nargs='+')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-q', '--quiet', action='store_true', help='Runs in quiet mode')
    parser.add_argument('-a', '--async', dest='async_command', action='store_true',
                        help='Run in asynchronized mode (uses ingest API).')
    parser.add_argument('-n', '--no-output', action='store_true',
                        help='Only works in conjunction with -a. Ingests the file and does not wait for the output.')
    parser.add_argument('-i', '--insecure', action='store_true', default=not verify,
                        help='Skip server cert validation. DEFAULT: insecure in auth section of ~/.al/submit.cfg')
    parser.add_argument('-t', '--text', action='store_true', help='Dumps results as text instead of json.')
    parser.add_argument('-d', '--run-dynamic', action='store_true',
                        help='Adds Dynamic Analysis to the list of service to run.')
    parser.add_argument('-u', '--user', default=user, metavar='"user"',
                        help='username to be used to connect to AL. DEFAULT: user in auth section of ~/.al/submit.cfg')
    parser.add_argument('-p', '--password', default=pw, metavar='"MYPASSWORD"',
                        help='password of the user. DEFAULT: password in auth section of ~/.al/submit.cfg')
    parser.add_argument('-o', '--output-file', metavar='"/home/user/output.txt"',
                        help='File to write the results to. DEFAULT: stdout')
    parser.add_argument('-s', '--server', default=server, metavar='"https://localhost:443"',
                        help='Server to connect to. DEFAULT: transport://host:port in '
                             'server section of ~/.al/submit.cfg')
    parser.add_argument('-c', '--cert', default=cert, metavar='"/path/to/pki.pem"',
                        help='Client cert used to connect to server. DEFAULT: cert in auth section of ~/.al/submit.cfg')
    parser.add_argument('-k', '--apikey', default=apikey, metavar='"MY_RANDOM_API_KEY"',
                        help='apikey to use for the user to login. DEFAULT: apikey in auth section of ~/.al/submit.cfg')
    parser.add_argument('-j', '--json-params', metavar='"{ ... }"', help='A JSON dictionary of submission parameters.')
    parser.add_argument('-m', '--metadata', metavar='"{ ... }"', help='A JSON dictionary of submission metadata.')
    parser.add_argument('--srv-spec', metavar='"{ ... }"', help='A JSON dictionary of service specific parameters.')
    parser.add_argument('--server-crt', metavar='"/path/to/server.crt"',
                        help='DEFAULT: cert in server section of ~/.al/submit.cfg')

    params = parser.parse_args(arguments)

    args = params.files
    verbose = not params.quiet
    async_command = params.async_command
    no_output = params.no_output
    json_output = not params.text
    dynamic = params.run_dynamic
    user = params.user
    cert = params.cert
    pw = params.password
    apikey = params.apikey

    if params.insecure:
        verify = False
    else:
        if params.server_crt:
            verify = params.server_crt

    if not cert and not user:
        sys.stderr.write("This server requires authentication...\n")
        sys.exit(1)

    if user and not pw and not apikey:
        if verbose:
            sys.stderr.write("You specified a username without a password.  What is your password?\n")
        pw = getpass()

    output = params.output_file

    if output:
        f = None
        try:
            f = open(output, "ab")
        except Exception:  # pylint: disable=W0702
            sys.stderr.write("!!ERROR!! Output file cannot be created (%s)\n" % output)
        finally:
            try:
                f.close()
            except Exception:  # pylint: disable=W0702
                pass

    server = params.server

    if not server:
        sys.stderr.write("!!ERROR!! No server specified, -s option is mandatory.\n\n%s" % parser.format_help())
        return -1

    if params.metadata:
        kw['metadata'] = json.loads(params.metadata)

    if params.json_params:
        kw["params"] = json.loads(params.json_params)

    if params.srv_spec:
        kw.setdefault("params", {})
        kw["params"]["service_spec"] = json.loads(params.srv_spec)

    auth = None
    api_auth = None
    if user and apikey:
        api_auth = (user, apikey)
    elif user and pw:
        auth = (user, pw)

    options = {
        'verbose': verbose,
        'json_output': json_output,
    }

    read_from_pipe = False
    if sys.platform.startswith("linux") or sys.platform.startswith("freebsd"):
        try:
            if select.select([sys.stdin, ], [], [], 0.0)[0]:
                read_from_pipe = True
        except io.UnsupportedOperation:
            # stdin has probably been replaced with a non-file python object
            # this is fine.
            pass

    if len(args) == 0 and not read_from_pipe:
        sys.stdout.write("%s\n" % parser.format_help())
        return 0

    try:
        client = get_client(server, apikey=api_auth, auth=auth, cert=cert, verify=verify)
        if isinstance(client, Client4):
            from assemblyline_client.v4_client.common.submit_utils import al_result_to_text
        else:
            from assemblyline_client.v3_client.utils import al_result_to_text
    except ClientError as e:
        if e.status_code == 401:
            sys.stderr.write("!!ERROR!! Authentication to the server failed.\n")
        elif e.status_code == 495:
            sys.stderr.write("!!ERROR!! Invalid SSL connection to the server:\n\t%s\n" % e)
        else:
            raise
        return 1

    if dynamic:
        p = client.user.submission_params("__CURRENT__")
        if "Dynamic Analysis" not in p['services']['selected']:
            p['services']['selected'].append("Dynamic Analysis")

        if 'params' in kw:
            p.update(kw['params'])

        kw['params'] = p

    if async_command and not no_output:
        kw['nq'] = "al_submit_%s" % get_random_id()

    # sanity check path
    if len(args) == 0 and read_from_pipe:
        while True:
            line = sys.stdin.readline()
            if not line:
                break

            line = line.strip()
            if line == '-':
                line = '/dev/stdin'

            if async_command:
                kw.setdefault('metadata', {})
                kw['metadata']['al_submit_id'] = get_id_from_path(line)
                send_async(client, line, verbose=verbose, **kw)
            else:
                send(client, line, output, options, **kw)
    else:
        ret_val = 0
        file_list = []

        for arg in args:
            if arg == '-':
                file_list.append('/dev/stdin')
            elif not exists(arg):
                sys.stderr.write("!!ERROR!! %s => File does not exist.\n" % arg)
                ret_val = 1
            elif isdir(arg):
                for root, _, fname_list in walk(arg):
                    for fname in fname_list:
                        file_list.append(join(root, fname))
            else:
                file_list.append(arg)

        queued_files = [get_id_from_path(f) for f in file_list]
        output_thread = None
        if async_command and not no_output:
            output_thread = start_result_thread(
                client, queued_files, output, options, **kw
            )

        for input_file in file_list:
            if async_command:
                kw.setdefault('metadata', {})
                kw['metadata']['al_submit_id'] = get_id_from_path(input_file)
                if not send_async(client, input_file, verbose=verbose, **kw):
                    with ASYNC_LOCK:
                        queued_files.remove(get_id_from_path(input_file))
                    if verbose:
                        sys.stderr.write("\tWARNING: Could not send file %s.\n" % input_file)
                    ret_val = 1
            else:
                if not send(client, input_file, output, options, **kw):
                    ret_val = 1

        if output_thread:
            output_thread.join()

        if ret_val != 0 and len(file_list) > 1:
            if verbose:
                sys.stderr.write("\n** WARNING: al_submit encountered some "
                                 "errors while processing multiple files. **\n")

        return ret_val


def send_async(client, path, verbose=False, **kw):
    try:
        if verbose:
            sys.stderr.write("Sending file %s for analysis...\n" % path)
        client.ingest(path=path, ingest_type='AL_SUBMIT', **kw)
        return True
    except ClientError:
        return False


def start_result_thread(client, queued_files, output, options, **kw):
    output_thread = Thread(
        target=result_thread,
        args=(client, queued_files, output, options),
        kwargs=kw
    )
    output_thread.start()
    return output_thread


def result_thread(client, queued_files, output, options, **kw):
    nq = kw['nq']
    verbose = options.get('verbose', False)

    while len(queued_files) != 0:
        if verbose:
            sys.stderr.write("Checking message on notification queue: %s\n" % nq)

        msgs = client.ingest.get_message_list(nq)
        for msg in msgs:
            sid = msg.get('submission', {}).get('sid', None) or msg.get('alert', {}).get('sid', None)
            if not sid:
                sys.stderr.write("!!ERROR!! Could not find the sid of the submitted "
                                 "file in the message.\n{}".format(msg))
                continue

            try:
                # v4 structure
                cur_file = msg['submission']['files'][0]['name']
                submission_id = msg['submission']['metadata']['al_submit_id']
            except KeyError:
                # v3 structure
                cur_file = msg.get('metadata', {}).get('filename', None) or msg['sha256']
                submission_id = msg['metadata']['al_submit_id']

            with ASYNC_LOCK:
                try:
                    queued_files.remove(submission_id)
                except ValueError:
                    pass

            if verbose:
                sys.stderr.write("\tFile '%s' complete. Fetching results for submission ID: %s...\n" % (cur_file, sid))

            final_results = client.submission.full(sid)
            if output:
                write_file(final_results, output, cur_file, **options)
            else:
                write_to_sdtout(final_results, **options)

        if len(queued_files) != 0:
            sleep(2)


def write_file(data, path, infile, verbose=False, json_output=True):
    with open(path, "ab") as out_file:
        if json_output:

            out_file.write("[{}] {} <==> {}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                      infile, json.dumps(data, separators=(',', ':'))).encode())
        else:
            out_file.write("[{}] {}\n\n{}\n\n--------\n\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                  infile, result_to_text(data)).encode())
    if verbose:
        sys.stderr.write("%s => Resulting file saved to %s\n" % (infile, path))

    return True


# noinspection PyUnusedLocal
def write_to_sdtout(data, verbose=False, json_output=True):  # pylint: disable=W0613
    try:
        sys.stdout.flush()
        if json_output:
            data = json.dumps(data, separators=(",", ":"))
        else:
            data = result_to_text(data)
        sys.stdout.write(data + "\n")
        sys.stdout.flush()
    except IOError as e:
        if e.errno == EPIPE:
            pass


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
