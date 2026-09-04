#!/usr/bin/env python3
"""Build /senior-living/ — the Senior Real Estate hub, migrated from
movingseniorsinindy.com. Reuses an existing page's header/footer/asset-hashes so
nav/footer stay in sync. Re-run after nav/footer changes.
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "services", "expired-listings", "index.html")
OUT_DIR = os.path.join(ROOT, "senior-living")
URL = "https://yourrealtylink.com/senior-living/"

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
 ("What is a senior real estate specialist?",
  "It&rsquo;s an agent who focuses on the needs of buyers and sellers over 55 &mdash; someone who understands downsizing, 55+ and one-level communities, coordinating the sale of a long-time family home with the purchase of the next one, and the emotional side of a later-in-life move. Janet Giles-Schultz and Elizabeth Cottler are Your Realty Link&rsquo;s senior specialists."),
 ("What is a retirement mortgage?",
  "&ldquo;Retirement mortgage&rdquo; is a general term for financing options built around retirement income and home equity &mdash; including reverse mortgages (HECMs) and reverse-for-purchase loans that let qualified buyers 62+ purchase a home with no required monthly mortgage payment. Every situation is different, so we connect you with trusted local lenders who specialize in these programs rather than giving one-size-fits-all advice."),
 ("Do you help with downsizing and the actual move?",
  "Yes. Beyond listing and buying, we help coordinate the pieces that make a later-in-life move manageable &mdash; right-sizing furniture, connecting you with movers and estate-sale help, and lining up the repairs and updates that get the family home ready for market."),
 ("What kind of homes do seniors move to in Central Indiana?",
  "Most of our senior clients look for low-maintenance, one-level living &mdash; ranch homes, patio homes, condominiums, and active-adult (55+) communities such as Del Webb. We can set up a saved search matching your must-haves so new listings come straight to you."),
]
def strip(t):
    return re.sub("&[a-z]+;|&#\\d+;", lambda m: {"&ldquo;":'"',"&rdquo;":'"',"&rsquo;":"'","&mdash;":"—","&amp;":"&"}.get(m.group(0),""), t)
faq_html = "\n".join(
 f'<details class="faq-item">\n<summary>{q}</summary>\n<div class="faq-answer"><p>{a}</p></div>\n</details>' for q,a in faqs)
faq_schema = ",\n".join(
 '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
 % (json.dumps(strip(q)), json.dumps(strip(a))) for q,a in faqs)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Senior Real Estate in Indianapolis &mdash; Moving After 55 | Your Realty Link</title>
 <meta name="description" content="Downsizing or moving to a 55+ community in Central Indiana? Your Realty Link's senior real estate specialists help you right-size and find one-level living.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="Senior Real Estate in Indianapolis — Moving After 55 | Your Realty Link">
 <meta property="og:description" content="Senior real estate specialists helping Central Indiana buyers and sellers downsize, right-size, and move to one-level and 55+ living.">
 <meta property="og:url" content="{URL}">
 <meta property="og:image" content="https://yourrealtylink.com/assets/img/services/senior-living-banner.jpg">
 <meta property="og:image:width" content="1600"><meta property="og:image:height" content="800">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:image" content="https://yourrealtylink.com/assets/img/services/senior-living-banner.jpg">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{
 "@context": "https://schema.org",
 "@graph": [
 {{ "@type": "WebPage", "url": "{URL}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"] }} }},
 {{
 "@type": ["LocalBusiness", "RealEstateAgent"],
 "name": "Your Realty Link — Senior Real Estate", "url": "https://yourrealtylink.com", "logo": "/assets/img/yrl-logo.png",
 "telephone": "317-997-7404", "email": "janet@yourrealtylink.com",
 "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US" }},
 "areaServed": "Indianapolis, Indiana and Central Indiana"
 }},
 {{ "@type": "FAQPage", "mainEntity": [
 {faq_schema}
 ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Senior Living", "item": "{URL}" }}
 ] }}
 ]
 }}
 </script>
 {FONTS}
 <style>
.service-wrap {{ max-width: 820px; margin: 0 auto; padding: 44px 0; }}
.sr-banner {{ display: block; max-width: 1100px; margin: 22px auto 0; }}
.sr-banner img {{ width: 100%; height: auto; display: block; border-radius: 14px; box-shadow: 0 8px 26px rgba(0,0,0,.14); }}
.sr-belt {{ background: #eef3ec; padding: 26px 0 30px; text-align: center; }}
.sr-belt .eyebrow {{ font-size: 12.5px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: #3f7d4f; margin-bottom: 10px; }}
.sr-belt h1 {{ color: #13294a; font-size: clamp(1.5rem, 3.2vw, 2.15rem); margin: 0 0 8px; line-height: 1.15; }}
.sr-belt p {{ color: #48566b; font-size: 1.05rem; max-width: 62ch; margin: 0 auto 16px; }}
.sr-belt .btn-group {{ justify-content: center; }}
.help-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 1.4rem 0; }}
.help-item {{ background: var(--light); border-radius: var(--radius); padding: 18px 20px; border: 1px solid var(--border); }}
.help-item h4 {{ font-size: 14.5px; margin-bottom: 6px; color: var(--red); }}
.help-item p {{ font-size: 13.5px; color: var(--mid); margin: 0; }}
.spec-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin: 1.4rem 0; }}
.spec-card {{ background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 22px 24px; }}
.spec-card h4 {{ margin: 0 0 2px; color: #13294a; font-size: 17px; }}
.spec-card .role {{ color: #3f7d4f; font-weight: 700; font-size: 12.5px; text-transform: uppercase; letter-spacing: .05em; }}
.spec-card p {{ font-size: 13.5px; color: var(--mid); margin: 10px 0 12px; }}
.spec-card a {{ font-weight: 700; }}
.search-links {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 1.2rem 0; }}
.search-links a {{ background: var(--light); border: 1px solid var(--border); border-radius: 100px; padding: 9px 16px; font-size: 13.5px; font-weight: 600; color: #13294a; text-decoration: none; }}
.search-links a:hover {{ border-color: var(--red); color: var(--red); }}
.sr-blog {{ margin: 2.4rem 0 0.5rem; }}
.sr-blog-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 1.2rem; }}
.sr-post {{ background: #fff; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; text-decoration: none; display: flex; flex-direction: column; transition: transform .15s ease, box-shadow .15s ease; }}
.sr-post:hover {{ transform: translateY(-3px); box-shadow: 0 12px 28px rgba(0,0,0,.12); }}
.sr-post img {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block; background: #12283f; }}
.sr-post .b {{ padding: 14px 16px 18px; display: flex; flex-direction: column; gap: 6px; flex: 1; }}
.sr-post .cat {{ font-size: .68rem; font-weight: 800; letter-spacing: .05em; text-transform: uppercase; color: #3f7d4f; }}
.sr-post h4 {{ font-size: .98rem; line-height: 1.3; color: #13294a; margin: 0; }}
.sr-post p {{ font-size: .82rem; color: var(--mid); line-height: 1.5; margin: 0; }}
.sr-post .more {{ margin-top: auto; color: var(--red); font-weight: 700; font-size: .8rem; padding-top: 4px; }}
 @media (max-width: 700px) {{ .sr-blog-grid {{ grid-template-columns: 1fr; }} }}
 @media (max-width: 600px) {{ .help-grid, .spec-grid {{ grid-template-columns: 1fr; }} }}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container">
 <a href="/">Home</a>
 <span>&rsaquo;</span>
 Senior Living
 </div>
</nav>

<picture class="sr-banner">
 <source srcset="/assets/img/services/senior-living-banner.webp" type="image/webp">
 <img src="/assets/img/services/senior-living-banner.jpg" alt="A senior couple moving forward to a new season of life — Simplify. Rightsize. Enjoy." width="1600" height="800">
</picture>
<section class="sr-belt">
 <div class="container">
 <div class="eyebrow">Senior Real Estate &middot; Moving After 55</div>
 <h1>Let&rsquo;s Talk Real Estate After 55</h1>
 <p>Moving on from the family home is a big step. Your Realty Link&rsquo;s senior specialists make it simpler &mdash; helping you right-size, find comfortable one-level living, and move forward to your next chapter with confidence.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-primary">📞 Call a Senior Specialist: 317-997-7404</a>
 <a href="#connect" class="btn btn-outline">Ask a Question →</a>
 </div>
 </div>
</section>

<div class="container">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">Your Realty Link is a Southport-based brokerage with senior real estate specialists who help Central Indiana homeowners over 55 downsize, sell the family home, and move to one-level or 55+ living. Call Janet Giles-Schultz at 317-997-7404 or Elizabeth Cottler at 317-507-7770.</p>
 <dl class="qa-facts">
 <div><dt>Who we help</dt><dd>Buyers &amp; sellers 55+ in Central Indiana</dd></div>
 <div><dt>Senior specialists</dt><dd>Janet Giles-Schultz &amp; Elizabeth Cottler</dd></div>
 <div><dt>Call or text</dt><dd><a href="tel:3179977404">317-997-7404</a></dd></div>
 <div><dt>Office</dt><dd>2302 E Southport Rd, Indianapolis</dd></div>
 </dl>
</div>
<!-- QA-END -->

 <div class="service-wrap">

 <p>For many people, the hardest part of moving after 55 isn&rsquo;t the house &mdash; it&rsquo;s everything the house holds. Your Realty Link is a boutique brokerage based in Southport, Indiana with agents who specialize in the senior market. We understand that the move from a two-story family home to a smaller, low-maintenance, one-level place is as much about feelings as it is about square footage, and we take the time to get it right.</p>

 <h2>What Are Your Senior Needs?</h2>
 <p>Every later-in-life move is different. Some clients want to be closer to grandchildren; others want a 55+ community with amenities and no yard work, or a ranch home where everything is on one floor. We start by listening &mdash; then we build a plan around what matters most to you.</p>
 <div class="help-grid">
 <div class="help-item"><h4>Right-Sizing, Not Just Downsizing</h4><p>We help you find the home that fits this chapter &mdash; often smaller and simpler, but the right size for how you actually live now.</p></div>
 <div class="help-item"><h4>One-Level &amp; Low-Maintenance</h4><p>Ranch homes, patio homes, condos, and 55+ communities like Del Webb &mdash; less upkeep, more time for what you enjoy.</p></div>
 <div class="help-item"><h4>Prepping the Family Home</h4><p>We line up the repairs, updates, and cleanout help that get a long-owned home ready to sell for top dollar.</p></div>
 <div class="help-item"><h4>Coordinating Both Sides</h4><p>Selling and buying at once is stressful. We align the timelines so you&rsquo;re not carrying two homes or scrambling to move.</p></div>
 </div>

 <h2>Why Use a Senior Specialist?</h2>
 <p>A senior real estate specialist does more than list a house. We know the 55+ communities across the metro, we&rsquo;re patient with a move that may take time, and we coordinate the moving pieces &mdash; downsizing, estate-sale help, movers, and repairs &mdash; so the transition feels manageable instead of overwhelming. And because Your Realty Link is a full-service MIBOR brokerage, you get the whole market and a proven marketing plan behind the sale of your current home.</p>

 <h2>What Is a Retirement Mortgage?</h2>
 <p>You don&rsquo;t always have to pay cash to buy your next home. &ldquo;Retirement mortgage&rdquo; options &mdash; including reverse mortgages (HECMs) and reverse-for-purchase loans &mdash; can let qualified buyers 62 and older buy a home with no required monthly mortgage payment, using home equity and retirement income. These programs aren&rsquo;t right for everyone, so rather than give one-size-fits-all advice, we connect you with <a href="/services/preferred-lenders/">trusted local lenders</a> who specialize in retirement financing and can walk you through the numbers.</p>

 <h2>Managing the Move</h2>
 <p>The logistics are often what people dread most. We help you break the move into steps &mdash; deciding what to keep, arranging estate sales or donations for the rest, scheduling movers, and timing everything around your closing &mdash; so &ldquo;goodbye to the memories&rdquo; can become &ldquo;hello to the next chapter&rdquo; without the chaos.</p>

 <h2>Start Your Search for One-Level &amp; 55+ Homes</h2>
 <p>Your Realty Link gives you the full MIBOR MLS &mdash; every active listing, updated in real time. Tell us your must-haves and we&rsquo;ll set up a saved search so new homes that fit come straight to you.</p>
 <div class="search-links">
 <a href="https://yourrealtylink.com/property-search" target="_blank" rel="noopener">Search All Homes</a>
 <a href="https://yourrealtylink.com/property-search" target="_blank" rel="noopener">Ranch &amp; One-Level Homes</a>
 <a href="https://yourrealtylink.com/property-search" target="_blank" rel="noopener">55+ &amp; Active-Adult Communities</a>
 <a href="/services/new-construction/">New Construction &amp; Del Webb</a>
 <a href="/services/free-home-valuation/">What&rsquo;s My Home Worth?</a>
 </div>

 <h2>Meet Your Senior Specialists</h2>
 <div class="spec-grid">
 <div class="spec-card">
 <span class="role">Broker / Owner &middot; Senior Specialist</span>
 <h4>Janet Giles-Schultz</h4>
 <p>Janet has been helping Central Indiana families buy and sell since the 1970s and leads Your Realty Link&rsquo;s senior real estate work with patience, honesty, and deep local knowledge.</p>
 <a href="tel:3179977404">📞 317-997-7404</a>
 </div>
 <div class="spec-card">
 <span class="role">Senior Specialist</span>
 <h4>Elizabeth Cottler</h4>
 <p>Elizabeth works closely with senior buyers and sellers across the metro, guiding right-sizing moves and 55+ transitions with genuine care for each client&rsquo;s situation.</p>
 <a href="tel:3175077770">📞 317-507-7770</a>
 </div>
 </div>

 <section class="sr-blog">
 <h2>From the Senior Living Blog</h2>
 <p>Plain-English guides on downsizing, managing a move, retirement mortgages, and property-tax deductions for Central Indiana seniors.</p>
 <!-- SENIOR-RECENT-POSTS -->
 <div class="sr-blog-grid"></div>
 <!-- /SENIOR-RECENT-POSTS -->
 <p style="margin-top:16px;"><a href="/blog/" style="color:var(--red);font-weight:700;text-decoration:none;">Read more on the Your Realty Link blog &rarr;</a></p>
 </section>

 <!-- PRIMARY CTA -->
 <div class="cta-block" id="connect">
 <h3>Let&rsquo;s Talk About Your Next Move</h3>
 <p>Whether you&rsquo;re ready now or just starting to think about it, our senior specialists will listen first and help you plan a move that feels right &mdash; no pressure.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call Janet: 317-997-7404</a>
 <a href="tel:3175077770" class="btn btn-outline">📞 Call Elizabeth: 317-507-7770</a>
 <a href="mailto:janet@yourrealtylink.com" class="btn btn-outline">✉️ Email Us</a>
 </div>
 </div>

 <!-- FAQ -->
 <section class="faq-section">
 <h2>Frequently Asked Questions &mdash; Senior Real Estate</h2>
{faq_html}
 </section>

 <hr class="divider">
 <h3>Related Resources</h3>
 <ul>
 <li><a href="/services/free-home-valuation/">Free Home Valuation</a></li>
 <li><a href="/services/downsizing/">Downsizing Your Home</a></li>
 <li><a href="/services/preferred-lenders/">Preferred Lenders</a></li>
 <li><a href="/services/new-construction/">New Construction Homes</a></li>
 <li><a href="/contact/">Contact Your Realty Link</a></li>
 </ul>

 </div>
</div>

<section class="cta-form-section">
 <div class="container">
 <h2>Ask a Senior Specialist</h2>
 <p>Send a note and Janet or Elizabeth will reach out personally — no obligation, no pressure.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="senior-living">
 <input type="hidden" name="interest_type" value="Senior Living">
 <input type="hidden" name="tags" value="senior,downsizing">
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
 <textarea id="sv-message" name="message" placeholder="Tell us a little about your move — downsizing, 55+ community, selling the family home, timing…"></textarea>
 <button type="submit">Send Message →</button>
 <p class="form-note">No spam · No obligation · A senior specialist responds personally</p>
 </form>
 </div>
</section>

{FOOTER}

{SCRIPTS}'''

os.makedirs(OUT_DIR, exist_ok=True)
open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page)

sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read()
if URL not in s:
    blk = f"<url>\n  <loc>{URL}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.7</priority>\n</url>\n"
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", blk + "</urlset>"))
    print("added sitemap entry")
print("built /senior-living/")
