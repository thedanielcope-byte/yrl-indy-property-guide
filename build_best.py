#!/usr/bin/env python3
"""
build_best.py — data-driven "/best/" list pages in the AI-Overview-winning format.

Reads best-pages.json and writes /best/<slug>/index.html for each entry, matching the
hand-authored /best/ pages exactly: Quick Answer box + qa-facts, "How We Chose These"
methodology, At-a-Glance table, ranked picks, "How to Choose", CTA, FAQ (with FAQPage
schema), and the WebPage/Speakable + LocalBusiness + BreadcrumbList JSON-LD graph.

Pulls the canonical <header>/<footer>/tail + CSS hash from index.html (like glossary.py /
build_press.py). Builds <head> from scratch → run inject_gtag.py afterwards. Rebuilds the
/best/ hub cards + adds sitemap URLs. The 5 original hand-authored /best/ pages are NOT in
best-pages.json, so they are never touched.

Usage: python3 build_best.py
"""
import os, re, json, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://yourrealtylink.com"
UPDATED = datetime.date.today().strftime("%B %Y")

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
CANON_HDR = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
CANON_FTR = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
TAIL = src[src.index('</footer>') + len('</footer>'):src.index('</body>')]
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)

def esc(s): return html.escape(str(s or ""), quote=False)
def plain(s): return re.sub(r'<[^>]+>', '', str(s)).replace("&mdash;", "-").replace("&amp;", "&").replace("&ndash;", "-").replace("&rarr;", "").strip()

def head(r):
    canon = f"{SITE}/best/{r['slug']}/"
    faq_nodes = ",\n".join(
        '{\n "@type": "Question",\n "name": %s,\n "acceptedAnswer": { "@type": "Answer", "text": %s }\n }'
        % (json.dumps(plain(f["q"]), ensure_ascii=False), json.dumps(plain(f["a"]), ensure_ascii=False))
        for f in r["faqs"])
    t, d = esc(r["meta_title"]), esc(r["meta_desc"])
    ogt = esc(r.get("og_title", r["meta_title"]))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{t}</title>
 <meta name="description" content="{d}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{canon}">
 <meta property="og:title" content="{ogt}">
 <meta property="og:description" content="{d}">
 <meta property="og:url" content="{canon}">
 <meta property="og:image" content="{SITE}/assets/img/og-default.png">
 <meta property="og:image:width" content="1200">
 <meta property="og:image:height" content="630">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:title" content="{ogt}">
 <meta name="twitter:description" content="{d}">
 <meta name="twitter:image" content="{SITE}/assets/img/og-default.png">
 <meta property="og:type" content="article">
 <script type="application/ld+json">
 {{
 "@context": "https://schema.org",
 "@graph": [
 {{ "@type": "WebPage", "url": "{canon}", "speakable": {{ "@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"] }} }},
 {{
 "@type": ["LocalBusiness", "RealEstateAgent"],
 "name": "Your Realty Link",
 "url": "https://yourrealtylink.com",
 "logo": "/assets/img/yrl-logo.png",
 "telephone": "317-997-7404",
 "email": "info@yourrealtylink.com",
 "address": {{ "@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US" }},
 "areaServed": {{ "@type": "City", "name": "Indianapolis", "containedIn": "Marion County, Indiana" }},
 "sameAs": ["https://www.facebook.com/yourrealtylink", "https://www.linkedin.com/company/your-realty-link-llc/"]
 }},
 {{
 "@type": "FAQPage",
 "mainEntity": [
{faq_nodes}
 ]
 }},
 {{
 "@type": "BreadcrumbList",
 "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Best Of", "item": "https://yourrealtylink.com/best/" }},
 {{ "@type": "ListItem", "position": 3, "name": "{esc(r['breadcrumb'])}", "item": "{canon}" }}
 ]
 }}
 ]
 }}
 </script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap"></noscript>
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
</head>
<body>
"""

def body(r):
    slug = r["slug"]
    badges = "\n".join(' <span class="hero-badge">%s</span>' % b for b in r["badges"])
    qa_facts = "\n".join(' <div><dt>%s</dt><dd>%s</dd></div>' % (f["label"], f["value"]) for f in r["quick_answer"]["facts"])
    intro = "\n".join(" <p>%s</p>" % p for p in r["intro"])
    hwc = "\n".join(" <p>%s</p>" % p for p in r["how_we_chose"])
    cols = "".join("<th>%s</th>" % c for c in r["at_a_glance"]["cols"])
    rows = "\n".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in row) for row in r["at_a_glance"]["rows"])
    picks = "\n\n".join(
        " <h2>%s</h2>\n <p><strong>Best for:</strong> %s</p>\n%s"
        % (p["h2"], p["best_for"], "\n".join(" <p>%s</p>" % b for b in p["body"]))
        for p in r["picks"])
    faq_items = "\n".join(
        '  <details class="faq-item">\n <summary>%s</summary>\n <div class="faq-answer">\n <p>%s</p>\n </div>\n </details>'
        % (esc(plain(f["q"])), f["a"]) for f in r["faqs"])
    top_links = "\n".join(' <a href="%s" class="city-card">%s <span class="arrow">&rsaquo;</span></a>' % (u, esc(n)) for u, n in r["sidebar"]["top_links"])
    related = "\n".join(' <a href="%s" class="city-card">%s <span class="arrow">&rsaquo;</span></a>' % (u, esc(n)) for u, n in r["sidebar"]["related"])
    return f"""{CANON_HDR}
<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container">
 <a href="/">Home</a>
 <span>&rsaquo;</span>
 <a href="/best/">Best Of</a>
 <span>&rsaquo;</span>
 {esc(r['breadcrumb'])}
 </div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>{r['h1']}</h1>
 <p class="hero-sub">{r['hero_sub']}</p>
 <div class="hero-badges">
{badges}
 </div><p class="hero-reviewed">&#10004; Reviewed by <a href="/agents/janet-giles/">Janet Giles-Schultz</a>, Principal Broker &middot; MIBOR member &middot; Updated {UPDATED}</p>
 </div>
</section>

<div class="container">
 <div class="content-wrap">

 <main class="content-main">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">{r['quick_answer']['lead']}</p>
 <dl class="qa-facts">
{qa_facts}
 </dl>
</div>
<!-- QA-END -->

{intro}
 <h2>How We Chose These</h2>
{hwc}

 <h2>At a Glance</h2>
 <table class="data-table">
 <thead><tr>{cols}</tr></thead>
 <tbody>
{rows}
 </tbody>
 </table>

{picks}

 <h2>How to Choose</h2>
 <p>{r['how_to_choose']}</p>

 <div class="cta-block">
 <h3>{esc(r['cta']['h3'])}</h3>
 <p>{r['cta']['p']}</p>
 <div class="btn-group">
 <a href="/search/" class="btn btn-white" target="_blank" rel="noopener">Search All Listings &rarr;</a>
 <a href="/schedule/" class="btn btn-outline">&#128197; Schedule a Free Consultation</a>
 </div>
 </div>

 <section class="faq-section">
 <h2>Frequently Asked Questions &mdash; {esc(r['faq_heading'])}</h2>

{faq_items}

 </section>

 </main><!-- /content-main -->

 <aside class="content-sidebar">

  <div class="sidebar-card">
 <div class="sidebar-card-header">Get in Touch</div>
 <div class="sidebar-card-body">
 <p>Have questions? Fill out this quick form and we'll reach out.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="best/{slug}">
 <input type="hidden" name="interest_type" value="Buy a Home">
 <label for="sf-name-{slug}">Name *</label>
 <input type="text" id="sf-name-{slug}" name="name" required placeholder="Your name">
 <label for="sf-phone-{slug}">Phone *</label>
 <input type="tel" id="sf-phone-{slug}" name="phone" required placeholder="317-555-1234">
 <label for="sf-email-{slug}">Email *</label>
 <input type="email" id="sf-email-{slug}" name="email" required placeholder="you@example.com">
 <button type="submit">Connect With an Agent &rarr;</button>
 <p class="form-note">No spam &middot; No obligation &middot; We respond personally</p>
 </form>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">{esc(r['sidebar']['top_label'])}</div>
 <div class="sidebar-card-body" style="padding:12px;">
{top_links}
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Search Homes</div>
 <div class="sidebar-card-body">
 <p>Browse every active MIBOR MLS listing across Central Indiana.</p>
 <a href="/search/" class="btn btn-primary btn-sm btn-full" target="_blank" rel="noopener">Search Listings &rarr;</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline btn-sm btn-full">Free Home Valuation</a>
 </div>
 </div>

 <div class="sidebar-card">
 <div class="sidebar-card-header">Related</div>
 <div class="sidebar-card-body" style="padding:12px;">
{related}
 </div>
 </div>

 </aside><!-- /sidebar -->

 </div><!-- /content-wrap -->
</div><!-- /container -->
{CANON_FTR}
{TAIL}</body>
</html>
"""

def hub_card(r):
    return ('  <a href="/best/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
            % (r["slug"], esc(r["hub_card_label"])))

def update_sitemap(urls):
    sp = os.path.join(ROOT, "sitemap.xml")
    sm = open(sp, encoding="utf-8").read()
    today = datetime.date.today().isoformat()
    added = 0
    for u in urls:
        if f"<loc>{u}</loc>" in sm: continue
        sm = sm.replace("</urlset>", f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n</urlset>")
        added += 1
    open(sp, "w", encoding="utf-8").write(sm)
    return added

def main():
    data = json.load(open(os.path.join(ROOT, "best-pages.json"), encoding="utf-8"))
    urls = []
    for r in data:
        d = os.path.join(ROOT, "best", r["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(head(r) + body(r))
        urls.append(f"{SITE}/best/{r['slug']}/")
    added = update_sitemap(urls)
    print(f"best — built {len(data)} page(s); sitemap +{added}")
    print("hub cards to add to best/index.html:")
    for r in data: print(hub_card(r))

if __name__ == "__main__":
    main()
