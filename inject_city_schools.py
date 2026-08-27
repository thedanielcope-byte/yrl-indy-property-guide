#!/usr/bin/env python3
"""Deep-link every school district (and private school) that serves a city into
that city's page. Idempotent, HTML-only. Uses schools.json's city_schools map.

For pages with the hand-authored <!-- SCHOOLS --> prose, the marker-wrapped
deep-link block is appended right after that paragraph (keeps the good prose,
adds linked district/school cards). For pages without a schools section, the
block is inserted before the Communities/Explore anchor with its own H2. Also
refreshes the quick-facts 'School district' value to list every district.
Same injector pattern as inject_city_communities.py."""
import os, re, html, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "schools.json"), encoding="utf-8"))
CITY_SCHOOLS = DATA["city_schools"]
BY_SLUG = {d["slug"]: d for d in DATA["districts"]}
BEGIN, END = "<!-- CITY-SCHOOLS -->", "<!-- /CITY-SCHOOLS -->"

def esc(s): return html.escape(str(s or ""), quote=False)
def label(slug): return BY_SLUG.get(slug, {}).get("short_name") or slug

CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def city_dir(city):
    kebab = city.strip().lower().replace(" ", "-").replace(".", "")
    for d in CITY_DIRS:
        if os.path.basename(d.rstrip(os.sep)).startswith(kebab + "-"):
            return d.rstrip(os.sep)
    return None

def cards(slugs):
    return "\n".join(
      '  <a href="/schools/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
      % (s, esc(label(s))) for s in slugs)

def section(city, rec, with_h2):
    pub, prv, note = rec["public"], rec["private"], (rec.get("note") or "")
    out = [BEGIN]
    if with_h2:
        out += [' <hr class="divider">',
                ' <h2 id="schools">Schools in %s, Indiana</h2>' % esc(city),
                (' <p>%s is served by the school districts below. Because attendance boundaries '
                 'depend on the exact address, a Your Realty Link agent can confirm the assigned '
                 'schools for any home.</p>' % esc(city))]
    else:
        out.append(' <h3 id="school-districts">School Districts &amp; Schools Serving %s</h3>' % esc(city))
    out += [' <p><strong>Public school districts:</strong></p>', ' <div class="city-grid">', cards(pub), ' </div>']
    if prv:
        out += [' <p><strong>Private &amp; parochial schools:</strong></p>', ' <div class="city-grid">', cards(prv), ' </div>']
    if note:
        out.append(' <p class="school-note"><em>%s A Your Realty Link agent can confirm the assigned '
                   'schools for any specific address.</em></p>' % esc(note))
    out.append(' <p>Compare every district in the <a href="/schools/">Central Indiana school districts</a> guide.</p>')
    out.append(END)
    return "\n".join(out) + "\n\n "

def update_quickfacts(s, pub):
    """Refresh the quick-facts 'School district' value to name every district."""
    names = ", ".join(label(x) for x in pub)
    return re.sub(r'(<dt>School district</dt>\s*<dd>).*?(</dd>)',
                  lambda m: m.group(1) + esc(names) + m.group(2), s, count=1, flags=re.DOTALL)

def inject(pathdir, city, rec):
    f = os.path.join(pathdir, "index.html")
    s = open(f, encoding="utf-8").read()
    s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "", s, flags=re.DOTALL)
    s = update_quickfacts(s, rec["public"])   # edit quick-facts FIRST, then compute the anchor on final s
    has = "<!-- SCHOOLS -->" in s
    sec = section(city, rec, with_h2=not has)
    if has:
        i = s.index("<!-- SCHOOLS -->") + len("<!-- SCHOOLS -->")
        m = re.search(r"<!--", s[i:])          # insert before the next section marker
        pos = i + m.start() if m else None
    else:
        pos = None
    if pos is None:
        m = (re.search(re.escape("<!-- CITY-COMMUNITIES -->"), s)
             or re.search(r'<hr class="divider">\s*<h3>\s*Explore', s)
             or re.search(r'<div class="cta-form-section"', s))
        pos = m.start() if m else s.find("</main>")
    if pos < 0:
        return False
    open(f, "w", encoding="utf-8").write(s[:pos] + sec + s[pos:])
    return True

done, warn = 0, []
for city, rec in CITY_SCHOOLS.items():
    d = city_dir(city)
    if not d:
        warn.append("no city page for " + city); continue
    if inject(d, city, rec):
        done += 1
    else:
        warn.append("no anchor in " + city)

print("injected schools section into %d city pages" % done)
for w in warn: print("  WARN " + w)
