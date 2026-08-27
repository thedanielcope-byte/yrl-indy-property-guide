#!/usr/bin/env python3
"""Build the Communities & Subdivisions hub + per-community detail pages from
communities.json. Models the existing hand-authored detail pages (e.g.
communities/avalon-fishers/) and adds an info panel (HOA link, utilities-in-city
link, school/price/type) plus a future-ready image/video slot.

Detail pages are generated ONLY for communities whose directory does not already
exist, so the 10 rich hand-authored pages are preserved. The hub lists all.
Header/footer/fonts are regex-grabbed from index.html so the nav stays in sync.

    python3 build_communities.py
"""
import os, re, html, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "communities.json"), encoding="utf-8"))
CITY_ORDER = DATA["cities"]
COMMS = DATA["communities"]

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
def uhref(u): return str(u or "").replace("&", "&amp;")
def disp(c): return c.get("short_name") or c["name"]

# city -> city-page url (glob the cities/ tree)
CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def city_url(city):
    kebab = city.strip().lower().replace(" ", "-")
    for d in CITY_DIRS:
        base = os.path.basename(d.rstrip(os.sep))
        if base.startswith(kebab + "-"):
            cslug = os.path.basename(os.path.dirname(d.rstrip(os.sep)))
            return "/cities/%s/%s/" % (cslug, base)
    return None
def county_url(county):
    slug = county.strip().lower().replace(" ", "-") + "-county-indiana-real-estate"
    return "/counties/%s/" % slug if os.path.isdir(os.path.join(ROOT, "counties", slug)) else None

def natjoin(items):
    items = [i for i in items if i]
    if not items: return ""
    if len(items) == 1: return items[0]
    return ", ".join(items[:-1]) + ", and " + items[-1]

# ── detail page ──────────────────────────────────────────────────────────────
def faq_block(c):
    name = disp(c); city = c["city"]
    school = c.get("school_district")
    sc = ("%s is served by %s. Because attendance boundaries can change, a Your Realty Link agent can confirm the assigned schools for any specific home." % (name, school)) if school else \
         ("School attendance in %s can vary by exact address and boundaries change over time &mdash; a Your Realty Link agent can confirm the assigned schools for any specific home." % name)
    faqs = [
      ("What do homes cost in %s?" % name,
       "Homes in %s generally range from %s, depending on the specific home, size, and updates. Your Realty Link can provide a free market analysis for any address in the community." % (name, c.get("price_band","varying price ranges"))),
      ("How do I see homes for sale in %s?" % name,
       "Use the Your Realty Link property search to browse active MLS listings in %s and across %s &mdash; all pulled directly from the MIBOR MLS." % (name, city)),
      ("What schools serve %s?" % name, sc),
      ("Is %s a good community?" % name,
       "%s is a %s in %s that draws buyers for its location, amenities, and lifestyle. Your Realty Link knows the community and can help you weigh whether it fits your needs." % (name, c.get("type","community"), city)),
    ]
    html_ = "\n".join('<details class="faq-item">\n<summary>%s</summary>\n<div class="faq-answer"><p>%s</p></div>\n</details>' % (esc(q), a) for q, a in faqs)
    schema = ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
                        % (json.dumps(re.sub("<[^>]+>|&[a-z]+;|&#\\d+;", lambda m: {"&mdash;":"-","&amp;":"&"}.get(m.group(0),"") if m.group(0).startswith("&") else "", strip_amp(q))),
                           json.dumps(re.sub("<[^>]+>|&[a-z]+;|&#\\d+;", lambda m: {"&mdash;":"-","&amp;":"&"}.get(m.group(0),"") if m.group(0).startswith("&") else "", strip_amp(a))))
                        for q, a in faqs)
    return html_, schema

def strip_amp(t): return t

def info_panel(c):
    name = disp(c); city = c["city"]
    cu = city_url(city)
    rows = [
      '<li><span class="ci-k">📍 Location</span><span class="ci-v">%s, %s County</span></li>' % (esc(city), esc(c["county"])),
      '<li><span class="ci-k">🏡 Price range</span><span class="ci-v">%s</span></li>' % esc(c.get("price_band","Varies — ask us")),
      '<li><span class="ci-k">🏫 Schools</span><span class="ci-v">%s</span></li>' % (esc(c["school_district"]) if c.get("school_district") else "Confirm the assigned schools by address"),
      '<li><span class="ci-k">🏘 Type</span><span class="ci-v">%s</span></li>' % esc(c.get("type","Residential community")),
    ]
    if c.get("hoa_url"):
        rows.append('<li><span class="ci-k">🔗 HOA / community</span><span class="ci-v"><a href="%s" target="_blank" rel="noopener">Community & HOA info &#8599;</a></span></li>' % uhref(c["hoa_url"]))
    if cu:
        rows.append('<li><span class="ci-k">⚡ Utilities</span><span class="ci-v"><a href="%s#utilities">Setting up utilities in %s</a></span></li>' % (cu, esc(city)))
    media = ""
    if c.get("image"):
        media = '<div class="ci-media"><img src="%s" alt="%s in %s, Indiana" loading="lazy"></div>' % (uhref(c["image"]), esc(name), esc(city))
    elif c.get("video"):
        media = '<div class="ci-media"><video controls preload="none" src="%s"></video></div>' % uhref(c["video"])
    return ('<aside class="comm-info">\n<h2 class="ci-title">%s at a Glance</h2>\n%s<ul class="ci-list">\n%s\n</ul>\n</aside>'
            % (esc(name), media, "\n".join(rows)))

def detail_page(c):
    name = disp(c); full = c["name"]; city = c["city"]; county = c["county"]
    url = "https://janetgiles.com/communities/%s/" % c["slug"]
    price = c.get("price_band", "a range of price points")
    ctype = c.get("type", "residential community")
    school = c.get("school_district")
    hl = c.get("highlights", [])
    cu = city_url(city); cou = county_url(county)
    school_txt = ("served by %s" % school) if school else "with schools that vary by address"
    cu_link = ('<a href="%s">%s</a>' % (cu, esc(city))) if cu else esc(city)
    cou_link = ('<a href="%s">%s County</a>' % (cou, esc(county))) if cou else ("%s County" % esc(county))

    badges = [
      '<span class="hero-badge">📍 %s · %s County</span>' % (esc(city), esc(county)),
      '<span class="hero-badge">🏡 %s</span>' % esc(price),
    ]
    if school: badges.append('<span class="hero-badge">🏫 %s</span>' % esc(school))
    if hl: badges.append('<span class="hero-badge">✨ %s</span>' % esc(hl[0]))

    faq_html, faq_schema = faq_block(c)
    hl_sentence = natjoin([h[0].lower() + h[1:] for h in hl]) if hl else "well-kept homes and neighborhood amenities"
    intro_hl = esc(hl[0].lower()) if hl else "its location and lifestyle"
    intro_hl2 = (" and " + esc(hl[1].lower())) if len(hl) > 1 else ""
    schoolslink = '/schools/'
    if school:
        schools_p = '%s is served by <a href="%s">%s</a>, a key reason families choose the area. ' % (esc(name), schoolslink, esc(school))
    else:
        schools_p = 'School attendance for %s can vary by exact address, and boundaries change over time. ' % esc(name)
    if hl:
        amenities_p = 'Highlights of %s include %s. ' % (esc(name), natjoin([esc(h) for h in hl]))
    else:
        amenities_p = '%s offers the neighborhood amenities and green space %s buyers expect. ' % (esc(name), esc(city))
    explore = []
    if cu:  explore.append('<li><a href="%s">%s, Indiana Real Estate</a></li>' % (cu, esc(city)))
    if cou: explore.append('<li><a href="%s">%s County Real Estate</a></li>' % (cou, esc(county)))
    explore.append('<li><a href="/schools/">Central Indiana School Districts</a></li>')
    explore.append('<li><a href="/communities/">All Communities &amp; Subdivisions</a></li>')
    explore_items = "\n ".join(explore)
    badges_html = " ".join(badges)
    panel = info_panel(c)

    body = f'''<section class="page-hero">
 <div class="container">
 <h1>{esc(name)} <em>Homes for Sale</em></h1>
 <p class="hero-sub">A {esc(ctype)} in {esc(city)}, {esc(county)} County, {esc(school_txt)}. Your Realty Link helps buyers and sellers in {esc(name)}.</p>
 <div class="hero-badges">
 {badges_html}
 </div><p class="hero-reviewed">✔ Reviewed by <a href="/agents/janet-giles/">Janet Giles-Schultz</a>, Principal Broker · MIBOR member · Updated August 2026</p>
 </div>
</section>

<div class="container">
 <div class="content-wrap">
 <main class="content-main">

 <p>{esc(full)} is a {esc(ctype)} in {cu_link}, one of Central Indiana's most sought-after communities. Known for {intro_hl}{intro_hl2}, it's a place buyers ask about across {cou_link}. <strong>Your Realty Link</strong> &mdash; an Indianapolis-based MIBOR brokerage &mdash; helps buyers and sellers throughout {esc(name)} and the surrounding {esc(city)} area.</p>

 <h2>Living in {esc(name)}</h2>
 <p>{esc(name)} offers the kind of setting that keeps {esc(city)} in demand &mdash; {hl_sentence}. Everyday shopping, dining, and services are close by, and the broader {esc(city)} area surrounds the community with parks, employment, and strong public services. It's a community that suits families and professionals looking for an established {esc(city)} address.</p>

 <h2>{esc(name)} Homes &amp; Real Estate Market</h2>
 <p>Homes in {esc(name)} generally range from {esc(price)}, reflecting its profile as a {esc(ctype)}. Demand across {cou_link} is consistently strong, and pricing depends on the specific home, size, updates, and lot &mdash; so a local agent's read on value is helpful whether you're buying or selling. Ask Your Realty Link for a free, no-obligation market analysis for any address in the community.</p>

 <h2>Schools &amp; Location</h2>
 <p>{schools_p}We always recommend confirming the assigned schools for a specific home before buying. {esc(city)}'s location gives residents convenient access to the wider Indianapolis metro, employment corridors, shopping, and dining.</p>

 <h2>Amenities &amp; Lifestyle</h2>
 <p>{amenities_p}For buyers who value an established, well-located community, {esc(name)} checks the important boxes.</p>

 <h2>Work With a {esc(name)} Real Estate Agent</h2>
 <p>Your Realty Link helps buyers and sellers throughout {esc(name)} and the {esc(city)} area. <strong>Our team</strong> knows what draws buyers here and how to position homes to sell. Whether you're searching for a home in {esc(name)} or selling to reach ready buyers, we bring local knowledge and a proven marketing plan. Call us today or search homes online.</p>

 <div class="info-box">
 <strong>Selling a home in {esc(name)}? Your Realty Link knows the {esc(city)} market &mdash; request a free valuation.</strong> <a href="/services/free-home-valuation/" target="_blank" rel="noopener">Get your free home valuation →</a>
 </div>

 <div class="cta-block">
 <h3>Ready to Search Homes in {esc(name)}?</h3>
 <p>Browse all active MLS listings in {esc(name)} and {esc(city)} — updated in real time from the MIBOR MLS.</p>
 <div class="btn-group">
 <a href="https://yourrealtylink.com/property-search" class="btn btn-white" target="_blank" rel="noopener">Search {esc(name)} Homes →</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline" target="_blank" rel="noopener">Get a Free Home Valuation</a>
 <a href="/schedule/" class="btn btn-outline">📅 Schedule a Free Consultation</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Frequently Asked Questions — {esc(name)}</h2>
{faq_html}
 </section>

 <hr class="divider">
 <h3>Explore More Central Indiana Real Estate</h3>
 <ul>
 {explore_items}
 </ul>

 </main>
 {panel}
 </div>
</div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(name)} Homes for Sale | Your Realty Link</title>
 <meta name="description" content="{esc(name)} in {esc(city)}, Indiana: homes for sale, the {esc(ctype)} lifestyle, schools, amenities, and price ranges. Your Realty Link helps buyers and sellers in {esc(name)}.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="{esc(name)} Homes for Sale | Your Realty Link">
 <meta property="og:description" content="{esc(name)} in {esc(city)}, Indiana — homes, schools, amenities, and market info from Your Realty Link.">
 <meta property="og:url" content="{url}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{url}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".hero-sub"] }} }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "{esc(city)}, Indiana" }},
 {{ "@type": "FAQPage", "mainEntity": [ {faq_schema} ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Communities", "item": "https://janetgiles.com/communities/" }},
 {{ "@type": "ListItem", "position": 3, "name": "{esc(name)}", "item": "{url}" }} ] }}
 ] }}
 </script>
 {FONTS}
 <style>
.comm-info {{ background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 20px 22px; box-shadow: 0 5px 18px rgba(0,0,0,.05); align-self: start; }}
.comm-info .ci-title {{ font-size: 1.1rem; margin: 0 0 12px; color: #13294a; }}
.comm-info .ci-media {{ margin: 0 0 14px; border-radius: 10px; overflow: hidden; }}
.comm-info .ci-media img, .comm-info .ci-media video {{ width: 100%; display: block; }}
.comm-info .ci-list {{ list-style: none; margin: 0; padding: 0; }}
.comm-info .ci-list li {{ display: flex; flex-direction: column; gap: 1px; padding: 9px 0; border-bottom: 1px solid var(--border); font-size: 14px; }}
.comm-info .ci-list li:last-child {{ border-bottom: none; }}
.comm-info .ci-k {{ font-weight: 700; color: var(--mid); font-size: 12px; text-transform: uppercase; letter-spacing: .03em; }}
.comm-info .ci-v {{ color: #33373b; }}
.comm-info .ci-v a {{ color: var(--red); font-weight: 600; }}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/communities/">Communities</a> <span>&rsaquo;</span> {esc(name)}</div>
</nav>

{body}

{FOOTER}

{SCRIPTS}'''

# ── hub ──────────────────────────────────────────────────────────────────────
def build_hub():
    by_city = {}
    for c in COMMS:
        by_city.setdefault(c["city"], []).append(c)
    order = [c for c in CITY_ORDER if c in by_city] + [c for c in by_city if c not in CITY_ORDER]
    sections = []
    for city in order:
        cards = "\n".join(
          '    <a href="/communities/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
          % (c["slug"], esc(disp(c))) for c in sorted(by_city[city], key=lambda x: disp(x)))
        sections.append('  <h2>%s Communities</h2>\n  <div class="city-grid">\n%s\n  </div>' % (esc(city), cards))
    grid = "\n\n".join(sections)
    url = "https://janetgiles.com/communities/"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Central Indiana Communities &amp; Subdivisions | Your Realty Link</title>
 <meta name="description" content="Explore Central Indiana's most popular communities and subdivisions — golf, lake, luxury, and master-planned neighborhoods in Carmel, Fishers, Westfield, Zionsville, Noblesville and more.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="Central Indiana Communities &amp; Subdivisions | Your Realty Link">
 <meta property="og:description" content="Popular Central Indiana communities and subdivisions — homes, amenities, schools, and market info by neighborhood.">
 <meta property="og:url" content="{url}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{url}", "name": "Central Indiana Communities & Subdivisions" }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Communities", "item": "{url}" }} ] }}
 ] }}
 </script>
 {FONTS}
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> Communities &amp; Subdivisions</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>Central Indiana <em>Communities &amp; Subdivisions</em></h1>
 <p class="hero-sub">From golf and lakefront communities to master-planned and 55+ neighborhoods, explore the named communities that make Central Indiana's suburbs distinct. Each links to homes, amenities, schools, and local market info.</p>
 </div>
</section>

<div class="container">
 <main class="content-main" style="max-width:none;">
  <p>Central Indiana's most desirable suburbs are built from distinct named communities and subdivisions &mdash; each with its own character, amenities, and price range. Below are the communities Your Realty Link helps buyers and sellers in, grouped by city. Don't see yours? <a href="/contact/">Contact us</a> &mdash; we work across every Central Indiana community.</p>

{grid}

  <div class="cta-block" style="margin-top:32px;">
  <h3>Buying or Selling in One of These Communities?</h3>
  <p>Your Realty Link knows these neighborhoods block by block. Get a free home valuation or start your search today.</p>
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
os.makedirs(os.path.join(ROOT, "communities"), exist_ok=True)
open(os.path.join(ROOT, "communities", "index.html"), "w", encoding="utf-8").write(build_hub())

made, skipped, warn = 0, 0, []
for c in COMMS:
    d = os.path.join(ROOT, "communities", c["slug"])
    idx = os.path.join(d, "index.html")
    if c.get("existing") or os.path.exists(idx):
        skipped += 1; continue
    os.makedirs(d, exist_ok=True)
    open(idx, "w", encoding="utf-8").write(detail_page(c))
    made += 1
    if not city_url(c["city"]): warn.append("no city page for " + c["city"])

# sitemap
sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read(); blk = ""
for c in COMMS:
    loc = "https://janetgiles.com/communities/%s/" % c["slug"]
    if loc not in s:
        blk += "<url>\n  <loc>%s</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n" % loc
if blk:
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", blk + "</urlset>"))

print("hub rebuilt (%d communities). Detail pages: %d generated, %d preserved. Sitemap +%d." % (len(COMMS), made, skipped, blk.count("<url>")))
for w in sorted(set(warn)): print("  WARN " + w)
