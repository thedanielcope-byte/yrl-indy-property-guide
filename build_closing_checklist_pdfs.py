#!/usr/bin/env python3
"""Downloadable-PDF lead magnets for the buyer & seller closing checklists.

For each checklist: renders a branded PDF (headless Chrome) from the SAME content
as the interactive /services/*-closing-checklist/ page, and builds the standard
lead-magnet funnel: /resources/<slug>/ landing (form -> capture-lead) ->
/resources/<slug>/thank-you/ (noindex) -> /resources/<slug>/download/<Name>.pdf.
Also adds the two cards to the /resources/ hub + sitemap.

Reuses the checklist content by importing the cfg dicts from
build_closing_checklists (its build loop is guarded under __main__).

    python3 build_closing_checklist_pdfs.py
"""
import os, re, html, base64, subprocess
from build_closing_checklists import buyer, seller, WIRE_ALERT

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
LM_STYLE = re.search(r'<style>.*?</style>',
                     open(os.path.join(ROOT, "resources/central-indiana-buyers-guide/index.html"), encoding="utf-8").read(),
                     re.DOTALL).group()

def esc(s):  return html.escape(str(s or ""), quote=True)
def absl(s): return str(s).replace('href="/', 'href="https://janetgiles.com/')

# extract the wire-fraud copy from the shared WIRE_ALERT block (single source of truth)
_wa_h = re.search(r'<h3>(.*?)</h3>', WIRE_ALERT).group(1)
_wa_p = re.search(r'<p>(.*?)</p>', WIRE_ALERT, re.DOTALL).group(1)

# ── PDF ─────────────────────────────────────────────────────────────────────
PDF_INTRO = ("Print this checklist and check off each step as you go. It follows the same stages the "
             "Consumer Financial Protection Bureau recommends, tuned for how closings actually work here "
             "in Central Indiana. Questions on any step? Call Your Realty Link at 317-997-7404.")

def pdf_phase(title, intro, items):
    rows = []
    for label, help in items:
        h = '<p class="ckh">%s</p>' % absl(help) if help else ''
        rows.append('<div class="ck"><span class="box"></span><div class="ckt"><strong>%s</strong>%s</div></div>'
                    % (absl(label), h))
    return '<div class="sec"><h2>%s</h2><p class="lead">%s</p>%s</div>' % (title, intro, "\n".join(rows))

def pdf_html(cfg):
    phase_htmls = [pdf_phase(t, i, items) for t, i, items in cfg["phases"]]
    wire = ('<div class="callout"><h3>%s</h3><p>%s</p></div>' % (_wa_h, _wa_p))
    phase_htmls.insert(2, wire)
    body = "\n".join(phase_htmls)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: letter; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; font-family:-apple-system,'Segoe UI',Arial,sans-serif; }}
body {{ color:#1a1a1a; font-size:12px; line-height:1.55; }}
.cover {{ height:11in; background:linear-gradient(150deg,#13294a 0%,#7a2418 62%,#c03926 100%); color:#fff; padding:1.1in .9in; display:flex; flex-direction:column; justify-content:space-between; page-break-after:always; }}
.cover .logo {{ height:58px; background:#fff; padding:9px 15px; border-radius:10px; align-self:flex-start; }}
.cover h1 {{ font-family:'Playfair Display',Georgia,serif; font-size:44px; line-height:1.08; max-width:7.4in; }}
.cover .csub {{ font-size:18px; color:#f3d7d1; margin-top:16px; max-width:6.3in; }}
.cover .tag {{ display:inline-block; margin-top:22px; font-size:12px; letter-spacing:.09em; text-transform:uppercase; background:rgba(255,255,255,.16); padding:8px 15px; border-radius:20px; }}
.cover .cfoot {{ font-size:13.5px; color:#f0dcd8; }}
.cover .cfoot b {{ color:#fff; }}
.page {{ padding:.55in .9in; }}
.sec {{ margin-bottom:18px; page-break-inside:avoid; }}
h2 {{ font-family:'Playfair Display',Georgia,serif; font-size:19px; color:#c03926; border-bottom:2px solid #c03926; padding-bottom:5px; margin-bottom:8px; }}
.lead {{ color:#555; font-style:italic; margin-bottom:9px; }}
.ck {{ display:flex; gap:10px; align-items:flex-start; padding:6px 0; border-bottom:1px solid #eee; }}
.ck .box {{ flex:0 0 14px; width:14px; height:14px; border:2px solid #c03926; border-radius:3px; margin-top:2px; }}
.ckt strong {{ font-size:12.5px; }}
.ckh {{ color:#555; font-size:10.8px; margin-top:2px; }}
.ckh a {{ color:#c03926; text-decoration:none; }}
.callout {{ background:#fff5f3; border:1px solid #f3c9c0; border-left:4px solid #c03926; padding:11px 15px; border-radius:0 6px 6px 0; margin:12px 0; page-break-inside:avoid; }}
.callout h3 {{ color:#c03926; font-size:13px; margin-bottom:4px; }}
.callout p {{ font-size:10.8px; }}
.intro {{ background:#f7f7f7; border-radius:8px; padding:12px 16px; margin-bottom:16px; font-size:11.5px; }}
.cta {{ background:#f7f7f7; border:1px solid #e5e5e5; border-radius:10px; padding:17px 22px; margin-top:8px; page-break-inside:avoid; }}
.cta h3 {{ color:#c03926; font-size:15px; margin-bottom:6px; }}
.cta .big {{ font-size:15px; color:#13294a; font-weight:800; margin:8px 0 4px; }}
</style></head><body>
<div class="cover">
 <img class="logo" src="data:image/png;base64,{LOGO_B64}">
 <div>
  <h1>{cfg['h1']}</h1>
  <div class="csub">{cfg['herosub'].replace('interactive ', '')}</div>
  <span class="tag">Central Indiana &middot; Your Realty Link</span>
 </div>
 <div class="cfoot"><b>Your Realty Link</b> &middot; Janet Giles-Schultz, Principal Broker<br>yourrealtylink.com &middot; 317-997-7404 &middot; A MIBOR member brokerage</div>
</div>
<div class="page">
 <div class="intro">{PDF_INTRO}</div>
 {body}
 <div class="sec cta">
  <h3>Questions About Your Closing?</h3>
  <p>Your Realty Link guides Central Indiana buyers and sellers all the way to the closing table &mdash; and beyond. If any step raises a question, we are glad to walk you through it.</p>
  <p class="big">Call or text: 317-997-7404</p>
  <p>yourrealtylink.com &middot; A MIBOR member brokerage led by Principal Broker Janet Giles-Schultz</p>
 </div>
</div>
</body></html>"""

# ── landing + thank-you funnel ──────────────────────────────────────────────
LANDING = {
 "buyer": {
   "typ": "Buyer", "interest": "Buyer", "hero_img": "resource-buyer",
   "hero_h1": "The Home Buyer's Closing Checklist (Free PDF)",
   "hero_sub": "A printable, step-by-step checklist for closing on your Central Indiana home — before, during, and after the big day.",
   "bullets": [
     ("A clear pre-closing game plan", "what to line up in the weeks before closing so nothing surprises you"),
     ("How to read your Closing Disclosure", "compare it to your Loan Estimate and know what is allowed to change"),
     ("Wire-fraud protection", "the one habit that protects your down payment from scammers"),
     ("A closing-day grab list", "exactly what to bring and what to confirm before you sign"),
   ],
   "related": [("/services/buyer-closing-checklist/", "The interactive buyer closing checklist"),
               ("/services/closing-costs-buyers/", "Buyer Closing Costs in Indiana"),
               ("/services/home-buying-process/", "The Home Buying Process"),
               ("/utilities/", "Central Indiana Utilities & Setup Guide")],
   "intro": "Built by Your Realty Link for Central Indiana buyers &mdash; the practical, local details that keep closing day calm.",
 },
 "seller": {
   "typ": "Seller", "interest": "Seller", "hero_img": "resource-seller",
   "hero_h1": "The Home Seller's Closing Checklist (Free PDF)",
   "hero_sub": "A printable, step-by-step checklist for selling your Central Indiana home — from under contract to the closing table.",
   "bullets": [
     ("Your under-contract checklist", "the payoff, disclosure, and documents to line up early"),
     ("How to check your net proceeds", "read your settlement statement before closing day"),
     ("Wire-fraud protection", "how to receive your proceeds safely"),
     ("A closing-day grab list", "what to bring and what to hand over at the table"),
   ],
   "related": [("/services/seller-closing-checklist/", "The interactive seller closing checklist"),
               ("/services/closing-costs-sellers/", "Seller Closing Costs in Indiana"),
               ("/services/sell-my-home/", "Home Selling Services"),
               ("/services/free-home-valuation/", "Free Home Valuation")],
   "intro": "Built by Your Realty Link from real experience getting Central Indiana sellers to a smooth, well-priced closing.",
 },
}

def landing_html(kind, slug, pdf_name):
    L = LANDING[kind]; typ = L["typ"]
    title = f"Free {typ}'s Closing Checklist (PDF) | Your Realty Link"
    desc = f"Download the free {typ.lower()}'s closing checklist for Central Indiana — a printable, step-by-step guide to a smooth closing."
    blist = "\n".join(f'<li><span class="lm-check">&#10003;</span><span><strong>{esc(t)}</strong> &mdash; {esc(b)}</span></li>' for t, b in L["bullets"])
    rlist = "\n".join(f'<li style="border:none;display:list-item;padding:4px 0;"><a href="{u}">{esc(l)}</a></li>' for u, l in L["related"])
    ld = ('{"@context":"https://schema.org","@graph":['
          '{"@type":["LocalBusiness","RealEstateAgent"],"name":"Your Realty Link","url":"https://yourrealtylink.com","telephone":"317-997-7404","areaServed":"Central Indiana"},'
          '{"@type":"WebPage","name":"' + esc(title) + '","url":"https://janetgiles.com/resources/' + slug + '/"},'
          '{"@type":"BreadcrumbList","itemListElement":['
          '{"@type":"ListItem","position":1,"name":"Home","item":"https://janetgiles.com/"},'
          '{"@type":"ListItem","position":2,"name":"Resources","item":"https://janetgiles.com/resources/"},'
          '{"@type":"ListItem","position":3,"name":"' + esc(typ) + ' Closing Checklist","item":"https://janetgiles.com/resources/' + slug + '/"}]}]}')
    js = ("<script>document.getElementById('leadMagnetForm').addEventListener('submit',function(e){"
          "e.preventDefault();var btn=this.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Sending...';"
          "var data={};var inputs=this.querySelectorAll('input,select,textarea');"
          "for(var i=0;i<inputs.length;i++){if(inputs[i].name)data[inputs[i].name]=inputs[i].value;}"
          "data.source_url=window.location.href;data.submitted_at=new Date().toISOString();data.business='yrl';data.source='lead-magnet';data.tags='lead-magnet,__SLUG__';"
          "fetch('https://wdvolamasztetwpitbwg.supabase.co/functions/v1/capture-lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})"
          ".then(function(r){window.location.href='/resources/__SLUG__/thank-you/';})"
          ".catch(function(){btn.disabled=false;btn.textContent='Get the Checklist';alert('Something went wrong. Please try again or call 317-997-7404.');});});</script>").replace("__SLUG__", slug)
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
<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/resources/">Resources</a> <span>&rsaquo;</span> {typ}'s Closing Checklist</div></nav>
<section class="lm-hero" style="background:linear-gradient(160deg,rgba(27,58,92,0.86) 0%,rgba(192,57,38,0.55) 100%),image-set(url('/assets/img/heroes/{L['hero_img']}.webp') type('image/webp'), url('/assets/img/heroes/{L['hero_img']}.jpg') type('image/jpeg')) center 40%/cover no-repeat;"><h1>{esc(L['hero_h1'])}</h1><p class="hero-sub">{esc(L['hero_sub'])}</p></section>
<div class="lm-body">
 <div class="lm-value">
 <h2>What's Inside</h2>
 <ul>
{blist}
 </ul>
 <p>{L['intro']}</p>
 <p>Enter your name and email and you'll get instant access on the next page &mdash; we'll email you a copy too.</p>
 <p class="lm-social-proof">The same checklist as our interactive page, in a clean printable PDF you can bring to closing.</p>
 <hr class="divider" style="margin-top:32px;">
 <h3>Related Resources</h3>
 <ul style="list-style:disc;padding-left:20px;">
{rlist}
 </ul>
 </div>
 <div class="lm-form-card">
 <h3>Get the Free {typ}'s Checklist</h3>
 <p class="form-sub">Instant access — no waiting.</p>
 <form id="leadMagnetForm" novalidate>
 <input type="hidden" name="lead_magnet" value="{slug}">
 <input type="hidden" name="source_page" value="resources/{slug}">
 <input type="hidden" name="interest_type" value="{L['interest']}">
 <label for="lm-fname">First Name *</label>
 <input type="text" id="lm-fname" name="first_name" required placeholder="First name">
 <label for="lm-lname">Last Name *</label>
 <input type="text" id="lm-lname" name="last_name" required placeholder="Last name">
 <label for="lm-email">Email *</label>
 <input type="email" id="lm-email" name="email" required placeholder="you@example.com">
 <label for="lm-phone">Phone <span class="opt-label">(optional)</span></label>
 <input type="tel" id="lm-phone" name="phone" placeholder="317-555-1234">
 <button type="submit">Get the Checklist</button>
 <p class="form-note">No spam. Unsubscribe anytime. Your info stays private.</p>
 </form>
 </div>
</div>
{FOOTER}
{NAV_JS}
{js}
{SITE_ENH}
</body></html>"""

def thankyou_html(kind, slug, pdf_name):
    typ = LANDING[kind]["typ"]; dl = f"/resources/{slug}/download/{pdf_name}"
    other = "seller" if kind == "buyer" else "buyer"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Your {typ}'s Closing Checklist Is Ready | Your Realty Link</title>
 <meta name="robots" content="noindex, nofollow">
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 {FONT}
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 {LM_STYLE}
</head>
<body>
{HEADER}
<section class="ty-hero"><h1>&#127881; Your {typ}'s Closing Checklist Is Ready!</h1><p>Click below to download your printable checklist. We've also sent a copy to your email &mdash; check your inbox (and spam folder, just in case).</p></section>
<div class="ty-wrap">
 <a class="dl-btn" href="{dl}" download>&#11015; Download the {typ}'s Closing Checklist (PDF)</a>
 <p class="ty-note">Save it, print it, or keep it on your phone. Questions as you go? Call or text Your Realty Link at <a href="tel:3179977404">317-997-7404</a>.</p>
 <div class="ty-cards">
 <div class="ty-card"><h3>Use the Interactive Version</h3><p>Check items off online with saved progress.</p><a href="/services/{kind}-closing-checklist/">Open the checklist &rarr;</a></div>
 <div class="ty-card"><h3>What Closing Costs</h3><p>See what to budget at the closing table.</p><a href="/services/closing-costs-{kind}s/">Closing costs &rarr;</a></div>
 <div class="ty-card"><h3>Set Up Your Utilities</h3><p>Electric, gas, water, trash, and internet by city.</p><a href="/utilities/">Utilities guide &rarr;</a></div>
 <div class="ty-card"><h3>Talk to Your Realty Link</h3><p>Questions about your closing? We're glad to help.</p><a href="/contact/">Get in touch &rarr;</a></div>
 </div>
</div>
{FOOTER}
{NAV_JS}
{SITE_ENH}
</body></html>"""

# ── generate ────────────────────────────────────────────────────────────────
made = []
for kind, cfg in (("buyer", buyer), ("seller", seller)):
    slug = f"{kind}-closing-checklist"
    typ = LANDING[kind]["typ"]
    pdf_name = f"{typ}-Closing-Checklist.pdf"
    base = os.path.join(ROOT, "resources", slug)
    os.makedirs(os.path.join(base, "thank-you"), exist_ok=True)
    os.makedirs(os.path.join(base, "download"), exist_ok=True)
    open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(landing_html(kind, slug, pdf_name))
    open(os.path.join(base, "thank-you", "index.html"), "w", encoding="utf-8").write(thankyou_html(kind, slug, pdf_name))
    hp = os.path.join(SCRATCH, slug + ".html")
    open(hp, "w", encoding="utf-8").write(pdf_html(cfg))
    out = os.path.abspath(os.path.join(base, "download", pdf_name))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + out, "file://" + hp], capture_output=True)
    ok = os.path.exists(out)
    made.append((slug, ok, os.path.getsize(out)//1024 if ok else 0))

print("Generated closing-checklist lead magnets:")
for slug, ok, kb in made:
    print("  %s  PDF:%s (%dKB)" % (slug, "OK" if ok else "FAIL", kb))

# ── /resources/ hub cards + sitemap (idempotent; placed BEFORE the city-guides
#    section so build_city_guides.py's cleanup regex never eats it) ──
MK_A, MK_B = "<!-- CLOSING-CHECKLIST-RESOURCES -->", "<!-- /CLOSING-CHECKLIST-RESOURCES -->"
cards = (
 '\n <div class="resource-card">\n <div class="resource-icon">✅</div>\n'
 ' <h2>Buyer&rsquo;s Closing Checklist</h2>\n'
 ' <p>A free, printable step-by-step checklist for closing on your Central Indiana home &mdash; what to do before, what to bring, and how to avoid wire fraud.</p>\n'
 ' <a href="/resources/buyer-closing-checklist/" class="btn btn-primary">Get the Buyer Checklist →</a>\n </div>\n'
 '\n <div class="resource-card">\n <div class="resource-icon">🏡</div>\n'
 ' <h2>Seller&rsquo;s Closing Checklist</h2>\n'
 ' <p>A free, printable step-by-step checklist for selling your Central Indiana home &mdash; from under contract to the closing table.</p>\n'
 ' <a href="/resources/seller-closing-checklist/" class="btn btn-primary">Get the Seller Checklist →</a>\n </div>\n')
section = (MK_A + '\n<div class="resources-intro" style="margin-top:16px;">'
           '<h2 style="text-align:center;color:var(--dark);font-size:1.6rem;margin:0 0 6px;">Free Closing Checklists</h2>'
           '<p>Printable buyer and seller closing checklists for Central Indiana &mdash; every step from contract to keys, plus what to bring and how to close safely.</p></div>\n'
           '<div class="resources-grid">' + cards + '</div>\n' + MK_B + '\n')

hub = os.path.join(ROOT, "resources/index.html"); ht = open(hub, encoding="utf-8").read()
ht = re.sub(re.escape(MK_A) + r".*?" + re.escape(MK_B) + r"\s*", "", ht, flags=re.DOTALL)
if '<div class="resources-intro" style="margin-top:16px;">' in ht:
    ht = ht.replace('<div class="resources-intro" style="margin-top:16px;">', section + '<div class="resources-intro" style="margin-top:16px;">', 1)
else:
    ht = ht.replace('<footer class="site-footer">', section + '<footer class="site-footer">', 1)
open(hub, "w", encoding="utf-8").write(ht)

smp = os.path.join(ROOT, "sitemap.xml"); sm = open(smp, encoding="utf-8").read(); blk = ""
for kind in ("buyer", "seller"):
    loc = "https://janetgiles.com/resources/%s-closing-checklist/" % kind
    if loc not in sm:
        blk += "<url>\n  <loc>%s</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n" % loc
if blk:
    open(smp, "w", encoding="utf-8").write(sm.replace("</urlset>", blk + "</urlset>"))
print("hub + sitemap updated (%d new sitemap URLs)" % blk.count("<url>"))
