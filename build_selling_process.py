#!/usr/bin/env python3
"""Build /services/home-selling-process/ — the step-by-step seller journey guide.
Mirror of build_buying_process.py (same .journey winding-road roadmap format).
Reuses header/footer/hashes from a sibling service page."""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "services", "expired-listings", "index.html")
OUT_DIR = os.path.join(ROOT, "services", "home-selling-process")
URL = "https://janetgiles.com/services/home-selling-process/"

src = open(TPL, encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

# (title, emoji, short blurb, deeper-dive label, deeper-dive URL)
STEPS = [
 ("Get Your Home's True Value", "💰",
  "It starts with a real comparative market analysis &mdash; grounded in what comparable homes actually sold for nearby, not an online guess. Price it right from day one and it sells faster, for more.",
  "Free home valuation", "/services/free-home-valuation/"),
 ("Prep &amp; Stage to Sell", "🧹",
  "Declutter, handle the small repairs buyers notice, boost curb appeal, and stage so your home photographs and shows at its best. First impressions drive offers.",
  "Home staging tips", "/services/home-staging/"),
 ("List &amp; Market", "📣",
  "We price it right, shoot professional photography, and put your home in front of buyers across the MIBOR MLS and every major search site &mdash; plus our own network.",
  "Our seller services", "/services/sell-my-home/"),
 ("Showings, Offers &amp; Negotiation", "🤝",
  "As buyers tour and offers come in, we help you weigh price, terms, financing strength, and contingencies &mdash; then negotiate the best deal, not just the highest number.",
  "How we price your home", "/services/pricing-your-home/"),
 ("Inspection to Closing", "🔑",
  "We manage inspection items, coordinate the appraisal and title work, and guide you through closing &mdash; so the sale actually gets to the finish line.",
  "Seller closing checklist", "/services/seller-closing-checklist/"),
]
steps_html = "\n".join(
 f'''<div class="jstep">
 <div class="jnum">{i}</div>
 <div class="jstep-card">
  <span class="jstep-emoji">{emoji}</span>
  <h4><a href="{url}">{t}</a></h4>
  <p>{blurb}</p>
  <a class="jstep-more" href="{url}">{more} &rarr;</a>
 </div>
</div>'''
 for i,(t,emoji,blurb,more,url) in enumerate(STEPS, 1))

ROAD_D = "M66,0 L66,10 C66,20 34,20 34,30 C34,40 66,40 66,50 C66,60 34,60 34,70 C34,80 66,80 66,90 L66,100"
ROAD_SVG = (f'<svg class="journey-road" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
            f'<path class="road-base" d="{ROAD_D}"/><path class="road-line" d="{ROAD_D}"/></svg>')

faqs = [
 ("How long does it take to sell a home in Indianapolis?", "Time on market varies by neighborhood, price, and condition. Well-priced, well-prepared homes in desirable Central Indiana areas often go under contract quickly &mdash; and we'll give you realistic expectations for your specific home and market before you list."),
 ("How do you decide what to list my home for?", "With a comparative market analysis (CMA) built on real, recent sales of comparable homes near you &mdash; not an online estimate. Pricing is the single most important decision when you sell, and getting it right from day one matters most."),
 ("What does it cost to sell with Your Realty Link?", "Commission and fee structures vary and are set up front, in writing, before you list. Call 317-997-7404 for a straightforward conversation about what's included and what it costs &mdash; we believe in transparency."),
 ("Do I need to make repairs or stage before listing?", "Not always &mdash; but small fixes and light staging usually pay for themselves in a faster sale and stronger offers. We'll walk your home with you and recommend only what actually moves the needle."),
]
def strip(t): return re.sub("<[^>]+>|&[a-z]+;|&#\\d+;", lambda m: {"&ldquo;":'"',"&rdquo;":'"',"&mdash;":"-","&ndash;":"-","&amp;":"&"}.get(m.group(0),"") if m.group(0).startswith("&") else "", t)
faq_html = "\n".join(f'<details class="faq-item">\n<summary>{q}</summary>\n<div class="faq-answer"><p>{a}</p></div>\n</details>' for q,a in faqs)
faq_schema = ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }' % (json.dumps(strip(q)), json.dumps(strip(a))) for q,a in faqs)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>How to Sell a Home in Indianapolis: The Step-by-Step Process | Your Realty Link</title>
 <meta name="description" content="The home selling process in Central Indiana, step by step: get a real valuation, prep and stage, list and market, review offers, and close with confidence.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="How to Sell a Home in Indianapolis: The Step-by-Step Process | Your Realty Link">
 <meta property="og:description" content="From your first valuation to the closing table — the Central Indiana home selling journey, explained step by step.">
 <meta property="og:url" content="{URL}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{URL}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead",".qa-facts"] }} }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" }},
 {{ "@type": "FAQPage", "mainEntity": [ {faq_schema} ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Services", "item": "https://janetgiles.com/services/" }},
 {{ "@type": "ListItem", "position": 3, "name": "Home Selling Process", "item": "{URL}" }} ] }}
 ] }}
 </script>
 {FONTS}
 <style>
.service-wrap {{ max-width: 780px; margin: 0 auto; padding: 44px 0; }}
/* Winding-road journey: an S-curve road (auto-sizes to content) with tiles alternating along the curve */
.journey {{ position: relative; margin: 2.2rem 0 1rem; }}
.journey-road {{ position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; overflow: visible; }}
.journey-road .road-base {{ fill: none; stroke: #3b4048; stroke-width: 46; stroke-linecap: butt; stroke-linejoin: round; vector-effect: non-scaling-stroke; }}
.journey-road .road-line {{ fill: none; stroke: #ffd24a; stroke-width: 3; stroke-dasharray: 16 15; stroke-linecap: butt; vector-effect: non-scaling-stroke; }}
.jstep {{ position: relative; z-index: 1; margin-bottom: 26px; min-height: 118px; }}
.jstep:last-child {{ margin-bottom: 0; }}
.jstep-card {{ position: relative; width: 62%; background: #fff; border: 1px solid var(--border); border-radius: 16px; padding: 16px 20px 18px; box-shadow: 0 6px 22px rgba(0,0,0,.12); display: block; transition: transform .15s ease, box-shadow .15s ease; }}
.jstep-card:hover {{ transform: translateY(-3px); box-shadow: 0 14px 30px rgba(0,0,0,.17); }}
.jstep:nth-child(even) .jstep-card {{ margin-left: 38%; }}
.jnum {{ position: absolute; top: 50%; transform: translate(-50%, -50%); width: 46px; height: 46px; border-radius: 50%; background: #13294a; color: #fff; font-weight: 800; font-size: 18px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 5px #fff, 0 0 0 7px #c03926; z-index: 3; }}
.jstep:nth-child(odd) .jnum {{ left: 66%; }}
.jstep:nth-child(even) .jnum {{ left: 34%; }}
.jstep-emoji {{ font-size: 23px; line-height: 1; }}
.jstep-card h4 {{ margin: 4px 0 5px; font-size: 1.1rem; }}
.jstep-card h4 a {{ color: #13294a; text-decoration: none; }}
.jstep-card:hover h4 a {{ color: var(--red); }}
.jstep-card p {{ margin: 0 0 10px; font-size: 13.5px; color: var(--mid); line-height: 1.6; }}
.jstep-card .jstep-more {{ color: var(--red); font-weight: 700; font-size: 13px; text-decoration: none; }}
@media (max-width: 720px) {{
 .journey-road {{ display: none; }}
 .jstep {{ min-height: 0; margin-bottom: 16px; }}
 .jstep-card, .jstep:nth-child(even) .jstep-card {{ width: 100%; margin-left: 0; padding-left: 56px; }}
 .jnum, .jstep:nth-child(odd) .jnum, .jstep:nth-child(even) .jnum {{ left: 28px; top: 30px; transform: translate(-50%, 0); width: 40px; height: 40px; font-size: 16px; }}
}}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/services/">Services</a> <span>&rsaquo;</span> Home Selling Process</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>How to Sell a Home in Indianapolis</h1>
 <p class="hero-sub">Selling has a rhythm to it. Here's the whole journey &mdash; from your first valuation to the closing table &mdash; so you always know what's next.</p>
 <div class="hero-badges">
 <span class="hero-badge">💰 Valuation</span>
 <span class="hero-badge">🧹 Prep</span>
 <span class="hero-badge">📣 Market</span>
 <span class="hero-badge">🔑 Closing</span>
 </div>
 </div>
</section>

<div class="container">
 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">Selling a home in Central Indiana follows five steps: get a real valuation, prep and stage, list and market, review offers and negotiate, then close. Your Realty Link guides you through every step &mdash; call 317-997-7404.</p>
 <dl class="qa-facts">
 <div><dt>Contract to close</dt><dd>Typically 30&ndash;45 days</dd></div>
 <div><dt>First step</dt><dd><a href="/services/free-home-valuation/">Free home valuation</a></dd></div>
 <div><dt>Pricing</dt><dd><a href="/services/pricing-your-home/">Pricing your home</a></dd></div>
 <div><dt>Call</dt><dd><a href="tel:3179977404">317-997-7404</a></dd></div>
 </dl>
</div>
<!-- QA-END -->

 <div class="service-wrap">

 <p>Whether it's your first sale or your fifth, listing a home can feel like a lot of moving parts. The good news: it's a well-worn path, and with the right agent it's genuinely manageable. Here is the Central Indiana home-selling journey, step by step &mdash; and how <strong>Your Realty Link</strong> helps at each stage.</p>

 <div class="journey">
 {ROAD_SVG}
{steps_html}
 </div>

 <div class="cta-block">
 <h3>Thinking About Selling? Let's Talk</h3>
 <p>Wherever you are &mdash; just curious what your home is worth, or ready to list &mdash; we'll meet you there. Free, no pressure, no obligation.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call: 317-997-7404</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline">Free Home Valuation →</a>
 <a href="/services/sell-my-home/" class="btn btn-outline">Our Seller Services →</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Home Selling FAQs</h2>
{faq_html}
 </section>

 <hr class="divider">
 <h3>Keep Exploring</h3>
 <ul>
 <li><a href="/services/sell-my-home/">Sell My Home</a></li>
 <li><a href="/services/free-home-valuation/">Free Home Valuation</a></li>
 <li><a href="/services/pricing-your-home/">Pricing Your Home</a></li>
 <li><a href="/services/home-staging/">Home Staging</a></li>
 <li><a href="/services/seller-closing-checklist/">Seller Closing Checklist</a></li>
 </ul>

 </div>
</div>

<section class="cta-form-section">
 <div class="container">
 <h2>Have a Question About Selling?</h2>
 <p>Send a note and a Your Realty Link agent will walk you through your next step.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="services/home-selling-process">
 <input type="hidden" name="interest_type" value="Home Selling Process">
 <div class="form-row">
 <div><label for="sv-name">Name *</label><input type="text" id="sv-name" name="name" required placeholder="Your name"></div>
 <div><label for="sv-phone">Phone *</label><input type="tel" id="sv-phone" name="phone" required placeholder="317-555-1234"></div>
 </div>
 <label for="sv-email">Email *</label>
 <input type="email" id="sv-email" name="email" required placeholder="you@example.com">
 <label for="sv-message">What stage are you at?</label>
 <textarea id="sv-message" name="message" placeholder="Just curious, getting a valuation, ready to list…"></textarea>
 <button type="submit">Send Message →</button>
 <p class="form-note">No spam · No obligation · We respond personally</p>
 </form>
 </div>
</section>

{FOOTER}

{SCRIPTS}'''

os.makedirs(OUT_DIR, exist_ok=True)
open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page)
sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read()
if URL not in s:
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", f"<url>\n  <loc>{URL}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.7</priority>\n</url>\n</urlset>"))
    print("added sitemap entry")
print("built /services/home-selling-process/")
