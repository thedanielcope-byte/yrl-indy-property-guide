#!/usr/bin/env python3
"""Inject a 'Communities & Subdivisions in <City>' section into each city page
that has named communities in communities.json. Idempotent (marker-wrapped),
HTML-only, links each community's detail page. Same pattern as inject_events.py."""
import os, re, html, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "communities.json"), encoding="utf-8"))
BEGIN, END = "<!-- CITY-COMMUNITIES -->", "<!-- /CITY-COMMUNITIES -->"

def esc(s): return html.escape(str(s or ""), quote=False)
def disp(c): return c.get("short_name") or c["name"]

CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def city_dir(city):
    kebab = city.strip().lower().replace(" ", "-").replace(".", "").replace("'", "").replace("’", "")
    for d in CITY_DIRS:
        if os.path.basename(d.rstrip(os.sep)).startswith(kebab + "-"):
            return d.rstrip(os.sep)
    return None

by_city = {}
for c in DATA["communities"]:
    by_city.setdefault(c["city"], []).append(c)

def section(city, comms):
    cards = "\n".join(
      '  <a href="/communities/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
      % (c["slug"], esc(disp(c))) for c in sorted(comms, key=lambda x: disp(x)))
    return "\n".join([
      BEGIN,
      ' <hr class="divider">',
      ' <h2 id="communities">Communities &amp; Subdivisions in %s</h2>' % esc(city),
      (' <p>%s is home to a number of established and newer named communities. Explore local '
       'subdivisions with market info, schools, and amenities:</p>' % esc(city)),
      ' <div class="city-grid">',
      cards,
      ' </div>',
      (' <p>See every neighborhood in the <a href="/communities/">Central Indiana communities '
       '&amp; subdivisions</a> directory.</p>'),
      END,
    ]) + "\n\n "

def inject(pathdir, sec):
    f = os.path.join(pathdir, "index.html")
    s = open(f, encoding="utf-8").read()
    s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "", s, flags=re.DOTALL)
    m = re.search(r'<hr class="divider">\s*<h3>\s*Explore', s)
    if m:
        pos = m.start()
    else:
        m2 = re.search(r'<div class="info-box"', s)
        pos = m2.start() if m2 else s.find("</main>")
    if pos < 0:
        return False
    open(f, "w", encoding="utf-8").write(s[:pos] + sec + s[pos:])
    return True

done, warn = 0, []
for city, comms in by_city.items():
    d = city_dir(city)
    if not d:
        warn.append("no city page for " + city); continue
    if inject(d, section(city, comms)):
        done += 1
    else:
        warn.append("no anchor in " + city)

print("injected communities section into %d city pages" % done)
for w in warn: print("  WARN " + w)
