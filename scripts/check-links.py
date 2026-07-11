#!/usr/bin/env python3
"""External-link checker for entry sources.

Fetches every http(s) link in entries/*.md and reports its status. Runs on a
schedule (and by hand), deliberately OFF the required-check path: a publisher's
transient outage should not block an editorial pull request, so link rot is
surfaced as a scheduled report instead. Redirects count as alive; only hard
failures (4xx/5xx after retry, DNS errors, timeouts) are reported as broken.

No third-party dependencies. Requires Python 3.9+.
Exit status: non-zero only if at least one link hard-fails.
"""
from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(REPO, "entries")
LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")
UA = {"User-Agent": "gold-plating-link-check/1 (+https://github.com)"}
TIMEOUT = 20


def probe(url: str) -> tuple[bool, str]:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=UA, method=method)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return True, f"{resp.status}"
        except urllib.error.HTTPError as e:
            if method == "GET":  # some hosts reject HEAD; only GET's verdict is final
                return False, f"HTTP {e.code}"
        except Exception as e:  # DNS, TLS, timeout — treat as hard failure on GET
            if method == "GET":
                return False, type(e).__name__
    return False, "unreachable"


def main() -> int:
    urls: dict[str, list[str]] = {}
    for name in sorted(os.listdir(ENTRIES)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(ENTRIES, name), encoding="utf-8") as fh:
            for url in LINK_RE.findall(fh.read()):
                urls.setdefault(url, []).append(name)

    broken = 0
    for url, files in urls.items():
        ok, status = probe(url)
        mark = "ok  " if ok else "DEAD"
        print(f"{mark} {status:>12}  {url}  ({', '.join(sorted(set(files)))})")
        if not ok:
            broken += 1

    print(f"\n{len(urls)} unique links checked, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
