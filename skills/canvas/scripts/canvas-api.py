#!/usr/bin/env python3
"""
canvas-api.py — opt-in Canvas API access for the back-to-school skills.

Stdlib only. Everything stays on this machine:
  ~/.claude/canvas/credentials.json   (0600, your token)
  ~/.claude/canvas/snapshot.json      (your coursework)

Commands:
  setup    save your Canvas URL + access token (requires accepting the risks)
  test     verify the token works
  pull     fetch courses, grades, and assignments -> snapshot.json
  status   show what's configured (never prints the token)
  revoke   delete the local token

Run `setup` before anything else.
"""

import argparse
import getpass
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DIR = os.path.expanduser("~/.claude/canvas")
CREDS = os.path.join(DIR, "credentials.json")
SNAPSHOT = os.path.join(DIR, "snapshot.json")

RISKS = """
CANVAS API ACCESS — READ THIS BEFORE CONTINUING

You are about to store a Canvas access token on this computer. What that means:

  1. The token acts as YOU. Anyone who reads the file can act as you in Canvas
     until the token is deleted. It is saved to
     ~/.claude/canvas/credentials.json with 0600 permissions (only your user
     can read it) but it is NOT encrypted.

  2. Never commit it, paste it in chat, or put it in a repo. This toolkit's
     .gitignore already excludes it, but that only helps inside this repo.

  3. Many schools prohibit or restrict API tokens in their acceptable-use
     policy. Some disable them entirely. Check yours. Getting this wrong is
     on you, not on this tool.

  4. This script only ever sends GET requests. It cannot submit, delete, or
     change anything in Canvas. But the token itself is not read-only —
     something else with that token could.

  5. Delete the token when you're done: `canvas-api.py revoke` removes the
     local copy, and you should ALSO delete it in Canvas at
     Account -> Settings -> Approved Integrations.

  6. Set an expiry date when you create the token. End of semester is a good
     one. This is the single best thing you can do to limit the damage.

To get a token: Canvas -> Account -> Settings -> "+ New Access Token".
Give it a purpose and an expiry date. Copy it — Canvas shows it once.

The browser-based /canvas skill needs none of this. Use that unless you have
a reason to be here.
"""


# ---------- storage ----------

def load_creds():
    if not os.path.exists(CREDS):
        die("Not set up. Run: canvas-api.py setup")
    with open(CREDS) as f:
        return json.load(f)


def save_creds(data):
    os.makedirs(DIR, mode=0o700, exist_ok=True)
    fd = os.open(CREDS, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(CREDS, 0o600)


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def normalize_url(url):
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    if not url.startswith("https://"):
        die("Canvas URL must be https")
    # strip any path a student pasted along with the domain
    p = urllib.parse.urlparse(url)
    return f"https://{p.netloc}"


# ---------- http ----------

def get(url, token, params=None):
    """GET one page. Returns (json, next_url)."""
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode("utf-8"))
            return body, next_link(r.headers.get("Link", ""))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            die("401 unauthorized — token is wrong, expired, or revoked. "
                "Make a new one and run setup again.")
        if e.code == 403:
            die("403 forbidden — your school may have API access disabled, "
                "or you hit a rate limit. Use the browser-based /canvas instead.")
        if e.code == 404:
            return None, None
        die(f"HTTP {e.code} from {url}")
    except urllib.error.URLError as e:
        die(f"could not reach Canvas: {e.reason}")


def next_link(header):
    for part in header.split(","):
        m = re.search(r'<([^>]+)>\s*;\s*rel="next"', part)
        if m:
            return m.group(1)
    return None


def get_all(base, token, path, params=None, cap=50):
    """Follow pagination. cap = max pages, so a bad loop can't run forever."""
    params = dict(params or {})
    params.setdefault("per_page", 100)
    out, url, pages = [], base + path, 0
    while url and pages < cap:
        body, url = get(url, token, params if pages == 0 else None)
        if body is None:
            break
        if isinstance(body, dict):
            return body
        out.extend(body)
        pages += 1
    return out


# ---------- shaping ----------

def status_of(sub, due_at):
    if not sub:
        return "unknown"
    if sub.get("missing"):
        return "missing"
    ws = sub.get("workflow_state")
    if ws == "graded":
        return "graded"
    if sub.get("late"):
        return "late"
    if sub.get("submitted_at"):
        return "submitted"
    if ws in ("unsubmitted", None):
        return "not_submitted"
    return "unknown"


def grade_of(course):
    for e in course.get("enrollments") or []:
        if e.get("type") in ("student", "StudentEnrollment") or "computed_current_score" in e:
            score = e.get("computed_current_score")
            letter = e.get("computed_current_grade")
            if score is None and letter is None:
                return None
            if score is None:
                return letter
            return f"{score}%" + (f" ({letter})" if letter else "")
    return None


# ---------- commands ----------

def cmd_setup(args):
    print(RISKS)
    if not args.i_accept_the_risks:
        try:
            typed = input('Type "I ACCEPT" to continue (anything else cancels): ')
        except (EOFError, KeyboardInterrupt):
            print()
            die("cancelled", 2)
        if typed.strip().upper() != "I ACCEPT":
            die("cancelled — nothing was saved", 2)

    url = normalize_url(args.url or input("Canvas URL (e.g. school.instructure.com): "))

    token = args.token or os.environ.get("CANVAS_TOKEN")
    if not token:
        token = getpass.getpass("Access token (input hidden): ")
    token = token.strip()
    if not token:
        die("no token given")

    save_creds({
        "canvas_url": url,
        "token": token,
        "accepted_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    })
    print(f"\nsaved to {CREDS} (0600)")
    cmd_test(args)


def cmd_test(args):
    c = load_creds()
    me, _ = get(c["canvas_url"] + "/api/v1/users/self", c["token"])
    print(f"ok — connected as {me.get('name', '?')} at {c['canvas_url']}")


def cmd_status(args):
    if not os.path.exists(CREDS):
        print("not configured — browser mode only")
        return
    c = load_creds()
    tok = c.get("token", "")
    mode = oct(os.stat(CREDS).st_mode & 0o777)
    print(f"canvas_url  {c['canvas_url']}")
    print(f"token       ...{tok[-4:]}  ({len(tok)} chars, {CREDS}, mode {mode})")
    print(f"accepted    {c.get('accepted_at', '?')}")
    if os.path.exists(SNAPSHOT):
        with open(SNAPSHOT) as f:
            print(f"snapshot    {json.load(f).get('pulled_at', '?')}")
    else:
        print("snapshot    none yet — run: canvas-api.py pull")


def cmd_revoke(args):
    if os.path.exists(CREDS):
        os.remove(CREDS)
        print(f"deleted {CREDS}")
    else:
        print("no local token to delete")
    print("\nAlso delete it in Canvas: Account -> Settings -> Approved Integrations.\n"
          "Removing the local copy does NOT invalidate the token itself.")


def cmd_pull(args):
    c = load_creds()
    base, token = c["canvas_url"], c["token"]

    courses = get_all(base, token, "/api/v1/courses", {
        "enrollment_state": "active",
        "include[]": ["total_scores"],
    })
    courses = [c_ for c_ in courses if c_.get("id") and not c_.get("access_restricted_by_date")]
    if args.course:
        q = args.course.lower()
        courses = [c_ for c_ in courses
                   if q in (c_.get("name") or "").lower()
                   or q in (c_.get("course_code") or "").lower()]
        if not courses:
            die(f"no active course matching {args.course!r}")

    out = {
        "pulled_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "canvas_url": base,
        "source": "api",
        "courses": [],
        "unread": [],
    }

    for course in courses:
        cid = course["id"]
        name = course.get("course_code") or course.get("name") or str(cid)
        print(f"  {name} ...", end="", flush=True)
        assignments = get_all(base, token, f"/api/v1/courses/{cid}/assignments", {
            "include[]": ["submission"],
            "order_by": "due_at",
        })
        if isinstance(assignments, dict):
            assignments = []
        items = []
        for a in assignments:
            sub = a.get("submission") or {}
            items.append({
                "title": a.get("name"),
                "due": a.get("due_at"),
                "points": a.get("points_possible"),
                "status": status_of(sub, a.get("due_at")),
                "score": sub.get("score"),
                "url": a.get("html_url"),
            })
        out["courses"].append({
            "id": str(cid),
            "name": name,
            "full_name": course.get("name"),
            "current_grade": grade_of(course),
            "assignments": items,
        })
        print(f" {len(items)} assignments")

    os.makedirs(DIR, mode=0o700, exist_ok=True)
    with open(SNAPSHOT, "w") as f:
        json.dump(out, f, indent=2)
    total = sum(len(c_["assignments"]) for c_ in out["courses"])
    print(f"\nwrote {SNAPSHOT} — {len(out['courses'])} courses, {total} assignments")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("setup", help="save Canvas URL + token")
    s.add_argument("--url")
    s.add_argument("--token", help="prefer stdin or $CANVAS_TOKEN; argv is visible in ps")
    s.add_argument("--i-accept-the-risks", action="store_true",
                   help="skip the interactive confirmation")
    s.set_defaults(func=cmd_setup)

    sub.add_parser("test", help="verify the token").set_defaults(func=cmd_test)
    sub.add_parser("status", help="show config").set_defaults(func=cmd_status)
    sub.add_parser("revoke", help="delete the local token").set_defaults(func=cmd_revoke)

    s = sub.add_parser("pull", help="fetch coursework -> snapshot.json")
    s.add_argument("--course", help="only courses matching this name/code")
    s.set_defaults(func=cmd_pull)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
