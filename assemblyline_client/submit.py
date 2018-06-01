#!/usr/bin/env python

# noinspection PyProtectedMember
from assemblyline_client import Client, ClientError, __build__

import datetime
import sys
import select
import uuid
import json
import io

from copy import deepcopy
from errno import EPIPE
from getpass import getpass
from os.path import exists, isdir, basename, join, expanduser
from os import walk
from signal import signal, SIGINT, SIG_DFL
from threading import Thread, Lock
from time import sleep

if sys.version_info[0] == 3:
    # noinspection PyUnresolvedReferences
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

ASYNC_LOCK = Lock()

__version__ = "al_submit v%s.%s.%s" % (__build__[0], __build__[1], __build__[2])


SRV_DOWN_HASH = "eb54dc2e040a925f84e55e91ff27601ad"
MAX_RETRY_HASH = "ec502020e499f01f230e06a58ad9b5dcc"
MAX_DEPTH_HASH = "e56d398ad9e9c4de4dd0ea8897073d430"
MAX_FILES_HASH = "e6e34a5b7aa6fbfb6b1ac0d35f2c44d70"

KNOWN_ERRORS = {
    SRV_DOWN_HASH: "SERVICE_DOWN",
    MAX_RETRY_HASH: "MAX_RETRY_REACHED",
    MAX_DEPTH_HASH: "MAX_EMBEDDED_DEPTH_REACHED",
    MAX_FILES_HASH: "MAX_FILES_REACHED",
}


def al_result_to_text(r, show_errors=True, verbose_error=False):
    lines = ["", ":: Submission Detail %s::" % {True: "", False: "[Errors hidden]"}[show_errors],
             "\t%-20s %s" % ("state:", r["state"]), ""]
    for key in sorted(r['submission'].keys()):
        if isinstance(r['submission'][key], list):
            lines.append("\t%-20s %s" % (key + ":", " | ".join(r['submission'][key])))
        else:
            lines.append("\t%-20s %s" % (key + ":", r['submission'][key]))
    lines.append("")
    lines.append("\t:: Timing info ::")
    for key in sorted(r['times'].keys()):
        lines.append("\t\t%-12s %s" % (key + ":", r['times'][key].replace("T", " ").replace("Z", "")))
    lines.append("\t\t%-12s %s" % ("expiry:", r["__expiry_ts__"].replace("T", " ").replace("Z", "")))
    lines.append("")
    lines.append("\t:: Services info ::")
    for key in sorted(r['services'].keys()):
        if isinstance(r['services'][key], list):
            lines.append("\t\t%-12s %s" % (key + ":", " | ".join(r['services'][key])))
        else:
            lines.append("\t\t%-12s %s" % (key + ":", r['services'][key]))

    lines.append("")
    lines.append("\t:: Missing results/errors ::")
    if len(r['missing_result_keys']) == 0 and len(r['missing_error_keys']) == 0:
        lines.append("\t\tNone")
    else:
        for i in r['missing_result_keys']:
            lines.append("\t\t%s [RESULT]" % i)
        for i in r['missing_error_keys']:
            lines.append("\t\t%s [ERROR]" % i)

    lines.append("")
    lines.append(":: Submitted files ::")
    for name, sha256 in r['files']:
        lines.append("\t%s [%s]" % (name, sha256))

    if show_errors and len(r['errors']) > 0:
        lines.append("")
        lines.append(":: ERRORS ::")
        for key in r['errors'].keys():
            sha256 = key[:64]
            service = key[65:].split(".", 1)[0]
            ehash = key[-33:]
            if ehash in KNOWN_ERRORS:
                lines.append("\tService %s failed for file %s [%s]" % (service, sha256, KNOWN_ERRORS[ehash]))
            else:
                lines.append(
                    "\tService %s failed for file %s [%s]" % (service, sha256, r['errors'][key]["response"]['status']))
                if verbose_error and r['errors'][key]["response"]["message"] != "":
                    err_lines = r['errors'][key]["response"]["message"].split("\n")
                    for l in err_lines:
                        lines.append("\t\t%s" % l)

    lines.append("")
    lines.append(":: Service results ::")
    res_key_list = sorted(r['results'].keys())
    for _, sha256 in r['files']:
        for key in res_key_list:
            if key.startswith(sha256):
                lines.extend(process_res(r['results'][key], sha256))
                del r['results'][key]

    for key in sorted(r['results'].keys()):
        lines.extend(process_res(r['results'][key], key[:64]))

    return lines


def process_res(res, sha256):
    out = [""]
    out.extend(get_service_info(res, sha256))
    out.extend(recurse_sections(res['result']['sections']))

    if res['result']['tags']:
        out.append('')
        out.append("\t\t:: Generated Tags ::")
        for tag in res['result']['tags']:
            out.append("\t\t\t%s [%s]" % (tag['value'], tag['type']))

    if res['response']['extracted']:
        out.append('')
        out.append("\t\t:: Extracted files ::")
        for name, fhash, _ in res['response']['extracted']:
            out.append("\t\t\t%s [%s]" % (name, fhash))

    return out


def get_service_info(srv_res, fhash):
    out = ["\t:: %s [%s] - %s (%s) ::" % (
        srv_res['response']['service_name'], srv_res['result']['score'], srv_res['response']['service_version'], fhash)]
    return out


def recurse_sections(sections, depth=1):
    out = []
    first = True
    for section in sections:
        if not first:
            out.append("")
        out.append("\t%s[%s] %s" % ("\t" * depth, section['score'], section['title_text'].replace("\n", "")))

        if section['body']:
            out.extend(["\t\t%s%s" % ("\t" * depth, x) for x in section['body'].splitlines()])

        if section['subsections']:
            out.extend(recurse_sections(section['subsections'], depth + 1))

        first = False

    return out


def result_to_text(data):
    return "\n".join(al_result_to_text(data))


def get_details_from_key(key):
    file_hash = key[:64]
    key = key[65:]
    name = key[:key.index(".")]

    return file_hash, name


# send(client, input_file, output, verbose=verbose, **kw)
def send(client, path, output, options=None, **kw):
    if options is None:
        options = {}
    name = basename(path)
    verbose = options.get('verbose', False)

    try:
        submission = client.submit(path, **kw)
        sid = submission['submission']['sid']

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
                        if verbose:
                            sys.stderr.write("\tAll messages received, fetching results...\n")

                        final_results = client.submission.full(sid)
                        if output:
                            write_file(final_results, output, name, **options)
                        else:
                            write_to_sdtout(final_results, **options)

                        if verbose:
                            sys.stderr.write("Missing result keys: %s\n" % str(final_results["missing_result_keys"]))

                        done = True
                        break
                    else:
                        wq_id = client.live.setup_watch_queue(sid)['wq_id']
                        if verbose:
                            sys.stderr.write("\tSubmission hasn't started on the server yet (new WQ_ID: %s)\n" % wq_id)

                elif m['type'] == "stop":
                    if verbose:
                        sys.stderr.write("\tAll messages received, fetching results...\n")

                    final_results = client.submission.full(sid)
                    if output:
                        write_file(final_results, output, name, **options)
                    else:
                        write_to_sdtout(final_results, **options)

                    if verbose:
                        sys.stderr.write("Missing result keys: %s\n" % str(final_results["missing_result_keys"]))

                    done = True
                    break
                elif m["type"] == "cachekey" or m["type"] == "cachekeyerr":
                    file_hash, srv_name = get_details_from_key(m["msg"])
                    if verbose:
                        sys.stderr.write("\t\t[x] %s (%s) - %s\n" % (
                            srv_name, file_hash, {
                                True: "ERROR",
                                False: "SUCCESS"
                            }[m["type"] == "cachekeyerr"])
                                         )
                else:
                    if verbose:
                        sys.stdout.write("%s\n", str(m))

            if not done:
                sleep(2)

    except ClientError as e:
        if e.status_code == 401:
            sys.stderr.write("!!ERROR!! Authentication to the server failed.\n")
        elif e.status_code == 403:
            data = json.loads(e.message)
            sys.stderr.write("!!ERROR!! %s\n" % data['api_error_message'])
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
    parser.add_argument('-s', '--server', default=server, metavar='"http://my.al.server"',
                        help='Server to connect to. DEFAULT: transport://host:port in '
                             'server section of ~/.al/submit.cfg')
    parser.add_argument('-c', '--cert', default=cert, metavar='"/path/to/pki.pem"',
                        help='Client cert used to connect to server. DEFAULT: cert in auth section of ~/.al/submit.cfg')
    parser.add_argument('-k', '--apikey', default=apikey, metavar='"MY_RANDOM_API_KEY"',
                        help='apikey to use for the user to login. DEFAULT: apikey in auth section of ~/.al/submit.cfg')
    parser.add_argument('-j', '--json-params', metavar='"{ ... }"', help='A JSON dictionary of submission parameters.')
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
        sys.stderr.write("!!ERROR!! No server specified, -s option is mandatory.\n\n" % parser.format_help())
        return -1

    if params.json_params:
        kw["params"] = json.loads(params.json_params)

    if params.srv_spec:
        kw["srv_spec"] = json.loads(params.srv_spec)

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
        client = Client(server, apikey=api_auth, auth=auth, cert=cert, verify=verify)
    except ClientError as e:
        if e.status_code == 401:
            sys.stderr.write("!!ERROR!! Authentication to the server failed.\n")
        elif e.status_code == 495:
            sys.stderr.write("!!ERROR!! Invalid SSL connection to the server:\n\t%s\n" % e.message)
        else:
            raise
        return 1

    if dynamic:
        p = client.user.submission_params("__CURRENT__")
        if "Dynamic Analysis" not in p['selected']:
            p['selected'].append("Dynamic Analysis")

        if 'params' in kw:
            p.update(kw['params'])

        kw['params'] = p
    if async_command and not no_output:
        kw['nq'] = uuid.uuid4().get_hex()

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

        queued_files = deepcopy(file_list)
        output_thread = None
        if async_command and not no_output:
            output_thread = start_result_thread(
                client, queued_files, output, options, **kw
            )

        for input_file in file_list:
            if async_command:
                if not send_async(client, input_file, verbose=verbose, **kw):
                    with ASYNC_LOCK:
                        queued_files.remove(input_file)
                    if verbose:
                        sys.stderr.write("\n\tWARNING: Could not send file %s.\n" % input_file)
                    ret_val = 1
            else:
                if not send(client, input_file, output, options, **kw):
                    ret_val = 1

        if output_thread:
            output_thread.join()

        if ret_val != 0 and len(file_list) > 1:
            if verbose:
                sys.stderr.write("\n\tWARNING: al_submit encountered some errors while processing multiple files.\n")

        return ret_val


def send_async(client, path, verbose=False, **kw):
    try:
        if verbose:
            sys.stderr.write("\nSending file %s for analysis...\n" % path)
        client.ingest(path, ingest_type='AL_SUBMIT', **kw)
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
            sid = msg['alert']['sid']
            cur_file = msg['metadata']['filename']
            with ASYNC_LOCK:
                try:
                    queued_files.remove(cur_file)
                except ValueError:
                    pass

            if verbose:
                sys.stderr.write("\tFile %s complete. Fetching results for %s...\n" % (cur_file, sid))

            final_results = client.submission.full(sid)
            if output:
                write_file(final_results, output, cur_file, **options)
            else:
                write_to_sdtout(final_results, **options)

            if verbose:
                sys.stderr.write("Missing result keys: %s\n" % str(final_results["missing_result_keys"]))

        if len(queued_files) != 0:
            sleep(2)


def write_file(data, path, infile, verbose=False, json_output=True):
    with open(path, "ab") as out_file:
        if json_output:
            out_file.write("[%s] %s <==> %s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), infile,
                                                  json.dumps(data, separators=(",", ":"))))
        else:
            out_file.write("[%s] %s\n\n%s\n\n--------\n\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                              infile, result_to_text(data)))
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
