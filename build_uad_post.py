#!/usr/bin/env python3
"""Build /blog/uad-3-6-appraisal-changes-indiana/ (requested by Janet, Oct 19 2026).

Facts from: Fannie Mae/Freddie Mac UMDP notice "Available Now in Broad Production: UAD 3.6 and
Forms Redesign" (Jan 26, 2026) — Nov 2, 2026 mandate for all appraisal reports on loans sold to
the GSEs; NAR REALTOR News "Appraisal Ready: What Agents and Brokers Can Do Now for UAD 3.6"
(Sept 22, 2026) — conventional loans, FHA adopting with no mandatory date, longer appraisals,
agent prep steps, facts-not-value. Lender tip credited to Melissa Lutes (Ruoff Mortgage), who is
on our preferred-lenders page. Shell = what-hurts-a-home-appraisal post. Re-runnable; then run
inject_ai_answer.py (entry in ai-answers.json) for the Quick Answer + Speakable block.
"""
import html, json, os, re

SRC = "blog/what-hurts-a-home-appraisal-in-indiana/index.html"
SLUG = "uad-3-6-appraisal-changes-indiana"
URL = f"https://yourrealtylink.com/blog/{SLUG}/"
TITLE = "UAD 3.6 Appraisal Changes: What to Know in Indiana"
HEADLINE = "UAD 3.6: What the New Appraisal Report Means for Indiana Buyers and Sellers"
DESC = ("Starting Nov. 2, 2026, appraisals on conventional loans use the new UAD 3.6 report. "
        "What changes, what doesn't, and how Indiana buyers and sellers can prepare.")
OG = "https://yourrealtylink.com/assets/img/og-default.png"
NAR = "https://www.nar.realtor/news/real-estate-news/appraisal-ready-what-agents-and-brokers-can-do-now-for-uad-3-6"
GSE = "https://sf.freddiemac.com/docs/pdf/announcement_uad_january-2026.pdf"
FRE = "https://sf.freddiemac.com/tools-learning/uniform-mortgage-data-program/uad"

FAQS = [
 ("When does UAD 3.6 take effect?",
  "November 2, 2026. From that date, Fannie Mae and Freddie Mac require all appraisal reports on loans sold to them to use UAD 3.6. Lenders have been allowed to use it since January 26, 2026."),
 ("Will UAD 3.6 change my home's appraised value?",
  "No. UAD 3.6 changes how property information is collected and reported, not how value is determined. The appraiser still forms an independent opinion of value, and more detail doesn't automatically mean a higher number."),
 ("Does UAD 3.6 apply to FHA and VA loans?",
  "The November 2 requirement is for conventional loans sold to Fannie Mae and Freddie Mac. As of September 2026, FHA had announced it is adopting UAD 3.6 but had not set a mandatory date, and VA and USDA timelines shouldn't be assumed. Ask your lender which format they're ordering."),
 ("How can sellers prepare for a UAD 3.6 appraisal?",
  "Have a dated list of updates ready (for example, roof replaced 2021), plus records for systems and any finished or unfinished areas, and allow time for a longer appraisal visit. Share facts through your agent or the lender's process, never value suggestions."),
]

TOC = [("what-is-uad", "What UAD 3.6 Is"), ("what-doesnt-change", "What Doesn't Change"), ("which-loans", "Which Loans It Affects"),
       ("sellers", "For Sellers"), ("buyers", "For Buyers"), ("our-team", "How Our Team Prepares"), ("faq", "FAQ")]

BODY = f"""
 <p>Starting <strong>November 2, 2026</strong>, the appraisal on most conventional mortgages looks different. Fannie Mae and Freddie Mac now require all appraisal reports on loans sold to them to use <strong>UAD 3.6</strong>, the updated Uniform Appraisal Dataset and redesigned appraisal report. It&rsquo;s one of the biggest changes to residential appraisal reporting in years. Here&rsquo;s what it means for buyers and sellers in Indianapolis and Central Indiana, and what to do now.</p>

 <h2 id="what-is-uad">What Is UAD 3.6?</h2>
 <p>UAD 3.6 is a more structured way for appraisers to report what they find. Instead of the separate forms appraisers have used for years, there&rsquo;s one redesigned report that adapts to the property and the assignment. It asks for considerably more detail: individual levels, rooms and areas, improvements, amenities and site features. Fannie Mae and Freddie Mac opened it to all lenders on January 26, 2026, and it becomes required on November 2, 2026.</p>

 <h2 id="what-doesnt-change">What Doesn&rsquo;t Change: How Value Is Decided</h2>
 <p>UAD 3.6 changes how property information is organized and reported. It does <strong>not</strong> change how a home is valued. The appraiser still makes an independent analysis and opinion of value, and a more detailed report doesn&rsquo;t automatically mean a higher (or lower) number. Agents, buyers and sellers can share facts about the home; they can&rsquo;t direct the appraiser toward a value.</p>

 <h2 id="which-loans">Which Loans It Affects</h2>
 <p>The November 2 requirement covers <strong>conventional loans sold to Fannie Mae and Freddie Mac</strong>, which is most conventional financing. Many lenders are already ordering UAD 3.6 reports. As of September 2026, FHA had announced it is adopting UAD 3.6 but hadn&rsquo;t set a mandatory date, and VA and USDA timelines shouldn&rsquo;t be assumed. The simplest step: ask your lender, &ldquo;Which appraisal report format are you ordering?&rdquo;</p>

 <h2 id="sellers">What It Means for Sellers</h2>
 <ul>
 <li><strong>Expect a longer appraisal visit.</strong> The appraiser has more to document. A longer visit doesn&rsquo;t signal a problem with your home.</li>
 <li><strong>Gather accurate property facts early:</strong> finished and unfinished living areas and any additional spaces, documented improvements, systems and site features.</li>
 <li><strong>Be specific and date your updates.</strong> &ldquo;Roof replaced 2021&rdquo; and &ldquo;HVAC replaced 2019&rdquo; are far more useful than &ldquo;updated.&rdquo;</li>
 <li><strong>Keep it factual.</strong> Property information belongs in the packet; value suggestions don&rsquo;t. Facts should go through your agent or the lender&rsquo;s approved process.</li>
 </ul>
 <p>Thinking about listing? Our <a href="/blog/what-hurts-a-home-appraisal-in-indiana/">guide to what hurts a home appraisal</a> covers the condition items that matter most.</p>

 <h2 id="buyers">What It Means for Buyers</h2>
 <ul>
 <li><strong>Plan for more time.</strong> The appraisal itself, plus the lender&rsquo;s review afterward, may take longer during the transition, so build reasonable time into your contract dates.</li>
 <li><strong>Talk to your lender early</strong> about timing and which report format they&rsquo;re using.</li>
 <li><strong>Don&rsquo;t plan around the fastest turnaround you&rsquo;ve heard of.</strong> Timing is less predictable while lenders and appraisers adjust.</li>
 </ul>
 <p>If an appraisal does come in under contract price, see <a href="/blog/what-to-do-when-your-appraisal-comes-in-low-indiana/">what to do when your appraisal comes in low</a>.</p>

 <h2 id="our-team">How Our Team Is Preparing</h2>
 <p>For every listing and purchase, our agents prepare a factual appraisal packet on the property and relevant sales (the less flattering facts included), record concessions, repairs and unusual circumstances in the MLS so they&rsquo;re preserved for future appraisals, return appraisers&rsquo; calls promptly, and build realistic timelines with your lender. Our thanks to Melissa Lutes, Senior Loan Officer at Ruoff Mortgage and one of our <a href="/services/preferred-lenders/">preferred lenders</a>, for helping our team prepare.</p>

 <!-- FAQ -->
 <h2 id="faq">Frequently Asked Questions</h2>
__FAQ__

 <p style="font-size:.85rem;color:var(--gray);">Sources: <a href="{GSE}" target="_blank" rel="noopener">Fannie Mae &amp; Freddie Mac, &ldquo;Available Now in Broad Production: UAD 3.6 and Forms Redesign&rdquo; (Jan. 26, 2026)</a> &middot; <a href="{NAR}" target="_blank" rel="noopener">NAR, &ldquo;Appraisal Ready: What Agents and Brokers Can Do Now for UAD 3.6&rdquo; (Sept. 22, 2026)</a> &middot; <a href="{FRE}" target="_blank" rel="noopener">Freddie Mac UAD resources</a>.</p>

 """


def main():
    s = open(SRC, encoding="utf-8").read()
    s = re.sub(r"<!-- YOAST:.*?-->", "<!-- YOAST: Focus Keyword: uad 3.6 appraisal | Category: Buying &amp; Selling -->", s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s, count=1)
    for prop, val in (("og:title", TITLE), ("og:description", DESC), ("og:url", URL), ("og:image", OG)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", DESC), ("twitter:title", TITLE), ("twitter:description", DESC), ("twitter:image", OG)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": HEADLINE, "description": DESC,
         "author": {"@type": "Person", "name": "Janet Giles-Schultz", "url": "https://yourrealtylink.com/agents/janet-giles/", "jobTitle": "Principal Broker",
                    "worksFor": {"@type": "Organization", "name": "Your Realty Link"}},
         "publisher": {"@type": "Organization", "name": "Your Realty Link", "logo": {"@type": "ImageObject", "url": "/assets/img/yrl-logo.png"}},
         "image": OG, "datePublished": "2026-10-19", "dateModified": "2026-10-19", "mainEntityOfPage": URL},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yourrealtylink.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": HEADLINE, "item": URL}]}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    # 1-2: Article graph + FAQ; 3rd (template's Speakable WebPage) is dropped — inject_ai_answer.py re-adds one for this URL
    for m in reversed(blocks[2:]):
        if '"speakable"' in m.group(0):
            s = s[:m.start()] + s[m.end():]
    new = ['<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n</script>',
           '<script type="application/ld+json">\n' + json.dumps(faqld, indent=1, ensure_ascii=False) + '\n</script>']
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    for m, rep in reversed(list(zip(blocks[:2], new))):
        s = s[:m.start()] + rep + s[m.end():]

    s = re.sub(r"(<span>&rsaquo;</span>\s*)What Hurts a Home Appraisal in Indiana(\s*</div>\s*</nav>)", r"\1UAD 3.6 Appraisal Changes\2", s, count=1)
    s = re.sub(r"<h1>.*?</h1>", "<h1>UAD 3.6: What the New Appraisal Report Means <em>for Indiana Buyers &amp; Sellers</em></h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) +
               "Starting November 2, 2026, appraisals on most conventional loans use a new, more detailed report. Here&rsquo;s what changes, what doesn&rsquo;t, and how to prepare." + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<div class="hero-badges">.*?</div>', '<div class="hero-badges">\n <span class="hero-badge">Appraisals</span>\n'
               ' <span class="hero-badge">Indianapolis &amp; Central Indiana</span>\n <span class="hero-badge">By Janet Giles-Schultz</span>\n </div>', s, count=1, flags=re.S)
    s = re.sub(r"Updated [A-Z][a-z]+ 2026</p>", "Updated October 2026</p>", s, count=1)
    s = re.sub(r'<div class="post-meta">.*?</div>', '<div class="post-meta">\n <span class="category-badge">Buying &amp; Selling</span>\n <span>October 2026</span>\n'
               ' <span>By Janet Giles-Schultz, Principal Broker &mdash; Your Realty Link</span>\n <span>~5 min read</span>\n </div>', s, count=1, flags=re.S)
    faq = "\n".join(f' <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in FAQS)
    i = s.index("</div>", s.index('<div class="post-meta">')) + len("</div>")
    j = s.index("<!-- CTA -->")
    s = s[:i] + "\n" + BODY.replace("__FAQ__", faq) + s[j:]
    toc = "\n".join(f' <li><a href="#{a}">{l}</a></li>' for a, l in TOC)
    s = re.sub(r'(<div class="toc">\s*<h4>In This Article</h4>\s*<ol>).*?(</ol>)', lambda m: m.group(1) + "\n" + toc + "\n " + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<div class="sidebar-card-header">Related Posts</div>\s*<div class="sidebar-card-body">\s*<ul class="contact-list">).*?(</ul>)', lambda m: m.group(1) + """
 <li><a href="/blog/what-hurts-a-home-appraisal-in-indiana/">What Hurts a Home Appraisal in Indiana</a></li>
 <li><a href="/blog/what-to-do-when-your-appraisal-comes-in-low-indiana/">When Your Appraisal Comes In Low</a></li>
 <li><a href="/blog/home-inspections-appraisals-indianapolis/">Home Inspections &amp; Appraisals in Indianapolis</a></li>
 """ + m.group(2), s, count=1, flags=re.S)
    os.makedirs(f"blog/{SLUG}", exist_ok=True)
    open(f"blog/{SLUG}/index.html", "w", encoding="utf-8").write(s)
    print("built", SLUG)

    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL not in sm:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>",
             f" <url>\n <loc>{URL}</loc>\n <lastmod>2026-10-19</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.7</priority>\n </url>\n</urlset>"))
    # blog index card — first card in the static grid
    bi = open("blog/index.html", encoding="utf-8").read()
    if f"/blog/{SLUG}/" not in bi:
        m = re.search(r'\n( *)<div class="blog-card">\s*<div class="blog-card-img">', bi)
        ind = m.group(1)
        card = (f'\n{ind}<div class="blog-card">\n <div class="blog-card-img"><img src="/assets/img/blog/what-hurts-a-home-appraisal-in-indiana.png" alt="uad 3.6 appraisal changes indiana" loading="lazy"></div>\n'
                f' <div class="blog-card-body">\n <div class="blog-card-cat">Buying &amp; Selling</div>\n <h3>{html.escape(HEADLINE, quote=False)}</h3>\n'
                f' <p>{DESC}</p>\n <a href="/blog/{SLUG}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
        open("blog/index.html", "w", encoding="utf-8").write(bi[:m.start()] + card + bi[m.start():])
        print("blog index card added")
    # link from the two related appraisal posts
    for p in ("blog/what-hurts-a-home-appraisal-in-indiana/index.html", "blog/what-to-do-when-your-appraisal-comes-in-low-indiana/index.html"):
        t = open(p, encoding="utf-8").read()
        if f"/blog/{SLUG}/" in t or "<!-- CTA -->" not in t:
            continue
        note = (f' <p><strong>New for 2026:</strong> appraisals on most conventional loans now use the UAD 3.6 report. '
                f'See <a href="/blog/{SLUG}/">what UAD 3.6 means for Indiana buyers and sellers</a>.</p>\n\n ')
        t = t.replace(" <!-- FAQ -->", note + "<!-- FAQ -->", 1) if " <!-- FAQ -->" in t else t.replace("<!-- CTA -->", note + "<!-- CTA -->", 1)
        open(p, "w", encoding="utf-8").write(t)
        print("linked from", p)


if __name__ == "__main__":
    main()
