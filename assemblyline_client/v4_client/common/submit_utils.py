import json
import hashlib
import pprint
import sys

from io import BytesIO
from typing import Union

SRV_BUSY_ID = "20"
SRV_DOWN_ID = "21"
MAX_RETRY_ID = "12"
MAX_DEPTH_ID = "10"
MAX_FILES_ID = "11"

KNOWN_ERRORS = {
    SRV_BUSY_ID: "SERVICE_BUSY",
    SRV_DOWN_ID: "SERVICE_DOWN",
    MAX_RETRY_ID: "MAX_RETRY_REACHED",
    MAX_DEPTH_ID: "MAX_EMBEDDED_DEPTH_REACHED",
    MAX_FILES_ID: "MAX_FILES_REACHED",
}

if sys.version_info >= (3, 0):
    L1 = "\u2591"
    L2 = "\u2592"
    L3 = "\u2593"
    L4 = "\u2588"
    LD = "\u02e7"
    RD = "\ua714"
else:
    L1 = u"\u2591".encode("utf-8")
    L2 = u"\u2592".encode("utf-8")
    L3 = u"\u2593".encode("utf-8")
    L4 = u"\u2588".encode("utf-8")
    LD = u"\u02e7".encode("utf-8")
    RD = u"\ua714".encode("utf-8")


def get_file_handler(content: Union[str, bytes], fname=None) -> BytesIO:
    if isinstance(content, str):
        content = content.encode()
    fh = BytesIO(content)
    fh.name = fname or hashlib.sha256(content).hexdigest()
    return fh


def al_result_to_text(r, show_errors=True, verbose_error=False):
    lines = ["", ":: Submission Detail %s::" % {True: "", False: "[Errors hidden]"}[show_errors],
             "\t%-36s %s" % ("state:", r["state"]), ""]
    for key in sorted(r['params'].keys()):
        if key == 'service_spec':
            continue

        if key == 'services':
            lines.append("\t%-36s %s" % (key + ":", " | ".join(r['params']['services']['selected'])))
        elif isinstance(r['params'][key], list):
            lines.append("\t%-36s %s" % (key + ":", " | ".join(r['params'][key])))
        else:
            lines.append("\t%-36s %s" % (key + ":", r['params'][key]))
    lines.append("")
    lines.append("\t:: Timing info ::")
    for key in sorted(r['times'].keys()):
        if r['times'][key] is not None:
            lines.append("\t\t%-12s %s (UTC)" % (key + ":", r['times'][key].replace("T", " ").replace("Z", "")))
    if r["expiry_ts"]:
        lines.append("\t\t%-12s %s (UTC)" % ("expiry:", r["expiry_ts"].replace("T", " ").replace("Z", "")))

    if len(r['metadata']) > 0:
        lines.append("")
        lines.append("\t:: Metadata ::")
        for key in sorted(r['metadata'].keys()):
            lines.append("\t\t%-36s %s" % (key + ":", r['metadata'][key]))

    lines.append("")
    lines.append("\t:: Services specific info ::")
    if len(r['params']['service_spec'].keys()) != 0:
        for key in sorted(r['params']['service_spec'].keys()):
            if isinstance(r['params']['service_spec'][key], list):
                lines.append("\t\t%-12s %s" % (key + ":", " | ".join(r['params']['service_spec'][key])))
            else:
                lines.append("\t\t%-12s %s" % (key + ":", r['params']['service_spec'][key]))
    else:
        lines.append("\t\tNone")

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
    for f in r['files']:
        lines.append("\t%s [%s] -> %s bytes" % (f['name'], f['sha256'], f['size']))

    if show_errors and len(r['errors']) > 0:
        lines.append("")
        lines.append(":: ERRORS ::")
        for key in r['errors'].keys():
            sha256 = key[:64]
            service = key[65:].split(".", 1)[0]
            eid = key.rsplit(".e", 1)[1]
            if eid in KNOWN_ERRORS:
                lines.append("\tService %s failed for file %s [%s]" % (service, sha256, KNOWN_ERRORS[eid]))
            else:
                lines.append(
                    "\tService %s failed for file %s [%s]" % (service, sha256, r['errors'][key]["response"]['status']))
                if verbose_error and r['errors'][key]["response"]["message"] != "":
                    err_lines = r['errors'][key]["response"]["message"].split("\n")
                    for line in err_lines:
                        lines.append("\t\t%s" % line)

    lines.append("")
    lines.append(":: Service results ::")
    res_key_list = sorted(r['results'].keys())
    for f in r['files']:
        for key in res_key_list:
            if key.startswith(f['sha256']):
                lines.extend(process_res(r['results'][key], f['sha256']))
                del r['results'][key]

    for key in sorted(r['results'].keys()):
        lines.extend(process_res(r['results'][key], key[:64]))

    return lines


def process_res(res, sha256):
    out = [""]
    out.extend(get_service_info(res, sha256))
    for section in res['result']['sections']:
        out.extend(show_section(section))

    if res['response']['extracted']:
        out.append('')
        out.append("\t\t:: Extracted files ::")
        for extracted_file in res['response']['extracted']:
            out.append("\t\t\t{} [{}] :: {}".format(extracted_file['name'], extracted_file['sha256'],
                                                    extracted_file['description']))

    if res['response']['supplementary']:
        out.append('')
        out.append("\t\t:: Supplementary files ::")
        for supplementary in res['response']['supplementary']:
            out.append("\t\t\t{} [{}] :: {}".format(supplementary['name'], supplementary['sha256'],
                                                    supplementary['description']))

    return out


def get_service_info(srv_res, fhash):
    classification = "{} :: ".format(srv_res['classification']) if srv_res['classification'] else ""
    out = ["\t{}{} [{}] - {} ({})".format(classification, srv_res['response']['service_name'],
                                          srv_res['result']['score'], srv_res['response']['service_version'], fhash)]
    return out


def show_section(section):
    out = [""]

    depth = '\t' * (section['depth'] + 1)
    classification = "{} :: ".format(section['classification']) if section['classification'] else ""
    title = section['title_text'].replace('\n', '')

    if section['heuristic'] is not None:
        score = section['heuristic']['score']
        out.append("\t{}{}[{}] {}".format(depth, classification, score, title))

    else:
        out.append("\t{}{}{}".format(depth, classification, title))

    if section['body']:
        if section['body_format'] in ["TEXT", "MEMORY_DUMP"]:
            out.extend(["\t\t{}{}".format(depth, x) for x in section['body'].splitlines()])
        elif section['body_format'] == 'GRAPH_DATA':
            try:
                body = json.loads(section['body'])
            except TypeError:
                body = section['body']
            dom_min, dom_max = body['data']['domain']
            values = body['data']['values']
            step = (dom_max - dom_min) / 5.0
            cmap = []

            for v in values:
                if v < dom_min + step:
                    cmap.append(" ")
                elif v < dom_min + (step * 2):
                    cmap.append(L1)
                elif v < dom_min + (step * 3):
                    cmap.append(L2)
                elif v < dom_min + (step * 4):
                    cmap.append(L3)
                else:
                    cmap.append(L4)

            out.append("\t\t{} [ ]: {} .. {}        [{}]: {} .. {}".format(depth, dom_min*1.0, dom_min + step*1.0, L4,
                                                                           dom_max-step*1.0, dom_max*1.0))
            out.append("\t\t{}{}{}{}".format(depth, LD, ''.join(cmap), RD))
        elif section['body_format'] == 'URL':
            try:
                body = json.loads(section['body'])
            except TypeError:
                body = section['body']
            if not isinstance(body, list):
                body = [body]
            for url in body:
                if 'name' in url:
                    out.append("\t\t{}{}: {}".format(depth, url['name'], url['url']))
                else:
                    out.append("\t\t{}{}".format(depth, url['url']))
        elif section['body_format'] == 'JSON':
            try:
                body = pprint.pformat(json.loads(section['body']))
            except TypeError:
                body = pprint.pformat(section['body'])
            out.extend(["\t\t{}{}".format(depth, x) for x in body.splitlines()])
        elif section['body_format'] == 'KEY_VALUE':
            try:
                body = json.loads(section['body'])
            except TypeError:
                body = section['body']
            out.extend(["\t\t{}{}: {}".format(depth, k, v) for k, v in body.items()])
        else:
            out.append("Unknown section type: {}".format(section['body_format']))

    heuristic = section.get('heuristic')
    spacer = True
    if heuristic:
        spacer = False
        out.append('')
        out.append("\t\t\t{}[HEURISTIC] {}".format(depth, heuristic['name']))
        for signature in heuristic.get('signature', []):
            out.append("\t\t\t{}[SIGNATURE] {} ({}x)".format(depth, signature['name'], signature['frequency']))
        for attack in heuristic.get('attack', []):
            out.append("\t\t\t{}[ATTACK] {} ({})".format(depth, attack['pattern'], attack['attack_id']))

    if section['tags']:
        if spacer:
            out.append('')
        for tag in section['tags']:
            out.append("\t\t\t{}[{}] {}".format(depth, tag['short_type'].upper(), tag['value']))

    return out
