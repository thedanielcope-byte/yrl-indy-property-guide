#!/usr/bin/env python3
"""Build /blog/housemaster-heartland-home-inspector-indianapolis/ (Dan's request, Oct 26 2026).

Vendor spotlight for our preferred home inspector, HouseMaster Serving Heartland, written as a
useful inspection guide. Facts only from their own pages (housemaster.com/heartland and
/heartland/our-team, read Oct 26 2026): locally owned HouseMaster franchise in Avon, owners
Trent Paino and Tim Paino, service area (Indianapolis, Carmel, Bloomington and dozens of nearby
towns), service and add-on list, "Limited Repair Reimbursement Guarantee", office (317) 209-9100.
The four "why we recommend them" points are their own stated commitments (their Oct 2026 agent
email). Radon guidance: Indiana Department of Health radon brochure. No prices, no ratings, no
compensation claims. Shell = home-inspections-appraisals post. Re-runnable.
"""
import html, json, os, re

SRC = "blog/home-inspections-appraisals-indianapolis/index.html"
SLUG = "housemaster-heartland-home-inspector-indianapolis"
URL = f"https://yourrealtylink.com/blog/{SLUG}/"
TITLE = "Home Inspector in Indianapolis: Why We Recommend HouseMaster"
HEADLINE = "Our Preferred Home Inspector: HouseMaster Serving Heartland"
DESC = ("Why Your Realty Link recommends HouseMaster Heartland for home inspections in Indianapolis "
        "and Central Indiana: services, add-on tests and how to book.")
IMG = "/assets/img/blog/housemaster-heartland-home-inspector-indianapolis.png"
OG = "https://yourrealtylink.com" + IMG
HM = "https://housemaster.com/heartland"
PLA = "https://mylicense.in.gov/everification/"
IDOH = "https://secure.in.gov/health/leadsafe/files/26_Radon_short-brochure_July-2023_UpdatFeb26_English.pdf"
DATE = "2026-10-26"

FAQS = [
 ("Who is Your Realty Link's preferred home inspector?",
  "One of our preferred inspectors is HouseMaster Serving Heartland, a locally owned HouseMaster franchise based in Avon that serves Indianapolis and the surrounding Central Indiana communities. Their office number is (317) 209-9100."),
 ("Do I have to use the home inspector my agent recommends?",
  "No. You can hire any licensed Indiana home inspector. We share recommendations because clients ask for them, and you can verify any inspector's license through the Indiana Professional Licensing Agency."),
 ("How much does a home inspection cost?",
  "It depends on the home's size, age and type, plus any add-ons such as radon screening or sewer scoping. Ask the inspector for a quote when you book."),
 ("Should I test for radon when buying a home in Indiana?",
  "The Indiana Department of Health recommends that Indiana residents test their homes for radon, and the EPA's action level is 4 pCi/L. Adding a radon test during your inspection period gives you time to negotiate mitigation if levels come back high."),
]

TOC = [("who", "Who HouseMaster Heartland Is"), ("why", "Why We Recommend Them"), ("services", "Inspections They Offer"),
       ("add-ons", "Add-On Tests Worth Considering"), ("sellers", "For Sellers"), ("contract", "How It Fits Your Purchase"),
       ("choosing", "Choosing Your Inspector"), ("book", "How to Book"), ("faq", "FAQ")]

BODY = f"""
 <p>Ask buyers which week of a purchase is the most stressful, and many will point to the inspection. A good inspector makes that week calmer: they find what matters, explain it clearly and get the report to you fast enough to act within your inspection period. Clients ask us all the time who we recommend. One of our preferred home inspectors is <strong>HouseMaster Serving Heartland</strong>. Here&rsquo;s why, what they offer and how to book.</p>

 <h2 id="who">Who HouseMaster Heartland Is</h2>
 <p>HouseMaster Serving Heartland is a locally owned and operated HouseMaster franchise based in Avon, run by owners Trent Paino and Tim Paino. HouseMaster, part of the Neighborly family of home service brands, has been in the home inspection business since the 1970s. The Heartland office serves Indianapolis, Carmel and Bloomington plus dozens of surrounding communities, including Fishers, Noblesville, Westfield, Zionsville, Avon, Brownsburg, Plainfield and Greenwood.</p>

 <h2 id="why">Why We Recommend Them</h2>
 <p>Once you&rsquo;re under contract, the clock is running. HouseMaster Heartland focuses on the things that keep a purchase on track:</p>
 <ul>
 <li><strong>Easy scheduling,</strong> including last-minute inspections when timelines get tight.</li>
 <li><strong>Clear, easy-to-read reports,</strong> delivered quickly, so you know what matters and what comes next.</li>
 <li><strong>Client education.</strong> They walk buyers through findings calmly, which helps separate real problems from normal wear and tear.</li>
 <li><strong>Thorough, straightforward inspections</strong> that keep the deal moving without unnecessary friction.</li>
 </ul>
 <p>Their inspections are also backed by HouseMaster&rsquo;s Limited Repair Reimbursement Guarantee. Ask them for the details and terms when you book.</p>

 <h2 id="services">Inspections They Offer</h2>
 <ul>
 <li><strong>Buyer home inspections</strong> during your inspection period.</li>
 <li><strong>New construction inspections.</strong> An independent inspector works for you, not the builder, and can catch items to fix before closing. See our <a href="/services/new-construction/">new construction guide</a>.</li>
 <li><strong>Pre-listing inspections</strong> for sellers who want to find issues before buyers do.</li>
 <li><strong>Maintenance and post-close inspections</strong> for current homeowners.</li>
 <li><strong>Commercial and multi-unit inspections</strong> for investors and business owners.</li>
 </ul>

 <h2 id="add-ons">Add-On Tests Worth Considering in Central Indiana</h2>
 <p>A standard <a href="/glossary/home-inspection/">home inspection</a> covers the home&rsquo;s visible systems and structure. Depending on the property, these add-ons can be worth it:</p>
 <ul>
 <li><strong>Radon screening.</strong> The Indiana Department of Health recommends that Indiana residents test their homes for radon, and the EPA&rsquo;s action level is 4 pCi/L. Testing during your inspection period leaves time to negotiate a mitigation system if levels are high.</li>
 <li><strong>Sewer scoping.</strong> A camera inspection of the sewer line can reveal root intrusion, breaks or sags. It&rsquo;s worth considering on older homes and lots with mature trees.</li>
 <li><strong>WDI/WDO (wood-destroying insect) inspection.</strong> Some lenders and loan programs require one, so ask your lender early.</li>
 <li><strong>Septic inspection and water quality sampling</strong> for rural homes on a septic system or private well. See our guide to <a href="/blog/buying-a-rural-home-central-indiana-radon-wells-septic/">buying a rural home in Central Indiana</a>.</li>
 <li><strong>Air quality and mold testing, thermal imaging and pool or spa inspections</strong> when the home calls for them.</li>
 </ul>

 <h2 id="sellers">For Sellers: A Pre-Listing Inspection</h2>
 <p>A pre-listing inspection shows you what a buyer&rsquo;s inspector is likely to find before you&rsquo;re under contract. You can make repairs on your own schedule, gather quotes, or price with known issues in mind, which means fewer surprises and renegotiations later. Our <a href="/services/home-selling-process/">home selling process</a> walks through how it fits into getting ready to list.</p>

 <h2 id="contract">How the Inspection Fits Into Your Purchase</h2>
 <p>In Indiana, the inspection usually happens during an inspection period written into your purchase agreement. That window is negotiated in each contract, so line up your inspector as soon as your offer is accepted. After the report comes back, you and your agent decide whether to move forward as is, ask for repairs or credits, or, if the contract allows, walk away. Our guide to <a href="/blog/home-inspection-under-contract-what-to-expect-indianapolis/">what to expect from a home inspection under contract</a> and the glossary entry on <a href="/glossary/inspection-contingency/">inspection contingencies</a> cover the details.</p>

 <h2 id="choosing">You&rsquo;re Always Free to Choose Your Inspector</h2>
 <p>We share recommendations because clients ask for them, but the choice is always yours. Indiana requires home inspectors to be licensed, and you can look up any inspector&rsquo;s license through the <a href="{PLA}" target="_blank" rel="noopener">Indiana Professional Licensing Agency</a>. For more options, see the home inspectors on our <a href="/vendors/">preferred vendors list</a>.</p>

 <h2 id="book">How to Book HouseMaster Heartland</h2>
 <p>Call their office at <a href="tel:3172099100">(317) 209-9100</a> or book online at <a href="{HM}" target="_blank" rel="noopener">housemaster.com/heartland</a>. If you&rsquo;re working with one of our agents, they&rsquo;ll help you time the inspection within your contract&rsquo;s inspection period.</p>

 <!-- FAQ -->
 <h2 id="faq">Frequently Asked Questions</h2>
__FAQ__

 <p style="font-size:.85rem;color:var(--gray);">Sources: <a href="{HM}" target="_blank" rel="noopener">HouseMaster Serving Heartland</a> &middot; <a href="{IDOH}" target="_blank" rel="noopener">Indiana Department of Health, radon brochure</a> &middot; <a href="{PLA}" target="_blank" rel="noopener">Indiana Professional Licensing Agency license lookup</a>.</p>

 """


def main():
    s = open(SRC, encoding="utf-8").read()
    s = re.sub(r"<!-- YOAST:.*?-->", "<!-- YOAST: Focus Keyword: home inspector indianapolis | Category: Buying a Home -->", s, count=1)
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
         "mentions": {"@type": "LocalBusiness", "name": "HouseMaster Serving Heartland", "url": HM, "telephone": "+1-317-209-9100",
                      "address": {"@type": "PostalAddress", "addressLocality": "Avon", "addressRegion": "IN", "postalCode": "46123"}}},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yourrealtylink.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": HEADLINE, "item": URL}]}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    assert len(blocks) >= 2, len(blocks)
    new = ['<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n</script>',
           '<script type="application/ld+json">\n' + json.dumps(faqld, indent=1, ensure_ascii=False) + '\n</script>']
    for m, rep in reversed(list(zip(blocks[:2], new))):
        s = s[:m.start()] + rep + s[m.end():]
    for m in reversed(blocks[2:]):          # any extra template blocks (old Speakable etc.)
        s = s[:m.start()] + s[m.end():]

    s = re.sub(r"(<span>&rsaquo;</span>\s*)Home Inspections &amp; Appraisals(\s*</div>\s*</nav>)", r"\1Our Preferred Home Inspector\2", s, count=1)
    s = re.sub(r"<h1>.*?</h1>", "<h1>Our Preferred Home Inspector: <em>HouseMaster Serving Heartland</em></h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) +
               "A locally owned inspection company based in Avon, serving Indianapolis and the surrounding communities. What they offer, and how an inspection fits into your purchase." + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<div class="hero-badges">.*?</div>', '<div class="hero-badges">\n <span class="hero-badge">Home Inspections</span>\n'
               ' <span class="hero-badge">Preferred Vendor</span>\n <span class="hero-badge">Central Indiana</span>\n </div>', s, count=1, flags=re.S)
    s = re.sub(r"Updated [A-Z][a-z]+ 2026</p>", "Updated October 2026</p>", s, count=1)
    s = re.sub(r'<div class="post-meta">.*?</div>', '<div class="post-meta">\n <span class="category-badge">Buying a Home</span>\n <span>October 2026</span>\n'
               ' <span>By Daniel Cope, Real Estate Broker &mdash; Your Realty Link</span>\n <span>~5 min read</span>\n </div>', s, count=1, flags=re.S)
    faq = "\n".join(f' <details class="faq-item">\n <summary>{html.escape(q, quote=False)}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in FAQS)
    i = s.index("</div>", s.index('<div class="post-meta">')) + len("</div>")
    j = s.index("<!-- CTA -->")
    s = s[:i] + "\n" + BODY.replace("__FAQ__", faq) + s[j:]
    toc = "\n".join(f' <li><a href="#{a}">{l}</a></li>' for a, l in TOC)
    s = re.sub(r'(<div class="toc">\s*<h4>In This Article</h4>\s*<ol>).*?(</ol>)', lambda m: m.group(1) + "\n" + toc + "\n " + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<div class="sidebar-card-header">Related Posts</div>\s*<div class="sidebar-card-body">\s*<ul class="contact-list">).*?(</ul>)', lambda m: m.group(1) + """
 <li><a href="/blog/home-inspection-under-contract-what-to-expect-indianapolis/">Home Inspection Under Contract</a></li>
 <li><a href="/blog/home-inspection-red-flags-indianapolis/">Home Inspection Red Flags</a></li>
 <li><a href="/blog/home-inspections-appraisals-indianapolis/">Home Inspections &amp; Appraisals</a></li>
 """ + m.group(2), s, count=1, flags=re.S)
    os.makedirs(f"blog/{SLUG}", exist_ok=True)
    open(f"blog/{SLUG}/index.html", "w", encoding="utf-8").write(s)
    print("built", SLUG)

    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL not in sm:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>",
             f" <url>\n <loc>{URL}</loc>\n <lastmod>{DATE}</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.7</priority>\n </url>\n</urlset>"))
    bi = open("blog/index.html", encoding="utf-8").read()
    if f"/blog/{SLUG}/" not in bi:
        m = re.search(r'\n( *)<div class="blog-card">\s*<div class="blog-card-img">', bi)
        ind = m.group(1)
        card = (f'\n{ind}<div class="blog-card">\n <div class="blog-card-img"><img src="{IMG}" alt="home inspector indianapolis" loading="lazy"></div>\n'
                f' <div class="blog-card-body">\n <div class="blog-card-cat">Buying a Home</div>\n <h3>{html.escape(HEADLINE, quote=False)}</h3>\n'
                f' <p>{DESC}</p>\n <a href="/blog/{SLUG}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
        open("blog/index.html", "w", encoding="utf-8").write(bi[:m.start()] + card + bi[m.start():])
        print("blog index card added")
    for p in ("blog/home-inspection-under-contract-what-to-expect-indianapolis/index.html",
              "blog/home-inspections-appraisals-indianapolis/index.html",
              "blog/home-inspection-red-flags-indianapolis/index.html"):
        t = open(p, encoding="utf-8").read()
        if f"/blog/{SLUG}/" in t or "<!-- CTA -->" not in t:
            continue
        note = (f' <p><strong>Need an inspector?</strong> Meet <a href="/blog/{SLUG}/">our preferred home inspector, HouseMaster Serving Heartland</a>, '
                f'or browse the inspectors on our <a href="/vendors/">preferred vendors list</a>.</p>\n\n ')
        t = t.replace(" <!-- FAQ -->", note + "<!-- FAQ -->", 1) if " <!-- FAQ -->" in t else t.replace("<!-- CTA -->", note + "<!-- CTA -->", 1)
        open(p, "w", encoding="utf-8").write(t)
        print("linked from", p)


if __name__ == "__main__":
    main()
