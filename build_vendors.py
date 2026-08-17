#!/usr/bin/env python3
"""Build /vendors/ — Preferred Vendors directory, sourced from the YRL hub's
'yrl-vendors-state' (Supabase hub_content). Snapshot embedded below; to refresh,
re-pull with the same query and replace VENDORS. Reuses header/footer/hashes from
a sibling page. Emails intentionally omitted (spam); phone + website shown.
"""
import os, re, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "services", "expired-listings", "index.html")
OUT_DIR = os.path.join(ROOT, "vendors")
URL = "https://janetgiles.com/vendors/"

# Category display order (money/closing first, then home services)
ORDER = ["💰 Lenders & Mortgage", "🏛️ Title & Closing", "🔍 Home Inspectors",
 "📐 Appraisers", "🛡️ Home Warranty", "⚖️ Attorneys & Legal", "✍️ Notary & Signing",
 "🏦 Banking & Financial", "🏠 Builders & New Construction", "🚚 Moving & Hauling",
 "🛋️ Staging & Design", "📸 Photography & Media", "🔧 Contractors & Repairs",
 "🚰 Plumbing, HVAC & Electrical", "🧱 Concrete & Masonry", "🌳 Lawn, Fence & Landscaping",
 "🐜 Pest Control", "🧹 Cleaning Services", "🧰 Other Services"]

VENDORS = json.loads(r'''[
{"category":"⚖️ Attorneys & Legal","company":"Giles Law Group","contact":"Clark Giles & Steve Ruby","phone":"888-478-2889","website":"https://gileslawgroup.com/","notes":""},
{"category":"✍️ Notary & Signing","company":"Law Notary LLC","contact":"Tasha Law-Jones — CEO","phone":"317-540-3478","website":"linktr.ee/lawnotary","notes":"Mobile Loan Signing · Remote Online Notary · General Notary"},
{"category":"✍️ Notary & Signing","company":"Notary Slayer","contact":null,"phone":null,"website":null,"notes":"Mobile Notary · Loan Signing Agent · Title Producing License · Marion & surrounding counties"},
{"category":"🌳 Lawn, Fence & Landscaping","company":"Good Shepherd Fence Company","contact":"Joe Papp — Outside Sales Rep","phone":"317-677-4204","website":"www.GoodShepherdFenceCompany.com","notes":"Office 317-786-2557 · 1410 Sheldon St, Indianapolis IN 46201"},
{"category":"🌳 Lawn, Fence & Landscaping","company":"Perfect Lawns LLC","contact":"Jason Johnson","phone":"317-373-6350","website":null,"notes":"Residential & Commercial"},
{"category":"🌳 Lawn, Fence & Landscaping","company":"Steve's Tree Service","contact":null,"phone":"317-724-2669","website":null,"notes":"Trimming · Topping · Removal · Hauling · Stump Grinding · Licensed & Insured · Free estimates"},
{"category":"🏛️ Title & Closing","company":"ATA National Title Group","contact":"Karen Willits — Account Manager","phone":"317-477-7545","website":"www.atatitle.com","notes":"1298 N. State St, Greenfield IN 46140"},
{"category":"🏛️ Title & Closing","company":"Denali Title & Escrow Agency","contact":"Heather Wright — Closing Agent","phone":"317-403-5078","website":null,"notes":"Office 317-668-2152 · 14074 Trade Center Dr Ste 237, Fishers IN 46038"},
{"category":"🏛️ Title & Closing","company":"Investors Title Service","contact":"Michael J. Beasley — President","phone":"317-989-6888","website":"www.InvestorsTitleService.com","notes":"8580 Cedar Place Dr Suite 117, Indianapolis IN 46240"},
{"category":"🏛️ Title & Closing","company":"Title Alliance of Indy Metro","contact":"Kristina Earhart — Office Manager","phone":"317-884-9327","website":"www.taofindymetro.com","notes":"48 N. Emerson Ave Suite 200, Greenwood IN 46143"},
{"category":"🏛️ Title & Closing","company":"Transnation Title Agency","contact":"Sheila Alderson — Account Executive","phone":"317-885-0500","website":"www.TransnationTitle.com","notes":"1648 Fry Rd Suite B, Greenwood IN 46142"},
{"category":"🏠 Builders & New Construction","company":"Bob's Construction & Repairs","contact":null,"phone":"317-388-8885","website":"bobsconstructionindy.com","notes":"Roofing · Siding · Windows · Decks · Kitchens & Baths · Additions · Serving Indiana 30 yrs"},
{"category":"🏠 Builders & New Construction","company":"D.R. Horton","contact":"Jordan Dybas — New Home Consultant","phone":"317-496-2741","website":"www.drhorton.com","notes":"3665 Priority Way S. Dr, Indianapolis IN 46240"},
{"category":"🏠 Builders & New Construction","company":"Ron Joyner Construction","contact":"Ron Joyner — Owner","phone":"317-443-9723","website":null,"notes":"Built with Integrity"},
{"category":"🏦 Banking & Financial","company":"Crane Credit Union","contact":"Joshua Howard — Business Loan Officer","phone":"812-863-6112","website":"www.cranecu.org","notes":"2028 N. Morton St, Franklin IN 46131"},
{"category":"🏦 Banking & Financial","company":"Tides Bookkeeping","contact":"Daniel Cope — Lead Bookkeeper","phone":"864-559-2686","website":"www.tidesbookkeeping.com","notes":"QuickBooks Certified"},
{"category":"🐜 Pest Control","company":"Bugz Bug Me Pest Control","contact":"Dustin McNabney — Owner","phone":"317-221-9968","website":null,"notes":"7250 Tresa Dr, Indianapolis IN 46239"},
{"category":"🐜 Pest Control","company":"Hauk's LLC Termite & Pest Control","contact":"David Sr.","phone":"765-795-3012","website":null,"notes":"Toll-free 1-800-762-5540 · Cloverdale, IN"},
{"category":"🐜 Pest Control","company":"Orkin Pest Control","contact":"Joshua Howard — Inspector","phone":"463-239-5166","website":"www.orkin.com","notes":"3733 E Margaret Dr, Indianapolis IN 46226"},
{"category":"🐜 Pest Control","company":"Witt's Pest Control LLC","contact":"Kevin & Becky Witt — Owners","phone":"317-787-8106","website":"www.wittspestcontrol.com","notes":"Commercial & Residential · Since 1990"},
{"category":"💰 Lenders & Mortgage","company":"Bailey & Wood / Hoosier Mortgage Team","contact":"Jody Bleier — Mortgage Consultant","phone":"317-213-1387","website":"hoosiermortgageteam.com","notes":"NMLS #226933 · 616 N Madison Ave, Greenwood IN 46142"},
{"category":"💰 Lenders & Mortgage","company":"CrownMark Mortgage Inc","contact":"Joe Rangel — Sr. Mortgage Consultant","phone":"317-594-9800","website":"www.crownmarkgroup.com","notes":"NMLS #146972 · 8980 Technology Dr, Fishers IN 46038"},
{"category":"💰 Lenders & Mortgage","company":"Elements Financial","contact":"Brad Smith — Mortgage Loan Originator","phone":"317-331-4587","website":"elements.org/bsmith","notes":"Toll-free 800-621-2105 x7443"},
{"category":"💰 Lenders & Mortgage","company":"Fairway / Team Turley","contact":"Angie Turley — Branch Sales Manager","phone":"317-797-0615","website":"www.teamturley.com","notes":"NMLS #363066 · 1 West Main St, Mooresville IN 46158"},
{"category":"💰 Lenders & Mortgage","company":"First Community Mortgage","contact":"Sherry Sullivan — Team Loan Originator","phone":"317-522-8301","website":"firstcommunitymortgage.com/sherrysullivan","notes":"NMLS 2135930 · 3815 River Crossing Pkwy Suite 100, Indianapolis IN 46240"},
{"category":"💰 Lenders & Mortgage","company":"Grandview Lending Inc","contact":"Michael Farrell — President","phone":"317-833-8143","website":"www.grandviewlending.com","notes":"NMLS 168737 · 8445 Keystone Crossing Blvd Suite 101, Indianapolis IN 46240"},
{"category":"💰 Lenders & Mortgage","company":"Ruoff Mortgage","contact":"Melissa Lutes — Senior Loan Officer","phone":"812-639-2041","website":"apply.ruoff.com/melissalutes","notes":"NMLS 234601 · 9100 Keystone Crossing Suite 750, Indianapolis IN 46240"},
{"category":"💰 Lenders & Mortgage","company":"Team Turley / Fairway","contact":"Josh Hargis — Business Development Manager","phone":"317-557-3245","website":"www.teamturley.com","notes":"1 W Main St, Mooresville IN 46158"},
{"category":"💰 Lenders & Mortgage","company":"The Huntington National Bank","contact":"Amanda Shepard — CRA Mortgage Loan Officer","phone":"317-361-2012","website":"www.huntington.com","notes":"NMLS 444455 · 45 N Pennsylvania St, Indianapolis IN 46204"},
{"category":"📐 Appraisers","company":"Spoonamore Appraisal Group","contact":"Josh Spoonamore — Certified Residential Appraiser","phone":"317-997-2934","website":"spoonamoreag.com","notes":"Office 317-536-1886"},
{"category":"📸 Photography & Media","company":"Myers Imaging","contact":"Mark Myers — Photographer","phone":"317-383-6627","website":"myersimaging.com","notes":""},
{"category":"🔍 Home Inspectors","company":"Carter's Home Inspections Inc","contact":"David L. Carter — Certified Professional Home Inspector","phone":"317-363-9262","website":"www.cartershomeinspectionsinc.com","notes":""},
{"category":"🔍 Home Inspectors","company":"HouseMaster (Heartland)","contact":"Trent Paino — Owner / Inspector","phone":"317-513-1968","website":"heartland.housemaster.com","notes":"Office 317-209-9100"},
{"category":"🔍 Home Inspectors","company":"IH Inspections","contact":"Shane Martin — Licensed Professional Home Inspector","phone":"317-519-4293","website":"ihinspections.com","notes":""},
{"category":"🔧 Contractors & Repairs","company":"ALTIC Lock Service","contact":null,"phone":"317-490-1469","website":null,"notes":"Locksmith · Since 2005"},
{"category":"🔧 Contractors & Repairs","company":"Blair & Norris","contact":"Kamree Bowling — Office Support","phone":"317-245-7262","website":"BlairNorris.com","notes":"Well · Pump · Drilling · Septic · 12610 Southeastern Ave, Indianapolis IN 46259"},
{"category":"🔧 Contractors & Repairs","company":"Carpets Mostly — Abbey Carpet & Floor","contact":"Powers Hapgood","phone":"317-881-3265","website":null,"notes":"Flooring · Carpet · Hardwood · Laminate · Vinyl · Since 1964 · 3230 W. Southport Rd, Indianapolis IN 46217"},
{"category":"🔧 Contractors & Repairs","company":"CP & Associates Painting","contact":null,"phone":"317-460-8090","website":null,"notes":"Interior/Exterior · Staining · Power Washing · Epoxy · Greenwood IN 46142"},
{"category":"🔧 Contractors & Repairs","company":"Gilpin Glass Service","contact":"Sherry Doss","phone":"317-635-7256","website":null,"notes":"Residential & Commercial glass · 2908 E. Washington St, Indianapolis IN 46201"},
{"category":"🔧 Contractors & Repairs","company":"Indy Roof Company","contact":"Quinton Miller — Project Manager","phone":"219-819-9683","website":null,"notes":"Roofing · 5240 Elmwood Ave, Indianapolis IN 46203"},
{"category":"🔧 Contractors & Repairs","company":"Innovative Garages Inc","contact":"Lisa Newkirk — Office Manager","phone":"317-272-5163","website":"www.InnovativeGarages.com","notes":"Showroom 154 Vista Park Way, Avon IN 46123"},
{"category":"🔧 Contractors & Repairs","company":"Kelley Locksmith LLC","contact":"Jeff Kelley — Registered Locksmith","phone":"765-525-5397","website":"kelleylocksmith.com","notes":"Residential · Commercial · Automotive · High Security"},
{"category":"🔧 Contractors & Repairs","company":"ProSource Wholesale","contact":"Lynn Weathers","phone":"317-992-0135","website":"www.prosourcewholesale.com/indianapolis","notes":"Flooring & project supplies · 7375 Company Dr, Indianapolis IN 46237"},
{"category":"🔧 Contractors & Repairs","company":"VIP Home Solutions","contact":"Heather Griggs — Business Development","phone":"317-883-1909","website":null,"notes":"General Contractor · Financing available · 5602 Madison Ave, Indianapolis IN 46227"},
{"category":"🧰 Other Services","company":"Christy's Design & Sign Inc","contact":"Christy Holt","phone":"317-882-5444","website":null,"notes":"500 S. Polk St Suite 17, Greenwood IN 46143"},
{"category":"🧰 Other Services","company":"Finchum's Computer Services","contact":"Ryan T. Finchum — Owner","phone":"317-847-3279","website":"www.finchumfixesit.com","notes":"213 Black Maple Court, Greenwood IN 46143"},
{"category":"🧱 Concrete & Masonry","company":"Jordans Concrete Services","contact":"Jordan Henry","phone":"317-442-3403","website":null,"notes":"Call or text"},
{"category":"🧱 Concrete & Masonry","company":"Rod's Custom Concrete","contact":"Rod Vore","phone":"463-336-0035","website":null,"notes":"Commercial & Residential · Since 1989 · Whiteland IN 46184"},
{"category":"🧱 Concrete & Masonry","company":"S&F Marble and Granite LLC","contact":"Saul Cabrera — Owner","phone":"317-400-9959","website":"snfstone.com","notes":"Countertops · 1308 West Troy Ave"},
{"category":"🧹 Cleaning Services","company":"Green Apron Cleaning Services","contact":"Michele Matherly — Owner","phone":"317-727-3121","website":"greenaproncleaning.com","notes":"244 Leaning Tree Rd, Greenwood IN 46142"},
{"category":"🚚 Moving & Hauling","company":"Here To There Movers","contact":null,"phone":"1-888-218-6683","website":"www.heretotheremovers.com","notes":"Local & long distance"},
{"category":"🚚 Moving & Hauling","company":"Professional Estate Services","contact":"Brandon Keith — President","phone":"317-504-6158","website":null,"notes":"Cash buy-outs · Moving/Hauling · Furniture disposal · Personal property appraiser"},
{"category":"🚰 Plumbing, HVAC & Electrical","company":"Electrical Enterprises Inc","contact":"Jason Straber","phone":"317-784-2224","website":null,"notes":"Electrical Contractors · 5715 Churchman Ave Suite M, Indianapolis IN 46203"},
{"category":"🚰 Plumbing, HVAC & Electrical","company":"Indiana Filter Supply","contact":null,"phone":"317-827-2754","website":"www.indianafilter.com","notes":"HVAC filters · North 317-827-2754 · South 317-788-2897"},
{"category":"🚰 Plumbing, HVAC & Electrical","company":"Make It Mowery","contact":"John Perkins","phone":"317-608-7173","website":"www.makeitmowery.com","notes":"Heating · A/C · Plumbing · Drain Cleaning · Brownsburg IN"},
{"category":"🚰 Plumbing, HVAC & Electrical","company":"Professional Plumbing Services LLC","contact":"Steve Anderson — Owner / Technician","phone":"317-531-8775","website":"ProfessionalPlumbingService.net","notes":"PC 19700042 · 264 Howard Rd, Greenwood IN 46142"},
{"category":"🛋️ Staging & Design","company":"A&V Interior Design","contact":"Vicki Bosley","phone":"330-962-6657","website":null,"notes":"Also: Jeanne McCullough 317-371-1492"},
{"category":"🛡️ Home Warranty","company":"ACHOSA","contact":"Marti Brown","phone":"317-712-6368","website":"achosahw.com","notes":""},
{"category":"🛡️ Home Warranty","company":"American Home Shield / HSA","contact":"Angela Wire — Account Manager","phone":"317-491-3773","website":"www.ahs.com","notes":"Also www.onlinehsa.com"},
{"category":"🛡️ Home Warranty","company":"Residential Warranty Services Inc","contact":"Jon Wirth — Account Manager","phone":"317-640-1499","website":"www.rwswarranty.com","notes":"Orders/Claims 800-544-8156 · 698 Pro-Med Lane, Carmel IN 46032"}
]''')

# Static, factual Central Indiana utilities (not referral vendors — a setup helper)
UTILITIES = [
 ("Electric", "AES Indiana (Indianapolis/Marion County)", "888-261-8222", "aesindiana.com"),
 ("Electric", "Duke Energy Indiana (most suburbs)", "800-521-2232", "duke-energy.com"),
 ("Gas", "Citizens Energy Group (Indianapolis metro)", "317-924-3311", "citizensenergygroup.com"),
 ("Gas", "CenterPoint Energy (select areas)", "800-227-1376", "centerpointenergy.com"),
 ("Water / Sewer", "Citizens Water (Indianapolis) / Indiana American Water / your town utility", "317-924-3311", "citizensenergygroup.com"),
 ("Trash / Recycling", "By city — municipal service or Republic/Ray's/GFL (ask your town)", "", ""),
 ("Internet / TV", "AT&T · Xfinity (Comcast) · Metronet · T-Mobile Home Internet", "", ""),
]

src = open(TPL, encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

def esc(s): return html.escape(s or "", quote=True)
def telnum(p): return re.sub(r"\D", "", p or "")
def anchor(cat): return re.sub(r"[^a-z0-9]+", "-", cat.split(" ", 1)[-1].lower()).strip("-")
def norm_url(u):
    if not u: return None
    return u if u.startswith("http") else "https://" + u

def vcard(v):
    parts = [f'<h3>{esc(v["company"])}</h3>']
    if v.get("contact"): parts.append(f'<p class="vd-contact">{esc(v["contact"])}</p>')
    rows = []
    if v.get("phone"):
        rows.append(f'<a class="vd-row" href="tel:{telnum(v["phone"])}">📞 {esc(v["phone"])}</a>')
    if v.get("website"):
        rows.append(f'<a class="vd-row" href="{esc(norm_url(v["website"]))}" target="_blank" rel="noopener nofollow">🌐 {esc(v["website"])}</a>')
    if rows: parts.append('<div class="vd-links">' + "".join(rows) + '</div>')
    if v.get("notes"): parts.append(f'<p class="vd-notes">{esc(v["notes"])}</p>')
    return '<div class="vendor-card">' + "".join(parts) + '</div>'

# group + order
bycat = {}
for v in VENDORS: bycat.setdefault(v["category"], []).append(v)
sections = ""
for cat in ORDER:
    if cat not in bycat: continue
    cards = "\n".join(vcard(v) for v in sorted(bycat[cat], key=lambda x: x["company"]))
    sections += f'\n<h2 id="{anchor(cat)}">{esc(cat)}</h2>\n<div class="vendor-grid">\n{cards}\n</div>\n'

jump_html = "\n".join(f'  <a href="#{anchor(c)}">{esc(c)}</a>' for c in ORDER if c in bycat)

def util_row(t, name, ph, w):
    cell = f'<strong>{esc(name)}</strong>'
    if ph: cell += f' · <a href="tel:{telnum(ph)}">{esc(ph)}</a>'
    if w:  cell += f' · <a href="https://{esc(w)}" target="_blank" rel="noopener nofollow">{esc(w)}</a>'
    return f'<tr><td>{esc(t)}</td><td>{cell}</td></tr>'
util_rows = "\n".join(util_row(*u) for u in UTILITIES)

count = len(VENDORS)
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Preferred Vendors &amp; Trusted Local Partners | Your Realty Link</title>
 <meta name="description" content="Your Realty Link's preferred local vendors across Central Indiana — trusted lenders, title companies, home inspectors, contractors, movers, home warranty, and more.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="Preferred Vendors & Trusted Local Partners | Your Realty Link">
 <meta property="og:description" content="Trusted Central Indiana lenders, title companies, inspectors, contractors, movers, and more — vetted by Your Realty Link.">
 <meta property="og:url" content="{URL}">
 <meta property="og:image" content="https://janetgiles.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@graph": [
 {{ "@type": "WebPage", "url": "{URL}", "name": "Preferred Vendors" }},
 {{ "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Preferred Vendors", "item": "{URL}" }} ] }}
 ] }}
 </script>
 {FONTS}
 <style>
.vendors-wrap {{ max-width: 1000px; margin: 0 auto; padding: 10px 0 40px; }}
.vendors-wrap h2 {{ color: #13294a; font-size: 1.35rem; margin: 2.2rem 0 .3rem; scroll-margin-top: 80px; }}
.vendor-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-top: 14px; }}
.vendor-card {{ background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; box-shadow: 0 2px 10px rgba(0,0,0,.05); }}
.vendor-card h3 {{ font-size: 1.02rem; color: #13294a; margin: 0 0 3px; }}
.vendor-card .vd-contact {{ font-size: .84rem; color: var(--mid); font-weight: 600; margin: 0 0 10px; }}
.vendor-card .vd-links {{ display: flex; flex-direction: column; gap: 6px; }}
.vendor-card .vd-row {{ font-size: .88rem; color: var(--red); font-weight: 600; text-decoration: none; word-break: break-word; }}
.vendor-card .vd-row:hover {{ text-decoration: underline; }}
.vendor-card .vd-notes {{ font-size: .78rem; color: var(--text-muted, #9ca3af); line-height: 1.5; margin: 12px 0 0; padding-top: 10px; border-top: 1px solid var(--border); }}
.vendor-jump {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 6px; }}
.vendor-jump a {{ background: var(--light); border: 1px solid var(--border); border-radius: 100px; padding: 7px 14px; font-size: 13px; font-weight: 600; color: #13294a; text-decoration: none; }}
.vendor-jump a:hover {{ border-color: var(--red); color: var(--red); }}
.util-table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: .9rem; }}
.util-table td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }}
.util-table td:first-child {{ font-weight: 700; color: var(--red); white-space: nowrap; width: 130px; }}
.vd-disclaimer {{ font-size: .82rem; color: #6e6e70; background: var(--light); border-radius: 10px; padding: 14px 18px; margin: 8px 0 0; }}
 </style>
</head>
<body>

{HEADER}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> Preferred Vendors</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>Our Preferred Vendors</h1>
 <p class="hero-sub">Buying, selling, or just keeping up a home in Central Indiana is easier with people you can trust. These are the local lenders, title companies, inspectors, contractors, and service pros <strong>Your Realty Link clients rely on</strong> &mdash; {count}+ vetted partners in one place.</p>
 <div class="hero-badges">
 <span class="hero-badge">💰 Lenders</span>
 <span class="hero-badge">🏛️ Title &amp; Closing</span>
 <span class="hero-badge">🔍 Inspectors</span>
 <span class="hero-badge">🔧 Contractors</span>
 </div>
 </div>
</section>

<div class="container">
 <div class="vendors-wrap">

 <div class="vendor-jump">
{jump_html}
 </div>
{sections}

 <h2 id="utilities">🔌 Utilities &amp; Home Setup</h2>
 <p>Setting up a new home? Here are the main Central Indiana utility providers. Your exact electric, water, and trash provider depends on your address &mdash; when in doubt, ask us and we&rsquo;ll point you to the right one.</p>
 <table class="util-table"><tbody>
{util_rows}
 </tbody></table>

 <p class="vd-disclaimer">These businesses are independent third parties, not affiliated with or paid by Your Realty Link, and we receive no compensation, referral fees, or kickbacks for listing them. They&rsquo;re shared as a convenience based on our experience; please do your own due diligence and confirm licensing, insurance, and pricing directly. To be added or updated, <a href="/contact/">contact us</a>.</p>

 <div class="cta-block" style="margin-top:28px;">
 <h3>Need a Recommendation?</h3>
 <p>Not sure who to call? Tell us what you need and we&rsquo;ll connect you with the right trusted local pro.</p>
 <div class="btn-group">
 <a href="tel:3179977404" class="btn btn-white">📞 Call Us: 317-997-7404</a>
 <a href="/contact/" class="btn btn-outline">Ask for a Referral →</a>
 </div>
 </div>

 </div>
</div>

{FOOTER}

{SCRIPTS}'''

os.makedirs(OUT_DIR, exist_ok=True)
open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page)

sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read()
if URL not in s:
    open(sm, "w", encoding="utf-8").write(s.replace("</urlset>", f"<url>\n  <loc>{URL}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.6</priority>\n</url>\n</urlset>"))
    print("added sitemap entry")
print(f"built /vendors/ with {count} vendors across {len(bycat)} categories")
