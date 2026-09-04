#!/usr/bin/env python3
"""Build the buyer & seller closing-checklist pages:

  /services/buyer-closing-checklist/
  /services/seller-closing-checklist/

Interactive: each item is a checkbox whose state saves to localStorage, with a
progress bar, a Print button, and a Reset button. Content is modeled on the CFPB
mortgage-closing checklist but rewritten in Your Realty Link's warm, local
Indiana voice. Nothing legal/financial is fabricated — ranges + "confirm with
your lender/title company" throughout. Shell (fonts/header/footer/scripts) is
reused from a sibling service page so nav stays in sync.

    python3 build_closing_checklists.py
"""
import os, re, json
from local_essentials import block as local_essentials_block

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL  = os.path.join(ROOT, "services", "expired-listings", "index.html")

src = open(TPL, encoding="utf-8").read()
def grab(p):
    m = re.search(p, src, re.S)
    if not m: raise SystemExit("extract failed: " + p[:40])
    return m.group(0)
FONTS  = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">')
HEADER = grab(r'<header class="site-header">.*?</header>')
FOOTER = grab(r'<footer class="site-footer">.*?</footer>')
SCRIPTS = grab(r'<script>\nfunction toggleNav.*?</body>\n</html>')

def strip(t):
    return re.sub(r"<[^>]+>", "", t).replace("&amp;", "&").replace("&quot;", '"').replace("&mdash;", "—").replace("&ndash;", "–")

CSS = """
.ck-wrap { max-width: 830px; margin: 0 auto; padding: 22px 0 10px; }
.ck-progress { position: sticky; top: 62px; z-index: 6; background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px; margin: 0 0 20px; display: flex; align-items: center; gap: 14px; box-shadow: 0 5px 18px rgba(0,0,0,.06); }
.ck-bar { flex: 1; height: 10px; background: var(--light); border-radius: 6px; overflow: hidden; }
.ck-bar > span { display: block; height: 100%; width: 0; background: linear-gradient(90deg, #c03926, #e0573f); transition: width .3s ease; }
.ck-count { font-weight: 700; color: #13294a; font-size: .88rem; white-space: nowrap; }
.ck-actions { display: flex; gap: 8px; }
.ck-actions button { font: inherit; font-size: .8rem; font-weight: 600; padding: 8px 12px; border-radius: 8px; border: 1px solid var(--border); background: #fff; color: #13294a; cursor: pointer; }
.ck-actions button:hover { border-color: var(--red); color: var(--red); }
.ck-phase { background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 4px 24px 16px; margin: 16px 0; box-shadow: 0 4px 16px rgba(0,0,0,.04); }
.ck-phase > h2 { color: var(--red); font-size: 1.12rem; margin: 18px 0 3px; }
.ck-phase-intro { color: var(--mid); font-size: .9rem; margin: 0 0 8px; }
ul.ck-list { list-style: none; margin: 0; padding: 0; }
li.ck-item { border-top: 1px solid var(--border); padding: 12px 0; }
li.ck-item:first-child { border-top: none; }
.ck-item label { display: flex; gap: 11px; align-items: flex-start; cursor: pointer; font-weight: 600; color: #1a1a1a; line-height: 1.45; }
.ck-item input { margin-top: 2px; width: 19px; height: 19px; accent-color: var(--red); flex-shrink: 0; cursor: pointer; }
.ck-item input:checked ~ .ck-label { color: #9ca3af; text-decoration: line-through; }
.ck-help { margin: 5px 0 0 30px; color: var(--mid); font-size: .86rem; line-height: 1.55; }
.ck-help a { color: var(--red); font-weight: 600; }
.ck-alert { background: #fff5f3; border: 1px solid #f3c9c0; border-left: 4px solid var(--red); border-radius: 10px; padding: 16px 20px; margin: 20px 0; }
.ck-alert h3 { margin: 0 0 6px; color: var(--red); font-size: 1.02rem; }
.ck-alert p { margin: 0; font-size: .9rem; color: #33373b; line-height: 1.6; }
.ck-cross { background: var(--light); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin: 22px 0; font-size: .92rem; }
.ck-cross strong { color: #13294a; }
.ck-pdfcta { margin: 0 0 14px; font-weight: 600; font-size: .95rem; }
.ck-pdfcta a { color: var(--red); }
@media print { .ck-pdfcta { display: none !important; } }
@media print {
  .site-header, .breadcrumbs, .page-hero, .ck-actions, .cta-block, .cta-form-section, .site-footer, .ck-progress, .quick-answer, .faq-section { display: none !important; }
  .ck-phase { box-shadow: none; border: 1px solid #ccc; break-inside: avoid; }
}
@media (max-width: 560px) { .ck-progress { position: static; flex-wrap: wrap; } }
"""

PROGRESS = ('<div class="ck-progress">\n'
            ' <div class="ck-bar"><span id="ckBar"></span></div>\n'
            ' <span class="ck-count" id="ckCount">0 done</span>\n'
            ' <div class="ck-actions"><button id="ckPrint" type="button">🖨 Print</button>'
            '<button id="ckReset" type="button">Reset</button></div>\n'
            '</div>')

CK_JS = """
<script>
(function(){
 var boxes=[].slice.call(document.querySelectorAll('.ck-item input[type=checkbox]'));
 var bar=document.getElementById('ckBar'), cnt=document.getElementById('ckCount');
 var KEY='ckl:'+location.pathname, saved={};
 try{ saved=JSON.parse(localStorage.getItem(KEY)||'{}'); }catch(e){}
 boxes.forEach(function(b,i){ if(saved[i]) b.checked=true; b.addEventListener('change',function(){ update(); save(); }); });
 function save(){ var o={}; boxes.forEach(function(b,i){ if(b.checked)o[i]=1; }); try{ localStorage.setItem(KEY,JSON.stringify(o)); }catch(e){} }
 function update(){ var d=boxes.filter(function(b){return b.checked;}).length; bar.style.width=(boxes.length?Math.round(d/boxes.length*100):0)+'%'; cnt.textContent=d+' of '+boxes.length+' done'; }
 var pr=document.getElementById('ckPrint'); if(pr) pr.addEventListener('click',function(){ window.print(); });
 var rs=document.getElementById('ckReset'); if(rs) rs.addEventListener('click',function(){ boxes.forEach(function(b){ b.checked=false; }); update(); save(); });
 update();
})();
</script>"""

WIRE_ALERT = ('<div class="ck-alert">\n'
 '<h3>⚠ Protect your money from wire fraud</h3>\n'
 '<p>Real estate closings are a top target for scammers. Never trust wiring instructions &mdash; '
 'or last-minute changes to them &mdash; that arrive by email or text. Before you move a single '
 'dollar, call the title company using a phone number you already know (not one from the email) '
 'and confirm the account details out loud. When something feels off, slow down and check with us.</p>\n'
 '</div>')

def phase(title, intro, items):
    lis = []
    for label, help in items:
        h = '<p class="ck-help">%s</p>' % help if help else ''
        lis.append('<li class="ck-item"><label><input type="checkbox"><span class="ck-label">%s</span></label>%s</li>'
                   % (label, h))
    return ('<div class="ck-phase">\n<h2>%s</h2>\n<p class="ck-phase-intro">%s</p>\n'
            '<ul class="ck-list">\n%s\n</ul>\n</div>' % (title, intro, "\n".join(lis)))

def faq_block(faqs):
    html = "\n".join('<details class="faq-item">\n<summary>%s</summary>\n<div class="faq-answer"><p>%s</p></div>\n</details>'
                     % (q, a) for q, a in faqs)
    schema = ",\n".join('{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
                        % (json.dumps(strip(q)), json.dumps(strip(a))) for q, a in faqs)
    return html, schema

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>@@TITLE@@</title>
 <meta name="description" content="@@DESC@@">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="@@URL@@">
 <meta property="og:title" content="@@OGTITLE@@">
 <meta property="og:description" content="@@DESC@@">
 <meta property="og:url" content="@@URL@@">
 <meta property="og:image" content="https://yourrealtylink.com/assets/img/og-default.png">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 { "@context": "https://schema.org", "@graph": [
 { "@type": "WebPage", "url": "@@URL@@", "name": "@@NAME@@", "speakable": { "@type": "SpeakableSpecification", "cssSelector": [".qa-lead"] } },
 { "@type": ["LocalBusiness","RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404", "areaServed": "Central Indiana" },
 { "@type": "FAQPage", "mainEntity": [ @@FAQSCHEMA@@ ] },
 { "@type": "BreadcrumbList", "itemListElement": [
 { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/" },
 { "@type": "ListItem", "position": 2, "name": "Services", "item": "https://yourrealtylink.com/services/" },
 { "@type": "ListItem", "position": 3, "name": "@@NAME@@", "item": "@@URL@@" } ] }
 ] }
 </script>
 @@FONTS@@
 <style>@@CSS@@</style>
</head>
<body>

@@HEADER@@

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/services/">Services</a> <span>&rsaquo;</span> @@CRUMB@@</div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>@@H1@@</h1>
 <p class="hero-sub">@@HEROSUB@@</p>
 <div class="hero-badges">@@BADGES@@</div>
 </div>
</section>

<div class="container">
 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">@@QA@@</p>
</div>
<!-- QA-END -->

 <div class="ck-wrap">
@@PROGRESS@@
@@PDFCTA@@
@@INTRO@@
@@PHASES@@
@@EXTRAS@@

 <div class="ck-cross">@@CROSS@@</div>

 <div class="cta-block">
@@CTA@@
 </div>

 <section class="faq-section">
 <h2>@@CRUMB@@ FAQs</h2>
@@FAQ@@
 </section>
 </div>
</div>
@@CKJS@@

@@FOOTER@@

@@SCRIPTS@@"""

def build(cfg):
    faq_html, faq_schema = faq_block(cfg["faqs"])
    phase_htmls = [phase(t, i, items) for t, i, items in cfg["phases"]]
    phase_htmls.insert(2, WIRE_ALERT)   # wire-fraud callout after the money-movement phase
    phases = "\n".join(phase_htmls)
    out = PAGE
    repl = {
        "@@TITLE@@": cfg["title"], "@@DESC@@": cfg["desc"], "@@URL@@": cfg["url"],
        "@@OGTITLE@@": cfg["title"], "@@NAME@@": cfg["name"], "@@CRUMB@@": cfg["crumb"],
        "@@H1@@": cfg["h1"], "@@HEROSUB@@": cfg["herosub"], "@@BADGES@@": cfg["badges"],
        "@@QA@@": cfg["qa"], "@@INTRO@@": cfg["intro"], "@@CROSS@@": cfg["cross"],
        "@@CTA@@": cfg["cta"], "@@FAQ@@": faq_html, "@@FAQSCHEMA@@": faq_schema,
        "@@PHASES@@": phases, "@@PROGRESS@@": PROGRESS, "@@CKJS@@": CK_JS, "@@CSS@@": CSS,
        "@@FONTS@@": FONTS, "@@HEADER@@": HEADER, "@@FOOTER@@": FOOTER, "@@SCRIPTS@@": SCRIPTS,
        "@@PDFCTA@@": ('<p class="ck-pdfcta">📄 <a href="/resources/%s/">Prefer a printable copy? '
                       'Get the PDF checklist &rarr;</a></p>' % cfg["pdf_landing"]),
        "@@EXTRAS@@": cfg.get("extras", ""),
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    d = os.path.join(ROOT, cfg["dir"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    # sitemap
    sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm, encoding="utf-8").read()
    if cfg["url"] not in s:
        open(sm, "w", encoding="utf-8").write(
            s.replace("</urlset>", f'<url>\n  <loc>{cfg["url"]}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.7</priority>\n</url>\n</urlset>'))
    return cfg["dir"]

# ─────────────────────────────── BUYER ───────────────────────────────
buyer = {
 "dir": "services/buyer-closing-checklist",
 "pdf_landing": "buyer-closing-checklist",
 "extras": local_essentials_block(),
 "url": "https://yourrealtylink.com/services/buyer-closing-checklist/",
 "title": "Buyer&rsquo;s Closing Checklist for Indianapolis Home Buyers | Your Realty Link",
 "desc": "A step-by-step closing checklist for Central Indiana home buyers: what to do before closing, what to bring on closing day, and how to protect yourself from wire fraud.",
 "name": "Buyer's Closing Checklist",
 "crumb": "Buyer&rsquo;s Closing Checklist",
 "h1": "The Home Buyer&rsquo;s Closing Checklist",
 "herosub": "Closing is the last &mdash; and biggest &mdash; step of buying your home. This interactive checklist walks you through what to do before closing, what to bring to the table, and how to close with confidence.",
 "badges": ('<span class="hero-badge">✅ Before Closing</span>'
            '<span class="hero-badge">🖊 Closing Day</span>'
            '<span class="hero-badge">🏡 After Closing</span>'
            '<span class="hero-badge">🖨 Printable</span>'),
 "qa": ('Before closing, review your Closing Disclosure the moment it arrives and compare it to your Loan '
        'Estimate. On closing day, bring a government photo ID, a cashier&rsquo;s check or verified wire for your '
        'cash to close, and your Closing Disclosure. Never trust wiring changes sent by email &mdash; verify by '
        'phone. Check off each step below, and call Your Realty Link at <a href="tel:3179977404">317-997-7404</a> '
        'with any questions.'),
 "intro": ('<p>We built this checklist so nothing about closing catches you off guard. Tap each item to check it '
           'off &mdash; your progress saves on this device &mdash; and use the Print button to bring a copy to the '
           'table. It follows the same stages the Consumer Financial Protection Bureau recommends, tuned for how '
           'closings actually work here in Central Indiana.</p>'),
 "phases": [
   ("A couple of weeks out: get your ducks in a row",
    "A smooth closing starts well before closing day. Knock these out early so nothing surprises you at the table.",
    [("Confirm your <strong>closing date, time, and location</strong> with Your Realty Link, your lender, and the title company",
      "In Indiana, closings are usually handled by a title or settlement company. We&rsquo;ll make sure everyone is on the same page."),
     ("Lock in your <strong>homeowner&rsquo;s insurance</strong> and send the policy to your lender",
      "Your lender needs proof of insurance before they&rsquo;ll fund the loan. Shop a couple of quotes &mdash; premiums vary."),
     ("Schedule your <strong>final walkthrough</strong> for the 24&ndash;48 hours before closing",
      "Your last chance to confirm the home&rsquo;s condition, that any agreed repairs were done, and that nothing changed since your offer."),
     ("Keep your finances <strong>steady and boring</strong>",
      "Until you have the keys, don&rsquo;t open new credit, finance a car, make large deposits, or change jobs &mdash; any of it can derail your approval."),
     ("Confirm your <strong>&ldquo;cash to close&rdquo;</strong> amount and how you&rsquo;ll deliver it",
      "You&rsquo;ll typically bring a cashier&rsquo;s check or send a wire. Get the exact amount and instructions from the title company.")]),
   ("Three days before: your Closing Disclosure",
    "By law, your lender must give you the Closing Disclosure at least three business days before closing. That window is for you &mdash; use it.",
    [("Review your <strong>Closing Disclosure (CD)</strong> the moment it arrives",
      "This is the final accounting of your loan and costs. Read every line."),
     ("Compare the CD to your original <strong>Loan Estimate</strong>",
      "Check that the loan type, interest rate, monthly payment, and cash to close match what you expected. Only certain costs are allowed to change."),
     ("Ask your loan officer about <strong>anything that changed</strong> or that you don&rsquo;t understand",
      "Fees you don&rsquo;t recognize, a different rate, escrow questions &mdash; get answers before you sign, not at the table."),
     ("Confirm your <strong>final cash-to-close number</strong>",
      "So your cashier&rsquo;s check or wire is for the exact amount.")]),
   ("Closing day: what to bring",
    "Show up ready. Here&rsquo;s your grab-list for the table.",
    [("<strong>Government-issued photo ID</strong> for every buyer on the loan",
      "A valid driver&rsquo;s license, state ID, or passport."),
     ("Your <strong>cashier&rsquo;s check or proof of wire</strong> for the cash to close",
      "Made out per the title company&rsquo;s instructions."),
     ("A copy of your <strong>Closing Disclosure</strong>",
      "To compare against the final documents one more time."),
     ("Your <strong>co-borrower</strong>, if you have one",
      "Everyone on the loan needs to sign."),
     ("Your <strong>checkbook</strong>, just in case",
      "For any small last-minute difference.")]),
   ("At the table: before you sign",
    "Take your time. You have every right to read and understand what you&rsquo;re signing, no matter how long it takes.",
    [("Confirm the <strong>key numbers match</strong> across your documents",
      "Loan amount, interest rate, and monthly payment should be identical on the note, the mortgage, and your Closing Disclosure."),
     ("Ask how your <strong>property taxes and insurance</strong> are handled",
      "Are they escrowed into your monthly payment, or do you pay them yourself? Indiana property taxes are billed in two installments each year."),
     ("Ask <strong>where to send your payment</strong> and about any <strong>HOA dues</strong>",
      "Know who will service your loan and how HOA payments work if your neighborhood has an association."),
     ("Collect your <strong>keys, garage remotes, and mailbox keys</strong>",
      "Make sure you leave the table with everything you need to get into your home.")]),
   ("After closing: settle in",
    "Congratulations &mdash; you&rsquo;re a homeowner. A few last things to protect your investment.",
    [("<strong>Store your closing documents</strong> somewhere safe",
      "You&rsquo;ll need them for taxes and future reference. A digital backup is smart."),
     ("<strong>Set up your utilities</strong>",
      'Use our <a href="/utilities/">Central Indiana utilities &amp; setup guide</a> to line up electric, gas, water, trash, and internet for your new address.'),
     ("File for your <strong>Indiana homestead deduction</strong>",
      "This lowers property taxes on your primary residence &mdash; file with your county auditor. Ask us or your title company about the current deadline."),
     ("<strong>Change the locks</strong> and update your address",
      "New locks for peace of mind, plus USPS, your driver&rsquo;s license, banks, and subscriptions.")]),
 ],
 "cross": ('<strong>Keep going:</strong> understand the numbers with our '
           '<a href="/services/closing-costs-buyers/">buyer closing costs guide</a>, see the full '
           '<a href="/services/home-buying-process/">home buying process</a>, estimate your payment with the '
           '<a href="/services/mortgages/">mortgage calculator</a>, or set up your new home with the '
           '<a href="/utilities/">utilities guide</a>.'),
 "cta": ('<h3>Questions About Your Closing?</h3>\n'
         '<p>Buying with Your Realty Link means you&rsquo;re never guessing at the closing table. Call Janet '
         'Giles and the team, or send a note and we&rsquo;ll walk you through it.</p>\n'
         '<div class="btn-group">\n'
         '<a href="tel:3179977404" class="btn btn-white">📞 Call: 317-997-7404</a>\n'
         '<a href="/contact/" class="btn btn-outline">Contact Your Realty Link →</a>\n'
         '<a href="/services/closing-costs-buyers/" class="btn btn-outline">Buyer Closing Costs →</a>\n'
         '</div>'),
 "faqs": [
   ("When do I get my Closing Disclosure?",
    "By law, at least three business days before closing. That window exists so you can review the final loan terms and costs without pressure &mdash; use it, and bring any questions to your loan officer before closing day."),
   ("What do I need to bring to closing in Indiana?",
    "A government photo ID for everyone on the loan, a cashier's check or proof of a verified wire for your cash to close, a copy of your Closing Disclosure, and your co-borrower if you have one. We'll give you the exact amount and instructions ahead of time."),
   ("How much money will I need at closing?",
    'Your "cash to close" is your down payment plus closing costs, minus credits and your earnest money. The exact figure is on your Closing Disclosure. See our <a href="/services/closing-costs-buyers/">buyer closing costs guide</a> for what&rsquo;s included.'),
   ("Can I still walk away at closing?",
    "Until you sign, yes &mdash; though there can be consequences depending on your contract and contingencies. If something feels wrong, tell us and pause. It&rsquo;s always better to ask than to sign a deal you&rsquo;re not comfortable with."),
   ("Who handles the closing?",
    "In Central Indiana, closings are typically conducted by a title or settlement company that also issues title insurance. Your Realty Link coordinates with them, your lender, and the other side so closing day goes smoothly."),
 ],
}

# ─────────────────────────────── SELLER ───────────────────────────────
seller = {
 "dir": "services/seller-closing-checklist",
 "pdf_landing": "seller-closing-checklist",
 "url": "https://yourrealtylink.com/services/seller-closing-checklist/",
 "title": "Seller&rsquo;s Closing Checklist for Indianapolis Home Sellers | Your Realty Link",
 "desc": "A step-by-step closing checklist for Central Indiana home sellers: what to prepare under contract, how to review your net proceeds, what to bring to closing, and what to do after.",
 "name": "Seller's Closing Checklist",
 "crumb": "Seller&rsquo;s Closing Checklist",
 "h1": "The Home Seller&rsquo;s Closing Checklist",
 "herosub": "Selling comes down to a smooth closing. This interactive checklist covers what to line up once you&rsquo;re under contract, how to check your net proceeds, and what to bring to the table.",
 "badges": ('<span class="hero-badge">📄 Under Contract</span>'
            '<span class="hero-badge">🖊 Closing Day</span>'
            '<span class="hero-badge">💵 Your Proceeds</span>'
            '<span class="hero-badge">🖨 Printable</span>'),
 "qa": ('Once you&rsquo;re under contract, request your mortgage payoff, complete your Indiana seller&rsquo;s disclosure, '
        'and gather keys, remotes, and documents. Before closing, review your settlement statement and net-proceeds '
        'figure, and set up wire verification to avoid fraud. On closing day, bring a government photo ID and every '
        'key and code. Check off each step below &mdash; questions? Call Your Realty Link at '
        '<a href="tel:3179977404">317-997-7404</a>.'),
 "intro": ('<p>Selling has fewer moving parts at the table than buying, but the details still matter &mdash; '
           'especially your payoff and net proceeds. Tap each item to check it off (your progress saves on this '
           'device) and use the Print button for a copy. Have questions on any step? That&rsquo;s what we&rsquo;re here for.</p>'),
 "phases": [
   ("Under contract: start the paperwork",
    "Once your home is under contract, a few early moves keep closing day painless.",
    [("Confirm the <strong>title company, closing date, and time</strong> with Your Realty Link",
      "We&rsquo;ll coordinate with the buyer&rsquo;s side and the title company so everyone is aligned."),
     ("Request your <strong>mortgage payoff statement</strong>",
      "Ask your lender for a written payoff good through your closing date &mdash; and include any second mortgage or HELOC so nothing is missed."),
     ("Complete your <strong>Indiana Seller&rsquo;s Residential Real Estate Disclosure</strong>",
      "If you haven&rsquo;t already. Being upfront about the home&rsquo;s condition protects you down the road."),
     ("Gather the <strong>documents and extras</strong> the buyer will want",
      "Warranties and appliance manuals, HOA documents, any survey, and a list of all keys, remotes, and gate or alarm codes."),
     ("Schedule any <strong>agreed-upon repairs</strong> and keep the receipts",
      "Buyers often want to see proof the work was completed before closing.")]),
   ("Before closing day: review your numbers",
    "You&rsquo;ll receive a settlement statement showing exactly what you net. Check it carefully.",
    [("Review your <strong>settlement statement (ALTA)</strong>",
      "Confirm the sale price, your loan payoff, prorated taxes, commission, and your net proceeds."),
     ("Confirm your <strong>prorated property taxes</strong> and any HOA dues",
      "Indiana property taxes are paid in arrears, so proration matters &mdash; the title company calculates your share."),
     ("Decide how you&rsquo;ll <strong>receive your proceeds</strong>",
      "Wire transfer or check. If you&rsquo;re wiring, set up verification with the title company by phone to avoid fraud."),
     ("Plan your <strong>move-out and utility stop</strong>",
      'Schedule utilities to stop the day after closing &mdash; don&rsquo;t cancel early. Our <a href="/utilities/">utilities guide</a> has the providers by city.')]),
   ("Closing day: what to bring",
    "Sellers usually have a lighter table than buyers, but don&rsquo;t forget these.",
    [("<strong>Government-issued photo ID</strong> for every person on the title",
      "Driver&rsquo;s license, state ID, or passport."),
     ("<strong>All keys, garage and gate remotes, mailbox keys, and codes</strong>",
      "Plus appliance manuals and warranties for the new owner."),
     ("Your <strong>proceeds instructions</strong>",
      "A voided check or the wire information you verified with the title company."),
     ("Any <strong>outstanding documents</strong> the title company requested",
      "Payoff details, HOA paperwork, or trust and power-of-attorney documents, if applicable.")]),
   ("At the table: before you sign",
    "Read before you sign &mdash; this is where ownership legally transfers.",
    [("Confirm your <strong>net proceeds</strong> figure",
      "Make sure it matches the settlement statement you reviewed."),
     ("Sign the <strong>deed and closing documents</strong>",
      "The deed transfers ownership; the settlement statement documents the money."),
     ("Hand over <strong>keys, remotes, and codes</strong>",
      "Once the sale funds and records, the home belongs to the buyer.")]),
   ("After closing: wrap it up",
    "A few final steps once the sale records.",
    [("<strong>Cancel your homeowner&rsquo;s insurance</strong> &mdash; after the sale records",
      "Don&rsquo;t cancel early; wait until you&rsquo;re confirmed closed and recorded."),
     ("<strong>Stop utilities and forward your mail</strong>",
      "Set the stop date for after closing, and file a change of address with USPS."),
     ("<strong>Keep your settlement statement</strong> for taxes",
      "You may need it for capital-gains reporting. A tax professional can tell you whether the sale is taxable."),
     ("<strong>Notify your HOA</strong> of the sale",
      "So dues and communications transfer to the new owner.")]),
 ],
 "cross": ('<strong>Keep going:</strong> see what selling costs with our '
           '<a href="/services/closing-costs-sellers/">seller closing costs guide</a>, review our full '
           '<a href="/services/sell-my-home/">home selling services</a>, learn about '
           '<a href="/services/pricing-your-home/">pricing your home</a>, or point your buyer to the '
           '<a href="/utilities/">utilities guide</a>.'),
 "cta": ('<h3>Thinking About Selling?</h3>\n'
         '<p>Start with what your home is worth today. Your Realty Link gives you a free, no-pressure valuation '
         'and a clear plan all the way to the closing table.</p>\n'
         '<div class="btn-group">\n'
         '<a href="tel:3179977404" class="btn btn-white">📞 Call: 317-997-7404</a>\n'
         '<a href="/contact/" class="btn btn-outline">Get a Free Home Valuation →</a>\n'
         '<a href="/services/closing-costs-sellers/" class="btn btn-outline">Seller Closing Costs →</a>\n'
         '</div>'),
 "faqs": [
   ("What do I net from selling my home?",
    'Your net is the sale price minus your mortgage payoff, prorated property taxes, commission, and closing costs. The title company&rsquo;s settlement statement shows the exact figure. See our <a href="/services/closing-costs-sellers/">seller closing costs guide</a> for the details.'),
   ("What do I need to bring to closing as a seller?",
    "A government photo ID for everyone on the title, all keys, remotes, and codes for the home, and your verified instructions for receiving proceeds. The title company will tell you if they need anything else from you."),
   ("How do I get paid when I sell?",
    "Usually by wire transfer or check on or shortly after closing day, once the sale funds and records. Set up wire details directly with the title company by phone to protect yourself against fraud."),
   ("Do I have to be at the closing table?",
    "Not always. Many Indiana closings can be handled with a mail-away or remote signing, especially if you&rsquo;ve already moved. Ask us and the title company about your options."),
   ("When should I cancel my utilities and insurance?",
    'Schedule utilities to stop the day after closing, and wait to cancel your homeowner&rsquo;s insurance until the sale has recorded. Our <a href="/utilities/">utilities guide</a> lists the providers by city.'),
 ],
}

if __name__ == "__main__":
    for cfg in (buyer, seller):
        d = build(cfg)
        print("built /%s/" % d)
