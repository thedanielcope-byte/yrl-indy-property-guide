# How Much House Can I Afford in Indianapolis? (Nov 2026)
# Every figure is dated and sourced (researched Nov 2 2026):
#  - 30-yr fixed 7.24% (week of Oct 29 2026; 6.17% a year earlier): Freddie Mac PMMS + FRED MORTGAGE30US
#  - DTI: Fannie Mae Selling Guide B3-6-02 (36% manual, up to 45% w/ credit+reserves, 50% DU); CFPB "limits vary"
#  - FHA: HUD ML 2023-05 (UFMIP 1.75%; annual MIP 55 bps for >95% LTV, life of loan; 11 yrs at <=90% LTV)
#  - PMI: Freddie Mac My Home ($30-$70/mo per $100K; cancel at 20% equity; auto-ends at 78%)
#  - Insurance: Insurify, Indiana avg $2,023/yr end of 2025, +17.5% vs 2023 (published Mar 31 2026)
#  - Property tax: Indiana DLGF circuit-breaker fact sheet (1% homestead cap; referendum levies outside caps)
#  - Income: Census ACS 2025 1-yr B19013 (city balance $69,787; metro $83,815; U.S. $84,780)
#  - Price: MIBOR region median $320,000, Sept 2026 (our October 2026 market update)
# Table math (scratchpad calc.py): price = (0.28 * income/12 - insurance) / (monthly cost per $ of price),
# P&I at 7.24%/30 yrs; FHA loan = 96.5% x 1.0175, MIP 0.55%/yr of base loan; conventional loan 90%,
# PMI 0.60%/yr ($50 per $100K per month); taxes 1%/yr of price; insurance $2,023/yr. Rounded to $5,000.

POST = dict(
 slug="how-much-house-can-i-afford-indianapolis",
 title="How Much House Can I Afford in Indianapolis? (2026)",
 headline="How Much House Can I Afford in Indianapolis?",
 h1_html="How Much House Can I Afford <em>in Indianapolis?</em>",
 desc=("How much house can you afford in Indianapolis? Estimated prices for $60K to $150K incomes at today's 7.24% rate, "
       "with taxes, insurance and PMI built in."),
 date="2026-11-02", month="November 2026",
 category="Buying a Home", eyebrow="BUYING A HOME",
 focus="how much house can i afford indianapolis",
 hero_sub=("Estimated home budgets for $60,000 to $150,000 household incomes at today&rsquo;s mortgage rates, "
           "with property taxes, insurance and mortgage insurance built in."),
 badges=["Buying a Home", "Updated for 2026", "Indianapolis"],
 read_min=8,
 card_title="How Much House Can I Afford?",
 card_sub="What $60K to $150K incomes buy in Indianapolis at today's rates.",
 qa_heading="Indianapolis Home Affordability at a Glance",
 qa_lead=("<strong>How much house can I afford in Indianapolis?</strong> A common rule of thumb is to keep your total housing "
          "payment (mortgage, property taxes, insurance and mortgage insurance) at or under 28% of your gross income. At the "
          "7.24% average 30-year rate, that works out to roughly <strong>$230,000 on an $80,000 household income</strong> and "
          "<strong>$290,000 on $100,000</strong> with 10% down. Buying the region&rsquo;s $320,000 median home takes about "
          "$109,000 a year at that ratio. These are estimates. A lender&rsquo;s pre-approval is the real number."),
 qa_facts=[
  ("30-year fixed rate", "7.24% average (Freddie Mac, Oct 29, 2026)"),
  ("Median home price", "$320,000, MIBOR region (Sept 2026)"),
  ("Median household income", "$83,815 metro &middot; $69,787 city (Census, 2025)"),
  ("Rule of thumb", "Housing &le; 28% of gross income, all debts &le; 36%"),
  ("Income for the median home", "About $109,000 (10% down, 28% rule)"),
  ("Property tax cap", "1% of assessed value on a filed homestead"),
 ],
 toc=[("rule", "The 28/36 Rule"), ("table", "What Your Income Buys"), ("median", "Can You Afford the Median Home?"),
      ("costs", "Costs Beyond the Mortgage"), ("debts", "Debts and Rates"), ("stretch", "Making Your Budget Go Further"),
      ("next", "Next Steps")],
 body="""
 <p>&ldquo;How much house can we afford?&rdquo; is usually the first real question buyers ask us, and the honest answer has changed a lot in the past year. The average 30-year mortgage rate was <strong>7.24%</strong> in the last week of October 2026, up from 6.17% a year earlier (Freddie Mac). Below we walk through the math lenders use, show estimated price ranges for common Indianapolis household incomes, and cover the local costs, like Indiana&rsquo;s property tax cap, that change the answer. Treat every number here as a starting estimate, not a loan offer. Your lender&rsquo;s <a href="/blog/pre-approval-vs-pre-qualification-indianapolis/">pre-approval</a> is the number that counts.</p>

 <h2 id="rule">The 28/36 Rule (and What Lenders Actually Allow)</h2>
 <p>The most common rule of thumb is <strong>28/36</strong>. Keep your total housing payment (principal, interest, property taxes, homeowners insurance and any mortgage insurance, often shortened to <a href="/glossary/piti/">PITI</a>) at or under 28% of your gross monthly income, and keep all monthly debt payments, housing included, at or under 36%. That second figure is your <a href="/glossary/debt-to-income-ratio/">debt-to-income ratio</a>.</p>
 <p>28/36 is a comfort guideline, not a lender rule. Limits vary by loan type and lender, as the Consumer Financial Protection Bureau notes. For conventional loans, Fannie Mae caps total debt-to-income at 36% for manually underwritten loans, or up to 45% with strong credit and cash reserves, and its automated underwriting system can approve up to 50%. So you may well be approved for more than the tables below show. Whether you <em>should</em> borrow that much is a budget question only you can answer.</p>

 <h2 id="table">What Your Income Buys in Indianapolis</h2>
 <p>Here&rsquo;s what each household income supports under the 28% guideline. We used these assumptions:</p>
 <ul>
  <li><strong>Rate:</strong> 30-year fixed at 7.24%, Freddie Mac&rsquo;s weekly average for October 29, 2026. Your rate depends on credit, loan type and points, and FHA rates can differ.</li>
  <li><strong>Payment:</strong> total housing cost of 28% of gross income. The last column shows a lender approving you at 36%.</li>
  <li><strong>No other debts</strong> (car loans, student loans or credit cards). See the next sections for how debts change this.</li>
  <li><strong>Property taxes:</strong> 1% of the price per year, the ceiling for a homestead under Indiana&rsquo;s tax cap.</li>
  <li><strong>Homeowners insurance:</strong> $2,023 a year, Insurify&rsquo;s Indiana average at the end of 2025.</li>
  <li><strong>FHA:</strong> 3.5% down, a 1.75% upfront mortgage insurance premium added to the loan, and 0.55% a year in annual premium (HUD).</li>
  <li><strong>Conventional:</strong> 10% down, with private mortgage insurance (PMI) at $50 a month per $100,000 borrowed, the middle of Freddie Mac&rsquo;s $30 to $70 range.</li>
  <li>No HOA dues. Down payment and closing costs are paid separately. Prices are rounded to the nearest $5,000.</li>
 </ul>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Household income</th><th>Housing budget (28%)</th><th>FHA, 3.5% down</th><th>Conventional, 10% down</th><th>10% down, approved at 36%</th></tr></thead>
 <tbody>
 <tr><td>$60,000</td><td>$1,400/mo</td><td>~$155,000</td><td>~$165,000</td><td>~$220,000</td></tr>
 <tr><td>$80,000</td><td>$1,867/mo</td><td>~$215,000</td><td>~$230,000</td><td>~$300,000</td></tr>
 <tr><td>$100,000</td><td>$2,333/mo</td><td>~$270,000</td><td>~$290,000</td><td>~$380,000</td></tr>
 <tr><td>$125,000</td><td>$2,917/mo</td><td>~$345,000</td><td>~$370,000</td><td>~$485,000</td></tr>
 <tr><td>$150,000</td><td>$3,500/mo</td><td>~$420,000</td><td>~$450,000</td><td>~$585,000</td></tr>
 </tbody>
 </table>
 </div>
 <p>To see how the payment breaks down, take the $100,000 household buying at about $290,000 with 10% down. That&rsquo;s roughly $1,790 a month in principal and interest, $131 in PMI, $243 in property taxes and $169 in insurance, for about $2,333 total. FHA prices come out lower than conventional because the upfront premium is added to the loan and the annual premium runs higher than the PMI we assumed, even though the down payment is much smaller. Want to try your own numbers? Use our <a href="/services/mortgages/">mortgage calculator</a>.</p>

 <h2 id="median">Can You Afford the Median Indianapolis Home?</h2>
 <p>The median single-family home in the MIBOR region sold for <strong>$320,000</strong> in September 2026, according to our <a href="/blog/indianapolis-market-update-october-2026/">October market update</a>. Using the same assumptions, a $320,000 home costs about <strong>$2,540 a month</strong> with 10% down ($32,000) or about <strong>$2,720</strong> with FHA&rsquo;s 3.5% down ($11,200). Under the 28% guideline, that takes a household income of roughly <strong>$109,000</strong> with 10% down, or about $116,500 with FHA.</p>
 <p>For comparison, the median household income was <strong>$83,815</strong> across the Indianapolis metro and $69,787 in the city itself in 2025 (U.S. Census Bureau). At 28%, the typical metro household supports about $240,000 with 10% down. In other words, at today&rsquo;s rates the median home is a stretch for the median household under the conservative rule. Buyers close that gap with a higher approved ratio, down payment help, a second income, or by shopping below the median. Plenty of the metro sits below it: our market update shows Marion County homes ranging from the $150s, and Johnson and Hendricks counties from the $250s.</p>

 <h2 id="costs">The Costs Beyond the Mortgage</h2>
 <h3>Property taxes</h3>
 <p>Indiana caps property taxes on an owner-occupied home at <strong>1% of its gross assessed value</strong>, but only after you file your homestead deduction. That&rsquo;s why we used 1% as a conservative estimate. After deductions, many homestead bills land below the cap. Two caveats: voter-approved referendum levies for schools or public safety can sit outside the caps (Indiana DLGF), and because Indiana property taxes are billed a year in arrears, your first bills reflect the seller&rsquo;s assessment and deductions. Ask your lender how they&rsquo;re estimating your escrow. Our guides to <a href="/blog/indiana-property-tax-caps-explained/">Indiana&rsquo;s property tax caps</a> and <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">filing your homestead exemption</a> explain the details.</p>
 <h3>Homeowners insurance</h3>
 <p>Insurify puts Indiana&rsquo;s average homeowners premium at <strong>$2,023 a year</strong> at the end of 2025, up 17.5% since 2023. Premiums vary widely by home, ZIP code, roof age and claims history, so get a quote early in your search rather than at the closing table.</p>
 <h3>Mortgage insurance</h3>
 <p>Put less than 20% down on a conventional loan and you&rsquo;ll typically pay <a href="/glossary/private-mortgage-insurance/">PMI</a>. Freddie Mac estimates $30 to $70 a month per $100,000 borrowed, depending mostly on your credit score and down payment. You can ask to cancel it once you reach 20% equity, and it ends automatically when your balance is scheduled to hit 78% of the original value. FHA loans work differently: a 1.75% upfront premium plus an annual premium that, with less than 10% down, lasts for the life of the loan (HUD). See our <a href="/blog/fha-loans-in-indiana-requirements-and-benefits/">guide to FHA loans in Indiana</a>.</p>
 <h3>HOA dues and closing costs</h3>
 <p>Many newer subdivisions around Indianapolis have HOA dues, which count toward your housing payment and shrink your budget. You&rsquo;ll also need cash for <a href="/services/closing-costs-buyers/">buyer closing costs</a> on top of the down payment, so get an estimate from your lender before you set a price ceiling.</p>

 <h2 id="debts">How Debts and Rates Change the Number</h2>
 <p>The table assumes no other debts. Once your other payments push you past the 36% total limit, every dollar of debt comes straight out of your housing budget. Take an $80,000 household with $800 a month in car and student loan payments: 36% of income is $2,400, which leaves $1,600 for housing and drops the estimate from about $230,000 to about <strong>$195,000</strong> with 10% down. As a rough guide, every $100 a month of payment equals about $13,500 of purchase price at today&rsquo;s rate.</p>
 <p>Rates matter just as much. If rates were a full point lower, at 6.24%, the same $100,000 household would qualify for about <strong>$315,000</strong> with 10% down instead of $290,000. Nobody can promise where rates go, so we&rsquo;d set your budget on today&rsquo;s rate and treat any drop as a bonus.</p>

 <h2 id="stretch">Ways to Make Your Budget Go Further</h2>
 <ul>
  <li><strong>Down payment assistance.</strong> Indiana has state and local programs that help with the down payment and closing costs for qualifying buyers. Start with our <a href="/blog/down-payment-assistance-programs-in-indiana-2026/">guide to Indiana down payment assistance</a>.</li>
  <li><strong>Pay down a monthly payment.</strong> Clearing a car loan or a credit card balance before you apply can add more buying power than the same cash put toward your down payment.</li>
  <li><strong>Improve your credit.</strong> A higher score usually means a better rate and cheaper PMI.</li>
  <li><strong>Widen the map.</strong> Price ranges vary a lot across Central Indiana. Our <a href="/blog/first-time-home-buyer-guide-indianapolis-2026/">first-time buyer guide</a> covers where your budget goes furthest.</li>
  <li><strong>Ask about seller concessions.</strong> In some negotiations, sellers help with closing costs or a rate buydown. It depends on the home and the market at the time.</li>
 </ul>

 <h2 id="next">Next Steps</h2>
 <p>Use the table to get a feel for your price range, then get a real number. A lender&rsquo;s <a href="/blog/pre-approval-vs-pre-qualification-indianapolis/">pre-approval</a> looks at your actual credit, income, debts and loan options, and sellers expect one with your offer. Our team can connect you with local lenders, help you set a monthly payment you&rsquo;re comfortable with, and show you which parts of the metro fit it. <a href="/schedule/">Book a free call with our team</a> or <a href="/search/">start browsing homes</a> in your range.</p>
""",
 faqs=[
  ("How much house can I afford on $60,000 a year in Indianapolis?",
   "Under the 28% guideline, a $60,000 household income supports about $1,400 a month for housing, or roughly $155,000 with an FHA loan (3.5% down) or $165,000 with 10% down at the 7.24% average rate from late October 2026. That assumes no other debts and includes property taxes, insurance and mortgage insurance. A lender may approve more."),
  ("How much house can I afford on $100,000 a year?",
   "About $270,000 with FHA (3.5% down) or $290,000 with 10% down if you keep housing at 28% of gross income, at the 7.24% average rate from late October 2026 with no other debts. If a lender approves you at 36% of income, the 10% down figure rises to roughly $380,000."),
  ("What salary do you need to buy a house in Indianapolis?",
   "To buy the MIBOR region's $320,000 median home (September 2026) while keeping housing at 28% of gross income, you'd need roughly $109,000 a year with 10% down or about $116,500 with FHA's 3.5% down, at a 7.24% rate. You can buy with less income if a lender approves a higher ratio, you use down payment assistance, or you buy below the median."),
  ("What is the 28/36 rule?",
   "It's a rule of thumb: spend no more than 28% of your gross monthly income on housing (principal, interest, taxes, insurance and mortgage insurance) and no more than 36% on all debt payments combined. Lenders often allow more. Fannie Mae, for example, can approve total debt-to-income up to 50% through automated underwriting."),
  ("Are Indiana property taxes really capped at 1%?",
   "For an owner-occupied home with a filed homestead deduction, Indiana's constitution caps the tax bill at 1% of gross assessed value. Voter-approved referendum levies can add to that, and the first bills after you buy are based on the seller's assessment and deductions because Indiana taxes are billed a year in arrears."),
  ("How much does a lower mortgage rate change what I can afford?",
   "A lot. Using our assumptions, a $100,000 household with 10% down can afford about $290,000 at 7.24%, but about $315,000 if rates were a full point lower at 6.24%. Each $100 of monthly payment equals about $13,500 of purchase price at today's rate."),
 ],
 sources=[
  ("Freddie Mac Primary Mortgage Market Survey (Oct 29, 2026)", "https://www.freddiemac.com/pmms"),
  ("Fannie Mae Selling Guide B3-6-02, debt-to-income ratios", "https://selling-guide.fanniemae.com/sel/b3-6-02/debt-income-ratios"),
  ("CFPB, what is a debt-to-income ratio", "https://www.consumerfinance.gov/ask-cfpb/what-is-a-debt-to-income-ratio-en-1791/"),
  ("HUD Mortgagee Letter 2023-05, FHA premiums", "https://www.hud.gov/sites/dfiles/OCHCO/documents/2023-05hsgml.pdf"),
  ("Freddie Mac, breaking down PMI", "https://myhome.freddiemac.com/buying/breaking-down-pmi"),
  ("Insurify, Indiana home insurance costs (Mar 2026)", "https://insurify.com/homeowners-insurance/news/indiana-rate-increases/"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("Indiana DLGF, property tax due dates", "https://www.in.gov/dlgf/understanding-your-tax-bill/property-tax-due-dates/"),
  ("U.S. Census Bureau, American Community Survey 2025 (table B19013)", "https://www.census.gov/programs-surveys/acs/news/data-releases/2025/release.html"),
  ("home prices: MIBOR REALTOR&reg; Association via our market update", "/blog/indianapolis-market-update-october-2026/"),
 ],
 related=[
  ("/blog/pre-approval-vs-pre-qualification-indianapolis/", "Pre-Approval vs. Pre-Qualification"),
  ("/blog/down-payment-assistance-programs-in-indiana-2026/", "Down Payment Assistance in Indiana"),
  ("/blog/first-time-home-buyer-guide-indianapolis-2026/", "First-Time Home Buyer Guide 2026"),
 ],
 cta=("Find Out What You Can Comfortably Buy",
      "We&rsquo;ll help you set a realistic budget, connect you with local lenders for a pre-approval and show you which Central Indiana areas fit your number.",
      [("/schedule/", "Book a Free Call &rarr;", "btn-white"), ("/services/mortgages/", "Try the Mortgage Calculator", "btn-outline")]),
 resources=[
  ("/services/mortgages/", "Mortgage Calculator"),
  ("/services/mortgage-pre-approval/", "Mortgage Pre-Approval"),
  ("/services/first-time-home-buyers/", "First-Time Home Buyers"),
  ("/services/closing-costs-buyers/", "Buyer Closing Costs"),
 ],
 link_from=[
  ("blog/first-time-home-buyer-guide-indianapolis-2026/index.html",
   'Not sure what price range to shop in? Our guide to <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford in Indianapolis</a> shows estimated budgets for incomes from $60,000 to $150,000 at today&rsquo;s rates.'),
  ("blog/pre-approval-vs-pre-qualification-indianapolis/index.html",
   'Before you talk to a lender, see our estimates of <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford in Indianapolis</a> on your income, including taxes, insurance and mortgage insurance.'),
 ],
)
