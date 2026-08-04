#!/usr/bin/env python3
"""Per-city lead-magnet guides (buyer + seller) for the flagship cities.
For each city+type: builds /resources/<slug>/ landing + thank-you pages (form ->
capture-lead) and renders a city-custom branded PDF via headless Chrome.
Reuses the canonical header/footer + the existing lead-magnet funnel pattern."""
import os, re, html, base64, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCRATCH = "/private/tmp/claude-501/-Users-danielcope-Library-Mobile-Documents-com-apple-CloudDocs-Claude-YRL/26f905d9-f2dc-48a5-9205-1e23c0b750ad/scratchpad"

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
HEADER = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
FOOTER = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)
FONT = ('<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" onload="this.onload=null;this.rel=\'stylesheet\'">'
        '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap"></noscript>')
LOGO_B64 = base64.b64encode(open(os.path.join(ROOT, "assets/img/yrl-logo.png"), "rb").read()).decode()

NAV_JS = ("<script>function toggleNav(){document.getElementById('siteNav').classList.toggle('open');}"
          "document.addEventListener('click',function(e){var dd=e.target.closest('.nav-item-dropdown');"
          "if(dd&&window.innerWidth<=960){var nav=dd.closest('.site-nav');if(nav&&nav.classList.contains('open'))"
          "{e.preventDefault();dd.classList.toggle('open');}}});</script>")
SITE_ENH = '<script src="/assets/js/site-enhancements.js?v=ae5261c2" defer></script>'

LM_STYLE = open(os.path.join(ROOT, "resources/central-indiana-buyers-guide/index.html"), encoding="utf-8").read()
LM_STYLE = re.search(r'<style>.*?</style>', LM_STYLE, re.DOTALL).group()

def esc(s):
    return html.escape(str(s or ""), quote=True)

# ── flagship city data (real facts; price tiers per CLAUDE.md, ranges not exacts) ──
CITIES = {
 "carmel": dict(name="Carmel", county="Hamilton County", url="/cities/hamilton-county/carmel-indiana-real-estate/",
   price="the mid-$400s to well over $1 million",
   schools="the highly regarded Carmel Clay Schools",
   areas=["the walkable Arts &amp; Design District", "the Village of WestClay", "West Carmel and the Clay Terrace area", "established golf communities like Bridgewater and Brookshire"],
   commute="roughly 20 minutes to downtown Indianapolis via US-31/Meridian Street and Keystone Parkway",
   character="an upscale, amenity-rich suburb famous for its roundabouts, the Palladium concert hall, the Monon Trail, and a genuinely walkable downtown"),
 "fishers": dict(name="Fishers", county="Hamilton County", url="/cities/hamilton-county/fishers-indiana-real-estate/",
   price="the low $300s to the $600s and beyond",
   schools="Hamilton Southeastern Schools",
   areas=["the vibrant Nickel Plate District", "waterfront living around Geist Reservoir", "established neighborhoods like Sunblest and Brooks Chase", "newer developments near Fishers Marketplace"],
   commute="about 25 minutes to downtown Indianapolis via I-69 and SR-37",
   character="one of America's most-recognized 'best places to live' — family-friendly, safe, and anchored by a lively Nickel Plate District with its amphitheater and farmers market"),
 "greenwood": dict(name="Greenwood", county="Johnson County", url="/cities/johnson-county/greenwood-indiana-real-estate/",
   price="the $250s to the $450s",
   schools="Center Grove and Greenwood Community Schools",
   areas=["revitalized Old Town Greenwood", "the sought-after Center Grove area", "Stones Crossing and the west side", "newer subdivisions near Worthsville Road"],
   commute="around 15 minutes to downtown Indianapolis via I-65 and US-31",
   character="the south metro's fast-growing retail and dining hub, offering strong value, an active Old Town, and easy interstate access"),
 "noblesville": dict(name="Noblesville", county="Hamilton County", url="/cities/hamilton-county/noblesville-indiana-real-estate/",
   price="the $300s to the $600s",
   schools="Noblesville Schools",
   areas=["the historic downtown square", "waterfront communities on Morse Reservoir", "The Harbour and Sagamore", "newer growth along SR-32 and Pleasant Street"],
   commute="about 30 minutes to downtown Indianapolis via SR-37 and I-69",
   character="Hamilton County's historic county seat, blending a charming courthouse-square downtown with lakefront living and steady new growth"),
 "westfield": dict(name="Westfield", county="Hamilton County", url="/cities/hamilton-county/westfield-indiana-real-estate/",
   price="the $300s to the $600s",
   schools="Westfield Washington Schools",
   areas=["the growing downtown Grand Junction district", "luxury living at Chatham Hills", "Maple Village and Wood Wind", "family neighborhoods near Grand Park"],
   commute="roughly 30 minutes to downtown Indianapolis via US-31",
   character="home of the massive Grand Park Sports Campus and one of Indiana's fastest-growing cities, with a rapidly developing downtown"),
 "zionsville": dict(name="Zionsville", county="Boone County", url="/cities/boone-county/zionsville-indiana-real-estate/",
   price="the mid-$400s to over $1 million",
   schools="the top-rated Zionsville Community Schools",
   areas=["the historic brick-street Village", "the Holliday Farms golf community", "Stonegate and Austin Oaks", "wooded estates on the north and west sides"],
   commute="about 25 minutes to downtown Indianapolis via I-65 and Michigan Road",
   character="small-town luxury at its finest — a charming brick-paved Main Street, boutique shopping, wooded lots, and some of the state's best schools"),
 "avon": dict(name="Avon", county="Hendricks County", url="/cities/hendricks-county/avon-indiana-real-estate/",
   price="the $250s to the $450s",
   schools="Avon Community School Corporation",
   areas=["family subdivisions along US-36", "the Avon Town Hall Park area", "newer communities near Ronald Reagan Parkway", "established neighborhoods off County Road 100 N"],
   commute="about 25 minutes to downtown Indianapolis via US-36 (Rockville Road) and I-74",
   character="a fast-growing, family-first Hendricks County community known for strong schools, new shopping, and excellent value on the west side"),
 "brownsburg": dict(name="Brownsburg", county="Hendricks County", url="/cities/hendricks-county/brownsburg-indiana-real-estate/",
   price="the $250s to the $450s",
   schools="the well-regarded Brownsburg Community School Corporation",
   areas=["downtown Brownsburg and Arbuckle Acres", "newer subdivisions near SR-267", "the Northfield and Cardinal areas", "communities close to I-74"],
   commute="about 25 minutes to downtown Indianapolis via I-74",
   character="a welcoming west-side town with racing heritage, top-rated schools, and a growing downtown that keeps a genuine small-town feel"),
}

# ── shared reusable process copy ──
BUY_STEPS = [
 ("Get mortgage-ready", "Before you fall in love with a home, talk to a local lender and get pre-approved. A pre-approval tells you your real budget and makes your offer credible to sellers."),
 ("Set your must-haves", "Decide what matters most — bedrooms, yard, garage, commute, schools. Knowing your non-negotiables keeps the search focused."),
 ("Tour homes with your agent", "Your Realty Link sets up showings, points out what a listing photo won't show you, and helps you compare homes objectively."),
 ("Make a strong offer", "We prepare a comparative market analysis so you offer smart, and we structure the terms — earnest money, contingencies, timeline — to protect you."),
 ("Inspection and appraisal", "A home inspection uncovers the condition; the lender's appraisal confirms value. We help you negotiate repairs or price if something turns up."),
 ("Final walk-through and closing", "You confirm the home is in the agreed condition, then sign at closing and get your keys. We're with you every step to the finish line."),
]
SELL_STEPS = [
 ("Get a real valuation", "It starts with a comparative market analysis grounded in what comparable homes have actually sold for nearby — not an online guess."),
 ("Prepare and stage", "Declutter, handle small repairs, boost curb appeal, and stage so buyers see the home at its best. First impressions drive offers."),
 ("List and market", "We price it right, shoot professional photography, and put it in front of buyers across the MLS and every major site — plus our own network."),
 ("Showings and open houses", "We manage showings and feedback and keep you informed, so your home gets maximum exposure to serious buyers."),
 ("Review offers", "When offers come in, we help you weigh price, terms, financing strength, and contingencies to choose the best one — not just the highest number."),
 ("Inspection to closing", "We negotiate any inspection items, coordinate the appraisal, and guide you through closing so the sale actually gets to the finish line."),
]

def pdf_html(city_key, kind):
    d = CITIES[city_key]
    n = d["name"]
    accent = "#c03926"
    steps = BUY_STEPS if kind == "buyer" else SELL_STEPS
    title = f"The {n}, Indiana Home {'Buyer' if kind=='buyer' else 'Seller'}’s Guide"
    sub = (f"Everything you need to buy a home in {n} — the market, the neighborhoods, the schools, and the process, start to finish."
           if kind == "buyer" else
           f"How to sell your {n} home for the best price — pricing, prep, marketing, and every step to a smooth closing.")
    areas = "".join(f"<li><strong>{a.split(' like ')[0].split(' around ')[0]}</strong> — {a}</li>" if False else f"<li>{a}</li>" for a in d["areas"])
    steps_html = "".join(
        f'<div class="step"><div class="stepnum">{i+1}</div><div><h3>{esc(t)}</h3><p>{esc(b)}</p></div></div>'
        for i,(t,b) in enumerate(steps))

    if kind == "buyer":
        body = f"""
<div class="sec"><h2>Welcome to {esc(n)}</h2>
<p>{esc(n)} is {d['character']}. Buyers are drawn here for {d['schools'].replace('the ','').replace('highly regarded ','').replace('top-rated ','').replace('well-regarded ','')}, a strong sense of community, and everyday convenience — all within {d['commute']}.</p>
<p>This guide walks you through what it actually takes to buy a home in {esc(n)}, from understanding the market to getting your keys.</p></div>

<div class="sec"><h2>The {esc(n)} Housing Market</h2>
<p>Homes in {esc(n)} typically range from {d['price']}, depending on size, age, location, and updates. You'll find everything from low-maintenance ranches and townhomes to two-story family homes and new construction.</p>
<div class="callout"><strong>Local tip:</strong> Online estimates miss the mark in {esc(n)} because condition and updates vary so much street to street. A local comparative market analysis is the only reliable way to know what a home is really worth.</div></div>

<div class="sec"><h2>Where to Live in {esc(n)}</h2>
<p>A few of the areas {esc(n)} buyers ask about most:</p>
<ul class="areas">{areas}</ul>
<p>The right fit depends on your budget, commute, and lifestyle — we're happy to help you weigh the trade-offs.</p></div>

<div class="sec"><h2>Schools</h2>
<p>{esc(n)} is served by {d['schools']}, one of the biggest reasons families put down roots here. If schools are a priority, we'll help you understand boundaries before you fall in love with a specific home.</p></div>

<div class="sec"><h2>Getting Around</h2>
<p>{esc(n)} sits {d['commute']}, making it a practical choice for commuters while keeping shopping, dining, and parks close to home.</p></div>

<div class="sec"><h2>Your Step-by-Step Buying Roadmap</h2>{steps_html}</div>

<div class="sec cta"><h2>Ready to Buy in {esc(n)}?</h2>
<p>Your Realty Link is a full-service, MIBOR-member brokerage led by Principal Broker Janet Giles-Schultz. We help buyers across {esc(n)} and all of Central Indiana find the right home and negotiate the right deal.</p>
<p class="big">Call or text Daniel Cope: <strong>317-201-6323</strong></p>
<p>Search every active {esc(n)} listing at <strong>yourrealtylink.com</strong> · Questions? info@yourrealtylink.com</p></div>
"""
    else:
        body = f"""
<div class="sec"><h2>Selling Your Home in {esc(n)}</h2>
<p>{esc(n)} is {d['character']} — and that demand is good news for sellers. Buyers actively look here for {d['schools'].replace('the ','').replace('highly regarded ','').replace('top-rated ','').replace('well-regarded ','')} and the lifestyle, but the homes that sell fastest and for the most are the ones that are priced right and presented well.</p></div>

<div class="sec"><h2>Pricing Your {esc(n)} Home Right</h2>
<p>Homes in {esc(n)} generally sell in the range of {d['price']}, but your home's number depends on its condition, updates, and exact location. Pricing is the single most important decision you'll make.</p>
<div class="callout"><strong>Price it right from day one.</strong> Overpriced homes sit, go stale, and often sell for less than if they'd been priced correctly at the start. We build your price on real, recent {esc(n)}-area sales — not a website estimate.</div></div>

<div class="sec"><h2>Preparing Your Home to Sell</h2>
<p>Before we list, a little work pays off:</p>
<ul class="areas"><li>Declutter and depersonalize so buyers can picture themselves living there</li><li>Handle the small repairs buyers notice — leaky faucets, scuffs, sticking doors</li><li>Deep clean and boost curb appeal; the front of the house sets the tone</li><li>Stage key rooms so they photograph and show at their best</li></ul></div>

<div class="sec"><h2>The Your Realty Link Marketing Plan</h2>
<p>When you list with us, your {esc(n)} home gets:</p>
<ul class="areas"><li>Professional photography that makes buyers stop scrolling</li><li>Full exposure on the MIBOR MLS and every major search site</li><li>Targeted online and social promotion to local buyers</li><li>Showings and open houses managed for maximum interest</li></ul></div>

<div class="sec"><h2>Your Step-by-Step Selling Roadmap</h2>{steps_html}</div>

<div class="sec cta"><h2>Thinking About Selling in {esc(n)}?</h2>
<p>Start with a free, no-obligation home valuation from Your Realty Link — a MIBOR-member brokerage led by Principal Broker Janet Giles-Schultz. We'll give you an honest, data-backed number and a plan to get your {esc(n)} home sold.</p>
<p class="big">Call or text Daniel Cope: <strong>317-201-6323</strong></p>
<p>Get your free valuation at <strong>yourrealtylink.com</strong> · info@yourrealtylink.com</p></div>
"""

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: letter; margin: 0; }}
*{{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,'Segoe UI',Arial,sans-serif;}}
body{{color:#1a1a1a;font-size:12px;line-height:1.6;}}
.cover{{height:11in;background:linear-gradient(150deg,#1a1a1a 0%,#7a2418 55%,{accent} 100%);color:#fff;padding:1.1in 0.9in;display:flex;flex-direction:column;justify-content:space-between;page-break-after:always;}}
.cover .logo{{height:64px;background:#fff;padding:10px 16px;border-radius:10px;align-self:flex-start;}}
.cover h1{{font-family:'Playfair Display',Georgia,serif;font-size:46px;line-height:1.08;max-width:8in;}}
.cover .csub{{font-size:19px;color:#f3d7d1;margin-top:16px;max-width:6.6in;}}
.cover .cfoot{{font-size:15px;color:#f0dcd8;}}
.cover .cfoot b{{color:#fff;}}
.page{{padding:0.7in 0.9in;}}
.sec{{margin-bottom:22px;page-break-inside:avoid;}}
h2{{font-family:'Playfair Display',Georgia,serif;font-size:22px;color:{accent};border-bottom:2px solid {accent};padding-bottom:6px;margin-bottom:10px;}}
p{{margin-bottom:9px;}}
.callout{{background:#f7f2f1;border-left:4px solid {accent};padding:12px 16px;border-radius:0 6px 6px 0;margin:10px 0;font-size:11.5px;}}
ul.areas{{list-style:none;margin:6px 0 10px;}}
ul.areas li{{padding:6px 0 6px 20px;position:relative;border-bottom:1px solid #eee;}}
ul.areas li:before{{content:'▪';color:{accent};position:absolute;left:2px;}}
.step{{display:flex;gap:14px;margin-bottom:12px;align-items:flex-start;}}
.stepnum{{flex:0 0 30px;width:30px;height:30px;background:{accent};color:#fff;border-radius:50%;text-align:center;line-height:30px;font-weight:800;font-size:14px;}}
.step h3{{font-size:14px;margin-bottom:2px;color:#1a1a1a;}}
.cta{{background:#f7f7f7;border:1px solid #e5e5e5;border-radius:10px;padding:20px 24px;margin-top:8px;}}
.cta .big{{font-size:16px;color:{accent};font-weight:800;margin:10px 0;}}
</style></head><body>
<div class="cover"><img class="logo" src="data:image/png;base64,{LOGO_B64}">
<div><h1>{esc(title)}</h1><div class="csub">{esc(sub)}</div></div>
<div class="cfoot"><b>Your Realty Link</b> · Central Indiana Real Estate<br>yourrealtylink.com · 317-997-7404 · Daniel Cope, Real Estate Broker</div></div>
<div class="page">{body}</div>
</body></html>"""

# ── landing + thank-you page builders ──
def landing_html(city_key, kind, slug, pdf_name):
    d = CITIES[city_key]; n = d["name"]
    is_buy = kind == "buyer"
    hero_img = "resource-buyer" if is_buy else "resource-seller"
    typ = "Buyer" if is_buy else "Seller"
    title = f"Free {n} Home {typ}’s Guide (Indiana) | Your Realty Link"
    desc = (f"Download the free {n}, Indiana home {typ.lower()}'s guide from Your Realty Link — the {n} market, neighborhoods, schools, and the {'buying' if is_buy else 'selling'} process, step by step.")
    hero_h1 = f"The Free {n} Home {typ}’s Guide"
    if is_buy:
        hero_sub = f"Everything you need to buy a home in {n}, Indiana — the market, the best neighborhoods, the schools, and how to win the home."
        bullets = [
          (f"The {n} housing market", f"what homes really cost in {n} and the styles you'll find, in plain English"),
          (f"Where to live in {n}", "the neighborhoods and areas buyers ask about most, and how to choose"),
          (f"Schools and commute", f"{d['schools']} and how quickly you can get around"),
          ("Your step-by-step buying roadmap", "from getting pre-approved to keys in hand, the Central Indiana way"),
        ]
        related = [("/services/first-time-home-buyers/","First-Time Home Buyer Services"),
                   ("/services/down-payment-assistance/","Down Payment Assistance in Indiana"),
                   (d["url"], f"{n} Real Estate — Homes for Sale"),
                   ("https://yourrealtylink.com/property-search","Search Homes on YourRealtyLink.com")]
        intro = f"This guide was built by <strong>Daniel Cope</strong> at Your Realty Link for people buying in {n} and the surrounding area — with the local details national guides leave out."
    else:
        hero_sub = f"How to sell your {n}, Indiana home for the best price — pricing, prep, marketing, and every step to a smooth closing."
        bullets = [
          (f"Pricing your {n} home right", "how local pricing works and why it beats an online estimate"),
          ("Preparing your home to sell", "the prep and staging that actually moves the needle on offers"),
          ("The Your Realty Link marketing plan", "professional photography, the MLS, and full online exposure"),
          ("Your step-by-step selling roadmap", "from valuation to closing, with nothing left to guess"),
        ]
        related = [("/services/free-home-valuation/","Free Home Valuation"),
                   ("/services/pricing-your-home/","How to Price Your Home"),
                   (d["url"], f"{n} Real Estate — Market Overview"),
                   ("/services/home-staging/","Home Staging in Indianapolis")]
        intro = f"This guide was built by <strong>Daniel Cope</strong> at Your Realty Link from real experience helping {n}-area sellers price, prep, and close — for top dollar."

    blist = "\n".join(f'<li><span class="lm-check">&#10003;</span><span><strong>{esc(t)}</strong> &mdash; {esc(b)}</span></li>' for t,b in bullets)
    rlist = "\n".join(f'<li style="border:none;display:list-item;padding:4px 0;"><a href="{u}">{esc(l)}</a></li>' for u,l in related)
    ld = ('{"@context":"https://schema.org","@graph":['
          '{"@type":["LocalBusiness","RealEstateAgent"],"name":"Your Realty Link","url":"https://yourrealtylink.com","telephone":"317-997-7404","areaServed":"' + esc(n) + ', Indiana"},'
          '{"@type":"WebPage","name":"' + esc(title) + '","url":"https://janetgiles.com/resources/' + slug + '/"},'
          '{"@type":"BreadcrumbList","itemListElement":['
          '{"@type":"ListItem","position":1,"name":"Home","item":"https://janetgiles.com/"},'
          '{"@type":"ListItem","position":2,"name":"Resources","item":"https://janetgiles.com/resources/"},'
          '{"@type":"ListItem","position":3,"name":"' + esc(n) + ' ' + typ + ' Guide","item":"https://janetgiles.com/resources/' + slug + '/"}]}]}')

    js = ("<script>document.getElementById('leadMagnetForm').addEventListener('submit',function(e){"
          "e.preventDefault();var btn=this.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Sending...';"
          "var data={};var inputs=this.querySelectorAll('input,select,textarea');"
          "for(var i=0;i<inputs.length;i++){if(inputs[i].name)data[inputs[i].name]=inputs[i].value;}"
          "data.source_url=window.location.href;data.submitted_at=new Date().toISOString();data.business='yrl';data.source='lead-magnet';data.tags='lead-magnet,__SLUG__';"
          "fetch('https://wdvolamasztetwpitbwg.supabase.co/functions/v1/capture-lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})"
          ".then(function(r){window.location.href='/resources/__SLUG__/thank-you/';})"
          ".catch(function(){btn.disabled=false;btn.textContent='Get the Guide';alert('Something went wrong. Please try again or call 317-997-7404.');});});</script>").replace("__SLUG__", slug)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(title)}</title>
 <meta name="description" content="{esc(desc)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="https://janetgiles.com/resources/{slug}/">
 <meta property="og:title" content="{esc(title)}">
 <meta property="og:description" content="{esc(desc)}">
 <meta property="og:url" content="https://janetgiles.com/resources/{slug}/">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">{ld}</script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 {FONT}
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 {LM_STYLE}
</head>
<body>
{HEADER}
<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/resources/">Resources</a> <span>&rsaquo;</span> {esc(n)} {typ}'s Guide</div></nav>
<section class="lm-hero" style="background:linear-gradient(160deg,rgba(27,58,92,0.86) 0%,rgba(192,57,38,0.55) 100%),image-set(url('/assets/img/heroes/{hero_img}.webp') type('image/webp'), url('/assets/img/heroes/{hero_img}.jpg') type('image/jpeg')) center 40%/cover no-repeat;"><h1>{esc(hero_h1)}</h1><p class="hero-sub">{esc(hero_sub)}</p></section>
<div class="lm-body">
 <div class="lm-value">
 <h2>What's Inside</h2>
 <ul>
{blist}
 </ul>
 <p>{intro}</p>
 <p>Enter your name and email and you'll get instant access on the next page &mdash; we'll email you a copy too.</p>
 <p class="lm-social-proof">Written for {esc(n)}, Indiana buyers and sellers by a local Your Realty Link broker.</p>
 <hr class="divider" style="margin-top:32px;">
 <h3>Related Resources</h3>
 <ul style="list-style:disc;padding-left:20px;">
{rlist}
 </ul>
 </div>
 <div class="lm-form-card">
 <h3>Get Your Free {esc(n)} Guide</h3>
 <p class="form-sub">Instant access — no waiting.</p>
 <form id="leadMagnetForm" novalidate>
 <input type="hidden" name="lead_magnet" value="{slug}">
 <input type="hidden" name="source_page" value="resources/{slug}">
 <input type="hidden" name="interest_type" value="{typ}">
 <label for="lm-fname">First Name *</label>
 <input type="text" id="lm-fname" name="first_name" required placeholder="First name">
 <label for="lm-lname">Last Name *</label>
 <input type="text" id="lm-lname" name="last_name" required placeholder="Last name">
 <label for="lm-email">Email *</label>
 <input type="email" id="lm-email" name="email" required placeholder="you@example.com">
 <label for="lm-phone">Phone <span class="opt-label">(optional)</span></label>
 <input type="tel" id="lm-phone" name="phone" placeholder="317-555-1234">
 <button type="submit">Get the {esc(n)} Guide</button>
 <p class="form-note">No spam. Unsubscribe anytime. Your info stays private.</p>
 </form>
 </div>
</div>
{FOOTER}
{NAV_JS}
{js}
{SITE_ENH}
</body></html>"""

def thankyou_html(city_key, kind, slug, pdf_name):
    d = CITIES[city_key]; n = d["name"]; typ = "Buyer" if kind == "buyer" else "Seller"
    dl = f"/resources/{slug}/download/{pdf_name}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Your {esc(n)} {typ}'s Guide Is Ready | Your Realty Link</title>
 <meta name="robots" content="noindex, nofollow">
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 {FONT}
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 {LM_STYLE}
</head>
<body>
{HEADER}
<section class="ty-hero"><h1>&#127881; Your {esc(n)} {typ}'s Guide Is Ready!</h1><p>Click below to download your guide. We've also sent a copy to your email &mdash; check your inbox (and spam folder, just in case).</p></section>
<div class="ty-wrap">
 <a class="dl-btn" href="{dl}" download>&#11015; Download the {esc(n)} {typ}'s Guide (PDF)</a>
 <p class="ty-note">Save it, print it, or keep it on your phone. Questions as you read? Call or text Daniel at <a href="tel:3179977404">317-997-7404</a>.</p>
 <div class="ty-cards">
 <div class="ty-card"><h3>Search {esc(n)} Homes</h3><p>Browse every active MLS listing in {esc(n)} and Central Indiana.</p><a href="https://yourrealtylink.com/property-search" target="_blank" rel="noopener">Start searching &rarr;</a></div>
 <div class="ty-card"><h3>Free Home Valuation</h3><p>Curious what your {esc(n)} home is worth in today's market? Get a no-obligation estimate.</p><a href="/services/free-home-valuation/">Get my value &rarr;</a></div>
 <div class="ty-card"><h3>Explore {esc(n)}</h3><p>Prices, neighborhoods, schools, and local events for {esc(n)}.</p><a href="{d['url']}">See the {esc(n)} guide &rarr;</a></div>
 <div class="ty-card"><h3>Talk to Daniel</h3><p>Talk through your goals with a local Your Realty Link broker — no pressure.</p><a href="/contact/">Get in touch &rarr;</a></div>
 </div>
</div>
{FOOTER}
{NAV_JS}
{SITE_ENH}
</body></html>"""

# ── generate ──
made = []
for city_key in CITIES:
    d = CITIES[city_key]; n = d["name"]
    for kind in ("buyer", "seller"):
        typ = "Buyer" if kind == "buyer" else "Seller"
        slug = f"{city_key}-home-{kind}s-guide"
        pdf_name = f"{n.replace(' ','-')}-Home-{typ}s-Guide.pdf"
        base = os.path.join(ROOT, "resources", slug)
        os.makedirs(os.path.join(base, "thank-you"), exist_ok=True)
        os.makedirs(os.path.join(base, "download"), exist_ok=True)
        open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(landing_html(city_key, kind, slug, pdf_name))
        open(os.path.join(base, "thank-you", "index.html"), "w", encoding="utf-8").write(thankyou_html(city_key, kind, slug, pdf_name))
        # PDF
        hp = os.path.join(SCRATCH, slug + ".html")
        open(hp, "w", encoding="utf-8").write(pdf_html(city_key, kind))
        out = os.path.abspath(os.path.join(base, "download", pdf_name))
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf=" + out, "file://" + hp], capture_output=True)
        ok = os.path.exists(out)
        made.append((slug, ok, os.path.getsize(out)//1024 if ok else 0))

print("Generated %d city guides (landing + thank-you + PDF):" % len(made))
for slug, ok, kb in made:
    print("  %s  PDF:%s (%dKB)" % (slug, "OK" if ok else "FAIL", kb))
