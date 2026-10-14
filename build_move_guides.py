#!/usr/bin/env python3
"""Build the Cincinnati and Louisville "moving to Indianapolis" guides (Oct 2026 SEO audit).

Same shell and approach as build_chicago_post.py (relocation-guide template). Every number is
from a dated official source: BEA Regional Price Parities 2024 (via FRED), Census ACS 2024
1-year (metro median home value B25077, median real estate taxes B25103), Indiana DOR 2026
county rates, Ohio 2026 flat rate (EY on HB 96), City of Cincinnati, Kentucky DOR 2026,
Louisville Metro Form OL-3, Visit Indy driving chart. Framed honestly: Cincinnati costs about
the same as Indianapolis, and Louisville is cheaper on housing.

Re-runnable. Adds each post to sitemap.xml and the blog index, and links the three move
guides (Chicago, Cincinnati, Louisville) from the relocation guide.
"""
import html, json, os, re

SRC = "blog/moving-to-indianapolis-relocation-guide/index.html"
IMG = "https://yourrealtylink.com/assets/img/blog/moving-to-indianapolis-relocation-guide.png"
FRED = "https://fred.stlouisfed.org/series/"
ACS_V = "https://data.census.gov/table/ACSDT1Y2024.B25077"
ACS_T = "https://data.census.gov/table/ACSDT1Y2024.B25103"
DOR = "https://www.in.gov/dor/files/dn01.pdf"
OTHER_GUIDES = {"chicago": ("Chicago", "/blog/moving-from-chicago-to-indianapolis/"),
                "cincinnati": ("Cincinnati", "/blog/moving-from-cincinnati-to-indianapolis/"),
                "louisville": ("Louisville", "/blog/moving-from-louisville-to-indianapolis/")}

GUIDES = {
"cincinnati": dict(city="Cincinnati", slug="moving-from-cincinnati-to-indianapolis",
 desc="Moving from Cincinnati to Indianapolis? Compare cost of living, home prices, property and income taxes and the I-74 drive, plus where Cincinnati transplants tend to buy.",
 hero="Under two hours up I-74: how the cost of living, home prices and taxes actually compare, and where Cincinnati transplants tend to buy.",
 rpp=("95.4", "87.6", "RPPALL17140"), home="$288,700", tax="$3,255",
 inc="Ohio 2.75% + Cincinnati city tax 1.8%",
 intro="Cincinnati and Indianapolis are a lot alike: similar-sized Midwest metros, a similar cost of living, and just under two hours apart on I-74. People make the move for a job, family or a fresh start rather than a dramatically cheaper life, so the details matter more than the headline. Here&rsquo;s what the federal, state and city data shows, and where Cincinnati transplants tend to settle.",
 cost="The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored 95.7 and the Cincinnati metro 95.4, essentially the same. Housing is close too: 88.9 for Indianapolis versus 87.6 for Cincinnati. In other words, don&rsquo;t expect a big drop in everyday costs. The real differences are in taxes and in what&rsquo;s available at your price point.",
 homes="The Census Bureau&rsquo;s 2024 survey puts the median home value at $291,400 for the Indianapolis metro and $288,700 for the Cincinnati metro, almost identical. What changes is the mix: Central Indiana has a lot of newer construction in its fast-growing suburbs, so many buyers trade an older home for a newer one at a similar price. Start with our <a href=\"/best/indianapolis-suburbs-for-families/\">best suburbs for families</a> and <a href=\"/best/most-affordable-indianapolis-suburbs/\">most affordable suburbs</a> rankings, or <a href=\"/search/\">search live listings</a>.",
 taxes_income="Ohio&rsquo;s state income tax is a flat 2.75% for 2026 on income above $26,050, and the City of Cincinnati adds a 1.8% income tax, about 4.55% combined for a city resident. Indiana&rsquo;s state rate is 2.95% plus a county income tax: 1.10% in Hamilton County (Carmel, Fishers, Westfield, Noblesville) and 2.02% in Marion County (Indianapolis), for example. So income taxes come out a bit lower if you land in Hamilton County and a bit higher in Marion County. Exemptions differ between the states, so run your own numbers with a tax professional. Indiana sets your county rate by where you live on January 1, which matters in your move year.",
 taxes_prop="Property tax bills tend to be lower in Indianapolis. The median homeowner bill was $2,409 in the Indianapolis metro versus $3,255 in the Cincinnati metro (Census ACS 2024). Indiana&rsquo;s constitution caps property taxes on your primary home at 1% of its assessed value, and you&rsquo;ll want to file the homestead deduction with the county auditor after you close.",
 drive="Indianapolis is about 112 miles from Cincinnati, a bit under two hours on I-74. Both cities are on Eastern time, so there&rsquo;s no clock change. I-74 enters Indianapolis from the southeast, so if you&rsquo;ll be driving back to Cincinnati often, the southeast side shortens the trip.",
 where=[("Close to I-74 for trips back", 'the southeast side, including <a href="/neighborhoods/franklin-township-indianapolis/">Franklin Township</a> and <a href="/cities/shelby-county/shelbyville-indiana-real-estate/">Shelbyville</a> right on I-74.'),
        ("Walkable, urban living", 'downtown and close-in neighborhoods like <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>, <a href="/neighborhoods/fletcher-place-indianapolis/">Fletcher Place</a> and <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a>.'),
        ("Schools and newer suburbs", '<a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a>, <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a> and <a href="/cities/hamilton-county/noblesville-indiana-real-estate/">Noblesville</a> in Hamilton County, which also has the metro&rsquo;s lowest county income tax.'),
        ("Value with a short commute", '<a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a> and the south side, including <a href="/neighborhoods/perry-township-indianapolis/">Perry Township</a>.')],
 faqs=[("Is Indianapolis cheaper than Cincinnati?", "About the same. The Bureau of Economic Analysis puts 2024 price levels at 95.7 for the Indianapolis metro and 95.4 for the Cincinnati metro, and median home values are nearly identical ($291,400 vs. $288,700). Property tax bills tend to be lower in Indianapolis."),
       ("How far is Indianapolis from Cincinnati?", "About 112 miles, a bit under two hours by car on I-74."),
       ("Are income taxes higher in Indianapolis than Cincinnati?", "It depends on the county. A Cincinnati resident pays about 4.55% (Ohio 2.75% plus the 1.8% city tax). In Indiana it's 2.95% plus the county rate: about 4.05% in Hamilton County and 4.97% in Marion County. Exemptions differ, so check with a tax professional."),
       ("Are Indianapolis and Cincinnati in the same time zone?", "Yes. Both are on Eastern time.")],
 sources=[(FRED + "RPPALL17140", "BEA Regional Price Parities (2024) via FRED"), (ACS_V, "Census ACS 2024 median home value"), (ACS_T, "median real estate taxes"),
          (DOR, "Indiana DOR county tax rates (2026)"), ("https://taxnews.ey.com/news/2026-1619-ohio-releases-modified-2026-income-tax-withholding-formulas-and-tables-reflecting-scheduled-tax-cut", "EY: Ohio 2026 rate"),
          ("https://www.cincinnati-oh.gov/finance/income-taxes/", "City of Cincinnati income tax")]),

"louisville": dict(city="Louisville", slug="moving-from-louisville-to-indianapolis",
 desc="Moving from Louisville to Indianapolis? Compare cost of living, home prices, income and property taxes and the I-65 drive, plus where Louisville transplants tend to buy.",
 hero="About two hours up I-65: an honest look at cost of living, home prices and taxes, and where Louisville transplants tend to buy.",
 rpp=("93.1", "78.6", "RPPALL31140"), home="$265,900", tax="$2,130",
 inc="Kentucky 3.5% + Louisville Metro 2.2%",
 intro="Louisville to Indianapolis is an easy move on paper: about two hours straight up I-65, same time zone, and plenty of family and friends within a day trip. It isn&rsquo;t a move to save on housing, though; Louisville is the cheaper of the two. People make the jump for jobs, schools, newer homes and a lower income tax bill. Here&rsquo;s what the federal, state and local data shows, and where Louisville transplants tend to settle.",
 cost="The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored 95.7 and the Louisville metro 93.1, so everyday prices run about 3% higher in Indianapolis. Housing shows the bigger gap: 88.9 for Indianapolis versus 78.6 for Louisville, roughly 13% higher. If housing cost is your main reason to move, Louisville already has the edge; Indianapolis wins on other things below.",
 homes="The Census Bureau&rsquo;s 2024 survey puts the median home value at $291,400 for the Indianapolis metro and $265,900 for the Louisville metro. Expect to budget a bit more for a similar home, especially in the most popular suburbs. In return, Central Indiana&rsquo;s fast-growing suburbs offer a lot of newer construction. Start with our <a href=\"/best/most-affordable-indianapolis-suburbs/\">most affordable suburbs</a> and <a href=\"/best/indianapolis-suburbs-for-families/\">best suburbs for families</a> rankings, or <a href=\"/search/\">search live listings</a>.",
 taxes_income="This is where Indianapolis comes out ahead. Kentucky&rsquo;s income tax is a flat 3.5% for 2026, and Louisville Metro adds a 2.2% occupational tax for residents, about 5.7% combined. Indiana&rsquo;s state rate is 2.95% plus a county income tax: 1.10% in Hamilton County (Carmel, Fishers, Westfield, Noblesville), 1.40% in Johnson County (Greenwood, Franklin) and 2.02% in Marion County (Indianapolis), for example. That&rsquo;s roughly 4% to 5% combined. Exemptions differ between the states, so run your own numbers with a tax professional. Indiana sets your county rate by where you live on January 1, which matters in your move year.",
 taxes_prop="Property tax bills are a bit higher in the Indianapolis metro: the median homeowner bill was $2,409 versus $2,130 in the Louisville metro (Census ACS 2024), largely because home values are higher. Indiana&rsquo;s constitution caps property taxes on your primary home at 1% of its assessed value, and you&rsquo;ll want to file the homestead deduction with the county auditor after you close.",
 drive="Indianapolis is about 114 miles from Louisville, roughly two hours on I-65. Both cities are on Eastern time. I-65 enters Indianapolis from the south, so if you&rsquo;ll be driving back to Louisville often, the south side and Johnson County keep that trip short.",
 where=[("Close to I-65 for trips back", '<a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a>, <a href="/cities/johnson-county/franklin-indiana-real-estate/">Franklin</a>, <a href="/neighborhoods/center-grove-indiana/">Center Grove</a> and <a href="/neighborhoods/perry-township-indianapolis/">Perry Township</a>.'),
        ("Lower county income tax", 'Hamilton County suburbs like <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>, <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a> and <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a> (1.10%).'),
        ("Walkable, urban living", 'close-in neighborhoods like <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a>, <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a> and <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>.'),
        ("Value close to the city", 'south-side and southwest options like <a href="/neighborhoods/decatur-township-indianapolis/">Decatur Township</a> and <a href="/cities/marion-county/beech-grove-indiana-real-estate/">Beech Grove</a>.')],
 faqs=[("Is Indianapolis more expensive than Louisville?", "Somewhat. The Bureau of Economic Analysis puts 2024 price levels at 95.7 for the Indianapolis metro and 93.1 for Louisville, and housing costs run roughly 13% higher. Median home values are $291,400 in the Indianapolis metro versus $265,900 in the Louisville metro."),
       ("How far is Indianapolis from Louisville?", "About 114 miles, roughly two hours by car on I-65."),
       ("Are taxes lower in Indianapolis than Louisville?", "Income taxes usually are: Kentucky's 3.5% plus Louisville Metro's 2.2% occupational tax is about 5.7%, versus roughly 4% to 5% in Indiana depending on the county. Property tax bills run a little higher in the Indianapolis metro because home values are higher."),
       ("Are Indianapolis and Louisville in the same time zone?", "Yes. Both are on Eastern time.")],
 sources=[(FRED + "RPPALL31140", "BEA Regional Price Parities (2024) via FRED"), (ACS_V, "Census ACS 2024 median home value"), (ACS_T, "median real estate taxes"),
          (DOR, "Indiana DOR county tax rates (2026)"), ("https://revenue.ky.gov/Business/Pages/Employer-Payroll-Withholding.aspx", "Kentucky DOR (2026)"),
          ("https://www.louisvilleky.gov/revenue-commission/forms/form-ol-3", "Louisville Metro occupational tax")]),
}


def body(g):
    c = g["city"]
    a_rpp, a_house, _ = g["rpp"]
    others = [f'<a href="{u}">{n}</a>' for k, (n, u) in OTHER_GUIDES.items() if n != c]
    where = "\n".join(f" <li><strong>{h}:</strong> {t}</li>" for h, t in g["where"])
    faq = "\n".join(f' <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in g["faqs"])
    src = " &middot; ".join(f'<a href="{u}" target="_blank" rel="noopener">{l}</a>' for u, l in g["sources"])
    return f"""
 <p>{g['intro']}</p>

 <h2 id="at-a-glance">Indianapolis vs. {c} at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <tr><th></th><th>Indianapolis</th><th>{c}</th></tr>
 <tr><td>Overall price level (BEA, 2024; U.S. = 100)</td><td>95.7</td><td>{a_rpp}</td></tr>
 <tr><td>Housing price level (BEA, 2024)</td><td>88.9</td><td>{a_house}</td></tr>
 <tr><td>Median home value, metro (Census ACS 2024)</td><td>$291,400</td><td>{g['home']}</td></tr>
 <tr><td>Median homeowner property tax bill, metro (ACS 2024)</td><td>$2,409</td><td>{g['tax']}</td></tr>
 <tr><td>Income tax (2026)</td><td>Indiana 2.95% + county tax (1.10%&ndash;2.02% in the core counties)</td><td>{g['inc']}</td></tr>
 <tr><td>Time zone</td><td>Eastern</td><td>Eastern</td></tr>
 </table>
 </div>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>{g['cost']}</p>

 <h2 id="home-prices">Home Prices and What Your Budget Buys</h2>
 <p>{g['homes']}</p>

 <h2 id="taxes">Taxes: Income, Property and the Trade-Offs</h2>
 <p><strong>Income tax.</strong> {g['taxes_income']}</p>
 <p><strong>Property tax.</strong> {g['taxes_prop']} Comparing counties? See <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>.</p>

 <h2 id="drive">The Drive and Trips Back</h2>
 <p>{g['drive']}</p>

 <h2 id="where-to-live">Where {c} Transplants Tend to Look</h2>
 <ul>
{where}
 </ul>
 <p>Not sure which fits? Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro. Moving from somewhere else? See our {others[0]} and {others[1]} guides.</p>

 <h2 id="checklist">Your Move Checklist</h2>
 <ul>
 <li>Update your driver&rsquo;s license and vehicle registration with the Indiana BMV.</li>
 <li>File your homestead deduction with the county auditor after you close.</li>
 <li>Check which county&rsquo;s income tax applies for your move year.</li>
 <li>Set up utilities before move-in with our <a href="/utilities/">Central Indiana utilities guide</a>.</li>
 <li>Talk with us about buyer representation; a written buyer agreement sets out how your agent is paid, so you know the terms before you tour.</li>
 </ul>

 <h2 id="work-with-us">Talk to Our Team</h2>
 <p>Our team helps relocating buyers every month, including virtual tours and buying before you arrive. Tell us what you have in {c} and what you want here, and we&rsquo;ll map out the areas that fit. Call <a href="tel:3179977404">317-997-7404</a> or <a href="/schedule/buyer-consultation/">book a buyer consultation</a>.</p>

 <!-- FAQ -->
 <h2 id="faq">Frequently Asked Questions</h2>
{faq}

 <p style="font-size:.85rem;color:var(--gray);">Sources: {src} &middot; <a href="{ACS_V}" target="_blank" rel="noopener">Indianapolis metro figures from the same tables</a>. General information, not tax advice.</p>

 """


def build(key, g, tpl):
    url = f"https://yourrealtylink.com/blog/{g['slug']}/"
    c = g["city"]
    title = f"Moving from {c} to Indianapolis: 2026 Guide"
    headline = f"Moving from {c} to Indianapolis: Costs, Taxes & Where to Live"
    s = tpl
    s = re.sub(r"<!-- YOAST:.*?-->", f"<!-- YOAST: Focus Keyword: moving from {c.lower()} to indianapolis | Category: Relocation -->", s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop, val in (("og:title", title), ("og:description", g["desc"]), ("og:url", url)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", g["desc"]), ("twitter:title", title), ("twitter:description", g["desc"])):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": headline, "description": g["desc"],
         "author": {"@type": "Person", "name": "Daniel Cope", "url": "https://yourrealtylink.com/agents/daniel-cope/", "jobTitle": "Real Estate Broker",
                    "worksFor": {"@type": "Organization", "name": "Your Realty Link"}},
         "publisher": {"@type": "Organization", "name": "Your Realty Link", "logo": {"@type": "ImageObject", "url": "/assets/img/yrl-logo.png"}},
         "image": IMG, "datePublished": "2026-10-14", "dateModified": "2026-10-14", "mainEntityOfPage": url},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yourrealtylink.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": url}]}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faqs"]]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    new = ['<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n</script>',
           '<script type="application/ld+json">\n' + json.dumps(faqld, indent=1, ensure_ascii=False) + '\n</script>']
    for m, rep in reversed(list(zip(blocks[:2], new))):
        s = s[:m.start()] + rep + s[m.end():]
    s = s.replace(" Moving to Indianapolis Relocation Guide\n </div>\n</nav>", f" Moving from {c} to Indianapolis\n </div>\n</nav>", 1)
    s = re.sub(r"<h1>.*?</h1>", f"<h1>Moving from {c} to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em></h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) + g["hero"] + m.group(2), s, count=1, flags=re.S)
    s = s.replace("Updated August 2026</p>", "Updated October 2026</p>", 1)
    s = re.sub(r'(<div class="post-meta">.*?<span>)August 2026(</span>.*?<span>)~9 min read', r"\1October 2026\2~7 min read", s, count=1, flags=re.S)
    i = s.index("</div>", s.index('<div class="post-meta">')) + len("</div>")
    j = s.index("<!-- CTA -->")
    s = s[:i] + "\n" + body(g) + s[j:]
    os.makedirs(f"blog/{g['slug']}", exist_ok=True)
    open(f"blog/{g['slug']}/index.html", "w", encoding="utf-8").write(s)
    print("built", g["slug"])
    return url


def main():
    tpl = open(SRC, encoding="utf-8").read()
    sm = open("sitemap.xml", encoding="utf-8").read()
    bi = open("blog/index.html", encoding="utf-8").read()
    for key, g in GUIDES.items():
        url = build(key, g, tpl)
        if url not in sm:
            sm = sm.replace("</urlset>", f" <url>\n <loc>{url}</loc>\n <lastmod>2026-10-14</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.7</priority>\n </url>\n</urlset>")
        if f"/blog/{g['slug']}/" not in bi:
            m = re.search(r'\n( *)<div class="blog-card">\s*<div class="blog-card-img"><img src="/assets/img/blog/moving-to-indianapolis-relocation-guide\.png" alt="moving to', bi)
            if m:
                ind = m.group(1)
                card = (f'\n{ind}<div class="blog-card">\n <div class="blog-card-img"><img src="/assets/img/blog/moving-to-indianapolis-relocation-guide.png" alt="moving from {g["city"].lower()} to indianapolis" loading="lazy"></div>\n'
                        f' <div class="blog-card-body">\n <div class="blog-card-cat">Relocation</div>\n <h3>Moving from {g["city"]} to Indianapolis: Costs, Taxes &amp; Where to Live</h3>\n'
                        f' <p>{g["desc"]}</p>\n <a href="/blog/{g["slug"]}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
                bi = bi[:m.start()] + card + bi[m.start():]
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    open("blog/index.html", "w", encoding="utf-8").write(bi)
    # relocation guide: one line pointing to all three city guides
    rg = open(SRC, encoding="utf-8").read()
    line = ('<p>Coming from Chicago, Cincinnati or Louisville? See our side-by-side guides on costs, taxes and the drive: '
            '<a href="/blog/moving-from-chicago-to-indianapolis/">Chicago</a>, <a href="/blog/moving-from-cincinnati-to-indianapolis/">Cincinnati</a> '
            'and <a href="/blog/moving-from-louisville-to-indianapolis/">Louisville</a>.</p>')
    rg2 = re.sub(r"<p>Coming from Chicago[^\n]*?</p>", line, rg, count=1)
    if rg2 != rg:
        open(SRC, "w", encoding="utf-8").write(rg2)
        print("relocation guide links updated")


if __name__ == "__main__":
    main()
