"""Moving from California to Indianapolis (Nov 2026). Joins the move-guide series (Chicago,
Cincinnati, Louisville; build_move_guides.py) with the same framing: dated federal/state data,
honest trade-offs, where to look by preference.

Every figure is dated and sourced (researched Nov 3 2026):
- BEA Regional Price Parities 2024 via FRED: all items Indy RPPALL26900 95.7, California CARPPALL
  110.720, Los Angeles RPPALL31080 113.566, San Diego RPPALL41740 111.887, Sacramento RPPALL40900
  106.670; housing Indy RPPSERVERENT26900 88.9, California CARPPSERVERENT 154.346, LA 170.433,
  San Diego 179.267, Sacramento 130.230.
- Census ACS 2025 1-year summary files (acsdt1y2025-*.dat, read directly): B25077 median value
  (CA 770,700 / Indy metro 304,600 / LA 925,900 / SD 927,700 / Sac 594,600); B25064 median gross
  rent (2,160 / 1,380 / 2,170 / 2,416 / 1,929); B25103 median real estate taxes (5,537 / 2,596 /
  6,159 / 6,270 / 4,724); B19013 median household income (102,159 / 83,815 / 100,145 / 110,941 /
  102,327). San Jose skipped (taxes top-coded).
- FTB 2026 California Tax Rate Schedules (PDF): 1%-12.3%; 9.3% from $75,197 single / $150,394 joint;
  1% from $0, 2% from $11,456, 4% from $27,157 to $42,861 (single). Behavioral Health Services Tax
  (formerly Mental Health Services Tax) on taxable income over $1,000,000 (FTB 2025 540-ES
  instructions). FTB Publication 1031 (2025): nonresidents taxed only on CA-source income incl.
  services performed in CA; part-year residents file 540NR. EDD: 2026 SDI 1.3%, no wage limit.
- CDTFA: statewide base sales tax 7.25%, district taxes 0.10%-2.00%. LAO: Prop 13 1% rate limit,
  taxable value +2% or inflation (lower) per year, reassessed at purchase price on sale.
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026): 2.95%; Hamilton 1.10%, Marion 2.02%;
  county determined on Jan. 1. DLGF circuit-breaker fact sheet (1% homestead cap).
- EIA Electric Power Monthly Table 5.6.A: residential Aug 2026 California 29.75c, Indiana 17.02c,
  U.S. 18.16c.
- NWS 1991-2020 normals (Jan 28.5F, ~25.5 in snow), Walk Score 31, Census commute 25.1 min (same as
  the living-in-Indianapolis post). ind.com/flights (Nov 3 2026): LAX, SFO nonstop; SAN, BUR seasonal.
- MIBOR Sept 2026 median $320,000 (our October market update). Freddie Mac 7.24% (Oct 29 2026).
  Payment and ratio math is ours (principal + interest, 10% down, 30 years).
No crime/safety, no political framing.
"""

_MARKET = "/blog/indianapolis-market-update-october-2026/"
_FRED = "https://fred.stlouisfed.org/series/"

POST = dict(
 slug="moving-from-california-to-indianapolis",
 title="Moving from California to Indianapolis: 2026 Guide",
 headline="Moving from California to Indianapolis: Costs, Taxes & Where to Live",
 crumb="Moving from California to Indianapolis",
 h1_html="Moving from California to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em>",
 desc=("Moving from California to Indianapolis? Compare home prices, rent, taxes and utilities with real 2026 "
       "numbers, plus the trade-offs and where to look."),
 date="2026-11-03", month="November 2026",
 category="Relocation", eyebrow="RELOCATION",
 focus="moving from california to indianapolis",
 hero_sub="How home prices, rent, taxes and everyday costs really compare, the trade-offs Californians notice first, and where to look in Central Indiana.",
 badges=["Relocation", "California to Indy", "Updated for 2026"],
 read_min=8,
 card_title="Moving from California to Indy",
 card_sub="Home prices, rent, taxes and the trade-offs, with real 2026 numbers.",
 qa_heading="California vs. Indianapolis at a Glance",
 qa_lead=("<strong>Is Indianapolis cheaper than California?</strong> Yes, by a wide margin, mostly because of housing. "
          "Everyday prices run about 14% lower in the Indianapolis metro than in California overall (BEA, 2024), the typical "
          "home is valued at about $305,000 versus $771,000 statewide, and median rent is about $1,380 versus $2,160 (Census, 2025). "
          "The trade-offs: real winters, humid summers, flat terrain and a car-dependent metro."),
 qa_facts=[
  ("Price level (U.S. = 100)", "Indy metro 95.7 &middot; California 110.7 (2024)"),
  ("Median home value", "$304,600 Indy metro &middot; $770,700 California (2025)"),
  ("Median gross rent", "$1,380 Indy metro &middot; $2,160 California (2025)"),
  ("Median property tax bill", "$2,596 Indy metro &middot; $5,537 California (2025)"),
  ("Income tax (2026)", "Indiana 2.95% + county &middot; California 1% to 12.3%"),
  ("Electricity (Aug 2026)", "17.02&cent;/kWh Indiana &middot; 29.75&cent; California"),
 ],
 toc=[("at-a-glance", "Indianapolis vs. California at a Glance"), ("cost-of-living", "Cost of Living"),
      ("home-prices", "Home Prices and Payments"), ("taxes", "Taxes"), ("remote-work", "Keeping a California Job"),
      ("trade-offs", "The Trade-Offs"), ("where-to-live", "Where to Look"), ("buying-from-california", "Buying Before You Move")],
 body=f"""
 <p>California to Indianapolis is one of the bigger lifestyle changes we help people make: a different climate, a different time zone and a very different housing market. Most people we talk to are moving for space, a lower monthly payment, family or a job, and many keep a California salary and work remotely. Here&rsquo;s how the costs actually compare, using federal and state data, plus the honest downsides and where to start looking.</p>

 <h2 id="at-a-glance">Indianapolis vs. California at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th></th><th>Indy metro</th><th>California</th><th>Los Angeles</th><th>San Diego</th><th>Sacramento</th></tr></thead>
 <tbody>
 <tr><td>Overall price level (BEA, 2024; U.S. = 100)</td><td>95.7</td><td>110.7</td><td>113.6</td><td>111.9</td><td>106.7</td></tr>
 <tr><td>Housing price level (BEA, 2024)</td><td>88.9</td><td>154.3</td><td>170.4</td><td>179.3</td><td>130.2</td></tr>
 <tr><td>Median home value (Census ACS, 2025)</td><td>$304,600</td><td>$770,700</td><td>$925,900</td><td>$927,700</td><td>$594,600</td></tr>
 <tr><td>Median gross rent (ACS, 2025)</td><td>$1,380</td><td>$2,160</td><td>$2,170</td><td>$2,416</td><td>$1,929</td></tr>
 <tr><td>Median homeowner property tax bill (ACS, 2025)</td><td>$2,596</td><td>$5,537</td><td>$6,159</td><td>$6,270</td><td>$4,724</td></tr>
 <tr><td>Median household income (ACS, 2025)</td><td>$83,815</td><td>$102,159</td><td>$100,145</td><td>$110,941</td><td>$102,327</td></tr>
 </tbody>
 </table>
 </div>
 <p style="font-size:.85rem;color:var(--gray);">Metro figures are for each metropolitan area as the Census Bureau and BEA define it. Home values are what owners estimate their homes are worth, not recent sale prices.</p>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>The Bureau of Economic Analysis measures how expensive each place is compared with the national average. In 2024 the Indianapolis metro scored <strong>95.7</strong> and California <strong>110.7</strong>, so everyday prices run about 14% lower here. Housing is where the gap gets dramatic: the BEA&rsquo;s housing index is 88.9 for Indianapolis versus 154.3 for California, 170.4 for Los Angeles and 179.3 for San Diego.</p>
 <p>Incomes are lower too, which is the honest other half. The median household income is $83,815 in the Indianapolis metro and $102,159 in California (Census, 2025). But home values fall much further than incomes: the typical home is worth about 3.6 times the median household income here, compared with about 7.5 times in California (our math from the same Census tables). If you keep a California-level salary, that difference goes a very long way. Utilities follow the same pattern. Indiana&rsquo;s average residential electricity price was 17.02&cent; per kWh in August 2026, against 29.75&cent; in California (EIA). For a fuller breakdown, see our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis</a> guide.</p>

 <h2 id="home-prices">Home Prices and What Your Payment Buys</h2>
 <p>Across the MIBOR region, the median home <em>sold</em> for <strong>$320,000</strong> in September 2026, according to our <a href="{_MARKET}">market update</a>. For a like-for-like comparison with California, the Census Bureau&rsquo;s 2025 survey puts the median home value at $304,600 in the Indianapolis metro and $770,700 statewide.</p>
 <p>Here&rsquo;s what that means for a monthly payment. At the 7.24% average 30-year rate Freddie Mac reported on October 29, 2026, with 10% down, principal and interest come to about <strong>$1,868 a month</strong> on a $304,600 home, versus about $4,727 on a $770,700 home (our math, before taxes and insurance). That difference is why many of the Californians we work with buy a newer or larger home here, or keep part of their equity in the bank. To see what your budget buys, use our <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house can I afford</a> guide, then browse our <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> and <a href="/best/most-affordable-indianapolis-suburbs/">most affordable suburbs</a> rankings or <a href="/search/">search live listings</a>.</p>

 <h2 id="taxes">Taxes: Income, Property and Sales</h2>
 <p><strong>Income tax.</strong> California&rsquo;s 2026 rates run from 1% to 12.3%, plus an extra 1% Behavioral Health Services Tax on taxable income over $1 million. The 9.3% rate starts at $75,197 of taxable income for single filers and $150,394 for joint filers (FTB 2026 tax rate schedules). California workers also pay 1.3% of their wages for State Disability Insurance in 2026, with no wage limit (EDD). Indiana has a flat 2.95% state rate plus a county income tax, such as 1.10% in Hamilton County (Carmel, Fishers, Westfield) and 2.02% in Marion County (Indianapolis), or about 4.05% to 4.97% combined. Indiana sets your county rate by where you live or work on January 1, which matters in your move year (Indiana DOR).</p>
 <p>How much you save depends on your income. California&rsquo;s rates on the first $40,000 or so of a single filer&rsquo;s taxable income are only 1% to 4%, so many middle-income households see a smaller difference than they expect. The gap grows quickly once income reaches the 9.3% bracket and above. Deductions and credits differ between the states, so run your own numbers with a tax professional.</p>
 <p><strong>Property tax.</strong> Both states cap the tax rate on a home at about 1%. California&rsquo;s Proposition 13 limits the rate to 1% plus voter-approved debt and limits increases in taxable value to 2% a year, but a home is reassessed at its purchase price when it sells (Legislative Analyst&rsquo;s Office). So the low bill on a California home you&rsquo;ve owned for years isn&rsquo;t the right comparison; the price of your next home is. Indiana caps the tax on your primary home at 1% of its assessed value once you file the homestead deduction (<a href="/blog/indiana-property-tax-caps-explained/">how the caps work</a>). The median homeowner bill is $2,596 in the Indianapolis metro and $5,537 in California (Census, 2025), largely because homes here cost less. See <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a> and how to file the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a>.</p>
 <p><strong>Sales tax.</strong> California&rsquo;s statewide base rate is 7.25%, and local district taxes add 0.10% to 2.00% in many areas (CDTFA). Indiana&rsquo;s sales tax is 7% statewide.</p>

 <h2 id="remote-work">Keeping a California Job</h2>
 <p>Plenty of our California clients keep working for a California employer after they move. Two things to plan for. First, the clock: Indianapolis is on Eastern time, three hours ahead of California, so a 9 a.m. Pacific meeting is noon here. Second, taxes: the California Franchise Tax Board says nonresidents are taxed only on income from California sources, including pay for work performed in California. In the year you move, you&rsquo;ll generally file as a part-year resident (California Form 540NR) for the months you lived there. Residency is a question of facts, so have a tax professional review your situation before and after the move.</p>

 <h2 id="trade-offs">The Trade-Offs Californians Notice First</h2>
 <ul>
 <li><strong>Winter.</strong> January averages 28.5&deg;F, and the area gets about 25.5 inches of snow a year, mostly December through February (National Weather Service, 1991-2020 normals).</li>
 <li><strong>Humid summers.</strong> July highs average about 85&deg;F, and humidity makes it feel warmer.</li>
 <li><strong>No ocean or mountains.</strong> Central Indiana is flat. Locals use reservoirs like Geist and Morse, trails like the Monon and state parks within an hour or so.</li>
 <li><strong>Driving.</strong> Walk Score rates Indianapolis 31 out of 100, so most households drive. The good news is the average commute is 25.1 minutes, below the national 27.4 (Census, 2025).</li>
 <li><strong>Getting back to California.</strong> Indianapolis International has nonstop flights to Los Angeles and San Francisco, plus seasonal nonstops to San Diego and Burbank (airport flight list, November 2026).</li>
 </ul>
 <p>For the full picture, read our honest <a href="/blog/living-in-indianapolis-pros-and-cons/">pros and cons of living in Indianapolis</a>.</p>

 <h2 id="where-to-live">Where to Look, Based on What You Want</h2>
 <ul>
 <li><strong>Walkable, urban living:</strong> close-in neighborhoods like <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>, <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a> and <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>.</li>
 <li><strong>Newer homes and highly rated schools:</strong> Hamilton County suburbs like <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>, <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a> and <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a>, which also have the metro&rsquo;s lowest county income tax.</li>
 <li><strong>Value with a short commute:</strong> <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a> and the south side, including <a href="/neighborhoods/perry-township-indianapolis/">Perry Township</a>.</li>
 <li><strong>More room and bigger lots:</strong> Hendricks County towns like <a href="/cities/hendricks-county/brownsburg-indiana-real-estate/">Brownsburg</a> and <a href="/cities/hendricks-county/danville-indiana-real-estate/">Danville</a>.</li>
 </ul>
 <p>Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro. Moving from closer to home? See our <a href="/blog/moving-from-chicago-to-indianapolis/">Chicago</a>, <a href="/blog/moving-from-cincinnati-to-indianapolis/">Cincinnati</a> and <a href="/blog/moving-from-louisville-to-indianapolis/">Louisville</a> guides.</p>

 <h2 id="buying-from-california">Buying Before You Move</h2>
 <p>Most of our California buyers do much of their search from home. We run live video tours, give a straight read on condition and neighborhood, and line up inspections and closing so you can sign remotely where your lender and title company allow it. Our guide to <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">buying with virtual home tours</a> covers how that works. Before you tour, you&rsquo;ll sign a written buyer agreement that spells out our services and how we&rsquo;re paid, so the terms are clear from the start. And after you close, file your homestead deduction, switch your driver&rsquo;s license and registration to the Indiana BMV, and set up service with our <a href="/utilities/">utilities guide</a>.</p>
 <p>Ready to compare areas? <a href="/schedule/">Book a call with our team</a>, tell us what you have in California and what you want here, and we&rsquo;ll map out the parts of the metro that fit.</p>
""",
 faqs=[
  ("Is Indianapolis cheaper than California?",
   "Yes. The Bureau of Economic Analysis put 2024 price levels at 95.7 for the Indianapolis metro and 110.7 for California, so everyday prices run about 14% lower. Housing is the biggest difference: the median home value is $304,600 in the Indianapolis metro versus $770,700 in California, and median rent is $1,380 versus $2,160 (Census ACS, 2025)."),
  ("How much cheaper are houses in Indianapolis than in California?",
   "The typical home is valued at about 60% less. The Census Bureau's 2025 survey puts the median home value at $304,600 in the Indianapolis metro and $770,700 in California, and the median home sold for $320,000 across the MIBOR region in September 2026. At a 7.24% rate with 10% down, principal and interest are about $1,868 a month on a $304,600 home versus about $4,727 on a $770,700 home."),
  ("Will I pay less income tax in Indiana than in California?",
   "Usually, though the savings depend on your income. Indiana charges a flat 2.95% plus a county tax, about 4.05% to 4.97% combined in Hamilton and Marion counties. California's 2026 rates run from 1% to 12.3%, plus 1% on taxable income over $1 million, and workers also pay 1.3% for State Disability Insurance. Middle incomes see a smaller gap than high incomes. Check your numbers with a tax professional."),
  ("Do I still owe California tax if I keep my California job and work remotely from Indiana?",
   "Generally, California taxes nonresidents only on California-source income, which includes pay for work performed in California, according to the Franchise Tax Board. In the year you move, you typically file a part-year resident return. Residency depends on your facts, so get advice from a tax professional."),
  ("What is the weather like in Indianapolis compared with California?",
   "Colder in winter and more humid in summer. January averages 28.5 degrees with about 25.5 inches of snow a year, and July highs average about 85 degrees, based on National Weather Service 1991-2020 normals."),
  ("Are there direct flights from Indianapolis to California?",
   "Yes. As of November 2026, Indianapolis International Airport lists nonstop flights to Los Angeles and San Francisco, plus seasonal nonstops to San Diego and Burbank. Schedules change, so check the airport's flight list for current routes."),
 ],
 sources=[
  ("BEA Regional Price Parities (2024): Indianapolis", _FRED + "RPPALL26900"),
  ("California", _FRED + "CARPPALL"),
  ("Los Angeles", _FRED + "RPPALL31080"),
  ("San Diego", _FRED + "RPPALL41740"),
  ("Sacramento", _FRED + "RPPALL40900"),
  ("BEA housing price levels: Indianapolis", _FRED + "RPPSERVERENT26900"),
  ("California housing", _FRED + "CARPPSERVERENT"),
  ("Census ACS 2025 median home value", "https://data.census.gov/table/ACSDT1Y2025.B25077"),
  ("median gross rent", "https://data.census.gov/table/ACSDT1Y2025.B25064"),
  ("median real estate taxes", "https://data.census.gov/table/ACSDT1Y2025.B25103"),
  ("median household income", "https://data.census.gov/table/ACSDT1Y2025.B19013"),
  ("California FTB 2026 tax rate schedules", "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf"),
  ("FTB Behavioral Health Services Tax", "https://www.ftb.ca.gov/forms/2025/2025-540-es-instructions.html"),
  ("FTB Publication 1031, residency", "https://www.ftb.ca.gov/forms/2025/2025-1031-publication.pdf"),
  ("California EDD, 2026 SDI rate", "https://edd.ca.gov/en/payroll_taxes/rates_and_withholding/"),
  ("CDTFA sales tax rates", "https://www.cdtfa.ca.gov/taxes-and-fees/sales-use-tax-rates.htm"),
  ("Legislative Analyst&rsquo;s Office, Proposition 13", "https://lao.ca.gov/Publications/Report/3497"),
  ("Indiana DOR 2026 county tax rates", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("EIA electricity prices (Aug 2026)", "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a"),
  ("Freddie Mac 30-year rate (Oct 29, 2026)", "https://fred.stlouisfed.org/series/MORTGAGE30US"),
  ("National Weather Service climate normals", "https://www.weather.gov/media/ind/climate/INDnormalschange.pdf"),
  ("Walk Score", "https://www.walkscore.com/IN/Indianapolis"),
  ("Indianapolis International Airport flights", "https://www.ind.com/flights"),
  ("home prices: MIBOR REALTOR&reg; Association via our market update", _MARKET),
  ("General information, not tax advice", ""),
 ],
 related=[
  ("/blog/living-in-indianapolis-pros-and-cons/", "Living in Indianapolis: Pros and Cons"),
  ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
  ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
 ],
 cta=("Moving From California?",
      "Tell us where you&rsquo;re coming from, your budget and what matters most, and our team will map out the parts of Central Indiana that fit, then help you buy confidently from a distance.",
      [("/services/relocation-buyers/", "Explore Relocation Services →", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[
  ("/services/relocation-buyers/", "Relocation Buyers"),
  ("/blog/relocating-to-indianapolis-virtual-home-tours/", "Buying With Virtual Home Tours"),
  ("/blog/how-much-house-can-i-afford-indianapolis/", "How Much House Can I Afford?"),
  ("/utilities/", "Utilities by City and Town"),
 ],
 link_from=[
  ("blog/moving-to-indianapolis-relocation-guide/index.html",
   '<strong>Coming from the West Coast?</strong> Our <a href="/blog/moving-from-california-to-indianapolis/">moving from California to Indianapolis</a> guide compares home prices, rent, taxes and the trade-offs, with 2026 numbers.'),
  ("blog/living-in-indianapolis-pros-and-cons/index.html",
   'Weighing a move from California? See how costs and taxes compare in our <a href="/blog/moving-from-california-to-indianapolis/">California to Indianapolis guide</a>.'),
 ],
 about={"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
