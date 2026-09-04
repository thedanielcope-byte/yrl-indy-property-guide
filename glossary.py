#!/usr/bin/env python3
"""
Glossary generator — builds /glossary/index.html (A-Z + categories + schema) and
/glossary/<slug>/index.html full explainer pages, matching the site design.

Data:
  - TERMS_BASE below (the original ~46 terms).
  - glossary-new-terms.json  (extra index-only terms: [{term,cat,def}])
  - glossary-pages.json       (full explainer pages: [{slug,term,h1,title,meta,...}])
The 9 hand-built full pages (escrow, earnest-money, …) are left untouched; the
index just links to them. New full pages are (re)generated from glossary-pages.json.

Run: python3 glossary.py
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://yourrealtylink.com"

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
CANON_HDR = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
CANON_FTR = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
TAIL = src[src.index('</footer>') + len('</footer>'):src.index('</body>')]
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)

def esc(s): return html.escape(str(s or ""), quote=True)

# ── The original 46 terms: (term, category, definition, link-or-None) ──
CATS = ["Lending & Mortgage", "Offers & Contracts", "Inspections & Appraisal",
        "Title & Legal", "Closing & Costs", "Listing & Market",
        "Taxes & Ownership", "New Construction", "Investment",
        "HOA & Community", "Roles & Working With Agents"]

TERMS_BASE = [
 ("Adjustable-rate mortgage (ARM)", "Lending & Mortgage", "A mortgage whose interest rate changes periodically after an initial fixed period, causing your payment to rise or fall.", None),
 ("Amortization", "Lending & Mortgage", "The schedule by which loan payments are applied to interest and principal over time. Early payments are mostly interest; later ones mostly principal.", "/glossary/amortization/"),
 ("Appraisal", "Inspections & Appraisal", "An independent professional estimate of a property's market value, ordered by your lender to confirm the home supports the loan amount.", "/glossary/home-appraisal/"),
 ("Appraisal gap", "Inspections & Appraisal", "The difference between the contract price and a lower appraised value, which the buyer generally must cover in cash.", "/glossary/appraisal-gap/"),
 ("As-is", "Offers & Contracts", "A sale in which the seller will not make repairs. You can still inspect, and in Indiana the seller must still complete a disclosure.", "/glossary/as-is-sale/"),
 ("Backup offer", "Offers & Contracts", "A formal second-position offer that moves to first if the current contract falls through. Worth submitting on a contingent listing.", "/glossary/contingent-vs-pending/"),
 ("Buyer's agency agreement", "Roles & Working With Agents", "A written agreement setting out what your agent will do and how they're paid. Buyers now sign one before touring homes.", "/glossary/buyers-agency-agreement/"),
 ("Closing", "Closing & Costs", "The final step, where documents are signed, funds are disbursed, and ownership transfers to the buyer.", "/glossary/closing-day/"),
 ("Closing costs", "Closing & Costs", "Fees and prepaid items due at closing — loan origination, title, recording, taxes and insurance. Commonly 2–5% of price for buyers.", "/services/closing-costs-buyers/"),
 ("Closing disclosure", "Closing & Costs", "A standardized form itemizing your final loan terms and closing costs, provided at least three business days before closing.", None),
 ("Comparables (comps)", "Listing & Market", "Recently sold homes similar in size, age, condition and location, used to estimate value.", "/glossary/comparative-market-analysis/"),
 ("Comparative market analysis (CMA)", "Listing & Market", "An agent's estimate of a home's value based on recent comparable sales, current competition, and market trends.", "/glossary/comparative-market-analysis/"),
 ("Contingency", "Offers & Contracts", "A condition that must be met for a sale to proceed. If unmet, the buyer can usually cancel and recover their earnest money.", "/glossary/contingency/"),
 ("Contingent", "Listing & Market", "A listing status meaning an offer is accepted but conditions such as inspection or financing are still outstanding.", "/glossary/contingent-vs-pending/"),
 ("Conventional loan", "Lending & Mortgage", "A mortgage not insured by a government program. Often as little as 3–5% down, with PMI required under 20%.", "/glossary/conventional-loan/"),
 ("Days on market (DOM)", "Listing & Market", "How long a home has been actively listed before going under contract — a signal of demand and of negotiating room.", "/glossary/days-on-market/"),
 ("Deed", "Title & Legal", "The legal document transferring ownership of real property from one party to another.", "/glossary/deed/"),
 ("Down payment", "Lending & Mortgage", "The portion of the purchase price you pay upfront. Ranges from 0% on VA and USDA loans to 20%+ on conventional.", "/services/down-payment-assistance/"),
 ("Earnest money", "Offers & Contracts", "A good-faith deposit submitted with an offer, held in escrow and credited toward your costs at closing.", "/glossary/earnest-money/"),
 ("Easement", "Title & Legal", "A right allowing someone else to use part of your property for a specific purpose, such as utility access.", None),
 ("Equity", "Taxes & Ownership", "The difference between your home's market value and what you still owe on it.", "/glossary/home-equity/"),
 ("Escrow", "Closing & Costs", "A neutral third party holding money or documents until conditions are met. Also the lender account that pays your taxes and insurance.", "/glossary/escrow/"),
 ("FHA loan", "Lending & Mortgage", "A government-insured mortgage with lower credit thresholds and a low down payment, popular with first-time buyers.", "/services/fha-loan-buyers/"),
 ("Fixed-rate mortgage", "Lending & Mortgage", "A mortgage whose interest rate stays the same for the life of the loan.", None),
 ("HOA (homeowners association)", "HOA & Community", "An organization governing a community, funded by dues, that maintains shared areas and enforces rules. Always review the documents and dues history.", "/glossary/hoa/"),
 ("Home inspection", "Inspections & Appraisal", "A professional evaluation of a home's condition and systems, typically performed during the inspection contingency period.", "/glossary/home-inspection/"),
 ("Homestead exemption", "Taxes & Ownership", "An Indiana property tax deduction available on your primary residence. File it after closing — it lowers your tax bill.", "/glossary/homestead-exemption/"),
 ("Lien", "Title & Legal", "A legal claim against a property for an unpaid debt. Liens must generally be cleared before ownership transfers.", None),
 ("Loan estimate", "Lending & Mortgage", "A standardized form showing your estimated loan terms and closing costs, provided shortly after you apply.", None),
 ("MIBOR", "Listing & Market", "The Metropolitan Indianapolis Board of Realtors, which operates the MLS covering Central Indiana.", None),
 ("MLS", "Listing & Market", "The Multiple Listing Service — the database where brokers share active listings and sale data.", None),
 ("Pending", "Listing & Market", "A listing status meaning contingencies are cleared and the sale is moving toward closing.", "/glossary/contingent-vs-pending/"),
 ("PMI (private mortgage insurance)", "Lending & Mortgage", "Insurance protecting the lender when a conventional borrower puts less than 20% down. Removable once you build enough equity.", "/glossary/private-mortgage-insurance/"),
 ("Pre-approval", "Lending & Mortgage", "A lender's conditional commitment based on verified income, assets and credit. Stronger than a pre-qualification.", "/glossary/pre-approval-vs-pre-qualification/"),
 ("Pre-qualification", "Lending & Mortgage", "An informal estimate of what you might borrow, based on unverified information.", "/glossary/pre-approval-vs-pre-qualification/"),
 ("Principal", "Lending & Mortgage", "The amount you borrowed, separate from interest.", None),
 ("Property tax caps", "Taxes & Ownership", "Indiana constitutional limits on property tax as a share of assessed value, which vary by property type.", "/glossary/property-tax-caps/"),
 ("Seller's disclosure", "Title & Legal", "An Indiana-required form on which sellers report known defects. It reflects knowledge, not condition — never a substitute for inspection.", "/glossary/sellers-disclosure/"),
 ("Short sale", "Listing & Market", "A sale for less than the mortgage balance, requiring lender approval.", "/services/short-sale/"),
 ("Survey", "Title & Legal", "A drawing showing a property's legal boundaries, structures and easements.", None),
 ("Title", "Title & Legal", "Legal ownership of a property, and the history of that ownership.", "/glossary/title-insurance/"),
 ("Title insurance", "Title & Legal", "A one-time policy protecting against ownership problems that predate your purchase, such as liens or recording errors.", "/glossary/title-insurance/"),
 ("Underwriting", "Lending & Mortgage", "The lender's final review of your finances and the property before issuing loan approval.", None),
 ("USDA loan", "Lending & Mortgage", "A zero-down loan for eligible rural areas — which covers more of Central Indiana than most buyers expect.", "/services/usda-loans/"),
 ("VA loan", "Lending & Mortgage", "A loan for eligible veterans and service members, typically with no down payment and no mortgage insurance.", "/services/va-loan-buyers/"),
 ("Walk-through", "Closing & Costs", "A final inspection shortly before closing to confirm the home's condition and that agreed repairs were made.", "/glossary/final-walk-through/"),
]

# Full pages that already exist by hand (index links to them; generator won't rebuild).
EXISTING_FULL = {"appraisal-gap", "contingency", "contingent-vs-pending", "days-on-market",
                 "earnest-money", "escrow", "private-mortgage-insurance",
                 "sellers-disclosure", "title-insurance"}

def load_json(name):
    p = os.path.join(ROOT, name)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print(f"  ! {name}: {e}")
    return []

NEW_TERMS = load_json("glossary-new-terms.json")   # [{term,cat,def}]
FULL_PAGES = load_json("glossary-pages.json")        # [{slug,term,h1,...}]

# Merge all index terms
def norm(t): return re.sub(r"\s*\(.*?\)", "", t).strip().lower()
ALL = []
seen = set()
for t in TERMS_BASE:
    ALL.append({"term": t[0], "cat": t[1], "def": t[2], "link": t[3]})
    seen.add(norm(t[0]))
for t in NEW_TERMS:
    term = html.unescape(str(t.get("term", ""))).strip()
    if not term or norm(term) in seen:
        continue
    seen.add(norm(term))
    ALL.append({"term": term, "cat": html.unescape(str(t.get("cat", "Listing & Market"))),
                "def": html.unescape(str(t.get("def", ""))), "link": None})

ALL.sort(key=lambda x: x["term"].lower())
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def first_letter(term):
    c = term.lstrip("\"'").upper()[:1]
    return c if c in LETTERS else "#"

# Full-page slug->term map (existing + new) for the sidebar list
FULL_SLUGS = {p["slug"]: p["term"] for p in FULL_PAGES}
EXISTING_LABELS = {
    "escrow": "Escrow", "earnest-money": "Earnest Money", "contingency": "Contingency",
    "contingent-vs-pending": "Contingent vs Pending", "private-mortgage-insurance": "PMI",
    "sellers-disclosure": "Seller's Disclosure", "title-insurance": "Title Insurance",
    "appraisal-gap": "Appraisal Gap", "days-on-market": "Days on Market",
}

GL_CSS = """
 .gl-az { display:flex; flex-wrap:wrap; gap:6px; margin:12px 0 26px; }
 .gl-az a, .gl-az span { display:inline-flex; width:34px; height:34px; align-items:center; justify-content:center; border-radius:6px; font-weight:700; font-size:.9rem; }
 .gl-az a { border:1px solid #e4e4e4; color:var(--red); text-decoration:none; }
 .gl-az a:hover { background:var(--red); color:#fff; border-color:var(--red); }
 .gl-az span { color:#cfcfcf; }
 .gl-letter { font-family:var(--font-serif,'Playfair Display',Georgia,serif); color:var(--red); font-size:1.5rem; border-bottom:2px solid #eee; padding-bottom:4px; margin:30px 0 4px; scroll-margin-top:90px; }
 .gl-cat { display:inline-block; font-size:.66rem; text-transform:uppercase; letter-spacing:.05em; color:#9a9a9a; font-weight:700; margin-left:8px; vertical-align:middle; }
"""

def index_page():
    n = len(ALL)
    present = sorted({first_letter(t["term"]) for t in ALL})
    # A-Z nav
    az = "".join(
        (f'<a href="#L{c}">{c}</a>' if c in present else f'<span>{c}</span>')
        for c in LETTERS)
    # grouped list
    groups = []
    cur = None
    body = []
    for t in ALL:
        L = first_letter(t["term"])
        if L != cur:
            cur = L
            body.append(f'<h2 class="gl-letter" id="L{esc(L)}">{esc(L)}</h2>\n<dl class="gl-list">')
            # close previous handled by join below; simpler: build per-letter
    # Rebuild grouped properly
    body = []
    cur = None
    for t in ALL:
        L = first_letter(t["term"])
        if L != cur:
            if cur is not None:
                body.append("</dl>")
            cur = L
            body.append(f'<h2 class="gl-letter" id="L{esc(L)}">{esc(L)}</h2>')
            body.append('<dl class="gl-list">')
        dt = f'<a href="{t["link"]}">{esc(t["term"])}</a>' if t["link"] else esc(t["term"])
        body.append(f'  <div class="gl-item"><dt>{dt} <span class="gl-cat">{esc(t["cat"])}</span></dt><dd>{esc(t["def"])}</dd></div>')
    if cur is not None:
        body.append("</dl>")
    list_html = "\n".join(body)

    # DefinedTermSet schema
    terms_json = ",\n".join(
        '{ "@type": "DefinedTerm", "name": %s, "description": %s }' % (json.dumps(t["term"]), json.dumps(t["def"]))
        for t in ALL)

    # sidebar full-explainer list (existing + new), alpha by label
    full_links = {}
    for s in EXISTING_FULL:
        full_links[s] = EXISTING_LABELS.get(s, s.replace("-", " ").title())
    for s, term in FULL_SLUGS.items():
        full_links[s] = term
    side = "\n".join(
        f'  <a href="/glossary/{s}/" class="city-card">{esc(lbl)} <span class="arrow">&rsaquo;</span></a>'
        for s, lbl in sorted(full_links.items(), key=lambda kv: kv[1].lower()))

    desc = f"Plain-English definitions of {n}+ real estate terms for Indiana buyers and sellers — mortgages, contracts, title, taxes, closing and more."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Indiana Real Estate Glossary | Your Realty Link</title>
 <meta name="description" content="{esc(desc)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{SITE}/glossary/">
 <meta property="og:title" content="Indiana Real Estate Glossary | Your Realty Link">
 <meta property="og:description" content="{esc(desc)}">
 <meta property="og:url" content="{SITE}/glossary/">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{
 "@context": "https://schema.org",
 "@graph": [
 {{ "@type": "WebPage", "url": "{SITE}/glossary/", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead"] }} }},
 {{
 "@type": ["LocalBusiness", "RealEstateAgent"],
 "name": "Your Realty Link", "url": "https://yourrealtylink.com",
 "telephone": "317-997-7404", "email": "info@yourrealtylink.com",
 "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US" }},
 "areaServed": {{ "@type": "City", "name": "Indianapolis", "containedIn": "Marion County, Indiana" }},
 "sameAs": ["https://www.facebook.com/yourrealtylink", "https://www.linkedin.com/company/your-realty-link-llc/"]
 }},
 {{
 "@type": "DefinedTermSet",
 "name": "Indiana Real Estate Glossary",
 "url": "{SITE}/glossary/",
 "hasDefinedTerm": [
{terms_json}
 ]
 }},
 {{ "@type": "BreadcrumbList", "itemListElement": [{{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},{{ "@type": "ListItem", "position": 2, "name": "Glossary", "item": "{SITE}/glossary/" }}] }}
 ]
 }}
 </script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" rel="stylesheet">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 <style>{GL_CSS}</style>
</head>
<body>

{CANON_HDR}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> Glossary</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>Indiana Real Estate <em>Glossary</em></h1>
 <p class="hero-sub">Plain-English definitions of the terms you'll actually run into buying or selling a home in Central Indiana.</p>
 <div class="hero-badges">
 <span class="hero-badge">📘 {n} Terms</span>
 <span class="hero-badge">📍 Indiana-Specific</span>
 <span class="hero-badge">🔑 Buyers &amp; Sellers</span>
 </div>
 </div>
</section>

<div class="container">
 <div class="content-wrap">
 <main class="content-main">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">This glossary defines <strong>{n} real estate terms</strong> in plain English for Indiana buyers and sellers — from <a href="/glossary/earnest-money/">earnest money</a> and <a href="/glossary/escrow/">escrow</a> to <a href="/glossary/contingency/">contingencies</a>, <a href="/glossary/private-mortgage-insurance/">PMI</a>, and Indiana's required <a href="/glossary/sellers-disclosure/">seller's disclosure</a>. Terms shown as links have a full explainer page.</p>
</div>
<!-- QA-END -->

 <p>Real estate has a jargon problem. Most of these words describe simple ideas dressed up in language that makes buyers feel like they're missing something. They usually aren't. Below is every term you're likely to meet in a Central Indiana transaction, defined plainly, with Indiana-specific notes where the state does things its own way.</p>

 <nav class="gl-az" aria-label="Jump to letter">{az}</nav>

{list_html}

 <div class="cta-block">
 <h3>Still Have Questions?</h3>
 <p>We'd rather explain it now than have you guess. Call Daniel Cope at 317-997-7404 — no pressure, no obligation.</p>
 <div class="btn-group">
 <a href="/contact/" class="btn btn-white">Contact Your Realty Link →</a>
 <a href="/guides/buying-a-home-in-indianapolis/" class="btn btn-outline">Read the Buying Guide</a>
 </div>
 </div>

 </main>

 <aside class="content-sidebar">
 <div class="sidebar-card">
 <div class="sidebar-card-header">Full Explainers</div>
 <div class="sidebar-card-body" style="padding:12px;">
{side}
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Start Here</div>
 <div class="sidebar-card-body">
 <p>New to buying or selling in Central Indiana? These walk through the whole process.</p>
 <a href="/guides/buying-a-home-in-indianapolis/" class="btn btn-primary btn-sm btn-full">Buying Guide →</a>
 <a href="/guides/selling-a-home-in-indianapolis/" class="btn btn-outline btn-sm btn-full">Selling Guide</a>
 </div>
 </div>
 </aside>

 </div>
</div>

{CANON_FTR}
{TAIL}</body>
</html>
"""

def htmlish(s):
    # For fields with intentional inline <a> links: restore the tag delimiters
    # only, leaving &amp;/&mdash;/etc. as valid entities.
    return str(s or "").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')

def txt(s):
    # For plain-text display fields: normalize any entities the writer included,
    # then re-escape properly (avoids double-encoding like &amp;amp;).
    return esc(html.unescape(str(s or "")))

def sch(s):
    return html.unescape(str(s or ""))  # plain text for JSON-LD

def full_page(p):
    slug, term = p["slug"], p["term"]
    qa_facts = "".join(f"<div><dt>{txt(a)}</dt><dd>{txt(b)}</dd></div>" for a, b in p.get("qa_facts", []))
    sections = ""
    for h2, paras in p.get("sections", []):
        sections += f"\n <h2>{txt(h2)}</h2>\n" + "\n".join(f" <p>{htmlish(para)}</p>" for para in paras)
    faqs_html = ""
    for q, a in p.get("faqs", []):
        faqs_html += f'\n  <details class="faq-item">\n <summary>{txt(q)}</summary>\n <div class="faq-answer">\n <p>{txt(a)}</p>\n </div>\n </details>\n'
    faq_schema = ",\n".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }' % (json.dumps(sch(q)), json.dumps(sch(a)))
        for q, a in p.get("faqs", []))
    related = "".join(f'  <a href="{u}" class="city-card">{esc(l)} <span class="arrow">&rsaquo;</span></a>\n' for l, u in p.get("related", []))
    sid = re.sub(r"[^a-z0-9]+", "-", slug)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(p['title'])}</title>
 <meta name="description" content="{esc(p['meta'])}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{SITE}/glossary/{slug}/">
 <meta property="og:title" content="{esc(p['title'])}">
 <meta property="og:description" content="{esc(p['meta'])}">
 <meta property="og:url" content="{SITE}/glossary/{slug}/">
 <meta property="og:type" content="article">
 <script type="application/ld+json">
 {{
 "@context": "https://schema.org",
 "@graph": [
 {{ "@type": "WebPage", "url": "{SITE}/glossary/{slug}/", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"] }} }},
 {{
 "@type": ["LocalBusiness", "RealEstateAgent"],
 "name": "Your Realty Link", "url": "https://yourrealtylink.com", "logo": "/assets/img/yrl-logo.png",
 "telephone": "317-997-7404", "email": "info@yourrealtylink.com",
 "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US" }},
 "areaServed": {{ "@type": "City", "name": "Indianapolis", "containedIn": "Marion County, Indiana" }},
 "sameAs": ["https://www.facebook.com/yourrealtylink", "https://www.linkedin.com/company/your-realty-link-llc/"]
 }},
 {{ "@type": "DefinedTerm", "name": {json.dumps(term)}, "description": {json.dumps(p['definition'])}, "inDefinedTermSet": "{SITE}/glossary/" }},
 {{ "@type": "FAQPage", "mainEntity": [
{faq_schema}
 ] }},
 {{ "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Glossary", "item": "{SITE}/glossary/" }},
 {{ "@type": "ListItem", "position": 3, "name": {json.dumps(term)}, "item": "{SITE}/glossary/{slug}/" }}
 ] }}
 ]
 }}
 </script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" rel="stylesheet">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
</head>
<body>

{CANON_HDR}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/glossary/">Glossary</a> <span>&rsaquo;</span> {esc(term)}</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>{p['h1']}</h1>
 <p class="hero-sub">{esc(p['hero_sub'])}</p>
 <div class="hero-badges">
 <span class="hero-badge">📘 Real Estate Term</span>
 <span class="hero-badge">📍 Indiana</span>
 <span class="hero-badge">🔑 Buyers &amp; Sellers</span>
 </div>
 </div>
</section>

<div class="container">
 <div class="content-wrap">
 <main class="content-main">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">{p['qa_lead']}</p>
 <dl class="qa-facts">{qa_facts}</dl>
</div>
<!-- QA-END -->
{sections}

 <div class="info-box">
 <strong>Note:</strong> this is general information for Indiana buyers and sellers, not legal or tax advice. For advice on your specific situation, talk to your attorney, lender, or CPA — or <a href="/contact/">call Daniel Cope at 317-997-7404</a>.
 </div>

 <div class="cta-block">
 <h3>Questions About Your Situation?</h3>
 <p>We'll walk you through it in plain English — no pressure, no obligation.</p>
 <div class="btn-group">
 <a href="/contact/" class="btn btn-white">Contact Your Realty Link →</a>
 <a href="https://yourrealtylink.com/property-search" class="btn btn-outline" target="_blank" rel="noopener">Search Homes</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Frequently Asked Questions — {esc(term)}</h2>
{faqs_html}
 </section>

 </main>

 <aside class="content-sidebar">
 <div class="sidebar-card">
 <div class="sidebar-card-header">Get in Touch</div>
 <div class="sidebar-card-body">
 <p>Have questions? Fill out this quick form and we'll reach out.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="glossary/{slug}">
 <input type="hidden" name="interest_type" value="Glossary — {esc(term)}">
 <label for="sf-name-{sid}">Name *</label>
 <input type="text" id="sf-name-{sid}" name="name" required placeholder="Your name">
 <label for="sf-phone-{sid}">Phone *</label>
 <input type="tel" id="sf-phone-{sid}" name="phone" required placeholder="317-555-1234">
 <label for="sf-email-{sid}">Email *</label>
 <input type="email" id="sf-email-{sid}" name="email" required placeholder="you@example.com">
 <button type="submit">Connect With an Agent →</button>
 <p class="form-note">No spam · No obligation · We respond personally</p>
 </form>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Related Terms</div>
 <div class="sidebar-card-body" style="padding:12px;">
{related}  <a href="/glossary/" class="city-card">Full Glossary <span class="arrow">&rsaquo;</span></a>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Start Here</div>
 <div class="sidebar-card-body">
 <p>New to buying or selling in Central Indiana? Our complete guides walk through the whole process.</p>
 <a href="/guides/buying-a-home-in-indianapolis/" class="btn btn-primary btn-sm btn-full">Buying Guide →</a>
 <a href="/guides/selling-a-home-in-indianapolis/" class="btn btn-outline btn-sm btn-full">Selling Guide</a>
 </div>
 </div>
 </aside>

 </div>
</div>

{CANON_FTR}
{TAIL}</body>
</html>
"""

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "glossary"), exist_ok=True)
    open(os.path.join(ROOT, "glossary", "index.html"), "w", encoding="utf-8").write(index_page())
    built = 0
    for p in FULL_PAGES:
        if p.get("slug") in EXISTING_FULL:
            print(f"  skip {p['slug']} (hand-built)"); continue
        d = os.path.join(ROOT, "glossary", p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(full_page(p))
        built += 1
    print(f"built glossary index ({len(ALL)} terms) + {built} new full pages")
