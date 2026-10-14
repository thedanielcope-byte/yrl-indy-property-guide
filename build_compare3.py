#!/usr/bin/env python3
"""Build /compare/greenwood-vs-franklin-vs-zionsville/ from the greenwood-vs-franklin page shell.

GSC (Sep 2026): "what is the better town greenwood, franklin or zionsville" = 720 impressions at
position 7.4 with 0 clicks, and no page answered the three-way question. Prices/schools/commutes
match city_guides_data.py and the city pages; tax rates are Indiana DOR county rates (Boone rose to
1.71% on Oct 1 2026). Re-runnable. Not picked up by inject_compare_links.py (3-way slug), so the
hub card and city-page links are added here.
"""
import html, json, os, re

SRC = "compare/greenwood-vs-franklin/index.html"
SLUG = "greenwood-vs-franklin-vs-zionsville"
URL = f"https://yourrealtylink.com/compare/{SLUG}/"
TITLE = "Greenwood vs Franklin vs Zionsville: Which Is Better? | Your Realty Link"
DESC = ("Greenwood, Franklin or Zionsville? Compare home prices, schools, commute and small-town feel "
        "to choose the right town near Indianapolis.")
G = "/cities/johnson-county/greenwood-indiana-real-estate/"
F = "/cities/johnson-county/franklin-indiana-real-estate/"
Z = "/cities/boone-county/zionsville-indiana-real-estate/"

FAQS = [
 ("Which is better: Greenwood, Franklin or Zionsville?",
  "It depends on your budget and where you work. Greenwood has the shortest commute (about 15 minutes to downtown) and the most shopping, with homes from the $250s to the $450s. Franklin is the small-town, courthouse-square pick from the $200s to the $400s, with a longer drive. Zionsville offers top-rated schools and a brick-street village, but prices start in the mid-$400s."),
 ("Which of the three is the most affordable?",
  "Franklin, with homes typically from the $200s to the $400s, followed closely by Greenwood ($250s to $450s). Zionsville is the premium option, typically from the mid-$400s to over $1 million."),
 ("Which has the shortest commute to downtown Indianapolis?",
  "Greenwood, at about 15 minutes via I-65 or US-31. Zionsville is about 25 minutes via I-65 and Michigan Road, and Franklin about 30 minutes via I-65 or US-31."),
 ("Do property taxes differ between the three?",
  "All three get Indiana's 1% homestead property tax cap. The bigger difference is local income tax: Johnson County (Greenwood and Franklin) is 1.40%, while Boone County (Zionsville) rose to 1.71% on October 1, 2026."),
]

MAIN = f"""<main class="content-main">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">It depends on your budget and where you work. <strong>Greenwood</strong> has the shortest commute (about 15 minutes to downtown) and the most shopping, with homes from the $250s to the $450s. <strong>Franklin</strong> is the small-town, courthouse-square pick from the $200s to the $400s, with a longer drive. <strong>Zionsville</strong> offers top-rated schools and a brick-street village, but prices start in the mid-$400s.</p>
 <dl class="qa-facts">
 <div><dt>Greenwood prices</dt><dd>$250s &ndash; $450s</dd></div>
 <div><dt>Franklin prices</dt><dd>$200s &ndash; $400s</dd></div>
 <div><dt>Zionsville prices</dt><dd>Mid-$400s &ndash; $1M+</dd></div>
 <div><dt>Commute</dt><dd>Greenwood ~15 min · Zionsville ~25 · Franklin ~30</dd></div>
 </dl>
</div>
<!-- QA-END -->

 <p>Greenwood, Franklin and Zionsville come up together more often than you&rsquo;d expect, even though they sit on opposite sides of Indianapolis. All three offer something buyers want from a town near the city &mdash; convenience, character or top schools &mdash; but they deliver it at very different price points. Here&rsquo;s how they compare, using the same ranges our team uses on each town&rsquo;s page.</p>

 <h2>At a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <tr><th></th><th>Greenwood</th><th>Franklin</th><th>Zionsville</th></tr>
 <tr><td><strong>Typical prices</strong></td><td>$250s &ndash; $450s</td><td>$200s &ndash; $400s</td><td>Mid-$400s &ndash; $1M+</td></tr>
 <tr><td><strong>Schools</strong></td><td>Center Grove or Greenwood Community (Clark-Pleasant in parts)</td><td>Franklin Community Schools</td><td>Zionsville Community Schools</td></tr>
 <tr><td><strong>Commute to downtown</strong></td><td>~15 min (I-65 / US-31)</td><td>~30 min (I-65 / US-31)</td><td>~25 min (I-65 / Michigan Rd)</td></tr>
 <tr><td><strong>Character</strong></td><td>South-metro shopping and dining hub with a revitalized Old Town</td><td>Johnson County seat: courthouse square, Artcraft Theatre, Franklin College</td><td>Brick-street Village, boutiques, wooded lots</td></tr>
 <tr><td><strong>Local income tax</strong></td><td>1.40% (Johnson County)</td><td>1.40% (Johnson County)</td><td>1.71% (Boone County)</td></tr>
 <tr><td><strong>Best for</strong></td><td>Commuters who want value plus convenience</td><td>Budget buyers who want a small-town, college-town feel</td><td>Buyers who put schools and upscale small-town living first</td></tr>
 <tr><td><strong>Biggest tradeoff</strong></td><td>Busy roads; school district varies by address</td><td>Longer commute; fewer new builds</td><td>Price</td></tr>
 </table>
 </div>

 <h2>Location and Commute</h2>
 <p>Start with the map. <a href="{G}">Greenwood</a> and <a href="{F}">Franklin</a> sit about 15 minutes apart on the south side along I-65, while <a href="{Z}">Zionsville</a> is on the northwest side in Boone County. If your job is downtown or on the south side, Greenwood wins on drive time. If you work on the north or northwest side, Zionsville&rsquo;s I-65 and Michigan Road access makes more sense. Franklin asks the most of a daily downtown commuter, at about 30 minutes.</p>

 <h2>Price: What Your Budget Buys</h2>
 <p>Greenwood and Franklin overlap from the $250s into the $400s, so you can compare like-for-like homes, and Franklin reaches down into the $200s. Zionsville typically starts in the mid-$400s and climbs past $1 million, so a budget under that line will feel tight there. Our agents can pull recent sales in all three towns so you can compare real numbers for the kind of home you want.</p>

 <h2>Schools</h2>
 <p>Zionsville Community Schools are among the state&rsquo;s top-rated, and that&rsquo;s a big part of Zionsville&rsquo;s price. Greenwood spans more than one district &mdash; parts of the city are in the sought-after <a href="/neighborhoods/center-grove-indiana/">Center Grove</a> district, others in Greenwood Community or Clark-Pleasant &mdash; so confirm boundaries by address. Franklin is served by Franklin Community Schools.</p>

 <h2>Small-Town Feel</h2>
 <p>Each town reads &ldquo;small town&rdquo; differently. Greenwood gives you the most shopping and dining plus a revitalized Old Town. Franklin offers a true county-seat square, the Artcraft Theatre and a college-town rhythm. Zionsville pairs a brick-street Village with larger, often wooded lots.</p>

 <h2>How to Choose</h2>
 <ul>
 <li><strong>Choose Greenwood</strong> if a short commute and everyday convenience matter most.</li>
 <li><strong>Choose Franklin</strong> if you want the most house for the money and a genuine small-town square, and the longer drive works for you.</li>
 <li><strong>Choose Zionsville</strong> if schools and a village setting come first and your budget starts in the mid-$400s.</li>
 </ul>
 <p>Before you decide, check the details that are easy to miss: confirm school boundaries by address, factor in county income tax (1.40% in Johnson County versus 1.71% in Boone County), and drive each commute at rush hour. Each town&rsquo;s page has an honest pros-and-cons rundown: <a href="{G}#pros-cons">Greenwood</a>, <a href="{F}#pros-cons">Franklin</a> and <a href="{Z}#pros-cons">Zionsville</a>.</p>

 <div class="cta-block">
 <h3>Tour All Three Before You Decide</h3>
 <p>Our team works across Johnson and Boone counties. We&rsquo;ll set up showings in each town and pull the recent sales that matter for your budget.</p>
 <div class="btn-group">
 <a href="/search/" class="btn btn-white">Search Homes →</a>
 <a href="/schedule/buyer-consultation/" class="btn btn-outline">📅 Book a Buyer Consultation</a>
 </div>
 </div>

 <!-- FAQ -->
 <section class="faq-section">
 <h2>Frequently Asked Questions &mdash; Greenwood vs Franklin vs Zionsville</h2>
__FAQ__
 </section>

 <p style="font-size:.85rem;color:var(--gray);">Sources: price ranges and commutes from our town pages; county income tax rates from the <a href="https://www.in.gov/dor/files/dn01.pdf" target="_blank" rel="noopener">Indiana Department of Revenue</a> (Boone County&rsquo;s October 2026 change per the <a href="https://payroll.org/news-resources/news/news-detail/2026/09/30/one-indiana-county-has-tax-rate-change-effective-october-1" target="_blank" rel="noopener">American Payroll Association</a>).</p>

<!-- RELATED-COMPARES -->
<section class="related-compares">
<h2>More Central Indiana Comparisons</h2>
<div class="compare-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:12px">
 <a href="/compare/greenwood-vs-franklin/" class="city-card">Greenwood vs Franklin <span class="arrow">›</span></a>
 <a href="/compare/zionsville-vs-carmel/" class="city-card">Zionsville vs Carmel <span class="arrow">›</span></a>
 <a href="/compare/zionsville-vs-whitestown/" class="city-card">Zionsville vs Whitestown <span class="arrow">›</span></a>
 <a href="/compare/franklin-vs-bargersville/" class="city-card">Franklin vs Bargersville <span class="arrow">›</span></a>
 <a href="/best/indianapolis-suburbs-for-families/" class="city-card">Best Suburbs for Families <span class="arrow">›</span></a>
 <a href="/compare/" class="city-card">All Comparisons <span class="arrow">›</span></a>
</div>
</section>
</main>"""


def main():
    s = open(SRC, encoding="utf-8").read()
    t = html.escape(TITLE, quote=False)
    s = re.sub(r"<title>.*?</title>", f"<title>{t}</title>", s, count=1)
    for prop, val in (("og:title", t), ("og:description", DESC), ("og:url", URL)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", DESC), ("twitter:title", t), ("twitter:description", DESC)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "url": URL, "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"]}},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com",
         "logo": "/assets/img/yrl-logo.png", "telephone": "317-997-7404", "email": "indy@yourrealtylink.com",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis",
                     "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US"},
         "areaServed": "Indianapolis, Indiana and Central Indiana"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://yourrealtylink.com/compare/"},
            {"@type": "ListItem", "position": 3, "name": "Greenwood vs Franklin vs Zionsville", "item": URL}]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n </script>', s, count=1, flags=re.S)
    s = s.replace(" Greenwood vs Franklin\n </div>\n</nav>", " Greenwood vs Franklin vs Zionsville\n </div>\n</nav>", 1)
    s = re.sub(r"<h1>.*?</h1>", "<h1>Greenwood vs Franklin vs Zionsville: <em>Which Is Better?</em></h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) +
               "Three towns buyers often weigh together &mdash; a south-side retail hub, a historic county seat and a premium northwest village &mdash; compared on price, schools, commute and feel." + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<div class="hero-badges">.*?</div>', '<div class="hero-badges">\n <span class="hero-badge">📍 Johnson &amp; Boone Counties</span>\n'
               ' <span class="hero-badge">🏡 $200s – $1M+</span>\n <span class="hero-badge">🎓 Three School Districts</span>\n </div>', s, count=1, flags=re.S)
    s = s.replace("Updated September 2026</p>", "Updated October 2026</p>", 1)
    faq = "\n".join(f' <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in FAQS)
    s = re.sub(r'<main class="content-main">.*?</main>', lambda m: MAIN.replace("__FAQ__", faq), s, count=1, flags=re.S)
    s = s.replace("compare-greenwood-vs-franklin", f"compare-{SLUG}").replace('value="compare/greenwood-vs-franklin"', f'value="compare/{SLUG}"')
    s = s.replace(f'<a href="{F}" class="city-card"><h3>Franklin</h3><span class="cprice">$200s – $400s</span><span class="arrow">›</span></a>',
                  f'<a href="{F}" class="city-card"><h3>Franklin</h3><span class="cprice">$200s – $400s</span><span class="arrow">›</span></a>\n'
                  f' <a href="{Z}" class="city-card"><h3>Zionsville</h3><span class="cprice">$400s – $1M+</span><span class="arrow">›</span></a>', 1)
    s = s.replace("Browse every active MIBOR MLS listing in Johnson County.", "Browse every active MIBOR MLS listing in Johnson and Boone counties.", 1)
    os.makedirs(f"compare/{SLUG}", exist_ok=True)
    open(f"compare/{SLUG}/index.html", "w", encoding="utf-8").write(s)
    print("built", SLUG)

    # sitemap
    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL not in sm:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>",
             f" <url>\n <loc>{URL}</loc>\n <lastmod>2026-10-14</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.8</priority>\n </url>\n</urlset>"))
    # links from the two-way pages it extends
    for p in ("compare/greenwood-vs-franklin/index.html", "compare/zionsville-vs-whitestown/index.html", "compare/zionsville-vs-carmel/index.html"):
        if not os.path.exists(p):
            continue
        t2 = open(p, encoding="utf-8").read()
        card = f' <a href="/compare/{SLUG}/" class="city-card">Greenwood vs Franklin vs Zionsville <span class="arrow">›</span></a>\n'
        if f"/compare/{SLUG}/" not in t2 and '<div class="compare-grid"' in t2:
            i = t2.index(">", t2.index('<div class="compare-grid"')) + 2
            open(p, "w", encoding="utf-8").write(t2[:i] + card + t2[i:])
            print("linked from", p)


if __name__ == "__main__":
    main()
