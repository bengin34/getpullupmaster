#!/usr/bin/env python3
"""Append a link to the "Keep reading" list of an existing article page.

Usage:
    python3 scripts/add_keep_reading.py <page-dir> <href> <title>
    e.g. python3 scripts/add_keep_reading.py de/klimmzug-muskeln /de/latissimus-klimmzug/ "Latissimus: ..."

Idempotent: does nothing if the href is already in that list. Exits 1 if the page has no keep-reading list.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADINGS = ["Keep reading", "Weiterlesen", "Bunları da oku", "Sigue aprendiendo", "À lire aussi"]


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    page_dir, href, title = sys.argv[1:4]
    path = os.path.join(ROOT, page_dir.strip("/"), "index.html")
    src = open(path, encoding="utf-8").read()
    pat = re.compile(r"(<h2>(?:%s)</h2>\s*<ul[^>]*>)(.*?)(</ul>)" % "|".join(map(re.escape, HEADINGS)), re.S)
    m = pat.search(src)
    if not m:
        print(f"no keep-reading list in {path}")
        sys.exit(1)
    if f'href="{href}"' in m.group(2):
        print(f"already linked: {page_dir} -> {href}")
        return
    li = f'<li><a href="{html.escape(href, quote=True)}">{html.escape(title, quote=False)}</a></li>'
    new = src[: m.end(2)] + li + src[m.end(2):]
    open(path, "w", encoding="utf-8").write(new)
    print(f"linked: {page_dir} -> {href}")


if __name__ == "__main__":
    main()
