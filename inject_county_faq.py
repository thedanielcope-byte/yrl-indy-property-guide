#!/usr/bin/env python3
"""Add a "What county is <Town>, Indiana in?" FAQ to every city page (visible FAQ + FAQPage
JSON-LD). Targets the "what county is X in" searches where the city pages already rank on
page one (Fishers, Noblesville, Lawrence, Carmel, Zionsville, Greenwood...). Idempotent:
the visible answer sits between <!-- COUNTY-FAQ --> markers and the JSON-LD question is
replaced, not duplicated. Re-run after rebuilding city pages.

Answers are verified (Nov 2026). Multi-county towns: Cumberland (Marion/Hancock), Geist
(Marion/Hamilton), Shirley (Hancock/Henry), Elwood (Madison/Tipton), Chesterfield
(Madison/Delaware). County seats only where certain. Also corrects six quick-fact county
labels that were wrong (Plainfield is not the county seat; Mooresville is NE Morgan; New
Palestine is SW Hancock) or missed a second county.
"""
import glob, html, json, re

START, END = "<!-- COUNTY-FAQ -->", "<!-- /COUNTY-FAQ -->"

SEATS = {"noblesville": "Hamilton", "franklin": "Johnson", "shelbyville": "Shelby", "greenfield": "Hancock",
         "danville": "Hendricks", "lebanon": "Boone", "anderson": "Madison", "martinsville": "Morgan",
         "columbus": "Bartholomew", "greensburg": "Decatur", "nashville": "Brown", "greencastle": "Putnam",
         "rockville": "Parke", "crawfordsville": "Montgomery"}
INDY = {"broad-ripple", "irvington", "eagle-creek", "camby"}            # parts of Indianapolis
MARION_TOWNS = {"beech-grove", "southport", "speedway", "lawrence", "homecroft", "meridian-hills", "clermont"}
SPECIAL = {
 "cumberland": "Cumberland straddles the county line on Indianapolis&rsquo;s east side: the western part is in Marion County and the eastern part is in Hancock County.",
 "geist": "Geist is a lake community on Geist Reservoir that spans two counties: the south shore is in Marion County (Lawrence Township) and the north shore is in Hamilton County (Fishers).",
 "shirley": "Shirley is mostly in Hancock County. Main Street is the county line, and the smaller east side of town is in Henry County.",
 "elwood": "Elwood is in Madison County, with a very small part of the city in neighboring Tipton County.",
 "chesterfield": "Chesterfield is mostly in Madison County, with a small portion extending east into Delaware County.",
 "edinburgh": "Edinburgh is in Johnson County, in the county&rsquo;s southeast corner near the Bartholomew and Shelby county lines.",
}
LABEL_FIX = {   # quick-facts "County" value corrections: slug -> (old, new)
 "plainfield": ("Hendricks County Seat", "Hendricks County"),
 "mooresville": ("SE Morgan County", "NE Morgan County"),
 "new-palestine": ("SE Hancock County", "SW Hancock County"),
 "shirley": ("E Hancock County", "Hancock &amp; Henry Co."),
 "elwood": ("N Madison County", "Madison &amp; Tipton Co."),
 "chesterfield": ("Madison County", "Madison &amp; Delaware Co."),
}


def town_name(s, slug):
    t = re.search(r"<h1>(.*?)</h1>", s, re.S)
    raw = html.unescape(re.sub(r"<[^>]+>", " ", t.group(1))) if t else ""
    m = re.match(r"\s*([A-Z][\w.'’ -]+?)(?:,| Indiana| Indianapolis| Real Estate| Homes)", raw)
    return m.group(1).strip() if m else slug.replace("-", " ").title()


def answer(slug, town, county):
    if slug in SPECIAL:
        return SPECIAL[slug]
    if slug in INDY:
        return f"{town} is in Marion County. It&rsquo;s part of the City of Indianapolis."
    if slug in MARION_TOWNS:
        return f"{town} is in Marion County, inside the Indianapolis area but with its own local government."
    if slug in SEATS:
        return f"{town} is in {county} County, and it&rsquo;s the county seat."
    return f"{town} is in {county} County, Indiana."


n = 0
for path in sorted(glob.glob("cities/*/*/index.html")):
    county_slug = path.split("/")[1]
    slug = re.sub(r"-(indiana|indianapolis)-real-estate$", "", path.split("/")[2])
    county = county_slug.replace("-county", "").replace("-", " ").title()
    s = open(path, encoding="utf-8").read()
    if "<section class=\"faq-section\">" not in s:
        print("  skip (no FAQ section)", path); continue
    town = town_name(s, slug)
    q = f"What county is {town}, Indiana in?"
    a = answer(slug, town, county)
    county_url = f"/counties/{county_slug}-indiana-real-estate/"
    link = f' See our <a href="{county_url}">{county} County real estate guide</a>.' if slug not in SPECIAL else ""
    block = (f'{START}\n <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n'
             f' <p>{a}{link}</p>\n </div>\n </details>\n {END}\n')
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, flags=re.S)
    sec = s.index('<section class="faq-section">')
    close = s.index("</section>", sec)
    s = s[:close] + block + " " + s[close:]
    # JSON-LD FAQPage
    def fix_ld(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        nodes = d.get("@graph", [d]) if isinstance(d, dict) else []
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                me = [x for x in node.get("mainEntity", []) if not str(x.get("name", "")).startswith("What county is ")]
                me.append({"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r"<[^>]+>", "", a))}})
                node["mainEntity"] = me
                return '<script type="application/ld+json">\n' + json.dumps(d, indent=1, ensure_ascii=False) + '\n</script>'
        return m.group(0)
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, s, flags=re.S)
    if slug in LABEL_FIX:
        old, new = LABEL_FIX[slug]
        s = s.replace(f"<dt>County</dt><dd>{old}</dd>", f"<dt>County</dt><dd>{new}</dd>")
    open(path, "w", encoding="utf-8").write(s)
    n += 1
print("county FAQ on", n, "city pages")
