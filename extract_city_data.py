#!/usr/bin/env python3
"""Extract per-city guide data (county, price, schools, commute) from the built
city pages' 'at a glance' box, for every city not already hand-curated. Writes
city_guides_auto.json into the repo (merged by city_guides_data.py)."""
import os, re, html, json, glob, sys

REPO = "/Users/danielcope/Library/Mobile Documents/com~apple~CloudDocs/Claude/YRL/indypropertyguide"
os.chdir(REPO)
sys.path.insert(0, REPO)
from city_guides_data import CITIES as HAVE

def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()

def price_phrase(raw):
    raw = clean(raw).replace("—", "–").replace("-", "–")
    if "–" in raw:
        lo, hi = [x.strip() for x in raw.split("–", 1)]
        return f"the {lo} to the {hi}"
    return f"around {raw}" if raw else "a range of price points"

def commute_phrase(raw):
    m = re.search(r"(\d+)", raw or "")
    return f"about {m.group(1)} minutes to downtown Indianapolis" if m else "a manageable drive to downtown Indianapolis"

DEFAULT_AREAS = ["established neighborhoods near the town center",
                 "newer subdivisions on the edge of town",
                 "quiet residential streets close to the schools",
                 "homes with a little more land just outside town"]

auto = {}
skipped = []
for page in sorted(glob.glob("cities/*/*/index.html")):
    d = os.path.dirname(page)
    slug_dir = os.path.basename(d)
    key = slug_dir.replace("-indiana-real-estate", "").replace("-indianapolis-real-estate", "")
    if key in HAVE:
        continue
    t = open(page, encoding="utf-8").read()
    facts = dict((clean(a), clean(b)) for a, b in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", t, re.S))
    h1 = re.search(r"<h1>(.*?)</h1>", t, re.S)
    name = re.split(r" Indiana(?:polis)? ", clean(h1.group(1)))[0].strip() if h1 else key.replace("-", " ").title()
    county = re.sub(r"^(N|S|E|W|NE|NW|SE|SW|Central|Northern|Southern|Eastern|Western)\s+", "", facts.get("County", ""))
    price = facts.get("Typical home prices", "")
    commute = facts.get("Drive to downtown Indy", "") or facts.get("Drive to downtown", "")
    schools = facts.get("School district", "")
    if not schools or schools.lower() in ("varies", "n/a", ""):
        m = re.search(r"[Ii]t'?s served by ([^.]+?)\.", t)   # from the qa-lead summary
        if m:
            schools = clean(m.group(1))
    if not schools or schools.lower() in ("varies", "n/a", ""):
        sm = re.search(r"<h2>Schools.*?</h2>(.*?)<h2", t, re.S)   # from the Schools section
        seg = clean(sm.group(1)) if sm else ""
        dm = re.search(r"([A-Z][A-Za-z.'&-]+(?:\s+[A-Z][A-Za-z.'&-]+){0,3}\s+(?:Community School Corporation|Consolidated School Corporation|School Corporation|Community Schools|Consolidated Schools|Schools))", seg)
        if dm:
            schools = dm.group(1).strip()
    if not (county and name):
        skipped.append(key); continue
    auto[key] = dict(
        name=name, county=county, url="/" + os.path.relpath(d, ".") + "/",
        price=price_phrase(price),
        schools=schools or "the local school district",
        areas=DEFAULT_AREAS,
        commute=commute_phrase(commute),
        character=f"a {county} community known for its local character, {(schools or 'good schools')}, and convenient access to the greater Indianapolis area")
json.dump(auto, open(os.path.join(REPO, "city_guides_auto.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("Extracted %d auto cities (hand-curated: %d, total will be %d)." % (len(auto), len(HAVE), len(auto)+len(HAVE)))
if skipped:
    print("skipped (missing data):", skipped)
print("\nSample entries:")
for k in list(auto)[:3]:
    a = auto[k]
    print(f"  {k}: {a['name']} | {a['county']} | price={a['price']} | schools={a['schools']} | commute={a['commute']}")
