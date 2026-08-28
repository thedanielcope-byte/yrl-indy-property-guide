#!/usr/bin/env python3
"""Build city-vs-city comparison pages from the vetted per-city data in
city_guides_data.py. Mirrors the hand-authored compare pages
(compare/carmel-vs-fishers/) and generates ONLY matchups whose directory does
not already exist — so the 8 hand-authored compares are preserved. Also adds
the new cards to the compare hub and sitemap. All prose is derived from the
already-verified county/price/schools/commute/character fields — nothing new is
invented. Header/footer/fonts are grabbed from index.html so the nav stays in sync.

    python3 build_compare.py
"""
import os, re, html, json
import importlib.util
import idx_config as idx

ROOT = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cg", os.path.join(ROOT, "city_guides_data.py"))
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
CITIES = cg.CITIES

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS  = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

def esc(s): return html.escape(str(s or ""), quote=False)
def plain(t): return re.sub(r"<[^>]+>", "", str(t)).replace("&amp;", "&").replace("&mdash;", "-").strip()

# Short, condensed "known for" + "best for" — distilled from each city's vetted
# character blurb (no new facts). Only the matchup cities are needed.
KNOWN_FOR = {
 "carmel":"the Arts & Design District, the Palladium, roundabouts, and a walkable downtown",
 "westfield":"the Grand Park Sports Campus and a fast-developing downtown",
 "noblesville":"a historic courthouse-square downtown and lakefront living",
 "fishers":"the Nickel Plate District, Geist access, and a young, tech-driven energy",
 "geist":"Geist Reservoir waterfront living and boating",
 "mccordsville":"newer construction and the walkable McCord Square town center",
 "zionsville":"a brick-paved Main Street, boutique shopping, and wooded lots",
 "whitestown":"the Anson mixed-use development and fast growth",
 "avon":"strong schools, new shopping, and west-side value",
 "plainfield":"the Metropolis shopping district, parks and trails, and airport access",
 "brownsburg":"racing heritage, top-rated schools, and a small-town downtown",
 "danville":"a classic courthouse-square county seat with small-town charm",
 "greenwood":"a fast-growing retail and dining hub with an active Old Town",
 "bargersville":"small-town growth, wineries, and Center Grove-area schools",
 "whiteland":"affordable newer homes and quick I-65 access",
 "franklin":"a restored courthouse-square downtown, the Artcraft Theatre, and a college-town feel",
 "mooresville":"a walkable downtown, small-town charm, and quick interstate access",
 "fortville":"small-town character, Mt. Vernon schools, and easy northeast-side access",
 "lebanon":"a classic courthouse-square downtown, affordable homes, and LEAP-district growth",
 "southport":"a tight-knit south-side community, affordable homes, and an easy commute",
}
# second-person clauses so they fit both "Choose X if you ___" and "Buyers who ___"
BEST_FOR = {
 "carmel":"prioritize top schools, walkability, and resale prestige",
 "westfield":"want newer construction, room to grow, and a youth-sports hub",
 "noblesville":"want value, historic character, and steady growth",
 "fishers":"want more home per dollar in a top-rated district",
 "geist":"want lake access and upscale suburban homes",
 "mccordsville":"want new construction and value on the northeast side",
 "zionsville":"want small-town luxury and top-rated schools",
 "whitestown":"want new construction and quick interstate access",
 "avon":"want value and convenience on the west side",
 "plainfield":"want amenities, value, and easy interstate and airport access",
 "brownsburg":"want strong schools and a genuine small-town feel",
 "danville":"want small-town character and Hendricks County value",
 "greenwood":"want value and amenities on the south side",
 "bargersville":"want newer homes and small-town character south of Indy",
 "whiteland":"want affordable new construction in Clark-Pleasant schools",
 "franklin":"want more house per dollar and genuine small-town character",
 "mooresville":"want small-town charm and value on the southwest side",
 "fortville":"want a small-town feel with newer homes northeast of Indy",
 "lebanon":"want affordability and long-term growth potential in Boone County",
 "southport":"want affordability and a genuine community feel close to downtown",
}

# High-value matchups to generate (a, b). Skips any whose dir already exists.
MATCHUPS = [
 ("carmel","westfield"), ("carmel","noblesville"), ("noblesville","westfield"),
 ("fishers","geist"), ("fishers","mccordsville"), ("westfield","zionsville"),
 ("zionsville","whitestown"), ("avon","plainfield"), ("brownsburg","plainfield"),
 ("plainfield","danville"), ("greenwood","bargersville"), ("greenwood","whiteland"),
 ("carmel","greenwood"), ("fishers","avon"), ("mccordsville","noblesville"),
 # round 2
 ("zionsville","fishers"), ("geist","noblesville"), ("plainfield","greenwood"),
 ("avon","greenwood"), ("mooresville","greenwood"), ("mooresville","plainfield"),
 ("franklin","bargersville"), ("bargersville","whiteland"), ("avon","danville"),
 ("brownsburg","danville"), ("whitestown","brownsburg"), ("mccordsville","fortville"),
 ("lebanon","whitestown"), ("greenwood","southport"),
]

def low(price):
    m = re.search(r"\$(\d[\d,]*)", price or "")
    return int(m.group(1).replace(",", "")) if m else 0

def pricier(a, b):
    la, lb = low(CITIES[a]["price"]), low(CITIES[b]["price"])
    if la >= lb + 40: return a
    if lb >= la + 40: return b
    return None

def county_short(c):  # "Hamilton County" -> "Hamilton"
    return re.sub(r"\s*County.*$", "", c).strip()
def county_url(c):
    slug = county_short(c).lower().replace(" ", "-") + "-county-indiana-real-estate"
    return "/counties/%s/" % slug if os.path.isdir(os.path.join(ROOT, "counties", slug)) else None

def faq_schema(pairs):
    return ",\n".join('{\n "@type": "Question",\n "name": %s,\n "acceptedAnswer": { "@type": "Answer", "text": %s }\n }'
                      % (json.dumps(plain(q)), json.dumps(plain(a))) for q, a in pairs)

def page(a, b):
    A, B = CITIES[a], CITIES[b]
    an, bn = A["name"], B["name"]
    slug = "%s-vs-%s" % (a, b)
    url = "https://janetgiles.com/compare/%s/" % slug
    title = "%s vs %s: Which Indiana Suburb? | Your Realty Link" % (an, bn)
    meta = ("%s vs %s, Indiana: compare home prices, schools, commute, and lifestyle side by side to decide which suburb fits you best." % (an, bn))
    same_county = county_short(A["county"]) == county_short(B["county"])
    pr = pricier(a, b)
    # price sentence
    if pr == a:   price_lead = "%s generally carries a premium, while %s tends to give you more home per dollar." % (an, bn)
    elif pr == b: price_lead = "%s generally carries a premium, while %s tends to give you more home per dollar." % (bn, an)
    else:         price_lead = "The two land in a similar price range, so budget is rarely the deciding factor here."
    cheaper = (b if pr == a else a if pr == b else None)
    au, bu = A["url"], B["url"]
    ac, bc = county_url(A["county"]), county_url(B["county"])

    # quick answer
    qa = ("<strong>Choose %s</strong> if you %s. <strong>Choose %s</strong> if you %s. %s"
          % (an, BEST_FOR.get(a, "want the fit described below"), bn, BEST_FOR.get(b, "want the fit described below"), price_lead))

    # at a glance rows
    rows = [
      ("County", county_short(A["county"]), county_short(B["county"])),
      ("Typical prices", esc(A["price"]).replace("the ", "", 1), esc(B["price"]).replace("the ", "", 1)),
      ("School district", esc(A["schools"]).replace("the ", "", 1), esc(B["schools"]).replace("the ", "", 1)),
      ("Commute to downtown", esc(A["commute"]), esc(B["commute"])),
      ("Known for", esc(KNOWN_FOR.get(a, "")), esc(KNOWN_FOR.get(b, ""))),
      ("Best for", "Buyers who " + esc(BEST_FOR.get(a, "")), "Buyers who " + esc(BEST_FOR.get(b, "")))]
    table = "\n".join('<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>' % r for r in rows)

    faqs = [
      ("Is %s or %s more expensive?" % (an, bn),
       ("%s is generally the pricier of the two — it typically runs %s, versus %s for %s. At the same budget you'll usually get more home in %s."
        % (CITIES[pr]["name"], CITIES[pr]["price"], CITIES[cheaper]["price"], CITIES[cheaper]["name"], CITIES[cheaper]["name"]))
       if pr else
       ("They're closely matched on price — %s runs %s and %s runs %s — so the decision usually comes down to schools, commute, and feel rather than cost."
        % (an, A["price"], bn, B["price"]))),
      ("Which has better schools, %s or %s?" % (an, bn),
       "%s is served by %s and %s by %s. Both are worth touring in person, and the assigned schools depend on the specific address — a Your Realty Link agent can confirm attendance for any home." % (an, A["schools"], bn, B["schools"])),
      ("Which is a shorter commute to downtown Indianapolis?",
       "%s is %s. %s is %s. The better pick depends on which corridor matches your daily drive." % (an, A["commute"], bn, B["commute"])),
      ("Is %s or %s better for my family?" % (an, bn),
       "It depends on your priorities. %s is best for buyers who %s, while %s is best for buyers who %s. Because they're both in the Indianapolis metro, we can tour homes in each on the same day." % (an, BEST_FOR.get(a,""), bn, BEST_FOR.get(b,""))),
    ]
    faq_html = "\n".join('  <details class="faq-item">\n <summary>%s</summary>\n <div class="faq-answer">\n <p>%s</p>\n </div>\n </details>' % (esc(q), esc(a2)) for q, a2 in faqs)
    fs = faq_schema(faqs)

    # related compares — a stable mix of hand-authored + siblings
    related_pool = ["carmel-vs-fishers","fishers-vs-noblesville","zionsville-vs-carmel","westfield-vs-fishers",
                    "avon-vs-brownsburg","greenwood-vs-franklin","new-construction-vs-resale","realtor-vs-fsbo"]
    rel = [s for s in related_pool if s != slug][:6]
    rel_cards = "\n ".join('<a href="/compare/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
                           % (s, esc(s.replace("-vs-", " vs ").replace("-", " ").title().replace("Vs","vs").replace("Fsbo","FSBO"))) for s in rel)

    county_badge = ("📍 %s County" % county_short(A["county"])) if same_county else "📍 Central Indiana"
    fid = slug.replace("-", "")
    search = idx.county_search_url(county_short(A["county"])) if same_county else idx.SEARCH_BASE
    intro2 = ("Both sit in %s County, so this really comes down to feel, price, and schools rather than geography." % county_short(A["county"])) if same_county else \
             ("They sit in different parts of the metro, so commute direction and price do a lot of the deciding here.")

    return slug, f'''<!DOCTYPE html>
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
 <meta property="og:type" content="article">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{url}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"] }} }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" }},
 {{ "@type": "FAQPage", "mainEntity": [ {fs} ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Compare", "item": "https://janetgiles.com/compare/" }},
 {{ "@type": "ListItem", "position": 3, "name": "{esc(an)} vs {esc(bn)}", "item": "{url}" }} ] }}
 ] }}
 </script>
 {FONTS}
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/compare/">Compare</a> <span>&rsaquo;</span> {esc(an)} vs {esc(bn)}</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>{esc(an)} vs {esc(bn)}: <em>Which Suburb Is Right for You?</em></h1>
 <p class="hero-sub">Two Central Indiana suburbs, side by side — prices, schools, commute, and lifestyle compared honestly by a local MIBOR brokerage.</p>
 <div class="hero-badges">
 <span class="hero-badge">{county_badge}</span>
 <span class="hero-badge">🏡 Prices compared</span>
 <span class="hero-badge">🏫 Schools compared</span>
 </div><p class="hero-reviewed">✔ Reviewed by <a href="/agents/janet-giles/">Janet Giles-Schultz</a>, Principal Broker · MIBOR member · Updated August 2026</p>
 </div>
</section>

<div class="container">
 <div class="content-wrap">
 <main class="content-main">

<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">{qa}</p>
 <dl class="qa-facts">
 <div><dt>{esc(an)} prices</dt><dd>{esc(A["price"]).replace("the ","",1)}</dd></div>
 <div><dt>{esc(bn)} prices</dt><dd>{esc(B["price"]).replace("the ","",1)}</dd></div>
 <div><dt>{esc(an)} schools</dt><dd>{esc(A["schools"]).replace("the ","",1)}</dd></div>
 <div><dt>{esc(bn)} schools</dt><dd>{esc(B["schools"]).replace("the ","",1)}</dd></div>
 <div><dt>Compare listings</dt><dd><a href="{esc(search)}" target="_blank" rel="noopener">Search the MLS &rarr;</a></dd></div>
 </dl>
</div>

 <p>{esc(an)} and {esc(bn)} are two Central Indiana communities buyers often weigh against each other. {intro2} Here's how they actually compare — not the marketing, the real differences.</p>

 <h2>At a Glance</h2>
 <table class="data-table">
 <thead><tr><th></th><th>{esc(an)}</th><th>{esc(bn)}</th></tr></thead>
 <tbody>
{table}
 </tbody>
 </table>

 <h2>Home Prices</h2>
 <p>{esc(an)} homes typically run {esc(A["price"])}, while {esc(bn)} generally lands in {esc(B["price"])}. {price_lead} Compare current listings on our <a href="{au}">{esc(an)}</a> and <a href="{bu}">{esc(bn)}</a> pages, and remember that a local agent's read on value matters more than any published range.</p>

 <h2>Schools</h2>
 <p>{esc(an)} is served by {esc(A["schools"])}; {esc(bn)} is served by {esc(B["schools"])}. Both are worth touring in person rather than judging from rankings, and the assigned schools depend on the exact address. See our <a href="/schools/">Central Indiana school district guides</a> to compare boundaries and confirm attendance for a specific home.</p>

 <h2>Lifestyle &amp; Character</h2>
 <p><strong>{esc(an)}</strong> is {esc(A["character"])}. <strong>{esc(bn)}</strong> is {esc(B["character"])}. The two feel genuinely different day to day, and standing in each usually settles the choice faster than any list can.</p>

 <h2>Commute</h2>
 <p>{esc(an)} is {esc(A["commute"])}. {esc(bn)} is {esc(B["commute"])}. For many buyers the deciding factor isn't the suburb at all — it's which corridor matches the drive you'll actually make every day.</p>

 <h2>Choose {esc(an)} If…</h2>
 <ul>
 <li>Your budget fits {esc(A["price"]).replace("the ","",1)}</li>
 <li>You want {esc(KNOWN_FOR.get(a,""))}</li>
 <li>You want {esc(A["schools"])}</li>
 <li>You {esc(BEST_FOR.get(a,""))}</li>
 </ul>

 <h2>Choose {esc(bn)} If…</h2>
 <ul>
 <li>Your budget fits {esc(B["price"]).replace("the ","",1)}</li>
 <li>You want {esc(KNOWN_FOR.get(b,""))}</li>
 <li>You want {esc(B["schools"])}</li>
 <li>You {esc(BEST_FOR.get(b,""))}</li>
 </ul>

 <h2>The Honest Verdict</h2>
 <p>Both are strong choices, and most buyers should tour each before deciding. {("Since they're in the same county, you can see homes in both on the same afternoon." if same_county else "Because they sit in different parts of the metro, let your commute and budget lead.")} If value and more home per dollar matter most, {esc(CITIES[cheaper]["name"]) if cheaper else "either"} tends to win on price; if the {("prestige, amenities," if pr else "specific")} feel of {esc(CITIES[pr]["name"]) if pr else "a place"} is what you're after, that's where to lean. A Your Realty Link agent will help you compare real listings in both.</p>

 <div class="cta-block">
 <h3>Tour Both Before You Decide</h3>
 <p>We'll set up a same-day tour across {esc(an)} and {esc(bn)} so you can compare in person — with every active MIBOR MLS listing in both.</p>
 <div class="btn-group">
 <a href="{esc(search)}" class="btn btn-white" target="_blank" rel="noopener">Search Homes →</a>
 <a href="/schedule/" class="btn btn-outline">📅 Schedule a Tour</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Frequently Asked Questions — {esc(an)} vs {esc(bn)}</h2>
{faq_html}
 </section>

<section class="related-compares">
<h2>More Central Indiana Comparisons</h2>
<p>Weighing another pair of communities? Compare the metro's most-searched matchups:</p>
<div class="compare-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:12px">
 {rel_cards}
</div>
</section>
</main>

 <aside class="content-sidebar">
  <div class="sidebar-card">
 <div class="sidebar-card-header">Get in Touch</div>
 <div class="sidebar-card-body">
 <p>Weighing {esc(an)} vs {esc(bn)}? Fill out this quick form and we'll reach out.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="compare/{slug}">
 <input type="hidden" name="interest_type" value="Buy a Home">
 <label for="sf-name-{fid}">Name *</label>
 <input type="text" id="sf-name-{fid}" name="name" required placeholder="Your name">
 <label for="sf-phone-{fid}">Phone *</label>
 <input type="tel" id="sf-phone-{fid}" name="phone" required placeholder="317-555-1234">
 <label for="sf-email-{fid}">Email *</label>
 <input type="email" id="sf-email-{fid}" name="email" required placeholder="you@example.com">
 <button type="submit">Connect With an Agent →</button>
 <p class="form-note">No spam · No obligation · We respond personally</p>
 </form>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">The Two Cities</div>
 <div class="sidebar-card-body" style="padding:12px;">
 <a href="{au}" class="city-card">{esc(an)} Real Estate <span class="arrow">&rsaquo;</span></a>
 <a href="{bu}" class="city-card">{esc(bn)} Real Estate <span class="arrow">&rsaquo;</span></a>
 <a href="/compare/" class="city-card">All Comparisons <span class="arrow">&rsaquo;</span></a>
 </div>
 </div>
 </aside>
 </div>
</div>

{FOOTER}

{SCRIPTS}'''

# ── hub card copy (short, derived) ───────────────────────────────────────────
def hub_card(a, b):
    A, B = CITIES[a], CITIES[b]
    slug = "%s-vs-%s" % (a, b)
    pr = pricier(a, b)
    if pr: tail = "%s carries a premium; %s gives you more per dollar." % (CITIES[pr]["name"], CITIES[b if pr==a else a]["name"])
    else:  tail = "Closely matched on price — schools, commute, and feel decide it."
    desc = "%s vs %s: prices, schools, commute, and lifestyle side by side. %s" % (A["name"], B["name"], tail)
    return ('  <a href="/compare/%s/" class="home-feature-card">\n <h3>%s vs %s</h3>\n <p>%s</p>\n <span class="arrow">&rsaquo;</span>\n </a>\n'
            % (slug, esc(A["name"]), esc(B["name"]), esc(desc)))

# ── generate ─────────────────────────────────────────────────────────────────
# hand-authored compares to never overwrite (they're richer than the template)
PRESERVE = {"carmel-vs-fishers","fishers-vs-noblesville","zionsville-vs-carmel",
            "westfield-vs-fishers","avon-vs-brownsburg","greenwood-vs-franklin",
            "new-construction-vs-resale","realtor-vs-fsbo"}
os.makedirs(os.path.join(ROOT, "compare"), exist_ok=True)
made, skipped, newslugs = 0, 0, []
for a, b in MATCHUPS:
    slug = "%s-vs-%s" % (a, b)
    if slug in PRESERVE:
        skipped += 1; continue
    d = os.path.join(ROOT, "compare", slug); idxf = os.path.join(d, "index.html")
    firsttime = not os.path.exists(idxf)
    os.makedirs(d, exist_ok=True)
    _, htmlout = page(a, b)
    open(idxf, "w", encoding="utf-8").write(htmlout)
    made += 1
    if firsttime: newslugs.append((a, b, slug))

# add new cards to the compare hub (before the two topical cards)
hubf = os.path.join(ROOT, "compare", "index.html")
hub = open(hubf, encoding="utf-8").read()
anchor = '  <a href="/compare/new-construction-vs-resale/"'
if anchor in hub:
    add = "".join(hub_card(a, b) for a, b, s in newslugs if ('/compare/%s/' % s) not in hub)
    if add:
        hub = hub.replace(anchor, add + "\n" + anchor, 1)
        open(hubf, "w", encoding="utf-8").write(hub)

# sitemap
sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read(); blk = ""
for a, b in MATCHUPS:
    loc = "https://janetgiles.com/compare/%s-vs-%s/" % (a, b)
    if loc not in s:
        blk += "<url>\n  <loc>%s</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n" % loc
if blk:
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", blk + "</urlset>"))

print("compare pages: %d generated, %d preserved. Hub + sitemap +%d." % (made, skipped, blk.count("<url>")))
