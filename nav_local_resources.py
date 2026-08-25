#!/usr/bin/env python3
"""Convert the top-level nav "Vendors" link into a "Local Resources" dropdown
(Preferred Vendors + Utilities & Setup) across every public-site page.

The exact anchor `<a href="/vendors/">Vendors</a>` appears exactly once per page
(the nav; no footer/breadcrumb collision), so a literal string replace is safe.
Idempotent: pages already carrying the dropdown are skipped. HTML-only."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = '<a href="/vendors/">Vendors</a>'
NEW = ('<div class="nav-item-dropdown">\n'
       ' <a href="/vendors/">Local Resources</a>\n'
       ' <div class="nav-submenu">\n'
       ' <a href="/vendors/">Preferred Vendors</a>\n'
       ' <a href="/utilities/">Utilities &amp; Setup</a>\n'
       ' </div>\n'
       ' </div>')

changed = skipped = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    if ">Local Resources</a>" in s:
        skipped += 1; continue
    if OLD not in s:
        continue
    open(f, "w", encoding="utf-8").write(s.replace(OLD, NEW, 1))
    changed += 1

print("nav: converted Vendors -> Local Resources dropdown on %d pages (%d already done)"
      % (changed, skipped))
