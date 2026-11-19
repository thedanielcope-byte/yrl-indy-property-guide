# Selling a house when moving out of state from Indianapolis (Nov 2026).
# Why: GSC Nov 2026, "moving out of state" style queries = 516 impressions at position 31,
# landing on buyer-relocation pages (wrong intent). This is the seller-side answer.
# Sources and verification notes (all checked Nov 19 2026):
# - Home sale exclusion: IRS Pub 523 ("For use in preparing 2025 Returns"): $250,000 / $500,000 MFJ,
#   24 months of ownership and 24 months of use in the 5 years before the sale, once per 2 years,
#   partial exclusion for a work-related move (new job at least 50 miles farther than the old work
#   location), health and unforeseeable events; gain equal to depreciation allowed/allowable after
#   May 6, 1997 can't be excluded; the period after you last lived there (within the 5 years) is
#   not "nonqualified use". "About three years to sell after moving out" is arithmetic from the
#   2-of-5 use test, stated as "generally". IRS Tax Topic 701 for the reporting line.
# - Moving expenses: IRS Notice 2026-10 (sec. 70113(a) of the OBBBA made the moving expense
#   disallowance permanent except where sec. 217(g) applies; 70113(b) adds certain intelligence
#   community members who move after Dec 31, 2025). IRS Topic 455 (updated Oct 16 2026).
#   IRS Pub 15-B (2026): OBBBA permanently eliminates the exclusion for qualified moving expense
#   reimbursements, so they're generally taxable wages (Armed Forces / intel community excepted).
# - Remote notarization: IC 33-42-17-2 (register with the Secretary of State as a remote notary;
#   must be physically present in Indiana) and IC 33-42-17-3 (SOS-approved audiovisual technology,
#   act is recorded; principal may be outside Indiana within the U.S., or outside the U.S. in
#   limited cases such as property located in the U.S.), FindLaw "current as of January 1, 2026".
#   Out-of-state notarizations: IC 33-42-9-8 (presumed valid, same effect as an Indiana notarial
#   act). Power of attorney: IC 30-5-3-3(b) (record the POA before presenting a document signed
#   under it for recording). Whether a closing can be done remotely depends on the title company,
#   underwriter and any buyer's lender, so the post says "ask your title company".
# - Homestead: IC 6-1.1-12-37(g), 60 days to notify the county auditor after a change in use;
#   HEA 1210 (2026) makes non-filers liable ("shall") for the additional taxes plus a 10% civil
#   penalty (DLGF memo, May 27 2026, Section I.C).
# - Vacant home: Indiana OUCC frozen-pipe page ("do not set it lower than 55 degrees" when traveling;
#   know the master shut-off valve; have a neighbor check). Insurance: IRMI commentary on vacant
#   homes (homeowners policy cuts back coverage after a period of vacancy; vandalism and glass
#   breakage). No specific number of days stated in the post (policies vary).
# - Employer programs: North American Van Lines home sale program guide (industry source):
#   guaranteed buyout at appraised value after a marketing period, BVO, direct reimbursement
#   (taxable; often grossed up). Described in general terms only.
# - Seller's disclosure due before an offer is accepted: IC 32-21-5-10 (see the disclosure post).
# Left out (not verified): specific vacancy-clause day counts, Indiana income tax treatment of a
# nonresident's gain on an Indiana home, how many appraisals a buyout uses.
# General information, not legal, tax or lending advice.
FL = "https://codes.findlaw.com/in/"

POST = dict(
 slug="selling-a-house-when-moving-out-of-state-indianapolis",
 title="Selling a House When Moving Out of State From Indianapolis",
 headline="Selling a House When Moving Out of State From Indianapolis",
 crumb="Selling When Moving Out of State",
 h1_html="Moving Out of State? <em>How to Sell Your Indianapolis House</em>",
 desc=("Moving out of state from Indianapolis? How to time the sale, close remotely, protect a vacant "
       "house, and what the IRS and Indiana rules mean for sellers."),
 date="2026-11-19", month="November 2026",
 category="Selling a Home", eyebrow="SELLING A HOME",
 focus="selling a house when moving out of state",
 hero_sub="How to time the sale, sign and close from another state, keep an empty house safe and insured, and what the IRS and Indiana rules mean for sellers who are leaving town.",
 badges=["Selling a Home", "Relocation", "Updated 2026"],
 read_min=9,
 card_title="Selling a House When Moving Out of State",
 card_sub="Timing, remote closings, vacant homes and taxes.",
 qa_heading="Selling When You&rsquo;re Moving Out of State",
 qa_lead=("<strong>Can you sell your Indianapolis house after you move out of state?</strong> Yes. With a listing agent "
          "handling showings on the ground and a title company that can arrange a mail-away or remote closing, many sellers "
          "never have to come back. The bigger decisions are timing (sell first, move first, or rent it out), protecting the "
          "house if it sits empty, and taxes: owners who lived in the home 2 of the last 5 years can generally exclude up to "
          "$250,000 of gain ($500,000 married filing jointly), while moving costs are no longer deductible for most people."),
 qa_facts=[
  ("Home sale exclusion", "Up to $250,000 ($500,000 married filing jointly), IRS Pub. 523"),
  ("Ownership &amp; use test", "2 of the 5 years before the sale; partial exclusion possible for a job move"),
  ("Moving expenses", "Not deductible for most people; made permanent in 2025, with a military exception"),
  ("Remote notarization", "Allowed by an Indiana-registered remote notary (IC 33-42-17, 2026 Code)"),
  ("Renting it out?", "Tell the county auditor within 60 days (IC 6-1.1-12-37)"),
  ("Seller&rsquo;s disclosure", "Due before you accept an offer (IC 32-21-5-10)"),
 ],
 toc=[("timing", "Sell Before You Move, After, or Rent It Out"), ("remote-closing", "Selling and Closing From Out of State"),
      ("vacant", "If the House Will Sit Empty"), ("showings", "Showings, Lockboxes and Virtual Tours"),
      ("employer", "Employer Relocation Packages"), ("taxes", "Taxes: The Home Sale Exclusion and Moving Costs"),
      ("indiana-paperwork", "Indiana Paperwork You&rsquo;ll Still Need"), ("our-take", "Our Take")],
 body=f"""
 <p>Moving out of state from Indianapolis means juggling two big projects at once: starting over somewhere new and selling the house you&rsquo;re leaving behind. The good news is that it&rsquo;s practical to sell an Indiana home from a distance. Here&rsquo;s how to decide on timing, close without flying back, keep an empty house safe, and understand the tax rules before you go.</p>
 <p><em>This is general information, not legal, tax or lending advice. Talk to a tax professional, real estate attorney or lender about your own situation.</em> Statute references are to the 2026 Indiana Code; federal tax references are to IRS Publication 523 (for 2025 returns).</p>

 <h2 id="timing">Sell Before You Move, After You Move, or Rent It Out</h2>
 <p>It comes down to your moving date, your equity, and whether you can carry two housing payments for a while.</p>
 <h3>Sell before you move</h3>
 <p>Listing while you still live in the house usually makes the sale simplest. It&rsquo;s furnished, heated and looked after, you can handle small repairs yourself, and you know what you&rsquo;ll walk away with before you commit to your next home. The trade-offs are showings while you&rsquo;re packing, and timing: if closing comes before your start date, you may need short-term housing or a later <a href="/glossary/possession-date/">possession date</a> that the buyer agrees to.</p>
 <h3>Move first, sell after</h3>
 <p>Moving first means no showings while you pack. But you&rsquo;ll keep paying the mortgage, taxes, insurance, utilities and upkeep until closing, and an empty house brings its own challenges (more below). Our <a href="/services/job-relocation-sale/">job relocation sale</a> service is built for this situation: our team handles prep, showings and paperwork on the ground while you settle in.</p>
 <h3>Rent it out instead</h3>
 <p>Some owners keep the house as a rental, especially if they might move back or would rather not sell yet. Go in with eyes open: you become a long-distance landlord (or pay a property manager), and the tax picture changes. The home sale exclusion requires that you lived in the home for 2 of the 5 years before the sale, so if you lived there at least two years before moving out, you generally have up to about three years to sell and still qualify. Gain equal to any depreciation you were allowed while it was a rental can&rsquo;t be excluded (IRS Pub. 523). And in Indiana, once the home is no longer your principal residence, you have to notify the county auditor within 60 days so the homestead deduction comes off. A 2026 law change makes owners who don&rsquo;t notify liable for the additional taxes plus a 10% penalty (IC 6-1.1-12-37(g)). If you sell later with a tenant in place, see <a href="/blog/how-to-sell-a-home-with-tenants-in-indianapolis/">how to sell a home with tenants</a> and our <a href="/services/sell-rental-property/">rental property sale</a> page.</p>
 <h3>Buying in your new state before this one sells</h3>
 <p>If you need to buy before your Indianapolis house sells, there are a few common tools. A <a href="/glossary/home-sale-contingency/">home sale contingency</a> makes your offer depend on selling your current home; it protects you, but sellers in competitive markets often see it as a weaker offer. A bridge loan or a <a href="/glossary/home-equity-line-of-credit/">home equity line of credit</a> can let you tap your equity here for the next down payment, at the cost of interest, fees and, for a while, two payments. Talk to a lender in your new state early about how your current mortgage affects what you can borrow.</p>
 <p>Whatever you choose, pricing matters even more when you&rsquo;re carrying a house from another state, because every extra month on the market is another month of payments. Start from a <a href="/glossary/comparative-market-analysis/">comparative market analysis</a> rather than an online estimate; our <a href="/services/pricing-your-home/">pricing your home</a> page explains how we set a list price.</p>

 <h2 id="remote-closing">Selling and Closing From Out of State</h2>
 <p>You don&rsquo;t have to be in Indiana to sign. Listing agreements, the disclosure form, offers and counteroffers are routinely signed electronically. Closing is where a notary comes in, because the deed and some other seller documents have to be notarized. Most Central Indiana closings run through a <a href="/glossary/title-company/">title company</a>, and depending on the company and the deal, you may have these options:</p>
 <ul>
 <li><strong>Mail-away closing.</strong> The title company sends your seller documents ahead of closing, you sign them in front of a notary where you live, and you ship the originals back. Indiana presumes a notarization done in another state by a notary or other authorized official is valid, with the same effect as one done here (IC 33-42-9-8).</li>
 <li><strong>Remote online notarization.</strong> Indiana allows remote notarial acts by an Indiana notary who has registered with the Secretary of State as a remote notary, is physically in Indiana, and uses approved audio-video technology; the session is recorded. The signer can be anywhere in the United States, and outside the country in limited cases, such as a matter involving property in the U.S. (IC 33-42-17-2 and -3). Whether your closing can be done this way depends on the title company, its underwriter and, if the buyer is financing, the buyer&rsquo;s lender, so ask your title company early.</li>
 <li><strong>Power of attorney.</strong> Some sellers sign a power of attorney so a trusted person can sign for them. In Indiana, a power of attorney has to be recorded before a deed signed under it is presented for recording (IC 30-5-3-3), and title companies usually want to review and approve it well before closing. Have an attorney prepare it.</li>
 </ul>
 <p>Two practical tips. First, give your agent and the title company your new mailing address and best phone number early, and build shipping time into the schedule. Second, watch for wire fraud. If your proceeds are wired, you&rsquo;re exactly the kind of seller scammers target: never act on emailed changes to wire or payment instructions, and confirm by calling the title company at a number you already know. Our <a href="/glossary/closing-wire-fraud/">closing wire fraud</a> explainer has more, and <a href="/blog/how-long-does-it-take-to-close-on-a-house-in-indiana/">how long it takes to close in Indiana</a> walks through the timeline.</p>

 <h2 id="vacant">If the House Will Sit Empty</h2>
 <p>A vacant house can sell well, but it needs a plan before you hand over the keys to the movers:</p>
 <ul>
 <li><strong>Keep the utilities on.</strong> Buyers, inspectors and appraisers need power, water and heat, and so does the house. Indiana&rsquo;s Office of Utility Consumer Counselor advises not setting the thermostat below 55 degrees when you&rsquo;re away in cold weather. Keep the accounts in your name until closing; our <a href="/utilities/">utilities guide</a> lists providers by city.</li>
 <li><strong>Call your insurance agent before you move out.</strong> Many homeowners policies limit coverage once a home has been vacant for a set period, and vandalism and glass breakage are common exclusions. Check your policy&rsquo;s vacancy terms, tell your agent the house will be empty, and ask whether you need a vacancy endorsement or a separate vacant-home policy.</li>
 <li><strong>Winterize if it&rsquo;ll be empty in cold weather.</strong> Know where the main water shut-off is, have someone check the house regularly (especially during cold snaps), and consider a freeze alarm or a smart thermostat that alerts your phone. Ask a plumber whether shutting off and draining the water makes sense for your house; if it&rsquo;s drained, it will need to be turned back on for the buyer&rsquo;s inspection.</li>
 <li><strong>Keep it looking cared for.</strong> Arrange lawn care or snow removal, forward your mail, and put a few lamps on timers. A house that looks lived-in is a smaller target.</li>
 <li><strong>Think about staging.</strong> Empty rooms often look smaller in photos and in person. A few pieces in the main living areas help, and clearly labeled virtual staging can help the online photos. Our <a href="/services/vacant-home-sale/">vacant home sale</a> page covers how we handle empty listings.</li>
 </ul>

 <h2 id="showings">Showings, Lockboxes and Virtual Tours</h2>
 <p>Once you&rsquo;re gone, your listing agent becomes your eyes and ears. Here&rsquo;s how showings typically work when the seller is out of state:</p>
 <ul>
 <li><strong>Electronic lockbox.</strong> Buyers&rsquo; agents get in through an electronic lockbox that logs each entry, and showings are booked through a scheduling system, so you can see who&rsquo;s been in the house and when.</li>
 <li><strong>Feedback after showings.</strong> We follow up with buyers&rsquo; agents and pass along what we hear, so you can decide on price or prep changes with real information instead of guessing.</li>
 <li><strong>Virtual tours.</strong> Photos, a video walkthrough or a 3D tour help buyers decide whether to book a showing, and relocating buyers lean on them (our guide to <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">virtual home tours</a> explains how). They help you too: a live video walk-through with your agent can stand in for your own final look before listing.</li>
 </ul>

 <h2 id="employer">Employer Relocation Packages: Buyouts and Home Sale Help</h2>
 <p>If your employer is moving you, read the relocation policy before you list. Many programs have rules about which listing agreement you sign and who signs the purchase contract, and listing or accepting an offer on your own first can affect what&rsquo;s covered. Packages vary widely, but common home sale benefits include:</p>
 <ul>
 <li><strong>Closing cost or commission reimbursement</strong>, sometimes paid as a lump sum. For most employees, employer moving reimbursements now count as taxable wages (IRS Pub. 15-B), and some employers &ldquo;gross up&rdquo; the payment to help cover the tax.</li>
 <li><strong>Buyer value option (BVO).</strong> You market the home and find a buyer; the relocation company buys the home from you at that buyer&rsquo;s price and then completes the sale to the buyer.</li>
 <li><strong>Guaranteed buyout.</strong> If the home doesn&rsquo;t sell within the program&rsquo;s marketing period, the relocation company offers to buy it at a value based on independent appraisals. It buys certainty, though the appraised offer may not match what an open-market buyer would pay.</li>
 </ul>
 <p>Our team works directly with relocation companies on appraisals, buyout offers and paperwork. See our <a href="/services/job-relocation-sale/">job relocation sale</a> page for how that works.</p>

 <h2 id="taxes">Taxes: The Home Sale Exclusion and Moving Costs</h2>
 <p><em>General information, not tax advice. Talk to a CPA or tax professional before you sell.</em></p>
 <h3>The $250,000 / $500,000 exclusion</h3>
 <p>Under Section 121 of the tax code, you can exclude up to $250,000 of gain on the sale of your main home, or up to $500,000 if you&rsquo;re married filing jointly, when you meet both tests (IRS Pub. 523):</p>
 <ul>
 <li><strong>Ownership:</strong> you owned the home for at least 24 months of the 5 years before the sale.</li>
 <li><strong>Use:</strong> you lived in it as your main home for at least 24 months of those 5 years. The time doesn&rsquo;t have to be continuous.</li>
 </ul>
 <p>You generally can&rsquo;t use the exclusion if you already excluded gain on another home sale in the two years before this one. Your gain is the sale price minus selling costs and your adjusted basis, which includes what you paid plus the cost of improvements, so keep those receipts. See our <a href="/glossary/capital-gains-exclusion/">capital gains exclusion</a> glossary entry for more.</p>
 <h3>Moving before two years? A partial exclusion may apply</h3>
 <p>If a work-related move forces you to sell before you meet the two-year tests, you may qualify for a partial exclusion. Pub. 523 treats a move as work-related if, for example, your new job is at least 50 miles farther from the home than your old work location was. Health-related moves and certain unforeseeable events can also qualify. The partial amount is prorated based on how long you owned and lived in the home, so have your tax professional run the numbers.</p>
 <h3>Moving costs aren&rsquo;t deductible for most people</h3>
 <p>The 2017 tax law suspended the moving expense deduction for 2018 through 2025, and the One Big Beautiful Bill Act, signed in 2025, made that permanent. Active-duty military members moving under orders for a permanent change of station can still deduct qualifying moving costs, and so can certain members of the intelligence community who move after 2025 (IRS Notice 2026-10; IRS Topic 455). For everyone else, the cost of the moving truck and the trip isn&rsquo;t deductible. Selling costs on the house itself, like commissions and seller-paid closing costs, are a different matter: they reduce the gain on the sale (IRS Pub. 523).</p>

 <h2 id="indiana-paperwork">Indiana Paperwork You&rsquo;ll Still Need</h2>
 <ul>
 <li><strong>Seller&rsquo;s disclosure.</strong> Most sellers of homes with one to four units have to complete Indiana&rsquo;s Seller&rsquo;s Residential Real Estate Sales Disclosure and give it to the buyer before accepting an offer (IC 32-21-5-10). Fill it out before you leave, while the house and its repair history are in front of you. Our guide to the <a href="/blog/indiana-seller-disclosure-form/">Indiana seller&rsquo;s disclosure form</a> explains what it covers.</li>
 <li><strong>Closing costs and your net.</strong> Ask for a <a href="/services/seller-net-sheet/">seller net sheet</a> so you know roughly what you&rsquo;ll walk away with, and read <a href="/blog/closing-costs-in-indiana-what-sellers-need-to-know/">closing costs in Indiana for sellers</a> for how commissions, title fees and property tax prorations usually work.</li>
 <li><strong>Homestead deduction.</strong> If the house stops being your principal residence before it sells, for example because you rent it out, tell the county auditor within 60 days (IC 6-1.1-12-37(g)). Our <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead guide</a> explains the deduction.</li>
 </ul>

 <h2 id="our-take">Our Take</h2>
 <p>Selling a house from another state is very doable. The smoothest sales start with an early timing decision, a call to the insurance agent and title company before moving day, a disclosure filled out while the house is still in front of you, and a price set to sell rather than sit. If your employer is involved, read the relocation policy first, and run tax questions past a professional before you list. Ready to plan your move? <a href="/services/free-home-valuation/">Get a free home valuation</a> or <a href="/schedule/">book a call with our team</a>, and we&rsquo;ll handle the Indianapolis side while you focus on the new one.</p>
""",
 faqs=[
  ("Can I sell my house in Indiana after I've already moved out of state?",
   "Yes. Listing paperwork and offers are commonly signed electronically, your listing agent handles showings, and the title company can arrange a mail-away closing, where you sign with a notary where you live, or a remote online notarization if the title company and any buyer's lender accept it. Indiana presumes a notarization done in another state is valid (IC 33-42-9-8)."),
  ("Is it better to sell my house before or after I move out of state?",
   "Selling before you move usually makes the house easier to show and maintain, and you know what you'll net before you buy again. Moving first avoids showings while you pack, but you carry the mortgage, insurance, utilities and upkeep on an empty house until it closes. The right choice depends on your move date, your equity and your budget."),
  ("Do I pay capital gains tax if I sell my house and move out of state?",
   "Many sellers don't. If you owned the home and lived in it as your main home for at least 2 of the 5 years before the sale, you can generally exclude up to $250,000 of gain, or $500,000 if married filing jointly (IRS Publication 523). If a work-related move forces a sale sooner, a partial exclusion may apply. This is general information, not tax advice."),
  ("Are moving expenses tax deductible in 2026?",
   "Not for most people. The moving expense deduction was suspended for 2018 through 2025, and the One Big Beautiful Bill Act made that permanent. The exceptions are active-duty military members moving under orders for a permanent change of station and certain intelligence community members moving after 2025 (IRS Notice 2026-10)."),
  ("Does homeowners insurance cover a vacant house?",
   "It depends on the policy. Many homeowners policies limit coverage once a home has been vacant for a set period, and vandalism and glass breakage are common exclusions. Check your policy and talk to your insurance agent before you move out; you may need a vacancy endorsement or a separate vacant-home policy."),
  ("Can I rent out my Indianapolis house and sell it later?",
   "Yes, but plan for the tax effects. To keep the home sale exclusion you generally need to sell within about three years of moving out, gain equal to depreciation can't be excluded, and Indiana requires you to notify the county auditor within 60 days once the home is no longer your principal residence so the homestead deduction comes off (IC 6-1.1-12-37)."),
 ],
 sources=[
  ("IRS Publication 523, Selling Your Home (for 2025 returns)", "https://www.irs.gov/publications/p523"),
  ("IRS Tax Topic 701, Sale of your home", "https://www.irs.gov/taxtopics/tc701"),
  ("IRS Notice 2026-10 (moving expense disallowance made permanent)", "https://www.irs.gov/pub/irs-drop/n-26-10.pdf"),
  ("IRS Topic 455, Moving expenses for the Armed Forces and Intelligence Community", "https://www.irs.gov/taxtopics/tc455"),
  ("IRS Publication 15-B (2026), moving expense reimbursements", "https://www.irs.gov/publications/p15b"),
  ("IC 33-42-17-2, remote notary registration", FL + "title-33-courts-and-court-officers/in-code-sect-33-42-17-2/"),
  ("IC 33-42-17-3, remote notarial acts", FL + "title-33-courts-and-court-officers/in-code-sect-33-42-17-3/"),
  ("IC 33-42-9-8, notarial acts in another state", FL + "title-33-courts-and-court-officers/in-code-sect-33-42-9-8/"),
  ("IC 30-5-3-3, recording a power of attorney", FL + "title-30-trusts-and-fiduciaries/in-code-sect-30-5-3-3/"),
  ("IC 6-1.1-12-37, homestead deduction and change in use", FL + "title-6-taxation/in-code-sect-6-1-1-12-37.html"),
  ("Indiana DLGF memo on 2026 legislation (HEA 1210), May 27, 2026", "https://www.in.gov/dlgf/files/2026-memos/260527-Cockerill-Memo-Legislation-Affecting-Deductions-Credits-and-Exemptions.pdf"),
  ("IC 32-21-5-10, seller's disclosure before an offer is accepted", FL + "title-32-property/in-code-sect-32-21-5-10.html"),
  ("Indiana Office of Utility Consumer Counselor, preventing frozen pipes", "https://secure.in.gov/oucc/watersewer/tips-and-publications/preventing-frozen-pipes"),
  ("IRMI, Managing the Risks of a Vacant Home", "https://www.irmi.com/articles/expert-commentary/managing-the-risks-of-a-vacant-home"),
  ("North American Van Lines, guide to corporate home sale programs", "https://www.northamerican.com/corporate-relocation/resources/guides/ultimate-guide-to-home-sale-programs"),
 ],
 related=[
  ("/services/job-relocation-sale/", "Job Relocation Home Sales"),
  ("/services/vacant-home-sale/", "Selling a Vacant Home"),
  ("/blog/indiana-seller-disclosure-form/", "Indiana Seller's Disclosure Form"),
 ],
 cta=("Moving Out of State?",
      "Tell us your moving date and we&rsquo;ll build a plan around it: a realistic price, a prep list, and a team on the ground for showings and closing while you settle in somewhere new.",
      [("/services/free-home-valuation/", "Get a Free Home Valuation →", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[
  ("/services/pricing-your-home/", "Pricing Your Home"),
  ("/blog/closing-costs-in-indiana-what-sellers-need-to-know/", "Closing Costs in Indiana for Sellers"),
  ("/services/seller-net-sheet/", "Seller Net Sheet"),
  ("/glossary/capital-gains-exclusion/", "Capital Gains Exclusion (Glossary)"),
 ],
 link_from=[
  ("services/job-relocation-sale/index.html",
   'Moving out of state and weighing your options? Our guide to <a href="/blog/selling-a-house-when-moving-out-of-state-indianapolis/">selling a house when moving out of state</a> covers timing, remote closings, vacant-home insurance and the tax rules.'),
  ("services/vacant-home-sale/index.html",
   'Already moved away? Read <a href="/blog/selling-a-house-when-moving-out-of-state-indianapolis/">selling your Indianapolis house when moving out of state</a> for remote closing options, insurance and winterizing tips, and how showings work while you&rsquo;re gone.'),
 ],
 about={"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
