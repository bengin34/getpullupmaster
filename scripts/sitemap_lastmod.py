#!/usr/bin/env python3
"""Set <lastmod> in sitemap.xml from git history (idempotent).

    python3 scripts/sitemap_lastmod.py

Each <loc> maps to <path>/index.html. lastmod is the date of the last commit that
touched that file; files with uncommitted changes get today's date. Run it before
committing a content change so Google sees accurate dates.
"""
import datetime
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://getpullupmaster.app"


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout


def main():
    dirty = {line[3:] for line in git("status", "--porcelain").splitlines()}
    today = datetime.date.today().isoformat()
    path = os.path.join(ROOT, "sitemap.xml")
    xml = open(path, encoding="utf-8").read()

    def repl(m):
        loc = m.group(1)
        rel = loc[len(BASE):].strip("/")
        f = f"{rel}/index.html" if rel else "index.html"
        if f in dirty:
            date = today
        else:
            date = git("log", "-1", "--format=%cs", "--", f).strip() or today
        rest = re.sub(r"<lastmod>[^<]*</lastmod>", "", m.group(2))
        return f"<url><loc>{loc}</loc><lastmod>{date}</lastmod>{rest}</url>"

    new = re.sub(r"<url><loc>([^<]+)</loc>(.*?)</url>", repl, xml)
    open(path, "w", encoding="utf-8").write(new)
    print(f"lastmod set on {new.count('<lastmod>')} URL(s)")


if __name__ == "__main__":
    main()
