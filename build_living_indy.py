#!/usr/bin/env python3
"""Build /blog/living-in-indianapolis-pros-and-cons/ (Nov 2026).

Pillar page for "living in Indianapolis", "pros and cons of living in Indianapolis" and
"is Indianapolis a good place to live" (Copilot already cites us for these; Google shows us
around position 20-45). Complements the relocation guide (where to live / buying from out of
state) with numbers and honest downsides. Every figure is dated and sourced (research
sheet, Nov 2 2026): Census V2025 + ACS 2025 1-yr, BEA RPP 2024, Indiana DOR Notice #1
(2026 rates), DLGF circuit-breaker fact sheet, NWS 1991-2020 normals, SEC filings, IND /
ACI release (Feb 2026), IndyGo, Walk Score (undated, attributed), our own MIBOR-based
September 2026 market figure. No crime/safety content. Shell = relocation guide post.
Also renders the post's card image with the finalize_new_posts.py template.
Re-runnable; then run inject_gtag.py, inject_favicon.py, gloss_autolink.py . --apply.
"""
import base64, html, json, os, re, subprocess

SRC = "blog/moving-to-indianapolis-relocation-guide/index.html"
SLUG = "living-in-indianapolis-pros-and-cons"
URL = f"https://yourrealtylink.com/blog/{SLUG}/"
TITLE = "Living in Indianapolis: Pros and Cons (2026)"
HEADLINE = "Living in Indianapolis: The Real Pros and Cons"
DESC = ("Thinking about living in Indianapolis? The real pros and cons for 2026: cost of living, "
        "taxes, weather, commute, jobs, and what locals wish they'd known.")
IMG = f"/assets/img/blog/{SLUG}.png"
OG = "https://yourrealtylink.com" + IMG
DATE = "2026-11-02"

QA_LEAD = ("<strong>Is Indianapolis a good place to live?</strong> For a lot of people, yes. The metro costs about 4% less "
           "than the U.S. average (housing about 11% less), state income tax is a flat 2.95%, commutes are shorter than "
           "the national average, and the airport has been named best in North America 14 years running. The trade-offs: "
           "you&rsquo;ll need a car, winters are real, and summers are humid.")
QA_FACTS = [("Population", "901,116 city &middot; 2.2M metro (2025)"), ("Cost of living", "About 4.3% below U.S. average (2024)"),
            ("Typical home price", "$320,000 metro median (Sept 2026)"), ("State income tax", "2.95% flat (2026)"),
            ("Average commute", "25.1 minutes (U.S. 27.4)"), ("Snowfall", "About 25.5 inches a year")]

FAQS = [
 ("Is Indianapolis a good place to live?",
  "For many people, yes. Living costs run about 4% below the U.S. average (BEA, 2024), Indiana's income tax is a flat 2.95% in 2026, commutes average about 25 minutes, and there are major employers, pro sports and a top-rated airport. The main downsides are car dependence, cold winters and humid summers."),
 ("Is Indianapolis expensive to live in?",
  "Not compared with most large U.S. metros. The Bureau of Economic Analysis puts the Indianapolis area's prices about 4.3% below the national average in 2024, and housing costs about 11% below. The median home sale price across the MIBOR region was $320,000 in September 2026."),
 ("What are the downsides of living in Indianapolis?",
  "Most people point to car dependence (Walk Score rates the city 31 out of 100, and about 1% of workers ride transit), winters with an average January temperature of 28.5°F, humid summers, and flat terrain. The cost advantage is also narrowing slowly: the area's price index rose from 93.8 in 2022 to 95.7 in 2024."),
 ("How much is income tax in Indianapolis?",
  "Indiana's state income tax is a flat 2.95% for 2026 (scheduled to drop to 2.90% in 2027), and Marion County adds a 2.02% local income tax. Surrounding counties are lower, such as Hamilton County at 1.10% and Johnson County at 1.40%."),
 ("How bad are winters in Indianapolis?",
  "Winters are cold but not extreme. Based on 1991-2020 normals, January averages 28.5°F with an average low of about 21°F, and the area gets about 25.5 inches of snow a year, mostly from December through February."),
]

TOC = [("glance", "Indianapolis at a Glance"), ("pros", "The Pros"), ("cons", "The Cons"), ("city-or-suburbs", "City or Suburbs?"),
       ("our-take", "Our Take"), ("faq", "FAQ")]

S = {
 "census": "https://www.census.gov/programs-surveys/popest.html",
 "acs": "https://www.census.gov/programs-surveys/acs/news/data-releases/2025/release.html",
 "rpp": "https://fred.stlouisfed.org/series/RPPALL26900",
 "dor": "https://www.in.gov/dor/files/dn01.pdf",
 "dlgf": "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf",
 "nws": "https://www.weather.gov/media/ind/climate/INDnormalschange.pdf",
 "ind": "https://www.ind.com/about/media/media-releases/travelers-name-indy-airport-no-1-for-the-14th-year-in-a-row",
 "indygo": "https://www.indygo.net/blue-line/",
 "walk": "https://www.walkscore.com/IN/Indianapolis",
 "market": "/blog/indianapolis-market-update-october-2026/",
}

BODY = f"""
<!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Living in Indianapolis at a Glance</p>
 <p class="qa-lead">{QA_LEAD}</p>
 <dl class="qa-facts">
{chr(10).join(f' <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in QA_FACTS)}
 </dl>
</div>
<!-- QA-END -->

 <p>People ask us some version of this every week, usually from another state: <em>is Indianapolis actually a good place to live?</em> Here&rsquo;s our honest answer, with real numbers rather than slogans, and the downsides we&rsquo;d want to know about if we were the ones moving. If you&rsquo;ve already decided and want to know <em>where</em> to live, our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> covers the suburbs, schools and buying from out of state.</p>

 <h2 id="glance">Indianapolis at a Glance</h2>
 <p>Indianapolis had about <strong>901,000 residents</strong> in 2025, making it the 16th-largest city in the U.S. and the third-largest in the Midwest, behind Chicago and Columbus. The wider metro, which includes Carmel, Fishers, Greenwood and nine other counties, is home to about <strong>2.2 million people</strong> and grew about 1% in 2024-25, faster than most large metros. It&rsquo;s also a young place: the median age is 35.0 in the city and 37.5 in the metro, compared with 39.5 nationally (U.S. Census Bureau, 2025).</p>

 <h2 id="pros">The Pros of Living in Indianapolis</h2>

 <h3>1. Your money goes further</h3>
 <p>The Bureau of Economic Analysis puts prices in the Indianapolis area about <strong>4.3% below the national average</strong> (2024), with housing costs about 11% below. Across the MIBOR region, the median home sold for <strong>$320,000</strong> in September 2026, according to our <a href="{S['market']}">latest market update</a>. That buys considerably more space here than in most large metros, especially in the suburbs.</p>

 <h3>2. Low, simple taxes</h3>
 <p>Indiana&rsquo;s state income tax is a <strong>flat 2.95%</strong> for 2026 and is scheduled to drop to 2.90% in 2027. Each county adds its own local income tax: 2.02% in Marion County, and less in several suburbs, such as 1.10% in Hamilton County and 1.40% in Johnson County. Property taxes on your primary residence are capped by the state constitution at <strong>1% of assessed value</strong> once you file your homestead deduction, and Indiana has no inheritance or estate tax. (Sales tax is 7%.) See our guide to the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">Indiana homestead exemption</a> for how to file.</p>

 <h3>3. Shorter commutes</h3>
 <p>The average one-way commute is <strong>25.1 minutes</strong> in Indianapolis and 25.9 minutes across the metro, compared with 27.4 minutes nationally (Census, 2025). The interstate grid, with I-465 circling the city and I-65, I-69, I-70 and I-74 running out from it, means most suburbs are roughly 20 to 35 minutes from downtown outside rush hour.</p>

 <h3>4. An airport people actually like</h3>
 <p>Indianapolis International Airport was named the <strong>best airport in North America for the 14th year in a row</strong> in its size class by Airports Council International (announced February 2026). It reached a record 58 nonstop destinations in October 2026, and it&rsquo;s typically about 15 to 25 minutes from downtown.</p>

 <h3>5. A solid job base</h3>
 <p>Eli Lilly, Elevance Health, Allison Transmission and Corteva are headquartered here, IU Health is building a roughly $4.3 billion downtown hospital campus due to open in late 2027, and the NCAA&rsquo;s national office is downtown. The city&rsquo;s FedEx Express hub is the company&rsquo;s second largest, and Salesforce has a major office in Salesforce Tower, the state&rsquo;s tallest building.</p>

 <h3>6. Big-city things to do</h3>
 <p>The Colts play at Lucas Oil Stadium, and the Pacers and Fever share Gainbridge Fieldhouse downtown. The Indianapolis Motor Speedway, home of the Indy 500 since 1911, is the largest stadium in the world by capacity, according to Guinness. The Children&rsquo;s Museum calls itself the world&rsquo;s biggest children&rsquo;s museum, Newfields is a 152-acre art and garden campus, and White River State Park packs the zoo, museums and a minor-league ballpark into 250 acres downtown. For getting outside, the roughly 8-mile Indianapolis Cultural Trail connects six downtown cultural districts, and the Monon Trail runs more than 25 miles north through Broad Ripple, Carmel and Westfield.</p>

 <h2 id="cons">The Cons of Living in Indianapolis</h2>

 <h3>1. You&rsquo;ll want a car</h3>
 <p>Walk Score rates Indianapolis <strong>31 out of 100</strong> (&ldquo;car-dependent&rdquo;), and only about 1.2% of city workers commute by transit (Census, 2025). IndyGo&rsquo;s Red Line and Purple Line rapid-bus routes help along their corridors, and the Blue Line, linking the airport, downtown and Cumberland, is under construction with an expected opening in late 2028. Walkable pockets exist, Fountain Square, Broad Ripple and Mass Ave among them, but most households drive.</p>

 <h3>2. Real winters</h3>
 <p>January averages <strong>28.5&deg;F</strong>, with an average low near 21&deg;F, and the area gets about 25.5 inches of snow a year, mostly December through February (National Weather Service, 1991-2020 normals). It&rsquo;s manageable, but it&rsquo;s a real winter.</p>

 <h3>3. Humid summers</h3>
 <p>July averages a high of about 85&deg;F, and summer humidity makes it feel warmer. Expect to run the air conditioning from June through August.</p>

 <h3>4. Flat, with no big natural draw</h3>
 <p>Central Indiana is flat farmland, with no mountains or coastline nearby. Locals make up for it with reservoirs like Geist, Morse and Eagle Creek, state parks within an hour or so, and trails, but if scenery is high on your list, it&rsquo;s worth weighing.</p>

 <h3>5. The cost gap is narrowing</h3>
 <p>Indianapolis is still cheaper than the national average, but less so than a few years ago: the area&rsquo;s price index rose from 93.8 in 2022 to 95.7 in 2024 (BEA). And within the metro, Marion County&rsquo;s 2.02% local income tax is higher than several suburban counties&rsquo;, which is worth factoring into a city-versus-suburb decision.</p>

 <h2 id="city-or-suburbs">City or Suburbs?</h2>
 <p>Much of the &ldquo;living in Indianapolis&rdquo; decision is really this question. Inside the city you&rsquo;ll find historic and walkable neighborhoods like <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>, <a href="/neighborhoods/irvington-indianapolis/">Irvington</a> and <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a>, plus township areas with newer subdivisions such as <a href="/neighborhoods/franklin-township-indianapolis/">Franklin Township</a> and <a href="/neighborhoods/washington-township-indianapolis/">Washington Township</a>. The suburbs, including <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>, <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a>, <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a> and <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a>, trade a longer drive for newer homes, bigger lots and lower local income tax in several counties. Our <a href="/best/">best-of rankings</a> and <a href="/compare/">suburb comparisons</a> lay out the trade-offs town by town.</p>

 <h2 id="our-take">Our Take</h2>
 <p>Indianapolis is easy to underrate from a distance. It&rsquo;s affordable for a metro of 2.2 million, the taxes are simple, and daily life (commutes, travel, getting to a game) is less of a grind than in bigger cities. If you need to walk everywhere or want mountains out the window, it may not be your place. For most of the families and professionals we help relocate, the trade is worth it. Want help figuring out which part of the metro fits you? <a href="/schedule/">Book a free call with our team</a> or <a href="/search/">start browsing homes</a>.</p>

 <!-- FAQ -->
 <h2 id="faq">Frequently Asked Questions</h2>
__FAQ__

 <p style="font-size:.85rem;color:var(--gray);">Sources: <a href="{S['census']}" target="_blank" rel="noopener">U.S. Census Bureau population estimates (2025)</a> &middot; <a href="{S['acs']}" target="_blank" rel="noopener">American Community Survey 2025</a> &middot; <a href="{S['rpp']}" target="_blank" rel="noopener">BEA Regional Price Parities (2024)</a> &middot; <a href="{S['dor']}" target="_blank" rel="noopener">Indiana Department of Revenue, 2026 tax rates</a> &middot; <a href="{S['dlgf']}" target="_blank" rel="noopener">Indiana DLGF, property tax caps</a> &middot; <a href="{S['nws']}" target="_blank" rel="noopener">National Weather Service climate normals</a> &middot; <a href="{S['ind']}" target="_blank" rel="noopener">Indianapolis Airport Authority (Feb 2026)</a> &middot; <a href="{S['indygo']}" target="_blank" rel="noopener">IndyGo</a> &middot; <a href="{S['walk']}" target="_blank" rel="noopener">Walk Score</a> &middot; home prices: MIBOR REALTOR&reg; Association via our <a href="{S['market']}">market update</a>.</p>

 """

CARD_SUB = "Cost of living, taxes, weather, commute, jobs, and the honest downsides."


def render_card():
    src = open("finalize_new_posts.py", encoding="utf-8").read()
    tpl = re.search(r'TPL = """(.*?)"""', src, re.S).group(1)
    logo = base64.b64encode(open("assets/img/yrl-logo.png", "rb").read()).decode()
    title = "Living in Indianapolis: Pros and Cons"
    fs = 72 if len(title) <= 34 else (60 if len(title) <= 48 else 50)
    tmp = "/tmp/yrl-living-card.html"
    open(tmp, "w").write(tpl.format(logo=logo, eyebrow="RELOCATION", title=html.escape(title), sub=html.escape(CARD_SUB), fs=fs))
    out = os.path.abspath(IMG.lstrip("/"))
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630", "--virtual-time-budget=3000",
                    "--screenshot=" + out, "file://" + tmp], capture_output=True)
    subprocess.run(["pngquant", "--quality=70-95", "--force", "--ext", ".png", out], capture_output=True)
    print("card", os.path.exists(out))


def main():
    if not os.path.exists(IMG.lstrip("/")):
        render_card()
    s = open(SRC, encoding="utf-8").read()
    s = re.sub(r"<!-- YOAST:.*?-->", "<!-- YOAST: Focus Keyword: living in indianapolis pros and cons | Category: Relocation -->", s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s, count=1)
    for prop, val in (("og:title", TITLE), ("og:description", DESC), ("og:url", URL), ("og:image", OG)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", DESC), ("twitter:title", TITLE), ("twitter:description", DESC), ("twitter:image", OG)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": HEADLINE, "description": DESC,
         "author": {"@type": "Person", "name": "Daniel Cope", "url": "https://yourrealtylink.com/agents/daniel-cope/", "jobTitle": "Real Estate Broker",
                    "worksFor": {"@type": "Organization", "name": "Your Realty Link"}},
         "publisher": {"@type": "Organization", "name": "Your Realty Link", "logo": {"@type": "ImageObject", "url": "/assets/img/yrl-logo.png"}},
         "image": OG, "datePublished": DATE, "dateModified": DATE, "mainEntityOfPage": URL,
         "about": {"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}}},
        {"@type": "WebPage", "url": URL, "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"]}},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yourrealtylink.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": HEADLINE, "item": URL}]}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    assert len(blocks) >= 2
    new = ['<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n</script>',
           '<script type="application/ld+json">\n' + json.dumps(faqld, indent=1, ensure_ascii=False) + '\n</script>']
    for m, rep in reversed(list(zip(blocks[:2], new))):
        s = s[:m.start()] + rep + s[m.end():]
    for m in reversed(blocks[2:]):
        s = s[:m.start()] + s[m.end():]
    s = re.sub(r"(<span>&rsaquo;</span>\s*)Moving to Indianapolis Relocation Guide(\s*</div>\s*</nav>)", r"\1Living in Indianapolis: Pros and Cons\2", s, count=1)
    s = re.sub(r"<h1>.*?</h1>", "<h1>Living in Indianapolis: <em>The Real Pros and Cons</em></h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) +
               "Cost of living, taxes, weather, commute and jobs, with real numbers, plus the downsides worth knowing before you move." + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<div class="hero-badges">.*?</div>', '<div class="hero-badges">\n <span class="hero-badge">Relocation</span>\n'
               ' <span class="hero-badge">Updated for 2026</span>\n <span class="hero-badge">Indianapolis</span>\n </div>', s, count=1, flags=re.S)
    s = re.sub(r"Updated [A-Z][a-z]+ 2026</p>", "Updated November 2026</p>", s, count=1)
    s = re.sub(r'<div class="post-meta">.*?</div>', '<div class="post-meta">\n <span class="category-badge">Relocation</span>\n <span>November 2026</span>\n'
               ' <span>By Daniel Cope, Real Estate Broker &mdash; Your Realty Link</span>\n <span>~8 min read</span>\n </div>', s, count=1, flags=re.S)
    faq = "\n".join(f' <details class="faq-item">\n <summary>{html.escape(q, quote=False)}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in FAQS)
    i = s.index("</div>", s.index('<div class="post-meta">')) + len("</div>")
    j = s.index("<!-- CTA -->")
    s = s[:i] + "\n" + BODY.replace("__FAQ__", faq) + s[j:]
    toc = "\n".join(f' <li><a href="#{a}">{l}</a></li>' for a, l in TOC)
    s = re.sub(r'(<div class="toc">\s*<h4>In This Article</h4>\s*<ol>).*?(</ol>)', lambda m: m.group(1) + "\n" + toc + "\n " + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<div class="sidebar-card-header">Related Posts</div>\s*<div class="sidebar-card-body">\s*<ul class="contact-list">).*?(</ul>)', lambda m: m.group(1) + """
 <li><a href="/blog/moving-to-indianapolis-relocation-guide/">Moving to Indianapolis: Relocation Guide</a></li>
 <li><a href="/best/indianapolis-suburbs-for-families/">Best Indianapolis Suburbs for Families</a></li>
 <li><a href="/blog/indianapolis-market-update-october-2026/">Indianapolis Market Update</a></li>
 """ + m.group(2), s, count=1, flags=re.S)
    os.makedirs(f"blog/{SLUG}", exist_ok=True)
    open(f"blog/{SLUG}/index.html", "w", encoding="utf-8").write(s)
    print("built", SLUG)

    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL not in sm:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>",
             f" <url>\n <loc>{URL}</loc>\n <lastmod>{DATE}</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.8</priority>\n </url>\n</urlset>"))
    bi = open("blog/index.html", encoding="utf-8").read()
    if f"/blog/{SLUG}/" not in bi:
        m = re.search(r'\n( *)<div class="blog-card">\s*<div class="blog-card-img">', bi)
        ind = m.group(1)
        card = (f'\n{ind}<div class="blog-card">\n <div class="blog-card-img"><img src="{IMG}" alt="living in indianapolis pros and cons" loading="lazy"></div>\n'
                f' <div class="blog-card-body">\n <div class="blog-card-cat">Relocation</div>\n <h3>{html.escape(HEADLINE, quote=False)}</h3>\n'
                f' <p>{DESC}</p>\n <a href="/blog/{SLUG}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
        open("blog/index.html", "w", encoding="utf-8").write(bi[:m.start()] + card + bi[m.start():])
        print("blog index card added")
    # link from the relocation guide and the relocation service page
    for p, anchor in (("blog/moving-to-indianapolis-relocation-guide/index.html", " <!-- FAQ -->"),
                      ("services/relocation-buyers/index.html", None)):
        t = open(p, encoding="utf-8").read()
        if f"/blog/{SLUG}/" in t:
            continue
        note = (f' <p><strong>Still deciding?</strong> Read our honest look at <a href="/blog/{SLUG}/">the pros and cons of living in Indianapolis</a>, '
                f'with cost of living, taxes, weather and commute numbers.</p>\n\n ')
        if anchor and anchor in t:
            t = t.replace(anchor, note + anchor.strip(), 1)
        elif "<!-- CTA -->" in t:
            t = t.replace("<!-- CTA -->", note + "<!-- CTA -->", 1)
        else:
            mm = re.search(r"<h2[^>]*>Frequently Asked Questions", t)
            if not mm:
                print("  no anchor in", p); continue
            t = t[:mm.start()] + note + t[mm.start():]
        open(p, "w", encoding="utf-8").write(t)
        print("linked from", p)


if __name__ == "__main__":
    main()
