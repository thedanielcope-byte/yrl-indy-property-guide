"""Moving to Indiana checklist for new residents (Nov 2026).

Facts and sources (checked Nov 3 2026):
- Indiana BMV, New Indiana Residents page: 60 days to get an Indiana driver's license with a valid
  out-of-state license (surrender it); vision screening 18+; knowledge exam if expired; skills test
  if expired 5+ years or held less than 1 year; 30-day temporary license while documents are verified;
  60 days to apply for a vehicle title (or submit State Form 1014), late filing = administrative
  penalty; VIN inspection at a branch, or law enforcement completes State Form 39530; title needs
  the certificate of title, proof of address within 60 days, SSN/FIN proof and proof of insurance.
- Indiana BMV New Resident Packet (InDesign stamp ~Feb 2023): new residents required to obtain a
  Real ID (RealID.IN.gov); one proof of identity, one of lawful status, full-SSN proof (card or W-2),
  two proofs of Indiana residency (USPS change-of-address confirmation; utility, credit card,
  doctor or hospital bill issued within 60 days); Indiana Residency Affidavit in limited cases;
  residency date given at title transfer "for tax proration purposes"; electronic-title states:
  request a printed title; lienholder: Request for Title, optional paid 30-day permit.
- Indiana BMV Excise Tax Information: annual excise tax + registration fee at registration; based on
  vehicle class (manufacturer's original retail price) and age. County excise surtax / wheel tax only
  where adopted (BMV county excise and wheel tax page).
- IDEM: vehicle emissions testing applies only in Lake and Porter counties.
- Indiana Secretary of State voter resources: register at least 29 days before election day;
  online at IndianaVoters.com, by mail, or in person at a BMV branch or county office; register at
  the address of your permanent residence.
- Indiana DOR current individual forms: part-year residents file IT-40PNR (2025 form current).
  DOR Departmental Notice #1 (2026): county of residence / principal work determined on Jan. 1;
  out-of-state on Jan. 1 but working in an Indiana county -> that county's rate; state rate 2.95%;
  Form WH-4 for withholding. County rates as in fresh_posts/cost-of-living-in-indianapolis.py.
- Indiana DLGF: deduction applications go to the county auditor; filing by Jan 15 2026 applied to
  the 2025 pay 2026 bill; June 2024 memo (HEA 1120-2024) set the Jan 15 deadline; due dates May/Nov.
  IC 6-1.1-12-44: the sales disclosure form can serve as the deduction application.
- Indiana PLA: professional license transfers handled board by board.
Not used (could not verify or out of scope): school voucher details, pet rules, a REAL ID page fetch
(RealID.IN.gov did not load from here), specific excise dollar amounts.
"""

BMV_NEW = "https://secure.in.gov/bmv/licenses-permits-ids/new-indiana-residents"
BMV_PACKET = "https://www.in.gov/bmv/files/new-resident-packet.pdf"

BODY = """
 <p>Moving to Indiana comes with a short list of state deadlines, and the one that catches most newcomers is the BMV&rsquo;s 60-day clock for your driver&rsquo;s license and vehicle titles. Here&rsquo;s what to do and when, from the week before you move to your first Indiana tax return, with links to the official state pages. If you&rsquo;re still deciding where to live, start with our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> and our <a href="/blog/cost-of-living-in-indianapolis/">cost of living breakdown</a>. Rules change; check the linked state pages before you act.</p>

 <h2 id="before-you-move">Before You Move</h2>
 <p>A little paperwork up front saves a second trip to the BMV. The Indiana Bureau of Motor Vehicles asks new residents for one proof of identity (such as an unexpired U.S. passport or a certified birth certificate), one proof of lawful status, one document showing your <strong>full</strong> Social Security number (your card or a W-2), and <strong>two proofs of Indiana address</strong>. A U.S. Postal Service change-of-address confirmation counts, as does a utility, credit card, doctor or hospital bill issued within the last 60 days. If your name has changed, bring the name-change documents too.</p>
 <p>Two other things to start early:</p>
 <ul>
 <li><strong>A car loan.</strong> If a lender holds your title, the BMV can send its Request for Title form to your lienholder, and you can buy a 30-day permit if your old registration runs out while you wait.</li>
 <li><strong>A professional license.</strong> Nurses, real estate agents, cosmetologists and other licensed professionals transfer through their board at the <a href="https://www.in.gov/pla/" target="_blank" rel="noopener">Indiana Professional Licensing Agency</a>. Each board sets its own rules and timelines, so check yours before your start date.</li>
 </ul>

 <h2 id="bmv">Get Your Indiana Driver&rsquo;s License Within 60 Days</h2>
 <p>If you hold a valid license from another state, you have <strong>60 days</strong> after moving to get an Indiana driver&rsquo;s license, and you surrender your old one when you apply. Adults with a valid out-of-state license need to pass a vision screening. If your license has expired, you&rsquo;ll take the knowledge exam, and if it expired more than five years ago, or you&rsquo;ve held a valid license for less than a year, you&rsquo;ll take a driving skills test as well. The BMV issues a temporary license, valid for 30 days, while it verifies your documents.</p>
 <p>The BMV&rsquo;s new-resident packet says new residents are required to get a <strong>Real ID</strong>, and the full list of accepted documents is at RealID.IN.gov. If you can&rsquo;t produce two proofs of address yet, for example because you&rsquo;re staying with family while you house-hunt, the BMV accepts an Indiana Residency Affidavit in a few specific situations, such as living with a relative or friend who signs it at the branch.</p>

 <h2 id="vehicles">Title and Register Your Vehicles Within 60 Days</h2>
 <p>You also have <strong>60 days</strong> after becoming a resident to apply for an Indiana title for each vehicle with an out-of-state title, or to submit the Request for Title form if a lender holds it. Miss the window and the BMV charges an administrative penalty. Plan on a branch visit with:</p>
 <ul>
 <li>Your most recent title (if your old state issues electronic titles, request a printed copy first)</li>
 <li>Proof of address dated within the last 60 days, proof of your Social Security number and proof of insurance</li>
 <li>The vehicle itself, for a VIN inspection at the branch (if you can&rsquo;t bring it, a law enforcement officer can complete the inspection form instead)</li>
 <li>The date you moved to Indiana, which the BMV uses to prorate your taxes</li>
 </ul>
 <p>When you register, you&rsquo;ll pay Indiana&rsquo;s annual <strong>vehicle excise tax</strong> plus a registration fee. The excise tax is based on the vehicle&rsquo;s class, set by its original manufacturer&rsquo;s retail price, and its age, and some counties add a county excise surtax or wheel tax on top. The BMV&rsquo;s fees and taxes pages list the current amounts.</p>
 <p>One thing you can skip: Central Indiana has no vehicle emissions test. Indiana requires testing only in Lake and Porter counties in the northwest corner of the state, according to the Indiana Department of Environmental Management.</p>

 <h2 id="voting">Register to Vote</h2>
 <p>You can register online at IndianaVoters.com, by mail, or in person at a BMV branch or your county voter registration office, so it&rsquo;s easy to handle during your license visit. To vote in an election, you need to register at least <strong>29 days before election day</strong>, at the address of your permanent residence (Indiana Secretary of State).</p>

 <h2 id="taxes">Indiana Income Tax in the Year You Move</h2>
 <p>Indiana&rsquo;s state income tax is a flat <strong>2.95%</strong> for 2026, plus a county income tax. For the year you move, you&rsquo;ll file Indiana&rsquo;s part-year resident return, <strong>Form IT-40PNR</strong>, which covers the income you received while living in Indiana plus any Indiana-source income, and you&rsquo;ll likely file a part-year return in your old state too. Give your new employer an Indiana Form WH-4 so the right state and county tax comes out of your paycheck.</p>
 <p>County tax runs on a January 1 rule. According to the Indiana Department of Revenue, your county is the one you lived in on January 1 of the tax year, or, if you lived out of state on January 1, the Indiana county where you worked. Rates vary a lot around Indianapolis: from 1.10% in Hamilton County to 2.72% in Morgan County, with Marion County at 2.02% (our <a href="/blog/cost-of-living-in-indianapolis/">cost of living breakdown</a> has the county table). Talk to a tax professional about your situation, especially if you still have income or property in your old state.</p>

 <h2 id="homestead">Bought a Home? File the Homestead Deduction by January 15</h2>
 <p>If you buy a home you&rsquo;ll live in, the homestead deduction is the biggest property tax saver you have. It lowers your home&rsquo;s taxable value and keeps your bill under Indiana&rsquo;s <a href="/blog/indiana-property-tax-caps-explained/">1% property tax cap</a>. You apply through your county auditor, and the deadline is <strong>January 15</strong>; the Department of Local Government Finance gives the example that a deduction filed by January 15, 2026 applied to the 2025 pay 2026 bill. When you buy, the Sales Disclosure Form your title company prepares at closing can double as your homestead application under Indiana law (IC 6-1.1-12-44), so make sure that part is filled in. Our <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">Indiana homestead deduction guide</a> walks through it.</p>
 <p>Indiana property taxes are paid a year behind and are due in two installments, in May and November. Our guide to <a href="/blog/buying-a-house-in-winter-indianapolis/">buying a house in winter</a> explains how that lag is handled at closing.</p>

 <h2 id="utilities-schools">Utilities, Mail and Schools</h2>
 <p>Set up electricity, gas, water and sewer, trash and internet before closing day or move-in, so you aren&rsquo;t waiting on service. In most of Central Indiana that means AES Indiana or Duke Energy for electricity, Citizens Energy Group or CenterPoint Energy for gas, and Citizens Water or your town&rsquo;s utility for water. Our <a href="/utilities/">utilities guide</a> lists the providers town by town. Your first Indiana utility bill also counts as one of your two proofs of address at the BMV, and so does your Postal Service change-of-address confirmation, so file that before you move.</p>
 <p>Public schools enroll by address, and many Indianapolis addresses are served by township school districts rather than Indianapolis Public Schools. Confirm the district for a specific address before you buy, then contact that district to enroll. Our <a href="/schools/">Central Indiana schools guide</a> covers every district.</p>

 <h2 id="checklist">Your Moving to Indiana Checklist</h2>
 <h3>Before you move</h3>
 <ol>
 <li>Gather your BMV documents: passport or certified birth certificate, Social Security card or W-2, and any name-change papers.</li>
 <li>If you have a car loan, ask your lender how they handle an out-of-state title transfer.</li>
 <li>Check professional license transfer rules with your Indiana board.</li>
 <li>Schedule utility start dates for your new address.</li>
 <li>File a change of address with the U.S. Postal Service and keep the confirmation.</li>
 </ol>
 <h3>First 30 days</h3>
 <ol>
 <li>Give your employer an Indiana Form WH-4.</li>
 <li>Keep your first Indiana utility bill as a second proof of address.</li>
 <li>Register to vote at IndianaVoters.com (at least 29 days before any election you want to vote in).</li>
 <li>Enroll your kids in school once you&rsquo;ve confirmed your district.</li>
 </ol>
 <h3>First 60 days</h3>
 <ol>
 <li>Get your Indiana driver&rsquo;s license or state ID (a Real ID) at a BMV branch.</li>
 <li>Title and register every vehicle, including the VIN inspection, and pay the excise tax and registration fee.</li>
 </ol>
 <h3>By January 15</h3>
 <ol>
 <li>If you bought a home, confirm your homestead deduction was filed with the county auditor, either through the Sales Disclosure Form at closing or a separate application.</li>
 </ol>
 <h3>At tax time</h3>
 <ol>
 <li>File Indiana Form IT-40PNR for the year you moved, plus your old state&rsquo;s part-year return.</li>
 </ol>

 <h2 id="our-take">Our Take</h2>
 <p>None of this is complicated, but the deadlines stack up during a busy month. If you bring the right documents, one BMV visit can cover your license, your vehicle titles and your voter registration. If you&rsquo;re buying, file the homestead deduction early, since it&rsquo;s the one item on this list that saves you money every year. Our team helps out-of-state buyers find the right part of the metro, tour homes by video and close remotely; see our <a href="/services/relocation-buyers/">relocation services</a>, read how <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">virtual home tours</a> work, or <a href="/schedule/">book a call with our team</a>. Once you&rsquo;re in, our <a href="/blog/new-homeowner-checklist-after-closing-indianapolis/">new homeowner checklist</a> covers the house itself.</p>
"""

POST = dict(
 slug="moving-to-indiana-checklist",
 title="Moving to Indiana Checklist: BMV, Taxes and Homestead",
 headline="Moving to Indiana Checklist: BMV, Taxes, Homestead and Utilities",
 h1_html="Moving to Indiana Checklist: <em>BMV, Taxes, Homestead and Utilities</em>",
 desc=("New to Indiana? A checklist for the 60-day BMV deadline, vehicle titles, voter registration, "
       "move-year taxes, the homestead deduction and utilities."),
 date="2026-11-03", month="November 2026",
 category="Relocation", eyebrow="RELOCATION",
 focus="moving to indiana checklist",
 hero_sub="What to do, and by when, after you move to Indiana: your driver&rsquo;s license and vehicle titles at the BMV, voter registration, income tax for the year you move, the homestead deduction and utilities.",
 badges=["Relocation", "New Residents", "Updated for 2026"],
 read_min=7,
 card_title="Moving to Indiana Checklist",
 card_sub="BMV deadlines, taxes, homestead and utilities, in order.",
 qa_heading="Moving to Indiana at a Glance",
 qa_lead=("<strong>What do you need to do after moving to Indiana?</strong> Get an Indiana driver&rsquo;s license and title "
          "and register your vehicles within <strong>60 days</strong> of becoming a resident, register to vote at least 29 days "
          "before the next election, file a part-year Indiana income tax return for the year you move, and, if you buy a home, "
          "file the homestead deduction by January 15."),
 qa_facts=[
  ("Driver&rsquo;s license", "Within 60 days of moving (Indiana BMV)"),
  ("Vehicle title &amp; registration", "Within 60 days (Indiana BMV)"),
  ("Voter registration", "At least 29 days before an election"),
  ("Move-year tax return", "Form IT-40PNR (part-year resident)"),
  ("Homestead deduction", "File by January 15 (county auditor)"),
  ("Emissions test", "Only in Lake and Porter counties"),
 ],
 toc=[("before-you-move", "Before You Move"), ("bmv", "Driver&rsquo;s License (60 Days)"), ("vehicles", "Vehicle Title and Registration"),
      ("voting", "Register to Vote"), ("taxes", "Income Tax the Year You Move"), ("homestead", "Homestead Deduction"),
      ("utilities-schools", "Utilities, Mail and Schools"), ("checklist", "The Checklist"), ("our-take", "Our Take"), ("faq", "FAQ")],
 body=BODY,
 faqs=[
  ("How long do I have to get an Indiana driver's license after moving?",
   "If you hold a valid license from another state, you have 60 days after moving to get an Indiana driver's license, according to the Indiana BMV. You surrender your old license when you apply, adults pass a vision screening, and the BMV gives you a temporary license valid for 30 days while it verifies your documents."),
  ("How long do I have to register my car in Indiana after moving?",
   "You have 60 days after becoming an Indiana resident to apply for an Indiana title for each vehicle with an out-of-state title, and late filing brings an administrative penalty. Bring your title, proof of address, proof of your Social Security number and proof of insurance, and bring the vehicle for a VIN inspection. You'll pay the annual vehicle excise tax and a registration fee when you register."),
  ("Does Indiana require emissions testing?",
   "Only in Lake and Porter counties in northwest Indiana, according to the Indiana Department of Environmental Management. Indianapolis and the rest of Central Indiana have no vehicle emissions test."),
  ("Do I pay Indiana income tax the year I move?",
   "Yes, on income you receive while living in Indiana plus any Indiana-source income. You file Indiana's part-year resident return, Form IT-40PNR. County income tax is based on where you lived on January 1, or where you worked in Indiana on January 1 if you lived out of state, so ask a tax professional how that applies to your move."),
  ("When do I file the homestead deduction in Indiana?",
   "File with your county auditor by January 15. The Indiana DLGF gives the example that a deduction filed by January 15, 2026 applied to the 2025 pay 2026 tax bill. If you buy a home, the Sales Disclosure Form completed at closing can serve as the application under IC 6-1.1-12-44."),
  ("How do I register to vote in Indiana?",
   "Register online at IndianaVoters.com, by mail, or in person at a BMV branch or your county voter registration office. You need to register at least 29 days before election day, at the address of your permanent residence."),
 ],
 sources=[
  ("Indiana BMV, new Indiana residents", BMV_NEW),
  ("Indiana BMV, new resident packet", BMV_PACKET),
  ("Indiana BMV, vehicle excise tax", "https://secure.in.gov/bmv/fees-taxes/vehicle-registration-fees-and-taxes/excise-tax-information/"),
  ("Indiana BMV, county excise and wheel taxes", "https://www.in.gov/bmv/fees-taxes/vehicle-registration-fees-and-taxes/county-vehicle-excise-tax-and-wheel-tax/"),
  ("IDEM, vehicle emissions testing program", "https://www.in.gov/idem/airquality/vehicle-emissions-testing-program/"),
  ("Indiana Secretary of State, voter resources", "https://www.in.gov/sos/civics/voters/voter-resources/"),
  ("Indiana DOR, individual tax forms (IT-40PNR)", "https://www.in.gov/dor/tax-forms/individual/current/"),
  ("Indiana DOR, Departmental Notice #1 (2026 county rates)", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana DLGF, deductions and credits", "https://www.in.gov/dlgf/deductions-and-credits/"),
  ("Indiana DLGF memo on the January 15 filing deadline (June 2024)", "https://in.gov/dlgf/files/2024-memos/240618-Shackle-Memo-Legislation-Affecting-Deductions-and-Exemptions.pdf"),
  ("Indiana DLGF, property tax due dates", "https://www.in.gov/dlgf/understanding-your-tax-bill/property-tax-due-dates/"),
  ("IC 6-1.1-12-44, sales disclosure form as a deduction application", "https://codes.findlaw.com/in/title-6-taxation/in-code-sect-6-1-1-12-44.html"),
  ("Indiana Professional Licensing Agency", "https://www.in.gov/pla/"),
 ],
 related=[
  ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
  ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
  ("/blog/new-homeowner-checklist-after-closing-indianapolis/", "New Homeowner Checklist After Closing"),
 ],
 cta=("Moving to Central Indiana?",
      "We help out-of-state buyers pick the right part of the metro, tour homes by video and close without extra trips. Tell us where you&rsquo;re coming from and your timeline.",
      [("/services/relocation-buyers/", "Explore Relocation Services →", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[
  ("/services/relocation-buyers/", "Relocation Buyers"),
  ("/utilities/", "Central Indiana Utilities Guide"),
  ("/schools/", "Central Indiana Schools"),
  ("/blog/indiana-homestead-exemption-lower-property-taxes/", "Indiana Homestead Deduction"),
 ],
 link_from=[
  ("blog/moving-to-indianapolis-relocation-guide/index.html",
   'Once you&rsquo;ve picked a home, our <a href="/blog/moving-to-indiana-checklist/">moving to Indiana checklist</a> covers the 60-day BMV deadline, voter registration, move-year taxes and the homestead deduction.'),
  ("blog/new-homeowner-checklist-after-closing-indianapolis/index.html",
   'New to the state as well as the house? See our <a href="/blog/moving-to-indiana-checklist/">moving to Indiana checklist</a> for BMV, tax and homestead deadlines.'),
 ],
 about={"@type": "State", "name": "Indiana"},
)
