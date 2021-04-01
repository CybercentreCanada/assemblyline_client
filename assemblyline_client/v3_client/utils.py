import json
import pprint
import sys

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


def al_result_to_text(r, show_errors=True, verbose_error=False):
    lines = ["", ":: Submission Detail %s::" % {True: "", False: "[Errors hidden]"}[show_errors],
             "\t%-36s %s" % ("state:", r["state"]), "\t%-36s %s" % ("classification:", r["classification"]), ""]
    for key in sorted(r['submission'].keys()):
        if key == 'metadata':
            continue
        if isinstance(r['submission'][key], list):
            lines.append("\t%-36s %s" % (key + ":", " | ".join(r['submission'][key])))
        else:
            lines.append("\t%-36s %s" % (key + ":", r['submission'][key]))
    lines.append("")

    lines.append("\t:: Timing info ::")
    for key in sorted(r['times'].keys()):
        lines.append("\t\t%-12s %s (UTC)" % (key + ":", r['times'][key].replace("T", " ").replace("Z", "")))
    lines.append("\t\t%-12s %s (UTC)" % ("expiry:", r["__expiry_ts__"].replace("T", " ").replace("Z", "")))
    lines.append("")

    if len(r['submission']['metadata']) > 0:
        lines.append("\t:: Metadata ::")
        for key in sorted(r['submission']['metadata'].keys()):
            lines.append("\t\t%-36s %s" % (key + ":", r['submission']['metadata'][key]))
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
                    for line in err_lines:
                        lines.append("\t\t%s" % line)

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
            if section['body_format'] in ["TEXT", "MEMORY_DUMP"]:
                out.extend(["\t\t{}{}".format("\t" * depth, x) for x in section['body'].splitlines()])
            elif section['body_format'] == 'GRAPH_DATA':
                body = json.loads(section['body'])
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

                out.append(
                    "\t\t{} [ ]: {} .. {}        [{}]: {} .. {}".format("\t" * depth, dom_min * 1.0,
                                                                        dom_min + step * 1.0, L4,
                                                                        dom_max - step * 1.0,
                                                                        dom_max * 1.0))
                out.append("\t\t{}{}{}{}".format("\t" * depth, LD, ''.join(cmap), RD))
            elif section['body_format'] == 'URL':
                body = json.loads(section['body'])
                if not isinstance(body, list):
                    body = [body]
                for url in body:
                    if 'name' in url:
                        out.append("\t\t{}{}: {}".format("\t" * depth, url['name'], url['url']))
                    else:
                        out.append("\t\t{}{}".format("\t" * depth, url['url']))
            elif section['body_format'] == 'JSON':
                body = pprint.pformat(section['body'])
                out.extend(["\t\t{}{}".format("\t" * depth, x) for x in body.splitlines()])
            else:
                out.append("Unknown section type: {}".format(section['body_format']))

        if section['subsections']:
            out.extend(recurse_sections(section['subsections'], depth + 1))

        first = False

    return out
