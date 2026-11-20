#!/usr/bin/env python3
"""Add a "More Neighborhoods in <Town>" block to every community page (Nov 2026).

Each /communities/<slug>/ page links the other communities in the same town (or the same area for
Indianapolis-area records with `area`, e.g. Franklin Township), plus the town's
/best/neighborhoods-in-<town>-indiana/ roundup when it exists. Before this, community pages linked
only to the /communities/ hub, so most had two or fewer internal links pointing in.

Marker-wrapped (<!-- COMMUNITY-SIBLINGS --> ... <!-- /COMMUNITY-SIBLINGS -->), inserted just before
the FAQ section. Idempotent: re-running refreshes the block. Re-run after build_communities.py or
build_neighborhood_roundups.py.
"""
import os, re, json, html, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "communities.json"), encoding="utf-8"))
START, END = "<!-- COMMUNITY-SIBLINGS -->", "<!-- /COMMUNITY-SIBLINGS -->"
CAP = 20

def esc(s): return html.escape(str(s or ""), quote=False)
def disp(c): return c.get("short_name") or c["name"]
def kebab(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "").replace("’", "")).strip("-")
def group_key(c): return c.get("area") or c["city"]

groups = collections.defaultdict(list)
for c in DATA["communities"]:
    groups[group_key(c)].append(c)

def roundup(city):
    k = kebab(city)
    p = os.path.join(ROOT, "best", f"neighborhoods-in-{k}-indiana", "index.html")
    return f"/best/neighborhoods-in-{k}-indiana/" if os.path.isfile(p) else None

ANCHOR = re.compile(r'(?:<!-- FAQ -->\s*)?<section class="faq-section">')

done = skipped = missing = 0
for c in DATA["communities"]:
    p = os.path.join(ROOT, "communities", c["slug"], "index.html")
    if not os.path.isfile(p):
        missing += 1; continue
    t = open(p, encoding="utf-8").read()
    t0 = t
    t = re.sub(r"\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n*", "\n", t, flags=re.S) if START in t else t
    g = group_key(c)
    sibs = sorted((x for x in groups[g] if x["slug"] != c["slug"]), key=disp)[:CAP]
    ru = roundup(c["city"]) if not c.get("area") else None
    if not sibs and not ru:
        skipped += 1
        if t != t0: open(p, "w", encoding="utf-8").write(t)
        continue
    place = esc(g)
    lead = f"Compare {esc(disp(c))} with other {place} neighborhoods"
    lead += (f", or see our guide to the <a href=\"{ru}\">best neighborhoods in {esc(c['city'])}</a>, grouped by type with typical prices and schools."
             if ru else ".")
    cards = "\n".join(f'  <a href="/communities/{x["slug"]}/" class="city-card">{esc(disp(x))} <span class="arrow">&rsaquo;</span></a>' for x in sibs)
    block = (f"{START}\n <h2 id=\"more-neighborhoods\">More Neighborhoods in {place}</h2>\n <p>{lead}</p>\n"
             + (f" <div class=\"city-grid\">\n{cards}\n </div>\n" if sibs else "")
             + f" {END}\n\n ")
    m = ANCHOR.search(t)
    if not m:
        print("no FAQ anchor:", c["slug"]); missing += 1; continue
    t = t[:m.start()] + block + t[m.start():]
    if t != t0:
        open(p, "w", encoding="utf-8").write(t); done += 1
print(f"community siblings — updated {done} | skipped (no siblings) {skipped} | missing/no anchor {missing}")
