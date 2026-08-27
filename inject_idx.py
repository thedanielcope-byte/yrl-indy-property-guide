#!/usr/bin/env python3
"""Inject the site-wide IDX / MLS listings slot into city, community, county and
neighborhood pages. Marker-wrapped (<!-- IDX-LISTINGS -->), idempotent, HTML-only.

Deeplink mode (now): each page gets a card linking to YRL's live Agent3000 MLS
search, pre-filtered by city/county. Embed mode (later): the same slot renders
the dedicated IDX widget. All behavior is driven by idx_config.py — switching or
upgrading the IDX is a config edit + re-running this script. Same injector
pattern as inject_city_communities.py."""
import os, re, html, json, glob
import idx_config as idx

ROOT = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = "<!-- IDX-LISTINGS -->", "<!-- /IDX-LISTINGS -->"
COMM = json.load(open(os.path.join(ROOT, "communities.json"), encoding="utf-8"))

def esc(s): return html.escape(str(s or ""), quote=False)

def h1_of(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if not m: return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).replace("&amp;", "&").strip()

def card(heading, body, btn_label, btn_url):
    """The listings slot. Deeplink now; embed later swaps the inner via config."""
    if idx.MODE == "embed" and idx.EMBED_SNIPPET:
        inner = idx.EMBED_SNIPPET + (
            '\n <p class="idx-fallback"><a href="%s" target="_blank" rel="noopener">%s</a></p>'
            % (esc(btn_url), esc(btn_label)))
    else:
        inner = "\n".join([
            ' <h3>%s</h3>' % esc(heading),
            ' <p>%s</p>' % esc(body),
            ' <div class="btn-group">',
            ('  <a href="%s" class="btn btn-primary" target="_blank" rel="noopener">%s</a>'
             % (esc(btn_url), esc(btn_label))),
            ('  <a href="/services/free-home-valuation/" class="btn btn-outline" '
             'target="_blank" rel="noopener">What\'s My Home Worth?</a>'),
            ' </div>',
        ])
    return "\n".join([BEGIN, ' <div class="cta-block cta-light idx-listings">', inner,
                      ' </div>', END]) + "\n\n "

def inject(f, sec):
    s = open(f, encoding="utf-8").read()
    s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "", s, flags=re.DOTALL)
    # place the slot above the Communities section / Explore links, below the written content
    m = (re.search(re.escape("<!-- CITY-COMMUNITIES -->"), s)
         or re.search(r'<hr class="divider">\s*<h3>\s*Explore', s)
         or re.search(r'<div class="cta-form-section"', s))
    pos = m.start() if m else s.find("</main>")
    if pos < 0:
        return False
    open(f, "w", encoding="utf-8").write(s[:pos] + sec + s[pos:])
    return True

done, warn = 0, []

def do(f, sec):
    global done
    if inject(f, sec): done += 1
    else: warn.append("no anchor: " + f)

# ---- City pages -> ?city=<City> (confirmed) ----
for d in sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep)):
    f = os.path.join(d, "index.html")
    if not os.path.exists(f): continue
    city = re.split(r"\s+Indiana", h1_of(open(f, encoding="utf-8").read()))[0].strip()
    if not city: warn.append("no city name: " + d); continue
    do(f, card("Search All Homes for Sale in %s" % city,
               "Browse every active %s listing on the MIBOR MLS — updated continuously with "
               "photos, prices and full details." % city,
               "View %s Homes for Sale →" % city, idx.city_search_url(city)))

# ---- Community detail pages -> ?city=<community.city> (reliable interim) ----
for c in COMM["communities"]:
    f = os.path.join(ROOT, "communities", c["slug"], "index.html")
    if not os.path.exists(f): continue
    name = c.get("short_name") or c["name"]; city = c["city"]
    do(f, card("Homes for Sale in %s" % name,
               "See active listings in and around %s in %s on the MIBOR MLS, refreshed "
               "continuously." % (name, city),
               "View %s Homes for Sale →" % city, idx.city_search_url(city)))

# ---- County hub pages -> ?county=<County> (best-effort interim) ----
for d in sorted(glob.glob(os.path.join(ROOT, "counties", "*") + os.sep)):
    f = os.path.join(d, "index.html")
    if not os.path.exists(f): continue
    disp = re.split(r"\s+Indiana", h1_of(open(f, encoding="utf-8").read()))[0].strip()
    if not disp: warn.append("no county name: " + d); continue
    county = re.sub(r"\s+County$", "", disp)
    do(f, card("Search Homes for Sale Across %s" % disp,
               "Browse active listings across %s on the MIBOR MLS, from starter homes to "
               "luxury — updated continuously." % disp,
               "View %s Listings →" % disp, idx.county_search_url(county)))

# ---- Indianapolis neighborhood pages -> ?city=Indianapolis (interim; area-precise in embed mode) ----
for d in sorted(glob.glob(os.path.join(ROOT, "neighborhoods", "*") + os.sep)):
    f = os.path.join(d, "index.html")
    if not os.path.exists(f): continue
    nm = re.split(r"\s+(?:Indianapolis|Homes|Real Estate|Neighborhood)",
                  h1_of(open(f, encoding="utf-8").read()))[0].strip()
    if not nm: warn.append("no nbhd name: " + d); continue
    do(f, card("Homes for Sale in %s" % nm,
               "Browse active Indianapolis MLS listings near %s — updated continuously with "
               "photos, prices and details." % nm,
               "View Indianapolis Homes for Sale →", idx.city_search_url("Indianapolis")))

print("IDX slot injected into %d pages (mode=%s)" % (done, idx.MODE))
for w in warn: print("  WARN " + w)
