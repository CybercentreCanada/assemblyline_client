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
    LD = "\u2524"
    RD = "\u251C"
else:
    L1 = u"\u2591".encode("utf-8")
    L2 = u"\u2592".encode("utf-8")
    L3 = u"\u2593".encode("utf-8")
    L4 = u"\u2588".encode("utf-8")
    LD = u"\u2524".encode("utf-8")
    RD = u"\u251C".encode("utf-8")


def get_file_handler(content: Union[str, bytes], fname=None) -> BytesIO:
    if isinstance(content, str):
        content = content.encode()
    fh = BytesIO(content)
    fh.name = fname or hashlib.sha256(content).hexdigest()
    return fh


def al_result_to_text(r, show_errors=True, verbose_error=False):
    lines = ["", ":: Submission Detail %s::" % {True: "", False: "[Errors hidden]"}[show_errors],
             "  %-36s %s" % ("state:", r["state"]), ""]
    for key in sorted(r['params'].keys()):
        if key == 'service_spec':
            continue

        if key == 'services':
            lines.append("  %-36s %s" % (key + ":", " | ".join(r['params']['services']['selected'])))
        elif isinstance(r['params'][key], list):
            lines.append("  %-36s %s" % (key + ":", " | ".join(r['params'][key])))
        else:
            lines.append("  %-36s %s" % (key + ":", r['params'][key]))
    lines.append("")
    lines.append("  :: Timing info ::")
    for key in sorted(r['times'].keys()):
        if r['times'][key] is not None:
            lines.append("    %-12s %s (UTC)" % (key + ":", r['times'][key].replace("T", " ").replace("Z", "")))
    if r["expiry_ts"]:
        lines.append("    %-12s %s (UTC)" % ("expiry:", r["expiry_ts"].replace("T", " ").replace("Z", "")))

    if len(r['metadata']) > 0:
        lines.append("")
        lines.append("  :: Metadata ::")
        for key in sorted(r['metadata'].keys()):
            lines.append("    %-36s %s" % (key + ":", r['metadata'][key]))

    lines.append("")
    lines.append("  :: Services specific info ::")
    if len(r['params']['service_spec'].keys()) != 0:
        for key in sorted(r['params']['service_spec'].keys()):
            if isinstance(r['params']['service_spec'][key], list):
                lines.append("    %-12s %s" % (key + ":", " | ".join(r['params']['service_spec'][key])))
            else:
                lines.append("    %-12s %s" % (key + ":", r['params']['service_spec'][key]))
    else:
        lines.append("    None")

    lines.append("")
    lines.append("  :: Missing results/errors ::")
    if len(r['missing_result_keys']) == 0 and len(r['missing_error_keys']) == 0:
        lines.append("    None")
    else:
        for i in r['missing_result_keys']:
            lines.append("    %s [RESULT]" % i)
        for i in r['missing_error_keys']:
            lines.append("    %s [ERROR]" % i)

    lines.append("")
    lines.append(":: Submitted files ::")
    for f in r['files']:
        lines.append("  %s [%s] -> %s bytes" % (f['name'], f['sha256'], f['size']))

    if show_errors and len(r['errors']) > 0:
        lines.append("")
        lines.append(":: ERRORS ::")
        for key in r['errors'].keys():
            sha256 = key[:64]
            service = key[65:].split(".", 1)[0]
            eid = key.rsplit(".e", 1)[1]
            if eid in KNOWN_ERRORS:
                lines.append("  Service %s failed for file %s [%s]" % (service, sha256, KNOWN_ERRORS[eid]))
            else:
                lines.append(
                    "  Service %s failed for file %s [%s]" % (service, sha256, r['errors'][key]["response"]['status']))
                if verbose_error and r['errors'][key]["response"]["message"] != "":
                    err_lines = r['errors'][key]["response"]["message"].split("\n")
                    for line in err_lines:
                        lines.append("    %s" % line)

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
        out.append("    :: Extracted files ::")
        for extracted_file in res['response']['extracted']:
            out.append("      {} [{}] :: {}".format(extracted_file['name'], extracted_file['sha256'],
                                                    extracted_file['description']))

    if res['response']['supplementary']:
        out.append('')
        out.append("    :: Supplementary files ::")
        for supplementary in res['response']['supplementary']:
            if supplementary['is_section_image']:
                continue

            out.append("      {} [{}] :: {}".format(supplementary['name'], supplementary['sha256'],
                                                    supplementary['description']))

    return out


def get_service_info(srv_res, fhash):
    classification = "{} :: ".format(srv_res['classification']) if srv_res['classification'] else ""
    out = ["  {}{} [{}] - {} ({})".format(classification, srv_res['response']['service_name'],
                                          srv_res['result']['score'], srv_res['response']['service_version'], fhash)]
    return out


def recurse_process(out, depth, data):
    for process in data:
        out.append(
            "    {}[{}] {} ({}) {{F:{} N:{} R:{} S:[{}]}}".format(
                depth, process['process_pid'],
                process['process_name'],
                process['command_line'],
                process.get('file_count', 0),
                process.get('network_count', 0),
                process.get('registry_count', 0),
                "|".join(process.get('signatures', {}).keys())))
        recurse_process(out, depth + '  ', process.get('children', []))


def process_section(out, depth, body_format, body):
    if body_format in ["TEXT", "MEMORY_DUMP"]:
        out.extend(["    {}{}".format(depth, x) for x in body.splitlines()])

    elif body_format == 'GRAPH_DATA':
        try:
            body = json.loads(body)
        except TypeError:
            pass
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

        out.append("    {} [ ]: {} .. {}        [{}]: {} .. {}".format(depth, dom_min*1.0, dom_min + step*1.0, L4,
                                                                       dom_max-step*1.0, dom_max*1.0))
        out.append("    {}{}{}{}".format(depth, LD, ''.join(cmap), RD))

    elif body_format == 'URL':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        if not isinstance(body, list):
            body = [body]
        for url in body:
            if 'name' in url:
                out.append("    {}{}: {}".format(depth, url['name'], url['url']))
            else:
                out.append("    {}{}".format(depth, url['url']))

    elif body_format == 'JSON':
        try:
            body = pprint.pformat(json.loads(body))
        except TypeError:
            body = pprint.pformat(body)
        out.extend(["    {}{}".format(depth, x) for x in body.splitlines()])

    elif body_format == 'KEY_VALUE':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        out.extend(["    {}{}: {}".format(depth, k, v) for k, v in body.items()])

    elif body_format == 'ORDERED_KEY_VALUE':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        out.extend(["    {}{}: {}".format(depth, k, v) for (k, v) in body])

    elif body_format == 'PROCESS_TREE':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        recurse_process(out, depth, body)

    elif body_format == 'TABLE':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        cols = {k for line in body for k in line.keys()}
        out.append("    {}{}".format(depth, " | ".join(["%-50s" % col for col in cols])))
        out.extend(["    {}{}".format(depth, " | ".join(["%-50s" % line.get(col, "") for col in cols]))
                    for line in body])

    elif body_format == 'IMAGE':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        out.extend(
            ["    {}{}: {} ({})".format(
                depth, img['img']['name'],
                img['img']['description'],
                img['img']['sha256'],) for img in body])

    elif body_format == 'TIMELINE':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        for item in body:
            out.append("    {}{}   |".format(depth, "%50s" % " "))
            out.append("    {}{}   o   {}".format(depth, "%50s" % item.get('opposite_content', ''),
                                                  "%-50s" % "{} ({})".format(item.get('title', ''),
                                                                             item.get('content', ''))))
            out.append("    {}{}   |".format(depth, "%50s" % " "))

    elif body_format == 'MULTI':
        try:
            body = json.loads(body)
        except TypeError:
            pass
        for subsection_type, subsection, _ in body:
            process_section(out, depth, subsection_type, subsection)

    elif body_format == 'DIVIDER':
        out.append("    {}{}".format(depth, "-" * 50))

    else:
        out.append("      ERR: Unknown section type: {}".format(body_format))


def show_section(section):
    out = [""]

    depth = '  ' * (section['depth'] + 1)
    classification = "{} :: ".format(section['classification']) if section['classification'] else ""
    title = section['title_text'].replace('\n', '')

    if section['heuristic'] is not None:
        score = section['heuristic']['score']
        out.append("  {}{}[{}] {}".format(depth, classification, score, title))

    else:
        out.append("  {}{}{}".format(depth, classification, title))

    if section['body']:
        process_section(out, depth, section['body_format'], section['body'])

    heuristic = section.get('heuristic')
    spacer = True
    if heuristic:
        spacer = False
        out.append('')
        out.append("      {}[HEURISTIC] {}".format(depth, heuristic['name']))
        for signature in heuristic.get('signature', []):
            out.append("      {}[SIGNATURE] {} ({}x)".format(depth, signature['name'], signature['frequency']))
        for attack in heuristic.get('attack', []):
            out.append("      {}[ATTACK] {} ({})".format(depth, attack['pattern'], attack['attack_id']))

    if section['tags']:
        if spacer:
            out.append('')
        for tag in section['tags']:
            out.append("      {}[{}] {}".format(depth, tag['short_type'].upper(), tag['value']))

    return out
