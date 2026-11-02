#!/usr/bin/env python3
"""City pages: send town-specific "search" links to that town's listings and add a short
call-to-action bar right under the Quick Answer.

- /search/?q=<Town> makes the Displet search filter by city (see inject_search_query.py,
  which recognizes the towns in county_towns.json). Neighborhood pages that aren't MLS
  cities use their ZIP instead (Broad Ripple 46220, Irvington 46219, Camby 46113, Eagle
  Creek 46254). Geist and Bean Blossom keep the plain search (no single ZIP fits).
- Only links whose anchor text names the town are re-pointed; site-wide "Search Homes"
  links are left alone.
- The CTA bar sits between <!-- CITY-CTA --> markers. Idempotent; re-run after city pages
  are rebuilt.
"""
import glob, html, json, re
from urllib.parse import quote

START, END = "<!-- CITY-CTA -->", "<!-- /CITY-CTA -->"
towns = json.load(open("county_towns.json"))
KNOWN = {re.sub(r"[^a-z0-9 ]", " ", t.lower()).strip() for lst in towns.values() for t in lst if t.strip()}
ZIPS = {"broad-ripple": "46220", "irvington": "46219", "camby": "46113", "eagle-creek": "46254"}


def town_name(s, slug):
    t = re.search(r"<h1>(.*?)</h1>", s, re.S)
    raw = html.unescape(re.sub(r"<[^>]+>", " ", t.group(1))) if t else ""
    m = re.match(r"\s*([A-Z][\w.'’ -]+?)(?:,| Indiana| Indianapolis| Real Estate| Homes)", raw)
    return m.group(1).strip() if m else slug.replace("-", " ").title()


n = 0
for path in sorted(glob.glob("cities/*/*/index.html")):
    slug = re.sub(r"-(indiana|indianapolis)-real-estate$", "", path.split("/")[2])
    s = open(path, encoding="utf-8").read(); s0 = s
    town = town_name(s, slug)
    norm = re.sub(r"[^a-z0-9 ]", " ", town.lower()).strip()
    q = town if norm in KNOWN else ZIPS.get(slug)
    search = f"/search/?q={quote(q)}" if q else "/search/"
    town_html = html.escape(town, quote=False).replace("'", "&#x27;")
    # re-point town-specific search links (anchor text mentions the town)
    def repoint(m):
        plain = html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))
        return f'<a href="{search}"{m.group(2)}>{m.group(3)}</a>' if town in plain else m.group(0)
    s = re.sub(r'<a href="(/search/(?:\?q=[^"]*)?)"([^>]*)>(.*?)</a>', repoint, s)
    # CTA bar under the Quick Answer
    bar = (f'{START}\n <div class="city-cta" style="display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 24px;">\n'
           f'  <a href="{search}" class="btn btn-primary">See {town_html} homes for sale &rarr;</a>\n'
           f'  <a href="/services/free-home-valuation/" class="btn btn-outline">What&rsquo;s my {town_html} home worth?</a>\n'
           f' </div>\n{END}\n')
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, flags=re.S)
    m = re.search(r"<!-- QA-END -->\n", s)
    if m:
        s = s[:m.end()] + bar + s[m.end():]
    else:   # newer pages without a Quick Answer: put the bar before the first section heading
        mm = s.find('<main class="content-main">')
        h = s.find("<h2", mm) if mm >= 0 else -1
        if h < 0:
            print("  no anchor:", path)
        else:
            ls = s.rfind("\n", 0, h) + 1
            s = s[:ls] + bar + s[ls:]
    if s != s0:
        open(path, "w", encoding="utf-8").write(s); n += 1
print("city CTA / search links updated on", n, "pages")
