"""Townhouse vs. condo explainer + where to find townhomes/condos around Indianapolis (Nov 2026).

Why: GSC Nov 2026 - "what is a townhouse" 178 impressions at pos 17.3, "townhouse" 56 at 9.3;
/glossary/townhouse/ 373 impressions at pos 22.

Facts and sources (checked Nov 19 2026):
- Indiana condominium law, IC 32-25, read via FindLaw ("current as of January 1, 2026"):
  32-25-1-1 (applies when the owner(s) submit property by executing and recording a declaration);
  32-25-2-4 (common areas and facilities, "unless otherwise provided in the declaration": land,
  foundations, roofs, halls, yards, parking, pools/recreation, central utilities, etc.);
  32-25-2-7 ("condominium" = real estate subjected to the article by recording condominium
  instruments, with undivided interests in the common areas vested in the unit owners);
  32-25-2-9 ("condominium unit" = enclosed space in a structure of one or more floors with an exit to
  a street or to a common space leading to one, plus the undivided interest in the common elements);
  32-25-4-1 (owner holds fee simple title, exclusive ownership and possession of the unit, plus an
  undivided interest in the common areas; units individually conveyed/encumbered);
  32-25-7-1 (declaration recorded with the county recorder: land, buildings, units, common and
  limited common areas, each unit's percentage interest, use restrictions; bylaws annexed; recorded
  floor plans referenced).
- History: IC 32-25 is the 2002 recodification of the Indiana Horizontal Property Act of 1963
  (IC 32-1-6). Source: Indiana Law Journal note, "Observations on Condominiums in Indiana: The
  Horizontal Property Act of 1963," 40 Ind. L.J. 57 (1964); Justia section histories show
  pre-2002 recodification citations to IC 32-1-6. The current article is titled "Condominiums",
  so the post says IC 32-25 "grew out of" the 1963 Horizontal Property Act rather than calling
  IC 32-25 itself the Horizontal Property Law.
- Insurance: no Indiana Department of Insurance consumer page on HO-6 found. Used state regulator
  explainers: Maryland Insurance Administration condo FAQ (HO-3 covers the entire structure; HO-6
  may only cover the interior and contents; master policy covers common areas, exterior, structure;
  loss assessment can cover the owner's share of an assessment or master deductible) and
  Washington OIC (master policy types: all-in, all-in excluding improvements, bare walls;
  certificate of insurance). Not Indiana-specific, so kept general.
- FHA: hud.gov FHA Condominiums page (Single-Unit Approval: unit in a project that is not
  FHA-approved; project complete, at least five dwelling units, not manufactured homes; public
  search of FHA-approved condos). HUD final rule "Project Approval for Single-Family Condominiums,"
  84 FR 41846 (Aug 15 2019), effective Oct 15 2019. FHA concentration limits and approval
  expiration not stated (conflicting/older sources).
- VA: va.gov purchase loan page lists "Buy a condo in a VA-approved project." VA Lender's Handbook
  ch. 16 (condos, not PUDs, need VA approval) seen only in search snippets, could not open it, so
  the post makes no VA-PUD claim.
- Conventional: Fannie Mae Selling Guide B4-2.1-01 and B4-2.1-02 (topics dated 08/05/2026):
  attached units in condo projects need Full Review (Condo Project Manager), Fannie Mae PERS review,
  or (established projects) FHA project approval; review waived for detached condo units, 2-4 unit
  projects, 5-10 unit projects not part of a larger development/master association, and PUD units.
  Freddie Mac: condo project review requirements in Guide ch. 5701; Condo Project Advisor tool.
- HOA disclosure at sale (IC 32-21-5-8.5, 10 days before closing): already covered in
  /blog/indiana-seller-disclosure-form/, linked rather than repeated.
- No HOA dollar ranges used.
- Communities: ONLY from communities.json (types/highlights mentioning townhomes or condos); every
  linked /communities/<slug>/ page exists. Descriptions paraphrase that data. The post tells
  readers to confirm ownership type per home; it makes no claim about any community's legal form.
- Search: inject_search_query.py verifies town, ZIP, street address and MLS # only; no
  property-type URL filter is claimed.
General information, not legal advice.
"""

BODY = """
 <p>&ldquo;Townhouse&rdquo; and &ldquo;condo&rdquo; get used as if they mean the same thing, but they answer two different questions. <strong>Townhouse</strong> describes what a home looks like: attached, usually two or three stories, sharing walls with its neighbors. <strong>Condo</strong> describes how a home is owned. That difference shapes what you own, your HOA dues, your insurance and your loan. Here&rsquo;s how it works in Indiana, and where to find both around Indianapolis.</p>
 <p><em>This is general information, not legal advice; for questions about a specific property, talk to a real estate attorney or your title company.</em> Statute references are to the 2026 Indiana Code.</p>

 <h2 id="difference">The Core Difference: A Building Style vs. a Form of Ownership</h2>
 <h3>What is a townhouse?</h3>
 <p>A townhouse (or townhome; the terms are interchangeable) is an architectural style: a multi-level home attached to one or more neighbors by shared side walls, with its own front door and nobody living above or below you. In most Central Indiana townhome communities you own the home <strong>fee simple</strong>, meaning the structure and the small lot under it, much like a detached house. An HOA typically owns and maintains the common areas, and some also handle lawn care, snow removal or exterior work. Our <a href="/glossary/townhouse/">townhouse glossary entry</a> covers the basics.</p>
 <h3>What is a condo?</h3>
 <p>A condominium is a legal form of ownership, not a building style. Indiana&rsquo;s condominium law, <strong>IC 32-25</strong>, grew out of the state&rsquo;s Horizontal Property Act of 1963, and property becomes a condo only when its owner records a declaration submitting it to that law (IC 32-25-1-1 and 32-25-2-7). Each owner then holds fee simple title to their unit, with exclusive ownership and possession of it, plus an <strong>undivided interest in the common areas and facilities</strong> (IC 32-25-4-1), in a percentage set by the declaration (IC 32-25-7-1). The unit itself is the enclosed space inside the building, what people often call the airspace inside your walls (IC 32-25-2-9). Unless the declaration says otherwise, the common areas include the land, foundations, roofs, hallways, yards, parking and recreational facilities (IC 32-25-2-4).</p>
 <p>In plain English: you own the space inside your unit, and you share ownership of the building, land and amenities with every other owner. More in our <a href="/glossary/condominium/">condominium</a> glossary entry.</p>
 <table class="data-table">
 <thead><tr><th></th><th>Townhouse (fee simple)</th><th>Condo</th></tr></thead>
 <tbody>
 <tr><td>What the word describes</td><td>A building style</td><td>A form of legal ownership</td></tr>
 <tr><td>What you own</td><td>The home and the lot under it</td><td>Your unit plus an undivided share of the common areas</td></tr>
 <tr><td>Roof and exterior</td><td>Usually the owner, unless the covenants say otherwise</td><td>Usually the association, as common areas</td></tr>
 <tr><td>Association</td><td>Common, mainly for shared areas</td><td>Always; bylaws are recorded with the declaration</td></tr>
 <tr><td>Typical insurance</td><td>HO-3 homeowners policy</td><td>HO-6 unit-owner policy plus the master policy</td></tr>
 <tr><td>Loan project approval</td><td>Usually not needed</td><td>Often required</td></tr>
 </tbody>
 </table>

 <h2 id="legally-a-condo">When a Townhome Is Legally a Condo</h2>
 <p>Here&rsquo;s the twist: because &ldquo;condo&rdquo; is about ownership, a building can look exactly like a row of townhouses and still be a condominium. Indiana&rsquo;s definition of a condo unit covers an enclosed space in a building of one or more stories, as long as it has an exit to a street or to a common area that leads to one (IC 32-25-2-9), so a two-story attached home with its own front door can qualify. Fannie Mae&rsquo;s lending guidelines even have a category for <em>detached</em> condo units. The label in the listing isn&rsquo;t the legal answer, so check the documents:</p>
 <ul>
 <li><strong>The legal description.</strong> On the deed and the <a href="/glossary/title-commitment/">title commitment</a>, a fee-simple townhome is typically described as a numbered lot on a recorded subdivision plat. A condo is typically described as a unit in a named condominium, referencing the recorded declaration and floor plans, with a percentage interest in the common areas.</li>
 <li><strong>The declaration.</strong> An Indiana condo declaration is recorded with the county recorder. It has to describe the land, the buildings and units, the common and limited common areas, each unit&rsquo;s percentage interest and the use restrictions, with the bylaws attached and the recorded floor plans referenced (IC 32-25-7-1). A fee-simple townhome community has recorded covenants for its HOA instead.</li>
 <li><strong>The plat or floor plans.</strong> A subdivision plat with a lot drawn around each home points to fee-simple ownership; recorded condominium floor plans point to a condo.</li>
 <li><strong>Ask the title company.</strong> Your <a href="/glossary/title-company/">title company</a> reviews the recorded documents early and can tell you which one you&rsquo;re buying. Tell your lender too; it changes how the loan is approved.</li>
 </ul>

 <h2 id="hoa-dues">HOA Dues: What Each Usually Covers</h2>
 <p>Both kinds of homes usually come with an <a href="/glossary/hoa/">HOA</a>, but the dues pay for different things, which is why comparing two monthly numbers side by side can mislead you.</p>
 <ul>
 <li><strong>Townhome HOAs</strong> typically maintain the <a href="/glossary/common-area/">common areas</a>: entrances, landscaping, ponds, private streets and any pool. Many include lawn care and snow removal. Whether the association also handles roofs, siding or exterior painting depends entirely on the covenants; in many fee-simple communities, the roof over your townhome is yours to replace.</li>
 <li><strong>Condo associations</strong> maintain the building itself, because the roof, foundation, exterior walls and grounds are common areas owned by everyone. Dues usually fund the association&rsquo;s master insurance policy too, along with savings for big projects like a new roof or parking lot.</li>
 </ul>
 <p>Condo dues usually cover more, so they&rsquo;re often higher. Either way, ask for the budget, the <a href="/glossary/reserve-fund/">reserve fund</a> balance and recent meeting minutes; a thin reserve can mean a <a href="/glossary/special-assessment/">special assessment</a> down the road. Our guide to <a href="/blog/buying-a-home-with-an-hoa-central-indiana/">buying a home with an HOA in Central Indiana</a> walks through the documents to read. Indiana also requires the seller to give you the HOA&rsquo;s governing documents and assessment information at least 10 days before closing; our <a href="/blog/indiana-seller-disclosure-form/">Indiana seller&rsquo;s disclosure guide</a> covers that rule.</p>

 <h2 id="insurance">Insurance: HO-3, HO-6 and the Master Policy</h2>
 <p>Insurance follows ownership. A fee-simple townhome is usually insured like a house, with a standard homeowners policy (most often the HO-3 form) covering the whole structure, inside and out, along with your belongings and liability. A condo usually has two policies working together: the association&rsquo;s <strong>master policy</strong>, paid for out of dues, which covers the structure, exterior and common areas, and your own <strong>HO-6</strong> unit-owner policy, which covers your belongings, your liability and the parts of the unit you&rsquo;re responsible for.</p>
 <p>Where one policy stops and the other starts depends on the association&rsquo;s documents. Some master policies cover the unit&rsquo;s interior finishes; &ldquo;bare walls&rdquo; policies leave the drywall, flooring, cabinets and fixtures to you. Ask for the association&rsquo;s certificate of insurance and the insurance section of the declaration or bylaws, and ask your insurance agent about <strong>loss assessment</strong> coverage, which can help pay your share of a special assessment or the master policy&rsquo;s deductible after a covered loss. And some townhome associations insure exteriors under a master policy too, so read the covenants before assuming an HO-3 fits.</p>

 <h2 id="financing">Financing: Why Condos Need Project Approval</h2>
 <p>A fee-simple townhome generally finances like a single-family home: the lender looks at you and at the property. A condo adds a third check, <strong>the condo project itself</strong>, because the association&rsquo;s finances, insurance and rules affect the value of every unit.</p>
 <ul>
 <li><strong>FHA loans.</strong> The unit generally has to be in an FHA-approved condo project, and HUD keeps a public, searchable list of them. Under HUD&rsquo;s 2019 condo rule, a unit in a project that isn&rsquo;t FHA-approved may still qualify through <strong>Single-Unit Approval</strong> if the project is complete, has at least five units and meets HUD&rsquo;s other requirements. Our guide to <a href="/blog/fha-loans-in-indiana-requirements-and-benefits/">FHA loans in Indiana</a> covers the rest.</li>
 <li><strong>VA loans.</strong> The VA lists buying &ldquo;a condo in a VA-approved project&rdquo; as a use of its purchase loan, so the project needs to be on the VA&rsquo;s approved list, or get added, before your loan can close. See our <a href="/blog/va-loans-in-indiana-a-complete-guide-for-veterans/">VA loan guide</a>.</li>
 <li><strong>Conventional loans.</strong> For a loan sold to Fannie Mae, an attached unit in a condo project generally needs a project review: the lender&rsquo;s own review through Fannie&rsquo;s Condo Project Manager, a review by Fannie Mae, or, for an established project, an existing FHA approval. Fannie waives project review for detached condo units, projects of two to ten units that aren&rsquo;t part of a larger development, and units in planned unit developments (Fannie Mae Selling Guide, August 2026). Freddie Mac has its own condo project requirements and a Condo Project Advisor tool.</li>
 </ul>
 <p>What that means for you: ask about the project&rsquo;s approval status before you write an offer, not after. A project that can&rsquo;t pass review can rule out some loan programs. It matters at resale too: a condo without FHA or VA approval may draw fewer buyers. A townhome you own fee simple, including one in a <a href="/glossary/planned-unit-development/">planned unit development</a> with an HOA, usually skips this step entirely.</p>

 <h2 id="pros-cons">Pros and Cons for Buyers</h2>
 <table class="data-table">
 <thead><tr><th></th><th>Townhouse (fee simple)</th><th>Condo</th></tr></thead>
 <tbody>
 <tr><td>Maintenance</td><td>Less yard than a house, but you may still own the roof and exterior</td><td>The least hands-on; the association handles the building and grounds</td></tr>
 <tr><td>Privacy</td><td>Shared side walls, no one above or below, often a private patio</td><td>Neighbors may share walls, floors and ceilings; outdoor space is often a limited common area like a balcony</td></tr>
 <tr><td>Cost</td><td>Usually lower dues; you budget for your own exterior repairs</td><td>Higher dues that cover big building costs</td></tr>
 <tr><td>Resale</td><td>Finances like a house for most loan types</td><td>Project approval status can limit which buyers can finance</td></tr>
 </tbody>
 </table>
 <p>Both are popular with <a href="/services/first-time-home-buyers/">first-time buyers</a> and <a href="/services/downsizing/">downsizers</a>. If you&rsquo;re downsizing, note that most townhomes have stairs, while many condos offer one-level living.</p>

 <h2 id="where">Where to Find Townhomes and Condos Around Indianapolis</h2>
 <p>Townhomes and condos are spread across Central Indiana. These neighborhoods in our <a href="/communities/">communities directory</a> include them; as always, confirm the ownership type of the specific home you&rsquo;re considering.</p>
 <h3>Townhome communities</h3>
 <ul>
 <li><a href="/communities/ellis-acres-whitestown/">Ellis Acres</a> and <a href="/communities/townhomes-at-anson-whitestown/">Townhomes at Anson</a> in Whitestown: two- and three-story townhomes near the Zionsville border, and townhomes within the Anson development</li>
 <li><a href="/communities/towns-at-pennsy-cumberland/">Towns at Pennsy</a> in Cumberland: three-bedroom Lennar townhomes backing up to the Pennsy Trail</li>
 <li><a href="/communities/carrington-woods-beech-grove/">Carrington Woods</a> in Beech Grove: low-maintenance townhomes near I-465 and Emerson Avenue</li>
 <li><a href="/communities/central-state-indianapolis/">Central State</a> in Indianapolis: homes and townhomes built since 2017 on the former Central State Hospital campus</li>
 <li>Neighborhoods mixing single-family homes and townhomes: <a href="/communities/centennial-westfield/">Centennial</a> and <a href="/communities/lancaster-westfield/">Lancaster</a> in Westfield, <a href="/communities/hampton-walk-mccordsville/">Hampton Walk</a> in McCordsville, <a href="/communities/saratoga-plainfield/">Saratoga</a> in Plainfield, <a href="/communities/parkrose-greenfield/">Parkrose</a> in Greenfield and <a href="/communities/tracy-commons-new-whiteland/">Tracy Commons</a> in New Whiteland</li>
 </ul>
 <h3>Condo communities</h3>
 <ul>
 <li><a href="/communities/castleton-farms-indianapolis/">Castleton Farms</a> in Indianapolis: mostly two-bedroom condos from the early 1980s, near Castleton shopping</li>
 <li><a href="/communities/newport-bay-indianapolis/">Newport Bay</a> in Indianapolis: a gated condo community on Lake Clearwater with secure garage parking</li>
 <li><a href="/communities/villas-at-quail-run-indianapolis/">The Villas at Quail Run</a> in Indianapolis: mid-1990s brick condos where the HOA covers lawn care and snow removal</li>
 <li><a href="/communities/waterfront-condominiums-at-morse-lake-cicero/">Waterfront Condominiums at Morse Lake</a> in Cicero: one-level flats in a lakefront building with an elevator and boat slips</li>
 <li><a href="/communities/bridgemor-village-mooresville/">Bridgemor Village</a> in Mooresville: maintenance-free condos in a 55+ active-adult community</li>
 <li>Neighborhoods with both: <a href="/communities/fort-harrison-lawrence/">Fort Ben</a> in Lawrence (condos in the historic officers&rsquo; quarters, plus newer townhomes), <a href="/communities/villages-of-oak-manor-westfield/">Villages of Oak Manor</a> in Westfield, <a href="/communities/southern-dunes-southport/">Southern Dunes</a> in Southport and <a href="/communities/broad-ripple-village-broad-ripple/">Broad Ripple Village</a></li>
 </ul>
 <p><strong>Search tip:</strong> our <a href="/search/">home search</a> takes a town name, ZIP code, street address or MLS number, so start with the town you like and narrow down from there. Because a listing&rsquo;s &ldquo;townhome&rdquo; label doesn&rsquo;t tell you the legal ownership, check the HOA details in each listing and have your agent confirm the ownership type before you write an offer.</p>

 <h2 id="our-take">Our Take</h2>
 <p>If you want the least upkeep and don&rsquo;t mind higher dues and a few more rules, a condo can be a great fit, especially a one-level unit. If you&rsquo;d rather own your land, finance like a house and keep more control, a fee-simple townhome usually makes more sense. Either way, the recorded documents, the HOA&rsquo;s finances and your loan approval matter more than the listing&rsquo;s label. Before you start touring, your agent will walk you through a <a href="/services/buyer-representation/">buyer representation agreement</a>, which Indiana buyers sign with the agent who represents them, and our <a href="/services/home-buying-process/">home buying process guide</a> lays out every step from pre-approval to closing. Ready to look? <a href="/search/">Search homes for sale</a> or <a href="/schedule/">book a call with our team</a>.</p>
"""

FL = "https://codes.findlaw.com/in/title-32-property/in-code-sect-"

POST = dict(
 slug="townhouse-vs-condo-indianapolis",
 title="What Is a Townhouse? Townhouse vs. Condo in Indianapolis",
 headline="Townhouse vs. Condo: What's the Difference, and Where to Find Townhomes Around Indianapolis",
 crumb="Townhouse vs. Condo",
 h1_html="Townhouse vs. Condo: <em>What&rsquo;s the Difference?</em>",
 desc=("What is a townhouse, and how is it different from a condo? Ownership, HOA dues, insurance and "
       "loan approval, plus where to find townhomes around Indianapolis."),
 date="2026-11-19", month="November 2026",
 category="Buying a Home", eyebrow="BUYING A HOME",
 focus="townhouse vs condo",
 hero_sub=("A townhouse is a building style; a condo is a form of ownership. Here&rsquo;s what that means for your HOA dues, "
           "insurance and loan, and where to find townhomes and condos around Indianapolis."),
 badges=["Buying a Home", "Indiana Law", "Central Indiana"],
 read_min=9,
 card_title="Townhouse vs. Condo: What's the Difference?",
 card_sub="Ownership, HOA dues, insurance and financing, plus where to find townhomes.",
 qa_heading="Townhouse vs. Condo at a Glance",
 qa_lead=("<strong>What is a townhouse, and how is it different from a condo?</strong> A townhouse is a building style: an attached, "
          "usually multi-level home that shares walls with its neighbors, typically owned fee simple with the lot under it and an HOA "
          "for the common areas. A condo is a form of ownership: under Indiana&rsquo;s condominium law (IC 32-25), you own your unit "
          "plus an undivided share of the building, land and amenities with the other owners. That&rsquo;s why some homes that look "
          "like townhouses are legally condos."),
 qa_facts=[
  ("Townhouse", "A building style: attached, multi-level, shared walls"),
  ("Condo", "A form of ownership under Indiana&rsquo;s IC 32-25"),
  ("Condo owner holds", "The unit plus an undivided share of the common areas (IC 32-25-4-1)"),
  ("Typical insurance", "HO-3 for a fee-simple townhome &middot; HO-6 plus the master policy for a condo"),
  ("Loan approval", "FHA, VA and conventional loans often require condo project approval or review"),
  ("How to tell", "The recorded declaration, plat and title commitment"),
 ],
 toc=[("difference", "Building Style vs. Form of Ownership"), ("legally-a-condo", "When a Townhome Is Legally a Condo"),
      ("hoa-dues", "HOA Dues: What Each Covers"), ("insurance", "Insurance: HO-3, HO-6 and the Master Policy"),
      ("financing", "Financing and Condo Project Approval"), ("pros-cons", "Pros and Cons for Buyers"),
      ("where", "Where to Find Townhomes and Condos"), ("our-take", "Our Take"), ("faq", "FAQ")],
 body=BODY,
 faqs=[
  ("What is a townhouse?",
   "A townhouse, or townhome, is an attached home, usually two or three stories, that shares one or more side walls with neighboring homes and has its own entrance, with no one living above or below. In most Central Indiana townhome communities, owners hold the home and the small lot under it fee simple, and an HOA maintains the common areas."),
  ("What is the difference between a townhouse and a condo?",
   "A townhouse is an architectural style, while a condo is a form of legal ownership. A fee-simple townhome owner typically owns the structure and the land under it. A condo owner in Indiana owns their unit plus an undivided percentage of the common areas, which include the land, roof, exterior and amenities unless the declaration says otherwise (IC 32-25-2-4 and IC 32-25-4-1)."),
  ("Can a townhouse be a condo?",
   "Yes. Because condo describes ownership, an attached townhouse-style building can be legally set up as a condominium by recording a declaration under IC 32-25. Check the legal description on the deed and title commitment, the recorded declaration and the plat or floor plans, and ask your title company which type you are buying."),
  ("Do I need HO-3 or HO-6 insurance for a townhouse?",
   "A fee-simple townhome is usually insured with a standard homeowners policy, most often the HO-3 form, that covers the whole structure. A condo owner usually needs an HO-6 unit-owner policy alongside the association's master policy. Some townhome associations insure exteriors under a master policy, so read the covenants and talk to your insurance agent before you choose."),
  ("Can I use an FHA or VA loan to buy a condo?",
   "Often, yes, but the project matters. FHA generally requires the condo project to be FHA-approved, though a unit in an unapproved project may qualify through Single-Unit Approval if the project meets HUD's requirements. The VA allows purchase loans for condos in VA-approved projects. Ask your lender to check the project's status before you make an offer."),
  ("Are condo HOA fees higher than townhome HOA fees?",
   "Often, because condo dues usually cover the building itself, including the roof, exterior, grounds and the association's master insurance policy. Townhome dues typically cover common areas and sometimes lawn care and snow removal, while the owner handles their own roof and exterior. Compare what the dues include, not just the monthly amount."),
 ],
 sources=[
  ("Indiana General Assembly, Indiana Code (official)", "https://iga.in.gov/"),
  ("IC 32-25-1-1, submitting property to the condominium law", FL + "32-25-1-1.html"),
  ("IC 32-25-2-4, common areas and facilities", FL + "32-25-2-4.html"),
  ("IC 32-25-2-7, definition of condominium", FL + "32-25-2-7.html"),
  ("IC 32-25-2-9, definition of condominium unit", FL + "32-25-2-9.html"),
  ("IC 32-25-4-1, unit ownership", FL + "32-25-4-1.html"),
  ("IC 32-25-7-1, the condominium declaration", FL + "32-25-7-1.html"),
  ("Indiana Law Journal, The Horizontal Property Act of 1963 (40 Ind. L.J. 57)", "https://www.repository.law.indiana.edu/ilj/vol40/iss1/4"),
  ("Maryland Insurance Administration, condominium insurance FAQ", "https://insurance.maryland.gov/Consumer/Pages/condo/faqs.aspx"),
  ("Washington Office of the Insurance Commissioner, how condo insurance works", "https://www.insurance.wa.gov/insurance-resources/condo-insurance/learn-how-condo-insurance-works"),
  ("HUD, FHA condominiums and Single-Unit Approval", "https://www.hud.gov/hud-partners/single-family-ins-condominiums"),
  ("HUD, search FHA-approved condominiums", "https://entp.hud.gov/idapp/html/condlook.cfm"),
  ("HUD final rule, Project Approval for Single-Family Condominiums (2019)", "https://www.govinfo.gov/content/pkg/FR-2019-08-15/html/2019-17213.htm"),
  ("VA, purchase loans", "https://www.va.gov/housing-assistance/home-loans/loan-types/purchase-loan/"),
  ("Fannie Mae Selling Guide B4-2.1-01, project standards", "https://selling-guide.fanniemae.com/sel/b4-2.1-01/general-information-project-standards"),
  ("Fannie Mae Selling Guide B4-2.1-02, waiver of project review", "https://selling-guide.fanniemae.com/sel/b4-2.1-02/waiver-project-review"),
  ("Freddie Mac, condominium unit mortgages", "https://sf.freddiemac.com/working-with-us/origination-underwriting/mortgage-products/condominium-unit-mortgages"),
  ("Your Realty Link communities directory", "/communities/"),
 ],
 related=[("/blog/buying-a-home-with-an-hoa-central-indiana/", "Buying a Home With an HOA in Central Indiana"),
          ("/blog/fha-loans-in-indiana-requirements-and-benefits/", "FHA Loans in Indiana"),
          ("/blog/first-time-home-buyer-guide-indianapolis-2026/", "First-Time Home Buyer Guide: Indianapolis")],
 cta=("Shopping for a Townhome or Condo?",
      "Tell us where you want to live and what you want to spend. Our team will find townhomes and condos that fit, dig into the HOA and the ownership type, and flag condo approval questions for your lender early.",
      [("/search/", "Search Homes for Sale &rarr;", "btn-white"), ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[("/services/home-buying-process/", "The Home Buying Process"),
            ("/communities/", "Communities &amp; Subdivisions"),
            ("/services/first-time-home-buyers/", "First-Time Home Buyers"),
            ("/services/downsizing/", "Downsizing")],
 link_from=[
  ("glossary/townhouse/index.html",
   'Comparing your options? Our guide to <a href="/blog/townhouse-vs-condo-indianapolis/">townhouse vs. condo</a> explains when a townhome is legally a condo, how insurance and loan approval differ, and where to find townhomes around Indianapolis.'),
  ("glossary/condominium/index.html",
   'Is that townhome actually a condo? Our <a href="/blog/townhouse-vs-condo-indianapolis/">townhouse vs. condo guide</a> covers Indiana&rsquo;s condominium law, HO-6 insurance, FHA and VA condo approval, and condo communities around Indianapolis.'),
  ("blog/buying-a-home-with-an-hoa-central-indiana/index.html",
   '<strong>Deciding between a townhome and a condo?</strong> Our guide to <a href="/blog/townhouse-vs-condo-indianapolis/">townhouse vs. condo</a> explains what each kind of HOA usually covers and how insurance and financing differ.'),
 ],
 about={"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
