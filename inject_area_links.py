#!/usr/bin/env python3
"""Contextual links from related city and school pages to the township / area guides
built by build_areas.py. One short sentence, marker-wrapped (<!-- AREA-LINK --> ...
<!-- /AREA-LINK -->), placed after the first paragraph of the page's "Living in" section.
Idempotent — re-run after rebuilding any of these pages.
"""
import re

START, END = "<!-- AREA-LINK -->", "<!-- /AREA-LINK -->"
PERRY = '<a href="/neighborhoods/perry-township-indianapolis/">Perry Township area guide</a>'
CG = '<a href="/neighborhoods/center-grove-indiana/">Center Grove area guide</a>'
FT = '<a href="/neighborhoods/franklin-township-indianapolis/">Franklin Township area guide</a>'
DT = '<a href="/neighborhoods/decatur-township-indianapolis/">Decatur Township area guide</a>'
WAY = '<a href="/neighborhoods/wayne-township-indianapolis/">Wayne Township area guide</a>'
WASH = '<a href="/neighborhoods/washington-township-indianapolis/">Washington Township area guide</a>'
LAW = '<a href="/neighborhoods/lawrence-township-indianapolis/">Lawrence Township area guide</a>'
PIKE = '<a href="/neighborhoods/pike-township-indianapolis/">Pike Township</a>'

LINKS = {
 "cities/marion-county/southport-indiana-real-estate/index.html": f"Southport sits inside Indianapolis&rsquo;s Perry Township; for the wider south side, see our {PERRY}.",
 "cities/marion-county/homecroft-indiana-real-estate/index.html": f"Homecroft sits inside Indianapolis&rsquo;s Perry Township; for the wider south side, see our {PERRY}.",
 "cities/marion-county/beech-grove-indiana-real-estate/index.html": f"Beech Grove sits between Perry and Franklin townships on the south side; see our {PERRY} and {FT}.",
 "cities/johnson-county/greenwood-indiana-real-estate/index.html": f"Parts of western Greenwood are in the Center Grove school district; see our {CG}.",
 "cities/johnson-county/bargersville-indiana-real-estate/index.html": f"Most of Bargersville is in the Center Grove area of White River Township; see our {CG}.",
 "cities/marion-county/camby-indiana-real-estate/index.html": f"Much of Camby is in Decatur Township on Indianapolis&rsquo;s southwest side; see our {DT}.",
 "schools/perry-township-schools/index.html": f"For neighborhoods, prices and commutes across the district, see our {PERRY}.",
 "schools/center-grove-schools/index.html": f"For neighborhoods, prices and new construction across the district, see our {CG}.",
 "schools/franklin-township-schools/index.html": f"For neighborhoods, prices and commutes across the district, see our {FT}.",
 "cities/marion-county/speedway-indiana-real-estate/index.html": f"Speedway sits inside Wayne Township on Indianapolis&rsquo;s west side; for the surrounding neighborhoods, see our {WAY}.",
 "cities/marion-county/clermont-indiana-real-estate/index.html": f"Clermont straddles the {PIKE} and Wayne Township line on the west side; see our {WAY}.",
 "cities/marion-county/meridian-hills-indiana-real-estate/index.html": f"Meridian Hills is one of the small included towns inside Washington Township; for the wider north side, see our {WASH}.",
 "neighborhoods/broad-ripple-indianapolis/index.html": f"Broad Ripple is part of Washington Township on Indianapolis&rsquo;s north side; see our {WASH}.",
 "neighborhoods/meridian-kessler-indianapolis/index.html": f"Meridian-Kessler is part of Washington Township on Indianapolis&rsquo;s north side; see our {WASH}.",
 "neighborhoods/butler-tarkington-indianapolis/index.html": f"Butler-Tarkington is part of Washington Township on Indianapolis&rsquo;s north side; see our {WASH}.",
 "neighborhoods/nora-indianapolis/index.html": f"Nora is part of Washington Township on Indianapolis&rsquo;s north side; see our {WASH}.",
 "cities/marion-county/lawrence-indiana-real-estate/index.html": f"The City of Lawrence covers about two-fifths of Lawrence Township; for the wider northeast side, including Castleton and Geist, see our {LAW}.",
 "neighborhoods/castleton-indianapolis/index.html": f"Most of Castleton sits in Lawrence Township on the northeast side; see our {LAW}.",
 "schools/msd-washington-township/index.html": f"For neighborhoods, prices and commutes across the township, see our {WASH}.",
 "schools/msd-lawrence-township/index.html": f"For neighborhoods, prices and commutes across the district, see our {LAW}.",
 "schools/decatur-township-schools/index.html": f"For neighborhoods, prices and new construction across the district, see our {DT}.",
}

for path, sentence in LINKS.items():
    s = open(path, encoding="utf-8", newline="").read()
    block = f'{START}\n <p>{sentence}</p>\n{END}\n'
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda m: block, s, flags=re.S)
    else:
        m = re.search(r"<h2>Living in [^<]*</h2>", s)
        if not m:
            raise SystemExit("no Living section in " + path)
        end_p = s.index("</p>", m.end()) + len("</p>")
        nl = s.find("\n", end_p) + 1
        s = s[:nl] + block + s[nl:]
    open(path, "w", encoding="utf-8", newline="").write(s)
    print("linked", path)
