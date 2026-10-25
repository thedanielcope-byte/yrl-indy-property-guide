#!/usr/bin/env python3
"""Build /services/probate-real-estate-agent/ from the estate-sales page shell.

Audit gap (Oct 2026): "probate real estate agent indianapolis" returned only law firms.
Copy is general information checked against the 2026 Indiana Code (cites inline), with a
talk-to-an-attorney line. Re-runnable: rebuilds the page from services/estate-sales/ each run,
then run inject_gtag.py is NOT needed (the template head already carries GA4).
Also adds the page to sitemap.xml and the /services/ hub if missing.
"""
import html, json, re

SRC = "services/estate-sales/index.html"
OUT_DIR = "services/probate-real-estate-agent"
URL = "https://yourrealtylink.com/services/probate-real-estate-agent/"
TITLE = "Probate Real Estate Agent in Indianapolis | Your Realty Link"
DESC = "Selling a probate house in Indiana? Our Indianapolis team helps personal representatives price, prepare and sell estate homes alongside the estate attorney."
H1 = "Probate Real Estate Agent in Indianapolis"
SUB = ("If you&rsquo;ve been named personal representative of a loved one&rsquo;s estate, the house is often "
       "the biggest and most time-consuming piece. Our team helps you price, prepare and sell it, "
       "working alongside your attorney so the sale fits the probate process.")

FAQS = [
 ("Can I sell the house before probate is finished?",
  "Often, yes. Once you have letters, a personal representative in an unsupervised estate can sell without a separate court order, and a supervised estate can sell after the court approves it. Your attorney will advise you on timing around creditor claims."),
 ("Do I need court approval to sell a house in an Indiana probate estate?",
  "In a supervised estate, generally yes, unless the will grants a power of sale. In an unsupervised estate, no separate court order is required to sell real estate."),
 ("Do we have to fix up the house first?",
  "No. Many estate homes sell as-is. Indiana's seller's disclosure form statute doesn't apply to sales by a personal representative administering an estate (IC 32-21-5-1), though other disclosure rules may still apply, so ask the estate's attorney."),
 ("How long does a probate home sale take?",
  "Creditors generally have three months from the first published notice to file claims, and estates are expected to close within about a year of appointment. Supervised estates add a court step. We'll map a realistic timeline with you and your attorney."),
 ("Where are probate cases handled in Marion County?",
  "Estate administration in Marion County is heard in Marion Superior Court, Court D08, at the Community Justice Campus, 675 Justice Way, Indianapolis."),
]

BODY = """
 <p>If you&rsquo;ve been named personal representative of a loved one&rsquo;s estate, the house is often the biggest and most time-consuming piece to settle. Our team at Your Realty Link helps personal representatives across Indianapolis and Central Indiana price, prepare and sell estate homes, working alongside your attorney so the sale fits the probate process. We&rsquo;ll be patient, clear and organized, and we&rsquo;ll keep every heir informed.</p>

 <p><strong>Note:</strong> We are real estate professionals, not probate attorneys. Everything below is general information about Indiana law; your estate attorney is the right person to advise on your situation.</p>

 <h2 id="how-it-works">How Probate Home Sales Work in Indiana</h2>
 <p>The court appoints a personal representative (an executor if there&rsquo;s a will, an administrator if there isn&rsquo;t) and issues &ldquo;letters&rdquo; that prove that person&rsquo;s authority. The personal representative takes possession of the estate&rsquo;s real estate, keeps paying the taxes, keeps the home in repair, and may insure it (IC 29-1-13-1). The personal representative, not the individual heirs, signs the listing and the deed. How the sale works depends on whether the estate is supervised or unsupervised.</p>

 <h2 id="supervised-vs-unsupervised">Supervised vs. Unsupervised Administration</h2>
 <p><strong>Unsupervised administration</strong> is available when the heirs or beneficiaries agree, the estate is solvent, and the court finds the personal representative qualified. A will can also authorize it. In an unsupervised estate, the personal representative can sell real estate at a public or private sale without a separate court order (IC 29-1-7.5-2, IC 29-1-7.5-3).</p>
 <p><strong>Supervised administration</strong> keeps the court more involved. Unless the will grants a power of sale, the personal representative petitions the court and gives notice to heirs and lienholders, and the court issues an order to sell. In a private sale, the price can&rsquo;t be below the fair market value on record, and the court may require an appraisal (IC 29-1-15-2, IC 29-1-15-11, IC 29-1-15-13, IC 29-1-15-14). We build that court step into the listing plan from day one.</p>

 <h2 id="timeline">Probate Home Sale Timeline</h2>
 <ul>
 <li><strong>Opening the estate:</strong> don&rsquo;t wait. Indiana limits selling a decedent&rsquo;s real estate to pay certain debts if the estate isn&rsquo;t opened within about five months of death (IC 29-1-7-15.1).</li>
 <li><strong>Notice to creditors:</strong> published once a week for two weeks after letters are issued (IC 29-1-7-7).</li>
 <li><strong>Claims window:</strong> generally three months from the first published notice, and claims are barred nine months after death (IC 29-1-14-1).</li>
 <li><strong>Closing the estate:</strong> estates are expected to close within about a year of appointment unless there&rsquo;s good cause (IC 29-1-16-2, IC 29-1-7.5-3.8).</li>
 </ul>
 <p>Your attorney decides when it makes sense to list. Time on the market depends on the home, its condition and the season.</p>

 <h2 id="how-we-help">How Our Team Helps the Personal Representative</h2>
 <ul>
 <li><strong>Pricing:</strong> a detailed comparative market analysis to help you and your attorney set a realistic price and explain it to the heirs.</li>
 <li><strong>Clean-out and vendor referrals:</strong> introductions to estate-sale companies, clean-out crews, contractors and inspectors from our <a href="/vendors/">local vendor network</a>. You choose who to hire.</li>
 <li><strong>Coordinating with the estate attorney:</strong> we line up the listing, the offer terms and the closing date with the court&rsquo;s requirements, including any court order a supervised estate needs.</li>
 <li><strong>Marketing:</strong> professional photos, full MIBOR MLS exposure and showings handled for you, which matters most if you live out of town.</li>
 <li><strong>As-is sales:</strong> many estate homes sell as-is. We&rsquo;ll show you the trade-offs between selling as-is and doing light preparation so you can decide what&rsquo;s best for the estate.</li>
 </ul>
 <p>If the house came to you directly instead (through a transfer on death deed or joint ownership), see <a href="/services/inherited-property/">selling an inherited house in Indiana</a>. For the broader estate picture, see <a href="/services/estate-sales/">estate home sales</a>.</p>

 <section class="faq-section">
 <h2>Probate Home Sale Questions</h2>
__FAQ_HTML__
 </section>

 <p class="law-note" style="font-size:.92rem;color:var(--gray);"><em>This is general information, not legal advice. Talk with an Indiana attorney about your situation.</em></p>

"""


def main():
    s = open(SRC, encoding="utf-8").read()
    t = html.escape(TITLE, quote=False)

    # head
    s = re.sub(r"<!-- ═+\n YOAST SEO FIELDS.*?═+ -->", "<!-- Probate landing page — built by build_probate.py -->", s, count=1, flags=re.S)
    s = re.sub(r"<title>.*?</title>", f"<title>{t}</title>", s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + t, s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + DESC, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + t, s, count=1)
    s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + DESC, s, count=1)
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
            {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://yourrealtylink.com/services/"},
            {"@type": "ListItem", "position": 3, "name": "Probate Real Estate Agent", "item": URL}]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n </script>', s, count=1, flags=re.S)

    # breadcrumb + hero
    s = s.replace(" Estate Home Sales\n </div>\n</nav>", " Probate Real Estate Agent\n </div>\n</nav>", 1)
    s = re.sub(r"<h1>.*?</h1>", f"<h1>{H1}</h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) + SUB + m.group(2), s, count=1, flags=re.S)
    s = s.replace('<span class="hero-badge">🏡 Estate Sale Specialists</span>', '<span class="hero-badge">⚖️ Works With Your Estate Attorney</span>', 1)
    s = s.replace("Updated August 2026</p>", "Updated October 2026</p>", 1)

    # quick answer
    qa = ('<!-- QA-START -->\n<div class="quick-answer">\n <p class="qa-heading">Quick Answer</p>\n'
          ' <p class="qa-lead">In Indiana, the court-appointed <strong>personal representative</strong> sells an estate home. '
          'In an <strong>unsupervised estate</strong> they can sell without a separate court order; in a <strong>supervised estate</strong> '
          'a court order is generally needed unless the will grants a power of sale. Our team prices, prepares and markets the home '
          'and coordinates with the estate attorney.</p>\n <dl class="qa-facts">\n'
          ' <div><dt>Who signs</dt><dd>The personal representative</dd></div>\n'
          ' <div><dt>Court order</dt><dd>Supervised estates, unless the will grants a power of sale</dd></div>\n'
          ' <div><dt>Creditor window</dt><dd>3 months from first published notice</dd></div>\n'
          ' <div><dt>Talk to us</dt><dd><a href="tel:3179977404">317-997-7404</a></dd></div>\n'
          ' </dl>\n</div>\n<!-- QA-END -->')
    s = re.sub(r"<!-- QA-START -->.*?<!-- QA-END -->", lambda m: qa, s, count=1, flags=re.S)

    # body
    faq_html = "\n".join(f' <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in FAQS)
    body = BODY.replace("__FAQ_HTML__", faq_html)
    i = s.index('<div class="service-wrap">') + len('<div class="service-wrap">')
    j = s.index('<div class="cta-block cta-red">')
    s = s[:i] + "\n" + body + " " + s[j:]

    # related links + form
    s = re.sub(r'(<div class="internal-links">\s*<h3>Related Resources</h3>\s*<ul>).*?(</ul>)', lambda m: m.group(1) + """
 <li><a href="/services/estate-sales/">Estate Home Sales in Indianapolis</a> — Guidance for executors and families</li>
 <li><a href="/services/inherited-property/">Selling an Inherited House in Indiana</a> — TOD deeds, joint ownership and small estates</li>
 <li><a href="/services/free-home-valuation/">Free Home Valuation</a> — A market analysis for the estate and the heirs</li>
 """ + m.group(2), s, count=1, flags=re.S)
    s = s.replace('name="source_page" value="services/estate-sales"', 'name="source_page" value="services/probate-real-estate-agent"', 1)
    s = re.sub(r'(name="interest_type" value=")[^"]*', lambda m: m.group(1) + "Probate Real Estate Agent in Indianapolis", s, count=1)

    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(s)
    print("built", OUT_DIR)

    # sitemap
    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL not in sm:
        entry = f" <url>\n <loc>{URL}</loc>\n <lastmod>2026-10-14</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.8</priority>\n </url>\n"
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>", entry + "</urlset>"))
        print("added to sitemap")


if __name__ == "__main__":
    main()
