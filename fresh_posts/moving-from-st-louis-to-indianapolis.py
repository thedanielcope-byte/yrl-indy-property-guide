"""Moving from St. Louis to Indianapolis (Nov 2026). Joins the move-guide series (Chicago,
Cincinnati, Louisville from build_move_guides.py; Columbus and California in fresh_posts/) with
the same sections and framing. Honest result: St. Louis is a touch cheaper overall and on rent and
utilities; Indianapolis wins on property taxes and recent sale prices.

Every figure is dated and sourced (researched Nov 3 2026):
- BEA Regional Price Parities 2024, metro file MARPP_MSA_2008_2024.csv (read directly): all items
  Indy 95.696 / St. Louis MO-IL (41180) 95.088; goods 94.318 / 99.996; housing 88.917 / 79.024;
  utilities 86.358 / 69.921; other services 99.141 / 98.642.
- Census ACS 2025 1-year summary files (acsdt1y2025-*.dat, read directly). Metro 26900 vs 41180:
  B25077 median value 304,600 / 283,300; B25064 median gross rent 1,380 / 1,232; B25103 median real
  estate taxes 2,596 / 3,187; B19013 median household income 83,815 / 83,656; B01003 population
  2,204,583 / 2,812,963. Cities (Indianapolis balance 1836003 / St. Louis city 2965000): taxes 2,393 /
  2,269. St. Louis County (29189) value 316,900, taxes 3,641; St. Charles County (29183) value 365,800,
  taxes 3,836. Hamilton County, IN value 483,600, taxes 4,356 (same tables, as in the Columbus guide).
- St. Louis REALTORS(R) Monthly Indicators, September 2026 (MARIS data, current as of Oct 5 2026),
  single-family: median $340,000 (+7.3%), 31 days on market, 1,302 closed. MIBOR September 2026
  single-family via our October market update: $320,000, 27 days. Payment gap math is ours
  (7.24% Freddie Mac Oct 29 2026, 10% down, 30 years): about $123/month.
- Missouri DOR FY2025 Financial and Statistical Report: top individual rate 4.7% for 2025 and 2026.
  City of St. Louis 1% earnings tax on residents (wherever they work) and on nonresidents for work in
  the city (City Collector of Revenue). Illinois 4.95% flat, 2026 exemption $2,925 (IL-700-T 2026).
- Missouri vehicle personal property tax: assessed at 33 1/3% of value as of Jan 1 (RSMo 137.115),
  declaration filed with the county assessor (St. Louis County new-resident declaration). Indiana
  vehicle excise tax by class (original MSRP) and age, paid at registration; new residents have 60
  days to title and register (Indiana BMV).
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026) county rates, as in the Columbus guide.
  Income tax table is our rough math at the top/flat rates, before exemptions, deductions and credits.
- Distance: OpenStreetMap routing (OSRM), downtown to downtown, 243.5 miles.
No crime/safety content. Missouri suburbs are described only by housing style / feel.
"""

_ACS = "https://data.census.gov/table/ACSDT1Y2025."
_MARKET = "/blog/indianapolis-market-update-october-2026/"

_GLANCE = [
    ("Overall price level (BEA, 2024; U.S. = 100)", "95.7", "95.1"),
    ("Goods price level (BEA, 2024)", "94.3", "100.0"),
    ("Housing price level (BEA, 2024)", "88.9", "79.0"),
    ("Utilities price level (BEA, 2024)", "86.4", "69.9"),
    ("Median sale price, single-family (Sept 2026, local REALTOR&reg; reports)", "$320,000", "$340,000"),
    ("Median home value, metro (Census ACS 2025, owner estimates)", "$304,600", "$283,300"),
    ("Median gross rent, metro (ACS 2025)", "$1,380", "$1,232"),
    ("Median homeowner property tax bill, metro (ACS 2025)", "$2,596", "$3,187"),
    ("Median household income, metro (ACS 2025)", "$83,815", "$83,656"),
    ("Income tax (2026)", "Indiana 2.95% + county tax (1.10%&ndash;2.02% in the core counties)", "Missouri up to 4.7% (+1% city earnings tax in St. Louis); Illinois side 4.95%"),
    ("Time zone", "Eastern", "Central"),
]
_GLANCE_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in _GLANCE)

_TAX = [
    ("City of St. Louis", "$4,700", "$1,000 (city earnings tax)", "about $5,700"),
    ("St. Louis County or St. Charles County, working outside the city", "$4,700", "none", "about $4,700"),
    ("Illinois side (Metro East)", "$4,950", "none", "about $4,950"),
    ("Indianapolis (Marion County)", "$2,950", "$2,020", "about $4,970"),
    ("Avon or Plainfield (Hendricks County)", "$2,950", "$1,700", "about $4,650"),
    ("Greenwood (Johnson County)", "$2,950", "$1,400", "about $4,350"),
    ("Carmel or Fishers (Hamilton County)", "$2,950", "$1,100", "about $4,050"),
]
_TAX_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in _TAX)

POST = dict(
 slug="moving-from-st-louis-to-indianapolis",
 title="Moving from St. Louis to Indianapolis: 2026 Guide",
 headline="Moving from St. Louis to Indianapolis: Costs, Taxes & Where to Live",
 h1_html="Moving from St. Louis to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em>",
 crumb="Moving from St. Louis to Indianapolis",
 desc=("Moving from St. Louis to Indianapolis? Compare cost of living, home prices, rent, property and income "
       "taxes and the I-70 drive, plus where to look."),
 date="2026-11-03", month="November 2026",
 category="Relocation", eyebrow="RELOCATION",
 focus="moving from st louis to indianapolis",
 hero_sub="About four hours east on I-70: how cost of living, home prices and taxes really compare, where St. Louis comes out ahead, and where St. Louis transplants tend to buy.",
 badges=["Relocation", "St. Louis to Indy", "Updated for 2026"],
 read_min=8,
 card_title="Moving from St. Louis to Indy",
 card_sub="Cost of living, home prices, taxes and where to live, compared.",
 qa_heading="St. Louis vs. Indianapolis at a Glance",
 qa_lead=("<strong>Is Indianapolis cheaper than St. Louis?</strong> Not overall. The BEA puts both metros just below the "
          "national average (Indianapolis 95.7, St. Louis 95.1, where the U.S. is 100), and St. Louis is cheaper on rent and "
          "utilities. Indianapolis comes out ahead on property taxes, with a median bill about $600 a year lower, and "
          "single-family homes sold for a median $20,000 less in September 2026. The drive is about 244 miles on I-70, and "
          "Indianapolis is an hour ahead."),
 qa_facts=[
  ("Overall price level (2024)", "Indy 95.7 &middot; St. Louis 95.1"),
  ("Median sale price, single-family (Sept 2026)", "Indy $320,000 &middot; St. Louis $340,000"),
  ("Median rent, metro (2025)", "Indy $1,380 &middot; St. Louis $1,232"),
  ("Median property tax bill (2025)", "Indy $2,596 &middot; St. Louis $3,187"),
  ("Income tax (2026)", "IN 2.95% + county &middot; MO up to 4.7% (+1% in the city)"),
  ("Drive", "About 244 miles on I-70; Indy is an hour ahead"),
 ],
 toc=[("at-a-glance", "Indianapolis vs. St. Louis at a Glance"), ("cost-of-living", "Cost of Living"),
      ("home-prices", "Home Prices and Rent"), ("taxes", "Taxes: Income, Property and Vehicles"),
      ("drive", "The Drive and the Time Change"), ("where-to-live", "Where St. Louis Transplants Look"),
      ("checklist", "Your Move Checklist"), ("work-with-us", "Talk to Our Team")],
 body=f"""
 <p>St. Louis and Indianapolis have a lot in common: big Midwest metros on I-70, similar paychecks, and plenty of house for the money compared with the coasts. So a move from St. Louis is usually about a job, family or a fresh start rather than a dramatically cheaper life, and on a few costs St. Louis actually comes out ahead. Here&rsquo;s what the federal, state and local data shows, where each city wins, and where St. Louis transplants tend to settle around Indianapolis.</p>

 <h2 id="at-a-glance">Indianapolis vs. St. Louis at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th></th><th>Indianapolis</th><th>St. Louis</th></tr></thead>
 <tbody>
{_GLANCE_ROWS}
 </tbody>
 </table>
 </div>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored <strong>95.7</strong> and the St. Louis metro <strong>95.1</strong>, so St. Louis is slightly cheaper overall. The categories pull in different directions. St. Louis is clearly cheaper on housing (79.0 vs. 88.9) and utilities (69.9 vs. 86.4), while goods cost more there (100.0 vs. 94.3), right at the national average. Incomes are a near match: the median household earned $83,815 in the Indianapolis metro and $83,656 in the St. Louis metro in 2025 (Census ACS).</p>
 <p>In other words, day-to-day life costs about the same. Your rent and utility bills may run a little higher in Indianapolis, your shopping a little lower, and the bigger differences show up in property taxes and the kind of home you buy. Our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a> goes line by line through rent, utilities, taxes and the income you need.</p>

 <h2 id="home-prices">Home Prices and Rent</h2>
 <p>St. Louis REALTORS&reg; reported a median single-family sale price of <strong>$340,000</strong> for September 2026, while the single-family median across the MIBOR area around Indianapolis was <strong>$320,000</strong>, according to our <a href="{_MARKET}">market update</a>. That&rsquo;s about $20,000 less in Indianapolis, or roughly $120 a month on a mortgage with 10% down at the current 7.24% rate (Freddie Mac, Oct. 29, 2026). Homes sold a little faster here too: a median of 27 days versus 31.</p>
 <p>The Census Bureau&rsquo;s 2025 survey, which asks owners what their homes are worth, points the other way: a median of $304,600 in the Indianapolis metro versus $283,300 in the St. Louis metro. Each REALTOR&reg; association reports on its own service area, and the Census counts every owner in the metro, so the honest read is that home prices are close. Renters will notice a gap: median gross rent is $1,380 in the Indianapolis metro versus $1,232 in St. Louis, about $150 a month more here. Central Indiana&rsquo;s fast-growing suburbs have a lot of newer construction, so many buyers trade up to a newer home at a similar price. Start with our <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> and <a href="/best/most-affordable-indianapolis-suburbs/">most affordable suburbs</a> rankings, see <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford</a>, or <a href="/search/">search live listings</a>.</p>

 <h2 id="taxes">Taxes: Income, Property and Vehicles</h2>
 <p><strong>Income tax.</strong> Missouri&rsquo;s top individual rate is 4.7% for 2026, and the City of St. Louis adds a 1% earnings tax on residents, wherever they work, and on nonresidents for work done in the city. On the Illinois side of the metro, the state rate is a flat 4.95%. Indiana&rsquo;s state rate is 2.95% on nearly all income, plus a county income tax based on where you live on January 1: 1.10% in Hamilton County, 1.40% in Johnson, 1.70% in Hendricks, 1.71% in Boone, 1.94% in Hancock and 2.02% in Marion County. Here&rsquo;s our rough math for a single filer with $100,000 in wages, at the top or flat rates and before exemptions, deductions and credits (Missouri&rsquo;s lower brackets on the first slice of income would bring its figures down a little):</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Where you live</th><th>State tax</th><th>Local tax</th><th>Total</th></tr></thead>
 <tbody>
{_TAX_ROWS}
 </tbody>
 </table>
 </div>
 <p>So if you live in the City of St. Louis now, almost anywhere around Indianapolis will lower your income tax. From St. Louis County, St. Charles County or the Illinois side, it&rsquo;s closer to a wash: you&rsquo;ll pay less in Hamilton or Johnson County and about the same in Hendricks or Marion County. In your move year, expect to file part-year returns.</p>
 <p><strong>Property tax.</strong> This is where Indianapolis comes out ahead. The median homeowner property tax bill was <strong>$2,596</strong> in the Indianapolis metro in 2025 versus <strong>$3,187</strong> in the St. Louis metro (Census ACS), about $600 a year less, even though Indianapolis home values ran a bit higher in that survey. The suburban gap is bigger: the median bill was $3,641 in St. Louis County and $3,836 in St. Charles County. Inside the city limits it&rsquo;s close, at $2,393 in Indianapolis versus $2,269 in St. Louis. Indiana&rsquo;s constitution caps property taxes on your primary home at 1% of its assessed value once you file the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a>. Bills still follow home values: Hamilton County&rsquo;s median was $4,356, but on homes with a median value of $483,600. Compare counties in our guide to <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>.</p>
 <p><strong>Your car.</strong> Missouri charges personal property tax every year on vehicles you own on January 1, assessed at one-third of their value, and you file a declaration with your county assessor. Indiana doesn&rsquo;t tax vehicles as personal property. Instead you pay a vehicle excise tax with your registration each year, based on the car&rsquo;s original price class and its age, plus a county excise or wheel tax in some counties. New residents have 60 days to title and register with the Indiana BMV. This is general information, not tax advice, so run your own numbers with a tax professional.</p>

 <h2 id="drive">The Drive and the Time Change</h2>
 <p>Indianapolis is about 244 miles east of St. Louis, almost all of it on I-70, roughly a four-hour drive. Plan for the clock: St. Louis is on Central time and Indianapolis is on Eastern, so you lose an hour heading east and gain it back driving home. I-70 comes into Indianapolis from the west through Plainfield, so if you&rsquo;ll be making regular trips back to Missouri, the west side and Hendricks County keep that drive shortest.</p>

 <h2 id="where-to-live">Where St. Louis Transplants Tend to Look</h2>
 <ul>
 <li><strong>If you liked an older, walkable suburb like Kirkwood or Webster Groves:</strong> tree-lined streets and older homes near a small downtown, like <a href="/neighborhoods/irvington-indianapolis/">Irvington</a>, <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a> and <a href="/neighborhoods/meridian-kessler-indianapolis/">Meridian-Kessler</a>, or <a href="/cities/boone-county/zionsville-indiana-real-estate/">Zionsville</a> with its brick-street village.</li>
 <li><strong>If you liked Soulard, Lafayette Square or Tower Grove:</strong> historic, close-in neighborhoods near downtown, like <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a> and <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>.</li>
 <li><strong>If you liked newer suburbs like Chesterfield, O&rsquo;Fallon or Wentzville:</strong> planned neighborhoods and new construction in <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a> and <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a>, where Hamilton County also has the metro&rsquo;s lowest county income tax, or <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a> and <a href="/cities/hendricks-county/brownsburg-indiana-real-estate/">Brownsburg</a> on the west side.</li>
 <li><strong>Close to I-70 for trips back to Missouri:</strong> <a href="/cities/hendricks-county/plainfield-indiana-real-estate/">Plainfield</a> and Avon in Hendricks County.</li>
 </ul>
 <p>Not sure which fits? Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro, and our honest look at <a href="/blog/living-in-indianapolis-pros-and-cons/">the pros and cons of living in Indianapolis</a> covers the trade-offs. Moving from somewhere else? See our <a href="/blog/moving-from-chicago-to-indianapolis/">Chicago</a>, <a href="/blog/moving-from-louisville-to-indianapolis/">Louisville</a>, <a href="/blog/moving-from-columbus-to-indianapolis/">Columbus</a> and <a href="/blog/moving-from-california-to-indianapolis/">California</a> guides.</p>

 <h2 id="checklist">Your Move Checklist</h2>
 <ul>
 <li>Title and register your vehicles and switch your driver&rsquo;s license with the Indiana BMV within 60 days.</li>
 <li>File your homestead deduction with the county auditor after you close.</li>
 <li>Check which county&rsquo;s income tax applies for your move year, and plan on part-year Missouri (or Illinois) returns, plus the St. Louis earnings tax if it applied to you.</li>
 <li>Set up utilities before move-in with our <a href="/utilities/">Central Indiana utilities guide</a>.</li>
 <li>Talk with us about <a href="/services/buyer-representation/">buyer representation</a>; a written buyer agreement sets out how your agent is paid, so you know the terms before you tour.</li>
 </ul>

 <h2 id="work-with-us">Talk to Our Team</h2>
 <p>Our team helps relocating buyers every month, including <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">live virtual tours</a> and buying before you arrive. Tell us what you have in St. Louis and what you want here, and we&rsquo;ll map out the areas that fit. Call <a href="tel:3179977404">317-997-7404</a> or <a href="/schedule/buyer-consultation/">book a buyer consultation</a>.</p>
""",
 faqs=[
  ("Is Indianapolis cheaper than St. Louis?",
   "Not overall. The Bureau of Economic Analysis puts 2024 price levels at 95.7 for the Indianapolis metro and 95.1 for St. Louis, and St. Louis is cheaper on rent and utilities. Indianapolis comes out ahead on property taxes, with a median homeowner bill of $2,596 versus $3,187 in 2025 (Census ACS), and on recent sale prices: the single-family median was $320,000 in the MIBOR area versus $340,000 for St. Louis REALTORS in September 2026."),
  ("How far is Indianapolis from St. Louis?",
   "About 244 miles, almost all of it on I-70, or roughly four hours by car. St. Louis is on Central time and Indianapolis is on Eastern time, so Indianapolis is an hour ahead."),
  ("Are income taxes higher in Indianapolis or St. Louis?",
   "It depends where you live now. Missouri's top rate is 4.7% for 2026 and the City of St. Louis adds a 1% earnings tax; the Illinois side of the metro pays a flat 4.95%. Indiana charges 2.95% plus a county tax from 1.10% in Hamilton County to 2.02% in Marion County. On $100,000 of wages, our rough math before exemptions is about $5,700 in the City of St. Louis, $4,700 in St. Louis County, $4,050 in Hamilton County and $4,970 in Marion County."),
  ("Are property taxes lower in Indianapolis than in St. Louis?",
   "Across the metro, yes. The median homeowner property tax bill was $2,596 in the Indianapolis metro in 2025 versus $3,187 in the St. Louis metro, and $3,641 in St. Louis County, according to the Census Bureau's American Community Survey. Inside the city limits the two are close. Indiana caps property taxes on a primary home at 1% of assessed value once you file the homestead deduction."),
  ("Do I pay personal property tax on my car in Indiana?",
   "Not a personal property tax like Missouri's. Indiana charges a vehicle excise tax with your registration each year, based on the vehicle's original price class and its age, and some counties add a county excise or wheel tax. New residents have 60 days to title and register their vehicles with the Indiana BMV."),
  ("Which Indianapolis suburbs feel most like Chesterfield or Kirkwood?",
   "Buyers who like newer, planned suburbs like Chesterfield or O'Fallon often look at Fishers and Westfield in Hamilton County, or Avon and Brownsburg in Hendricks County. If you preferred an older, walkable suburb like Kirkwood or Webster Groves, look at Irvington, Broad Ripple, Meridian-Kessler or Zionsville's village."),
 ],
 sources=[
  ("BEA Regional Price Parities by metro (2024)", "https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area"),
  ("St. Louis RPP via FRED", "https://fred.stlouisfed.org/series/RPPALL41180"),
  ("Census ACS 2025 median home value", _ACS + "B25077"),
  ("median gross rent", _ACS + "B25064"),
  ("median real estate taxes", _ACS + "B25103"),
  ("median household income", _ACS + "B19013"),
  ("St. Louis REALTORS&reg; Monthly Indicators, September 2026", "https://www.stlrealtors.com/clientuploads/New_Website_PDFs/Housing_Reports/2026/09_September/September_MonthlyHousingReport.pdf"),
  ("Indianapolis home prices: MIBOR REALTOR&reg; Association via our market update", _MARKET),
  ("Freddie Mac mortgage rates (Oct 29, 2026)", "https://www.freddiemac.com/pmms"),
  ("Missouri DOR Financial and Statistical Report (top income tax rate by year)", "https://dor.mo.gov/revenue-annual-financial-report/documents/financialstatreport25.pdf"),
  ("City of St. Louis earnings tax", "https://www.stlouis-mo.gov/collector/earnings-tax-home.cfm"),
  ("Illinois withholding tables, 2026 (4.95%)", "https://tax.illinois.gov/content/dam/soi/en/web/tax/forms/withholding/documents/currentyear/il-700-t.pdf"),
  ("Missouri personal property assessment, RSMo 137.115", "http://revisor.mo.gov/main/OneSection.aspx?section=137.115"),
  ("St. Louis County new-resident personal property declaration", "https://stlouiscountymo.gov/st-louis-county-government/county-assessor/personal-property/assessor-personal-property-forms/new-resident-declaration/"),
  ("Indiana BMV vehicle excise tax", "https://secure.in.gov/bmv/fees-taxes/vehicle-registration-fees-and-taxes/excise-tax-information/"),
  ("Indiana BMV, new residents", "https://secure.in.gov/bmv/licenses-permits-ids/new-indiana-residents"),
  ("Indiana DOR county tax rates (2026)", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("distance: OpenStreetMap routing", "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=38.6270%2C-90.1994%3B39.7684%2C-86.1581"),
 ],
 related=[
  ("/blog/moving-from-columbus-to-indianapolis/", "Moving from Columbus to Indianapolis"),
  ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
  ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
 ],
 cta=("Moving From St. Louis?",
      "Tell us what you have in St. Louis and what you want here, and we&rsquo;ll map out the areas that fit, including virtual tours if you&rsquo;re buying before you arrive.",
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
   '<strong>Coming from Missouri?</strong> See our <a href="/blog/moving-from-st-louis-to-indianapolis/">guide to moving from St. Louis to Indianapolis</a>, with cost of living, home prices and taxes compared side by side.'),
  ("blog/moving-from-louisville-to-indianapolis/index.html",
   'Moving from St. Louis instead? Our <a href="/blog/moving-from-st-louis-to-indianapolis/">St. Louis to Indianapolis guide</a> runs the same comparison, including the property tax gap and Missouri&rsquo;s car tax.'),
 ],
)
