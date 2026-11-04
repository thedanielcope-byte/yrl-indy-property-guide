"""Moving from Detroit to Indianapolis (Nov 2026). Move-guide series (Chicago, Cincinnati, Louisville
from build_move_guides.py; Columbus and California from fresh_posts/); same sections and framing.

Every figure is dated and sourced (researched Nov 3 2026):
- BEA Regional Price Parities 2024, metro file MARPP_MSA_2008_2024.csv, read directly. Detroit-Warren-
  Dearborn 19820 vs Indianapolis 26900: all items 100.298 / 95.696; goods 98.817 / 94.318; housing
  94.690 / 88.917; utilities 106.988 / 86.358; other services 102.591 / 99.141.
- Census ACS 2025 1-year table-based summary files, read directly. Metro 310M700US19820 vs 26900:
  B25077 value 284,200 / 304,600; B25064 rent 1,316 / 1,380; B25103 real estate taxes 3,658 / 2,596;
  B19013 income 79,203 / 83,815; B01003 population 4,390,913 / 2,204,583. City of Detroit (2622000):
  value 102,600; taxes 1,449. Indianapolis balance (1836003): taxes 2,393.
- Realcomp MLS via WHMI (Oct 19 2026): Oakland County median sale price "just over $383,500", Sept 2026.
  No regional Realcomp dollar median for Sept 2026 was published that we could find, so none is used.
- MIBOR September 2026 via our October market update: median $320,000. Freddie Mac PMMS 7.24% (Oct 29 2026);
  payment math is ours.
- EIA Electric Power Monthly Table 5.6.A, August 2026 residential: Michigan 22.99, Indiana 17.02, U.S. 18.16 c/kWh.
- Michigan Treasury (Apr 15 2026): 2026 individual rate stays 4.25%. Detroit city income tax 2.4% resident /
  1.2% nonresident (Michigan Treasury Form 5469). Michigan Treasury: 24 cities levy income taxes (list read
  directly; Troy, Novi, Royal Oak, Dearborn are not on it). State Tax Commission Transfer of Ownership
  Guidelines: taxable value increases limited to 1.05 or inflation, whichever is less; uncapped the year after
  a transfer. PRE exempts up to 18 mills of school operating millage (Michigan Treasury).
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026): 2.95% state; Marion 2.02, Hamilton 1.10, Johnson 1.40,
  Hendricks 1.70. Income tax example is our rough math, before exemptions.
- Distance: OpenStreetMap routing (OSRM), downtown to downtown, 278.4 miles via I-75, US-24 and I-69.
- Snow: NWS 1991-2020 normals for Indianapolis (same as the living-in-Indianapolis post).
No crime/safety content. Michigan suburbs are described only by housing style / feel.
"""

_ACS = "https://data.census.gov/table/ACSDT1Y2025."
_MARKET = "/blog/indianapolis-market-update-october-2026/"

_GLANCE = [
    ("Overall price level (BEA, 2024; U.S. = 100)", "95.7", "100.3"),
    ("Housing price level (BEA, 2024)", "88.9", "94.7"),
    ("Utilities price level (BEA, 2024)", "86.4", "107.0"),
    ("Residential electricity (EIA, Aug 2026, statewide)", "17.02&cent;/kWh", "22.99&cent;/kWh"),
    ("Median home value, metro (Census ACS 2025, owner estimates)", "$304,600", "$284,200"),
    ("Median sale price (Sept 2026)", "$320,000 (MIBOR area)", "About $383,500 (Oakland County)"),
    ("Median gross rent, metro (ACS 2025)", "$1,380", "$1,316"),
    ("Median homeowner property tax bill, metro (ACS 2025)", "$2,596", "$3,658"),
    ("Median household income, metro (ACS 2025)", "$83,815", "$79,203"),
    ("Metro population (ACS 2025)", "About 2.2 million", "About 4.4 million"),
    ("Income tax (2026)", "Indiana 2.95% + county tax (1.10%&ndash;2.02% in the core counties)", "Michigan 4.25% + 2.4% if you live in Detroit"),
    ("Time zone", "Eastern", "Eastern"),
]
_GLANCE_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in _GLANCE)

_TAX = [
    ("Detroit", "$4,250", "$2,400 (city)", "about $6,650"),
    ("Troy, Novi or Royal Oak (no city income tax)", "$4,250", "none", "about $4,250"),
    ("Indianapolis (Marion County)", "$2,950", "$2,020", "about $4,970"),
    ("Avon or Plainfield (Hendricks County)", "$2,950", "$1,700", "about $4,650"),
    ("Greenwood (Johnson County)", "$2,950", "$1,400", "about $4,350"),
    ("Carmel or Fishers (Hamilton County)", "$2,950", "$1,100", "about $4,050"),
]
_TAX_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in _TAX)

POST = dict(
 slug="moving-from-detroit-to-indianapolis",
 title="Moving from Detroit to Indianapolis: 2026 Guide",
 headline="Moving from Detroit to Indianapolis: Costs, Taxes & Where to Live",
 h1_html="Moving from Detroit to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em>",
 crumb="Moving from Detroit to Indianapolis",
 desc=("Moving from Detroit or Michigan to Indianapolis? Compare cost of living, home prices, rent, utilities "
       "and taxes, plus where Detroit-area transplants buy."),
 date="2026-11-03", month="November 2026",
 category="Relocation", eyebrow="RELOCATION",
 focus="moving from detroit to indianapolis",
 hero_sub="About five hours south: how cost of living, utilities, home prices and taxes really compare, and where Detroit-area transplants tend to buy.",
 badges=["Relocation", "Detroit to Indy", "Updated for 2026"],
 read_min=7,
 card_title="Moving from Detroit to Indy",
 card_sub="Cost of living, home prices, taxes and where to live, compared.",
 qa_heading="Detroit vs. Indianapolis at a Glance",
 qa_lead=("<strong>Is Indianapolis cheaper than Detroit?</strong> On everyday costs, yes. The BEA scores the Indianapolis "
          "metro at 95.7 and metro Detroit at 100.3 (the U.S. is 100), with the biggest gap in utilities, and the typical "
          "property tax bill is about $1,060 a year lower. Housing is closer than people expect: metro Detroit&rsquo;s median "
          "home value and rent are a little lower overall, but popular suburbs like Oakland County cost more. The drive is about 280 miles."),
 qa_facts=[
  ("Overall price level (2024)", "Indy 95.7 &middot; Detroit metro 100.3"),
  ("Utilities price level (2024)", "Indy 86.4 &middot; Detroit metro 107.0"),
  ("Median home value, metro (2025)", "Indy $304,600 &middot; Detroit $284,200"),
  ("Median property tax bill (2025)", "Indy $2,596 &middot; Detroit $3,658"),
  ("Income tax (2026)", "IN 2.95% + county &middot; MI 4.25% (+2.4% in Detroit)"),
  ("Drive", "About 280 miles, roughly 5 hours"),
 ],
 toc=[("at-a-glance", "Indianapolis vs. Detroit at a Glance"), ("cost-of-living", "Cost of Living"),
      ("home-prices", "Home Prices and Rent"), ("taxes", "Taxes: Income and Property"),
      ("drive", "The Drive and Trips Back"), ("where-to-live", "Where Detroit-Area Transplants Look"),
      ("checklist", "Your Move Checklist"), ("work-with-us", "Talk to Our Team")],
 body=f"""
 <p>A lot of people moving to Indianapolis from Michigan expect a big drop in home prices. The real story is a little different. Day-to-day costs, utilities and property taxes do run lower here, but metro Detroit&rsquo;s housing is already affordable overall, so the bigger wins usually come from what you&rsquo;re comparing against: an Oakland County suburb, a Detroit city address, or a long-held Michigan home with a capped tax bill. Here&rsquo;s what the federal, state and local data shows, where Indianapolis comes out ahead, where it doesn&rsquo;t, and where Detroit-area transplants tend to settle.</p>

 <h2 id="at-a-glance">Indianapolis vs. Detroit at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th></th><th>Indianapolis</th><th>Detroit</th></tr></thead>
 <tbody>
{_GLANCE_ROWS}
 </tbody>
 </table>
 </div>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored <strong>95.7</strong> and metro Detroit <strong>100.3</strong>, so overall prices run roughly 5% lower here. Goods (94.3 vs. 98.8) and housing (88.9 vs. 94.7) are both lower, and the widest gap is utilities: 86.4 in Indianapolis versus 107.0 in metro Detroit, or roughly 19% lower relative to the rest of the country. The Energy Information Administration&rsquo;s August 2026 figures tell the same story: residential electricity averaged 17.02 cents per kilowatt-hour in Indiana and 22.99 cents in Michigan, against a U.S. average of 18.16. Incomes also lean Indianapolis&rsquo;s way, with a median household income of $83,815 in the Indianapolis metro and $79,203 in metro Detroit in 2025 (Census ACS).</p>
 <p>For a line-by-line look at rent, utilities, taxes and the income you need, see our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a>.</p>

 <h2 id="home-prices">Home Prices and Rent</h2>
 <p>This is where the comparison surprises people. The Census Bureau&rsquo;s 2025 survey, which asks owners what their homes are worth, puts the median home value at <strong>$284,200</strong> across metro Detroit versus <strong>$304,600</strong> in metro Indianapolis, and median gross rent at $1,316 versus $1,380. Part of the reason is the city of Detroit itself, where the median owner-estimated value is $102,600, which pulls the metro figure down.</p>
 <p>The suburbs many movers are coming from cost more. Oakland County&rsquo;s median sale price was just over <strong>$383,500</strong> in September 2026, according to Realcomp MLS figures reported by WHMI, while the median across the MIBOR area around Indianapolis was <strong>$320,000</strong>, according to our <a href="{_MARKET}">market update</a>. On that gap, a buyer putting 10% down at the current 7.24% rate (Freddie Mac, Oct. 29, 2026) would pay roughly $390 a month less in principal and interest here, by our math. The two figures cover different areas, so treat this as a rough comparison. Central Indiana&rsquo;s growing suburbs also have plenty of newer construction. Start with our <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> and <a href="/best/most-affordable-indianapolis-suburbs/">most affordable suburbs</a> rankings, see <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford</a>, or <a href="/search/">search live listings</a>.</p>

 <h2 id="taxes">Taxes: Income, Property and the Trade-Offs</h2>
 <p><strong>Income tax.</strong> Michigan&rsquo;s income tax stays at a flat 4.25% for 2026 (Michigan Treasury). Detroit adds a 2.4% city income tax for residents (1.2% for nonresidents who work in the city), and 24 Michigan cities levy some form of income tax in all, including Hamtramck, Highland Park and Pontiac. Most suburbs, including Troy, Novi, Royal Oak and Dearborn, don&rsquo;t. Indiana&rsquo;s state rate is 2.95% on nearly all income, plus a county income tax based on where you live on January 1: 1.10% in Hamilton County, 1.40% in Johnson, 1.70% in Hendricks and 2.02% in Marion County. Here&rsquo;s our rough math for a single filer with $100,000 in wages, before exemptions, deductions and credits:</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Where you live</th><th>State tax</th><th>Local tax</th><th>Total</th></tr></thead>
 <tbody>
{_TAX_ROWS}
 </tbody>
 </table>
 </div>
 <p>So if you&rsquo;re leaving the city of Detroit, every county around Indianapolis comes out well ahead on income tax. If you&rsquo;re leaving a suburb with no city tax, it&rsquo;s close: a little lower in Hamilton County and a few hundred dollars higher in Johnson, Hendricks or Marion County. In your move year, expect to file a part-year Michigan return, plus a Detroit return if you lived in the city.</p>
 <p><strong>Property tax.</strong> The median homeowner property tax bill was <strong>$2,596</strong> in the Indianapolis metro in 2025 versus <strong>$3,658</strong> in metro Detroit (Census ACS), about $1,060 a year less. Inside Detroit&rsquo;s city limits the median bill was lower ($1,449), but that reflects much lower home values. Two rule differences matter. Michigan limits yearly increases in a home&rsquo;s taxable value to 5% or inflation, whichever is less, then resets (&ldquo;uncaps&rdquo;) it the year after a sale, so a long-time Michigan owner&rsquo;s bill can look low compared with what a new buyer pays (Michigan State Tax Commission). Indiana assesses homes at market value each year, and the tax on your primary home is capped at 1% of its assessed value once you file the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a>, which plays a role similar to Michigan&rsquo;s Principal Residence Exemption. Compare counties in our guide to <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>. This is general information, not tax advice, so run your own numbers with a tax professional.</p>

 <h2 id="drive">The Drive and Trips Back</h2>
 <p>Indianapolis is about 280 miles from downtown Detroit, roughly a five-hour drive. The most direct route runs south on I-75 to Toledo, then US-24 to Fort Wayne and I-69 into Indianapolis; some drivers prefer I-94 west to I-69 south. Both cities are on Eastern time. I-69 enters the metro from the northeast through Fishers, so Hamilton County keeps trips back to Michigan shortest. Winters will feel familiar: Indianapolis averages about 25.5 inches of snow a year (National Weather Service, 1991&ndash;2020 normals).</p>

 <h2 id="where-to-live">Where Detroit-Area Transplants Tend to Look</h2>
 <ul>
 <li><strong>If you liked Troy, Novi or Rochester Hills:</strong> <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>, <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a>, <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a> and <a href="/cities/hamilton-county/noblesville-indiana-real-estate/">Noblesville</a> in Hamilton County, which also has the metro&rsquo;s lowest county income tax.</li>
 <li><strong>If you liked Royal Oak, Ferndale or Birmingham&rsquo;s walkable downtowns:</strong> <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>, <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>, <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a>, <a href="/neighborhoods/irvington-indianapolis/">Irvington</a> and <a href="/neighborhoods/meridian-kessler-indianapolis/">Meridian-Kessler</a>, or <a href="/cities/boone-county/zionsville-indiana-real-estate/">Zionsville</a>&rsquo;s brick-street village.</li>
 <li><strong>If you liked the newer subdivisions of Macomb Township or Canton:</strong> <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a>, <a href="/neighborhoods/franklin-township-indianapolis/">Franklin Township</a>, <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a>, <a href="/cities/hendricks-county/brownsburg-indiana-real-estate/">Brownsburg</a> and <a href="/cities/hendricks-county/plainfield-indiana-real-estate/">Plainfield</a>.</li>
 <li><strong>If you&rsquo;ll miss lake life:</strong> Central Indiana has no Great Lakes, but Geist and Morse reservoirs on the northeast side have waterfront neighborhoods. See our <a href="/blog/waterfront-living-near-indianapolis-lakes-guide/">lakes guide</a> and <a href="/blog/geist-reservoir-waterfront-homes-near-indianapolis/">Geist Reservoir homes</a>.</li>
 </ul>
 <p>Not sure which fits? Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro, and our honest look at <a href="/blog/living-in-indianapolis-pros-and-cons/">the pros and cons of living in Indianapolis</a> covers the trade-offs. Moving from somewhere else? See our <a href="/blog/moving-from-chicago-to-indianapolis/">Chicago</a>, <a href="/blog/moving-from-columbus-to-indianapolis/">Columbus</a> and <a href="/blog/moving-from-cincinnati-to-indianapolis/">Cincinnati</a> guides.</p>

 <h2 id="checklist">Your Move Checklist</h2>
 <ul>
 <li>Update your driver&rsquo;s license and vehicle registration with the Indiana BMV.</li>
 <li>File your homestead deduction with the county auditor after you close.</li>
 <li>If you sell or stop living in your Michigan home, ask your assessor about rescinding its Principal Residence Exemption (Michigan Form 2602).</li>
 <li>Plan on part-year Michigan (and, if you lived there, Detroit) returns, and check which Indiana county&rsquo;s income tax applies.</li>
 <li>Set up utilities before move-in with our <a href="/utilities/">Central Indiana utilities guide</a>.</li>
 <li>Talk with us about <a href="/services/buyer-representation/">buyer representation</a>; a written buyer agreement sets out how your agent is paid, so you know the terms before you tour.</li>
 </ul>

 <h2 id="work-with-us">Talk to Our Team</h2>
 <p>Our team helps relocating buyers every month, including <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">live virtual tours</a> and buying before you arrive. Tell us what you have in Michigan and what you want here, and we&rsquo;ll map out the areas that fit. Call <a href="tel:3179977404">317-997-7404</a> or <a href="/schedule/buyer-consultation/">book a buyer consultation</a>.</p>
""",
 faqs=[
  ("Is Indianapolis cheaper than Detroit?",
   "On everyday costs, yes. The Bureau of Economic Analysis puts 2024 price levels at 95.7 for the Indianapolis metro and 100.3 for metro Detroit, with utilities the biggest gap (86.4 vs. 107.0). The median property tax bill is also about $1,060 a year lower in the Indianapolis metro. Housing is closer: metro Detroit's median home value ($284,200) and rent ($1,316) are slightly lower than Indianapolis's ($304,600 and $1,380) in the 2025 Census survey, though suburbs like Oakland County cost more."),
  ("How far is Indianapolis from Detroit?",
   "About 280 miles from downtown to downtown, roughly a five-hour drive. The most direct route uses I-75 to Toledo, US-24 to Fort Wayne and I-69 into Indianapolis. Both cities are on Eastern time."),
  ("Are income taxes lower in Indiana than in Michigan?",
   "Compared with living in Detroit, yes. A Detroit resident pays Michigan's 4.25% plus the city's 2.4% income tax. Indiana's rate is 2.95% plus a county tax from 1.10% in Hamilton County to 2.02% in Marion County. On $100,000 of wages, our rough math before exemptions comes to about $6,650 in Detroit, $4,250 in a Michigan suburb with no city tax, $4,050 in Hamilton County and $4,970 in Marion County."),
  ("Are property taxes lower in Indianapolis than in metro Detroit?",
   "Generally, yes. The median homeowner property tax bill was $2,596 in the Indianapolis metro in 2025 versus $3,658 in metro Detroit, according to the Census Bureau's American Community Survey. Indiana caps property taxes on a primary home at 1% of assessed value once you file the homestead deduction. Michigan caps yearly increases in taxable value instead, then resets the value after a sale."),
  ("Which Indianapolis suburbs feel most like Troy or Novi?",
   "Buyers who like newer, planned suburbs often look at Carmel, Fishers, Westfield and Noblesville in Hamilton County. If you preferred Royal Oak or Ferndale's walkable downtowns, close-in Indianapolis neighborhoods like Broad Ripple, Mass Ave and Fountain Square, or the village of Zionsville, have a similar feel."),
  ("Can I buy a home in Indianapolis before I move from Michigan?",
   "Yes, and many relocating buyers do. Our team runs live video tours, gives honest neighborhood and condition read-outs, and coordinates inspections and closing so you can buy while you're still in Michigan. Many buyers also make one in-person trip to see their short list."),
 ],
 sources=[
  ("BEA Regional Price Parities by metro (2024)", "https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area"),
  ("Detroit RPP via FRED", "https://fred.stlouisfed.org/series/RPPALL19820"),
  ("Census ACS 2025 median home value", _ACS + "B25077"),
  ("median gross rent", _ACS + "B25064"),
  ("median real estate taxes", _ACS + "B25103"),
  ("median household income", _ACS + "B19013"),
  ("Realcomp September 2026 figures via WHMI (Oct 19, 2026)", "https://www.whmi.com/news/article/home-sales-in-se-mi-slowed-in-september-despite-influx-of-new-listings"),
  ("Indianapolis home prices: MIBOR REALTOR&reg; Association via our market update", _MARKET),
  ("Freddie Mac mortgage rates (Oct 29, 2026)", "https://www.freddiemac.com/pmms"),
  ("EIA electricity prices by state (August 2026)", "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a"),
  ("Michigan Treasury, 2026 income tax rate", "https://www.michigan.gov/treasury/news/2026/04/15/state-individual-income-tax-rate-for-2026-tax-year-determined"),
  ("Michigan Treasury, Detroit income tax withholding (Form 5469)", "https://www.michigan.gov/taxes/-/media/Project/Websites/taxes/Forms/City-Withholding/TY2025/5469_ty2025.pdf"),
  ("Michigan Treasury, cities that impose an income tax", "https://www.michigan.gov/taxes/citytax/what-cities-impose-an-income-tax"),
  ("Michigan State Tax Commission, transfer of ownership and uncapping", "https://www.michigan.gov/-/media/Project/Websites/treasury/MISC_9/TransferOwnershipGuidelines.pdf"),
  ("Michigan Treasury, Principal Residence Exemption", "https://www.michigan.gov/taxes/property/principal"),
  ("Indiana DOR county tax rates (2026)", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("National Weather Service climate normals", "https://www.weather.gov/media/ind/climate/INDnormalschange.pdf"),
  ("distance: OpenStreetMap routing", "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=42.3314%2C-83.0458%3B39.7684%2C-86.1581"),
 ],
 related=[
  ("/blog/moving-from-chicago-to-indianapolis/", "Moving from Chicago to Indianapolis"),
  ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
  ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
 ],
 cta=("Moving From Michigan?",
      "Tell us what you have in metro Detroit and what you want here, and we&rsquo;ll map out the areas that fit, including virtual tours if you&rsquo;re buying before you arrive.",
      [("/services/relocation-buyers/", "Explore Relocation Services →", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[
  ("/services/relocation-buyers/", "Relocation Buyers"),
  ("/blog/indiana-property-tax-caps-explained/", "Indiana Property Tax Caps Explained"),
  ("/utilities/", "Utilities by City and Town"),
  ("/blog/relocating-to-indianapolis-virtual-home-tours/", "Buying With Virtual Home Tours"),
 ],
 link_from=[
  ("blog/moving-to-indianapolis-relocation-guide/index.html",
   '<strong>Coming from Michigan?</strong> See our <a href="/blog/moving-from-detroit-to-indianapolis/">guide to moving from Detroit to Indianapolis</a>, comparing cost of living, utilities, home prices and taxes side by side.'),
  ("blog/moving-from-chicago-to-indianapolis/index.html",
   'Moving from Detroit instead? Our <a href="/blog/moving-from-detroit-to-indianapolis/">Detroit to Indianapolis guide</a> runs the same comparison, including the utility and property tax gaps.'),
 ],
)
