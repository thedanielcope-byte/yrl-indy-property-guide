#!/usr/bin/env python3
"""Search-snippet overrides (title + meta description) for pages that rank on page one
but get few clicks (from Search Console, Nov 2026). Applied to the finished HTML after the
generators run, so a rebuild can't undo them: title, og:title, twitter:title, description,
og:description, twitter:description. Idempotent. Runs in the GitHub Actions after
inject_gtag.py. Also adds a "Search MIBOR listings" call to action on the MIBOR glossary
page (people search "mibor", "mibor listings", "mibor property search").

Descriptions lead with the answer and only say what the page itself says.
"""
import html, re

SUFFIX = " | Your Realty Link"
OVERRIDES = {
 "compare/greenwood-vs-franklin-vs-zionsville/": (
  "Greenwood vs Franklin vs Zionsville: Which Town Is Best?",
  "Greenwood for the shortest commute and shopping, Franklin for small-town value from the $200s, Zionsville for a brick-street village from the mid-$400s."),
 "compare/greenwood-vs-franklin/": (
  "Greenwood vs Franklin, Indiana: Which Is Better for You?",
  "Greenwood for a ~15-minute commute and Center Grove schools; Franklin for value from the $200s and a real courthouse-square town. Compared side by side."),
 "compare/carmel-vs-westfield/": (
  "Carmel vs Westfield, Indiana: Which Suburb Is Better?",
  "Carmel for walkability and resale prestige; Westfield for newer homes and more house per dollar. Prices, schools, commute and lifestyle compared."),
 "compare/zionsville-vs-carmel/": (
  "Zionsville vs Carmel, Indiana: Which Suburb Is Better?",
  "Same price tier, different feel: Zionsville is a historic brick-street village of about 30,000; Carmel is a city of about 110,000 with more shopping and homes."),
 "glossary/mibor/": (
  "MIBOR: What It Is and How to Search MIBOR Listings",
  "MIBOR is the Indianapolis-area REALTOR association that runs the Central Indiana MLS. What it does, and how to search every active MIBOR listing free."),
 "glossary/earnest-money-receipt/": (
  "Earnest Money Receipt: What It Is and Who Holds It",
  "An earnest money receipt confirms your deposit was received, how much, and who holds it, usually the title company or listing brokerage. Why to keep it."),
 "glossary/common-area/": (
  "Common Area Meaning: What Counts as an HOA Common Area",
  "A common area is shared community property owned by HOA members, like pools, sidewalks and clubhouses. What's included and how it works in Central Indiana."),
 "glossary/model-home/": (
  "What Is a Model Home? Meaning and What to Watch For",
  "A model home is a builder's finished, decorated showcase of a floor plan, usually with upgrades beyond the base price. How to tell standard from extra."),
 "glossary/transfer-tax/": (
  "Does Indiana Have a Real Estate Transfer Tax? (No)", None),
 "services/free-home-valuation/": (
  "What's My Home Worth? Free Indianapolis Home Valuation",
  "How much is your house worth? Get a free, local home valuation (CMA) for Indianapolis, Hamilton, Johnson and Hendricks counties from Your Realty Link."),
 "best/small-towns-near-indianapolis/": (
  "Best Small Towns Near Indianapolis, 25 to 35 Minutes Out",
  "Zionsville, Danville, Pittsboro, Lebanon, Fortville and Cicero: real main streets about 25 to 35 minutes from downtown Indianapolis. Prices compared."),
 "cities/marion-county/southport-indiana-real-estate/": (
  "Southport, IN Real Estate and Homes for Sale",
  "Southport, IN real estate on Indy's south side: affordable homes, easy I-65 access and Perry Township schools. Search Southport homes or get a valuation."),
}

MIBOR_CTA = ('<!-- MIBOR-CTA -->\n <div class="info-box"><strong>Search MIBOR listings:</strong> browse every active MIBOR MLS listing '
             'in Indianapolis and Central Indiana, updated daily, on our <a href="/search/">home search</a>.</div>\n<!-- /MIBOR-CTA -->\n')


def attr(s):
    return html.escape(s, quote=False).replace('"', "&quot;")


def full_title(t):
    return t + SUFFIX if len(t + SUFFIX) <= 62 else t


n = 0
for path, (title, desc) in OVERRIDES.items():
    f = path + "index.html"
    s = open(f, encoding="utf-8").read(); s0 = s
    T = attr(full_title(title))
    s = re.sub(r"<title>.*?</title>", f"<title>{T}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + T, s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + T, s, count=1)
    if desc:
        assert len(desc) <= 160, (path, len(desc))
        D = attr(desc)
        for pat in (r'(<meta name="description" content=")[^"]*', r'(<meta property="og:description" content=")[^"]*',
                    r'(<meta name="twitter:description" content=")[^"]*'):
            s = re.sub(pat, lambda m: m.group(1) + D, s, count=1)
    if path == "glossary/mibor/":
        s = re.sub(r"<!-- MIBOR-CTA -->.*?<!-- /MIBOR-CTA -->\n", "", s, flags=re.S)
        m = re.search(r"<!-- QA-END -->\n", s) or re.search(r'<div class="quick-answer">.*?</dl>\s*</div>\n?', s, re.S)
        if m:
            s = s[:m.end()] + MIBOR_CTA + s[m.end():]
    if s != s0:
        open(f, "w", encoding="utf-8").write(s); n += 1
print("snippet overrides applied to", n, "pages")
