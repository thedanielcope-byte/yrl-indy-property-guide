#!/usr/bin/env python3
"""Add the buyer & seller closing-checklist links into the nav dropdowns
site-wide: buyer link into the Buyers submenu, seller link into the Sellers
submenu. Idempotent; HTML-only. Anchors are unique (one per page)."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

INSERTS = [
  ('<a href="/services/down-payment-assistance/">Down Payment Help</a>',
   '<a href="/services/down-payment-assistance/">Down Payment Help</a>\n'
   ' <a href="/services/buyer-closing-checklist/">Closing Checklist</a>',
   '/services/buyer-closing-checklist/'),
  ('<a href="/services/for-sale-by-owner/">For Sale By Owner</a>',
   '<a href="/services/for-sale-by-owner/">For Sale By Owner</a>\n'
   ' <a href="/services/seller-closing-checklist/">Closing Checklist</a>',
   '/services/seller-closing-checklist/'),
]

changed = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    orig = s
    for anchor, repl, marker in INSERTS:
        if marker in s:      # already has this checklist link in nav/body
            continue
        if anchor in s:
            s = s.replace(anchor, repl, 1)
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
        changed += 1

print("nav: added closing-checklist links on %d pages" % changed)
