"""Moving from Columbus, Ohio to Indianapolis (Nov 2026). Fourth guide in the move series
(Chicago, Cincinnati, Louisville come from build_move_guides.py); same sections and framing.

Every figure is dated and sourced (researched Nov 3 2026):
- BEA Regional Price Parities 2024, metro file MARPP_MSA_2008_2024.csv (updated Feb 19 2026), read
  directly: all items Indy 95.696 / Columbus 95.469; goods 94.318 / 93.628; housing 88.917 / 87.945;
  utilities 86.358 / 95.523; other services 99.141 / 98.939.
- Census ACS 2025 1-year summary files (table-based SF, read directly). Metro CBSA 26900 vs 18140:
  B25077 median value 304,600 / 347,600; B25064 median gross rent 1,380 / 1,468; B25103 median real
  estate taxes 2,596 / 4,433; B19013 median household income 83,815 / 84,015; B01003 population
  2,204,583 / 2,242,028. Cities (Indianapolis balance 1836003 / Columbus 3918000): taxes 2,393 / 3,900.
  Hamilton County, IN (from fresh_posts/cost-of-living-in-indianapolis.py, same tables): value 483,600, taxes 4,356.
- Columbus REALTORS Local Market Update, September 2026, Entire MLS: median $334,250 (+2.8%), 33 days, 2,550 closed.
- MIBOR September 2026 via our October market update: median $320,000, 27 days.
- Freddie Mac PMMS 7.24% (Oct 29 2026). Payment gap math is ours.
- Ohio HB 96: flat 2.75% on income over $26,050 from 2026 (EY). Columbus city income tax 2.5%, 100% credit
  for tax paid to another municipality up to 2.5% (City of Columbus IR-25 instructions, 2025).
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026): 2.95% state; Marion 2.02, Hamilton 1.10, Johnson 1.40,
  Hendricks 1.70, Boone 1.71, Hancock 1.94. Income tax example is our rough math, before exemptions.
- Distance: OpenStreetMap routing (OSRM), downtown to downtown, 175.8 miles.
No crime/safety content. Ohio suburbs are described only by housing style / feel.
"""

_ACS = "https://data.census.gov/table/ACSDT1Y2025."
_MARKET = "/blog/indianapolis-market-update-october-2026/"
_HOME = "https://yourrealtylink.com"

_GLANCE = [
    ("Overall price level (BEA, 2024; U.S. = 100)", "95.7", "95.5"),
    ("Housing price level (BEA, 2024)", "88.9", "87.9"),
    ("Utilities price level (BEA, 2024)", "86.4", "95.5"),
    ("Median sale price (Sept 2026, local REALTOR&reg; reports)", "$320,000", "$334,250"),
    ("Median home value, metro (Census ACS 2025, owner estimates)", "$304,600", "$347,600"),
    ("Median gross rent, metro (ACS 2025)", "$1,380", "$1,468"),
    ("Median homeowner property tax bill, metro (ACS 2025)", "$2,596", "$4,433"),
    ("Median household income, metro (ACS 2025)", "$83,815", "$84,015"),
    ("Income tax (2026)", "Indiana 2.95% + county tax (1.10%&ndash;2.02% in the core counties)", "Ohio 2.75% above $26,050 + Columbus 2.5%"),
    ("Time zone", "Eastern", "Eastern"),
]
_GLANCE_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in _GLANCE)

_TAX = [
    ("Columbus", "about $2,030", "$2,500 (city)", "about $4,530"),
    ("Indianapolis (Marion County)", "$2,950", "$2,020", "about $4,970"),
    ("Avon or Plainfield (Hendricks County)", "$2,950", "$1,700", "about $4,650"),
    ("Greenwood (Johnson County)", "$2,950", "$1,400", "about $4,350"),
    ("Carmel or Fishers (Hamilton County)", "$2,950", "$1,100", "about $4,050"),
]
_TAX_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in _TAX)

POST = dict(
 slug="moving-from-columbus-to-indianapolis",
 title="Moving from Columbus to Indianapolis: 2026 Guide",
 headline="Moving from Columbus to Indianapolis: Costs, Taxes & Where to Live",
 h1_html="Moving from Columbus to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em>",
 crumb="Moving from Columbus to Indianapolis",
 desc=("Moving from Columbus, Ohio to Indianapolis? Compare cost of living, home prices, rent, property taxes "
       "and the I-70 drive, plus where Columbus transplants buy."),
 date="2026-11-03", month="November 2026",
 category="Relocation", eyebrow="RELOCATION",
 focus="moving from columbus to indianapolis",
 hero_sub="About three hours west on I-70: how cost of living, home prices and taxes really compare, and where Columbus transplants tend to buy.",
 badges=["Relocation", "Columbus to Indy", "Updated for 2026"],
 read_min=7,
 card_title="Moving from Columbus to Indy",
 card_sub="Cost of living, home prices, taxes and where to live, compared.",
 qa_heading="Columbus vs. Indianapolis at a Glance",
 qa_lead=("<strong>Is Indianapolis cheaper than Columbus?</strong> A little, mostly on housing. Overall prices are "
          "about the same (the BEA scores Indianapolis 95.7 and Columbus 95.5, where the U.S. is 100), but homes sell for a bit "
          "less in Indianapolis, rent is lower, and the typical property tax bill is about $1,800 a year lower. Income "
          "taxes land in the same range, depending on which county you choose. The drive is about 176 miles on I-70."),
 qa_facts=[
  ("Overall price level (2024)", "Indy 95.7 &middot; Columbus 95.5"),
  ("Median sale price (Sept 2026)", "Indy $320,000 &middot; Columbus $334,250"),
  ("Median rent, metro (2025)", "Indy $1,380 &middot; Columbus $1,468"),
  ("Median property tax bill (2025)", "Indy $2,596 &middot; Columbus $4,433"),
  ("Income tax (2026)", "IN 2.95% + county &middot; OH 2.75% + Columbus 2.5%"),
  ("Drive", "About 176 miles on I-70, roughly 3 hours"),
 ],
 toc=[("at-a-glance", "Indianapolis vs. Columbus at a Glance"), ("cost-of-living", "Cost of Living"),
      ("home-prices", "Home Prices and Rent"), ("taxes", "Taxes: Income and Property"),
      ("drive", "The Drive and Trips Back"), ("where-to-live", "Where Columbus Transplants Look"),
      ("checklist", "Your Move Checklist"), ("work-with-us", "Talk to Our Team")],
 body=f"""
 <p>Columbus and Indianapolis might be the two most alike big cities in the Midwest. Both are state capitals, both metros have about 2.2 million people, and the typical household earns almost exactly the same in each. So a move from Columbus usually isn&rsquo;t about a dramatically cheaper life. It&rsquo;s about a job, family, or getting more house for the money. Here&rsquo;s what the federal, state and local data shows, where Indianapolis comes out ahead, where it doesn&rsquo;t, and where Columbus transplants tend to settle.</p>

 <h2 id="at-a-glance">Indianapolis vs. Columbus at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th></th><th>Indianapolis</th><th>Columbus</th></tr></thead>
 <tbody>
{_GLANCE_ROWS}
 </tbody>
 </table>
 </div>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored <strong>95.7</strong> and the Columbus metro <strong>95.5</strong>, which is a statistical tie. Goods (94.3 vs. 93.6) and housing (88.9 vs. 87.9) are nearly identical too. The one category with a real gap is utilities: Indianapolis scored 86.4 to Columbus&rsquo;s 95.5, so utility costs run roughly 10% lower relative to the rest of the country. Incomes match as well: the median household earned $83,815 in the Indianapolis metro and $84,015 in the Columbus metro in 2025 (Census ACS).</p>
 <p>In other words, your grocery bill and your paycheck will feel about the same. The differences show up in home prices, rent and, most of all, property taxes. Our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a> goes line by line through rent, utilities, taxes and the income you need.</p>

 <h2 id="home-prices">Home Prices and Rent</h2>
 <p>Columbus REALTORS&reg; reported a median sale price of <strong>$334,250</strong> for September 2026, while the median across the MIBOR area around Indianapolis was <strong>$320,000</strong>, according to our <a href="{_MARKET}">market update</a>. That&rsquo;s about $14,000 less in Indianapolis, or roughly $90 a month on a mortgage with 10% down at the current 7.24% rate (Freddie Mac, Oct. 29, 2026). Homes also sold a little faster here: a median of 27 days versus 33. Each association reports on its own service area, so treat this as a rough comparison.</p>
 <p>The Census Bureau&rsquo;s 2025 survey, which asks owners what their homes are worth, shows a wider gap: a median of $304,600 in the Indianapolis metro versus $347,600 in the Columbus metro. Renters see a smaller difference, with median gross rent at $1,380 versus $1,468, about $90 a month. Central Indiana&rsquo;s fast-growing suburbs also have plenty of newer construction, so many buyers trade up to a newer home at a similar price. Start with our <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> and <a href="/best/most-affordable-indianapolis-suburbs/">most affordable suburbs</a> rankings, see <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford</a>, or <a href="/search/">search live listings</a>.</p>

 <h2 id="taxes">Taxes: Income, Property and the Trade-Offs</h2>
 <p><strong>Income tax.</strong> Ohio&rsquo;s income tax is a flat 2.75% for 2026 on income above $26,050, and the City of Columbus adds a 2.5% income tax (residents who work in another Ohio city get credit for that city&rsquo;s tax, up to 2.5%). Indiana&rsquo;s state rate is 2.95% on nearly all income, plus a county income tax based on where you live on January 1: 1.10% in Hamilton County, 1.40% in Johnson, 1.70% in Hendricks, 1.71% in Boone, 1.94% in Hancock and 2.02% in Marion County. Here&rsquo;s our rough math for a single filer with $100,000 in wages, before exemptions, deductions and credits:</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Where you live</th><th>State tax</th><th>Local tax</th><th>Total</th></tr></thead>
 <tbody>
{_TAX_ROWS}
 </tbody>
 </table>
 </div>
 <p>So income tax is close to a wash. You&rsquo;ll pay less than in Columbus if you live in Hamilton or Johnson County, about the same in Hendricks or Boone, and a few hundred dollars more in Marion or Hancock County. In your move year, expect to file part-year returns in Ohio and Columbus.</p>
 <p><strong>Property tax.</strong> This is where Indianapolis clearly wins. The median homeowner property tax bill was <strong>$2,596</strong> in the Indianapolis metro in 2025 versus <strong>$4,433</strong> in the Columbus metro (Census ACS), about $1,800 a year less, and inside the city limits it was $2,393 in Indianapolis versus $3,900 in Columbus. Indiana&rsquo;s constitution caps property taxes on your primary home at 1% of its assessed value once you file the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a>. Bills still follow home values: Hamilton County&rsquo;s median was $4,356, close to Columbus&rsquo;s, but on homes with a median value of $483,600. Compare counties in our guide to <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>. This is general information, not tax advice, so run your own numbers with a tax professional.</p>

 <h2 id="drive">The Drive and Trips Back</h2>
 <p>Indianapolis is about 176 miles west of Columbus, almost all of it on I-70, roughly a three-hour drive. Both cities are on Eastern time, so there&rsquo;s no clock change. I-70 comes into Indianapolis from the east, so if you&rsquo;ll be driving back to Ohio often, the east side and Hancock County keep that trip shortest.</p>

 <h2 id="where-to-live">Where Columbus Transplants Tend to Look</h2>
 <ul>
 <li><strong>If you liked a newer, planned suburb like Dublin or New Albany:</strong> <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>, <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a> and <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a> in Hamilton County, which also has the metro&rsquo;s lowest county income tax, and <a href="/cities/boone-county/zionsville-indiana-real-estate/">Zionsville</a> with its brick-street village.</li>
 <li><strong>If you liked German Village, the Short North or Clintonville:</strong> close-in Indianapolis neighborhoods with older homes and walkable streets, like <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a>, <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>, <a href="/neighborhoods/irvington-indianapolis/">Irvington</a>, <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a> and <a href="/neighborhoods/meridian-kessler-indianapolis/">Meridian-Kessler</a>.</li>
 <li><strong>If you liked the value of Grove City or Hilliard:</strong> newer subdivisions with easy interstate access in <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a>, <a href="/neighborhoods/franklin-township-indianapolis/">Franklin Township</a>, <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a> and <a href="/cities/hendricks-county/plainfield-indiana-real-estate/">Plainfield</a>.</li>
 <li><strong>Close to I-70 for trips back to Ohio:</strong> <a href="/cities/hancock-county/greenfield-indiana-real-estate/">Greenfield</a>, <a href="/cities/hancock-county/cumberland-indiana-real-estate/">Cumberland</a> and Irvington on the east side.</li>
 </ul>
 <p>Not sure which fits? Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro, and our honest look at <a href="/blog/living-in-indianapolis-pros-and-cons/">the pros and cons of living in Indianapolis</a> covers the trade-offs. Moving from somewhere else? See our <a href="/blog/moving-from-chicago-to-indianapolis/">Chicago</a>, <a href="/blog/moving-from-cincinnati-to-indianapolis/">Cincinnati</a> and <a href="/blog/moving-from-louisville-to-indianapolis/">Louisville</a> guides.</p>

 <h2 id="checklist">Your Move Checklist</h2>
 <ul>
 <li>Update your driver&rsquo;s license and vehicle registration with the Indiana BMV.</li>
 <li>File your homestead deduction with the county auditor after you close.</li>
 <li>Check which county&rsquo;s income tax applies for your move year, and plan on part-year Ohio and Columbus returns.</li>
 <li>Set up utilities before move-in with our <a href="/utilities/">Central Indiana utilities guide</a>.</li>
 <li>Talk with us about <a href="/services/buyer-representation/">buyer representation</a>; a written buyer agreement sets out how your agent is paid, so you know the terms before you tour.</li>
 </ul>

 <h2 id="work-with-us">Talk to Our Team</h2>
 <p>Our team helps relocating buyers every month, including <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">live virtual tours</a> and buying before you arrive. Tell us what you have in Columbus and what you want here, and we&rsquo;ll map out the areas that fit. Call <a href="tel:3179977404">317-997-7404</a> or <a href="/schedule/buyer-consultation/">book a buyer consultation</a>.</p>
""",
 faqs=[
  ("Is Indianapolis cheaper than Columbus, Ohio?",
   "Slightly, mostly on housing and property taxes. The Bureau of Economic Analysis puts 2024 price levels at 95.7 for the Indianapolis metro and 95.5 for Columbus, essentially the same. But the median sale price in September 2026 was $320,000 in the MIBOR area versus $334,250 for Columbus REALTORS, median rent is about $90 a month lower, and the median property tax bill is about $1,800 a year lower in the Indianapolis metro (Census ACS 2025)."),
  ("How far is Indianapolis from Columbus, Ohio?",
   "About 176 miles, almost all of it on I-70, or roughly three hours by car. Both cities are on Eastern time."),
  ("Are income taxes higher in Indianapolis or Columbus?",
   "It depends on the county. A Columbus resident pays Ohio's 2.75% on income above $26,050 plus the city's 2.5% income tax. In Indiana it's 2.95% plus a county tax that ranges from 1.10% in Hamilton County to 2.02% in Marion County. On $100,000 of wages, our rough math before exemptions comes to about $4,530 in Columbus, $4,050 in Hamilton County and $4,970 in Marion County."),
  ("Are property taxes lower in Indianapolis than in Columbus?",
   "Generally, yes. The median homeowner property tax bill was $2,596 in the Indianapolis metro in 2025 versus $4,433 in the Columbus metro, according to the Census Bureau's American Community Survey. Indiana caps property taxes on a primary home at 1% of assessed value once you file the homestead deduction."),
  ("Which Indianapolis suburbs feel most like Dublin or New Albany?",
   "Buyers who like newer, planned suburbs often look at Carmel, Fishers and Westfield in Hamilton County, or Zionsville in Boone County. If you preferred German Village or the Short North, close-in Indianapolis neighborhoods like Fountain Square, Mass Ave and Irvington have a similar walkable, older-home feel."),
  ("Can I buy a home in Indianapolis before I move from Columbus?",
   "Yes, and many relocating buyers do. Our team runs live video tours, gives honest neighborhood and condition read-outs, and coordinates inspections and closing so you can buy while you're still in Columbus. At about three hours away, many buyers also make one in-person trip to see their short list."),
 ],
 sources=[
  ("BEA Regional Price Parities by metro (2024)", "https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area"),
  ("Columbus RPP via FRED", "https://fred.stlouisfed.org/series/RPPALL18140"),
  ("Census ACS 2025 median home value", _ACS + "B25077"),
  ("median gross rent", _ACS + "B25064"),
  ("median real estate taxes", _ACS + "B25103"),
  ("median household income", _ACS + "B19013"),
  ("Columbus REALTORS&reg; Local Market Update, September 2026", "https://marketstatsreports.showingtime.com/CR/sst/2026-09/Entire-MLS.pdf"),
  ("Indianapolis home prices: MIBOR REALTOR&reg; Association via our market update", _MARKET),
  ("Freddie Mac mortgage rates (Oct 29, 2026)", "https://www.freddiemac.com/pmms"),
  ("Indiana DOR county tax rates (2026)", "https://www.in.gov/dor/files/dn01.pdf"),
  ("EY: Ohio 2026 flat income tax (HB 96)", "https://taxnews.ey.com/news/2025-1744-ohio-legislation-lowers-top-personal-tax-rate-retroactive-to-january-1-2025-implements-flat-tax-in-2026"),
  ("City of Columbus income tax instructions (2025)", "https://www.columbus.gov/files/sharedassets/city/v/4/city-auditor/tax-forms/individuals/2025-ir-25-instructions.pdf"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("distance: OpenStreetMap routing", "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=39.9612%2C-82.9988%3B39.7684%2C-86.1581"),
 ],
 related=[
  ("/blog/moving-from-cincinnati-to-indianapolis/", "Moving from Cincinnati to Indianapolis"),
  ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
  ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
 ],
 cta=("Moving From Columbus?",
      "Tell us what you have in Columbus and what you want here, and we&rsquo;ll map out the areas that fit, including virtual tours if you&rsquo;re buying before you arrive.",
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
   '<strong>Coming from Ohio?</strong> See our <a href="/blog/moving-from-columbus-to-indianapolis/">guide to moving from Columbus to Indianapolis</a>, with cost of living, home prices and taxes compared side by side.'),
  ("blog/moving-from-cincinnati-to-indianapolis/index.html",
   'Moving from Columbus instead? Our <a href="/blog/moving-from-columbus-to-indianapolis/">Columbus to Indianapolis guide</a> runs the same comparison, including the property tax gap.'),
 ],
)
