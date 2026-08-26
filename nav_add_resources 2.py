#!/usr/bin/env python3
"""Add a "Free Guides & Resources" link (-> /resources/) into the Local Resources
nav dropdown site-wide, so the /resources/ hub is no longer orphaned from the
main nav. Idempotent; HTML-only. Anchor is unique (one per page)."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
ANCHOR = '<a href="/utilities/">Utilities &amp; Setup</a>'
NEW = (ANCHOR + '\n <a href="/resources/">Free Guides &amp; Resources</a>')
MARKER = '<a href="/resources/">Free Guides &amp; Resources</a>'

changed = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    if MARKER in s or ANCHOR not in s:
        continue
    open(f, "w", encoding="utf-8").write(s.replace(ANCHOR, NEW, 1))
    changed += 1

print("nav: added 'Free Guides & Resources' -> /resources/ on %d pages" % changed)
