#!/usr/bin/env python3
"""Generate glossary-cluster blog posts, reusing the canonical blog boilerplate.

Extracts the header, head-assets (fonts+css+inline style), and footer/tail from an
existing blog post so nav/footer/asset-hashes always match the rest of the site.
Each post's prose carries curated inline links to the matching /glossary/ pages.
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "blog", "what-is-my-home-worth-in-indianapolis", "index.html")

src = open(TEMPLATE, encoding="utf-8").read()

def grab(pattern, s, flags=re.DOTALL):
    m = re.search(pattern, s, flags)
    if not m:
        raise SystemExit("Could not extract: " + pattern[:40])
    return m.group(0)

HEAD_ASSETS = grab(r'<link rel="preconnect"[^\n]*googleapis.*?</style>', src)
HEADER      = grab(r'<header class="site-header">.*?</header>', src)
TAIL        = grab(r'<footer class="site-footer">.*\Z', src)

AUTHOR_BOX = '''<div class="author-box">
 <div class="author-avatar">DC</div>
 <div class="author-info">
 <h4><a href="/agents/daniel-cope/">Daniel Cope</a></h4>
 <p class="author-title">Real Estate Broker — Your Realty Link</p>
 <p>Daniel Cope is a full-time Real Estate Broker with Your Realty Link, serving buyers and sellers across Indianapolis and Central Indiana. He works with the team led by Principal Broker Janet Giles-Schultz, a longtime MIBOR member. <a href="https://yourrealtylink.com" target="_blank" rel="noopener">Learn more about Your Realty Link &rarr;</a></p>
 <p style="margin-top:8px;font-size:13px;">&#128222; <a href="tel:3179977404">317-997-7404</a> &nbsp;|&nbsp; &#9993;&#65039; <a href="mailto:info@yourrealtylink.com">info@yourrealtylink.com</a> &nbsp;|&nbsp; <a href="https://yourrealtylink.com" target="_blank" rel="noopener">yourrealtylink.com</a></p>
 </div>
</div>'''

VAL_CARD = '''<div class="sidebar-card">
 <div class="sidebar-card-header">Free Home Valuation</div>
 <div class="sidebar-card-body">
 <p>Find out what your Central Indiana home is worth &mdash; no obligation, no pressure.</p>
 <ul class="contact-list">
 <li><span class="icon">&#128222;</span> <a href="tel:3179977404">317-997-7404</a></li>
 <li><span class="icon">&#9993;&#65039;</span> <a href="mailto:info@yourrealtylink.com">info@yourrealtylink.com</a></li>
 </ul>
 <a href="/services/free-home-valuation/" class="btn btn-primary btn-sm btn-full" target="_blank" rel="noopener">Get My Valuation &rarr;</a>
 </div>
</div>'''

SEARCH_CARD = '''<div class="sidebar-card">
 <div class="sidebar-card-header">Search Indianapolis Homes</div>
 <div class="sidebar-card-body">
 <p>Browse all active MLS listings in Indianapolis and Central Indiana.</p>
 <a href="https://yourrealtylink.com/property-search" class="btn btn-primary btn-sm btn-full" target="_blank" rel="noopener">Search All Listings &rarr;</a>
 </div>
</div>'''

def esc(s):
    return html.escape(str(s), quote=True)

def sections_html(sections):
    out = []
    for sid, h2, paras in sections:
        out.append(f'\n <!-- section -->\n <h2 id="{sid}">{h2}</h2>')
        for p in paras:
            # a "paragraph" is raw HTML (may be <p>..</p>, <ul>..</ul>, etc.)
            out.append(" " + p)
    return "\n".join(out)

def toc_html(toc):
    lis = "\n".join(f' <li><a href="#{i}">{esc(l)}</a></li>' for i, l in toc)
    return f'<div class="toc">\n <h4>In This Article</h4>\n <ol>\n{lis}\n </ol>\n</div>'

def related_posts_html(items):
    lis = "\n".join(f' <li><a href="{h}">{esc(l)}</a></li>' for l, h in items)
    return ('<div class="sidebar-card">\n <div class="sidebar-card-header">Related Posts</div>\n'
            ' <div class="sidebar-card-body">\n <ul class="contact-list">\n' + lis +
            '\n </ul>\n </div>\n</div>')

def related_res_html(items):
    lis = "\n".join(f' <li><a href="{h}">{esc(l)}</a></li>' for l, h in items)
    return '<hr class="divider">\n <h3>Related Resources</h3>\n <ul>\n' + lis + '\n </ul>'

def schema(p):
    crumb = esc(p["schema_headline"])
    url = f'https://janetgiles.com/blog/{p["slug"]}/'
    return f'''<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@graph": [
 {{
 "@type": "Article",
 "headline": "{esc(p['schema_headline'])}",
 "description": "{esc(p['schema_desc'])}",
 "author": {{ "@type": "Person", "name": "Daniel Cope", "url": "https://janetgiles.com/agents/daniel-cope/", "jobTitle": "Real Estate Broker", "worksFor": {{ "@type": "Organization", "name": "Your Realty Link" }} }},
 "publisher": {{ "@type": "Organization", "name": "Your Realty Link", "logo": {{ "@type": "ImageObject", "url": "/assets/img/yrl-logo.png" }} }},
 "datePublished": "{p['date_pub']}",
 "dateModified": "{p['date_mod']}",
 "mainEntityOfPage": "{url}"
 }},
 {{
 "@type": ["LocalBusiness", "RealEstateAgent"],
 "name": "Your Realty Link",
 "url": "https://yourrealtylink.com",
 "telephone": "317-997-7404",
 "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227" }}
 }},
 {{
 "@type": "BreadcrumbList",
 "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://janetgiles.com/blog/" }},
 {{ "@type": "ListItem", "position": 3, "name": "{crumb}", "item": "{url}" }}
 ]
 }}
 ]
}}
</script>'''

def faq_schema(faqs):
    if not faqs:
        return ""
    items = ",\n ".join(
        f'{{ "@type": "Question", "name": "{esc(q)}", "acceptedAnswer": {{ "@type": "Answer", "text": "{esc(a)}" }} }}'
        for q, a in faqs)
    return f'''<script type="application/ld+json">
{{ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
 {items}
] }}
</script>'''

def faq_block(faqs):
    if not faqs:
        return ""
    rows = "\n".join(
        f' <details class="faq-item"><summary>{esc(q)}</summary><div class="faq-answer"><p>{a}</p></div></details>'
        for q, a in faqs)
    return f'\n <!-- FAQ -->\n <h2 id="faq">Frequently Asked Questions</h2>\n{rows}'

def build(p):
    url = f'https://janetgiles.com/blog/{p["slug"]}/'
    og_img = f'https://janetgiles.com/assets/img/blog/{p["slug"]}.png'
    badges = "\n".join(f' <span class="hero-badge">{esc(b)}</span>' for b in p["hero_badges"])
    body_parts = [f' <div class="post-meta">\n'
                  f' <span class="category-badge">{esc(p["category"])}</span>\n'
                  f' <span>{esc(p["date_label"])}</span>\n'
                  f' <span>By Daniel Cope, Real Estate Broker &mdash; Your Realty Link</span>\n'
                  f' <span>~{p["read_min"]} min read</span>\n </div>',
                  "\n <!-- intro -->\n " + p["intro"]]
    body_parts.append(sections_html(p["sections"]))
    if p.get("highlight"):
        q, c = p["highlight"]
        body_parts.append(f'\n <div class="highlight-box">\n <p>{q}</p>\n <cite>&mdash; {esc(c)}</cite>\n </div>')
    body_parts.append(faq_block(p.get("faqs")))
    # CTA
    b1l, b1h = p["cta_btn1"]; b2l, b2h = p["cta_btn2"]
    body_parts.append(
        f'\n <!-- CTA -->\n <div class="cta-block">\n <h3>{esc(p["cta_h3"])}</h3>\n'
        f' <p>{p["cta_p"]}</p>\n <div class="btn-group">\n'
        f' <a href="{b1h}" class="btn btn-white" target="_blank" rel="noopener">{esc(b1l)}</a>\n'
        f' <a href="{b2h}" class="btn btn-outline">{esc(b2l)}</a>\n </div>\n </div>')
    body_parts.append("\n " + related_res_html(p["related_res"]))
    body_parts.append("\n " + AUTHOR_BOX)
    article = '<article class="blog-body">\n' + "\n".join(body_parts) + '\n </article>'

    aside = ('<aside class="blog-sidebar">\n ' + toc_html(p["toc"]) + "\n " + VAL_CARD +
             "\n " + SEARCH_CARD + "\n " + related_posts_html(p["related_posts"]) + '\n </aside>')

    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">

 <!-- YOAST: Focus Keyword: {p["focus_kw"]} | Category: {p["category"]} -->

 <title>{esc(p["seo_title"])}</title>
 <meta name="description" content="{esc(p["meta_desc"])}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">

 <meta property="og:title" content="{esc(p["seo_title"])}">
 <meta property="og:description" content="{esc(p["meta_desc"])}">
 <meta property="og:url" content="{url}">
 <meta property="og:type" content="article">
 <meta property="og:image" content="{og_img}">
 <meta property="og:image:width" content="1200">
 <meta property="og:image:height" content="630">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:image" content="{og_img}">

 <!-- Schema -->
 {schema(p)}
 {faq_schema(p.get("faqs"))}

 {HEAD_ASSETS}
</head>
<body>

<!-- HEADER -->
{HEADER}

<!-- BREADCRUMBS -->
<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container">
 <a href="/">Home</a>
 <span>&rsaquo;</span>
 <a href="/blog/">Blog</a>
 <span>&rsaquo;</span>
 {esc(p["crumb"])}
 </div>
</nav>

<!-- HERO -->
<section class="page-hero">
 <div class="container">
 <h1>{p["h1"]}</h1>
 <p class="hero-sub">{p["hero_sub"]}</p>
 <div class="hero-badges">
{badges}
 </div>
 </div>
</section>

<!-- MAIN -->
<div class="container">
 <div class="blog-wrap">
 {article}
 {aside}
 </div>
</div>

<!-- FOOTER -->
{TAIL}
'''
    return head

# ─────────────────────────────────────────────────────────────────────────────
# CONTENT
# ─────────────────────────────────────────────────────────────────────────────
POSTS = []

# ── POST 1 — Home appraisal prep ──────────────────────────────────────────────
POSTS.append({
 "slug": "what-hurts-a-home-appraisal-in-indiana",
 "focus_kw": "home appraisal indiana",
 "seo_title": "What Hurts a Home Appraisal in Indiana (and How to Prep) | Your Realty Link",
 "meta_desc": "Worried about your home appraisal in Indiana? Learn what lowers an appraisal, how to prepare your home, and what to do if it comes in below your sale price.",
 "category": "Selling a Home",
 "read_min": 8,
 "date_label": "August 2026", "date_pub": "2026-08-03", "date_mod": "2026-08-03",
 "crumb": "What Hurts a Home Appraisal in Indiana",
 "h1": 'What Hurts a Home Appraisal <em>in Indiana</em>',
 "hero_sub": "If you're selling or refinancing in Central Indiana, the appraisal can make or break your deal. Here's what actually moves an appraiser's number — and the simple things you can do ahead of time to help your home appraise for what it's really worth.",
 "hero_badges": ["Selling a Home", "Indianapolis & Central Indiana", "By Daniel Cope"],
 "schema_headline": "What Hurts a Home Appraisal in Indiana (and How to Prepare)",
 "schema_desc": "A practical guide for Indiana sellers on what lowers a home appraisal, how to prepare for the appraiser's visit, and what to do if the appraisal comes in low.",
 "intro": ('<p>Few moments in a home sale create more quiet anxiety than the <a href="/glossary/home-appraisal/">home appraisal</a>. '
   'You’ve accepted a strong offer, you’re picturing the move — and now a licensed stranger walks through with a clipboard and, in effect, gets a vote on whether the deal survives. In Indiana, where a buyer’s lender orders that appraisal to make sure it isn’t lending more than the home is worth, the number the appraiser reaches can hold up a sale, force a price renegotiation, or send everyone back to the table. The good news: appraisals aren’t random. They follow logic you can understand and, to a meaningful degree, prepare for. This guide walks through what actually hurts a <strong>home appraisal in Indiana</strong>, and the practical steps that help yours land where it should.</p>'),
 "sections": [
  ("what-appraisal-is", "What a Home Appraisal Is (and Isn’t)", [
   '<p>An appraisal is an independent, licensed professional’s opinion of your home’s market value, based mostly on what comparable homes nearby have recently <em>sold</em> for. It is ordered by and reported to the buyer’s lender, not the buyer or seller, and the appraiser is required to stay neutral. Their job isn’t to hit the contract price — it’s to protect the lender from over-lending on the collateral.</p>',
   '<p>It helps to know what an appraisal is <em>not</em>. It is not a home inspection — an appraiser notes obvious condition issues but doesn’t crawl the attic or test every outlet the way a <a href="/glossary/home-inspection/">home inspection</a> does. And it is not the same as your agent’s <a href="/glossary/comparative-market-analysis/">comparative market analysis</a>, though the two use similar logic. The CMA sets your list price; the appraisal validates the contract price for the lender.</p>',
  ]),
  ("what-hurts", "What Actually Hurts Your Appraisal", [
   '<p>Most low appraisals trace back to a short list of causes. If you understand them going in, you can address the ones inside your control:</p>',
   '<ul>\n <li><strong>Weak or misleading comps.</strong> Appraisers lean on recent nearby sales. If the closest “comparable” sold as a distressed or estate sale, or if your neighborhood has few recent sales, the value can be dragged down by properties that aren’t truly like yours.</li>\n'
   ' <li><strong>Deferred maintenance.</strong> A worn roof, aging HVAC, water stains, cracked drywall, or peeling paint all signal risk and pull value down — especially for FHA and VA buyers, whose appraisals include minimum property standards.</li>\n'
   ' <li><strong>Dated condition versus the comps.</strong> If similar homes that sold nearby were updated and yours is original, the appraiser adjusts downward. Kitchens and bathrooms carry the most weight.</li>\n'
   ' <li><strong>Over-improvement for the neighborhood.</strong> A $90,000 renovation in a modest area rarely returns dollar-for-dollar — the comps simply won’t support it.</li>\n'
   ' <li><strong>Unpermitted work.</strong> A finished basement or addition done without permits may not count toward square footage or value, and can raise red flags.</li>\n'
   ' <li><strong>A rising market moving faster than the data.</strong> When prices climb quickly, recent closed sales lag today’s reality, and appraisals can trail a hot market.</li>\n </ul>',
  ]),
  ("how-to-prep", "How to Prepare for the Appraiser’s Visit", [
   '<p>You can’t change your comps, but you can make sure your home is presented accurately and in its best light. A little preparation removes doubt and gives the appraiser reasons to support your value.</p>',
   '<ul>\n <li><strong>Make a list of improvements.</strong> Note big-ticket updates with rough dates — new roof, furnace, windows, kitchen remodel, new flooring. Hand it to the appraiser; they can’t credit what they can’t see or verify.</li>\n'
   ' <li><strong>Handle small repairs.</strong> Fix leaky faucets, cracked caulk, sticking doors, and burned-out bulbs. None is huge alone, but together they shape an impression of how the home was maintained.</li>\n'
   ' <li><strong>Clean and declutter.</strong> A clean, accessible home is easier to measure and photograph, and simply reads as better cared-for.</li>\n'
   ' <li><strong>Ensure access.</strong> Clear paths to the attic, crawl space, electrical panel, and mechanicals so the appraiser can see everything without guessing.</li>\n'
   ' <li><strong>Let your agent share comps.</strong> A good listing agent provides the appraiser with strong, genuinely comparable recent sales that support the contract price.</li>\n </ul>',
  ]),
  ("low-appraisal", "What Happens If It Comes In Low", [
   '<p>Sometimes, despite everything, the appraisal lands below the agreed price. The gap between the appraised value and the contract price is called an <a href="/glossary/appraisal-gap/">appraisal gap</a>, and in Indiana you generally have a few paths forward.</p>',
   '<p>The buyer can bring extra cash to cover the difference, since the lender will only finance up to the appraised value. The seller can lower the price to meet the appraisal. The two sides can meet in the middle. Or, if the appraisal contains factual errors — wrong square footage, missed updates, poor comps — your agent can file a rebuttal (a “reconsideration of value”) with supporting evidence. Whether a buyer even has the right to walk away depends on the offer: a financing or appraisal contingency protects them, while a waived contingency does not.</p>',
   '<p>This is exactly where an experienced local agent earns their keep. Renegotiating a low appraisal calmly, with data instead of emotion, is often the difference between a deal that closes and one that collapses.</p>',
  ]),
  ("price-right", "The Best Defense: Price It Right From Day One", [
   '<p>The single most effective way to avoid appraisal trouble is to price your home correctly at the start, grounded in the same kind of recent, genuinely comparable sales an appraiser will use. Homes priced ahead of the data are the ones that most often run into appraisal gaps.</p>',
   '<p>At Your Realty Link, our <a href="/services/free-home-valuation/">free home valuation</a> is built on real neighborhood sales, not an algorithm — and our <a href="/services/pricing-your-home/">pricing consultation</a> helps you set a number that will both attract strong offers and stand up when the appraiser arrives.</p>',
  ]),
 ],
 "highlight": ("“An appraisal isn’t something to fear — it’s something to prepare for. When a home is priced on real comps and presented honestly, the number usually takes care of itself. It’s the surprises that hurt, and most surprises are preventable.”",
               "Daniel Cope, Real Estate Broker, Your Realty Link"),
 "faqs": [
  ("How long does a home appraisal take in Indiana?", "The on-site visit is usually 30 minutes to an hour depending on the home's size, and the written report typically comes back to the lender within a few days to about a week."),
  ("Who pays for the appraisal, the buyer or the seller?", "In a typical Indiana purchase the buyer pays for the appraisal as part of their closing costs, because the buyer's lender orders it. In a refinance, the homeowner pays."),
  ("Can I be present during the appraisal?", "Usually yes, though it isn't required. Many sellers simply leave a written list of improvements and recent updates for the appraiser instead of hovering during the visit."),
  ("What if the appraisal comes in higher than my sale price?", "That's good news for the buyer — they're buying at a price below market value and gaining instant equity. The sale price doesn't automatically rise; the contract price stands."),
 ],
 "cta_h3": "Price It Right — and Sell With Confidence",
 "cta_p": "Get a free, no-obligation home valuation from Your Realty Link built on real Central Indiana sales, so your home is priced to attract offers and hold up at appraisal.",
 "cta_btn1": ("Get My Free Valuation →", "/services/free-home-valuation/"),
 "cta_btn2": ("Talk to Daniel", "/contact/"),
 "related_res": [
  ("Home Appraisal — Glossary", "/glossary/home-appraisal/"),
  ("Appraisal Gap — Glossary", "/glossary/appraisal-gap/"),
  ("Free Home Valuation", "/services/free-home-valuation/"),
  ("How to Price Your Home in Indianapolis", "/services/pricing-your-home/"),
 ],
 "toc": [
  ("what-appraisal-is", "What an Appraisal Is"),
  ("what-hurts", "What Hurts Your Appraisal"),
  ("how-to-prep", "How to Prepare"),
  ("low-appraisal", "If It Comes In Low"),
  ("price-right", "Price It Right"),
  ("faq", "FAQ"),
 ],
 "related_posts": [
  ("What Is My Home Worth in Indianapolis?", "/blog/what-is-my-home-worth-in-indianapolis/"),
  ("Top 5 Things That Kill a Home Sale", "/blog/top-5-things-that-kill-a-home-sale-in-indianapolis/"),
  ("Home Staging Tips for Indianapolis Sellers", "/blog/home-staging-tips-for-indianapolis-sellers/"),
 ],
})

# ── POST 2 — Indiana homestead exemption ──────────────────────────────────────
POSTS.append({
 "slug": "indiana-homestead-exemption-lower-property-taxes",
 "focus_kw": "indiana homestead exemption",
 "seo_title": "Indiana Homestead Exemption: Lower Your Property Tax | Your Realty Link",
 "meta_desc": "The Indiana homestead exemption can significantly lower the property tax on your primary residence. Learn who qualifies, how to file, and how it helps buyers.",
 "category": "Buying a Home",
 "read_min": 7,
 "date_label": "August 2026", "date_pub": "2026-08-03", "date_mod": "2026-08-03",
 "crumb": "Indiana Homestead Exemption",
 "h1": 'The Indiana Homestead Exemption, <em>Explained</em>',
 "hero_sub": "If you own and live in your home in Indiana, the homestead deduction is one of the easiest ways to lower your property tax bill — but only if you file for it. Here's who qualifies, what it does, and how to make sure you're not leaving money on the table.",
 "hero_badges": ["Buying a Home", "Indiana Homeowners", "By Daniel Cope"],
 "schema_headline": "The Indiana Homestead Exemption, Explained",
 "schema_desc": "A homeowner's guide to the Indiana homestead deduction — who qualifies, how it lowers your property taxes and ties into the property tax caps, and how to file with your county auditor.",
 "intro": ('<p>When you buy a home in Indiana, one of the most valuable pieces of paperwork has nothing to do with your mortgage — it’s the homestead deduction. Often called the <strong>Indiana homestead exemption</strong>, it lowers the taxable value of your primary residence and, just as importantly, unlocks the most favorable property-tax cap the state offers. Yet every year, buyers move in and simply forget to file for it, quietly overpaying on their tax bill. This guide explains what the <a href="/glossary/homestead-exemption/">homestead exemption</a> actually does, who qualifies, how it connects to Indiana’s <a href="/glossary/property-tax-caps/">property tax caps</a>, and the simple step you need to take to claim it.</p>'),
 "sections": [
  ("what-it-is", "What the Homestead Exemption Actually Does", [
   '<p>Indiana property taxes are based on the assessed value of your home. The homestead deduction reduces the portion of that assessed value the county can tax on your <em>primary residence</em> — the home you own and actually live in. A qualifying homestead receives a standard deduction plus a supplemental deduction, and together they can take a meaningful bite out of your taxable value before the rate is ever applied.</p>',
   '<p>Because the exact deduction amounts and rules are set by state law and have been adjusted by the legislature in recent years, it’s best to confirm the current figures with your county auditor or the Indiana Department of Local Government Finance (DLGF) rather than relying on an old number. The principle, however, is stable: claiming your homestead lowers what you’re taxed on, year after year, for as long as it’s your primary home.</p>',
  ]),
  ("tax-caps", "The Bigger Benefit: The 1% Tax Cap", [
   '<p>The deduction is only half the story. Under Indiana’s constitutional property tax caps — often called the “circuit breaker” — your annual property tax bill is capped as a percentage of your home’s gross assessed value. A qualifying homestead (owner-occupied primary residence) receives the lowest cap tier the state allows, while non-homestead residential property, such as a rental or second home, is capped at a higher percentage.</p>',
   '<p>That difference is exactly why filing your homestead matters so much: it doesn’t just shrink your taxable value, it also qualifies you for the most protective cap. Two identical houses on the same street can carry very different tax bills purely because one owner filed for the homestead and the other didn’t. If you want the full picture of how those caps work by property type, our <a href="/glossary/property-tax-caps/">property tax caps</a> explainer breaks it down.</p>',
  ]),
  ("who-qualifies", "Who Qualifies", [
   '<p>The homestead deduction is for property you both <strong>own</strong> (or are buying under a recorded contract) and <strong>occupy as your primary residence</strong> as of the relevant assessment date. You can only claim the homestead on one property — your main home — not on a vacation home, a rental, or an investment property.</p>',
   '<p>Indiana also offers additional deductions that can stack with the homestead for those who qualify, including deductions for homeowners age 65 and older (subject to income and assessed-value limits), disabled veterans, and the blind or disabled. These have their own eligibility rules and applications, so it’s worth asking your county auditor which ones apply to your situation.</p>',
  ]),
  ("how-to-file", "How to File for Your Homestead Deduction", [
   '<p>Filing is straightforward, and in many Indiana counties it now happens right at closing. Here’s what to know:</p>',
   '<ul>\n <li><strong>Where:</strong> You file with the <em>county auditor</em> in the county where the home is located. Many counties let you file online; others use a paper form (the state’s homestead form).</li>\n'
   ' <li><strong>At closing:</strong> In a lot of Indiana transactions, the title company includes a homestead application with your closing paperwork — but confirm it was actually submitted. Don’t assume.</li>\n'
   ' <li><strong>You file once:</strong> Once approved, the homestead generally stays in place year to year as long as you own and occupy the home and your situation doesn’t change. You don’t re-file annually.</li>\n'
   ' <li><strong>Tell the auditor about changes:</strong> If you move, convert the home to a rental, or the ownership changes, you’re required to notify the auditor so the deduction can be removed.</li>\n </ul>',
   '<p>Deadlines matter: the deduction applies to the following year’s tax bill only if you file by the state’s cutoff, so file promptly after you close rather than waiting.</p>',
  ]),
  ("buyers-sellers", "Why It Matters for Buyers and Sellers", [
   '<p>For buyers, the takeaway is simple: filing your homestead is one of the highest-return five minutes of paperwork in the whole transaction. Confirm it was submitted, and follow up with the county auditor if you’re unsure.</p>',
   '<p>For sellers, it’s worth remembering that the tax figure a buyer sees on a listing may reflect <em>your</em> deductions, not what the new owner will pay — and a home that has been a rental may show a higher, non-homestead tax bill that a new owner-occupant can improve by filing. When we prepare a <a href="/services/free-home-valuation/">home valuation</a>, we help sellers present taxes accurately so buyers understand the real picture.</p>',
  ]),
 ],
 "highlight": ("“The homestead deduction is the closest thing to free money in a home purchase, and I still meet owners who never filed it. If you take one action after closing, make it this one — then double-check the auditor actually has it on file.”",
               "Daniel Cope, Real Estate Broker, Your Realty Link"),
 "faqs": [
  ("Do I have to re-file for the homestead exemption every year?", "No. Once your homestead deduction is approved, it generally carries over year to year as long as you continue to own and live in the home as your primary residence. You must notify the county auditor if that changes."),
  ("Can I claim the homestead exemption on a rental or second home?", "No. The homestead deduction applies only to your primary residence — the home you own and actually live in. Rentals, vacation homes, and investment properties don't qualify and fall under a higher property tax cap."),
  ("Where do I file for the Indiana homestead deduction?", "You file with the county auditor in the county where the home is located. Many counties offer online filing, and in a lot of transactions the title company submits the application at closing — but always confirm it went through."),
  ("How much does the homestead exemption save?", "It varies by home value, local tax rate, and current state law, which has changed in recent years. The deduction lowers your taxable value and also qualifies your home for the lowest property tax cap, so confirm current figures with your county auditor or the Indiana DLGF."),
 ],
 "cta_h3": "Thinking About Buying or Selling in Central Indiana?",
 "cta_p": "Your Realty Link helps buyers and sellers understand the full cost of ownership — taxes included. Reach out for straight answers and a free, no-pressure consultation.",
 "cta_btn1": ("Talk to Your Realty Link →", "/contact/"),
 "cta_btn2": ("Get a Free Home Valuation", "/services/free-home-valuation/"),
 "related_res": [
  ("Homestead Exemption — Glossary", "/glossary/homestead-exemption/"),
  ("Property Tax Caps — Glossary", "/glossary/property-tax-caps/"),
  ("First Time Home Buyers", "/services/first-time-home-buyers/"),
  ("Free Home Valuation", "/services/free-home-valuation/"),
 ],
 "toc": [
  ("what-it-is", "What It Does"),
  ("tax-caps", "The 1% Tax Cap"),
  ("who-qualifies", "Who Qualifies"),
  ("how-to-file", "How to File"),
  ("buyers-sellers", "Buyers & Sellers"),
  ("faq", "FAQ"),
 ],
 "related_posts": [
  ("First Time Home Buyer Guide — Indianapolis", "/blog/first-time-home-buyer-guide-indianapolis-2026/"),
  ("Closing Costs in Indiana — Sellers", "/blog/closing-costs-in-indiana-what-sellers-need-to-know/"),
  ("Rent vs Buy in Indianapolis 2026", "/blog/rent-vs-buy-in-indianapolis-2026-comparison/"),
 ],
})

# ── POST 3 — CMA vs Zestimate ─────────────────────────────────────────────────
POSTS.append({
 "slug": "cma-vs-zestimate-indianapolis",
 "focus_kw": "comparative market analysis indianapolis",
 "seo_title": "CMA vs Zestimate: Pricing a Home in Indianapolis | Your Realty Link",
 "meta_desc": "A comparative market analysis (CMA) beats a Zestimate for pricing an Indianapolis home. Learn how a CMA is built, why online estimates miss, and how to get one free.",
 "category": "Selling a Home",
 "read_min": 8,
 "date_label": "August 2026", "date_pub": "2026-08-03", "date_mod": "2026-08-03",
 "crumb": "CMA vs Zestimate in Indianapolis",
 "h1": 'CMA vs. Zestimate: <em>Pricing a Home in Indianapolis</em>',
 "hero_sub": "An online estimate is a fine place to start daydreaming — and a terrible place to set your list price. Here's how a real comparative market analysis is built, why automated estimates miss in a market as varied as Indianapolis, and how the two differ from a formal appraisal.",
 "hero_badges": ["Selling a Home", "Indianapolis & Central Indiana", "By Daniel Cope"],
 "schema_headline": "CMA vs Zestimate: How to Price a Home in Indianapolis",
 "schema_desc": "How a comparative market analysis (CMA) is built, why automated home-value estimates like the Zestimate miss the mark in Indianapolis, and how a CMA differs from an appraisal.",
 "intro": ('<p>Almost everyone starts in the same place: you type your address into a real-estate site and watch a confident number appear. It’s fun, it’s instant, and it feels authoritative. The problem comes when that number becomes the basis for a list price. In a market as varied as Indianapolis — where a beautifully renovated home and an untouched 1985 original can look identical in public records — automated estimates routinely miss by tens of thousands of dollars. The tool professionals actually use is a <a href="/glossary/comparative-market-analysis/">comparative market analysis</a>, or CMA. This guide explains how a CMA is built, why the <strong>Zestimate and other automated estimates fall short in Indianapolis</strong>, and how both differ from a formal appraisal.</p>'),
 "sections": [
  ("what-cma", "What a CMA Is", [
   '<p>A comparative market analysis is a structured estimate of your home’s market value based on what genuinely comparable homes have recently <em>sold</em> for near you. The emphasis is on <em>sold</em> — not listed, not hoped-for, but contracted and closed. It’s the same fundamental logic a lender’s appraiser uses, applied by your agent to set a smart list price.</p>',
   '<p>A good CMA doesn’t just average nearby sales. It selects homes that are truly similar — comparable square footage, bedroom and bath count, age, lot size, and location — and then makes line-item adjustments for the differences. A comparable with a finished basement yours lacks gets adjusted down; your three-car garage the comps don’t have gets adjusted up. The result is a value range grounded in your specific market, not a metro-wide guess.</p>',
  ]),
  ("how-built", "How a CMA Is Built", [
   '<p>When we prepare a CMA at Your Realty Link, the work runs through a few clear steps:</p>',
   '<ul>\n <li><strong>Pull the right comps.</strong> Recent sold homes — typically the last few months — in your neighborhood or a directly comparable one, filtered to properties genuinely like yours.</li>\n'
   ' <li><strong>Adjust for differences.</strong> Square footage, condition, updates, garage, basement, lot, and location are each accounted for so you’re comparing apples to apples.</li>\n'
   ' <li><strong>Read current conditions.</strong> How fast are homes selling? A market’s <a href="/glossary/days-on-market/">days on market</a> and the number of competing active listings tell us how aggressively to price.</li>\n'
   ' <li><strong>Factor in your actual home.</strong> A walkthrough (or detailed conversation) captures the updates and character that never show up in public data — the exact thing algorithms can’t see.</li>\n </ul>',
  ]),
  ("why-zestimate-misses", "Why the Zestimate Misses in Indianapolis", [
   '<p>Automated valuation models — the Zestimate and its cousins — estimate value by running public records data through a statistical model. That works better in cookie-cutter subdivisions where homes are nearly identical. It works poorly across Indianapolis, where condition and updates vary enormously from house to house and street to street.</p>',
   '<p>The core weakness is simple: public data is often incomplete, lagged, or wrong. A home gut-renovated three years ago — new kitchen, baths, mechanicals — looks the same in the record as the untouched house next door. The model can’t see the granite, the new roof, or the finished basement done without a permit. It also can’t tell that the low nearby “comp” was actually an estate sale. That’s how estimates end up off by tens of thousands — and why pricing off one leads sellers to either leave money on the table or overprice and stall.</p>',
  ]),
  ("cma-vs-appraisal", "CMA vs. Appraisal vs. Zestimate", [
   '<p>These three get blurred together, but each has a distinct job:</p>',
   '<ul>\n <li><strong>Zestimate / AVM:</strong> An instant, algorithm-driven estimate from public data. Useful as a rough starting point; not reliable for pricing.</li>\n'
   ' <li><strong>CMA:</strong> Your agent’s human analysis of real comparable sales, adjusted for your specific home, used to set the list price. Free, and far more accurate for your property.</li>\n'
   ' <li><strong>Appraisal:</strong> A licensed appraiser’s formal opinion of value, ordered by the buyer’s lender to protect the loan. It uses similar comp logic but is independent and comes with a fee. Our <a href="/glossary/home-appraisal/">home appraisal</a> explainer covers this step in depth.</li>\n </ul>',
   '<p>The smart sequence is: glance at the automated estimate for context, price off a real CMA, then present the home well so it appraises cleanly for the buyer’s lender.</p>',
  ]),
  ("get-cma", "Get a Free CMA for Your Home", [
   '<p>If you want to know what your Indianapolis-area home is actually worth today, a CMA is the honest answer — and ours is free with no obligation, whether you’re selling next month or just keeping an eye on your equity.</p>',
   '<p>Our <a href="/services/free-home-valuation/">free home valuation</a> pairs real neighborhood sales with a look at your specific home, and for sellers ready to go deeper, our <a href="/services/pricing-your-home/">pricing consultation</a> turns that value into a listing strategy. For more on how value gets determined overall, see <a href="/blog/what-is-my-home-worth-in-indianapolis/">What Is My Home Worth in Indianapolis?</a></p>',
  ]),
 ],
 "highlight": ("“A Zestimate is a conversation starter, not a price. The number that matters is the one built from real, recent sales of homes like yours — adjusted for the things a computer can’t see from a desk.”",
               "Daniel Cope, Real Estate Broker, Your Realty Link"),
 "faqs": [
  ("Is a CMA the same as an appraisal?", "No. A CMA is your agent's analysis of comparable sales used to set a list price, and it's free. An appraisal is a licensed appraiser's independent, fee-based opinion of value ordered by the buyer's lender. They use similar logic but serve different purposes."),
  ("How much does a comparative market analysis cost?", "At Your Realty Link a CMA is free and comes with no obligation, whether you're planning to sell soon or simply want to understand your home's current value."),
  ("Why is the Zestimate on my home wrong?", "Automated estimates rely on public records that are often incomplete or outdated. They can't see interior updates, renovation quality, or why a nearby home sold low, so in a varied market like Indianapolis they can be off by tens of thousands of dollars."),
  ("How accurate is a CMA?", "A well-prepared CMA is far more accurate than an automated estimate because it uses genuinely comparable recent sales and accounts for your home's specific condition and updates. It's the same comp-based logic an appraiser uses to value your property."),
 ],
 "cta_h3": "Find Out What Your Home Is Really Worth",
 "cta_p": "Skip the algorithm. Get a free, no-obligation CMA from Your Realty Link — built on real Central Indiana sales and an honest read of your specific home.",
 "cta_btn1": ("Get My Free CMA →", "/services/free-home-valuation/"),
 "cta_btn2": ("Talk to Daniel", "/contact/"),
 "related_res": [
  ("Comparative Market Analysis — Glossary", "/glossary/comparative-market-analysis/"),
  ("Home Appraisal — Glossary", "/glossary/home-appraisal/"),
  ("Free Home Valuation", "/services/free-home-valuation/"),
  ("What Is My Home Worth in Indianapolis?", "/blog/what-is-my-home-worth-in-indianapolis/"),
 ],
 "toc": [
  ("what-cma", "What a CMA Is"),
  ("how-built", "How a CMA Is Built"),
  ("why-zestimate-misses", "Why the Zestimate Misses"),
  ("cma-vs-appraisal", "CMA vs Appraisal"),
  ("get-cma", "Get a Free CMA"),
  ("faq", "FAQ"),
 ],
 "related_posts": [
  ("What Is My Home Worth in Indianapolis?", "/blog/what-is-my-home-worth-in-indianapolis/"),
  ("Top 5 Things That Kill a Home Sale", "/blog/top-5-things-that-kill-a-home-sale-in-indianapolis/"),
  ("Indianapolis Market Update 2026", "/blog/indianapolis-real-estate-market-update-2026/"),
 ],
})

# ─────────────────────────────────────────────────────────────────────────────
# The 3 dicts above are the ORIGINAL live posts and are NOT regenerated (they now
# carry site-wide auto-links). New posts are authored in blog-posts-new.json and
# written here. HTML attribute quotes are normalized single -> double.
import json

def normalize(htmlout):
    return re.sub(r"href='([^']*)'", r'href="\1"', htmlout)

new_path = os.path.join(ROOT, "blog-posts-new.json")
NEWPOSTS = json.load(open(new_path, encoding="utf-8")) if os.path.exists(new_path) else []

written = []
for p in NEWPOSTS:
    d = os.path.join(ROOT, "blog", p["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(normalize(build(p)))
    written.append(p["slug"])

print("Wrote", len(written), "NEW posts (3 original posts left untouched):")
for s in written:
    print("  /blog/%s/" % s)
