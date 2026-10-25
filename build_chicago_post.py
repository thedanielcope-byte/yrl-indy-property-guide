#!/usr/bin/env python3
"""Build /blog/moving-from-chicago-to-indianapolis/ from the relocation-guide post shell.

Oct 2026 SEO audit gap: "moving from chicago to indianapolis" was held by moving companies.
Every number is from a dated official source (BEA Regional Price Parities 2024, Census ACS 2024
1-year, Indiana DOR 2026 county rates, Illinois Comptroller 2026 bulletin, Visit Indy driving
chart, Visit Indiana time zones). No Chicago city income-tax claim (couldn't verify directly).
Re-runnable. Adds the post to sitemap.xml, the blog index, and links it from the relocation guide.
"""
import html, json, os, re

SRC = "blog/moving-to-indianapolis-relocation-guide/index.html"
SLUG = "moving-from-chicago-to-indianapolis"
URL = f"https://yourrealtylink.com/blog/{SLUG}/"
TITLE = "Moving from Chicago to Indianapolis: 2026 Guide | Your Realty Link"
H1 = "Moving from Chicago to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em>"
HEADLINE = "Moving from Chicago to Indianapolis: Costs, Taxes & Where to Live"
DESC = "Moving from Chicago to Indianapolis? Compare cost of living, home prices, taxes, the drive and the time zone, plus where Chicago transplants tend to buy."
IMG = "https://yourrealtylink.com/assets/img/blog/moving-to-indianapolis-relocation-guide.png"

FAQS = [
 ("Is it cheaper to live in Indianapolis than Chicago?",
  "Yes, on federal measures. The Bureau of Economic Analysis puts 2024 overall price levels at 95.7 for the Indianapolis metro versus 103.6 for the Chicago metro (U.S. = 100), about 7.6% lower, and housing costs about 21% lower."),
 ("How far is Indianapolis from Chicago?",
  "About 183 miles, roughly three hours by car, almost all of it on I-65."),
 ("Are property taxes lower in Indianapolis than Chicago?",
  "Generally, yes. The median homeowner property tax bill was $2,228 in Marion County versus $6,349 in Cook County (Census ACS 2024), and Indiana caps homestead property taxes at 1% of assessed value."),
 ("What time zone is Indianapolis in?",
  "Eastern time. Chicago is on Central time, so you lose an hour driving south; the northwest Indiana counties near Chicago stay on Central time."),
]

BODY = """
 <p>Every year a steady stream of Chicagoans head about three hours south on I-65 and land in Central Indiana. The draw is easy to see: a lower cost of living, much lower property tax bills, newer and bigger homes for the money, and a metro that&rsquo;s simple to get around. Here&rsquo;s what the numbers actually show, using federal, state and county sources, and where Chicago transplants tend to settle.</p>

 <h2 id="at-a-glance">Indianapolis vs. Chicago at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <tr><th></th><th>Indianapolis</th><th>Chicago</th></tr>
 <tr><td>Overall price level (BEA, 2024; U.S. = 100)</td><td>95.7</td><td>103.6</td></tr>
 <tr><td>Housing price level (BEA, 2024)</td><td>88.9</td><td>112.0</td></tr>
 <tr><td>Median home value, metro (Census ACS 2024)</td><td>$291,400</td><td>$339,700</td></tr>
 <tr><td>Median homeowner property tax bill, metro (ACS 2024)</td><td>$2,409</td><td>$6,461</td></tr>
 <tr><td>State income tax (2026)</td><td>2.95% + county tax (1.10%&ndash;2.02% in the core counties)</td><td>4.95% (Illinois)</td></tr>
 <tr><td>Time zone</td><td>Eastern</td><td>Central</td></tr>
 </table>
 </div>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored 95.7 and the Chicago metro 103.6, so everyday prices in Indianapolis run about 7.6% lower. The biggest gap is housing: 88.9 for Indianapolis versus 112.0 for Chicago, roughly 21% lower. These are metro-wide averages, so individual neighborhoods vary, but the direction is clear.</p>

 <h2 id="home-prices">Home Prices and What Your Budget Buys</h2>
 <p>The Census Bureau&rsquo;s 2024 survey puts the median home value at $291,400 for the Indianapolis metro and $339,700 for the Chicago metro. Inside city limits the gap is wider: $241,500 in Indianapolis versus $341,200 in Chicago. In practice, many of our Chicago clients find they can move from a condo or townhome into a detached house with a yard. To see what your budget buys town by town, start with our <a href="/best/most-affordable-indianapolis-suburbs/">most affordable suburbs</a> and <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> rankings, or <a href="/search/">search live listings</a>.</p>

 <h2 id="taxes">Taxes: Income, Property and the Trade-Offs</h2>
 <p><strong>Income tax.</strong> Illinois has a flat 4.95% income tax. Indiana&rsquo;s state rate is 2.95% for 2026, plus a county income tax that depends on where you live: 1.10% in Hamilton County (Carmel, Fishers, Westfield, Noblesville) and 2.02% in Marion County (Indianapolis), for example. That puts the combined rate close to Illinois&rsquo;s in Marion County and about a point lower in Hamilton County. Exemptions and deductions differ between the states, so run your own numbers with a tax professional. Indiana sets your county rate by where you live on January 1, which matters in your move year.</p>
 <p><strong>Property tax.</strong> This is where Chicago buyers notice the biggest difference. The median homeowner bill was $2,228 in Marion County versus $6,349 in Cook County (Census ACS 2024). Indiana&rsquo;s constitution caps property taxes on your primary home at 1% of its assessed value, and you&rsquo;ll want to file the homestead deduction with the county auditor after you close. Comparing counties? See <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>.</p>

 <h2 id="drive-time-zone">The Drive, Trips Back and the Time Zone</h2>
 <p>Indianapolis is about 183 miles from Chicago, roughly three hours, almost all of it on I-65. One thing to plan for: Chicago is on Central time and Indianapolis is on Eastern, so you lose an hour heading south. The northwest Indiana counties near Chicago (Lake, Porter, LaPorte, Jasper, Newton and Starke) stay on Central time, so the switch happens partway down the drive. If you&rsquo;re keeping a Chicago employer on a hybrid schedule, mind the one-hour calendar offset.</p>

 <h2 id="where-to-live">Where Chicago Transplants Tend to Look</h2>
 <ul>
 <li><strong>Walkable, urban living:</strong> downtown and close-in neighborhoods like <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>, <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a> and <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>.</li>
 <li><strong>Amenity-rich suburbs:</strong> <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>, with its Arts &amp; Design District and the Monon Trail, and <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a>, with the Nickel Plate District.</li>
 <li><strong>Newer construction:</strong> <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a>, <a href="/cities/boone-county/whitestown-indiana-real-estate/">Whitestown</a> and <a href="/cities/hancock-county/mccordsville-indiana-real-estate/">McCordsville</a>.</li>
 <li><strong>Value with a short commute:</strong> <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a> and the south side, including <a href="/neighborhoods/perry-township-indianapolis/">Perry Township</a>.</li>
 </ul>
 <p>Not sure which fits? Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro. Moving from somewhere else? See our <a href="/blog/moving-from-cincinnati-to-indianapolis/">Cincinnati</a> and <a href="/blog/moving-from-louisville-to-indianapolis/">Louisville</a> guides.</p>

 <h2 id="checklist">Your Move Checklist</h2>
 <ul>
 <li>Update your driver&rsquo;s license and vehicle registration with the Indiana BMV.</li>
 <li>File your homestead deduction with the county auditor after you close.</li>
 <li>Check which county&rsquo;s income tax applies for your move year.</li>
 <li>Set up utilities before move-in with our <a href="/utilities/">Central Indiana utilities guide</a>.</li>
 <li>Talk with us about buyer representation; a written buyer agreement sets out how your agent is paid, so you know the terms before you tour.</li>
 </ul>

 <h2 id="work-with-us">Talk to Our Team</h2>
 <p>Our team helps relocating buyers every month, including virtual tours and buying before you arrive. Tell us what you have in Chicago and what you want here, and we&rsquo;ll map out the areas that fit. Call <a href="tel:3179977404">317-997-7404</a> or <a href="/schedule/buyer-consultation/">book a buyer consultation</a>.</p>

 <!-- FAQ -->
 <h2 id="faq">Frequently Asked Questions</h2>
__FAQ__

 <p style="font-size:.85rem;color:var(--gray);">Sources: <a href="https://fred.stlouisfed.org/series/RPPALL26900" target="_blank" rel="noopener">BEA Regional Price Parities (2024) via FRED</a> &middot; <a href="https://data.census.gov/table/ACSDT1Y2024.B25077" target="_blank" rel="noopener">Census ACS 2024 median home value</a> and <a href="https://data.census.gov/table/ACSDT1Y2024.B25103" target="_blank" rel="noopener">median real estate taxes</a> &middot; <a href="https://www.in.gov/dor/files/dn01.pdf" target="_blank" rel="noopener">Indiana DOR county tax rates (2026)</a> &middot; <a href="https://illinoiscomptroller.gov/__media/sites/comptroller/assets/File/PayrollBulletins/Payroll%20Bulletin%201-26%20-%20Illinois%20State%20Income%20Tax%20Exemptions%20-%202026.pdf" target="_blank" rel="noopener">Illinois Comptroller (2026)</a> &middot; <a href="https://visitindiana.in.gov/about-indiana/time-zones" target="_blank" rel="noopener">Visit Indiana: time zones</a>. General information, not tax advice.</p>

 """


def main():
    s = open(SRC, encoding="utf-8").read()
    t = html.escape(TITLE, quote=False)
    s = re.sub(r"<!-- YOAST:.*?-->", "<!-- YOAST: Focus Keyword: moving from chicago to indianapolis | Category: Relocation -->", s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{t}</title>", s, count=1)
    for prop, val in (("og:title", t), ("og:description", DESC), ("og:url", URL)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", DESC), ("twitter:title", t), ("twitter:description", DESC)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": HEADLINE, "description": DESC,
         "author": {"@type": "Person", "name": "Daniel Cope", "url": "https://yourrealtylink.com/agents/daniel-cope/", "jobTitle": "Real Estate Broker",
                    "worksFor": {"@type": "Organization", "name": "Your Realty Link"}},
         "publisher": {"@type": "Organization", "name": "Your Realty Link", "logo": {"@type": "ImageObject", "url": "/assets/img/yrl-logo.png"}},
         "image": IMG, "datePublished": "2026-10-14", "dateModified": "2026-10-14", "mainEntityOfPage": URL},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yourrealtylink.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": HEADLINE, "item": URL}]}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    new = ['<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n</script>',
           '<script type="application/ld+json">\n' + json.dumps(faqld, indent=1, ensure_ascii=False) + '\n</script>']
    for m, rep in reversed(list(zip(blocks[:2], new))):
        s = s[:m.start()] + rep + s[m.end():]
    s = s.replace(" Moving to Indianapolis Relocation Guide\n </div>\n</nav>", " Moving from Chicago to Indianapolis\n </div>\n</nav>", 1)
    s = re.sub(r"<h1>.*?</h1>", f"<h1>{H1}</h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) +
               "About three hours down I-65: what the federal data says about cost of living, home prices and taxes, plus the time-zone switch and where Chicago transplants tend to buy." + m.group(2), s, count=1, flags=re.S)
    s = s.replace("Updated August 2026</p>", "Updated October 2026</p>", 1)
    s = re.sub(r'(<div class="post-meta">.*?<span>)August 2026(</span>.*?<span>)~9 min read', r"\1October 2026\2~7 min read", s, count=1, flags=re.S)
    faq = "\n".join(f' <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in FAQS)
    i = s.index("</div>", s.index('<div class="post-meta">')) + len("</div>")
    j = s.index("<!-- CTA -->")
    s = s[:i] + "\n" + BODY.replace("__FAQ__", faq) + s[j:]
    os.makedirs(f"blog/{SLUG}", exist_ok=True)
    open(f"blog/{SLUG}/index.html", "w", encoding="utf-8").write(s)
    print("built", SLUG)

    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL not in sm:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>",
             f" <url>\n <loc>{URL}</loc>\n <lastmod>2026-10-14</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.7</priority>\n </url>\n</urlset>"))
    # blog index card, placed before the relocation guide's card
    bi = open("blog/index.html", encoding="utf-8").read()
    if f"/blog/{SLUG}/" not in bi:
        m = re.search(r'\n( *)<div class="blog-card">\s*<div class="blog-card-img"><img src="/assets/img/blog/moving-to-indianapolis-relocation-guide\.png"', bi)
        if m:
            ind = m.group(1)
            card = (f'\n{ind}<div class="blog-card">\n <div class="blog-card-img"><img src="/assets/img/blog/moving-to-indianapolis-relocation-guide.png" alt="moving from chicago to indianapolis" loading="lazy"></div>\n'
                    f' <div class="blog-card-body">\n <div class="blog-card-cat">Relocation</div>\n <h3>Moving from Chicago to Indianapolis: Costs, Taxes &amp; Where to Live</h3>\n'
                    f' <p>Moving from Chicago to Indianapolis? Cost of living, home prices, property and income taxes, the drive and the time zone, plus where Chicago transplants tend to buy.</p>\n'
                    f' <a href="/blog/{SLUG}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
            bi = bi[:m.start()] + card + bi[m.start():]
            open("blog/index.html", "w", encoding="utf-8").write(bi)
            print("blog index card added")
    # link from the relocation guide
    rg = open(SRC, encoding="utf-8").read()
    if f"/blog/{SLUG}/" not in rg and '<h2 id="buying-remote">' in rg:
        rg = rg.replace('<h2 id="buying-remote">', f'<p>Coming from Chicago? See our <a href="/blog/{SLUG}/">Chicago-to-Indianapolis guide</a> for a side-by-side on costs, taxes and the time zone.</p>\n <h2 id="buying-remote">', 1)
        open(SRC, "w", encoding="utf-8").write(rg)
        print("linked from relocation guide")


if __name__ == "__main__":
    main()
