#!/usr/bin/env python3
"""Property-tax updates for 2026-2027 on the three Indiana property-tax posts (Oct 2026 SEO audit).

- indiana-property-tax-caps-explained: "Property Taxes by County Around Indianapolis" (2026 certified
  district rates via STATS Indiana/DLGF, 2026 county local income tax rates from Indiana DOR, ACS
  2020-2024 median taxes paid).
- indiana-homestead-exemption-lower-property-taxes: "What Changes in 2027" (SEA 1-2025 phase-in,
  checked against IC 6-1.1-12-37, -37.5, IC 6-1.1-20.6-7.7, DLGF memo of June 12, 2025).
- indiana-property-tax-deductions-seniors: what SEA 1 changed for seniors (over-65 credit,
  IC 6-1.1-51.3-1) plus the new homestead credit.

Marker-wrapped (<!-- TAX-2027 --> ... <!-- /TAX-2027 -->), inserted before each post's FAQ.
General information; every section ends with a verify-with-your-auditor line. Idempotent.
"""
import re

START, END = "<!-- TAX-2027 -->", "<!-- /TAX-2027 -->"
NOTE = ('<p style="font-size:.9rem;color:var(--gray);"><em>This is general information, not tax or legal advice. '
        'Verify current figures with your county auditor or the Indiana Department of Local Government Finance '
        '(<a href="https://www.in.gov/dlgf/" target="_blank" rel="noopener">in.gov/dlgf</a>).</em></p>')

COUNTIES = [("Marion", "$2.73", "2.02%", "$2,028"), ("Hamilton", "$2.02", "1.10%", "$3,549"), ("Hendricks", "$2.11", "1.70%", "$2,482"),
            ("Johnson", "$1.82", "1.40%", "$2,024"), ("Hancock", "$2.05", "1.94%", "$1,806"), ("Boone", "$1.57", "1.71%*", "$2,919"),
            ("Morgan", "$1.66", "2.72%", "$1,174"), ("Shelby", "$1.64", "1.70%", "$1,412"), ("Madison", "$2.65", "2.25%", "$1,192")]
rows = "\n".join(f" <tr><td>{c}</td><td>{r}</td><td>{l}</td><td>{m}</td></tr>" for c, r, l, m in COUNTIES)

SECTIONS = {
"blog/indiana-property-tax-caps-explained/index.html": f"""
 <h2 id="by-county">Property Taxes by County Around Indianapolis</h2>
 <p>Whether you&rsquo;re comparing a home in Carmel, Greenwood, Avon or downtown Indianapolis, here&rsquo;s where the metro counties actually differ.</p>
 <p><strong>Why posted tax rates look higher than 1%.</strong> Each county is divided into taxing districts, and each district&rsquo;s rate combines the city or town, township, schools, library and county. In 2026 the middle district rate ranged from about $1.57 per $100 of assessed value in Boone County to $2.73 in Marion County. That rate applies to your <em>net</em> assessed value after deductions; credits come off next, and then the cap applies. In higher-rate districts, the 1% homestead cap is often what actually limits a homeowner&rsquo;s bill.</p>
 <p><strong>Local income tax is where counties really differ.</strong> Every Indiana county adds a local income tax to the state&rsquo;s 2.95% rate (2026). Around Indianapolis it ranges from 1.10% in Hamilton County to 2.72% in Morgan County, and your rate is set by the county you live in on January 1 of the tax year.</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <tr><th>County</th><th>2026 tax rate per $100 AV (district median)</th><th>Local income tax (2026)</th><th>Median homeowner tax bill</th></tr>
{rows}
 </table>
 </div>
 <p style="font-size:.85rem;color:var(--gray);">*Boone County&rsquo;s rate rose from 1.70% to 1.71% on October 1, 2026. Tax rates: 2026 certified rates (Indiana DLGF, via <a href="https://www.stats.indiana.edu/web/profiles/tax_rates_2026/Hamilton.html" target="_blank" rel="noopener">STATS Indiana</a>). Income tax rates: <a href="https://www.in.gov/dor/files/dn01.pdf" target="_blank" rel="noopener">Indiana Department of Revenue</a>. Median bills: U.S. Census Bureau American Community Survey, 2020&ndash;2024 (all owner-occupied homes; higher-value counties show higher bills).</p>
 <p><strong>Investors feel rate differences more.</strong> Rentals and second homes don&rsquo;t get the homestead deductions or credit, and their cap is 2%, so district rates matter more for landlords. And changes are coming: Senate Enrolled Act 1 (2025) adds a homestead credit of 10% of the bill, up to $300, phases out the standard homestead deduction while growing the supplemental deduction through 2031, and restructures local income taxes starting in 2028. See <a href="/blog/indiana-homestead-exemption-lower-property-taxes/#changes-2027">what changes in 2027</a>.</p>
 <p>Want the real tax history on a home you&rsquo;re considering? Our team pulls it for every property we show.</p>
 {NOTE}
""",
"blog/indiana-homestead-exemption-lower-property-taxes/index.html": f"""
 <h2 id="changes-2027">What Changes in 2027: Indiana&rsquo;s Homestead Deduction</h2>
 <p>Indiana&rsquo;s 2025 property tax law (Senate Enrolled Act 1) is reshaping the homestead deduction over several years. Property is assessed one year and billed the next, so your 2026 assessment shows up on the bill you pay in 2027.</p>
 <ul>
 <li><strong>The standard deduction drops to $40,000</strong> (from $48,000) on 2027 bills, then steps down to $30,000, $20,000 and $10,000, reaching $0 with the 2030 assessment (IC 6-1.1-12-37).</li>
 <li><strong>The supplemental deduction rises to 46%</strong> of your assessed value after the standard deduction (from 40%), climbing each year to 66.7% for 2031 bills and beyond, capped at 75% of gross assessed value (IC 6-1.1-12-37.5).</li>
 <li><strong>The homestead credit continues:</strong> 10% of your homestead tax bill, up to $300. It started with 2026 bills, applies automatically if you have the homestead deduction, and doesn&rsquo;t count voter-approved referendum taxes (IC 6-1.1-20.6-7.7).</li>
 <li><strong>The 1% cap still applies.</strong> Homestead taxes stay capped at 1% of gross assessed value, not counting referendum taxes.</li>
 </ul>
 <p><strong>What it means for you:</strong> your net bill depends on your home&rsquo;s value, local tax rates and any referendums, so results vary by neighborhood. If you&rsquo;re buying, make sure your homestead deduction is filed with the county auditor by January 15 of the year the taxes are due (IC 6-1.1-12-37). If you&rsquo;ve just closed with our team, we&rsquo;re glad to point you to the right county form. Comparing counties? See <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>.</p>
 {NOTE}
""",
"blog/indiana-property-tax-deductions-seniors/index.html": f"""
 <h2 id="changes-2026">What&rsquo;s Changed for Seniors (2026&ndash;2027)</h2>
 <p>Indiana&rsquo;s 2025 property tax law (Senate Enrolled Act 1) changed some of the senior benefits described above:</p>
 <ul>
 <li><strong>The over-65 deduction is now a $150 credit</strong> for qualifying homeowners, with income limits of $60,000 for a single filer and $70,000 for a joint return (IC 6-1.1-51.3-1). It requires an application unless your county moves you over automatically, so check with your county auditor.</li>
 <li><strong>A new homestead credit</strong> of 10% of your homestead tax bill, up to $300, started with 2026 bills and applies automatically if you have the homestead deduction (IC 6-1.1-20.6-7.7).</li>
 <li><strong>The homestead deductions are shifting</strong> through 2031: the standard deduction phases out while the supplemental deduction grows. See <a href="/blog/indiana-homestead-exemption-lower-property-taxes/#changes-2027">what changes in 2027</a>.</li>
 </ul>
 {NOTE}
""",
}

for path, sec in SECTIONS.items():
    s = open(path, encoding="utf-8", newline="").read()
    block = f"{START}{sec}{END}\n"
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda m: block, s, flags=re.S)
    else:
        i = s.index(" <!-- FAQ -->")
        s = s[:i] + block + s[i:]
    s = re.sub(r'("dateModified": ")[0-9-]+(")', r"\g<1>2026-10-14\2", s, count=1)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print("updated", path)
