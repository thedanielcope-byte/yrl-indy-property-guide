# How to file the Indiana homestead deduction, county by county (Nov 19 2026, SEO audit strategic item).
# Companion to /blog/indiana-homestead-exemption-lower-property-taxes/ (the "what it is / how much"
# explainer, 1,523 impressions at avg position 7.5 in GSC). This page is the "how and where to file"
# half, with a section per county the site covers, so it doesn't cannibalize the explainer.
# General information, not tax or legal advice.
#
# Statewide facts, all from State Form 5473 / Form HC10 (R21 / 7-25), "Claim for Homestead Property
# Tax Standard / Supplemental Deduction", https://forms.in.gov/Download.aspx?id=6049 (read Nov 19 2026):
#  - WHEN TO FILE: "completed, dated, and filed or postmarked with the county auditor on or before
#    January 15 of the calendar year in which the property taxes are first due and payable." Applies
#    that year and later years. DLGF deductions page gives the same example (Jan 15, 2026 -> 2025-pay-2026 bill).
#  - Must be eligible (living there as principal residence) when the application is signed.
#  - Filed with the auditor of the county where the homestead is; mail -> include SASE for a stamped copy.
#  - Asks: legal names, last five digits of SSN (or DL/state ID last five if no SSN) for claimant and
#    spouse, parcel number, property owned elsewhere, vacated homestead address. Those numbers are
#    confidential under IC 6-1.1-12-37.
#  - One homestead per individual or married couple; income-producing portions don't qualify.
#  - Moving after the assessment date: old homestead stays for that cycle, apply on the new one
#    (IC 6-1.1-12-37(i)).
#  - Supplemental deduction (IC 6-1.1-12-37.5): "The county auditor is required to record and make the
#    deduction" (no separate application).
#  - Ineligibility: certified statement to the auditor within 60 days of the change, or liable for the
#    deduction plus a 10% civil penalty.
#  - DLGF deductions page (in.gov/dlgf/deductions-and-credits/): no annual reapplication; reapply when
#    the property is sold or the title changes. Lists the Homestead Deduction Change of Use Form
#    (forms.in.gov/Download.aspx?id=10282).
# County facts: researched Nov 19 2026 from each county's official site (auditor/treasurer pages, URLs
# in each entry); phones spot-checked by curl. Several county pages still list older deadlines
# (Dec 31, Jan 5; Jackson even May 10), so the page quotes the state form and tells readers to file early.
# Beacon (Schneider) pages answer 403 to scripts but are the counties' own linked portals.
import html as _h

STATE_FORM = "https://forms.in.gov/Download.aspx?id=6049"
CHANGE_FORM = "https://forms.in.gov/Download.aspx?id=10282"

# name, county-hub slug, office/address, phone, info url, filing (online tuple or None), paper note,
# status (url, label, tail) or None, status fallback text, notes
COUNTIES = [
 dict(n="Marion", office="Marion County Auditor&rsquo;s Office, City-County Building, 200 E. Washington St., Suite W-125, Indianapolis, IN 46204",
      phone="317-327-4646", info="https://www.indy.gov/activity/apply-for-a-homestead-deduction",
      online=("https://www.indy.gov/workflow/homestead-deduction-application", "Homestead Deduction Application",
              "on indy.gov. Only the owner or an authorized representative can apply. Keep the confirmation email: the county says it&rsquo;s your only receipt."),
      status=("https://www.indy.gov/activity/search-current-deductions-on-your-property", "Search Current Deductions or Credits on Your Property",
              " &ldquo;Pending&rdquo; or &ldquo;In-Process&rdquo; means you&rsquo;ve done your part."),
      notes="Marion asks you to re-file when the title changes, such as adding or removing an owner or moving the home into a trust."),
 dict(n="Hamilton", office="Hamilton County Auditor, Real Property Department, Historic Courthouse, 33 N. 9th St., 1st floor (southwest corner), Noblesville, IN 46060",
      phone="317-770-4412", info="https://www.hamiltoncounty.in.gov/376/Standard-Homestead-Credit",
      online=("https://secure2.hamiltoncounty.in.gov/DeductionForms/index.aspx", "Property Tax Deduction Forms",
              ". Look up your address or parcel number, choose the homestead claim and the county emails you a PDF copy."),
      status=("https://secure2.hamiltoncounty.in.gov/PropertyReports/index.aspx", "Hamilton County Property Reports", " (the Current Deductions tab)."),
      notes="Hamilton&rsquo;s own pages show different deadlines (December 31, January 5 and January 15), so don&rsquo;t wait. The county also says letters from Tax Management Associates about homestead eligibility are legitimate and should be answered."),
 dict(n="Hendricks", office="Hendricks County Auditor&rsquo;s Office, 355 S. Washington St., #220, Danville, IN 46122 (8 a.m.&ndash;4 p.m., no appointment needed)",
      phone="317-745-9300", info="https://www.co.hendricks.in.us/department/division.php?structureid=189",
      online=("https://lowtaxinfo.com/hendrickscounty", "LowTaxInfo",
              ". Search your property, open Property Details and click File E-Forms. Homestead is the only deduction Hendricks takes online; the rest are filed in person."),
      status=("https://lowtaxinfo.com/hendrickscounty", "LowTaxInfo", ": each parcel&rsquo;s Property Details shows &ldquo;Homestead Credit Filed?&rdquo;"),
      notes="Hendricks lists December 31 on some pages and January 15 on others. File as soon as you&rsquo;ve moved in."),
 dict(n="Johnson", office="Johnson County Auditor&rsquo;s Office, Government West Annex, 86 W. Court St., Franklin, IN 46131 (mail to the same address)",
      phone="317-346-4310", info="https://johnsoncounty.in.gov/topic/index.php?topicid=68&structureid=11",
      online=("https://beacon.schneidercorp.com/Application.aspx?AppID=129&LayerID=1554&PageTypeID=2&PageID=813", "Johnson County&rsquo;s Beacon property search",
              ". Find your address, open the property summary and use the &ldquo;Apply online for Indiana Homestead Property Tax Deduction&rdquo; link at the very bottom. You sign with a mouse, so use a computer."),
      status=("https://beacon.schneidercorp.com/Application.aspx?AppID=129&LayerID=1554&PageTypeID=2&PageID=813", "Beacon", ", which the county says shows deductions for each parcel."),
      notes="On a new purchase, the county says your closing company normally files the homestead for you, so confirm it did before filing again. Refinancing doesn&rsquo;t require re-filing."),
 dict(n="Hancock", office="Hancock County Auditor&rsquo;s Office, Courthouse Annex, 111 S. American Legion Place, Suite 217, Greenfield, IN 46140",
      phone="317-477-1105", info="https://www.hancockin.gov/173/Online-Deductions",
      online=("https://www.hancockin.gov/737/Applying-Online-Homestead-Deductions", "Applying Online for Homestead Deductions",
              ", the county&rsquo;s step-by-step page. It takes you to Beacon: search your parcel and use &ldquo;Apply online for Homestead Property Tax Deduction&rdquo; at the bottom of the property summary."),
      status=("https://lowtaxinfo.com/hancockcounty", "LowTaxInfo", ": each parcel&rsquo;s Property Details shows &ldquo;Homestead Credit Filed?&rdquo;"),
      notes="If a title company, lender or real estate agent filed your form, Hancock asks you to call and confirm it was filed on time. Refinancing doesn&rsquo;t affect deductions."),
 dict(n="Boone", office="Boone County Auditor&rsquo;s Office, Boone County Courthouse (2nd floor, southeast corner), 201 Courthouse Square, Lebanon, IN 46052",
      phone="765-482-2940", info="https://boonecounty.in.gov/offices/auditor/",
      paper=f'Paper form only: Form HC10, filed in person or by mail. Boone posts it on the <a href="https://boonecounty.in.gov/offices/auditor/forms/" target="_blank" rel="noopener">Auditor&rsquo;s forms page</a>; the current version is on the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>.',
      status=None, status_text="Call the Auditor&rsquo;s office, or check the deductions listed on your latest tax bill.",
      notes="Boone&rsquo;s pages still give a January 5 postmark date from an older version of the rule. File well before either date."),
 dict(n="Madison", office="Madison County Auditor&rsquo;s Office, Government Center, 16 E. 9th St., Room 101, Anderson, IN 46016",
      phone="765-641-9419 (deductions staff: 765-641-9422 or 765-641-9505)", info="https://www.madisoncounty.in.gov/property-taxes-and-deductions",
      paper='Download the Homestead Standard/Supplemental form from the Auditor&rsquo;s <a href="https://www.madisoncounty.in.gov/auditors-office-resources" target="_blank" rel="noopener">Resources page</a>, then mail it or bring it in. The county mentions online filing, but its deduction links weren&rsquo;t working when we checked in November 2026.',
      status=("http://treasurer.madisoncounty48.us/cgi.exe?PAGEID=0003&CALL_PROGRAM=C009LIST", "Treasurer&rsquo;s property tax search", " (the Deductions/Exemptions section of each parcel)."),
      notes="The county asks for your Indiana driver&rsquo;s license and the last five digits of your Social Security number, plus the same for your spouse, and stresses adding your email address to the form."),
 dict(n="Morgan", office="Morgan County Auditor, 180 S. Main St., Suite 104, Martinsville, IN 46151",
      phone="765-342-1001", info="https://www.morgancounty.in.gov/293/Taxation",
      paper=f'Paper form (Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>), filed in person, by mail, by fax (765-342-1015) or by email to auditor@morgancounty.in.gov.',
      status=("https://lowtaxinfo.com/morgancounty", "LowTaxInfo", ": each parcel&rsquo;s Property Details shows &ldquo;Homestead Credit Filed?&rdquo;"),
      notes="Mailing it? The county asks you to include a phone number and a self-addressed, stamped envelope for your receipt."),
 dict(n="Shelby", office="Shelby County Auditor, County Annex, 25 W. Polk St., Room 104, Shelbyville, IN 46176 (the Annex is open Monday&ndash;Thursday)",
      phone="317-392-6310", info="https://www.in.gov/counties/shelby/auditor/auditor-tax-deduction-forms/",
      paper=f'No online filing. Shelby&rsquo;s forms page doesn&rsquo;t include the homestead form, so use Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a> and file it with the Auditor.',
      status=("http://auditor.shelby.in.datapitstop.us/cgi.exe?PAGEID=0013&CALL_PROGRAM=C009LIST", "Auditor&rsquo;s property tax search", " (the Deductions/Exemptions section of each parcel)."),
      notes="Call ahead if you plan to mail or email the form; the county site doesn&rsquo;t say."),
 dict(n="Bartholomew", office="Bartholomew County Auditor, Deductions Department (1st floor), 440 3rd St., Columbus, IN 47201",
      phone="812-379-1510", info="https://bartholomew.in.gov/auditor",
      paper='Paper form. The Auditor&rsquo;s page posts the current homestead claim form; questions go to deductions@bartholomew.in.gov.',
      status=None, status_text="Ask the Deductions Department, or check the deductions listed on your latest tax bill.",
      notes="Any time a parcel&rsquo;s ownership changes, the county asks you to check with the Deductions Department so your deductions continue."),
 dict(n="Brown", office="Brown County Auditor, 201 Locust Lane, 1st floor, Nashville, IN 47448 (mail: P.O. Box 37, Nashville, IN 47448)",
      phone="812-988-5485", info="https://browncounty-in.gov/158/Auditor",
      paper=f'Paper form, filed in person or by mail. Brown&rsquo;s posted form is an older version, so use the current Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>.',
      status=None, status_text="Call the Auditor, or check the deductions listed on your latest tax bill.",
      notes="Deductions go through the Auditor, not the Assessor. Brown&rsquo;s Assessor FAQ still lists an older December 31 date."),
 dict(n="Decatur", office="Decatur County Auditor, Decatur County Courthouse, 150 Courthouse Square, Suite 133, Greensburg, IN 47240",
      phone="812-663-2570", info="https://decaturcounty.in.gov/auditor/",
      paper=f'No online filing, and the county doesn&rsquo;t post the form. Take Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a> to the Auditor&rsquo;s office.',
      status=None, status_text="Call the Auditor&rsquo;s office.", notes=""),
 dict(n="Jackson", office="Jackson County Auditor&rsquo;s Office, 111 S. Main St., Brownstown, IN 47220",
      phone="812-358-6161", info="https://www.jacksoncounty.in.gov/government/departments_a-h/auditor/homestead_credit_and_standard_deduction.php",
      paper=f'File at the Auditor&rsquo;s office. The county doesn&rsquo;t post the form, so bring Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>.',
      status=("https://lowtaxinfo.com/jacksoncounty", "LowTaxInfo", ": each parcel shows &ldquo;Homestead Credit Filed?&rdquo;"),
      notes="Jackson&rsquo;s deduction pages are out of date (one still says May 10). Go by the state&rsquo;s January 15 rule and file early."),
 dict(n="Jennings", office="Jennings County Auditor, 200 E. Brown St., Vernon, IN 47282 (mail: P.O. Box 383, Vernon, IN 47282)",
      phone="812-352-3016", info="https://jenningscounty-in.gov/auditor-home",
      paper=f'No online portal, but Jennings takes completed forms by email at CDAuditor@jenningscounty-in.gov (subject: &ldquo;Completed Form Submission&rdquo;), by mail or in person. Its posted form is an older version, so use the current Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>.',
      status=("https://jenningsin.wthgis.com/", "Jennings County GIS", ": open your parcel and click the Deductions tab."),
      notes=""),
 dict(n="Montgomery", office="Montgomery County Auditor, Government Center, 1580 Constitution Row, Suite A, Crawfordsville, IN 47933 (the office moved out of the courthouse)",
      phone="765-364-6400", info="https://www.montgomerycounty.in.gov/1195/Property-Tax-Deductions",
      paper=f'No online filing. The county says deductions are filed in the Auditor&rsquo;s office and doesn&rsquo;t post the homestead form, so bring Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>.',
      status=None, status_text="Call the Auditor&rsquo;s office.", notes="Hours are Monday&ndash;Friday, 8 a.m.&ndash;4:30 p.m."),
 dict(n="Parke", office="Parke County Auditor, 116 W. High St., Room 104, Rockville, IN 47872",
      phone="765-569-3422", info="https://www.in.gov/counties/parke/auditors-office/",
      paper=f'No online filing, and the county site doesn&rsquo;t post deduction forms. Use Form HC10 from the <a href="{STATE_FORM}" target="_blank" rel="noopener">state forms site</a>, or email auditor@parkecounty.in.gov.',
      status=("http://auditor.parkecounty61.us/cgi.exe?CALL_PROGRAM=C009LIST", "Auditor&rsquo;s property tax search", " (the Deductions/Exemptions section of each parcel)."),
      notes="Hours are Monday&ndash;Friday, 8 a.m.&ndash;4 p.m."),
 dict(n="Putnam", office="Putnam County Auditor, Courthouse (2nd floor), 1 W. Washington St., Room 20, Greencastle, IN 46135",
      phone="765-653-5513, option 1", info="https://co.putnam.in.us/auditor/exemptions",
      online=("https://portal.sbsportals.com/modules/internet-service-request.php?guid=IH36E33F", "Putnam County Auditor Online Deductions Process",
              ". Choose Homestead Deduction; you can sign online and upload documents, and track your request there too."),
      status=("https://lowtaxinfo.com/putnamcounty", "LowTaxInfo", ", the Treasurer&rsquo;s tax search."),
      notes="Courthouse offices close for lunch, noon&ndash;1 p.m."),
]


def _slug(n):
    return n.lower() + "-county"


def _county(c):
    a = lambda u, t: f'<a href="{_h.escape(u)}" target="_blank" rel="noopener">{t}</a>'
    li = []
    if c.get("online"):
        u, nm, how = c["online"]
        li.append(f"<li><strong>File online:</strong> {a(u, nm)}{how}</li>")
    else:
        li.append(f"<li><strong>How to file:</strong> {c['paper']}</li>")
    li.append(f"<li><strong>Where:</strong> {c['office']}</li>")
    li.append(f"<li><strong>Phone:</strong> {c['phone']}</li>")
    if c.get("status"):
        u, nm, tail = c["status"]
        li.append(f"<li><strong>Already filed?</strong> Check {a(u, nm)}{tail}</li>")
    else:
        li.append(f"<li><strong>Already filed?</strong> {c['status_text']}</li>")
    if c.get("notes"):
        li.append(f"<li><strong>Good to know:</strong> {c['notes']}</li>")
    s = _slug(c["n"])
    return (f' <h3 id="{s}">{c["n"]} County</h3>\n <ul>\n  ' + "\n  ".join(li) + "\n </ul>\n"
            f' <p style="font-size:.9rem;">Official county page: {a(c["info"], c["n"] + " County Auditor")} &middot; '
            f'Buying or selling here? See our <a href="/counties/{s}-indiana-real-estate/">{c["n"]} County real estate guide</a>.</p>\n')


JUMP = " &middot; ".join(f'<a href="#{_slug(c["n"])}">{c["n"]}</a>' for c in COUNTIES)
COUNTY_HTML = "\n".join(_county(c) for c in COUNTIES)

POST = dict(
 slug="how-to-file-homestead-deduction-indiana-by-county",
 title="How to File the Indiana Homestead Exemption, by County",
 headline="How to File for the Indiana Homestead Deduction, County by County",
 crumb="How to File the Homestead Deduction",
 h1_html="How to File Your Indiana Homestead Deduction: <em>County by County</em>",
 desc=("Where and how to file Indiana's homestead deduction in Marion, Hamilton, Hendricks, Johnson and 13 more "
       "counties, plus the January 15 deadline."),
 date="2026-11-19", modified="2026-11-19", month="November 2026",
 category="Buying a Home", eyebrow="PROPERTY TAXES",
 focus="how to file homestead exemption indiana",
 hero_sub=("Just bought a home? Filing is free, you only do it once, and it&rsquo;s the biggest property "
           "tax break most Indiana homeowners get. Here&rsquo;s exactly where to file in 17 counties."),
 badges=["Property Taxes", "Deadline: January 15", "17 Counties"],
 read_min=12,
 card_title="How to File Your Homestead Deduction",
 card_sub="Where to file in 17 Indiana counties, and the January 15 deadline.",
 qa_heading="Filing the Indiana Homestead Deduction at a Glance",
 qa_lead=("<strong>How do I file for the homestead deduction in Indiana?</strong> File State Form 5473 (Form HC10), or "
          "your county&rsquo;s online version, with the auditor of the county where the home is. It must be filed or "
          "postmarked by January 15 of the year the taxes are due, and you file once, not every year."),
 qa_facts=[
  ("Where", "The county auditor where the home is located"),
  ("Form", "State Form 5473 (Form HC10), or the county&rsquo;s online form"),
  ("Deadline", "Filed or postmarked by January 15 of the year the taxes are due"),
  ("You&rsquo;ll need", "Legal names, last 5 digits of your SSN (and your spouse&rsquo;s), parcel number"),
  ("Cost", "Free"),
  ("Re-file?", "Only when ownership or the deed changes, not every year"),
 ],
 toc=[("qualify", "Before You File: Who Qualifies"), ("deadline", "The Deadline: January 15"),
      ("need", "What You&rsquo;ll Need"), ("closing", "Did Your Title Company Already File It?"),
      ("counties", "How to File in Each County"), ("changes", "When You Move, Rent It Out or Change the Deed"),
      ("other", "Other Deductions You File Separately"), ("faq", "FAQ")],
 body=f"""
 <p>The homestead deduction is the single biggest property tax break most Indiana homeowners get, and it isn&rsquo;t automatic. You have to file for it, once, with the county auditor. Plenty of buyers assume the title company handled it at closing and find out a year later, when the first full tax bill arrives, that it didn&rsquo;t happen.</p>
 <p>This guide covers the filing itself: the deadline, what you&rsquo;ll need, and where to file in each of the 17 counties we serve, with links to each county&rsquo;s online form or paper process. For what the deduction is worth and how it&rsquo;s changing through 2031, see our <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">Indiana homestead exemption explainer</a>.</p>
 <p><em>This is general information, not tax or legal advice. County procedures change; confirm details with your county auditor or the Indiana Department of Local Government Finance (<a href="https://www.in.gov/dlgf/" target="_blank" rel="noopener">in.gov/dlgf</a>).</em></p>

 <h2 id="qualify">Before You File: Who Qualifies</h2>
 <p>Indiana law calls it the homestead standard deduction (most people say &ldquo;homestead exemption&rdquo;). You qualify if the home is your principal place of residence in Indiana and you:</p>
 <ul>
  <li><strong>Own it,</strong> or are buying it under a contract recorded with the county recorder that makes you responsible for the property taxes.</li>
  <li><strong>Actually live there when you sign the form.</strong> The state form says you must be using the property as your principal residence at the time of signing, so file after you move in, not before.</li>
  <li><strong>Don&rsquo;t claim another homestead.</strong> Only one individual or married couple can receive the deduction on a home, and a person or couple can&rsquo;t claim two homes in the same year.</li>
 </ul>
 <p>The deduction covers the house, one garage and up to one acre around it. Any part of the home that produces income, such as the other side of a duplex you rent out or a shop run out of the garage, doesn&rsquo;t qualify. Homes owned through a trust or an LLC can qualify in some cases; the county will ask for documents.</p>

 <h2 id="deadline">The Deadline: January 15</h2>
 <p>The current state form (State Form 5473, revised July 2025) says the application must be completed, dated and filed or postmarked with the county auditor <strong>on or before January 15 of the year the property taxes are first due</strong>. Once approved, it applies that year and every year after while you still qualify.</p>
 <p>In practice: if you close and move in during 2026, file by January 15, 2027, and the deduction applies to the property taxes you pay in 2027. Miss it, and you pay that year&rsquo;s taxes without the deduction; file anyway and it starts the following year.</p>
 <p><strong>Don&rsquo;t cut it close.</strong> Several county websites still show December 31 or January 5, dates from older versions of the rule, and one shows May 10. The safest move is to file the week you move in. If you&rsquo;re closing in late December, aim to file before the new year.</p>

 <h2 id="need">What You&rsquo;ll Need</h2>
 <p>Online or on paper, the form asks for the same things:</p>
 <ul>
  <li><strong>Legal names</strong> of you and your spouse, if married.</li>
  <li><strong>The last five digits of each person&rsquo;s Social Security number.</strong> If you don&rsquo;t have one, the last five digits of a driver&rsquo;s license or state ID and the issuing state. State law keeps these numbers confidential.</li>
  <li><strong>Your parcel number,</strong> which is on your closing documents and the county&rsquo;s property search. Most online forms let you look it up by address.</li>
  <li><strong>Any homestead you&rsquo;re leaving.</strong> The form asks whether you own property elsewhere and the address of a homestead you&rsquo;re vacating.</li>
  <li><strong>An email address</strong> for online filing, so you get a confirmation. Save it.</li>
 </ul>

 <h2 id="closing">Did Your Title Company Already File It?</h2>
 <p>In many Indiana closings, the title company includes the homestead application in your closing paperwork and sends it to the auditor. Johnson County even says your closing company normally files it for you. But it doesn&rsquo;t always happen, and Hancock County specifically asks owners to confirm that forms filed by title companies, lenders or agents went in on time.</p>
 <p>So check. Most counties below have an online lookup that shows whether your parcel has the deduction filed. If it isn&rsquo;t there a few weeks after closing, file it yourself. Filing a duplicate is far better than missing a year. It&rsquo;s on our <a href="/services/buyer-closing-checklist/">buyer closing checklist</a> for exactly this reason.</p>

 <h2 id="counties">How to File in Each County</h2>
 <p>Every county below was checked against its official website in November 2026. Jump to yours:</p>
 <p>{JUMP}</p>
{COUNTY_HTML}
 <h2 id="changes">When You Move, Rent It Out or Change the Deed</h2>
 <ul>
  <li><strong>You don&rsquo;t re-file every year.</strong> The Indiana DLGF says deductions carry over; you reapply only when the property is sold or the title changes.</li>
  <li><strong>Re-file when the deed changes.</strong> Adding or removing an owner, a marriage or divorce that changes the title, or moving the home into a trust can all require a new application. Refinancing alone doesn&rsquo;t.</li>
  <li><strong>Tell the auditor within 60 days if you stop qualifying.</strong> If you move out or turn the home into a rental, file a certified statement with the county auditor (the state&rsquo;s <a href="{CHANGE_FORM}" target="_blank" rel="noopener">Homestead Deduction Change of Use Form</a>). Miss the 60 days and you owe back the deduction plus a 10% civil penalty.</li>
  <li><strong>Moving mid-year?</strong> If you move from one Indiana homestead to another after the January 1 assessment date, the old home keeps its deduction for that tax cycle, and you can apply on the new one for the same cycle. The old one comes off the next year.</li>
 </ul>

 <h2 id="other">Other Deductions You File Separately</h2>
 <p>The supplemental homestead deduction comes with the standard deduction: the state form says the county auditor applies it for you. Other benefits need their own application with the same auditor, including the over-65 deduction and credit, the blind or disabled deduction and the disabled veteran deductions. See <a href="/blog/indiana-property-tax-deductions-seniors/">Indiana property tax deductions for seniors</a> for those, and <a href="/blog/indiana-property-tax-caps-explained/">Indiana property tax caps explained</a> for how the 1% homestead cap works.</p>
 <p>Buying a home and want a team that keeps track of these steps for you? That&rsquo;s part of working with our agents, from the offer through the first tax bill.</p>
""",
 faqs=[
  ("When is the deadline to file for the homestead deduction in Indiana?",
   "The current state form says the application must be completed, dated and filed or postmarked with the county auditor on or before January 15 of the year the property taxes are first due. If you close and move in during 2026, file by January 15, 2027 for the deduction to apply to taxes paid in 2027. Some county websites still list older dates, so file as soon as you move in."),
  ("Do I have to file for the homestead deduction every year?",
   "No. Once it's approved, the deduction carries over each year while you own and live in the home. You reapply only if the property is sold or the title changes, such as adding or removing an owner or moving the home into a trust. Refinancing alone doesn't require a new application."),
  ("Can I file for the homestead deduction online in Indiana?",
   "In most of the Indianapolis area, yes. Marion, Hamilton, Hendricks, Johnson and Hancock counties all have online filing, as does Putnam County. Boone, Morgan and several smaller counties use the paper state form (Form HC10), filed in person, by mail and in some counties by email."),
  ("How do I know if my homestead deduction was filed at closing?",
   "Check your county's property or tax lookup, which in most counties shows whether a parcel has the homestead deduction. Your property tax bill also lists the deductions applied. If it isn't there a few weeks after closing, call the county auditor or file it yourself."),
  ("What happens if I miss the January 15 deadline?",
   "You pay that year's property taxes without the deduction. File anyway: the application then applies to the following year's taxes and every year after while you qualify."),
  ("Do I need a separate form for the supplemental homestead deduction?",
   "No. The state form says the county auditor applies the supplemental deduction for anyone who qualifies for the standard homestead deduction. Over-65, disability and veteran deductions do need their own applications."),
 ],
 sources=[
  ("Indiana DLGF, State Form 5473 / Form HC10 (R21 / 7-25)", STATE_FORM),
  ("Indiana DLGF, Deductions and Credits", "https://www.in.gov/dlgf/deductions-and-credits/"),
  ("Indiana DLGF, Homestead Deduction Change of Use Form", CHANGE_FORM),
   ("County auditor and treasurer websites for the 17 counties above (checked November 2026)", "#counties"),
 ],
 related=[
  ("/blog/indiana-homestead-exemption-lower-property-taxes/", "Indiana Homestead Exemption Explained"),
  ("/blog/indiana-property-tax-deductions-seniors/", "Indiana Property Tax Deductions for Seniors"),
  ("/blog/indiana-property-tax-caps-explained/", "Indiana Property Tax Caps Explained"),
 ],
 cta=("Buying a Home in Central Indiana?",
      "Our agents walk you through every step, from the offer to closing to making sure your homestead deduction is filed.",
      [("/schedule/", "Schedule a Free Consultation &rarr;", "btn-white"), ("/services/home-buying-process/", "The Home Buying Process", "btn-outline")]),
 resources=[
  ("/services/buyer-closing-checklist/", "Buyer Closing Checklist"),
  ("/glossary/homestead-exemption/", "Homestead Exemption (Glossary)"),
  ("/services/closing-costs-buyers/", "Closing Costs for Buyers"),
  ("/services/first-time-home-buyers/", "First-Time Home Buyers"),
 ],
 about={"@type": "State", "name": "Indiana"},
 link_from=[
  ("blog/indiana-property-tax-deductions-seniors/index.html",
   '<strong>Filing the homestead deduction first?</strong> Here&rsquo;s <a href="/blog/how-to-file-homestead-deduction-indiana-by-county/">how to file the Indiana homestead deduction in each county</a>, with online links and the January 15 deadline.'),
  ("blog/indiana-property-tax-caps-explained/index.html",
   '<strong>Haven&rsquo;t filed your homestead yet?</strong> The 1% cap only applies once it&rsquo;s on file. Here&rsquo;s <a href="/blog/how-to-file-homestead-deduction-indiana-by-county/">how to file the homestead deduction in each Indiana county</a>.'),
 ],
)
