#!/usr/bin/env python3
"""Add a 'Free <County> Home Guides' section to each county hub, listing every
city in that county with links to its buyer + seller guide. Idempotent
(marker-wrapped), HTML-only. Cities are read from the county hub's own city links;
names come from city_guides_data.CITIES. Re-run after adding guides."""
import os, re, html, glob
from city_guides_data import CITIES

ROOT = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = "<!-- COUNTY-GUIDES -->", "<!-- /COUNTY-GUIDES -->"

def key_for(cityslug):
    return cityslug.replace("-indiana-real-estate", "").replace("-indianapolis-real-estate", "")

def county_name(county_slug):
    return county_slug.replace("-indiana-real-estate", "").replace("-", " ").title()

def section(cname, cities):
    rows = ""
    for key, name in cities:
        rows += (f'  <li><strong>{html.escape(name)}</strong> &mdash; '
                 f'<a href="/resources/{key}-home-buyers-guide/">Buyer&#8217;s Guide</a> &middot; '
                 f'<a href="/resources/{key}-home-sellers-guide/">Seller&#8217;s Guide</a></li>\n')
    return (
        f'{BEGIN}\n'
        ' <hr class="divider">\n'
        f' <h2>Free Home Guides for {html.escape(cname)} Cities</h2>\n'
        f' <p>Grab a free, city-specific buyer&#8217;s or seller&#8217;s guide for any {html.escape(cname)} community &mdash; the local market, schools, neighborhoods, and every step of the process.</p>\n'
        ' <ul style="columns:2;column-gap:32px;list-style:none;padding:0;margin:8px 0 0;">\n'
        f'{rows}'
        ' </ul>\n'
        f'{END}\n\n ')

done = 0
for hub in glob.glob(os.path.join(ROOT, "counties", "*", "index.html")):
    cslug = os.path.basename(os.path.dirname(hub))
    county_path = cslug.replace("-indiana-real-estate", "")   # e.g. hamilton-county
    src = open(hub, encoding="utf-8").read()
    # cities in THIS county only (exclude footer/other-county links)
    seen, cities = set(), []
    for m in re.finditer(r'href="/cities/' + re.escape(county_path) + r'/([a-z0-9-]+)/"', src):
        k = key_for(m.group(1))
        if k in seen:
            continue
        seen.add(k)
        if os.path.isdir(os.path.join(ROOT, "resources", f"{k}-home-buyers-guide")):
            name = CITIES.get(k, {}).get("name") or k.replace("-", " ").title()
            cities.append((k, name))
    if not cities:
        continue
    cities.sort(key=lambda x: x[1])
    src = re.sub(r"\s*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "\n ", src, flags=re.DOTALL)
    blk = section(county_name(cslug), cities)
    m = re.search(r'<hr class="divider">\s*<h3>\s*Explore', src)
    if m:
        out = src[:m.start()] + blk + src[m.start():]
    else:
        m2 = re.search(r'<aside class="content-sidebar">', src) or re.search(r'<footer class="site-footer">', src)
        if not m2:
            continue
        out = src[:m2.start()] + blk + src[m2.start():]
    open(hub, "w", encoding="utf-8").write(out)
    done += 1

print("Added county-guide section to %d county hubs." % done)
