#!/usr/bin/env python3
"""Build the Central Indiana utilities feature from data/city-utilities.json:

  1. /utilities/ — a dedicated move-in / transfer-service guide: a provider
     overview (electric, gas, water/sewer, trash, internet) plus a full
     county-grouped directory of every city's providers.
  2. A "Setting Up Utilities in <City>" block injected into each of the 62
     city pages (idempotent, marker-wrapped, HTML-only, no whitespace reflow).

Accuracy guardrail: nothing here is invented. Fields the research could not
confirm are rendered as "varies by address — confirm at setup" rather than
guessed. Re-run any time data/city-utilities.json is updated (e.g. when Janet
sends provider fills for the gap towns).

    python3 build_utilities.py
"""
import os, re, json, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "data", "city-utilities.json"), encoding="utf-8"))
TPL  = os.path.join(ROOT, "services", "expired-listings", "index.html")
OUT_DIR = os.path.join(ROOT, "utilities")
URL = "https://janetgiles.com/utilities/"

# ── shell (fonts w/ versioned css hash, header, footer, scripts) from a sibling ──
src = open(TPL, encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS  = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

# ── small html helpers ──
def esc(s):  return html.escape(str(s or ""), quote=False)
def uhref(u): return str(u or "").replace("&", "&amp;")
def telhref(p):
    d = re.sub(r"\D", "", str(p or ""))
    return "tel:" + d if d else ""

SERVICES = [
    ("electric",     "⚡ Electric"),
    ("gas",          "🔥 Natural gas"),
    ("water_sewer",  "🚰 Water &amp; sewer"),
    ("trash",        "🗑️ Trash &amp; recycling"),
]

def contact_cell(v):
    bits = []
    ph = v.get("phone")
    if ph:
        bits.append('<a href="%s">%s</a>' % (telhref(ph), esc(ph)))
    ur = v.get("url")
    if ur:
        bits.append('<a href="%s" target="_blank" rel="noopener">Start service &#8599;</a>' % uhref(ur))
    return " &middot; ".join(bits) if bits else "&mdash;"

def provider_cell(v):
    name = (v or {}).get("name")
    if name:
        return esc(name)
    return '<em>Varies by address &mdash; confirm your provider when you set up service.</em>'

def util_table(rec):
    rows = []
    for key, label in SERVICES:
        v = rec.get(key) or {}
        rows.append("  <tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                    % (label, provider_cell(v), contact_cell(v)))
    inet = [esc(i) for i in (rec.get("internet") or []) if i]
    inet_cell = ", ".join(inet) if inet else "&mdash;"
    rows.append('  <tr><td>🌐 Internet</td><td>%s</td><td>&mdash;</td></tr>' % inet_cell)
    return ('<div class="util-table-wrap">\n'
            '<table class="util-table">\n'
            '<thead><tr><th>Service</th><th>Provider</th><th>Set up / transfer</th></tr></thead>\n'
            '<tbody>\n' + "\n".join(rows) + '\n</tbody></table></div>')

# ── map each record to its city-page directory (slug = kebab city + -...-real-estate) ──
CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def find_dir(city):
    kebab = city.strip().lower().replace(" ", "-")
    for d in CITY_DIRS:
        base = os.path.basename(d.rstrip(os.sep))
        if base.startswith(kebab + "-"):
            return d.rstrip(os.sep)
    return None

def county_slug_of(pathdir):
    # cities/<county-slug>/<city-slug>
    return os.path.basename(os.path.dirname(pathdir))

def county_pretty(county_slug):
    return county_slug.replace("-", " ").title()  # "hamilton-county" -> "Hamilton County"

# ══════════════════════════════════════════════════════════════════════════
#  1. per-city block injection
# ══════════════════════════════════════════════════════════════════════════
BEGIN, END = "<!-- UTILITIES-SETUP -->", "<!-- /UTILITIES-SETUP -->"

def city_block(rec, pathdir):
    city = rec["city"]
    cslug = county_slug_of(pathdir)
    county = county_pretty(cslug)
    county_url = "/counties/%s-indiana-real-estate/" % cslug
    parts = [
        BEGIN,
        ' <hr class="divider">',
        ' <h2 id="utilities">Setting Up Utilities in %s, Indiana</h2>' % esc(city),
        (' <p>Moving to %s? Here is who to contact to start or transfer electric, gas, '
         'water and sewer, trash, and internet service. Utility service areas in Central '
         'Indiana often follow property lines rather than city limits, so confirm the '
         'provider for your exact address when you set up service.</p>' % esc(city)),
        ' ' + util_table(rec),
        (' <p class="util-note">Providers and phone numbers can change &mdash; confirm the '
         'details when you start service. Planning a move? <a href="/contact/">Contact Your '
         'Realty Link</a> and we will help you line up the details of moving day.</p>'),
        (' <p>More local resources: the full <a href="/utilities/">Central Indiana utilities '
         '&amp; setup guide</a>, our <a href="/vendors/">preferred local vendors</a>, and '
         '<a href="%s">%s real estate</a>.</p>' % (county_url, esc(county))),
        END,
    ]
    return "\n".join(parts) + "\n\n "

def inject(pathdir, section):
    f = os.path.join(pathdir, "index.html")
    s = open(f, encoding="utf-8").read()
    s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "", s, flags=re.DOTALL)
    # place right after Community Events, before the "Explore More" divider
    m = re.search(r'<hr class="divider">\s*<h3>\s*Explore', s)
    if m:
        pos = m.start()
    else:
        m = re.search(r'<div class="info-box"', s)
        pos = m.start() if m else s.find("</main>")
    if pos < 0:
        return False
    open(f, "w", encoding="utf-8").write(s[:pos] + section + s[pos:])
    return True

injected, warn = 0, []
by_county = {}
for rec in DATA:
    d = find_dir(rec["city"])
    if not d:
        warn.append("no page dir for " + rec["city"]); continue
    by_county.setdefault(county_slug_of(d), []).append((rec, d))
    if inject(d, city_block(rec, d)):
        injected += 1
    else:
        warn.append("no anchor in " + rec["city"])

# ══════════════════════════════════════════════════════════════════════════
#  2. the dedicated /utilities/ page
# ══════════════════════════════════════════════════════════════════════════
def prov(name, phone, url, note=""):
    c = []
    if phone: c.append('<a href="%s">%s</a>' % (telhref(phone), esc(phone)))
    if url:   c.append('<a href="%s" target="_blank" rel="noopener">%s &#8599;</a>' % (uhref(url), "Website"))
    contact = " &middot; ".join(c)
    n = ' <span class="uo-note">%s</span>' % esc(note) if note else ""
    return '<li><strong>%s</strong>%s%s%s</li>' % (esc(name), " &mdash; " if contact else "", contact, n)

# regional provider overview (confirmed across the research + known seed data)
OVERVIEW = [
 ("⚡", "Electricity", [
   prov("AES Indiana", "888-261-8222", "https://www.aesindiana.com", "Indianapolis / Marion County and parts of the metro"),
   prov("Duke Energy Indiana", "800-521-2232", "https://www.duke-energy.com", "much of the surrounding suburban and outlying area"),
   prov("Rural electric co-ops (REMC)", "", "", "NineStar, Hendricks Power, Boone REMC, Johnson County REMC, RushShelby Energy, SCI REMC and others serve rural addresses"),
   prov("Municipal electric", "", "", "some towns run their own — Anderson (AMLP), Greenfield (Power & Light), Pendleton, Edinburgh, Bargersville"),
 ]),
 ("🔥", "Natural gas", [
   prov("Citizens Energy Group", "317-924-3311", "https://www.citizensenergygroup.com/My-Home/Start-or-Stop-Service", "Indianapolis / Marion County and the inner ring"),
   prov("CenterPoint Energy", "800-227-1376", "https://www.centerpointenergy.com/en-us/residential", "most of the surrounding counties (formerly Vectren)"),
   prov("Propane", "", "", "some rural towns have no natural-gas main and use propane instead"),
 ]),
 ("🚰", "Water & sewer", [
   prov("Citizens Energy Group (Citizens Water)", "317-924-3311", "https://www.citizensenergygroup.com/My-Home/Start-or-Stop-Service", "Indianapolis and much of Marion County"),
   prov("Indiana American Water", "800-492-8373", "https://amwater.com/inaw", "Greenwood, Noblesville, Franklin and many suburbs"),
   prov("Municipal water & sewer", "", "", "most towns run their own utility — set up water and sewer with the city or town office"),
   prov("Private well & septic", "", "", "common on rural and edge-of-town properties"),
 ]),
 ("🗑️", "Trash & recycling", [
   prov("City / town collection", "", "", "many communities include trash on the municipal utility bill"),
   prov("Private subscription haulers", "", "", "elsewhere you choose a hauler — Republic Services, Ray's Trash, Best Way Disposal or GFL are common locally"),
 ]),
 ("🌐", "Internet", [
   prov("Cable", "", "", "Xfinity (Comcast) and Spectrum cover most of the metro"),
   prov("Fiber", "", "", "AT&T Fiber, Metronet, Brightspeed, plus regional fiber (NineStar, Endeavor, JCFiber)"),
   prov("5G home & satellite", "", "", "T-Mobile / Verizon 5G Home and Starlink fill in rural gaps"),
 ]),
]
overview_html = "\n".join(
  '<div class="uo-card"><h3>%s %s</h3>\n<ul class="uo-list">\n%s\n</ul></div>'
  % (icon, title, "\n".join(items)) for icon, title, items in OVERVIEW)

# full county-grouped directory
dir_sections = []
for cslug in sorted(by_county, key=lambda s: county_pretty(s)):
    cities = sorted(by_county[cslug], key=lambda t: t[0]["city"])
    cards = []
    for rec, d in cities:
        rel = "/cities/%s/%s/" % (cslug, os.path.basename(d))
        cid = "uc-" + rec["city"].strip().lower().replace(" ", "-").replace("/", "-")
        cards.append(
          '<details class="util-city" id="%s" data-city="%s">\n'
          '<summary>%s</summary>\n%s\n'
          '<p class="util-note"><a href="%s">%s, Indiana real estate &#8594;</a></p>\n'
          '</details>' % (cid, esc(rec["city"]), esc(rec["city"]), util_table(rec), rel, esc(rec["city"])))
    dir_sections.append(
      '<section class="uo-county"><h3>%s</h3>\n%s\n</section>'
      % (county_pretty(cslug), "\n".join(cards)))
directory_html = "\n".join(dir_sections)

# alphabetical jump dropdown (all cities, flat)
jump_options = "\n ".join(
  '<option value="uc-%s">%s</option>'
  % (r["city"].strip().lower().replace(" ", "-").replace("/", "-"), esc(r["city"]))
  for r in sorted(DATA, key=lambda x: x["city"]))

DESC = ("Who to call to set up electric, gas, water, sewer, trash, and internet when you move "
        "in Central Indiana — provider phone numbers, start-service links, and a city-by-city guide.")

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Central Indiana Utilities &amp; Setup Guide | Your Realty Link</title>
 <meta name="description" content="{DESC}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="Central Indiana Utilities &amp; Setup Guide | Your Realty Link">
 <meta property="og:description" content="{DESC}">
 <meta property="og:url" content="{URL}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{URL}", "name": "Central Indiana Utilities & Setup Guide", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead"] }} }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Local Resources", "item": "https://janetgiles.com/vendors/" }},
 {{ "@type": "ListItem", "position": 3, "name": "Utilities & Setup", "item": "{URL}" }} ] }}
 ] }}
 </script>
 <link rel="preload" as="image" href="/assets/img/heroes/utilities.jpg" fetchpriority="high">
 {FONTS}
 <style>
.uo-wrap {{ max-width: 900px; margin: 0 auto; padding: 34px 0 10px; }}
.uo-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin: 1.2rem 0 1.6rem; }}
.uo-card {{ background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 18px 22px; box-shadow: 0 5px 18px rgba(0,0,0,.05); }}
.uo-card h3 {{ margin: 0 0 8px; color: var(--red); font-size: 1.05rem; }}
.uo-list {{ margin: 0; padding-left: 1.05rem; }}
.uo-list li {{ margin: 0 0 8px; font-size: 14px; color: #33373b; line-height: 1.5; }}
.uo-note {{ display: block; color: #6e6e70; font-size: 12.5px; margin-top: 1px; }}
.uo-county {{ margin: 1.1rem 0; }}
.uo-county > h3 {{ color: #13294a; border-bottom: 2px solid var(--border); padding-bottom: 6px; margin-bottom: 10px; }}
.util-city {{ border: 1px solid var(--border); border-radius: 10px; margin: 8px 0; background: #fff; overflow: hidden; }}
.util-city > summary {{ cursor: pointer; padding: 12px 16px; font-weight: 700; color: #13294a; list-style: none; }}
.util-city > summary::-webkit-details-marker {{ display: none; }}
.util-city > summary::after {{ content: "＋"; float: right; color: var(--red); font-weight: 700; }}
.util-city[open] > summary::after {{ content: "－"; }}
.util-city[open] > summary {{ border-bottom: 1px solid var(--border); background: var(--light); }}
.util-city .util-table-wrap {{ padding: 4px 16px 0; }}
.util-city .util-note {{ padding: 0 16px 12px; }}
.uc-tools {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 1rem 0 1.3rem; }}
.uc-tools input, .uc-tools select {{ flex: 1; min-width: 220px; padding: 12px 14px; border: 1px solid var(--border); border-radius: 10px; font-size: 1rem; font-family: inherit; color: #13294a; background: #fff; }}
.uc-tools input:focus, .uc-tools select:focus {{ outline: none; border-color: var(--red); box-shadow: 0 0 0 3px rgba(192,57,38,.12); }}
 @media (max-width: 640px) {{ .uo-grid {{ grid-template-columns: 1fr; }} }}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/vendors/">Local Resources</a> <span>&rsaquo;</span> Utilities &amp; Setup</div>
</nav>

<section class="page-hero banner-raw" style="--hero-img: -webkit-image-set(url('/assets/img/heroes/utilities.webp') type('image/webp'), url('/assets/img/heroes/utilities.jpg') type('image/jpeg')); --hero-img: image-set(url('/assets/img/heroes/utilities.webp') type('image/webp'), url('/assets/img/heroes/utilities.jpg') type('image/jpeg')); --hero-pos: center;">
 <div class="container">
 <h1>Central Indiana Utilities &amp; Setup Guide</h1>
 <p class="hero-sub">Just bought or about to move? Here is who to call to turn on electric, gas, water, sewer, trash, and internet across the Indianapolis metro &mdash; with a city-by-city directory below.</p>
 <div class="hero-badges">
 <span class="hero-badge">⚡ Electric &amp; Gas</span>
 <span class="hero-badge">🚰 Water &amp; Sewer</span>
 <span class="hero-badge">🗑️ Trash</span>
 <span class="hero-badge">🌐 Internet</span>
 </div>
 </div>
</section>

<div class="container">
 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">In most of Central Indiana, set up electricity with AES Indiana or Duke Energy, natural gas with Citizens Energy Group or CenterPoint Energy, and water/sewer with Citizens Water, Indiana American Water, or your town office. Trash is either on your city bill or a private hauler. Service areas follow your exact address &mdash; use the city-by-city guide below, and call Your Realty Link at <a href="tel:3179977404">317-997-7404</a> if you need a hand.</p>
</div>
<!-- QA-END -->

 <div class="uo-wrap">
 <p>One of the small stresses of moving is figuring out who provides what. In Central Indiana the answer depends on which county and even which side of town you are on &mdash; utility territories often follow property lines, not city limits. Here is the big picture, followed by a directory for all {len(DATA)} communities we serve.</p>

 <h2>Who Provides What</h2>
 <div class="uo-grid">
 {overview_html}
 </div>

 <div class="cta-block">
 <h3>Not Sure Who Serves Your New Address?</h3>
 <p>Send us the address and we will point you to the right electric, gas, water, and trash providers &mdash; part of how we help buyers and sellers through moving day.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call: 317-997-7404</a>
 <a href="/contact/" class="btn btn-outline">Contact Your Realty Link →</a>
 <a href="/vendors/" class="btn btn-outline">Preferred Vendors →</a>
 </div>
 </div>

 <h2 id="by-city">Utilities by City</h2>
 <p>Search or jump to your city for its electric, gas, water/sewer, trash, and internet providers, with phone numbers and start-service links. Fields marked &ldquo;varies by address&rdquo; are where you should confirm the provider directly when you set up service.</p>
 <div class="uc-tools">
 <input type="search" id="uCitySearch" placeholder="🔎 Search your city…" autocomplete="off" aria-label="Search for your city">
 <select id="uCityJump" aria-label="Jump to a city A to Z">
 <option value="">Jump to a city (A–Z)…</option>
 {jump_options}
 </select>
 </div>
 <p id="uNoMatch" class="util-note" style="display:none;">No city matches that search. Try a different spelling, or <a href="/contact/">contact us</a> and we will track it down.</p>
 {directory_html}
 <script>
 (function(){{
  var q=document.getElementById('uCitySearch'),
      jump=document.getElementById('uCityJump'),
      noMatch=document.getElementById('uNoMatch'),
      cities=[].slice.call(document.querySelectorAll('details.util-city')),
      counties=[].slice.call(document.querySelectorAll('.uo-county'));
  function norm(s){{return (s||'').toLowerCase().trim();}}
  function filter(){{
   var v=norm(q.value), any=false;
   cities.forEach(function(d){{
    var show=!v || norm(d.getAttribute('data-city')).indexOf(v)>-1;
    d.style.display=show?'':'none'; if(show) any=true;
   }});
   counties.forEach(function(sec){{
    var vis=[].slice.call(sec.querySelectorAll('details.util-city')).some(function(d){{return d.style.display!=='none';}});
    sec.style.display=vis?'':'none';
   }});
   noMatch.style.display=any?'none':'';
  }}
  q.addEventListener('input',filter);
  jump.addEventListener('change',function(){{
   var id=jump.value; if(!id) return;
   q.value=''; filter();
   var el=document.getElementById(id);
   if(el){{ el.open=true; el.scrollIntoView({{behavior:'smooth',block:'start'}}); }}
   jump.selectedIndex=0;
  }});
 }})();
 </script>

 <p style="font-size:.85rem;color:#6e6e70;margin-top:1.4rem;">Your Realty Link provides this guide as a convenience for Central Indiana buyers and sellers. Providers, phone numbers, and service areas change over time &mdash; always confirm with the utility when you start service. We are a real estate brokerage and are not affiliated with the utilities listed.</p>
 </div>
</div>

{FOOTER}

{SCRIPTS}'''

os.makedirs(OUT_DIR, exist_ok=True)
open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page)

# sitemap
sm = os.path.join(ROOT, "sitemap.xml")
s = open(sm, encoding="utf-8").read()
if URL not in s:
    open(sm, "w", encoding="utf-8").write(
        s.replace("</urlset>", f"<url>\n  <loc>{URL}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n</urlset>"))
    print("added sitemap entry")

print("built /utilities/  (overview + %d-city directory)" % len(DATA))
print("injected utilities block into %d city pages" % injected)
for w in warn:
    print("  WARN " + w)
