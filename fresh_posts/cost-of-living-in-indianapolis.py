"""Cost of Living in Indianapolis (Nov 2026). The money breakdown that sits alongside
/blog/living-in-indianapolis-pros-and-cons/ (lifestyle + honest downsides).

Every figure is dated and sourced (researched Nov 2 2026):
- BEA Regional Price Parities 2024 via FRED (RPPALL26900 95.696, RPPSERVERENT26900 88.917,
  RPPGOOD26900 94.318, RPPSERVEOTH26900 99.141; 2022 all-items 93.805). No utilities RPP is on FRED, so
  utilities use EIA instead.
- Census ACS 2025 1-year summary files (released Oct 29 2026), read directly:
  B25064 median gross rent (US 1,557 / city 1,333 / metro 1,380 / Marion 1,334 / Hamilton 1,740 /
  Boone 1,680 / Hendricks 1,654 / Hancock 1,446 / Johnson 1,447); B19013 median household income
  (US 84,780 / city 69,787 / metro 83,815); B25077 owner-estimated median value (US 371,100 / metro
  304,600 / Marion 250,600 / Hamilton 483,600 / Boone 416,500 / Hendricks 344,900 / Hancock 328,100 /
  Johnson 323,100); B25103 median real estate taxes paid (US 3,344 / metro 2,596 / Marion 2,389 /
  Hamilton 4,356 / Boone 3,442 / Hendricks 2,747 / Hancock 2,479 / Johnson 2,679); B25040 heating fuel
  (metro: utility gas 56%, electricity 38%).
- MIBOR September 2026 (our October 2026 market update): median $320,000, +1.3% y/y, 98.1% of list, 27 days.
- Freddie Mac PMMS 30-year fixed 7.24% (Oct 29 2026, via FRED MORTGAGE30US). Payment math is ours.
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026): 2.95% state; county rates Marion 2.02%,
  Hamilton 1.10%, Boone 1.71% (changed since Jan 1), Hendricks 1.70%, Hancock 1.94%, Johnson 1.40%,
  Morgan 2.72%. 2.90% in 2027 per Bloomberg Tax. Sales tax 7% (DOR); grocery food exempt (SIB #29).
- DLGF circuit-breaker fact sheet (Nov 2025); new homestead credit (lesser of 10% or $300) from AIC.
- EIA Electric Power Monthly Table 5.6.A: Indiana residential 17.02 c/kWh Aug 2026 (16.21 Aug 2025;
  U.S. 18.16). EIA Table 5A (2024): Indiana 901 kWh/month, 14.77 c, $133.06 average bill (U.S. $142.26).
- MIT Living Wage Calculator, Indianapolis-Carmel-Greenwood, IN, updated Feb 15 2026.
No crime/safety content. Price tiers by suburb follow the site's standard ranges.
"""

_BUDGET = [
    ("Housing", "$1,108", "$1,461"),
    ("Food", "$340", "$994"),
    ("Child care", "$0", "$2,960"),
    ("Transportation", "$773", "$1,297"),
    ("Medical care", "$290", "$858"),
    ("Internet &amp; mobile", "$122", "$167"),
    ("Civic and entertainment", "$279", "$707"),
    ("Other necessities", "$379", "$821"),
]
_BUDGET_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in _BUDGET)

_COUNTIES = [
    ("Marion (Indianapolis)", "/counties/marion-county-indiana-real-estate/", "2.02%", "$1,334", "$250,600", "$2,389"),
    ("Hamilton (Carmel, Fishers, Westfield)", "/counties/hamilton-county-indiana-real-estate/", "1.10%", "$1,740", "$483,600", "$4,356"),
    ("Boone (Zionsville, Whitestown)", "/counties/boone-county-indiana-real-estate/", "1.71%", "$1,680", "$416,500", "$3,442"),
    ("Hendricks (Avon, Brownsburg, Plainfield)", "/counties/hendricks-county-indiana-real-estate/", "1.70%", "$1,654", "$344,900", "$2,747"),
    ("Hancock (Greenfield, McCordsville)", "/counties/hancock-county-indiana-real-estate/", "1.94%", "$1,446", "$328,100", "$2,479"),
    ("Johnson (Greenwood, Franklin)", "/counties/johnson-county-indiana-real-estate/", "1.40%", "$1,447", "$323,100", "$2,679"),
]
_COUNTY_ROWS = "\n".join(f' <tr><td><a href="{u}">{n}</a></td><td>{t}</td><td>{r}</td><td>{v}</td><td>{p}</td></tr>'
                         for n, u, t, r, v, p in _COUNTIES)

_MARKET = "/blog/indianapolis-market-update-october-2026/"

POST = dict(
 slug="cost-of-living-in-indianapolis",
 title="Cost of Living in Indianapolis: 2026 Breakdown",
 headline="Cost of Living in Indianapolis: What It Really Costs in 2026",
 h1_html="Cost of Living in Indianapolis: <em>What It Really Costs in 2026</em>",
 desc=("What it really costs to live in Indianapolis in 2026: rent, home prices, taxes, utilities and "
       "the salary you need, with city vs. suburb numbers."),
 date="2026-11-02", month="November 2026", category="Relocation", eyebrow="RELOCATION",
 focus="cost of living in indianapolis",
 hero_sub="Rent, home prices, taxes, utilities and the salary you need, with real, dated numbers for the city and the suburbs.",
 badges=["Relocation", "Updated for 2026", "Indianapolis"], read_min=8,
 card_title="Cost of Living in Indianapolis", card_sub="Rent, home prices, taxes, utilities and the salary you need in 2026.",
 qa_heading="Indianapolis Cost of Living at a Glance",
 qa_lead=("<strong>Is Indianapolis expensive to live in?</strong> Not by big-metro standards. Prices run about 4.3% below the "
          "U.S. average, and housing about 11% below (BEA, 2024). The median rent across the metro is $1,380 a month, the "
          "median home sold for $320,000 in September 2026, and MIT estimates a single adult needs about $47,700 a year "
          "before taxes to cover the basics."),
 qa_facts=[("Overall prices", "About 4.3% below U.S. average (2024)"),
           ("Median rent", "$1,380 metro &middot; $1,333 city (2025)"),
           ("Median home sale", "$320,000 (Sept 2026)"),
           ("Income tax", "2.95% state + 2.02% Marion County (2026)"),
           ("Electricity", "17.02&cent;/kWh in Indiana (Aug 2026; U.S. 18.16&cent;)"),
           ("Living wage, 1 adult", "$47,730 a year before taxes (MIT, 2026)")],
 toc=[("big-picture", "The Big Picture"), ("housing", "Housing: Rent and Home Prices"), ("taxes", "Taxes"),
      ("utilities", "Utilities"), ("everyday", "Food, Transportation and Child Care"), ("salary", "What Salary Do You Need?"),
      ("city-vs-suburbs", "City vs. Suburbs"), ("our-take", "Our Take")],
 body=f"""
 <p>When people ask us what it costs to live in Indianapolis, they&rsquo;re usually comparing it with somewhere specific: the city they live in now, or another metro on their shortlist. So here&rsquo;s the money side, line by line: rent and home prices, taxes, utilities, everyday costs and the income you&rsquo;d need, with the source and date for every number. For the lifestyle side (weather, commute, jobs and the honest downsides), see our companion piece on <a href="/blog/living-in-indianapolis-pros-and-cons/">the pros and cons of living in Indianapolis</a>.</p>

 <h2 id="big-picture">The Big Picture</h2>
 <p>The Bureau of Economic Analysis compares prices in every metro with the national average (U.S. = 100). In 2024, the latest year available, the Indianapolis metro scored <strong>95.7</strong>, so prices overall run about 4.3% below average. Most of that comes from housing:</p>
 <table class="data-table">
 <thead><tr><th>Category (BEA, 2024)</th><th>Indianapolis metro</th><th>vs. U.S. average</th></tr></thead>
 <tbody>
 <tr><td>All items</td><td>95.7</td><td>About 4% lower</td></tr>
 <tr><td>Housing (rents)</td><td>88.9</td><td>About 11% lower</td></tr>
 <tr><td>Goods</td><td>94.3</td><td>About 6% lower</td></tr>
 <tr><td>Other services</td><td>99.1</td><td>About the same</td></tr>
 </tbody>
 </table>
 <p>In plain terms, you save the most on rent and housing, a little on things you buy, and close to nothing on services. The gap is also narrowing: the all-items score was 93.8 in 2022. (BEA&rsquo;s metro still uses the older &ldquo;Indianapolis-Carmel-Anderson&rdquo; boundary, which includes Madison County.)</p>

 <h2 id="housing">Housing: Rent and Home Prices</h2>
 <h3>Renting</h3>
 <p>The Census Bureau&rsquo;s 2025 American Community Survey puts the <strong>median gross rent</strong> (rent plus any utilities the tenant pays) at <strong>$1,333 a month in Indianapolis</strong> and <strong>$1,380 across the metro</strong>, compared with $1,557 nationally. Newer apartments and rental houses in the north suburbs cost more: the Hamilton County median is $1,740.</p>
 <h3>Buying</h3>
 <p>Across the MIBOR region, the median single-family home sold for <strong>$320,000 in September 2026</strong>, up 1.3% from a year earlier, at 98.1% of list price after a median 27 days on the market (MIBOR, via our <a href="{_MARKET}">market update</a>). By the Census Bureau&rsquo;s measure of owner-estimated values, the typical metro home is worth $304,600, against $371,100 nationally.</p>
 <p>What does that look like monthly? As an illustration: put 10% down on a $320,000 home and borrow $288,000 at <strong>7.24%</strong> (Freddie Mac&rsquo;s average 30-year fixed rate for October 29, 2026), and principal and interest come to about <strong>$1,963 a month</strong>. Add property tax (the metro&rsquo;s median homeowner bill was $2,596 a year in 2025, or about $216 a month), homeowners insurance and, with less than 20% down, mortgage insurance. Your own numbers depend on price, down payment, credit and rate, so try our <a href="/services/mortgages/">mortgage calculator</a>, and see our <a href="/blog/rent-vs-buy-in-indianapolis-2026-comparison/">rent vs. buy comparison</a> if you&rsquo;re weighing the two. First-time buyers should also look at <a href="/blog/down-payment-assistance-programs-in-indiana-2026/">Indiana down payment assistance</a>.</p>

 <h2 id="taxes">Taxes</h2>
 <p><strong>Income tax.</strong> Indiana&rsquo;s state income tax is a <strong>flat 2.95%</strong> for 2026 and is scheduled to drop to 2.90% in 2027. Every county adds its own local income tax, set by where you live on January 1. Marion County&rsquo;s is 2.02%, so an Indianapolis resident pays about 4.97% combined (simple sum), compared with 4.05% in Hamilton County and 4.35% in Johnson County (Indiana Department of Revenue, rates effective October 1, 2026).</p>
 <p><strong>Sales tax.</strong> The rate is <strong>7%</strong> across the whole state, with no county or city sales tax on top (some counties add a separate tax on restaurant meals). Most grocery food is exempt; candy, soft drinks and prepared food are taxed.</p>
 <p><strong>Property tax.</strong> Indiana caps property tax bills at <strong>1% of assessed value</strong> for a primary residence (2% for rentals and other residential property, 3% for commercial), but only if you file for the homestead deduction. That&rsquo;s why property taxes here are modest by national standards: the median homeowner in the metro paid <strong>$2,596</strong> in 2025, compared with $3,344 nationally (Census). Starting with 2026 bills, homesteads also get a new credit of 10% of the bill or $300, whichever is less. Our guides to <a href="/blog/indiana-property-tax-caps-explained/">Indiana&rsquo;s property tax caps</a> and the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a> explain how to file.</p>

 <h2 id="utilities">Utilities</h2>
 <p>Electricity in Indiana averaged <strong>17.02&cent; per kilowatt-hour</strong> for homes in August 2026, below the U.S. average of 18.16&cent; but up about 5% from 16.21&cent; a year earlier (U.S. Energy Information Administration). In 2024, the average Indiana household used 901 kWh a month and paid an average electric bill of <strong>$133.06</strong>, compared with $142.26 nationally. At August 2026&rsquo;s price, that same usage would cost about $153 (our math).</p>
 <p>Heating is the other big line item. A little over half of homes in the metro heat with natural gas and about four in ten with electricity (Census, 2025), so expect your highest bills from December through February. Water, sewer and trash depend on the town. Our <a href="/utilities/">utilities guide</a> lists the providers for every city and town we cover.</p>

 <h2 id="everyday">Food, Transportation and Child Care</h2>
 <p>MIT&rsquo;s Living Wage Calculator builds a bare-bones budget for the Indianapolis-Carmel-Greenwood metro from federal data (housing is based on HUD fair market rents). Here&rsquo;s its monthly version for two household types:</p>
 <table class="data-table">
 <thead><tr><th>Monthly basic needs</th><th>1 adult</th><th>2 working adults, 2 children</th></tr></thead>
 <tbody>
{_BUDGET_ROWS}
 <tr><td><strong>Total after taxes</strong></td><td><strong>$3,292</strong></td><td><strong>$9,264</strong></td></tr>
 </tbody>
 </table>
 <p style="font-size:.85rem;color:var(--gray);">Source: MIT Living Wage Calculator, Indianapolis-Carmel-Greenwood, IN (updated February 15, 2026). Annual figures divided by 12 and rounded, so rows may not add exactly to the total. These are minimum needs, not a comfortable budget: they leave out savings, eating out and buying a home.</p>
 <p>Two things stand out. First, <strong>child care</strong> is the largest single cost for a family with two young kids, about $2,960 a month, more than housing. Second, <strong>transportation</strong> runs high because most households here need a car; the metro has limited transit, which we cover in the <a href="/blog/living-in-indianapolis-pros-and-cons/">pros and cons</a>.</p>

 <h2 id="salary">What Salary Do You Need?</h2>
 <p>According to MIT (2026), a <strong>single adult with no children needs about $47,730 a year</strong> before taxes ($22.95 an hour) to cover the basics in the metro. One adult with one child needs about $92,617, and a household with two working adults and two children needs about <strong>$130,645 combined</strong> ($31.41 an hour each), largely because of child care.</p>
 <p>For context, the median household income is <strong>$69,787 in Indianapolis</strong> and <strong>$83,815 across the metro</strong>, close to the U.S. median of $84,780 (Census, 2025). Because prices here run below average, that income goes further than it would in most large metros.</p>
 <p>If buying is the goal, here&rsquo;s a rough benchmark: many lenders like your housing payment to stay around 28% of gross income. The $320,000 example above (about $2,180 a month for principal, interest and property tax) works out to roughly <strong>$93,000 a year</strong> in household income before insurance is added. That&rsquo;s our estimate, not a lending rule; a lender will look at your debts, credit and down payment. <a href="/schedule/">Talk with our team</a> and we&rsquo;ll connect you with local lenders for a real pre-approval.</p>

 <h2 id="city-vs-suburbs">City vs. Suburbs</h2>
 <p>Where you live inside the metro changes the math more than most people expect. Indianapolis (Marion County) has the lowest rents, home values and property tax bills of the core counties, but the highest local income tax. The north suburbs flip that around:</p>
 <table class="data-table">
 <thead><tr><th>County</th><th>Local income tax (2026)</th><th>Median rent (2025)</th><th>Median home value (2025)</th><th>Median property tax (2025)</th></tr></thead>
 <tbody>
{_COUNTY_ROWS}
 </tbody>
 </table>
 <p style="font-size:.85rem;color:var(--gray);">Sources: Indiana Department of Revenue (rates effective October 1, 2026); Census ACS 2025 1-year (median gross rent, owner-estimated home value, median real estate taxes paid by homeowners).</p>
 <p>On $100,000 of income, the local tax difference between Marion County (2.02%) and Hamilton County (1.10%) is roughly $900 a year before exemptions, while the gap in rent or purchase price runs the other way. Some outlying counties have higher local rates too, such as Morgan County at 2.72%, so check the county before you fall for a house.</p>
 <p>By town, homes in <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a> and Zionsville typically run from the $400s to $1M+, Fishers, Westfield and Noblesville from the $300s to $600s, and <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a>, <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a> and Brownsburg from the $250s to $450s, while Indianapolis itself spans the $150s to $500s and up. Our <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> and <a href="/compare/">suburb comparisons</a> break the trade-offs down town by town.</p>

 <h2 id="our-take">Our Take</h2>
 <p>Indianapolis is still one of the more affordable large metros in the country, and the savings are real where they matter most: housing, property taxes and electricity. They&rsquo;re smaller on everyday services, the gap has narrowed since 2022, and a car and child care can eat into them quickly. The best way to make the numbers work is to choose the right part of the metro for your budget, commute and taxes. If you&rsquo;re planning a move, <a href="/schedule/">book a free call with our team</a> to talk through areas and price ranges, or <a href="/search/">start browsing homes</a>.</p>
 """,
 faqs=[
  ("Is Indianapolis expensive to live in?",
   "No, not compared with most large U.S. metros. The Bureau of Economic Analysis puts Indianapolis-area prices about 4.3% below the national average in 2024, with housing about 11% below. The median rent across the metro was $1,380 a month in 2025, and the median home sale price in the MIBOR region was $320,000 in September 2026."),
  ("What salary do you need to live in Indianapolis?",
   "MIT's Living Wage Calculator (updated February 2026) estimates a single adult needs about $47,730 a year before taxes to cover basic needs in the Indianapolis metro, and a family with two working adults and two children about $130,645 combined. To buy a $320,000 home with 10% down at October 2026 rates, we estimate a household income of roughly $93,000 or more, before insurance."),
  ("What is the average rent in Indianapolis?",
   "The median gross rent, which includes utilities paid by the tenant, was $1,333 a month in Indianapolis and $1,380 across the metro in 2025, compared with $1,557 nationally (Census American Community Survey). Suburban rents run higher, such as a $1,740 median in Hamilton County."),
  ("How much are utilities in Indianapolis?",
   "Indiana's average residential electricity price was 17.02 cents per kilowatt-hour in August 2026, below the U.S. average of 18.16 cents. The average Indiana household used 901 kWh a month in 2024 and paid an average electric bill of $133.06. Most homes heat with natural gas, so winter gas bills are the other major utility cost."),
  ("Are property taxes high in Indianapolis?",
   "No. Indiana caps property taxes on a primary residence at 1% of assessed value once you file for the homestead deduction. The median homeowner in the Indianapolis metro paid $2,596 in property tax in 2025, compared with $3,344 nationally, and Marion County's median was $2,389."),
  ("Is it cheaper to live in Indianapolis or the suburbs?",
   "It depends on which costs matter most to you. Indianapolis has lower rents, home prices and property tax bills than suburbs like Carmel or Fishers, but Marion County's 2.02% local income tax is higher than Hamilton County's 1.10% or Johnson County's 1.40%. For most buyers, the price of the home matters more than the tax difference."),
 ],
 sources=[
  ("BEA Regional Price Parities (2024)", "https://fred.stlouisfed.org/series/RPPALL26900"),
  ("BEA RPP housing", "https://fred.stlouisfed.org/series/RPPSERVERENT26900"),
  ("BEA RPP goods", "https://fred.stlouisfed.org/series/RPPGOOD26900"),
  ("BEA RPP other services", "https://fred.stlouisfed.org/series/RPPSERVEOTH26900"),
  ("U.S. Census Bureau, American Community Survey 2025", "https://www.census.gov/programs-surveys/acs/news/data-releases/2025/release.html"),
  ("Freddie Mac 30-year rate (Oct 29, 2026)", "https://fred.stlouisfed.org/series/MORTGAGE30US"),
  ("Indiana Department of Revenue, 2026 tax rates", "https://www.in.gov/dor/files/dn01.pdf"),
  ("2027 rate (Bloomberg Tax)", "https://news.bloombergtax.com/payroll/indiana-decreases-income-tax-rate-for-2026"),
  ("Indiana sales tax", "https://www.in.gov/dor/i-am-a/business-corp/county-tax-information/"),
  ("Indiana DOR food exemption bulletin", "https://www.in.gov/dor/files/reference/sib29.pdf"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("2026 homestead credit (Association of Indiana Counties)", "https://www.in.gov/counties/wabash/files/legal-notices/Legislation-Approved-During-the-2025-Legislative-Session-Provides-New-and-Expanded-Property-Tax-Deductions_.pdf"),
  ("EIA electricity prices (Aug 2026)", "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a"),
  ("EIA average residential bills (2024)", "https://www.eia.gov/electricity/sales_revenue_price/pdf/table_5A.pdf"),
  ("MIT Living Wage Calculator", "https://livingwage.mit.edu/metros/26900"),
  ("home prices: MIBOR REALTOR&reg; Association via our market update", _MARKET),
 ],
 related=[("/blog/living-in-indianapolis-pros-and-cons/", "Living in Indianapolis: Pros and Cons"),
          ("/blog/rent-vs-buy-in-indianapolis-2026-comparison/", "Rent vs. Buy in Indianapolis"),
          ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide")],
 cta=("Planning a Move to Indianapolis?",
      "Tell us your budget and where you work, and our team will show you which parts of the metro make the numbers work, whether you plan to rent first or buy right away.",
      [("/schedule/", "Book a Free Call →", "btn-white"), ("/search/", "Browse Homes for Sale", "btn-outline")]),
 resources=[("/services/relocation-buyers/", "Relocation Buyers"),
            ("/services/mortgages/", "Mortgage Calculator"),
            ("/blog/indiana-property-tax-caps-explained/", "Indiana Property Tax Caps Explained"),
            ("/utilities/", "Utilities by City and Town")],
 link_from=[
  ("blog/living-in-indianapolis-pros-and-cons/index.html",
   '<strong>Running the numbers?</strong> Our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a> covers rent, home prices, taxes, utilities and the salary you need, city vs. suburbs.'),
  ("blog/rent-vs-buy-in-indianapolis-2026-comparison/index.html",
   'For current rent, tax and utility figures across the metro, see our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a>.'),
 ],
)
