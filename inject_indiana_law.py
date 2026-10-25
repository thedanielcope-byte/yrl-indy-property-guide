#!/usr/bin/env python3
"""Indiana-law basics on the divorce, inherited and estate seller pages (Oct 2026 SEO audit).

Adds a marker-wrapped section (<!-- INDIANA-LAW --> ... <!-- /INDIANA-LAW -->) before each
page's "Why Choose Your Realty Link..." heading, and corrects a few statements that didn't
match Indiana law (equal-division presumption; temporary orders can't force a sale; how
probate court approval actually works).

Every legal point was checked against the 2026 Indiana Code on iga.in.gov (statute cites are
in the copy). General information only; each section ends with a talk-to-an-attorney line.
Idempotent — safe to re-run.
"""
import re

START, END = "<!-- INDIANA-LAW -->", "<!-- /INDIANA-LAW -->"
NOTE = ('<p class="law-note" style="font-size:.92rem;color:var(--gray);"><em>This is general information, '
        'not legal advice. Talk with an Indiana attorney about your situation.</em></p>')

SECTIONS = {
"services/divorce-home-sale/index.html": f"""
 <h2 id="indiana-law">Selling a Home During a Divorce in Indiana: The Basics</h2>
 <p>Indiana courts start from the presumption that an equal division of marital property is just and reasonable, though either spouse can present evidence for a different split (IC 31-15-7-5). In the final decree, the judge can award the house to one spouse with a payment to the other, or order it sold and the proceeds divided (IC 31-15-7-4). If you reach a written agreement about the house and the court approves it, that agreement becomes part of your decree.</p>
 <p>While the case is pending, either spouse can ask the court for an order that bars transferring or encumbering property (IC 31-15-4-3). An Indiana appeals court has held that temporary orders can decide who lives in the home during the case, but can&rsquo;t force a sale. In practice, selling before the decree usually depends on both of you agreeing. If an order is in place, ask your attorney about having it modified before you list.</p>
 <p>When you&rsquo;re both on the deed, expect both of you to sign the listing and closing paperwork. Our team helps you settle the practical pieces up front: one listing agent, a price backed by a comparative market analysis, who handles showings and repairs, and how offers get approved. Every update goes to both of you, and to your attorneys if you&rsquo;d like.</p>
 {NOTE}
""",
"services/inherited-property/index.html": f"""
 <h2 id="indiana-law">Selling an Inherited House in Indiana: The Basics</h2>
 <p>How you get to a sale depends on how the house was titled:</p>
 <ul>
 <li><strong>Transfer on death (TOD) deed.</strong> If the owner recorded a TOD deed before passing, the home goes to the named beneficiary without probate. The beneficiary then records an affidavit with the county recorder, endorsed by the county auditor (IC 32-17-14-11, IC 32-17-14-26).</li>
 <li><strong>Joint ownership.</strong> Homes owned by spouses, or by co-owners whose deed expressly creates a joint tenancy with right of survivorship, can often pass to the survivor without probate.</li>
 <li><strong>In the owner&rsquo;s name alone.</strong> An estate usually needs to be opened. Indiana&rsquo;s small estate affidavit (for deaths after June 30, 2022, estates of $100,000 or less after liens and funeral costs, available 45 days after death) is built for bank accounts, vehicles and other personal property (IC 29-1-8-1). Real estate in a small estate uses a separate recorded affidavit (IC 29-1-8-3), and many homes are worth more than that limit on their own. See <a href="/services/probate-real-estate-agent/">how probate home sales work in Indiana</a>.</li>
 </ul>
 <p>On taxes: Indiana has no inheritance tax for deaths after December 31, 2012. Federally, inherited property generally takes a basis equal to its value at the date of death. Your tax professional can tell you how that applies to you.</p>
 <p>Our team can provide a market analysis, help you decide between selling as-is or preparing the home, and coordinate timing with your attorney.</p>
 {NOTE}
""",
"services/estate-sales/index.html": f"""
 <h2 id="indiana-law">How Probate Home Sales Work in Indiana</h2>
 <p>When a house is part of an Indiana estate, the person with authority to sell is the personal representative: the executor or administrator the court appoints and issues letters to. How much court involvement the sale needs depends on the type of administration:</p>
 <ul>
 <li><strong>Unsupervised administration:</strong> when the heirs agree, the estate is solvent and the court approves, the personal representative can sell real estate without a separate court order (IC 29-1-7.5-3).</li>
 <li><strong>Supervised administration:</strong> the personal representative generally petitions the court for an order to sell, and a private sale can&rsquo;t go below the fair market value on record, unless the will grants a power of sale (IC 29-1-15-2, IC 29-1-15-11, IC 29-1-15-13).</li>
 </ul>
 <p>Either way, creditors generally have three months from the first published notice to file claims (IC 29-1-14-1), and estates are expected to close within about a year of appointment unless there&rsquo;s good cause. For the full picture, see our <a href="/services/probate-real-estate-agent/">probate real estate agent guide</a>.</p>
 <p>Our team works alongside the personal representative and the estate&rsquo;s attorney: a market analysis to help set a realistic price (the court may also require a formal appraisal), referrals for clean-out and repairs, and marketing for an as-is or prepared sale.</p>
 {NOTE}
""",
}

FIXES = {
"services/divorce-home-sale/index.html": [
  ("Indiana is an equitable distribution state, meaning marital assets — including the family home — are divided fairly, though not necessarily equally.",
   "Indiana courts presume that an equal division of marital property — including the family home — is just and reasonable, though either spouse can present evidence for a different split."),
  ("Indiana is an equitable distribution state, meaning courts divide marital property fairly — though not always equally.",
   "Indiana courts start from the presumption that an equal split of marital property is fair, though either spouse can show why a different division is just."),
  ("Indiana is an equitable distribution state, meaning courts divide marital property fairly — which does not always mean equally.",
   "Indiana courts start from the presumption that an equal split of marital property is fair, though either spouse can show why a different division is just."),
  ("A court can order the sale of a marital home if the parties cannot agree.",
   "If you can't agree, the court can order the home sold in the final decree; temporary orders during the case generally can't force a sale."),
  ("Does both spouses need to agree to sell the home during a divorce?",
   "Do both spouses need to agree to sell the home during a divorce?"),
],
"services/estate-sales/index.html": [
  ("It depends on how the property is titled and the size of the estate. Many Indiana estates go through probate, and the executor or personal representative may need court authorization to sell real property.",
   "It depends on how the estate is administered. In an unsupervised Indiana estate, the personal representative can sell real estate without a separate court order; in a supervised estate, a court order is generally required unless the will grants a power of sale. Homes that pass by a transfer on death deed or joint ownership may not go through probate at all."),
  ('<li><a href="/services/inherited-property/">Selling an Inherited Home in Indianapolis</a>',
   '<li><a href="/services/probate-real-estate-agent/">Probate Real Estate Agent in Indianapolis</a> — How Indiana probate home sales work, step by step</li>\n <li><a href="/services/inherited-property/">Selling an Inherited House in Indiana</a>'),
],
"services/inherited-property/index.html": [
  ("<title>Selling an Inherited Home Indianapolis | Your Realty Link</title>", "<title>Selling an Inherited House in Indiana | Your Realty Link</title>"),
  ('og:title" content="Selling an Inherited Home Indianapolis | Your Realty Link"', 'og:title" content="Selling an Inherited House in Indiana | Your Realty Link"'),
  ('twitter:title" content="Selling an Inherited Home Indianapolis | Your Realty Link"', 'twitter:title" content="Selling an Inherited House in Indiana | Your Realty Link"'),
  ('name="description" content="Inherited a home in Indianapolis or Central Indiana? Your Realty Link helps heirs understand their options and sell with confidence."',
   'name="description" content="Selling an inherited house in Indiana? How TOD deeds, joint ownership and probate affect the sale, and how our Indianapolis team helps heirs sell."'),
  ("<h1>Selling an Inherited Home in Indianapolis &amp; Central Indiana</h1>", "<h1>Selling an Inherited House in Indiana: Indianapolis &amp; Central Indiana</h1>"),
  ("SEO Title: Selling an Inherited Home Indianapolis | Your Realty Link", "SEO Title: Selling an Inherited House in Indiana | Your Realty Link"),
  ("Focus Keyword: inherited home indianapolis sell", "Focus Keyword: sell inherited house indiana"),
],
}

for path, section in SECTIONS.items():
    s = open(path, encoding="utf-8", newline="").read()
    for old, new in FIXES.get(path, []):
        if old in s:
            s = s.replace(old, new)
    block = f"{START}{section}{END}\n"
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda m: block, s, flags=re.S)
    else:
        m = re.search(r"\n([ \t]*)<h2>Why Choose Your Realty Link", s)
        if not m:
            raise SystemExit("anchor not found in " + path)
        s = s[:m.start() + 1] + block + "\n" + s[m.start() + 1:]
    open(path, "w", encoding="utf-8", newline="").write(s)
    print("updated", path)
