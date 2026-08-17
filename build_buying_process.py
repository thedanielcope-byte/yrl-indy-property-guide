#!/usr/bin/env python3
"""Build /services/home-buying-process/ — the step-by-step buyer journey guide.
Reuses header/footer/hashes from a sibling service page."""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "services", "expired-listings", "index.html")
OUT_DIR = os.path.join(ROOT, "services", "home-buying-process")
URL = "https://janetgiles.com/services/home-buying-process/"

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
 ("Get Pre-Approved", "✅",
  "Talk to a lender before you shop. Pre-approval sets your real budget, shows sellers you're serious, and lets you move fast on the right home.",
  "Pre-approval guide", "/services/mortgage-pre-approval/"),
 ("Search &amp; Make an Offer", "📝",
  "Tour homes, find the one, and write a competitive offer &mdash; the right price, contingencies, and terms that win without overpaying.",
  "How to make a winning offer", "/blog/making-a-winning-offer-on-a-home-indianapolis/"),
 ("Inspections &amp; Under Contract", "🔍",
  "Offer accepted! Now the inspection, appraisal, and title work happen &mdash; and we negotiate repairs on your behalf.",
  "Under contract, explained", "/blog/home-inspection-under-contract-what-to-expect-indianapolis/"),
 ("Closing", "🔑",
  "Final walkthrough, Closing Disclosure, sign the paperwork, exchange funds &mdash; and get the keys to your new home.",
  "What to expect on closing day", "/blog/closing-day-what-to-expect-buying-a-home-indianapolis/"),
 ("After You Close", "🏡",
  "Set up utilities, file your Indiana homestead deduction, protect your investment &mdash; and settle in.",
  "New homeowner checklist", "/blog/new-homeowner-checklist-after-closing-indianapolis/"),
]
steps_html = "\n".join(
 f'''<div class="stop">
 <div class="stop-marker">{i}</div>
 <div class="stop-card">
  <span class="stop-emoji">{emoji}</span>
  <h4><a href="{url}">{t}</a></h4>
  <p>{blurb}</p>
  <a class="stop-more" href="{url}">{more} &rarr;</a>
 </div>
</div>'''
 for i,(t,emoji,blurb,more,url) in enumerate(STEPS, 1))

faqs = [
 ("How long does it take to buy a home in Indianapolis?", "From accepted offer to closing typically runs 30&ndash;45 days when financing with a mortgage; cash purchases can close faster. Finding the right home varies &mdash; some buyers find it in a weekend, others take a few months."),
 ("Do I really need to get pre-approved first?", "Yes. Pre-approval tells you your real budget, makes your offers credible to sellers, and lets you act quickly. Most sellers won't seriously consider an offer without a pre-approval letter attached."),
 ("What does it cost me to use a buyer's agent?", "In many Central Indiana transactions, buyer representation costs you little or nothing out of pocket when the seller offers compensation &mdash; but that's negotiated per deal, and as of mid-2025 buyers sign a representation agreement up front. We'll walk you through exactly how it works before you commit."),
 ("What happens if the inspection finds problems?", "You have options: ask the seller to make repairs, request a credit or price reduction, or &mdash; if it's serious &mdash; walk away within your inspection contingency. We help you weigh what's worth negotiating and what's normal for a home's age."),
]
def strip(t): return re.sub("<[^>]+>|&[a-z]+;|&#\\d+;", lambda m: {"&ldquo;":'"',"&rdquo;":'"',"&mdash;":"-","&ndash;":"-","&amp;":"&"}.get(m.group(0),"") if m.group(0).startswith("&") else "", t)
faq_html = "\n".join(f'<details class="faq-item">\n<summary>{q}</summary>\n<div class="faq-answer"><p>{a}</p></div>\n</details>' for q,a in faqs)
faq_schema = ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }' % (json.dumps(strip(q)), json.dumps(strip(a))) for q,a in faqs)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>How to Buy a Home in Indianapolis: The Step-by-Step Process | Your Realty Link</title>
 <meta name="description" content="The home buying process in Central Indiana, step by step: get pre-approved, make an offer, inspections and under contract, closing, and after you close.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="How to Buy a Home in Indianapolis: The Step-by-Step Process | Your Realty Link">
 <meta property="og:description" content="From pre-approval to after you close — the Central Indiana home buying journey, explained step by step.">
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
 {{ "@type": "ListItem", "position": 3, "name": "Home Buying Process", "item": "{URL}" }} ] }}
 ] }}
 </script>
 {FONTS}
 <style>
.service-wrap {{ max-width: 780px; margin: 0 auto; padding: 44px 0; }}
/* Illustrated "road" journey: a vertical road with a driving car and alternating stops */
.roadmap {{ position: relative; margin: 2rem 0 1rem; padding: 6px 0; }}
.road {{ position: absolute; top: 0; bottom: 0; left: 50%; width: 52px; transform: translateX(-50%); background: #3b4048; border-radius: 26px; box-shadow: inset 0 0 0 3px #2d3138, 0 4px 16px rgba(0,0,0,.12); z-index: 0; }}
.road::before {{ content: ''; position: absolute; left: 50%; top: 14px; bottom: 14px; width: 4px; transform: translateX(-50%); background: repeating-linear-gradient(#ffd24a 0 20px, transparent 20px 40px); border-radius: 2px; }}
.road .car {{ position: absolute; left: 50%; top: 0; transform: translateX(-50%) rotate(90deg); font-size: 30px; line-height: 1; filter: drop-shadow(0 4px 5px rgba(0,0,0,.35)); animation: drive 12s linear infinite; }}
@keyframes drive {{ 0% {{ top: -3%; }} 90% {{ top: 101%; }} 100% {{ top: 101%; }} }}
@media (prefers-reduced-motion: reduce) {{ .road .car {{ animation: none; top: 0; }} }}
.stop {{ position: relative; display: grid; grid-template-columns: 1fr 52px 1fr; align-items: center; margin-bottom: 30px; z-index: 1; }}
.stop:last-child {{ margin-bottom: 0; }}
.stop-marker {{ grid-column: 2; justify-self: center; width: 40px; height: 40px; border-radius: 50%; background: #13294a; color: #fff; font-weight: 800; font-size: 16px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 4px #fff, 0 0 0 6px #c03926; z-index: 2; }}
.stop-card {{ background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 15px 18px 17px; box-shadow: 0 4px 16px rgba(0,0,0,.08); text-decoration: none; display: block; transition: transform .15s ease, box-shadow .15s ease; }}
.stop-card:hover {{ transform: translateY(-3px); box-shadow: 0 12px 28px rgba(0,0,0,.15); }}
.stop-emoji {{ font-size: 22px; }}
.stop-card h4 {{ margin: 3px 0 5px; font-size: 1.08rem; }}
.stop-card h4 a {{ color: #13294a; text-decoration: none; }}
.stop-card:hover h4 a {{ color: var(--red); }}
.stop-card .stop-more {{ text-decoration: none; display: inline-block; }}
.stop-card p {{ margin: 0 0 9px; font-size: 13.5px; color: var(--mid); line-height: 1.6; }}
.stop-card .stop-more {{ color: var(--red); font-weight: 700; font-size: 13px; }}
.stop:nth-child(odd) .stop-card {{ grid-column: 1; text-align: right; }}
.stop:nth-child(even) .stop-card {{ grid-column: 3; text-align: left; }}
@media (max-width: 700px) {{
 .road {{ left: 26px; }}
 .stop {{ grid-template-columns: 52px 1fr; }}
 .stop-marker {{ grid-column: 1; }}
 .stop:nth-child(odd) .stop-card, .stop:nth-child(even) .stop-card {{ grid-column: 2; text-align: left; }}
}}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/services/">Services</a> <span>&rsaquo;</span> Home Buying Process</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>How to Buy a Home in Indianapolis</h1>
 <p class="hero-sub">Buying a home has a rhythm to it. Here's the whole journey &mdash; from pre-approval to the day after you get the keys &mdash; so you always know what's next.</p>
 <div class="hero-badges">
 <span class="hero-badge">✅ Pre-Approval</span>
 <span class="hero-badge">📝 Offer</span>
 <span class="hero-badge">🔍 Inspection</span>
 <span class="hero-badge">🔑 Closing</span>
 </div>
 </div>
</section>

<div class="container">
 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">Buying a home in Central Indiana follows five steps: get pre-approved, search and make an offer, complete inspections while under contract, close, and settle in after closing. Your Realty Link guides you through every step &mdash; call 317-997-7404.</p>
 <dl class="qa-facts">
 <div><dt>Contract to close</dt><dd>Typically 30&ndash;45 days</dd></div>
 <div><dt>First step</dt><dd><a href="/services/mortgage-pre-approval/">Get pre-approved</a></dd></div>
 <div><dt>Financing</dt><dd><a href="/services/mortgages/">Mortgages &amp; calculator</a></dd></div>
 <div><dt>Call</dt><dd><a href="tel:3179977404">317-997-7404</a></dd></div>
 </dl>
</div>
<!-- QA-END -->

 <div class="service-wrap">

 <p>Whether it's your first home or your fifth, the process can feel like a lot of moving parts. The good news: it's a well-worn path, and with the right agent it's genuinely manageable. Here is the Central Indiana home-buying journey, step by step &mdash; and how <strong>Your Realty Link</strong> helps at each stage.</p>

 <div class="roadmap">
 <div class="road" aria-hidden="true"><span class="car">🚗</span></div>
{steps_html}
 </div>

 <div class="cta-block">
 <h3>Ready to Start? Let's Talk</h3>
 <p>Wherever you are in the process &mdash; just curious, getting pre-approved, or ready to tour &mdash; we'll meet you there. No pressure, no obligation.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call: 317-997-7404</a>
 <a href="/services/mortgages/" class="btn btn-outline">Financing &amp; Calculator →</a>
 <a href="/search/" class="btn btn-outline">Search Homes →</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Home Buying FAQs</h2>
{faq_html}
 </section>

 <hr class="divider">
 <h3>Keep Exploring</h3>
 <ul>
 <li><a href="/first-time-home-buyers-indianapolis/">First-Time Home Buyers</a></li>
 <li><a href="/services/mortgages/">Mortgages &amp; Calculator</a></li>
 <li><a href="/services/buyer-representation/">Buyer Representation</a></li>
 <li><a href="/services/new-construction/">New Construction</a></li>
 <li><a href="/vendors/">Preferred Vendors</a></li>
 </ul>

 </div>
</div>

<section class="cta-form-section">
 <div class="container">
 <h2>Have a Question About Buying?</h2>
 <p>Send a note and a Your Realty Link agent will walk you through your next step.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="services/home-buying-process">
 <input type="hidden" name="interest_type" value="Home Buying Process">
 <div class="form-row">
 <div><label for="sv-name">Name *</label><input type="text" id="sv-name" name="name" required placeholder="Your name"></div>
 <div><label for="sv-phone">Phone *</label><input type="tel" id="sv-phone" name="phone" required placeholder="317-555-1234"></div>
 </div>
 <label for="sv-email">Email *</label>
 <input type="email" id="sv-email" name="email" required placeholder="you@example.com">
 <label for="sv-message">What stage are you at?</label>
 <textarea id="sv-message" name="message" placeholder="Just starting, getting pre-approved, ready to tour…"></textarea>
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
print("built /services/home-buying-process/")
