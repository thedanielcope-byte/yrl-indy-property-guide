#!/usr/bin/env python3
"""Add a 'Free <City> Home Guides' CTA card to the sidebar of every city page that
has guides (per city_guides_data.CITIES). Idempotent (marker-wrapped), HTML-only.
Inserts just before the 'Search <City> Homes' sidebar card (falls back to the top
of the sidebar). Re-run after adding cities to city_guides_data.py."""
import os, re, html
from city_guides_data import CITIES

ROOT = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = "<!-- CITY-GUIDES-CTA -->", "<!-- /CITY-GUIDES-CTA -->"

def card(key):
    n = html.escape(CITIES[key]["name"])
    return (
        f'{BEGIN}\n'
        '  <div class="sidebar-card">\n'
        f'   <div class="sidebar-card-header">Free {n} Home Guides</div>\n'
        '   <div class="sidebar-card-body">\n'
        f'    <p>Buying or selling in {n}? Get our free, {n}-specific guide &mdash; the local market, neighborhoods, schools, and every step.</p>\n'
        f'    <a href="/resources/{key}-home-buyers-guide/" class="btn btn-primary btn-sm btn-full">Get the {n} Buyer&#8217;s Guide &rarr;</a>\n'
        f'    <p style="text-align:center;margin:10px 0 0;font-size:.85rem;"><a href="/resources/{key}-home-sellers-guide/" style="color:var(--red);font-weight:600;">Selling instead? Seller&#8217;s Guide &rarr;</a></p>\n'
        '   </div>\n  </div>\n'
        f'{END}\n ')

done = warn = 0
for key, d in CITIES.items():
    page = os.path.join(ROOT, d["url"].strip("/"), "index.html")
    if not os.path.isfile(page):
        warn += 1; print("  no page for", key, d["url"]); continue
    # guides must exist
    if not os.path.isdir(os.path.join(ROOT, "resources", f"{key}-home-buyers-guide")):
        continue
    src = open(page, encoding="utf-8").read()
    src = re.sub(r"\s*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "\n ", src, flags=re.DOTALL)
    block = card(key)
    m = re.search(r'<div class="sidebar-card">\s*<div class="sidebar-card-header">\s*Search[^<]*Homes', src)
    if m:
        out = src[:m.start()] + block + " " + src[m.start():]
    else:
        m2 = re.search(r'<aside class="content-sidebar">', src)
        if not m2:
            warn += 1; print("  no sidebar anchor in", key); continue
        out = src[:m2.end()] + "\n " + block + src[m2.end():]
    open(page, "w", encoding="utf-8").write(out)
    done += 1

print("Guide CTA added to %d city sidebars." % done)
if warn:
    print("warnings:", warn)
