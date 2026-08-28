#!/usr/bin/env python3
"""Build the School Districts hub + per-district and per-private-school detail
pages from schools.json. Mirrors the hand-authored district page
(schools/center-grove-schools/) and generates detail pages ONLY for slugs whose
directory does not already exist — so the 10 rich hand-authored district pages
are preserved. Header/footer/fonts are regex-grabbed from index.html so the nav
stays in sync. Deep-links every district/school to the cities it serves + its
county, and uses idx_config for the pre-filtered MLS search CTA.

    python3 build_schools.py
"""
import os, re, html, glob, json
import idx_config as idx

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "schools.json"), encoding="utf-8"))
SCHOOLS = DATA["districts"]

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS  = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

def esc(s):  return html.escape(str(s or ""), quote=False)
def plain(t): return re.sub(r"<[^>]+>", "", str(t)).replace("&amp;", "&").replace("&mdash;", "-").replace("&rsaquo;", ">").replace("&#8599;", "").strip()

# city -> city-page url
CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def city_url(city):
    kebab = city.strip().lower().replace(" ", "-").replace(".", "").replace("'", "").replace("’", "")
    for d in CITY_DIRS:
        base = os.path.basename(d.rstrip(os.sep))
        if base.startswith(kebab + "-"):
            cslug = os.path.basename(os.path.dirname(d.rstrip(os.sep)))
            return "/cities/%s/%s/" % (cslug, base)
    return None
def county_url(county):
    if not county: return None
    slug = county.strip().lower().replace(" ", "-") + "-county-indiana-real-estate"
    return "/counties/%s/" % slug if os.path.isdir(os.path.join(ROOT, "counties", slug)) else None
def city_link(city):
    u = city_url(city)
    return '<a href="%s">%s</a>' % (u, esc(city)) if u else esc(city)

def natjoin(items):
    items = [i for i in items if i]
    if not items: return ""
    if len(items) == 1: return items[0]
    return ", ".join(items[:-1]) + ", and " + items[-1]

# approximate price bands (CLAUDE.md tier guide) by city; primary city drives it
BAND = {
 "Carmel":"$400s to $1M+","Zionsville":"$400s to $1M+","Geist":"$350s to $900s+",
 "Fishers":"$300s to $600s","Westfield":"$300s to $600s","Noblesville":"$300s to $600s",
 "Whitestown":"$300s to $550s","Broad Ripple":"$250s to $600s",
 "McCordsville":"$280s to $500s","New Palestine":"$280s to $500s",
 "Greenwood":"$250s to $450s","Avon":"$250s to $450s","Brownsburg":"$250s to $450s",
 "Whiteland":"$250s to $400s","Lebanon":"$230s to $420s",
 "Plainfield":"$230s to $400s","Danville":"$230s to $400s","Bargersville":"$230s to $400s",
 "Franklin":"$230s to $400s","Eagle Creek":"$200s to $450s",
 "Mooresville":"$200s to $380s","Martinsville":"$200s to $380s","Pendleton":"$200s to $380s",
 "Cicero":"$200s to $400s","Arcadia":"$200s to $400s","Atlanta":"$200s to $400s","Sheridan":"$200s to $400s",
 "Lawrence":"$150s to $320s","Beech Grove":"$150s to $320s","Southport":"$150s to $320s",
 "Irvington":"$150s to $350s","Speedway":"$150s to $300s",
 "Shelbyville":"$150s to $300s","Greenfield":"$150s to $300s","Anderson":"$150s to $300s",
}
def band(city): return BAND.get(city, "$150s to $300s")

def search_url(city): return idx.city_search_url(city)

# ── FAQ ──────────────────────────────────────────────────────────────────────
def faq_schema(pairs):
    return ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
                      % (json.dumps(plain(q)), json.dumps(plain(a))) for q, a in pairs)
def faq_html(pairs):
    return "\n".join('<details class="faq-item">\n<summary>%s</summary>\n<div class="faq-answer"><p>%s</p></div>\n</details>' % (esc(q), a) for q, a in pairs)

# ── shared skeleton ──────────────────────────────────────────────────────────
def page(rec, title, meta, hero_sub, badges, intro, sections, cta_city, faqs,
         explore, quick_facts, related, crumb):
    slug = rec["slug"]; url = "https://janetgiles.com/schools/%s/" % slug
    fh = faq_html(faqs); fs = faq_schema(faqs)
    badges_html = "\n ".join(badges)
    sec_html = "\n\n ".join(sections)
    explore_items = "\n ".join(explore)
    qf = "\n".join(quick_facts)
    rel = "\n ".join(related)
    formid = slug.replace("-", "")[:24]
    search = search_url(cta_city)
    h1b = rec["_h1b"]
    h1 = esc(rec["_h1a"]) + ((" <em>%s</em>" % esc(h1b)) if h1b else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(title)}</title>
 <meta name="description" content="{esc(meta)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="{esc(title)}">
 <meta property="og:description" content="{esc(meta)}">
 <meta property="og:url" content="{url}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "{esc(cta_city)}, Indiana" }},
 {{ "@type": "FAQPage", "mainEntity": [ {fs} ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "School Districts", "item": "https://janetgiles.com/schools/" }},
 {{ "@type": "ListItem", "position": 3, "name": "{esc(plain(crumb))}", "item": "{url}" }} ] }}
 ] }}
 </script>
 {FONTS}
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/schools/">School Districts</a> <span>&rsaquo;</span> {crumb}</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>{h1}</h1>
 <p class="hero-sub">{hero_sub}</p>
 <div class="hero-badges">
 {badges_html}
 </div><p class="hero-reviewed">✔ Reviewed by <a href="/agents/janet-giles/">Janet Giles-Schultz</a>, Principal Broker · MIBOR member · Updated August 2026</p>
 </div>
</section>

<div class="container">
 <div class="content-wrap">
 <main class="content-main">

 {intro}

 {sec_html}

 <div class="cta-block">
 <h3>Ready to Search Homes Here?</h3>
 <p>Browse active MLS listings across the area — updated continuously from the MIBOR MLS.</p>
 <div class="btn-group">
 <a href="{search}" class="btn btn-white" target="_blank" rel="noopener">Search Homes for Sale →</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline" target="_blank" rel="noopener">Get a Free Home Valuation</a>
 <a href="/schedule/" class="btn btn-outline">📅 Schedule a Free Consultation</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Frequently Asked Questions</h2>
{fh}
 </section>

 <div class="cta-block cta-block-light">
 <h3>Thinking About Selling?</h3>
 <p>Get a free, no-obligation home valuation from Your Realty Link — we'll show you exactly what your home is worth in today's market.</p>
 <div class="btn-group">
 <a href="/services/free-home-valuation/" class="btn btn-primary" target="_blank" rel="noopener">Get a Free Valuation</a>
 <a href="/contact/" class="btn btn-outline">Contact Your Realty Link</a>
 </div>
 </div>

 <hr class="divider">
 <h3>Explore More Central Indiana Real Estate</h3>
 <ul>
 {explore_items}
 </ul>

 </main>

 <aside class="content-sidebar">
  <div class="sidebar-card">
 <div class="sidebar-card-header">Get in Touch</div>
 <div class="sidebar-card-body">
 <p>Questions about homes in this area? Fill out this quick form and we'll reach out.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="schools/{slug}">
 <input type="hidden" name="interest_type" value="Buy a Home">
 <label for="sf-name-{formid}">Name *</label>
 <input type="text" id="sf-name-{formid}" name="name" required placeholder="Your name">
 <label for="sf-phone-{formid}">Phone *</label>
 <input type="tel" id="sf-phone-{formid}" name="phone" required placeholder="317-555-1234">
 <label for="sf-email-{formid}">Email *</label>
 <input type="email" id="sf-email-{formid}" name="email" required placeholder="you@example.com">
 <button type="submit">Connect With an Agent →</button>
 <p class="form-note">No spam · No obligation · We respond personally</p>
 </form>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Search Homes</div>
 <div class="sidebar-card-body">
 <p>Browse active MLS listings in the area — updated continuously from the MIBOR MLS.</p>
 <a href="{search}" class="btn btn-primary btn-sm btn-full" target="_blank" rel="noopener">Search All Listings →</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline btn-sm btn-full" target="_blank" rel="noopener">Free Home Valuation</a>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Quick Facts</div>
 <div class="sidebar-card-body">
 <ul class="contact-list">
{qf}
 </ul>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Related</div>
 <div class="sidebar-card-body" style="padding:12px;">
 {rel}
 </div>
 </div>

 </aside>
 </div>
</div>

{FOOTER}

{SCRIPTS}'''

# ── public district detail ───────────────────────────────────────────────────
def district_page(rec):
    name = rec["name"]; short = rec["short_name"]; county = rec["county"]
    cities = rec["cities"]; prim = cities[0]; gs = rec["grade_span"]
    bnote = rec.get("boundary_note")
    rec["_h1a"] = name; rec["_h1b"] = "Homes for Sale"
    cou = county_url(county); pb = band(prim)
    served = natjoin([city_link(c) for c in cities])
    prim_link = city_link(prim)
    cou_link = ('<a href="%s">%s County</a>' % (cou, esc(county))) if cou else ("%s County" % esc(county))
    bsent = (" " + bnote) if bnote else ""

    hero_sub = ("Buying or selling a home in the %s district? Your Realty Link helps buyers and sellers "
                "throughout %s and the surrounding %s County area." % (esc(short), esc(prim), esc(county)))
    badges = [
      '<span class="hero-badge">📍 %s County</span>' % esc(county),
      '<span class="hero-badge">🏡 %s</span>' % esc(pb),
      '<span class="hero-badge">🎓 %s public schools</span>' % esc(gs),
      '<span class="hero-badge">🏫 %s</span>' % esc(prim),
    ]
    intro = ("<p>If you're searching for a home in the <strong>%s school district</strong>, you're focused on "
             "one of the areas families ask about most across %s. %s serves %s.%s Your Realty Link is an "
             "Indianapolis-based MIBOR brokerage helping buyers and sellers throughout the area — and because "
             "attendance boundaries can shift with growth, we'll help you confirm which schools serve any "
             "specific address before you buy.</p>"
             % (esc(short), cou_link, esc(name), served, bsent))
    sections = [
      ("<h2>Living in the %s Area</h2>\n <p>The %s area blends everyday convenience with a family-focused, "
       "community feel. Residents are close to the shopping, dining, and services of %s while enjoying "
       "established neighborhood streets, parks, and an active local sports and school scene. Neighborhoods "
       "range from mature, tree-lined subdivisions to newer communities with sidewalks and amenities — a "
       "practical, welcoming place where many families settle in for the schools and stay for the community."
       % (esc(short), esc(short), esc(prim))),
      ("<h2>%s Area Home Prices &amp; Real Estate Market</h2>\n <p>Homes across the %s area generally range "
       "from %s, depending on the specific home, size, updates, and lot. Because so many buyers prioritize "
       "the district, well-maintained homes at fair prices tend to attract steady interest. Buyers should be "
       "pre-approved and ready to move, and sellers benefit from professional pricing and marketing. A Your "
       "Realty Link agent can break down conditions in the specific neighborhoods you're targeting."
       % (esc(short), esc(short), esc(pb))),
      ('<div class="info-box">\n <strong>Thinking about selling in the %s area?</strong> Your Realty Link '
       'provides free comparative market analyses for homeowners across %s County. '
       '<a href="/services/free-home-valuation/" target="_blank" rel="noopener">Get your free home valuation →</a>\n </div>'
       % (esc(short), esc(county))),
      ("<h2>About %s</h2>\n <p>%s is the public school district serving this area, offering a full %s path "
       "and a reputation that factors heavily into local home demand.%s We don't publish specific ratings or "
       "test scores here, since those figures change from year to year — and because boundaries can change "
       "with growth, always confirm the current attendance area for any specific address before you buy. A "
       "Your Realty Link agent can help you verify which schools serve a home."
       % (esc(name), esc(name), esc(gs), bsent)),
      ("<h2>Commute &amp; Location</h2>\n <p>The %s area offers convenient access to the wider Indianapolis "
       "metro, with nearby highways and commuter routes connecting residents to downtown, employment "
       "corridors, shopping, and dining. For buyers who want this district with a manageable commute, the "
       "location is a major part of the appeal." % esc(short)),
      ("<h2>Work With a %s Area Real Estate Agent</h2>\n <p>Your Realty Link is your local resource for homes "
       "in the %s district. <strong>Our team</strong> helps buyers and sellers throughout %s and %s. Whether "
       "you're relocating for the schools, buying your first home, or selling in a competitive district, we "
       "bring local knowledge, a proven marketing plan, and full access to the MIBOR MLS. Because attendance "
       "areas matter here, we'll help you confirm boundaries, compare neighborhoods, and price or negotiate "
       "with confidence." % (esc(short), esc(short), prim_link, cou_link)),
    ]
    faqs = [
      ("Do homes in the %s district cost more?" % esc(short),
       "Homes in the %s area generally range from %s. The district's popularity supports steady resale demand, and larger or newer homes reach the upper end of that range." % (esc(short), esc(pb))),
      ("How do I find homes in the %s boundary?" % esc(short),
       'Use the <a href="%s" target="_blank" rel="noopener">Your Realty Link property search</a> to browse active MLS listings in the area, then have an agent confirm the exact attendance area for any address — assignment depends on the specific property.' % search_url(prim)),
      ("What grades does %s serve?" % esc(short),
       "%s is a %s public school district. Specific school assignments depend on your address, which a Your Realty Link agent can help you confirm." % (esc(name), esc(gs))),
      ("Is the %s area a good place to buy a home?" % esc(short),
       "Yes — the %s area draws buyers for its schools, established and newer neighborhoods, and convenient access across %s County. It's a popular choice for families." % (esc(short), esc(county))),
    ]
    explore = []
    for c in cities:
        u = city_url(c)
        if u: explore.append('<li><a href="%s">%s, Indiana Real Estate</a></li>' % (u, esc(c)))
    if cou: explore.append('<li><a href="%s">%s County Real Estate Overview</a></li>' % (cou, esc(county)))
    explore.append('<li><a href="/schools/">All Central Indiana School District Guides</a></li>')
    explore.append('<li><a href="/communities/">Communities &amp; Subdivisions</a></li>')
    quick_facts = [
      '<li><span class="icon">🏛</span> <strong>County:</strong> %s</li>' % esc(county),
      '<li><span class="icon">📍</span> <strong>Serves:</strong> %s</li>' % esc(", ".join(cities[:3])),
      '<li><span class="icon">🏡</span> <strong>Prices:</strong> %s</li>' % esc(pb),
      '<li><span class="icon">🎓</span> <strong>Type:</strong> %s public district</li>' % esc(gs),
    ]
    related = []
    pu = city_url(prim)
    if pu: related.append('<a href="%s" class="city-card">%s Real Estate <span class="arrow">&rsaquo;</span></a>' % (pu, esc(prim)))
    if cou: related.append('<a href="%s" class="city-card">%s County Homes <span class="arrow">&rsaquo;</span></a>' % (cou, esc(county)))
    related.append('<a href="/schools/" class="city-card">All School Districts <span class="arrow">&rsaquo;</span></a>')
    title = "%s Homes for Sale | Your Realty Link" % short
    meta = ("Searching %s homes for sale? Your Realty Link helps buyers and sellers in the %s area, %s County. Get a free valuation." % (esc(short), esc(prim), esc(county)))
    return page(rec, title, meta, hero_sub, badges, intro, sections, prim, faqs,
                explore, quick_facts, related, esc(name))

# ── private school detail ────────────────────────────────────────────────────
def private_page(rec):
    name = rec["name"]; city = rec["city"]; county = rec["county"]
    gs = rec["grade_span"]; aff = rec.get("affiliation") or "private"
    rec["_h1a"] = "Homes Near %s" % name; rec["_h1b"] = ""
    cou = county_url(county); pb = band(city); prim_link = city_link(city)
    cou_link = ('<a href="%s">%s County</a>' % (cou, esc(county))) if cou else ("%s County" % esc(county))

    hero_sub = ("Looking for a home near %s? This %s school (%s) is in %s. Your Realty Link helps families "
                "buy and sell homes throughout the %s area." % (esc(name), esc(aff), esc(gs), esc(city), esc(city)))
    badges = [
      '<span class="hero-badge">📍 %s · %s County</span>' % (esc(city), esc(county)),
      '<span class="hero-badge">🎓 %s (%s)</span>' % (esc(gs), esc(aff)),
      '<span class="hero-badge">🏡 %s</span>' % esc(pb),
      '<span class="hero-badge">🏫 Private school</span>',
    ]
    intro = ("<p>Families who prioritize <strong>%s</strong> often want to live nearby in %s. %s is a %s "
             "school (%s) in %s, %s. Your Realty Link is an Indianapolis-based MIBOR brokerage that helps "
             "buyers and sellers throughout the %s area — if being close to this school matters to you, we'll "
             "help you find the right neighborhood and confirm commute and enrollment details. (Admissions and "
             "enrollment are handled by the school directly; we help with the home.)</p>"
             % (esc(name), prim_link, esc(name), esc(aff), esc(gs), esc(city), cou_link, esc(city)))
    sections = [
      ("<h2>Living Near %s</h2>\n <p>The %s area around %s offers a mix of established and newer neighborhoods "
       "with convenient access to shopping, dining, parks, and major commuter routes. For families choosing a "
       "private-school setting, proximity, drive time, and neighborhood fit all matter — and %s has a range of "
       "housing options within a reasonable radius of the school."
       % (esc(name), esc(city), esc(name), esc(city))),
      ("<h2>Homes &amp; Real Estate Near %s</h2>\n <p>Homes in the %s area generally range from %s, depending "
       "on the specific home, size, and updates. Whether you're buying to be near %s or selling a nearby home, "
       "a local agent's read on value helps. Ask Your Realty Link for a free, no-obligation market analysis "
       "for any address in the area." % (esc(name), esc(city), esc(pb), esc(name))),
      ('<div class="info-box">\n <strong>Selling a home near %s?</strong> Your Realty Link provides free '
       'comparative market analyses for homeowners across %s County. '
       '<a href="/services/free-home-valuation/" target="_blank" rel="noopener">Get your free home valuation →</a>\n </div>'
       % (esc(name), esc(county))),
      ("<h2>About %s</h2>\n <p>%s is a %s school serving grades %s in %s. Private and parochial schools set "
       "their own admissions, tuition, and enrollment policies, so confirm current details with the school "
       "directly. Many families also weigh the assigned public district when choosing a home — see our "
       '<a href="/schools/">Central Indiana school district guides</a> to compare the public options that '
       "serve %s." % (esc(name), esc(name), esc(aff), esc(gs), esc(city), prim_link)),
      ("<h2>Work With a %s Area Real Estate Agent</h2>\n <p>Your Realty Link helps buyers and sellers "
       "throughout %s and %s. <strong>Our team</strong> knows the neighborhoods near %s and can help you "
       "balance location, commute, and value. Whether you're buying to be close to the school or selling a "
       "nearby home, we bring local knowledge, a proven marketing plan, and full access to the MIBOR MLS."
       % (esc(city), prim_link, cou_link, esc(name))),
    ]
    faqs = [
      ("What are home prices like near %s?" % esc(name),
       "Homes in the %s area generally range from %s, depending on the home, size, and updates. Your Realty Link can provide a free market analysis for any nearby address." % (esc(city), esc(pb))),
      ("How do I find homes for sale near %s?" % esc(name),
       'Use the <a href="%s" target="_blank" rel="noopener">Your Realty Link property search</a> to browse active MLS listings in %s and the surrounding area, all pulled from the MIBOR MLS.' % (search_url(city), esc(city))),
      ("Does buying a home near %s guarantee enrollment?" % esc(name),
       "No — %s is a private (%s) school that sets its own admissions and enrollment policies, independent of where you live. Confirm enrollment details with the school directly; Your Realty Link helps with the home." % (esc(name), esc(aff))),
    ]
    explore = []
    pu = city_url(city)
    if pu: explore.append('<li><a href="%s">%s, Indiana Real Estate</a></li>' % (pu, esc(city)))
    if cou: explore.append('<li><a href="%s">%s County Real Estate Overview</a></li>' % (cou, esc(county)))
    explore.append('<li><a href="/schools/">All Central Indiana School District Guides</a></li>')
    explore.append('<li><a href="/communities/">Communities &amp; Subdivisions</a></li>')
    quick_facts = [
      '<li><span class="icon">🏛</span> <strong>County:</strong> %s</li>' % esc(county),
      '<li><span class="icon">📍</span> <strong>City:</strong> %s</li>' % esc(city),
      '<li><span class="icon">🎓</span> <strong>Grades:</strong> %s (%s)</li>' % (esc(gs), esc(aff)),
      '<li><span class="icon">🏡</span> <strong>Nearby prices:</strong> %s</li>' % esc(pb),
    ]
    related = []
    if pu: related.append('<a href="%s" class="city-card">%s Real Estate <span class="arrow">&rsaquo;</span></a>' % (pu, esc(city)))
    if cou: related.append('<a href="%s" class="city-card">%s County Homes <span class="arrow">&rsaquo;</span></a>' % (cou, esc(county)))
    related.append('<a href="/schools/" class="city-card">All School Districts <span class="arrow">&rsaquo;</span></a>')
    title = "Homes Near %s | Your Realty Link" % name
    meta = ("Buying or selling a home near %s in %s, Indiana? Your Realty Link helps families across the %s area. Get a free valuation." % (esc(name), esc(city), esc(city)))
    return page(rec, title, meta, hero_sub, badges, intro, sections, city, faqs,
                explore, quick_facts, related, esc(name))

# ── hub ──────────────────────────────────────────────────────────────────────
COUNTY_ORDER = ["Marion","Hamilton","Hendricks","Johnson","Boone","Hancock","Madison","Morgan","Shelby","Henry"]
def hub():
    pub = [d for d in SCHOOLS if d["type"] == "public"]
    prv = [d for d in SCHOOLS if d["type"] == "private"]
    def group(items):
        by = {}
        for d in items: by.setdefault(d["county"] or "Other", []).append(d)
        order = [c for c in COUNTY_ORDER if c in by] + sorted(c for c in by if c not in COUNTY_ORDER)
        out = []
        for cty in order:
            cards = "\n".join(
              '    <a href="/schools/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
              % (d["slug"], esc(d["short_name"])) for d in sorted(by[cty], key=lambda x: x["short_name"]))
            label = ("%s County" % cty) if cty != "Other" else "Other Areas"
            out.append('  <h2>%s</h2>\n  <div class="city-grid">\n%s\n  </div>' % (esc(label), cards))
        return "\n\n".join(out)
    pub_grid = group(pub); prv_grid = group(prv)
    url = "https://janetgiles.com/schools/"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Central Indiana School Districts &amp; Schools | Your Realty Link</title>
 <meta name="description" content="Explore homes for sale by school district across Central Indiana — public districts and private schools in Carmel, Fishers, Westfield, Noblesville, Greenwood, Avon and more.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="Central Indiana School Districts &amp; Schools | Your Realty Link">
 <meta property="og:description" content="Homes for sale by school district across Central Indiana — public districts and private schools by area.">
 <meta property="og:url" content="{url}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{url}", "name": "Central Indiana School Districts" }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "School Districts", "item": "{url}" }} ] }}
 ] }}
 </script>
 {FONTS}
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> School Districts</div>
</nav>

<section class="page-hero banner-raw" style="--hero-img: -webkit-image-set(url('/assets/img/heroes/schools.webp') type('image/webp'), url('/assets/img/heroes/schools.jpg') type('image/jpeg')); --hero-img: image-set(url('/assets/img/heroes/schools.webp') type('image/webp'), url('/assets/img/heroes/schools.jpg') type('image/jpeg')); --hero-pos: center;">
 <div class="container">
 <h1>Central Indiana <em>School Districts &amp; Schools</em></h1>
 <p class="hero-sub">For many buyers, the school comes first. Explore homes for sale by district across Central Indiana — public districts and private schools — and let Your Realty Link help you find a home inside the boundary that matters to your family. School assignment depends on the exact address; we'll help you confirm it.</p>
 </div>
</section>

<div class="container">
 <main class="content-main" style="max-width:none;">
  <p>Central Indiana families often start their home search with schools. Below are the public school districts and private &amp; parochial schools across the metro, grouped by county. Each links to homes for sale in the area, plus local market info. Always confirm the assigned schools for a specific address — a Your Realty Link agent can help.</p>

  <h2 style="margin-top:8px;">Public School Districts</h2>
{pub_grid}

  <hr class="divider">
  <h2>Private &amp; Parochial Schools</h2>
{prv_grid}

  <div class="cta-block" style="margin-top:32px;">
  <h3>Searching for a Home in a Specific District?</h3>
  <p>Your Realty Link helps buyers find homes inside the school boundary that matters most. Get a free home valuation or start your search today.</p>
  <div class="btn-group">
  <a href="https://yourrealtylink.com/property-search" class="btn btn-white" target="_blank" rel="noopener">Search Homes →</a>
  <a href="/services/free-home-valuation/" class="btn btn-outline" target="_blank" rel="noopener">Free Home Valuation</a>
  <a href="/contact/" class="btn btn-outline">Contact Your Realty Link</a>
  </div>
  </div>
 </main>
</div>

{FOOTER}

{SCRIPTS}'''

# ── generate ─────────────────────────────────────────────────────────────────
os.makedirs(os.path.join(ROOT, "schools"), exist_ok=True)
open(os.path.join(ROOT, "schools", "index.html"), "w", encoding="utf-8").write(hub())

made, skipped, warn = 0, 0, []
for rec in SCHOOLS:
    d = os.path.join(ROOT, "schools", rec["slug"]); idxf = os.path.join(d, "index.html")
    if rec.get("existing"):          # preserve the 10 hand-authored district pages
        skipped += 1; continue
    os.makedirs(d, exist_ok=True)
    htmlout = district_page(rec) if rec["type"] == "public" else private_page(rec)
    open(idxf, "w", encoding="utf-8").write(htmlout)
    made += 1

# sitemap
sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read(); blk = ""
for rec in SCHOOLS:
    loc = "https://janetgiles.com/schools/%s/" % rec["slug"]
    if loc not in s:
        blk += "<url>\n  <loc>%s</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n" % loc
if blk:
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", blk + "</urlset>"))

print("hub rebuilt (%d public + %d private). Detail pages: %d generated, %d preserved. Sitemap +%d."
      % (sum(1 for d in SCHOOLS if d["type"]=="public"), sum(1 for d in SCHOOLS if d["type"]=="private"),
         made, skipped, blk.count("<url>")))
for w in sorted(set(warn)): print("  WARN " + w)
