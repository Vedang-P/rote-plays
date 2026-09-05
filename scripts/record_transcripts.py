#!/usr/bin/env python3
"""Record trimmed GitHub API responses for the contribution-ready reference corpus.

Dev-time tool (not shipped in the play package). For each reference repo it fetches
the exact endpoints the analyzer reads, trims each response to the used field set,
and writes resources/transcripts/<slug>/<step>.json plus <step>.status.

Usage: python3 scripts/record_transcripts.py [repo_slug ...]
"""

import datetime
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "contribution-ready" / "resources" / "transcripts"
UA = "contribution-ready-recorder/1.0"

REPOS = {
    # (slug, owner/repo, expected verdict in the corpus)
    "go-prettier": "prettier/prettier",
    "unsure-ky": "sindresorhus/ky",
    "avoid-archived": "sdmg15/Best-websites-a-programmer-should-visit",
    "dead-shadowsocks": "shadowsocks/shadowsocks-windows",
    # GSoC 2026 orgs (validation corpus)
    "gsoc-wagtail": "wagtail/wagtail",
    "gsoc-checkstyle": "checkstyle/checkstyle",
    "gsoc-dart": "dart-lang/sdk",
    "gsoc-openelis": "DIGI-UW/OpenELIS-Global-2",
}


def fetch(path, accept=None):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept or "application/vnd.github+json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                wait = int(e.headers.get("Retry-After", "5"))
                print(f"  rate-limited ({e.code}); waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            body = e.read().decode()[:200]
            try:
                return e.code, json.loads(body)
            except json.JSONDecodeError:
                return e.code, {"message": body}
    raise RuntimeError(f"gave up after retries: {url}")


def fetch_gh(path, accept=None):
    """Same endpoints via `gh api` (authenticated 5000/hr). Dev-time only."""
    import subprocess
    cmd = ["gh", "api", "--method", "GET", path]
    if accept:
        cmd += ["-H", f"Accept: {accept}"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        # gh prints a JSON body for HTTP errors on stdout
        try:
            return p.returncode + 100, json.loads(p.stdout)
        except json.JSONDecodeError:
            return p.returncode, {"message": p.stderr.strip()[:200]}
    return 200, json.loads(p.stdout)


def trim_repo(d):
    return {
        "full_name": d.get("full_name"),
        "private": d.get("private"),
        "fork": d.get("fork"),
        "archived": d.get("archived"),
        "default_branch": d.get("default_branch"),
        "open_issues_count": d.get("open_issues_count"),
        "license": {"spdx_id": (d.get("license") or {}).get("spdx_id")} if d.get("license") else None,
    }


def trim_commits(d):
    out = []
    for c in d or []:
        out.append({"sha": c.get("sha"),
                    "commit": {"author": {"date": ((c.get("commit") or {})
                                                   .get("author") or {}).get("date")}}})
    return out


def trim_contributors(d):
    return [{"login": c.get("login"), "contributions": c.get("contributions")} for c in d or []]


def trim_pulls(d):
    out = []
    for p in d or []:
        out.append({
            "number": p.get("number"),
            "state": p.get("state"),
            "created_at": p.get("created_at"),
            "merged_at": p.get("merged_at"),
            "user": {"login": (p.get("user") or {}).get("login")},
            "author_association": p.get("author_association"),
            "comments": p.get("comments"),
            "review_comments": p.get("review_comments"),
        })
    return out


QUERIED_TREE_PATHS = ('contributing.md', 'code_of_conduct.md', 'security.md')


def trim_trees(d):
    names = [t.get("path") for t in (d.get("tree") or [])]
    keep = [p for p in names if p and (p.lower() in QUERIED_TREE_PATHS
            or p.lower() == '.github'
            or 'workflows/' in p.lower()
            or 'pull_request_template' in p.lower())]
    return {"truncated": d.get("truncated"), "entry_count": len(names),
            "tree": [{"path": p} for p in keep]}


def trim_labels(d):
    return [{"name": l.get("name")} for l in d or []]


def trim_search(d):
    return {
        "total_count": d.get("total_count"),
        "items": [{
            "number": i.get("number"),
            "state": i.get("state"),
            "created_at": i.get("created_at"),
            "merged_at": i.get("merged_at"),
            "comments": i.get("comments"),
            "user": {"login": (i.get("user") or {}).get("login")},
            "author_association": i.get("author_association"),
        } for i in (d.get("items") or [])],
    }


def trim_contributing(d):
    return {"path": d.get("path"), "size": d.get("size"), "text": d.get("text")}


def record(repo_slug, owner_repo, via_gh=False):
    fetcher = fetch_gh if via_gh else fetch
    dest = OUT / repo_slug
    dest.mkdir(parents=True, exist_ok=True)
    o, r = owner_repo.split("/")
    print(f"== {repo_slug} ({owner_repo}) ==")

    def save(name, status, body, trimer):
        (dest / f"{name}.json").write_text(json.dumps(trimer(body), indent=1))
        (dest / f"{name}.status").write_text(str(status))
        print(f"  {name}: HTTP {status}")

    status, repo = fetcher(f"/repos/{o}/{r}")
    save("repos", status, repo, trim_repo)
    default_branch = repo.get("default_branch") or "main"

    status, commits = fetcher(f"/repos/{o}/{r}/commits?per_page=1&sha={default_branch}")
    save("commits", status, commits, trim_commits)

    status, contributors = fetcher(f"/repos/{o}/{r}/contributors?per_page=100")
    save("contributors", status, contributors, trim_contributors)

    status, pulls = fetcher(f"/repos/{o}/{r}/pulls?state=closed&sort=updated&direction=desc&per_page=100")
    save("pulls", status, pulls, trim_pulls)

    status, trees = fetcher(f"/repos/{o}/{r}/git/trees/{default_branch}?recursive=0")
    save("trees", status, trees, trim_trees)

    status, labels = fetcher(f"/repos/{o}/{r}/labels?per_page=100")
    save("labels", status, labels, trim_labels)

    since = (datetime.date.today() - datetime.timedelta(days=180)).isoformat()
    status, search = fetcher(
        f"/search/issues?q=repo:{o}/{r}+type:pr+is:merged+merged:%3E={since}"
        f"&sort=merged&order=desc&per_page=30")
    save("search", status, search, trim_search)

    status, protection = fetcher(f"/repos/{o}/{r}/branches/{default_branch}")
    save("branches", status, {"protected": (protection or {}).get("protected")}, lambda d: d)

    status, contributing = fetcher(f"/repos/{o}/{r}/contents/CONTRIBUTING.md?ref={default_branch}")
    if status == 200:
        save("contributing", status, {"content": contributing.get("content")}, lambda d: d)
    else:
        save("contributing", status, {}, lambda d: d)


def main():
    args = sys.argv[1:]
    via_gh = "--via-gh" in args
    args = [a for a in args if a != "--via-gh"]
    slugs = args or list(REPOS)
    for s in slugs:
        record(s, REPOS[s], via_gh=via_gh)


if __name__ == "__main__":
    main()
