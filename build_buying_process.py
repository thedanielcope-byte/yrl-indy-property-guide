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

STEPS = [
 ("Get Pre-Approved", "Before you tour a single home, talk to a lender and get pre-approved. It tells you your real budget, shows sellers you're serious, and lets you move fast when the right home appears. Your lender will look at your income, debts, credit, and down payment. Not sure where to start? Use our <a href='/services/mortgages/'>mortgage calculator and financing hub</a> or our list of <a href='/vendors/#lenders-mortgage'>preferred local lenders</a>, and see the <a href='/services/mortgage-pre-approval/'>pre-approval guide</a>."),
 ("Search &amp; Make an Offer", "Now the fun part &mdash; touring homes and finding the one. When you do, your Your Realty Link agent helps you craft a competitive offer: the right price, contingencies (financing, inspection, appraisal), earnest money, and closing timeline. In a tight market, strategy matters, and having an experienced <a href='/services/buyer-representation/'>buyer's agent</a> on your side is what turns a good home into an accepted offer."),
 ("Inspections &amp; Under Contract", "Once your offer is accepted, you're &ldquo;under contract&rdquo; and the clock starts. This is when you complete your <strong>home inspection</strong> (we'll connect you with a trusted <a href='/vendors/#home-inspectors'>inspector</a>), the lender orders the <strong>appraisal</strong>, and the <strong>title company</strong> researches the property. If the inspection turns up issues, we negotiate repairs or credits on your behalf. Stay responsive with your lender &mdash; this is where financing gets finalized."),
 ("Closing", "A few days before closing you'll do a <strong>final walkthrough</strong> to confirm the home's condition, and you'll receive your <strong>Closing Disclosure</strong> showing your final numbers. Review your <a href='/services/closing-costs-buyers/'>closing costs</a> ahead of time so there are no surprises. At the closing table (or a mobile signing), you sign, funds are exchanged, and &mdash; the best part &mdash; you get the keys."),
 ("After You Close", "Congratulations, you're a homeowner! A few things to knock out: set up your <a href='/vendors/#utilities'>utilities</a> and change your address, and &mdash; important in Indiana &mdash; <strong>file your homestead deduction</strong> with the county auditor to lower your property taxes (see our <a href='/blog/indiana-property-tax-deductions-seniors/'>deductions guide</a>). Then settle in. And remember: we're here long after closing for maintenance referrals, market questions, and whenever you're ready for the next move."),
]
steps_html = "\n".join(
 f'<li>\n<div class="step-num">{n}</div>\n<div class="step-content"><h4>{t}</h4><p>{b}</p></div>\n</li>'
 for n,(t,b) in enumerate(STEPS, 1))

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
.step-list {{ counter-reset: steps; list-style: none; padding: 0; margin: 1.5rem 0; }}
.step-list li {{ display: flex; gap: 18px; align-items: flex-start; margin-bottom: 22px; padding-bottom: 22px; border-bottom: 1px solid var(--border); }}
.step-list li:last-child {{ border: none; }}
.step-num {{ background: var(--red); color: var(--white); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; flex-shrink: 0; margin-top: 2px; }}
.step-content h4 {{ margin: 2px 0 6px; font-size: 1.12rem; color: #13294a; }}
.step-content p {{ font-size: 14.5px; color: var(--mid); margin: 0; line-height: 1.65; }}
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

 <ol class="step-list">
{steps_html}
 </ol>

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
