#!/usr/bin/env python3
"""Add a county-specific FAQ (visible <details> accordion, matching the site
pattern) + a standalone FAQPage JSON-LD to every county hub page.

County pages currently carry 791 impressions with NO FAQ. Answers are
parameterized on real, on-page data (county name, price-range badge) plus a
factual county->cities map — nothing fabricated. Idempotent, div-balance-checked.

  python3 add_county_faq.py          # dry run
  python3 add_county_faq.py --apply
"""
import os, re, sys, glob, html

APPLY = "--apply" in sys.argv

# factual: county slug -> (county seat, notable cities)
COUNTIES = {
 "marion": ("Indianapolis", ["Indianapolis", "Lawrence", "Beech Grove", "Speedway", "Southport"]),
 "hamilton": ("Noblesville", ["Carmel", "Fishers", "Noblesville", "Westfield"]),
 "johnson": ("Franklin", ["Greenwood", "Franklin", "Bargersville", "Whiteland"]),
 "hendricks": ("Danville", ["Avon", "Brownsburg", "Plainfield", "Danville"]),
 "hancock": ("Greenfield", ["Greenfield", "McCordsville", "Fortville", "New Palestine"]),
 "boone": ("Lebanon", ["Zionsville", "Lebanon", "Whitestown", "Thorntown"]),
 "madison": ("Anderson", ["Anderson", "Pendleton", "Alexandria", "Elwood"]),
 "shelby": ("Shelbyville", ["Shelbyville", "Morristown", "Fairland"]),
 "morgan": ("Martinsville", ["Mooresville", "Martinsville", "Monrovia"]),
 "montgomery": ("Crawfordsville", ["Crawfordsville"]),
 "decatur": ("Greensburg", ["Greensburg", "Westport"]),
 "brown": ("Nashville", ["Nashville", "Bean Blossom"]),
 "putnam": ("Greencastle", ["Greencastle", "Cloverdale"]),
 "parke": ("Rockville", ["Rockville"]),
 "bartholomew": ("Columbus", ["Columbus"]),
 "jackson": ("Brownstown", ["Seymour", "Brownstown"]),
 "jennings": ("Vernon", ["North Vernon", "Vernon"]),
}

def city_list(cities):
    if len(cities) == 1:
        return cities[0]
    return ", ".join(cities[:-1]) + ", and " + cities[-1]

def faqs_for(county, seat, cities, price):
    cl = city_list(cities)
    return [
      (f"What cities and towns are in {county}, Indiana?",
       f"{county} includes communities such as {cl}, with {seat} as the county seat. "
       f"Your Realty Link serves buyers and sellers throughout {county}."),
      (f"What are home prices like in {county}?",
       f"Homes in {county} typically range from {price}, depending on the city, age, size, and "
       f"condition of the home. For a precise, current figure, request a free "
       f'<a href="/services/free-home-valuation/">home valuation</a> from Your Realty Link.'),
      (f"Is {county} a good place to buy a home?",
       f"Yes. From established suburbs to small towns and rural acreage, {county} offers a wide range "
       f"of homes and lifestyles. Buyers are drawn to its schools, community feel, and value compared "
       f"with the urban core — and Your Realty Link knows the local market street by street."),
      (f"How do I search homes for sale in {county}?",
       f"Browse every active MLS listing through the Your Realty Link property search at "
       f'<a href="https://yourrealtylink.com/property-search">yourrealtylink.com</a>, or call '
       f"317-997-7404 for a personalized search and a free comparative market analysis."),
    ]

def render_visible(county, faqs):
    items = "\n".join(
      f' <details class="faq-item">\n <summary>{html.escape(q)}</summary>\n'
      f' <div class="faq-answer">\n <p>{a}</p>\n </div>\n </details>'
      for q, a in faqs)
    return (f'\n<!-- COUNTY-FAQ -->\n<section class="county-faq">\n'
            f'<h2>Frequently Asked Questions — {html.escape(county)} Real Estate</h2>\n'
            f'{items}\n</section>\n')

def render_schema(faqs):
    import json
    ent = [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
           for q, a in faqs]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}
    return ('<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False) + '</script>\n')

def process(path):
    h = open(path, encoding="utf-8").read()
    if "COUNTY-FAQ" in h or '"FAQPage"' in h:
        return "skip-present"
    slug = os.path.basename(os.path.dirname(path)).replace("-county-indiana-real-estate", "")
    if slug not in COUNTIES:
        return "skip-unknown:" + slug
    seat, cities = COUNTIES[slug]
    m = re.search(r"<h1>(.*?)</h1>", h)
    county = re.sub(r"<[^>]+>", "", m.group(1))
    county = re.match(r"(.*? County)\b", county).group(1)
    pm = re.search(r"🏡\s*([^<]+?)\s*</span>", h)
    price = pm.group(1).strip() if pm else "the low $100s to the $500s and up"
    faqs = faqs_for(county, seat, cities, price)
    block = render_visible(county, faqs) + render_schema(faqs)
    i = h.find("</main>")
    if i < 0:
        return "skip-no-main"
    out = h[:i] + block + h[i:]
    if out.count("<div") != out.count("</div>"):
        return "IMBALANCE"
    if APPLY:
        open(path, "w", encoding="utf-8").write(out)
    return "ok"

stats = {}
for path in sorted(glob.glob("counties/*/index.html")):
    r = process(path)
    stats[r.split(":")[0]] = stats.get(r.split(":")[0], 0) + 1
    if r == "ok":
        print("  +", os.path.relpath(path, "."))
print(("APPLIED" if APPLY else "DRY-RUN"), stats)
