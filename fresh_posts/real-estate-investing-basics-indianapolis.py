# Investing in Indianapolis real estate: the consolidated pillar (Nov 19 2026).
# Replaces three overlapping pages that split Google's attention for "investing in indianapolis
# real estate" and related queries (GSC 90 days to Nov 19 2026): this URL (195 impressions on the
# head term, avg position ~20), /guides/indianapolis-real-estate-investing/ and
# /blog/investment-property-in-indianapolis-is-now-a-good-time/. Those two now redirect here; the
# transactional side lives at /services/investment-property/ (the /indianapolis-investment-properties/
# hub redirects there). Content merged from all three; original publish date kept.
# General information, not investment, legal or tax advice. Facts reused from sourced posts:
#  - Marion County, October 2026 (MIBOR via build_market_social.py DATA): median $249,900 (-2.0% YoY),
#    791 sales (-14.2%), 32 median days on market (22 a year earlier), 4.0 months of supply.
#  - Freddie Mac PMMS 7.28% for Nov 19 2026 (same figure as house-hacking-in-indianapolis.py).
#  - FHA 3.5% down (580+), Fannie Mae DU 5% down on 2-4 unit principal residences: see the sourcing
#    notes in fresh_posts/house-hacking-in-indianapolis.py.
#  - Indiana DLGF circuit-breaker caps: 1% homestead, 2% other residential (incl. rentals and
#    2+ unit buildings).
#  - indy.gov Landlord Registry: residential rental units in the City must be registered, renewed
#    annually; excluded cities (Beech Grove, Lawrence, Southport, Speedway) exempt.
#  - IC 32-31-3-12: deposit + itemized notice within 45 days of termination and possession.
#  - IRS Pub 527: residential rental property depreciated over 27.5 years (GDS); depreciation
#    allowed or allowable reduces basis. IRS like-kind exchange tips: identify replacement property
#    within 45 days, receive it within 180 days (or the return due date, if earlier); real property
#    held for investment or business use.
POST = dict(
 slug="real-estate-investing-basics-indianapolis",
 title="Investing in Indianapolis Real Estate: 2026 Guide",
 headline="Investing in Indianapolis Real Estate: The Complete 2026 Guide",
 crumb="Investing in Indianapolis Real Estate",
 h1_html="Investing in Indianapolis Real Estate: <em>The Complete Guide</em>",
 desc=("How to invest in Indianapolis real estate in 2026: strategies, where investors buy, running the "
       "numbers, financing, Indiana landlord rules and taxes."),
 date="2026-08-17", modified="2026-11-19", month="November 2026",
 category="Investment Properties", eyebrow="INVESTMENT PROPERTIES",
 focus="investing in indianapolis real estate",
 hero_sub=("Strategies, neighborhoods, financing, landlord rules and the expense assumptions most investors get "
           "wrong, from a local team that will tell you when a deal doesn&rsquo;t work."),
 badges=["Investment Properties", "Updated for 2026", "Central Indiana"],
 read_min=13,
 card_title="Investing in Indianapolis Real Estate",
 card_sub="Strategies, neighborhoods, numbers and landlord rules for 2026.",
 qa_heading="Investing in Indianapolis Real Estate at a Glance",
 qa_lead=("<strong>Is Indianapolis a good place to invest in real estate?</strong> For a patient, selective investor, "
          "often yes. Purchase prices sit well below many large metros while rents don&rsquo;t fall proportionally, "
          "the job base is diverse and the suburbs keep growing. But at 2026 interest rates monthly cash flow is "
          "thinner than it was a few years ago, and Indianapolis changes <strong>block by block</strong>. Run "
          "conservative numbers, <strong>buy for cash flow</strong> and treat appreciation as a bonus."),
 qa_facts=[
  ("Common strategies", "Buy-and-hold rentals, small multi-family, house hacking, fix-and-flip"),
  ("Typical entry prices", "$150s&ndash;$450s depending on area and condition (ranges, not quotes)"),
  ("Marion County median sale price", "$249,900, down 2.0% from a year earlier (MIBOR, October 2026)"),
  ("30-year fixed rate", "7.28% average (Freddie Mac, Nov 19, 2026)"),
  ("Property tax cap on a rental", "2% of assessed value, vs. 1% on a homestead (Indiana DLGF)"),
  ("Cheapest way in", "House hack a 2&ndash;4 unit: 3.5% down FHA or 5% down conventional"),
 ],
 toc=[("why", "Why Investors Look at Indianapolis"), ("timing", "Is Now a Good Time?"),
      ("strategy", "Pick a Strategy First"), ("where", "Where Investors Buy"),
      ("numbers", "Running the Numbers"), ("financing", "Financing"),
      ("landlord", "Indiana Landlord Basics"), ("taxes", "Taxes and 1031 Exchanges"),
      ("mistakes", "Common Mistakes"), ("start", "How to Get Started")],
 body="""
 <p>Indianapolis shows up on nearly every list of the best Midwest markets for rental property, and the attention isn&rsquo;t hype. In markets where a modest house costs three or four times what it does here, the same rent doesn&rsquo;t cover the same mortgage. That price-to-rent relationship is why investors from across the country look at Central Indiana. It doesn&rsquo;t make it easy money, though. Cheap houses are cheap for reasons, out-of-state buyers routinely underestimate expenses, and the difference between a good rental and a bad one here is often two blocks. This guide covers how to think about investing in Indianapolis real estate in 2026, whether it&rsquo;s your first rental or your fifteenth.</p>
 <p><em>Not investment advice. This is general education about a local market, not a recommendation to buy any particular property or a promise of returns. Talk to your CPA, lender and attorney about your situation.</em></p>

 <h2 id="why">Why Investors Look at Indianapolis</h2>
 <ul>
  <li><strong>Price-to-rent ratio.</strong> Entry prices sit well below many comparable metros, with rents that don&rsquo;t fall proportionally. Less capital goes in, and there&rsquo;s more room for positive <a href="/glossary/cash-flow/">cash flow</a> at current rents.</li>
  <li><strong>A diverse employment base.</strong> Healthcare, life sciences, logistics, insurance, manufacturing and a growing tech sector. No single-industry dependence, which keeps tenant demand steadier through downturns.</li>
  <li><strong>Suburban growth.</strong> Hamilton, Boone, Hendricks and Johnson counties have grown substantially, supporting both rentals and resale. New residents arrive from the rest of Indiana and from higher-cost states.</li>
  <li><strong>A workable legal environment.</strong> Indiana&rsquo;s landlord&ndash;tenant framework is generally considered balanced and predictable, which matters when things don&rsquo;t go to plan. You still have to follow it precisely.</li>
  <li><strong>Inventory variety.</strong> Everything from pre-war doubles near downtown to newer suburban single-family homes.</li>
 </ul>

 <h2 id="timing">Is Now a Good Time to Buy Investment Property in Indianapolis?</h2>
 <p>There&rsquo;s no perfect moment, and waiting for one is the most common reason people never buy their first rental. Rates, inventory and prices are always moving. What you can control is buying a sound property at a fair price, in an area with real rental demand, at a payment you can comfortably carry. A good deal you can hold beats a perfect deal you keep waiting for.</p>
 <p>That said, 2026 is a different environment than 2018 or 2021:</p>
 <ul>
  <li><strong>Rental demand is solid.</strong> Population growth, a shortage of affordable homes for sale that keeps would-be buyers renting longer, and in-migration from pricier markets all support it. Suburban single-family rentals in areas like Greenwood, Avon, Brownsburg, Lawrence and the east side have been especially active with families who want good schools but aren&rsquo;t ready to buy.</li>
  <li><strong>Financing costs more.</strong> The 30-year fixed averaged 7.28% on November 19, 2026 (Freddie Mac). Leveraged buyers see much thinner monthly cash flow than they did in 2019&ndash;2021, and tenants expect more while operating costs have risen.</li>
  <li><strong>Prices have cooled a little.</strong> In Marion County, MIBOR reported a median sale price of $249,900 in October 2026, down 2.0% from a year earlier, with homes taking a median 32 days to sell (22 a year earlier) and 4.0 months of supply. More time on market can mean more room to negotiate. See our <a href="/market-updates/">monthly market updates</a> for the latest county figures.</li>
 </ul>
 <p>The upshot: today&rsquo;s buyers are getting in at more realistic valuations than the low-rate era, which rewards investors who are patient, selective and conservative with their numbers.</p>

 <h2 id="strategy">Pick a Strategy First</h2>
 <p>Most investor mistakes trace back to buying a property that doesn&rsquo;t match the strategy. Decide how hands-on you want to be, how much capital you&rsquo;ll commit and how long you&rsquo;ll hold before you look at listings.</p>
 <h3>Buy and hold (single-family rentals)</h3>
 <p>The most common approach here, and the one the price-to-rent ratio best supports. A well-located single-family home tends to attract longer-term tenants, needs less intensive management and has a more liquid exit: you can sell to another investor or to an owner-occupant. The trade-off is that a vacancy takes 100% of your rent, so tenant quality and retention matter enormously. See <a href="/services/rental-property/">rental property</a> and <a href="/services/cash-flow-properties/">cash flow properties</a>.</p>
 <h3>Small multi-family (2&ndash;4 units)</h3>
 <p>Duplexes through fourplexes still finance as residential property, spread income across units so one vacancy doesn&rsquo;t zero out your rent, and Indianapolis has an unusual supply of older doubles in Marion County and the inner-ring suburbs. Management is more intensive and the pool of exit buyers is smaller. Our <a href="/blog/multi-family-investing-indianapolis/">multi-family investing guide</a> goes deeper.</p>
 <h3>House hacking</h3>
 <p>Live in one unit of a small multi-family and rent the others. Because it&rsquo;s your principal residence, you can often use an owner-occupant loan with a far smaller down payment than an investor loan, which makes it the cheapest entry into investing there is. Our <a href="/blog/house-hacking-in-indianapolis/">house hacking guide</a> covers 2026 FHA, conventional and VA rules and a fully worked duplex example.</p>
 <h3>Fix and flip, and BRRRR</h3>
 <p><a href="/glossary/fix-and-flip/">Flipping</a> works in appreciating neighborhoods, but your margin depends entirely on your rehab estimate and <a href="/glossary/after-repair-value/">after-repair value</a> being right. Buy, rehab, rent, refinance, repeat (BRRRR) adds a rental and a cash-out refinance, so it also depends on what lenders and appraisers will support. Both suit hands-on investors with a reliable contractor. See <a href="/services/fix-and-flip/">fix and flip</a> and, for below-market inventory, <a href="/services/foreclosures/">HUD, VA and Fannie Mae foreclosures</a>.</p>
 <h3>Turnkey and portfolio building</h3>
 <p>Already-rented homes cost market value but produce rent from day one, which suits out-of-state and passive investors (verify the lease, the rent roll and the condition yourself). If you&rsquo;re scaling, see <a href="/services/off-market-properties/">off-market properties</a> and, when it&rsquo;s time to exit, <a href="/services/portfolio-selling/">portfolio selling</a>.</p>

 <h2 id="where">Where Investors Buy in Central Indiana</h2>
 <p>There&rsquo;s a trade-off between yield and stability. Lower-priced areas can show stronger cash flow on paper and carry more management intensity; higher-priced suburbs offer steadier tenants and appreciation with thinner monthly margins.</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Area type</th><th>Examples</th><th>Typical prices</th><th>Profile</th></tr></thead>
 <tbody>
 <tr><td>Inner-ring value</td><td><a href="/neighborhoods/warren-township-indianapolis/">Warren Township</a>, <a href="/neighborhoods/garfield-park-indianapolis/">Garfield Park</a></td><td>$150s&ndash;$350s</td><td>Lower entry, higher management intensity</td></tr>
 <tr><td>Appreciating urban</td><td><a href="/neighborhoods/irvington-indianapolis/">Irvington</a>, <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a></td><td>$150s&ndash;$500s+</td><td>Mix of cash flow and appreciation</td></tr>
 <tr><td>Stable suburban</td><td><a href="/cities/marion-county/lawrence-indiana-real-estate/">Lawrence</a>, <a href="/cities/marion-county/beech-grove-indiana-real-estate/">Beech Grove</a></td><td>$150s&ndash;$320s</td><td>Steadier tenants, moderate yield</td></tr>
 <tr><td>Growth suburbs</td><td><a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a>, <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a></td><td>$250s&ndash;$450s</td><td>Appreciation-led, thinner monthly margins</td></tr>
 <tr><td>Outlying value</td><td><a href="/cities/madison-county/anderson-indiana-real-estate/">Anderson</a>, <a href="/cities/shelby-county/shelbyville-indiana-real-estate/">Shelbyville</a></td><td>$150s&ndash;$300s</td><td>Lowest entry, thinner tenant pools</td></tr>
 </tbody>
 </table>
 </div>
 <p>Price ranges are general and vary by submarket and condition. A few areas experienced local investors keep coming back to:</p>
 <ul>
  <li><strong>Lawrence and the northeast side:</strong> solid single-family inventory at accessible prices, steady demand from working families and proximity to northeast-side employers.</li>
  <li><strong>Beech Grove:</strong> a small, independent city surrounded by Indianapolis, with affordable single-family homes that tend to stay occupied. It rewards patient landlords.</li>
  <li><strong>Greenwood and southern Johnson County:</strong> strong tenants who want good schools and suburban amenities, typically with low vacancy, though purchase prices have risen accordingly.</li>
  <li><strong><a href="/neighborhoods/perry-township-indianapolis/">Southport and Perry Township</a>:</strong> stable south-side neighborhoods with consistent rental demand and moderate entry prices.</li>
  <li><strong>Near east and near south:</strong> Irvington, Fountain Square and the corridor toward Beech Grove have seen real revitalization and better tenant quality over the past decade. Entry prices are higher than they were, and so is the tenant base.</li>
  <li><strong><a href="/cities/hancock-county/mccordsville-indiana-real-estate/">McCordsville</a> and the Avon/Brownsburg/Plainfield corridor:</strong> newer housing stock and family tenant demand; more of an appreciation play than a cash-flow play.</li>
 </ul>
 <p>The most important thing to understand, especially from out of state: <strong>Indianapolis varies block by block.</strong> A street can change character within two blocks in a way no spreadsheet or satellite view will show you. Drive it at different times of day, check what comparable homes actually rent for, and watch where the area is heading. New employers, road projects and school changes can all signal an area on the rise.</p>

 <h2 id="numbers">Running the Numbers Properly</h2>
 <p>Cash flow is what&rsquo;s left each month after <em>every</em> expense, not just the mortgage. The most common error is underestimating expenses. A realistic model includes, at minimum:</p>
 <ul>
  <li>Mortgage principal and interest</li>
  <li><strong>Property taxes at the rental rate.</strong> Indiana caps property taxes at 1% of assessed value on a homestead but 2% on other residential property, which includes rentals (Indiana DLGF). Don&rsquo;t model an investment property using the current owner&rsquo;s homestead tax bill. Our guide to <a href="/blog/indiana-property-tax-caps-explained/">Indiana&rsquo;s property tax caps</a> explains how it works.</li>
  <li>Insurance: a landlord policy, which typically costs more than a homeowners policy</li>
  <li>Vacancy. Assume some; 100% occupancy is not a plan.</li>
  <li>Maintenance and capital expenditures. Roofs, furnaces and water heaters have finite lives and will come due.</li>
  <li>Property management, if you won&rsquo;t self-manage</li>
  <li>Turnover costs: cleaning, paint and re-leasing</li>
  <li>HOA dues, if any (some neighborhoods also restrict rentals, so read the covenants)</li>
 </ul>
 <p>Then judge the deal with real metrics: <a href="/glossary/net-operating-income/">net operating income</a>, <a href="/glossary/capitalization-rate/">cap rate</a> and <a href="/glossary/cash-on-cash-return/">cash-on-cash return</a>. Rules of thumb like the &ldquo;1% rule&rdquo; or a <a href="/glossary/gross-rent-multiplier/">gross rent multiplier</a> are screening shortcuts, not analysis; they ignore condition, taxes and where the neighborhood is heading. Use them to decide what to look at, never what to buy.</p>
 <h3>What returns to realistically expect</h3>
 <p>Too many investors arrive with expectations set by seminars and social media rather than local numbers. In practice:</p>
 <ul>
  <li><strong>Gross yield</strong> (annual rent divided by price) varies a lot by submarket. Cheaper inner-city homes can show higher gross yields but carry more maintenance, management and vacancy risk. Suburban rentals show more moderate gross yields and more predictable net results once expenses are counted.</li>
  <li><strong>Cash flow</strong> at today&rsquo;s rates is thin for buyers putting 20&ndash;25% down. Cash-heavy or lower-leverage buyers have better monthly economics. Be selective on price and don&rsquo;t skip the capital-reserve line.</li>
  <li><strong>Appreciation</strong> has been a meaningful part of total return here over the past decade, and the long-term trend has been positive. It still isn&rsquo;t a reason to buy a property that doesn&rsquo;t work at today&rsquo;s numbers.</li>
 </ul>
 <p>Real estate wealth is usually built slowly: rent tends to rise over time while a fixed-rate payment stays put and the loan balance shrinks. Think in terms of five, ten or twenty years, not months.</p>

 <h2 id="financing">Financing an Investment Property</h2>
 <p>Investment loans differ from owner-occupant loans: expect a larger down payment, somewhat higher rates and reserve requirements, with lenders typically wanting several months of payments in the bank. Three things worth knowing:</p>
 <ul>
  <li><strong>Living in one unit changes everything.</strong> On a 2&ndash;4 unit home you&rsquo;ll occupy, FHA allows 3.5% down with a 580+ credit score and Fannie Mae&rsquo;s automated underwriting allows 5% down conventional, far less than a typical investor loan. Details are in our <a href="/blog/house-hacking-in-indianapolis/">house hacking guide</a>.</li>
  <li><strong>DSCR loans</strong> qualify on the property&rsquo;s rental income rather than your personal income, and are common for investors scaling a portfolio. Expect different pricing and terms than a conventional loan.</li>
  <li><strong>Use a lender who actually does investor lending.</strong> Not all do. Get pre-approved before you shop so you can move when the right property appears. Our <a href="/services/mortgages/">mortgage calculator</a> helps you rough out payments.</li>
 </ul>

 <h2 id="landlord">Indiana and Indianapolis Landlord Basics</h2>
 <ul>
  <li><strong>Register the rental.</strong> Residential rental units inside the City of Indianapolis must be registered with the city&rsquo;s Department of Business and Neighborhood Services and renewed every year. Rentals in Beech Grove, Lawrence, Southport and Speedway are exempt from the city registry, so check with those cities directly. Short-term rentals need their own annual permit.</li>
  <li><strong>Security deposits.</strong> Within 45 days after the lease ends and you get the unit back, return the deposit minus allowed deductions with an itemized written notice. If you don&rsquo;t, the tenant can recover the deposit plus attorney&rsquo;s fees (IC 32-31-3-12).</li>
  <li><strong>Your duties.</strong> Deliver a safe, clean, habitable unit and keep the electrical, plumbing, heating and other systems in good working order (IC 32-31-8-5).</li>
  <li><strong>Use a real lease and document everything.</strong> Have an Indiana attorney review your lease rather than downloading a generic template, and take dated photos at move-in and move-out. Procedural mistakes are the usual reason landlords lose otherwise winnable cases.</li>
  <li><strong>Budget for management if you&rsquo;re remote.</strong> Management typically costs a percentage of collected rent plus leasing fees. Put it in your model from the start, not as an afterthought when self-management stops working.</li>
 </ul>

 <h2 id="taxes">Taxes, Depreciation and 1031 Exchanges</h2>
 <p>Rent is taxable income, and the tax side can make or break a deal. The IRS generally depreciates residential rental buildings (not the land) over 27.5 years, which can offset rental income; but depreciation reduces your basis, so recapture at sale surprises many owners (IRS Publication 527). The line between a deductible repair and a capital improvement that has to be depreciated matters too.</p>
 <p>When you sell, a <a href="/services/1031-exchange/">1031 exchange</a> can defer capital gains if you reinvest in like-kind real property held for investment or business use. The deadlines are strict: identify replacement property within 45 days and close within 180 days (or your tax return due date, if earlier). Line up a qualified intermediary before you close the sale. These are CPA conversations to have before you buy or sell, not at filing time.</p>

 <h2 id="mistakes">Common Mistakes</h2>
 <ul>
  <li><strong>Buying by spreadsheet from out of state.</strong> Block-by-block variation is real. Have someone competent physically walk the property and the street.</li>
  <li><strong>Underestimating rehab.</strong> Older Indianapolis housing hides expensive surprises in mechanicals, plumbing stacks and foundations.</li>
  <li><strong>Modeling zero vacancy and zero capex.</strong> Both are guaranteed over any real holding period.</li>
  <li><strong>Chasing the highest yield on paper.</strong> The cheapest properties often carry the heaviest management burden.</li>
  <li><strong>Running without a cushion.</strong> A furnace, a roof or a stretch between tenants will come. Set aside several months of expenses per property before you buy, and keep refilling that account as rent comes in.</li>
  <li><strong>Skipping the inspection.</strong> Never sensible, least of all on an older rental.</li>
 </ul>

 <h2 id="start">How to Get Started</h2>
 <ol>
  <li><strong>Set your strategy and budget.</strong> Decide on buy-and-hold, multi-family, a house hack or a flip, and how hands-on you&rsquo;ll be.</li>
  <li><strong>Get pre-approved</strong> with a lender who does investor or multi-unit loans.</li>
  <li><strong>Pick target areas</strong> using the trade-offs above, then learn them street by street.</li>
  <li><strong>Underwrite conservatively</strong> with every expense line, at the rental tax rate, with vacancy and reserves.</li>
  <li><strong>Inspect, negotiate and close,</strong> then set up registration, the lease, insurance and management before the first tenant moves in.</li>
 </ol>
 <p>An investor-friendly agent thinks differently from a typical buyer&rsquo;s agent: they can read a property&rsquo;s income potential, spot red flags in a rental inspection, handle a tenant-occupied purchase and tell you which areas look good on paper but carry hidden risk. Your Realty Link works with investors at every level, from first rentals to portfolio sales, and we&rsquo;ll tell you when a deal doesn&rsquo;t work. When you&rsquo;re ready to buy, see our <a href="/services/investment-property/">Indianapolis investment property services</a> or <a href="/search/">search every active MIBOR listing</a>. Selling a tenant-occupied property? See <a href="/services/sell-rental-property/">selling a rental property</a>.</p>
""",
 faqs=[
  ("Is Indianapolis a good place to invest in real estate?",
   "It's frequently cited as one of the better Midwest rental markets because purchase prices sit well below many large metros while rents don't fall proportionally, the employment base is diverse and the suburbs have grown steadily. At 2026 interest rates cash flow is thinner than it was a few years ago, and results depend entirely on the specific property and block, so local due diligence matters more than the market's reputation."),
  ("How much money do I need to start investing in Indianapolis real estate?",
   "Investment loans typically require a larger down payment than owner-occupant loans, plus closing costs and cash reserves for repairs and vacancy. The cheapest entry is usually house hacking: if you live in one unit of a two- to four-unit home, FHA allows 3.5% down with a 580+ credit score and a conventional loan through Fannie Mae's automated underwriting allows 5% down."),
  ("Is now a good time to buy investment property in Indianapolis?",
   "There's no perfect time, but conditions in late 2026 favor patient buyers. Rental demand is solid, while the 30-year fixed rate averaged 7.28% on November 19, 2026 (Freddie Mac), which thins monthly cash flow for leveraged buyers. In Marion County, homes took a median 32 days to sell in October 2026 versus 22 a year earlier (MIBOR), which can mean more room to negotiate. Buy for cash flow and treat appreciation as a bonus."),
  ("What expenses should I include for an Indianapolis rental?",
   "At minimum: principal and interest, property taxes at the rental rate (Indiana caps rentals at 2% of assessed value versus 1% for a homestead), a landlord insurance policy, vacancy, maintenance and capital expenditures such as roofs and furnaces, property management if you won't self-manage, turnover costs and any HOA dues. Underestimating vacancy and capital expenditures is the most common modeling error."),
  ("Do I have to register a rental property in Indianapolis?",
   "Yes, if the rental is inside the City of Indianapolis. Owners or landlords of residential rental units must register with the Department of Business and Neighborhood Services and renew every year. Rentals in the excluded cities of Beech Grove, Lawrence, Southport and Speedway are exempt from the city registry, and short-term rentals need their own annual permit."),
  ("Can I defer taxes when I sell an Indianapolis investment property?",
   "A 1031 exchange can defer capital gains if you reinvest in like-kind real property held for investment or business use. You must identify replacement property within 45 days and close within 180 days, or by your tax return due date if that's earlier. Depreciation recapture also applies at sale. Talk to a CPA before you buy or sell."),
 ],
 sources=[
  ("MIBOR REALTOR Association, Marion County market data (October 2026)", "/market-updates/"),
  ("Freddie Mac Primary Mortgage Market Survey (Nov 19, 2026)", "https://www.freddiemac.com/pmms"),
  ("Indiana DLGF, property tax caps (Nov 2025)", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("City of Indianapolis, landlord registration", "https://www.indy.gov/activity/landlord-registration-program"),
  ("IC 32-31-3-12, security deposits", "https://codes.findlaw.com/in/title-32-property/in-code-sect-32-31-3-12/"),
  ("IC 32-31-8-5, landlord obligations", "https://codes.findlaw.com/in/title-32-property/in-code-sect-32-31-8-5/"),
  ("IRS Publication 527, residential rental property", "https://www.irs.gov/publications/p527"),
  ("IRS, like-kind exchanges: real estate tax tips", "https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips"),
 ],
 related=[
  ("/blog/house-hacking-in-indianapolis/", "House Hacking in Indianapolis"),
  ("/blog/multi-family-investing-indianapolis/", "Multi-Family Investing in Indianapolis"),
  ("/blog/indiana-property-tax-caps-explained/", "Indiana Property Tax Caps Explained"),
 ],
 cta=("Looking at Indianapolis Investment Property?",
      "Tell us your strategy and target returns. We&rsquo;ll show you what the numbers actually look like, including the deals we&rsquo;d pass on.",
      [("/schedule/", "Schedule an Investor Call &rarr;", "btn-white"), ("/services/investment-property/", "Investment Property Services", "btn-outline")]),
 resources=[
  ("/services/investment-property/", "Indianapolis Investment Properties"),
  ("/services/rental-property/", "Rental Property"),
  ("/services/multi-family/", "Multi-Family Homes"),
  ("/services/1031-exchange/", "1031 Exchange"),
 ],
)
