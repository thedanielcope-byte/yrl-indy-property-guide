#!/usr/bin/env python3
"""Build /services/mortgages/ — buyer financing hub with an interactive payment
calculator, loan types, pre-approval/DPA links, and preferred lenders.
Reuses header/footer/hashes from a sibling service page."""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "services", "expired-listings", "index.html")
OUT_DIR = os.path.join(ROOT, "services", "mortgages")
URL = "https://janetgiles.com/services/mortgages/"

src = open(TPL, encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

faqs = [
 ("How much home can I afford in Indianapolis?",
  "A common guideline is keeping your total housing payment near 28% of gross monthly income, but the real answer depends on your debts, down payment, rate, and comfort level. The calculator above gives a quick payment estimate; a lender pre-approval gives you the real number. We're glad to connect you with a trusted local lender."),
 ("What credit score do I need to buy a home?",
  "It varies by loan. FHA loans can go as low as the 500s&ndash;580 with a larger down payment; conventional loans usually want 620+; and the best rates go to scores around 740+. Do not assume you can't qualify &mdash; a lender can tell you exactly where you stand and what to improve."),
 ("How much do I need for a down payment?",
  "Less than most people think. Conventional loans can go as low as 3% down, FHA is 3.5%, and VA and USDA can be 0% down for those who qualify. Indiana also has down payment assistance programs. See our <a href='/services/down-payment-assistance/'>down payment assistance</a> guide."),
 ("Should I get pre-approved before I start looking?",
  "Yes. A pre-approval tells you your real budget, shows sellers you're serious, and lets you move fast when you find the right home. It's the first real step &mdash; start with our <a href='/services/mortgage-pre-approval/'>pre-approval guide</a>."),
]
def strip(t): return re.sub("<[^>]+>|&[a-z]+;|&#\\d+;", lambda m: {"&ndash;":"-","&amp;":"&"}.get(m.group(0),"") if m.group(0).startswith("&") else "", t)
faq_html = "\n".join(f'<details class="faq-item">\n<summary>{q}</summary>\n<div class="faq-answer"><p>{a}</p></div>\n</details>' for q,a in faqs)
faq_schema = ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }' % (json.dumps(strip(q)), json.dumps(strip(a))) for q,a in faqs)

CALC = '''
<div class="mtg-calc">
 <h2 style="margin-top:0;">Mortgage Payment Calculator</h2>
 <p style="color:#6e6e70;font-size:.92rem;margin-top:0;">Estimate your monthly principal &amp; interest. Taxes, insurance, HOA, and mortgage insurance are not included.</p>
 <div class="mc-grid">
 <label>Home price <span>$</span><input type="number" id="mc-price" value="300000" min="0" step="1000"></label>
 <label>Down payment <span>%</span><input type="number" id="mc-down" value="10" min="0" max="100" step="1"></label>
 <label>Interest rate <span>%</span><input type="number" id="mc-rate" value="6.5" min="0" max="25" step="0.05"></label>
 <label>Loan term <span>yrs</span><input type="number" id="mc-term" value="30" min="1" max="40" step="1"></label>
 </div>
 <div class="mc-out">
 <div class="mc-pay"><span class="mc-num" id="mc-payment">$0</span><span class="mc-lbl">est. monthly P&amp;I</span></div>
 <div class="mc-meta"><span id="mc-loan">Loan amount: $0</span> &middot; <span id="mc-dp">Down: $0</span></div>
 </div>
 <p style="font-size:.78rem;color:#9ca3af;margin:12px 0 0;">Estimate only &mdash; not a loan offer or commitment. Actual terms come from your lender. For the full amortization calculator, <a href="https://yourrealtylink.com/content/mortgage-calculator" target="_blank" rel="noopener">open the Your Realty Link calculator</a>.</p>
</div>
<script>
(function(){
 var f=function(n){return '$'+Math.round(n).toLocaleString('en-US');};
 function calc(){
  var price=+document.getElementById('mc-price').value||0;
  var down=+document.getElementById('mc-down').value||0;
  var rate=+document.getElementById('mc-rate').value||0;
  var term=+document.getElementById('mc-term').value||30;
  var dp=price*down/100, loan=Math.max(price-dp,0), i=rate/100/12, n=term*12, m;
  m = i>0 ? loan*i*Math.pow(1+i,n)/(Math.pow(1+i,n)-1) : (n>0?loan/n:0);
  document.getElementById('mc-payment').textContent=f(m||0);
  document.getElementById('mc-loan').textContent='Loan amount: '+f(loan);
  document.getElementById('mc-dp').textContent='Down: '+f(dp);
 }
 ['mc-price','mc-down','mc-rate','mc-term'].forEach(function(id){
  var el=document.getElementById(id); el.addEventListener('input',calc); el.addEventListener('change',calc);
 });
 calc();
})();
</script>'''

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Mortgages &amp; Home Loans in Indianapolis | Your Realty Link</title>
 <meta name="description" content="Financing your Central Indiana home: an interactive mortgage payment calculator, loan types (FHA, VA, USDA, conventional), pre-approval, down payment help, and preferred local lenders.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="Mortgages & Home Loans in Indianapolis | Your Realty Link">
 <meta property="og:description" content="Mortgage calculator, loan types, pre-approval, down payment assistance, and trusted local lenders for Central Indiana buyers.">
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
 {{ "@type": "ListItem", "position": 3, "name": "Mortgages", "item": "{URL}" }} ] }}
 ] }}
 </script>
 {FONTS}
 <style>
.service-wrap {{ max-width: 820px; margin: 0 auto; padding: 40px 0; }}
.mtg-calc {{ background: #fff; border: 1px solid var(--border); border-radius: 16px; padding: 26px 28px; box-shadow: 0 6px 22px rgba(0,0,0,.07); margin: 1.4rem 0; }}
.mc-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 4px 0 8px; }}
.mc-grid label {{ display: flex; flex-direction: column; font-size: .8rem; font-weight: 700; color: #13294a; gap: 5px; position: relative; }}
.mc-grid label span {{ position: absolute; right: 12px; top: 33px; color: #9ca3af; font-weight: 600; font-size: .8rem; }}
.mc-grid input {{ border: 1px solid var(--border); border-radius: 9px; padding: 11px 40px 11px 12px; font-size: 1rem; font-family: inherit; color: #13294a; }}
.mc-grid input:focus {{ outline: none; border-color: var(--red); }}
.mc-out {{ background: linear-gradient(135deg,#13294a,#0d1e38); color: #fff; border-radius: 12px; padding: 20px 24px; text-align: center; margin-top: 8px; }}
.mc-num {{ font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 800; display: block; line-height: 1; }}
.mc-lbl {{ font-size: .85rem; color: #c9d4e0; }}
.mc-meta {{ font-size: .82rem; color: #c9d4e0; margin-top: 10px; }}
.loan-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 1.3rem 0; }}
.loan-card {{ background: var(--light); border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; }}
.loan-card h4 {{ margin: 0 0 5px; color: var(--red); font-size: 15px; }}
.loan-card p {{ margin: 0 0 8px; font-size: 13.5px; color: var(--mid); }}
.loan-card a {{ font-size: 13px; font-weight: 700; }}
 @media (max-width: 560px) {{ .mc-grid, .loan-grid {{ grid-template-columns: 1fr; }} }}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/services/">Services</a> <span>&rsaquo;</span> Mortgages</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>Mortgages &amp; Home Loans</h1>
 <p class="hero-sub">Financing is where a home purchase is won or lost. Estimate your payment, understand your loan options, and get connected with a trusted local lender &mdash; all in one place.</p>
 <div class="hero-badges">
 <span class="hero-badge">🧮 Payment Calculator</span>
 <span class="hero-badge">🏦 Loan Types</span>
 <span class="hero-badge">✅ Pre-Approval</span>
 <span class="hero-badge">💵 Down Payment Help</span>
 </div>
 </div>
</section>

<div class="container">
 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">Use the calculator to estimate your monthly payment, explore conventional, FHA, VA, and USDA loans, and get pre-approved with a trusted local lender. Your Realty Link connects Central Indiana buyers with the right financing &mdash; call 317-997-7404.</p>
 <dl class="qa-facts">
 <div><dt>Down payment</dt><dd>As low as 0&ndash;3.5%</dd></div>
 <div><dt>First step</dt><dd>Get pre-approved</dd></div>
 <div><dt>Lenders</dt><dd><a href="/vendors/#lenders-mortgage">Our preferred lenders</a></dd></div>
 <div><dt>Call</dt><dd><a href="tel:3179977404">317-997-7404</a></dd></div>
 </dl>
</div>
<!-- QA-END -->

 <div class="service-wrap">

 <p>Before you fall in love with a home, it helps to know what you can comfortably afford &mdash; and which loan fits your situation. Start with a quick payment estimate below, then talk to a lender to turn it into a real pre-approval. Your Realty Link works with a network of <a href="/vendors/#lenders-mortgage">trusted local lenders</a> and will help you find the right fit.</p>

 {CALC}

 <h2>Loan Types at a Glance</h2>
 <div class="loan-grid">
 <div class="loan-card"><h4>Conventional</h4><p>As little as 3% down for well-qualified buyers. Best rates with strong credit; no upfront mortgage-insurance fee.</p></div>
 <div class="loan-card"><h4>FHA</h4><p>3.5% down and flexible credit &mdash; popular with first-time buyers. <a href="/services/fha-loan-buyers/">FHA loans →</a></p></div>
 <div class="loan-card"><h4>VA</h4><p>0% down for eligible veterans and service members, with no monthly mortgage insurance. <a href="/services/va-loan-buyers/">VA loans →</a></p></div>
 <div class="loan-card"><h4>USDA</h4><p>0% down in eligible rural and edge-of-metro areas of Central Indiana. <a href="/services/usda-loans/">USDA loans →</a></p></div>
 </div>

 <h2>Your Financing Roadmap</h2>
 <ul>
 <li><strong><a href="/services/mortgage-pre-approval/">Get pre-approved</a></strong> &mdash; the real first step; know your budget and shop with confidence.</li>
 <li><strong><a href="/services/down-payment-assistance/">Down payment assistance</a></strong> &mdash; Indiana (IHCDA) programs that help with upfront costs.</li>
 <li><strong><a href="/services/closing-costs-buyers/">Closing costs</a></strong> &mdash; what to budget beyond the down payment.</li>
 <li><strong><a href="/vendors/#lenders-mortgage">Preferred lenders</a></strong> &mdash; the local loan officers our clients trust.</li>
 </ul>

 <p style="font-size:.85rem;color:#6e6e70;">Your Realty Link is a real estate brokerage, not a lender, and we receive no compensation for lender referrals. We connect you with independent local lenders so you get advice tailored to your situation.</p>

 <div class="cta-block">
 <h3>Ready to Get Pre-Approved?</h3>
 <p>Tell us where you are in the process and we'll connect you with a trusted local lender &mdash; no pressure, no obligation.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call: 317-997-7404</a>
 <a href="/services/mortgage-pre-approval/" class="btn btn-outline">Pre-Approval Guide →</a>
 <a href="/vendors/#lenders-mortgage" class="btn btn-outline">See Our Lenders →</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Mortgage FAQs</h2>
{faq_html}
 </section>

 </div>
</div>

<section class="cta-form-section">
 <div class="container">
 <h2>Talk Financing With Your Realty Link</h2>
 <p>Not sure which loan or lender fits? Send a note and we'll point you in the right direction.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="services/mortgages">
 <input type="hidden" name="interest_type" value="Mortgages">
 <div class="form-row">
 <div><label for="sv-name">Name *</label><input type="text" id="sv-name" name="name" required placeholder="Your name"></div>
 <div><label for="sv-phone">Phone *</label><input type="tel" id="sv-phone" name="phone" required placeholder="317-555-1234"></div>
 </div>
 <label for="sv-email">Email *</label>
 <input type="email" id="sv-email" name="email" required placeholder="you@example.com">
 <label for="sv-message">How can we help?</label>
 <textarea id="sv-message" name="message" placeholder="First-time buyer, refinancing questions, need a lender referral…"></textarea>
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
print("built /services/mortgages/")
