# House hacking in Indianapolis (Nov 2026). Researched Nov 19 2026; general information, not
# lending/legal/tax advice. Every lending/legal fact is from the agency's own document:
#  - FHA: HUD Handbook 4000.1, Update 18 (issued Aug 12 2026), read from the PDF:
#    MDCS >=580 = max financing, 500-579 = 90% LTV; purchase max LTV 96.5% (II.A.2); occupy within
#    60 days + intend 1 year (II.A.1.b.iii); FHA won't insure >1 principal residence per borrower;
#    3-4 unit self-sufficiency: PITI / (appraiser FMR of ALL units incl. borrower's, minus greater of
#    appraiser vacancy/maintenance or 25%) <= 100%; 3-4 unit reserves 3 months PITI; subject-property
#    rent with no history = 75% of lesser of appraiser FMR or lease, ADDED to income (can't reduce
#    the payment); boarder income needs 12-month history, max 30% of effective income;
#    Appendix 1.0: UFMIP 175 bps, annual MIP 55 bps for base loan <= $726,200 at LTV > 95%, mortgage term.
#  - 2026 limits: HUD FHA lookup (entp.hud.gov, CY2026, Marion County, MSA 26900 Indianapolis-Carmel-
#    Greenwood) = $541,287 / $693,050 / $837,700 / $1,041,125 (national floor; HUD No. 25-145, Dec 11
#    2025, ML 2025-23, case numbers on/after Jan 1 2026). Conforming: FHFA 2026 county file - every
#    Indiana county (incl. Marion, FIPS 18097) at baseline $832,750 / $1,066,250 / $1,288,800 /
#    $1,601,750 (FHFA release Nov 25 2025). No 2027 limits announced as of Nov 19 2026.
#  - Fannie Mae: white paper page (Oct 25 2023) confirms the Nov 18 2023 DU update raised max
#    LTV/CLTV/HCLTV for 2-4 unit principal residences. 95% figure: Eligibility Matrix (Dec 10 2025
#    version) "2-4 Units FRM/ARM: 95%" + Fannie product summary "2-4 unit DU Only: 95%" (seen via search
#    index; the matrix PDF itself returned 403 to direct fetch, so the post says DU-only and not
#    manual/high-balance and does not quote prior limits). Selling Guide (fetched): B2-1.1-01
#    (11/04/2026) occupy within 60 days + 1 year; B3-4.1-01 (08/07/2024) DU = 6 months reserves for
#    2-4 unit principal residence; B3-3.8-02 (09/02/2026) gross rent x .75, Form 1007/1025, <12 months
#    management experience = offset PITIA only; B3-4.3-06 (11/04/2026) 5% own funds when grants used
#    above 80% LTV on 2-4 units. LL-2026-09 (Nov 4 2026) changes the MANUAL matrix for loans sold on/
#    after Feb 22 2027 (not cited in the post; DU 95% unaffected).
#  - VA: VA.gov purchase loan page (updated Jan 7 2026): "single-family home, up to 4 units", must live
#    there, no down payment if price <= appraised value. 38 CFR 36.4340(f)(12)(i) (eCFR current to Nov 17
#    2026): multi-unit rent counted only with documented landlord likelihood of success + reserves to
#    carry the loan 6 months without the rent; based on 75% of rent.
#  - Rate: Freddie Mac PMMS 7.28% for Nov 19 2026 (prior week 7.11%; year ago 6.26%). Newer than the
#    7.24% (Oct 29) used in how-much-house-can-i-afford-indianapolis.py.
#  - Indianapolis: indy.gov landlord & STR registries page (Landlord Registry updated Nov 4 2026):
#    owners/landlords of residential rental units in the City must register; excluded cities exempt.
#    BNS fact sheet (PDF): began Jan 1 2015; Citizen Access portal; $5 fee covers all of one owner's
#    properties; Indiana-resident landlord/manager contact; units per parcel; annual renewal; excluded
#    cities = Beech Grove, Lawrence, Southport, Speedway. STR permit program effective Jan 1 2025, annual
#    permit per unit, one-time $150 initial fee (Ch. 852). Municode Ch. 851 blocked by Cloudflare.
#  - Indiana law (FindLaw, current as of Jan 1 2026): IC 32-31-3-12 (45 days after termination +
#    delivery of possession, itemized notice, tenant must give mailing address in writing, tenant
#    recovers deposit + attorney's fees if landlord fails); IC 32-31-8-5 (landlord duties).
#  - Taxes: DLGF circuit-breaker fact sheet (Nov 2025): 1% homestead / 2% residential, residential
#    includes "a building that includes two (2) or more dwelling units". IRS Pub 527 (2025 returns):
#    duplex example, split shared expenses, depreciate rental part.
#  - Insurance: Triple-I peer-to-peer rental page (regular rental of all/part of home = business use).
#  - Zoning/ADU: Indianapolis secondary-dwelling-unit rules conflicted across sources and Municode was
#    blocked, so no ADU/zoning specifics are stated. Duplex locations hedged "in our experience".
# Worked example math (scratchpad calc.py): $250,000 duplex, FHA 3.5% down $8,750, base $241,250,
# UFMIP $4,221.88 financed -> $245,471.88; 7.28%/30 yrs P&I $1,679.55; MIP $110.57; taxes 1.5%/yr
# $312.50 (blend of 1% + 2% caps; shown as $312); insurance $200; PITI $2,302.62; rent $1,250 -> net
# $1,052.62; +15% reserve $187.50 -> $1,240.12; yr-1 principal $2,362. Full rental: $2,500/mo,
# taxes 2% $416.67, ins $200, vacancy 5% $125, repairs 10% $250 -> NOI $1,508.33; minus $1,790.12 ->
# -$281.79/mo, -$3,381/yr; cash $16,750 -> CoC -20.2%; at $1,450/unit +$58.21/mo, CoC 4.2%. GRM 8.33;
# 1% ratio 1.00%. Fourplex: $400,000, FHA, P&I $2,687.28 + MIP $176.92 + tax 1.75% $583.33 + ins $300
# = PITI $3,747.53 vs $3,000 net self-sufficiency rent (125%); passes at ~$1,249/unit.

POST = dict(
 slug="house-hacking-in-indianapolis",
 title="House Hacking in Indianapolis: Duplex to Fourplex (2026)",
 headline="House Hacking in Indianapolis: How to Buy a Duplex to Fourplex and Live in One Unit",
 crumb="House Hacking in Indianapolis",
 h1_html="House Hacking in Indianapolis: <em>Live in One Unit, Rent the Rest</em>",
 desc=("How house hacking works in Indianapolis: FHA, conventional and VA loans for 2-4 unit homes, "
       "how lenders count rent, a worked duplex example and local rules."),
 date="2026-11-19", month="November 2026",
 category="Investment Properties", eyebrow="INVESTMENT PROPERTIES",
 focus="house hacking indianapolis",
 hero_sub=("How to buy a duplex, triplex or fourplex (or rent out rooms), live in one unit and let rent cover part "
           "of the mortgage, with 2026 loan rules, Indianapolis requirements and a fully worked example."),
 badges=["Investment Properties", "Updated for 2026", "Indianapolis"],
 read_min=10,
 card_title="House Hacking in Indianapolis",
 card_sub="Buy a duplex to fourplex, live in one unit, rent the rest.",
 qa_heading="House Hacking in Indianapolis at a Glance",
 qa_lead=("<strong>What is house hacking?</strong> Buying a home with two to four units (or a home with spare rooms), "
          "living in one unit and renting the others so tenants cover part of your mortgage. Because it&rsquo;s your "
          "principal residence, you can use owner-occupant loans: <strong>FHA with 3.5% down</strong>, <strong>conventional "
          "with 5% down</strong> through Fannie Mae&rsquo;s automated underwriting, or <strong>VA with no down payment</strong> "
          "for eligible veterans. Lenders generally count about 75% of the expected rent, and 3&ndash;4 unit FHA loans must "
          "pass a self-sufficiency test."),
 qa_facts=[
  ("FHA down payment", "3.5% with a 580+ credit score (HUD Handbook 4000.1, Aug 2026)"),
  ("Conventional", "5% down on 2&ndash;4 units via Fannie Mae DU (since Nov 18, 2023)"),
  ("VA", "Up to 4 units, $0 down if price &le; appraised value (VA, 2026)"),
  ("2026 FHA limits, Marion County", "$693,050 (2 units) &middot; $837,700 (3) &middot; $1,041,125 (4)"),
  ("Occupancy", "Move in within 60 days, stay at least 1 year (FHA and Fannie Mae)"),
  ("30-year fixed rate", "7.28% average (Freddie Mac, Nov 19, 2026)"),
 ],
 toc=[("what", "What House Hacking Is"), ("loans", "Loan Options for 2&ndash;4 Units"),
      ("rent", "How Lenders Count the Rent"), ("math", "Run the Numbers"),
      ("indy", "Indianapolis Rules to Know"), ("risks", "The Risks"), ("next", "Next Steps")],
 body="""
 <p>House hacking is one of the most practical ways to start investing in Indianapolis real estate: buy a duplex, triplex or fourplex, live in one unit and rent the others. Your tenants&rsquo; rent helps pay the mortgage while you build equity and learn landlording next door. It also comes with rules: occupancy requirements, lenders that discount the rent they&rsquo;ll count, and Indianapolis&rsquo;s own landlord registration. Below we cover 2026 loan options, how lenders count rent, a fully worked hypothetical example, local rules and the risks.</p>
 <p><em>This is general information, not lending, legal or tax advice. Loan rules change and lenders can add their own requirements, so confirm the details with your lender, attorney or CPA.</em></p>

 <h2 id="what">What House Hacking Is (and Isn&rsquo;t)</h2>
 <p>The classic version is a small multi-family property: you live in one unit and rent the other one to three. A lighter version is renting spare bedrooms in a single-family home. Either way, the property has to be your <strong>principal residence</strong>. That&rsquo;s what unlocks owner-occupant financing with far smaller down payments than an investment-property loan, and it&rsquo;s the commitment your lender holds you to. Our <a href="/glossary/house-hacking/">house hacking glossary entry</a> covers the basics. The owner-occupant programs below stop at four units; buildings with five or more are generally financed with commercial loans.</p>

 <h2 id="loans">Loan Options for 2&ndash;4 Unit Homes in 2026</h2>
 <h3>FHA: 3.5% down</h3>
 <p>FHA loans are the most common house-hacking tool. Under HUD&rsquo;s Single Family Housing Policy Handbook 4000.1 (updated August 12, 2026):</p>
 <ul>
  <li><strong>Down payment:</strong> 3.5% (a 96.5% maximum loan-to-value) with a minimum decision credit score of 580 or higher. Scores from 500 to 579 are limited to 90% loan-to-value, or 10% down.</li>
  <li><strong>Occupancy:</strong> at least one borrower must move in within 60 days of closing and intend to live there for at least one year. FHA generally won&rsquo;t insure more than one principal residence per borrower at a time.</li>
  <li><strong>Self-sufficiency test (3&ndash;4 units only):</strong> take the appraiser&rsquo;s fair market rent for <em>all</em> the units, including the one you&rsquo;ll live in, and subtract the greater of the appraiser&rsquo;s vacancy and maintenance estimate or 25%. What&rsquo;s left has to cover the full monthly payment (principal, interest, taxes and insurance).</li>
  <li><strong>Reserves:</strong> 3&ndash;4 unit properties need three months of payments in verified reserves after closing.</li>
  <li><strong>Mortgage insurance:</strong> 1.75% upfront plus 0.55% a year for the life of the loan with 3.5% down (on base loans up to $726,200).</li>
 </ul>
 <h3>Conventional: 5% down through Fannie Mae</h3>
 <p>Fannie Mae&rsquo;s November 18, 2023 update to Desktop Underwriter (DU), its automated underwriting system, raised the maximum loan-to-value on 2&ndash;4 unit principal residences, and its Eligibility Matrix now allows <strong>95% loan-to-value, or 5% down</strong>, on those purchases. That applies to loans approved through DU, not manually underwritten or high-balance loans. DU also requires <strong>six months of reserves</strong> on a 2&ndash;4 unit principal residence, and if you use grant money above 80% loan-to-value, at least 5% must come from your own funds. Expect private mortgage insurance with less than 20% down. The occupancy rule mirrors FHA&rsquo;s: move in within 60 days and stay at least a year.</p>
 <h3>VA: up to four units with no down payment</h3>
 <p>Eligible veterans and service members can use a VA-backed purchase loan on a home with up to four units, as long as they live in it, with no down payment if the price isn&rsquo;t higher than the appraised value (VA). Counting rent is stricter: under VA&rsquo;s underwriting rule (38 CFR 36.4340), the lender can only use rent from the other units if you can document that you&rsquo;re likely to succeed as a landlord and you have cash reserves to cover the payments for at least six months without that rent. See our <a href="/services/va-loan-buyers/">VA loan buyers</a> page.</p>
 <h3>2026 loan limits in Marion County</h3>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Units</th><th>FHA limit (Marion County)</th><th>Conforming limit (Fannie Mae / Freddie Mac)</th></tr></thead>
 <tbody>
 <tr><td>2 units</td><td>$693,050</td><td>$1,066,250</td></tr>
 <tr><td>3 units</td><td>$837,700</td><td>$1,288,800</td></tr>
 <tr><td>4 units</td><td>$1,041,125</td><td>$1,601,750</td></tr>
 </tbody>
 </table>
 </div>
 <p>These are maximum loan amounts. Marion County sits at FHA&rsquo;s national &ldquo;floor,&rdquo; and every Indiana county uses the baseline conforming limits for 2026 (HUD; FHFA). FHFA announced the 2026 figures on November 25, 2025, and HUD on December 11, 2025, so check for 2027 updates if you&rsquo;re closing next year.</p>

 <h2 id="rent">How Lenders Count the Rent</h2>
 <p>Lenders don&rsquo;t credit every dollar of rent. The usual 25% haircut covers vacancy and upkeep:</p>
 <ul>
  <li><strong>FHA:</strong> with no rental history on the property, the lender uses 75% of the lesser of the appraiser&rsquo;s fair market rent or the lease rent. That amount is added to your income; it doesn&rsquo;t reduce the payment, which still counts in full in your <a href="/glossary/debt-to-income-ratio/">debt-to-income ratio</a>.</li>
  <li><strong>Fannie Mae:</strong> gross monthly rent times 75%, supported by the appraiser&rsquo;s rent figures and any lease that transfers to you. With less than 12 months of property management experience, the rent can only offset the property&rsquo;s own payment.</li>
  <li><strong>VA:</strong> generally 75% of the rent, and only with the landlord documentation and reserves described above.</li>
 </ul>
 <p><strong>Renting rooms is harder to qualify with.</strong> FHA only counts boarder income (rent from someone living inside your own unit) with a current 12-month history, capped at 30% of your qualifying income. For a first purchase, plan to qualify on your own income and treat roommate rent as a bonus.</p>

 <h2 id="math">Run the Numbers: A Hypothetical Duplex</h2>
 <p><strong>Everything in this example is hypothetical and for illustration only.</strong> It isn&rsquo;t a listing, a rent survey or a loan quote. Our assumptions:</p>
 <ul>
  <li><strong>Price:</strong> $250,000 for a duplex with two similar units.</li>
  <li><strong>Loan:</strong> FHA with 3.5% down ($8,750). The 1.75% upfront premium is financed, for a $245,472 loan, plus 0.55% a year in annual premium.</li>
  <li><strong>Rate:</strong> 7.28% on a 30-year fixed, Freddie Mac&rsquo;s average for November 19, 2026.</li>
  <li><strong>Property taxes:</strong> 1.5% of the price a year, blending Indiana&rsquo;s 1% homestead cap on your unit with the 2% cap on the rented unit. The caps are ceilings, so a real bill could be lower.</li>
  <li><strong>Insurance:</strong> $2,400 a year for a policy that covers the rented unit (get a real quote).</li>
  <li><strong>Rent</strong> on the other unit: $1,250 a month. <strong>Closing costs:</strong> $8,000.</li>
 </ul>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Monthly, while you live there</th><th>Amount</th></tr></thead>
 <tbody>
 <tr><td>Principal and interest</td><td>$1,680</td></tr>
 <tr><td>FHA annual mortgage insurance</td><td>$111</td></tr>
 <tr><td>Property taxes</td><td>$312</td></tr>
 <tr><td>Insurance</td><td>$200</td></tr>
 <tr><td><strong>Total payment</strong></td><td><strong>$2,303</strong></td></tr>
 <tr><td>Less rent from the other unit</td><td>&minus;$1,250</td></tr>
 <tr><td><strong>Your net housing cost</strong></td><td><strong>$1,053</strong></td></tr>
 </tbody>
 </table>
 </div>
 <p><strong>Rent offset:</strong> the tenant covers about 54% of the payment. Set aside 15% of the rent ($187.50) for vacancy and repairs and your true cost is about $1,240 a month, while roughly $2,360 of your first year&rsquo;s payments goes to principal. If you&rsquo;d otherwise rent a unit like the one next door for $1,250, you&rsquo;re living for about the same cost and building equity. <strong>What the lender sees:</strong> FHA would add 75% of the rent, or $937.50, to your monthly income and count the full $2,303 payment. With two units, there&rsquo;s no self-sufficiency test.</p>
 <h3>The investor view: GRM, the 1% rule and cash-on-cash return</h3>
 <p>Now picture moving out after the first year and renting both units for $1,250 each, or $30,000 a year:</p>
 <ul>
  <li><strong><a href="/glossary/gross-rent-multiplier/">Gross rent multiplier</a> (GRM):</strong> $250,000 &divide; $30,000 = 8.3. A lower GRM means more rent per dollar of price, but it ignores expenses.</li>
  <li><strong>The 1% rule:</strong> $2,500 of monthly rent is 1.0% of the price, so this duplex just passes a rough screen many investors use. Passing doesn&rsquo;t make it a good deal.</li>
  <li><strong><a href="/glossary/cash-on-cash-return/">Cash-on-cash return</a>:</strong> annual cash flow divided by the cash you put in. Without the homestead cap, taxes rise to as much as $417 a month. Add $200 for insurance, $125 for 5% vacancy and $250 for repairs, and the property nets about $1,508 a month before the mortgage. Subtract the $1,790 loan payment and it loses about $282 a month, or $3,381 a year. On $16,750 of cash invested, that&rsquo;s a cash-on-cash return of about <strong>&minus;20%</strong>.</li>
 </ul>
 <p>That&rsquo;s the honest lesson at 7%-plus rates with 3.5% down: a property can pass the 1% rule and still lose money as a pure rental. Here, rents of about $1,450 per unit would turn cash flow slightly positive (about $58 a month, a 4% cash-on-cash return). The house hack works because you&rsquo;re replacing your own rent. Try your own numbers with our <a href="/services/mortgages/">mortgage calculator</a>, and see <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford in Indianapolis</a>.</p>
 <h3>Triplexes and fourplexes: the self-sufficiency hurdle</h3>
 <p>Now take a hypothetical $400,000 fourplex with an FHA loan and an appraised fair market rent of $1,000 per unit. HUD counts all four units, including yours: $4,000 minus 25% leaves $3,000. The payment (with taxes at a blended 1.75% and $3,600 a year of insurance) comes to about $3,748, or 125% of that figure, so it fails. Rents would need to be about $1,250 per unit to pass. Ask your lender to run this test before you write an offer.</p>

 <h2 id="indy">Indianapolis Rules to Know Before You Buy</h2>
 <h3>Register as a landlord</h3>
 <p>Owners or landlords of residential rental units in the City of Indianapolis have to register them with the city&rsquo;s Department of Business and Neighborhood Services, a program that started January 1, 2015. You register online through the city&rsquo;s Citizen Access portal, list an Indiana-based landlord or property manager contact and the number of rental units on each parcel, and renew every year; the city&rsquo;s fact sheet lists a $5 fee covering all of one owner&rsquo;s properties. Rentals in the excluded cities of Beech Grove, Lawrence, Southport and Speedway are exempt from the city registry, so check with those cities directly. Renting the other unit short-term? Since January 1, 2025, Indianapolis has required an annual permit for each short-term rental unit, with a one-time $150 fee on the first permit.</p>
 <h3>Indiana landlord&ndash;tenant basics</h3>
 <ul>
  <li><strong>Security deposits:</strong> within 45 days after the lease ends and you get the unit back, you must return the deposit minus allowed deductions (such as unpaid rent, damage from the tenant not following the law or the lease, and unpaid utilities the tenant owed), with an itemized written notice. Your obligation starts once the tenant gives you a mailing address in writing. If you don&rsquo;t comply, the tenant can recover the deposit plus reasonable attorney&rsquo;s fees (IC 32-31-3-12).</li>
  <li><strong>Your duties:</strong> deliver the unit safe, clean and habitable, comply with health and housing codes, keep common areas reasonably clean, and keep the electrical, plumbing, sanitary, heating, ventilation and air conditioning systems in good working order (IC 32-31-8-5).</li>
 </ul>
 <h3>Property taxes on a house hack</h3>
 <p>Indiana caps property taxes at 1% of gross assessed value for a homestead and 2% for other residential property, a category that includes buildings with two or more dwelling units (Indiana DLGF). The 1% cap covers only your homestead, so expect the rented units to fall under the higher cap, and the whole building if you move out. Ask the assessor how a property is split, and see our guide to <a href="/blog/indiana-property-tax-caps-explained/">Indiana&rsquo;s property tax caps</a>.</p>
 <h3>Make sure every unit is legal</h3>
 <p>A basement or attic unit that was never permitted isn&rsquo;t a legal unit, and it can cause problems with the appraisal, insurance and the city, so check zoning and permit history before you count on that rent. In our experience, 2&ndash;4 unit buildings are more common in Indianapolis&rsquo;s older neighborhoods closer to downtown than in newer, mostly single-family suburbs, and their age and condition vary a lot. Our <a href="/blog/multi-family-investing-indianapolis/">multi-family investing guide</a> covers the market side.</p>

 <h2 id="risks">The Risks: Vacancy, Repairs and Living Next to Your Tenant</h2>
 <ul>
  <li><strong>Vacancy:</strong> in a duplex, one empty unit means no rent at all. Keep reserves beyond the minimums and budget for turnover.</li>
  <li><strong>Repairs:</strong> two furnaces, two water heaters, one roof. Older buildings can surprise you, so price in near-term replacements the inspection turns up.</li>
  <li><strong>Being a landlord to your neighbor:</strong> you&rsquo;ll hear about the leaky faucet at 10 p.m. and have to enforce the lease with someone on the other side of the wall. Screen carefully and put everything in writing.</li>
  <li><strong>Insurance:</strong> standard homeowners policies are designed for personal risks, and many insurers treat regularly renting all or part of your home as business use (Triple-I). Tell your agent about the rented units and ask about landlord coverage, liability limits and lost rent. Tenants need their own renters policy.</li>
  <li><strong>Taxes:</strong> rent is taxable income. When you live in one unit of a duplex, the IRS has you split shared expenses such as mortgage interest and property taxes between the rental and personal parts, and you can depreciate the rental part (IRS Publication 527). Ask a CPA.</li>
  <li><strong>Occupancy is a commitment:</strong> misstating your plans on a loan application can have serious legal consequences. If your plans change, talk to your lender.</li>
 </ul>

 <h2 id="next">Next Steps</h2>
 <ol>
  <li><strong>Get pre-approved with a lender who does 2&ndash;4 unit loans.</strong> Not every loan officer regularly handles multi-unit FHA, conventional or VA loans. Ask how they&rsquo;ll count rent, what reserves you need and, for 3&ndash;4 units, whether a property passes self-sufficiency. See our <a href="/blog/pre-approval-vs-pre-qualification-indianapolis/">pre-approval guide</a>.</li>
  <li><strong>Run every property both ways:</strong> your net cost while you live there, and the full-rental cash flow if you move out.</li>
  <li><strong>Work with an agent who knows small multi-family.</strong> We can pull rent comparables, flag units that may not be legal and write an offer with the right inspection and appraisal protections. A written <a href="/services/buyer-representation/">Buyer Representation Agreement</a> is required before we tour homes with you, and it spells out our services and compensation (<a href="/blog/why-must-i-sign-a-buyer-agreement/">here&rsquo;s why</a>).</li>
 </ol>
 <p>Ready to look? See our <a href="/services/multi-family/">multi-family</a> and <a href="/services/investment-property/">investment property</a> services, or <a href="/schedule/">book a call with our team</a>.</p>
""",
 faqs=[
  ("Can I buy a duplex with an FHA loan in Indianapolis?",
   "Yes. FHA insures homes with up to four units as long as at least one borrower moves in within 60 days of closing and intends to live there at least a year. With a credit score of 580 or higher, the minimum down payment is 3.5%. In Marion County, the 2026 FHA loan limit is $693,050 for a two-unit property."),
  ("How much do I need to put down on a fourplex I'll live in?",
   "As little as 3.5% with FHA (580+ credit score), 5% with a conventional loan approved through Fannie Mae's Desktop Underwriter, or nothing with a VA loan if you're eligible and the price doesn't exceed the appraised value. FHA also requires three months of payments in reserves on a 3-4 unit property, and Fannie Mae's DU requires six months on a 2-4 unit principal residence."),
  ("What is the FHA self-sufficiency test?",
   "It applies to FHA loans on three- and four-unit properties. The appraiser's fair market rent for all units, including the one you'll live in, minus the greater of the appraiser's vacancy and maintenance estimate or 25%, must be at least equal to the monthly principal, interest, taxes and insurance."),
  ("Will the lender count the rent from the other units?",
   "Usually, but not all of it. FHA, Fannie Mae and VA generally count about 75% of the expected rent, based on the appraiser's rent estimate or a lease. FHA adds it to your income rather than subtracting it from the payment, Fannie Mae limits how it's used if you have less than 12 months of property management experience, and VA requires landlord documentation and six months of reserves."),
  ("Do I have to register a rental with the City of Indianapolis?",
   "Yes, if the rental unit is inside the City of Indianapolis. Owners or landlords of residential rental units must register with the Department of Business and Neighborhood Services and renew every year. Properties in the excluded cities of Beech Grove, Lawrence, Southport and Speedway are exempt from the city registry. Short-term rentals need a separate annual permit."),
  ("How long do I have to live in a house hack?",
   "FHA and Fannie Mae both expect you to move in within 60 days of closing and live there for at least one year. After that you can generally move out and keep the property as a rental, but talk to your lender about your plans, and expect the property taxes on your unit to rise once it's no longer your homestead."),
 ],
 sources=[
  ("HUD Handbook 4000.1, FHA Single Family Housing Policy (Aug 12, 2026)", "https://www.hud.gov/sites/default/files/Housing/documents/40001-hsgh-Update-18.pdf"),
  ("HUD, 2026 FHA loan limits (Dec 11, 2025)", "https://www.hud.gov/news/hud-no-25-145"),
  ("HUD FHA mortgage limits lookup (Marion County, CY2026)", "https://entp.hud.gov/idapp/html/hicostlook.cfm"),
  ("FHFA, 2026 conforming loan limits (Nov 25, 2025)", "https://www.fhfa.gov/news/news-release/fhfa-announces-conforming-loan-limit-values-for-2026"),
  ("Fannie Mae, 2-4 unit LTV change in DU (Oct 25, 2023)", "https://singlefamily.fanniemae.com/news-events/white-paper-responsibly-increasing-affordable-housing-supply-access-credit"),
  ("Fannie Mae Eligibility Matrix", "https://singlefamily.fanniemae.com/media/20786/display"),
  ("Fannie Mae Selling Guide B2-1.1-01, occupancy types", "https://selling-guide.fanniemae.com/sel/b2-1.1-01/occupancy-types"),
  ("Fannie Mae Selling Guide B3-3.8-02, rental income from the subject property", "https://selling-guide.fanniemae.com/sel/b3-3.8-02/rental-income-subject-property"),
  ("Fannie Mae Selling Guide B3-4.1-01, minimum reserves", "https://selling-guide.fanniemae.com/sel/b3-4.1-01/minimum-reserve-requirements"),
  ("Fannie Mae Selling Guide B3-4.3-06, grants", "https://selling-guide.fanniemae.com/sel/b3-4.3-06/grants-and-lender-contributions"),
  ("VA, purchase loans (updated Jan 7, 2026)", "https://www.va.gov/housing-assistance/home-loans/loan-types/purchase-loan/"),
  ("38 CFR 36.4340, VA underwriting standards", "https://www.ecfr.gov/current/title-38/chapter-I/part-36/subpart-B/subject-group-ECFR6c1bb6e9b0e3a3a/section-36.4340"),
  ("Freddie Mac Primary Mortgage Market Survey (Nov 19, 2026)", "https://www.freddiemac.com/pmms"),
  ("City of Indianapolis, landlord and short-term rental registries", "https://www.indy.gov/activity/landlord-registration-program"),
  ("IC 32-31-3-12, security deposits", "https://codes.findlaw.com/in/title-32-property/in-code-sect-32-31-3-12/"),
  ("IC 32-31-8-5, landlord obligations", "https://codes.findlaw.com/in/title-32-property/in-code-sect-32-31-8-5/"),
  ("Indiana DLGF, property tax caps (Nov 2025)", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("IRS Publication 527, residential rental property", "https://www.irs.gov/publications/p527"),
  ("Triple-I, peer-to-peer home rental insurance", "https://www.iii.org/article/peer-to-peer-home-rental"),
 ],
 related=[
  ("/blog/multi-family-investing-indianapolis/", "Multi-Family Investing in Indianapolis"),
  ("/blog/real-estate-investing-basics-indianapolis/", "Real Estate Investing Basics"),
  ("/blog/fha-loans-in-indiana-requirements-and-benefits/", "FHA Loans in Indiana"),
 ],
 cta=("Thinking About a House Hack?",
      "We&rsquo;ll help you find 2&ndash;4 unit properties that fit your budget, check the rent and the numbers before you offer, and connect you with lenders who do multi-unit FHA, conventional and VA loans.",
      [("/schedule/", "Book a Free Call &rarr;", "btn-white"), ("/services/multi-family/", "Multi-Family Services", "btn-outline")]),
 resources=[
  ("/services/multi-family/", "Multi-Family Homes"),
  ("/services/investment-property/", "Investment Property"),
  ("/services/mortgages/", "Mortgage Calculator"),
  ("/services/buyer-representation/", "Buyer Representation"),
 ],
 link_from=[
  ("glossary/house-hacking/index.html",
   'Want the full picture? Our guide to <a href="/blog/house-hacking-in-indianapolis/">house hacking in Indianapolis</a> covers FHA, conventional and VA loan rules for 2&ndash;4 unit homes, how lenders count rent and a worked duplex example.'),
  ("services/multi-family/index.html",
   'Planning to live in one unit? Read our guide to <a href="/blog/house-hacking-in-indianapolis/">house hacking in Indianapolis</a> for 2026 loan options, the FHA self-sufficiency test and a fully worked duplex example.'),
  ("blog/multi-family-investing-indianapolis/index.html",
   'Thinking of living in one unit while you rent the others? Our guide to <a href="/blog/house-hacking-in-indianapolis/">house hacking in Indianapolis</a> walks through FHA, conventional and VA financing, how lenders count rent, and the cash-on-cash math.'),
 ],
)
