#!/usr/bin/env python3
"""Build /services/preferred-lenders/ from lenders.json.

Reuses an existing service page's <header>, <footer>, and asset-version links so
nav/footer/hashes always match the live site. Re-run after editing lenders.json.
Source of truth for the data: the YRL hub vendors list (💰 Lenders & Mortgage).

Usage:  python3 build_lenders.py
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "services", "expired-listings", "index.html")   # any current service page
OUT_DIR = os.path.join(ROOT, "services", "preferred-lenders")
URL = "https://janetgiles.com/services/preferred-lenders/"

src = open(TPL, encoding="utf-8").read()
def grab(pat):
    m = re.search(pat, src, re.S)
    if not m: raise SystemExit("extract failed: " + pat[:40])
    return m.group(0)
FONTS = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

lenders = json.load(open(os.path.join(ROOT, "lenders.json"), encoding="utf-8"))

def esc(s): return html.escape(str(s or ""), quote=True)
def weburl(w):
    w = (w or "").strip()
    return w if w.startswith("http") else "https://" + w

def card(v):
    site = v.get("website", "")
    site_html = (f'<a class="ld-row" href="{esc(weburl(site))}" target="_blank" rel="noopener">'
                 f'<span class="ld-ic">&#127760;</span>{esc(site)}</a>') if site else ""
    phone = v.get("phone", "")
    phone_html = (f'<a class="ld-row" href="tel:{esc(re.sub(r"[^0-9]","",phone))}">'
                  f'<span class="ld-ic">&#128222;</span>{esc(phone)}</a>') if phone else ""
    email = v.get("email", "")
    email_html = (f'<a class="ld-row" href="mailto:{esc(email)}">'
                  f'<span class="ld-ic">&#9993;&#65039;</span>{esc(email)}</a>') if email else ""
    notes = v.get("notes", "")
    notes_html = f'<p class="ld-notes">{esc(notes)}</p>' if notes else ""
    return (f'<div class="lender-card">\n'
            f'  <h3>{esc(v.get("company"))}</h3>\n'
            f'  <p class="ld-contact">{esc(v.get("contact"))}</p>\n'
            f'  <div class="ld-links">{phone_html}{email_html}{site_html}</div>\n'
            f'  {notes_html}\n</div>')

cards = "\n".join(card(v) for v in lenders)

# FAQ (kept in sync with schema below)
faqs = [
 ("Do I have to use one of these lenders?",
  "No. This list is a convenience, not a requirement. You're welcome to work with any lender you choose. We share these names because our clients have had great experiences with them — but the choice is always yours."),
 ("Does Your Realty Link get paid for referring these lenders?",
  "No. We receive no compensation, referral fees, or kickbacks for recommending any lender on this page. We simply want you working with people we trust."),
 ("Why should I get pre-approved before I start shopping?",
  "A pre-approval tells you exactly what you can afford, makes your offer far stronger when you find the right home, and lets you move quickly in a competitive market. It's the first step we recommend after you've chosen your agent and signed your Buyer Representation Agreement."),
]
faq_html = "\n".join(
 f'<details class="faq-item">\n<summary>{esc(q)}</summary>\n<div class="faq-answer"><p>{esc(a)}</p></div>\n</details>'
 for q, a in faqs)
faq_schema = ",\n".join(
 '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
 % (json.dumps(q), json.dumps(a)) for q, a in faqs)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Preferred Mortgage Lenders in Indianapolis | Your Realty Link</title>
 <meta name="description" content="Your Realty Link's list of trusted local mortgage lenders and loan officers across Central Indiana. Get pre-approved and choose a lender we recommend. Call 317-997-7404.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="Preferred Mortgage Lenders in Indianapolis | Your Realty Link">
 <meta property="og:description" content="Trusted local mortgage lenders and loan officers recommended by Your Realty Link across Central Indiana.">
 <meta property="og:url" content="{URL}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-home.jpg">
 <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:image" content="https://janetgiles.com/assets/img/og-home.jpg">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{
 "@context": "https://schema.org",
 "@graph": [
 {{ "@type": "WebPage", "url": "{URL}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"] }} }},
 {{
 "@type": ["LocalBusiness", "RealEstateAgent"],
 "name": "Your Realty Link", "url": "https://yourrealtylink.com", "logo": "/assets/img/yrl-logo.png",
 "telephone": "317-997-7404", "email": "csirealtyteam@yourrealtylink.com",
 "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US" }},
 "areaServed": "Indianapolis, Indiana and Central Indiana"
 }},
 {{ "@type": "FAQPage", "mainEntity": [
 {faq_schema}
 ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Services", "item": "https://janetgiles.com/services/" }},
 {{ "@type": "ListItem", "position": 3, "name": "Preferred Lenders", "item": "{URL}" }}
 ] }}
 ]
 }}
 </script>
 {FONTS}
 <style>
.service-wrap {{ max-width: 900px; margin: 0 auto; padding: 48px 0; }}
.lender-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; margin: 8px 0 8px; }}
.lender-card {{ background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 20px 22px; box-shadow: 0 2px 10px rgba(0,0,0,.05); }}
.lender-card h3 {{ font-size: 1.05rem; color: #13294a; margin: 0 0 3px; }}
.lender-card .ld-contact {{ font-size: .86rem; color: var(--mid); font-weight: 600; margin: 0 0 12px; }}
.lender-card .ld-links {{ display: flex; flex-direction: column; gap: 7px; }}
.lender-card .ld-row {{ display: flex; align-items: center; gap: 9px; font-size: .9rem; color: var(--red); font-weight: 600; text-decoration: none; word-break: break-word; }}
.lender-card .ld-row:hover {{ text-decoration: underline; }}
.lender-card .ld-ic {{ width: 16px; flex-shrink: 0; filter: grayscale(1); opacity: .7; }}
.lender-card .ld-notes {{ font-size: .78rem; color: var(--text-muted, #9ca3af); line-height: 1.5; margin: 14px 0 0; padding-top: 12px; border-top: 1px solid var(--border); }}
.ld-disclaimer {{ background: var(--light); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; font-size: .88rem; color: var(--mid); line-height: 1.6; margin: 8px 0 28px; }}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container">
 <a href="/">Home</a>
 <span>&rsaquo;</span>
 <a href="/services/">Services</a>
 <span>&rsaquo;</span>
 Preferred Lenders
 </div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>Preferred Mortgage Lenders in <em>Central Indiana</em></h1>
 <p class="hero-sub">Getting pre-approved is the first step to buying a home. These are local loan officers our clients know and trust — pick one and get started.</p>
 <div class="hero-badges">
 <span class="hero-badge">📍 Indianapolis &amp; Central Indiana</span>
 <span class="hero-badge">🤝 Trusted Local Lenders</span>
 <span class="hero-badge">📞 317-997-7404</span>
 </div>
 </div>
</section>

<div class="container">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">These are the local mortgage lenders and loan officers Your Realty Link recommends across Central Indiana. Getting pre-approved is the first step after you choose an agent and sign your Buyer Representation Agreement. You're free to use any lender you like. Call 317-997-7404.</p>
 <dl class="qa-facts">
 <div><dt>Area served</dt><dd>Indianapolis &amp; Central Indiana</dd></div>
 <div><dt>Lenders listed</dt><dd>{len(lenders)} trusted local loan officers</dd></div>
 <div><dt>Call</dt><dd><a href="tel:3179977404">317-997-7404</a></dd></div>
 <div><dt>Next step</dt><dd><a href="/services/mortgage-pre-approval/">Get pre-approved &rarr;</a></dd></div>
 </dl>
</div>
<!-- QA-END -->

 <div class="service-wrap">

 <p>Before you start touring homes, the smartest first move is getting <a href="/services/mortgage-pre-approval/">pre-approved</a>. A pre-approval shows you exactly what you can afford, makes your offer far stronger, and lets you move fast when you find the right home. The lenders below are local loan officers our clients have worked with and had great experiences with — reach out to any of them to get started.</p>

 <p class="ld-disclaimer"><strong>A quick note:</strong> Your Realty Link shares this list purely as a convenience. You're welcome to use any lender you choose — and we receive <strong>no compensation, referral fees, or kickbacks</strong> for recommending anyone on this page. These are simply people we trust to take good care of you.</p>

 <div class="lender-grid">
{cards}
 </div>

 <!-- PRIMARY CTA -->
 <div class="cta-block">
 <h3>Not Sure Which Lender to Call?</h3>
 <p>Tell us a little about your situation and we'll point you to the loan officer who fits best — and help you take the next step toward your home.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call 317-997-7404</a>
 <a href="/contact/" class="btn btn-outline">Ask Us Anything →</a>
 <a href="/services/first-time-home-buyers/" class="btn btn-outline">First-Time Buyer Guide</a>
 </div>
 </div>

 <!-- FAQ -->
 <section class="faq-section">
 <h2>Frequently Asked Questions — Preferred Lenders</h2>
{faq_html}
 </section>

 <hr class="divider">
 <h3>Related Services &amp; Resources</h3>
 <ul>
 <li><a href="/services/mortgage-pre-approval/">Mortgage Pre-Approval in Indianapolis</a></li>
 <li><a href="/services/first-time-home-buyers/">First-Time Home Buyers Guide</a></li>
 <li><a href="/services/buyer-representation/">Buyer Representation — What Your Realty Link Offers</a></li>
 <li><a href="/services/down-payment-assistance/">Down Payment Assistance in Indiana</a></li>
 <li><a href="/services/mortgage-calculator/">Mortgage Calculator</a></li>
 </ul>

 </div>
</div>

<section class="cta-form-section">
 <div class="container">
 <h2>Ready to Take the Next Step?</h2>
 <p>Fill out the form below and a Your Realty Link agent will reach out — no obligation, no pressure.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="services/preferred-lenders">
 <input type="hidden" name="interest_type" value="Pre-Approval / Lenders">
 <div class="form-row">
 <div>
 <label for="sv-name">Name *</label>
 <input type="text" id="sv-name" name="name" required placeholder="Your name">
 </div>
 <div>
 <label for="sv-phone">Phone *</label>
 <input type="tel" id="sv-phone" name="phone" required placeholder="317-555-1234">
 </div>
 </div>
 <label for="sv-email">Email *</label>
 <input type="email" id="sv-email" name="email" required placeholder="you@example.com">
 <label for="sv-message">How can we help?</label>
 <textarea id="sv-message" name="message" placeholder="Tell us where you are in the process…"></textarea>
 <button type="submit">Send Message →</button>
 <p class="form-note">No spam · No obligation · We respond personally</p>
 </form>
 </div>
</section>

{FOOTER}

{SCRIPTS}'''

os.makedirs(OUT_DIR, exist_ok=True)
open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page)

# sitemap (idempotent)
sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read()
if URL not in s:
    blk = f"<url>\n  <loc>{URL}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n"
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", blk + "</urlset>"))
    print("added sitemap entry")
print(f"built /services/preferred-lenders/ with {len(lenders)} lenders")
