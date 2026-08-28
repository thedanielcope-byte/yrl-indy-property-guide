#!/usr/bin/env python3
"""Build NEW city pages from new_cities.json — for sizable Central Indiana towns
that don't have a page yet (New Whiteland, Ingalls, Chesterfield, ...). Clones the
existing city-page template (e.g. cities/johnson-county/greenwood-indiana-real-estate/):
hero + QA block + 5 H2 sections + FAQ+schema + Explore + sidebar. Leaves the
<!-- SCHOOLS --> marker and the Explore anchor so inject_city_schools.py and
inject_idx.py enrich it afterward. Header/footer/fonts grabbed from index.html.

Generates ONLY towns whose dir doesn't already exist. All prose is built from the
web-verified data in new_cities.json — nothing fabricated.

    python3 build_city.py   →   then: inject_city_schools.py, inject_idx.py
"""
import os, re, html, glob, json
import idx_config as idx

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "new_cities.json"), encoding="utf-8"))

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
def plain(t): return re.sub(r"<[^>]+>", "", str(t)).replace("&amp;", "&").replace("&mdash;", "-").strip()

CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def city_url(name):
    kebab = name.strip().lower().replace(" ", "-").replace(".", "")
    for d in CITY_DIRS:
        if os.path.basename(d.rstrip(os.sep)).startswith(kebab + "-"):
            cslug = os.path.basename(os.path.dirname(d.rstrip(os.sep)))
            return "/cities/%s/%s/" % (cslug, os.path.basename(d.rstrip(os.sep)))
    return None
def county_url(county):
    slug = county.strip().lower().replace(" ", "-") + "-county-indiana-real-estate"
    return "/counties/%s/" % slug if os.path.isdir(os.path.join(ROOT, "counties", slug)) else None
def short_school(s):
    return re.sub(r"\s+(Community\s+)?School(s)?(\s+Corporation)?.*$", "", s).strip() or s

def faq_schema(pairs):
    return ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
                      % (json.dumps(plain(q)), json.dumps(plain(a))) for q, a in pairs)

def page(c):
    name = c["name"]; county = c["county"]; slug = c["slug"]
    cslug = county.lower().replace(" ", "-") + "-county"
    url = "https://janetgiles.com/cities/%s/%s-indiana-real-estate/" % (cslug, slug)
    price = c["price_band"]; sch = c["school_district"]; sch_s = c.get("school_short") or short_school(sch)
    commute = c["commute"]; commute_s = c.get("commute_short", ""); hwy = c.get("highways", "")
    pop = c.get("population"); char = c["character"]; hl = c.get("highlights", [])
    cou = county_url(county); idxu = idx.city_search_url(name)
    formid = ("cities-%s-%s" % (cslug, slug))[:34]
    cou_link = ('<a href="%s">%s County</a>' % (cou, esc(county))) if cou else ("%s County" % esc(county))
    gov = c.get("gov_url"); wiki = c.get("wiki_url") or ("https://en.wikipedia.org/wiki/%s,_Indiana" % name.replace(" ", "_"))
    wiki_c = "https://en.wikipedia.org/wiki/%s_County,_Indiana" % county.replace(" ", "_")

    # nearby city links
    nearby = []
    for nm in c.get("nearby_towns", []):
        u = city_url(nm)
        if u: nearby.append((nm, u))
    nearby = nearby[:3]

    pop_line = ("with a population of roughly %s, " % f"{pop:,}") if pop else ""
    hl_join = ""
    if hl:
        hl_join = hl[0][0].lower() + hl[0][1:]
        if len(hl) > 1: hl_join += ", " + (", ".join(h[0].lower()+h[1:] for h in hl[1:-1] + ([hl[-1]] if len(hl)>2 else []))) if len(hl)>2 else " and " + hl[1][0].lower()+hl[1][1:]

    faqs = [
      ("What is the average home price in %s Indiana?" % name,
       "Homes in %s typically range from %s, depending on the neighborhood, size, age, and condition. Contact Your Realty Link for a free comparative market analysis specific to %s." % (name, price, name)),
      ("What school district serves %s Indiana?" % name,
       "%s is served by %s. School assignment depends on your specific address — a Your Realty Link agent can confirm the assigned schools when you're searching for homes." % (name, sch)),
      ("How do I search homes for sale in %s Indiana?" % name,
       "Use the Your Realty Link property search to browse all active MLS listings in %s and across %s County. All listings pull directly from the MIBOR MLS." % (name, county)),
      ("Is %s a good place to live?" % name,
       "Yes — %s draws buyers for its %s. Contact Your Realty Link and we'll help you decide whether %s fits your needs and budget." % (name, (hl[0].lower() if hl else "location, value, and community feel"), name)),
    ]
    fh = "\n".join('<details class="faq-item">\n<summary>%s</summary>\n<div class="faq-answer"><p>%s</p></div>\n</details>' % (esc(q), esc(a)) for q, a in faqs)
    fs = faq_schema(faqs)

    badges = ['<span class="hero-badge">📍 %s County</span>' % esc(county),
              '<span class="hero-badge">🏫 %s</span>' % esc(sch_s),
              '<span class="hero-badge">🏡 %s</span>' % esc(price)]
    if commute_s: badges.append('<span class="hero-badge">%s to Downtown</span>' % esc(commute_s))
    badges_html = "\n ".join(badges)

    qa_lead = ("<strong>%s, Indiana</strong> is a %s County community%s where homes typically range from %s. It's served by %s. Your Realty Link helps buyers and sellers across %s and %s County."
               % (name, county, (" " + commute_s.replace("~", "about ") + " from downtown Indianapolis," if commute_s else ""), price, sch_s, name, county))

    explore = ['<li><a href="%s">%s County Indiana Real Estate — County Overview</a></li>' % (cou, esc(county)) if cou else '']
    for nm, u in nearby:
        explore.append('<li><a href="%s">%s Indiana Real Estate &amp; Homes for Sale</a></li>' % (u, esc(nm)))
    explore.append('<li><a href="/indianapolis-real-estate/">Indianapolis Real Estate — Central Indiana Overview</a></li>')
    explore_items = "\n ".join(x for x in explore if x)

    nearby_cards = "\n ".join('<a href="%s" class="city-card">%s <span class="arrow">&rsaquo;</span></a>' % (u, esc(nm)) for nm, u in nearby)
    nearby_cards += '\n <a href="/indianapolis-real-estate/" class="city-card">Indianapolis <span class="arrow">&rsaquo;</span></a>'

    qf = ['<li><span class="icon">🏛</span> <strong>County:</strong> %s</li>' % esc(county)]
    if pop: qf.append('<li><span class="icon">👥</span> <strong>Population:</strong> ~%s</li>' % f"{pop:,}")
    qf += ['<li><span class="icon">🏫</span> <strong>Schools:</strong> %s</li>' % esc(sch_s),
           '<li><span class="icon">🏡</span> <strong>Prices:</strong> %s</li>' % esc(price)]
    if commute_s: qf.append('<li><span class="icon">🚗</span> <strong>Indy commute:</strong> %s</li>' % esc(commute_s))
    if hwy: qf.append('<li><span class="icon">🛣</span> <strong>Highways:</strong> %s</li>' % esc(hwy))
    qf_html = "\n ".join(qf)

    reslinks = []
    if gov: reslinks.append('<li><a href="%s" target="_blank" rel="noopener">Official %s Government ↗</a></li>' % (gov, esc(name)))
    reslinks += ['<li><a href="%s" target="_blank" rel="noopener">%s, Indiana (Wikipedia) ↗</a></li>' % (wiki, esc(name)),
                 '<li><a href="%s" target="_blank" rel="noopener">%s County, Indiana (Wikipedia) ↗</a></li>' % (wiki_c, esc(county)),
                 '<li><a href="https://www.stats.indiana.edu/" target="_blank" rel="noopener">STATS Indiana — Community Data ↗</a></li>']
    reslinks_html = "\n    ".join(reslinks)

    metadesc = "Search %s Indiana homes for sale with Your Realty Link. %s County living with homes from %s and %s. Get a free home valuation." % (name, county, price, sch_s)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(name)} Indiana Real Estate | Your Realty Link</title>
 <meta name="description" content="{esc(metadesc)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="{esc(name)} Indiana Real Estate | Your Realty Link">
 <meta property="og:description" content="{esc(metadesc)}">
 <meta property="og:url" content="{url}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{url}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"] }} }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "logo": "/assets/img/yrl-logo.png", "telephone": "317-997-7404", "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US" }}, "areaServed": {{ "@type": "City", "name": "{esc(name)}", "containedIn": "{esc(county)} County, Indiana" }} }},
 {{ "@type": "FAQPage", "mainEntity": [ {fs} ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "{esc(county)} County", "item": "https://janetgiles.com/counties/{cslug}-indiana-real-estate/" }},
 {{ "@type": "ListItem", "position": 3, "name": "{esc(name)} Indiana Real Estate", "item": "{url}" }} ] }}
 ] }}
 </script>
 {FONTS}
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/counties/{cslug}-indiana-real-estate/">{esc(county)} County</a> <span>&rsaquo;</span> {esc(name)} Indiana Real Estate</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>{esc(name)} Indiana Real Estate &amp; <em>Homes for Sale</em></h1>
 <p class="hero-sub">Buying or selling in {esc(name)}? Your Realty Link's agents know {esc(county)} County inside and out. Search all active listings and get a free home valuation.</p>
 <div class="hero-badges">
 {badges_html}
 </div><p class="hero-reviewed">✔ Reviewed by <a href="/agents/janet-giles/">Janet Giles-Schultz</a>, Principal Broker · MIBOR member · Updated August 2026</p>
 </div>
</section>

<div class="container">
 <div class="content-wrap">
 <main class="content-main">

<div class="quick-answer">
 <p class="qa-heading">{esc(name)} Indiana Real Estate at a Glance</p>
 <p class="qa-lead">{qa_lead}</p>
 <dl class="qa-facts">
 <div><dt>County</dt><dd>{esc(county)} County</dd></div>
 <div><dt>Typical home prices</dt><dd>{esc(price)}</dd></div>
 {('<div><dt>Drive to downtown Indy</dt><dd>' + esc(commute_s) + '</dd></div>') if commute_s else ''}
 <div><dt>School district</dt><dd>{esc(sch_s)}</dd></div>
 <div><dt>Search listings</dt><dd><a href="{esc(idxu)}" target="_blank" rel="noopener">Search {esc(name)} listings &rarr;</a></dd></div>
 </dl>
</div>

 <p>{esc(char)} Your Realty Link serves buyers and sellers throughout {esc(name)} and {cou_link}, with experienced MIBOR agents who know the local market.</p>

 <h2>Living in {esc(name)}, Indiana</h2>
 <p>{esc(name)} offers the kind of {esc(county)} County lifestyle that keeps buyers interested — {esc(hl_join or 'a genuine community feel, local amenities, and convenient access to the greater Indianapolis area')}. Everyday shopping, dining, parks, and schools are close by, and the surrounding area adds even more. It's a community that suits families and professionals looking for {esc(name)}-area value with metro access.</p>

 <h2>{esc(name)} Home Prices &amp; Real Estate Market</h2>
 <p>Homes in {esc(name)} generally range from {esc(price)}, depending on the specific home, size, age, updates, and lot. You'll find a mix of established neighborhoods and, in many parts of {esc(county)} County, newer construction as well. Demand and pricing shift with the season and the neighborhood, so a local agent's read on value is helpful whether you're buying or selling. Ask Your Realty Link for a free, no-obligation market analysis for any {esc(name)} address.</p>

 <div class="info-box">
 <strong>Thinking about selling in {esc(name)}?</strong> Your Realty Link provides free comparative market analyses for homeowners across {esc(county)} County. <a href="/services/free-home-valuation/" target="_blank" rel="noopener">Get your free home valuation →</a>
 </div>

 <!-- SCHOOLS -->
 <h2>Schools in {esc(name)}, Indiana</h2>
 <p>{esc(name)} is served by <strong>{esc(sch)}</strong>. School district boundaries are an important factor for many buyers, and assignment depends on the exact address — a Your Realty Link agent can help you identify the right neighborhoods based on your preferred school assignment.</p>

 <h2>Commute from {esc(name)} to Indianapolis</h2>
 <p>{esc(commute)} {("Main routes serving the area include " + esc(hwy) + ". ") if hwy else ""}For buyers who want {esc(county)} County value with access to the wider Indianapolis metro, {esc(name)} is a practical choice.</p>

 <h2>Work With a {esc(name)} Indiana Real Estate Agent</h2>
 <p>Your Realty Link is ready to help you buy or sell a home in {esc(name)}. <strong>Our team</strong> brings hands-on knowledge of {esc(county)} County's neighborhoods, price trends, and market dynamics. Whether you're a first-time buyer or a seller looking to maximize your return, we combine local expertise and a proven marketing approach. Call us today or start your search online.</p>

 <div class="cta-block">
 <h3>Ready to Search Homes in {esc(name)}?</h3>
 <p>Browse all active MLS listings in {esc(name)} and {esc(county)} County — updated in real time from the MIBOR MLS.</p>
 <div class="btn-group">
 <a href="{esc(idxu)}" class="btn btn-white" target="_blank" rel="noopener">Search Homes in {esc(name)} →</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline" target="_blank" rel="noopener">Get a Free Home Valuation</a>
 <a href="/schedule/" class="btn btn-outline">📅 Schedule a Free Consultation</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Frequently Asked Questions — {esc(name)} Indiana Real Estate</h2>
{fh}
 </section>

 <div class="cta-block cta-block-light">
 <h3>Selling a Home in {esc(name)}?</h3>
 <p>Get a free, no-obligation home valuation from Your Realty Link. Our {esc(county)} County team will show you exactly what your {esc(name)} home is worth in today's market.</p>
 <div class="btn-group">
 <a href="/services/free-home-valuation/" class="btn btn-primary" target="_blank" rel="noopener">Get a Free Valuation</a>
 <a href="/contact/" class="btn btn-outline">Contact Your Realty Link</a>
 </div>
 </div>

 <hr class="divider">
 <h3>Explore More {esc(county)} County Real Estate</h3>
 <p>{esc(name)} is one of several great communities in {esc(county)} County. Explore nearby cities or learn more about the full county market:</p>
 <ul>
 {explore_items}
 </ul>

 <div class="info-box" style="margin-top:24px;">
 <strong>Helpful Local Resources</strong>
 <ul style="margin:10px 0 0; padding-left:20px;">
    {reslinks_html}
 </ul>
 </div>

 </main>

 <aside class="content-sidebar">
  <div class="sidebar-card">
 <div class="sidebar-card-header">Get in Touch</div>
 <div class="sidebar-card-body">
 <p>Have questions about {esc(name)}? Fill out this quick form and we'll reach out.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="cities/{cslug}/{slug}-indiana-real-estate">
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
 <div class="sidebar-card-header">Search {esc(name)} Homes</div>
 <div class="sidebar-card-body">
 <p>Browse all active MLS listings in {esc(name)} — updated continuously from the MIBOR MLS.</p>
 <a href="{esc(idxu)}" class="btn btn-primary btn-sm btn-full" target="_blank" rel="noopener">Search All Listings →</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline btn-sm btn-full" target="_blank" rel="noopener">Free Home Valuation</a>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">{esc(name)} Quick Facts</div>
 <div class="sidebar-card-body">
 <ul class="contact-list">
 {qf_html}
 </ul>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Nearby Cities</div>
 <div class="sidebar-card-body" style="padding:12px;">
 {nearby_cards}
 </div>
 </div>

 </aside>
 </div>
</div>

{FOOTER}

{SCRIPTS}'''

# ── generate ─────────────────────────────────────────────────────────────────
made, skipped, warn = 0, 0, []
for c in DATA["cities"]:
    cslug = c["county"].lower().replace(" ", "-") + "-county"
    d = os.path.join(ROOT, "cities", cslug, "%s-indiana-real-estate" % c["slug"])
    idxf = os.path.join(d, "index.html")
    if os.path.exists(idxf) and not DATA.get("overwrite"):
        skipped += 1; continue
    os.makedirs(d, exist_ok=True)
    open(idxf, "w", encoding="utf-8").write(page(c))
    made += 1
    if not county_url(c["county"]): warn.append("no county page for " + c["county"])

# sitemap
sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read(); blk = ""
for c in DATA["cities"]:
    cslug = c["county"].lower().replace(" ", "-") + "-county"
    loc = "https://janetgiles.com/cities/%s/%s-indiana-real-estate/" % (cslug, c["slug"])
    if loc not in s:
        blk += "<url>\n  <loc>%s</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.7</priority>\n</url>\n" % loc
if blk:
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", blk + "</urlset>"))

print("city pages: %d generated, %d preserved. Sitemap +%d." % (made, skipped, blk.count("<url>")))
for w in sorted(set(warn)): print("  WARN " + w)
