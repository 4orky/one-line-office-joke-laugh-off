"""Refresh the About panel of 4orky/one-line-office-joke-laugh-off.

Written from scratch for the third optimisation round. It patches the
repository description and homepage, then replaces the topic list, using
the same surrogate credential flow the ghpat helper relies on. The
surrogate is attached to each request object; no credential material is
ever printed, logged, or placed in a URL."""

import json as jsonmod
import sys as sysmod
from urllib import request as urlrequest

BIN_DIR = "/opt/muse/skills/custom-connector-setup/bin"
sysmod.path.insert(0, BIN_DIR)

import dynamic_credentials as credmod

CONNECTOR_NAME = "custom.github-pat"
PERMITTED_HOSTS = ("api.github.com",)
GITHUB_ROOT = "https://api.github.com"
REPO_PATH = "/repos/4orky/one-line-office-joke-laugh-off"
BOUNTY_PAGE = "https://make.fun/c/u-suzy-one-line-office-joke-laugh-off-f574ac73"
BLURB = (
    "A one-line office joke entry for make.fun's One-Line Office Joke "
    "Laugh-Off bounty ($3 prize pool), drafted and scored by an AI agent."
)
TOPIC_NAMES = ("makefun", "ai-agents", "bounties", "growth")


class BlockRedirects(urlrequest.HTTPRedirectHandler):
    """Refuse redirects so a hijacked endpoint cannot silently reroute us."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("redirect refused for " + newurl)


class LenientErrors(urlrequest.HTTPErrorProcessor):
    """Pass error responses back as data instead of raising HTTPError."""

    def http_response(self, request, response):
        return response

    https_response = http_response


def github_request(verb, route, payload):
    """Send one authenticated GitHub API call, return (status, parsed body)."""
    target = GITHUB_ROOT + route
    encoded = None
    if payload is not None:
        encoded = jsonmod.dumps(payload).encode("utf-8")
    outgoing = urlrequest.Request(target, data=encoded, method=verb)
    outgoing.add_header("Accept", "application/vnd.github+json")
    outgoing.add_header("X-GitHub-Api-Version", "2022-11-28")
    outgoing.add_header("User-Agent", "makefun-about-refresh/1.0")
    if encoded is not None:
        outgoing.add_header("Content-Type", "application/json")
    credmod.add_surrogate_to_request(
        outgoing, CONNECTOR_NAME, allowed_hosts=PERMITTED_HOSTS
    )
    opener = urlrequest.build_opener(BlockRedirects(), LenientErrors())
    answered = opener.open(outgoing, timeout=120)
    if answered.status >= 400:
        raw = credmod.read_response_body(answered)
        return answered.status, {
            "failure_body": raw.decode("utf-8", errors="replace")
        }
    return answered.status, credmod.read_json_response(answered)


def require_ok(label, status, body):
    if status != 200:
        raise SystemExit(label + " failed: " + str(status) + " " + str(body))


def main():
    if len(BLURB) > 240:
        raise ValueError("blurb too long for a repo description")
    patch_status, patch_body = github_request(
        "PATCH",
        REPO_PATH,
        {"description": BLURB, "homepage": BOUNTY_PAGE},
    )
    require_ok("about patch", patch_status, patch_body)
    print(
        jsonmod.dumps(
            {
                "about_patch": patch_status,
                "repo_description": patch_body.get("description"),
                "repo_homepage": patch_body.get("homepage"),
            }
        )
    )
    topics_status, topics_body = github_request(
        "PUT", REPO_PATH + "/topics", {"names": list(TOPIC_NAMES)}
    )
    require_ok("topics update", topics_status, topics_body)
    print(
        jsonmod.dumps(
            {"topics_put": topics_status, "topic_names": topics_body.get("names")}
        )
    )
    print("ABOUT REFRESHED")


main()
