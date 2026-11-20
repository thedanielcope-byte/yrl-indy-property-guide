"""Moving from New York to Indianapolis (Nov 2026). Move-guide series (Chicago, Cincinnati, Louisville
from build_move_guides.py; Columbus, California, Detroit, St. Louis from fresh_posts/); same sections
and framing.

WHY NEW YORK (picked from migration data, researched Nov 19 2026):
- Census ACS 2016-2020 metro-to-metro flows (metro-to-metro-2016-2020.xlsx, read directly; the most
  recent metro-to-metro release; the flows API now needs a key). Movers into Indianapolis-Carmel-Anderson
  (26900) by origin metro, people 1+ who lived there a year earlier: Chicago 7,637 +/-1,378; Louisville
  2,354 +/-666; Cincinnati 1,825 +/-767; New York-Newark-Jersey City 1,373 +/-520; Atlanta 1,082 +/-424;
  Fayetteville NC 973 +/-791; Miami 885 +/-580; Los Angeles 813 +/-354. (In-state metros and "abroad"
  rows skipped.) Chicago, Louisville, Cincinnati are covered, so New York is the top uncovered origin.
- Cross-check, IRS SOI county-to-county inflow files 2021-22, 2022-23, 2023-24 (countyinflowYYYY.csv,
  read directly), out-of-state origin counties aggregated to 2023 OMB metros (list1_2023.xlsx), into the
  11-county Indianapolis metro: New York is 3rd by returns in all three years (2023-24: Chicago 1,234
  returns / 1,934 people; Miami-Fort Lauderdale 939 / 1,772; New York 700 / 1,250). Marion + Hamilton
  only: same order (NY 582 returns / 1,040 people in 2023-24). Note: IRS ranks Miami above New York;
  ACS ranks New York above Miami (overlapping margins). New York is top-2 uncovered in both sources.

Every figure below is dated and sourced (researched Nov 19 2026):
- BEA Regional Price Parities 2024, metro file MARPP_MSA_2008_2024.csv, read directly. Indianapolis 26900
  vs New York-Newark-Jersey City 35620: all items 95.696 / 112.563; goods 94.318 / 110.261; housing
  88.917 / 148.616; utilities 86.358 / 127.018. (Indy figures match the other guides.)
- Census ACS 2025 1-year table-based summary files (acsdt1y2025-*.dat), read directly. Metro 26900 vs
  35620: B25077 value 304,600 / 691,700; B25064 rent 1,380 / 1,932; B25103 real estate taxes 2,596 /
  "10,000+" (top-coded: 10001, MOE -333333333; also top-coded for Nassau, Suffolk, Westchester, Bergen);
  B19013 income 83,815 / 102,139; B01003 population 2,204,583 / 20,112,448. NYC (3651000): value 810,700,
  rent 1,881, taxes 6,898, income 83,778. Indianapolis balance (1836003): taxes 2,393. NJ state taxes
  9,648. Hamilton County IN value 483,600, taxes 4,356. Mean commute = B08013_001 / B08303_001: Indy metro
  25.9, Indianapolis 25.1 (matches the living-in-Indy post), NY metro 36.8, NYC 40.8, U.S. 27.4.
  60+ minute commutes (B08303_012+013): Indy metro 5.1%, NY metro 21.7%. B08301 public transit share:
  Indy metro 0.6%, NY metro 28.2%, NYC 50.3%. B08201 no-vehicle households: Indy metro 6.4%, NY metro
  32.6%, NYC 58.9%. Value/income ratios are our math.
- OneKey MLS October 2026 release (Nov 17 2026): single-family median $775,000 (+4.7%), all types
  $700,000; covers Bronx, Dutchess, Manhattan, Nassau, Orange, Putnam, Queens, Rockland, Suffolk,
  Sullivan, Westchester (not Brooklyn, Staten Island or NJ).
- MIBOR October 2026 single-family (17-county region) via our November market update: median $310,000.
  NEWER than the $320,000 September figure the Oct-dated guides use. Freddie Mac PMMS 7.28% (Nov 19 2026,
  FRED MORTGAGE30US), newer than the 7.24% the other guides use. Payment math is ours (P&I, 10% down,
  30 years): $1,909 vs $4,772.
- NY Tax Law 601(c)(1)(vii), single, tax years beginning 2026: 3.90% to $8,500 ... 5.40% $13,900-$80,650,
  $4,191 + 5.90% over $80,650 to $215,400 ... 10.90% over $25M (NY Senate law text; brackets re-added and
  consistent). NYS DTF: 2026 state and Yonkers tables revised for rate cuts; "no legislative income tax
  rate changes" to NYC tables (bulletin Dec 12 2025). NYC single schedule from 2025 IT-201 instructions:
  3.078% / 3.762% / 3.819% / $1,813 + 3.876% over $50,000. Yonkers resident surcharge 16.75% of state tax
  (IT-201 instructions). NJ rate schedule (2020 and after): single $100k = 100,000 x .0637 - 2,126.25.
  Tax table math at $100,000 wages, before exemptions/deductions/credits: NY $5,333, NYC $3,751, NJ $4,244.
- NYS DTF TSB-M-06(5)I (May 15 2006): convenience of the employer test; bona fide employer office
  exception. Form IT-203 = nonresident and part-year resident return.
- NYS transfer tax $2 per $500, paid by grantor (tax.ny.gov). NYC RPTT residential 1% at $500,000 or
  less, 1.425% above (NYC Finance / NYC311).
- NY DMV: surrender NY plates before NY liability insurance is canceled, or registration (and possibly
  license) can be suspended. Indiana BMV: 60 days for license and for title/registration; surrender
  out-of-state credentials; vision screening; VIN inspection.
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026): 2.95% state for 2026; Marion 2.02, Hamilton 1.10,
  Johnson 1.40, Hendricks 1.70. DLGF circuit-breaker fact sheet: 1% homestead, 2% other residential, 3%
  nonresidential.
- NOAA 1991-2020 normals (NCEI API): Central Park USW00094728 Jan avg 33.7F, July high 84.9F, snow 29.8 in;
  Indianapolis USW00093819 Jan avg 28.5F, July high 85.2F, snow 25.5 in.
- Walk Score: New York 88, Indianapolis 31. IndyGo: Blue Line (third BRT line, airport to Cumberland via
  downtown) opens late 2028. ind.com/flights (Nov 19 2026): nonstops to JFK, LGA, EWR.
- Distance: OpenStreetMap routing (OSRM), City Hall to Monument Circle, 709.3 miles via I-78, I-81, I-76, I-70.
No crime/safety content, no political framing. New York suburbs are described only by feel.
"""

_ACS = "https://data.census.gov/table/ACSDT1Y2025."
_MARKET = "/blog/indianapolis-market-update-november-2026/"

_GLANCE = [
    ("Overall price level (BEA, 2024; U.S. = 100)", "95.7", "112.6"),
    ("Goods price level (BEA, 2024)", "94.3", "110.3"),
    ("Housing price level (BEA, 2024)", "88.9", "148.6"),
    ("Utilities price level (BEA, 2024)", "86.4", "127.0"),
    ("Median sale price, single-family (Oct 2026)", "$310,000 (MIBOR area)", "$775,000 (OneKey MLS area)"),
    ("Median home value, metro (Census ACS 2025, owner estimates)", "$304,600", "$691,700"),
    ("Median gross rent, metro (ACS 2025)", "$1,380", "$1,932"),
    ("Median homeowner property tax bill, metro (ACS 2025)", "$2,596", "$10,000 or more"),
    ("Median household income, metro (ACS 2025)", "$83,815", "$102,139"),
    ("Average one-way commute, metro (ACS 2025)", "25.9 minutes", "36.8 minutes"),
    ("Workers who commute by public transit (ACS 2025)", "0.6%", "28.2%"),
    ("Income tax (2026)", "Indiana 2.95% + county tax (1.10%&ndash;2.02% in the core counties)", "New York 3.9%&ndash;10.9%, + 3.078%&ndash;3.876% in NYC; New Jersey 1.4%&ndash;10.75%"),
    ("Metro population (ACS 2025)", "About 2.2 million", "About 20.1 million"),
    ("Time zone", "Eastern", "Eastern"),
]
_GLANCE_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in _GLANCE)

_TAX = [
    ("New York City", "$5,330", "$3,750 (city)", "about $9,080"),
    ("Long Island or Westchester (outside Yonkers)", "$5,330", "none", "about $5,330"),
    ("New Jersey suburbs", "$4,240", "none", "about $4,240"),
    ("Indianapolis (Marion County)", "$2,950", "$2,020", "about $4,970"),
    ("Avon or Plainfield (Hendricks County)", "$2,950", "$1,700", "about $4,650"),
    ("Greenwood (Johnson County)", "$2,950", "$1,400", "about $4,350"),
    ("Carmel or Fishers (Hamilton County)", "$2,950", "$1,100", "about $4,050"),
]
_TAX_ROWS = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in _TAX)

POST = dict(
 slug="moving-from-new-york-to-indianapolis",
 title="Moving from New York to Indianapolis: 2026 Guide",
 headline="Moving from New York to Indianapolis: Costs, Taxes & Where to Live",
 h1_html="Moving from New York to Indianapolis: <em>Costs, Taxes &amp; Where to Live</em>",
 crumb="Moving from New York to Indianapolis",
 desc=("Moving from New York to Indianapolis? Compare home prices, rent, income and property taxes, "
       "commutes and weather with 2026 data, plus where to look."),
 date="2026-11-19", month="November 2026",
 category="Relocation", eyebrow="RELOCATION",
 focus="moving from new york to indianapolis",
 hero_sub="How home prices, rent, taxes, commutes and weather really compare, what changes when you trade the subway for a car, and where New Yorkers tend to buy.",
 badges=["Relocation", "New York to Indy", "Updated for 2026"],
 read_min=9,
 card_title="Moving from New York to Indy",
 card_sub="Home prices, rent, taxes and where to live, compared.",
 qa_heading="New York vs. Indianapolis at a Glance",
 qa_lead=("<strong>Is Indianapolis cheaper than New York?</strong> Yes, by a wide margin. The BEA puts everyday prices "
          "about 15% lower in the Indianapolis metro than in metro New York (95.7 vs. 112.6, where the U.S. is 100), and "
          "housing about 40% lower. In October 2026, single-family homes sold for a median $310,000 in the MIBOR area "
          "around Indianapolis versus $775,000 across OneKey MLS&rsquo;s New York counties. The trade-offs: you&rsquo;ll "
          "almost certainly need a car, and January runs about five degrees colder."),
 qa_facts=[
  ("Overall price level (2024)", "Indy 95.7 &middot; NY metro 112.6"),
  ("Median single-family sale price (Oct 2026)", "Indy $310,000 &middot; NY $775,000"),
  ("Median rent, metro (2025)", "Indy $1,380 &middot; NY $1,932"),
  ("Median property tax bill (2025)", "Indy $2,596 &middot; NY metro $10,000+"),
  ("Income tax (2026)", "IN 2.95% + county &middot; NY 3.9%&ndash;10.9% (+NYC 3.078%&ndash;3.876%)"),
  ("Getting back", "About 710 miles; nonstops to JFK, LGA and EWR"),
 ],
 toc=[("at-a-glance", "Indianapolis vs. New York at a Glance"), ("cost-of-living", "Cost of Living"),
      ("home-prices", "Home Prices, Payments and Rent"), ("taxes", "Taxes: Income, Property and Selling"),
      ("new-york-job", "Keeping a New York Job"), ("commute", "Commutes, Transit and Your Car"),
      ("weather-and-travel", "Weather, the Drive and Flights"), ("where-to-live", "Where New Yorkers Look"),
      ("checklist", "Your Move Checklist"), ("work-with-us", "Talk to Our Team")],
 body=f"""
 <p>New York is one of the biggest sources of new Indianapolis residents from outside Indiana. Census Bureau estimates for 2016&ndash;2020 put the flow at roughly 1,400 people a year from the New York metro to the Indianapolis metro, the fourth-largest from any metro area outside the state after Chicago, Louisville and Cincinnati. IRS migration data, which is based on tax returns, ranks the New York metro third among out-of-state sources in each of the three most recent years, with about 700 returns and 1,250 people moving in 2023&ndash;24. Most of the New Yorkers we talk to want more space, a lower monthly payment or to be near family, and plenty keep their New York job. Here&rsquo;s how the costs actually compare, what changes day to day, and where to start looking.</p>

 <h2 id="at-a-glance">Indianapolis vs. New York at a Glance</h2>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th></th><th>Indianapolis</th><th>New York</th></tr></thead>
 <tbody>
{_GLANCE_ROWS}
 </tbody>
 </table>
 </div>
 <p style="font-size:.85rem;color:var(--gray);">Metro figures are for each metropolitan area as the Census Bureau and BEA define it; the New York metro includes northern New Jersey. Home values are what owners estimate their homes are worth, and rent is what all renters pay, including long-term leases. The Census Bureau reports metro New York&rsquo;s median property tax bill only as &ldquo;$10,000 or more,&rdquo; the top of its range.</p>

 <h2 id="cost-of-living">Cost of Living: What the Federal Data Shows</h2>
 <p>The Bureau of Economic Analysis measures how expensive each metro is compared with the national average. In 2024 the Indianapolis metro scored <strong>95.7</strong> and metro New York <strong>112.6</strong>, so overall prices run about 15% lower here. Every major category points the same way: goods (94.3 vs. 110.3), utilities (86.4 vs. 127.0) and, by far the biggest gap, housing (88.9 vs. 148.6), about 40% lower.</p>
 <p>Incomes are lower too, and that&rsquo;s the honest other half. The median household earned $83,815 in the Indianapolis metro in 2025 versus $102,139 in metro New York (Census ACS). Inside New York City, though, the median was $83,778, almost exactly the same as here. Home values fall much further than incomes: the typical home is worth about 3.6 times the median household income in the Indianapolis metro, compared with about 6.8 times in metro New York and 9.7 times in New York City (our math from the same Census tables). If you keep a New York salary, that gap goes a very long way. For a line-by-line look at rent, utilities and taxes, see our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a>. To see what a New York salary is worth in Indianapolis, try our <a href="/cost-of-living-calculator-indianapolis/">Indianapolis cost of living calculator</a>.</p>

 <h2 id="home-prices">Home Prices, Payments and Rent</h2>
 <p>In October 2026, the median single-family home sold for <strong>$310,000</strong> across the 17-county MIBOR region around Indianapolis, according to our <a href="{_MARKET}">November market update</a>. OneKey MLS reported a single-family median of <strong>$775,000</strong> for the same month across the 11 New York counties it covers, including Manhattan, Queens, the Bronx, Nassau, Suffolk and Westchester (Brooklyn, Staten Island and New Jersey aren&rsquo;t in its figures). The Census Bureau&rsquo;s 2025 survey shows the same pattern: a median home value of $304,600 in the Indianapolis metro, $691,700 in metro New York and $810,700 in New York City.</p>
 <p>Here&rsquo;s what that means for a monthly payment. At the 7.28% average 30-year rate Freddie Mac reported on November 19, 2026, with 10% down, principal and interest come to about <strong>$1,909 a month</strong> on a $310,000 home versus about <strong>$4,772</strong> on a $775,000 home, a difference of roughly $2,860 a month (our math, before taxes and insurance). That&rsquo;s why many New Yorkers we work with buy a newer or larger home here, or keep part of their equity in the bank.</p>
 <p>Renters will notice a smaller but real gap: median gross rent is $1,380 in the Indianapolis metro versus $1,932 in metro New York, about $550 a month less. To see what your budget buys, use our <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house can I afford</a> guide, browse our <a href="/best/indianapolis-suburbs-for-families/">best suburbs for families</a> and <a href="/best/most-affordable-indianapolis-suburbs/">most affordable suburbs</a> rankings, or <a href="/search/">search live listings</a>.</p>

 <h2 id="taxes">Taxes: Income, Property and Selling</h2>
 <p><strong>Income tax.</strong> New York&rsquo;s 2026 rates run from 3.9% to 10.9%; for single filers, the 5.9% rate covers taxable income from $80,650 to $215,400 (New York Tax Law). New York City adds its own resident income tax of 3.078% to 3.876%, and Yonkers residents pay a surcharge equal to 16.75% of their state tax (NYS Department of Taxation and Finance). New Jersey&rsquo;s rates run from 1.4% to 10.75%. Indiana&rsquo;s state rate is 2.95% on nearly all income for 2026, plus a county income tax based on where you live on January 1: 1.10% in Hamilton County, 1.40% in Johnson, 1.70% in Hendricks and 2.02% in Marion County (Indiana DOR). Here&rsquo;s our rough math for a single filer with $100,000 in wages, before exemptions, deductions and credits:</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Where you live</th><th>State tax</th><th>Local tax</th><th>Total</th></tr></thead>
 <tbody>
{_TAX_ROWS}
 </tbody>
 </table>
 </div>
 <p>So leaving New York City cuts income tax roughly in half almost anywhere around Indianapolis. From Long Island or Westchester, every county here still comes out lower. From New Jersey, it&rsquo;s closer to a wash at this income: a little lower in Hamilton County, about the same in Johnson County and several hundred dollars higher in Hendricks or Marion County, though New Jersey&rsquo;s 6.37% rate above $75,000 means higher earners save more by moving. In your move year, expect part-year resident returns in both states.</p>
 <p><strong>Property tax.</strong> This is one of the biggest monthly differences. The Census Bureau&rsquo;s 2025 survey reports the median homeowner property tax bill in metro New York only as &ldquo;$10,000 or more,&rdquo; and the same is true in Nassau, Suffolk, Westchester and Bergen counties. Inside New York City the median was $6,898, and statewide in New Jersey $9,648. In the Indianapolis metro it was <strong>$2,596</strong>, and $2,393 in the city of Indianapolis. Indiana&rsquo;s constitution caps property taxes at 1% of assessed value on your primary home once you file the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a>, 2% on other residential property such as a rental or second home, and 3% on commercial property (Indiana DLGF). Bills still follow home values: Hamilton County&rsquo;s median was $4,356, on homes with a median value of $483,600. Compare counties in our guide to <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county around Indianapolis</a>.</p>
 <p><strong>Selling in New York.</strong> Budget for transfer taxes when you sell. New York State charges $2 for every $500 of the sale price (0.4%), paid by the seller, and inside the city the NYC Real Property Transfer Tax adds 1% on homes of $500,000 or less and 1.425% above that. This is general information, not tax advice, so run your own numbers with a tax professional.</p>

 <h2 id="new-york-job">Keeping a New York Job</h2>
 <p>Plenty of our New York clients keep working for a New York employer after they move, and the tax rules here are different from most states. If your assigned office is in New York and you work from home in Indiana by choice, New York&rsquo;s &ldquo;convenience of the employer&rdquo; test generally treats those days as New York workdays, so New York can still tax that pay. The main exception is a home office that qualifies as a bona fide employer office under the factors the Tax Department lays out (NYS DTF memo TSB-M-06(5)I). New York City&rsquo;s income tax applies only to city residents, so that part ends when you move. In the year you move, you&rsquo;ll generally file New York&rsquo;s nonresident and part-year resident return (Form IT-203) along with your Indiana return. How the two states&rsquo; credits work out depends on your situation, so have a tax professional review your plan before you move.</p>

 <h2 id="commute">Commutes, Transit and Your Car</h2>
 <p>This is the biggest day-to-day change. In metro New York, 28.2% of workers commute by public transit (50.3% inside the city), and 58.9% of New York City households don&rsquo;t have a vehicle. In the Indianapolis metro, 0.6% of workers take transit and only 6.4% of households go without a vehicle (Census ACS, 2025). Walk Score rates New York City 88 out of 100 and Indianapolis 31.</p>
 <p>The upside is time. The average one-way commute is 25.9 minutes in the Indianapolis metro versus 36.8 minutes in metro New York and 40.8 in the city, and 5.1% of Indianapolis-area commuters spend an hour or more getting to work, compared with 21.7% around New York (Census ACS, 2025). Transit is growing: IndyGo runs the Red and Purple bus rapid transit lines and is building a third, the Blue Line, from the airport through downtown to Cumberland, scheduled to open in late 2028. If going car-light matters to you, the most walkable options are the neighborhoods closest to downtown.</p>

 <h2 id="weather-and-travel">Weather, the Drive and Flights</h2>
 <p>Indianapolis winters run a little colder than New York&rsquo;s, with a little less snow: January averages 28.5&deg;F here versus 33.7&deg;F in Central Park, and the area gets about 25.5 inches of snow a year versus 29.8 inches in Central Park (NOAA 1991&ndash;2020 normals). Summers are a near match, with July highs around 85&deg;F in both. Indianapolis is about 710 miles from Manhattan by car, mostly on I-78, the Pennsylvania Turnpike and I-70, so plan on a full day of driving or two easier days. Both cities are on Eastern time, so your calendar doesn&rsquo;t change. For trips back, Indianapolis International Airport has nonstop flights to JFK, LaGuardia and Newark (airport flight list, November 2026).</p>

 <h2 id="where-to-live">Where New Yorkers Tend to Look</h2>
 <ul>
 <li><strong>If you&rsquo;re used to walking everywhere:</strong> historic districts next to downtown, like <a href="/neighborhoods/lockerbie-square-indianapolis/">Lockerbie Square</a> with its cobblestone streets and restored cottages, <a href="/neighborhoods/fletcher-place-indianapolis/">Fletcher Place</a> with cottages and rowhomes, <a href="/neighborhoods/chatham-arch-indianapolis/">Chatham Arch</a> and the lofts and condos of <a href="/neighborhoods/mass-ave-indianapolis/">Mass Ave</a>, or the restored Victorians of the <a href="/neighborhoods/old-northside-indianapolis/">Old Northside</a> and <a href="/neighborhoods/herron-morton-place-indianapolis/">Herron-Morton Place</a>.</li>
 <li><strong>If you want a neighborhood with its own restaurant strip:</strong> <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>, <a href="/neighborhoods/fountain-square-indianapolis/">Fountain Square</a> and tree-lined <a href="/neighborhoods/meridian-kessler-indianapolis/">Meridian-Kessler</a>.</li>
 <li><strong>If you liked a village downtown on Long Island or in Westchester:</strong> <a href="/cities/boone-county/zionsville-indiana-real-estate/">Zionsville</a>&rsquo;s brick Main Street, <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a>&rsquo;s Arts &amp; Design District and the Monon Trail, or the Nickel Plate District in <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a>.</li>
 <li><strong>If you want a newer home and a bigger yard:</strong> Carmel, Fishers and <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield</a> in Hamilton County, which also has the metro&rsquo;s lowest county income tax, or <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a> on the south side for more value.</li>
 <li><strong>If you&rsquo;ll miss the water:</strong> Central Indiana has no ocean, but <a href="/blog/geist-reservoir-waterfront-homes-near-indianapolis/">Geist Reservoir</a> on the northeast side has waterfront neighborhoods.</li>
 </ul>
 <p>Not sure which fits? Our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a> walks through the whole metro, and our honest look at <a href="/blog/living-in-indianapolis-pros-and-cons/">the pros and cons of living in Indianapolis</a> covers the trade-offs. Moving from somewhere else? See our <a href="/blog/moving-from-california-to-indianapolis/">California</a>, <a href="/blog/moving-from-chicago-to-indianapolis/">Chicago</a> and <a href="/blog/moving-from-columbus-to-indianapolis/">Columbus</a> guides.</p>

 <h2 id="checklist">Your Move Checklist</h2>
 <ul>
 <li>Get your Indiana driver&rsquo;s license within 60 days. You&rsquo;ll surrender your New York license and pass a vision screening (Indiana BMV).</li>
 <li>Title and register your vehicles with the Indiana BMV within 60 days; you&rsquo;ll need a VIN inspection, usually done at the branch.</li>
 <li>Don&rsquo;t cancel your New York auto insurance until you&rsquo;ve surrendered your New York plates. NY DMV can suspend your registration, and possibly your license, if coverage lapses first.</li>
 <li>File your <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead deduction</a> with the county auditor after you close.</li>
 <li>Plan on a part-year New York return (and New Jersey, if that&rsquo;s where you lived), and check which Indiana county&rsquo;s income tax applies.</li>
 <li>Set up utilities before move-in with our <a href="/utilities/">Central Indiana utilities guide</a>, and work through the rest of our <a href="/blog/moving-to-indiana-checklist/">moving to Indiana checklist</a>.</li>
 <li>Talk with us about <a href="/services/buyer-representation/">buyer representation</a>; a written buyer agreement sets out how your agent is paid, so you know the terms before you tour.</li>
 </ul>

 <h2 id="work-with-us">Talk to Our Team</h2>
 <p>Our team helps relocating buyers every month, including <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">live virtual tours</a> and buying before you arrive. Tell us what you have in New York and what you want here, and we&rsquo;ll map out the areas that fit. Call <a href="tel:3179977404">317-997-7404</a> or <a href="/schedule/buyer-consultation/">book a buyer consultation</a>.</p>
""",
 faqs=[
  ("Is Indianapolis cheaper than New York?",
   "Yes, by a wide margin. The Bureau of Economic Analysis puts 2024 price levels at 95.7 for the Indianapolis metro and 112.6 for metro New York, about 15% lower overall, with housing about 40% lower. In October 2026 the median single-family home sold for $310,000 in the MIBOR area around Indianapolis versus $775,000 across OneKey MLS's New York counties, and median rent is $1,380 versus $1,932 (Census ACS, 2025)."),
  ("How much lower are property taxes in Indianapolis than in New York?",
   "Much lower. The median homeowner property tax bill was $2,596 in the Indianapolis metro in 2025, while the Census Bureau reports metro New York's median only as $10,000 or more. Inside New York City the median was $6,898. Indiana caps property taxes on a primary home at 1% of assessed value once you file the homestead deduction."),
  ("Will I pay less income tax in Indiana than in New York?",
   "In most cases, yes. Indiana charges 2.95% plus a county tax from 1.10% in Hamilton County to 2.02% in Marion County. New York's 2026 rates run from 3.9% to 10.9%, and New York City adds 3.078% to 3.876%. On $100,000 of wages, our rough math before exemptions is about $9,080 in New York City, $5,330 elsewhere in New York State, $4,050 in Hamilton County and $4,970 in Marion County. Check your numbers with a tax professional."),
  ("Do I still owe New York tax if I keep my New York job and work remotely from Indiana?",
   "Possibly. Under New York's convenience of the employer test, days you work from home outside New York by choice are generally treated as New York workdays if your assigned office is in New York, unless your home office qualifies as a bona fide employer office. New York City income tax applies only to city residents. Have a tax professional review your situation before you move."),
  ("Do I need a car in Indianapolis?",
   "Almost certainly. Only 0.6% of Indianapolis-area workers commute by public transit and 6.4% of households have no vehicle, compared with 58.9% of New York City households (Census ACS, 2025). Commutes are shorter, though: 25.9 minutes on average in the Indianapolis metro versus 36.8 in metro New York."),
  ("How far is Indianapolis from New York City?",
   "About 710 miles by car, mostly on I-78, the Pennsylvania Turnpike and I-70, or a full day of driving. Both cities are on Eastern time, and Indianapolis International Airport has nonstop flights to JFK, LaGuardia and Newark."),
 ],
 sources=[
  ("Census ACS 2016&ndash;2020 metro-to-metro migration flows", "https://www.census.gov/data/tables/2020/demo/geographic-mobility/metro-to-metro-migration.html"),
  ("IRS SOI county-to-county migration data (2021&ndash;2024)", "https://www.irs.gov/statistics/soi-tax-stats-migration-data"),
  ("BEA Regional Price Parities by metro (2024)", "https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area"),
  ("New York RPP via FRED", "https://fred.stlouisfed.org/series/RPPALL35620"),
  ("Census ACS 2025 median home value", _ACS + "B25077"),
  ("median gross rent", _ACS + "B25064"),
  ("median real estate taxes", _ACS + "B25103"),
  ("median household income", _ACS + "B19013"),
  ("commute time", _ACS + "B08303"),
  ("means of transportation to work", _ACS + "B08301"),
  ("vehicles available", _ACS + "B08201"),
  ("OneKey&reg; MLS October 2026 market data (Nov 17, 2026)", "https://corporate.onekeymls.com/news/m34hkzw439atucqdn2kgtkr0l19sge"),
  ("Indianapolis home prices: MIBOR REALTOR&reg; Association via our market update", _MARKET),
  ("Freddie Mac 30-year rate (Nov 19, 2026)", "https://fred.stlouisfed.org/series/MORTGAGE30US"),
  ("New York Tax Law &sect;601 (2026 rate schedules)", "https://www.nysenate.gov/legislation/laws/TAX/601"),
  ("NYS DTF withholding rate changes (2026)", "https://www.tax.ny.gov/bus/wt/rate.htm"),
  ("NYS DTF IT-201 instructions (New York City rates, Yonkers surcharge)", "https://www.tax.ny.gov/pdf/current_forms/it/it201i.pdf"),
  ("NYS DTF TSB-M-06(5)I, convenience of the employer", "https://www.tax.ny.gov/pdf/memos/income/m06_5i.pdf"),
  ("New Jersey tax rate schedules", "https://www.nj.gov/treasury/taxation/pdf/current/njtaxratesch.pdf"),
  ("NYS real estate transfer tax", "https://www.tax.ny.gov/bus/transfer/rptidx.htm"),
  ("NYC Real Property Transfer Tax", "https://www.nyc.gov/site/finance/property/property-real-property-transfer-tax-rptt.page"),
  ("NY DMV, moving to or from New York", "https://dmv.ny.gov/more-info/moving-to-or-from-new-york-state"),
  ("Indiana DOR county tax rates (2026)", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("Indiana BMV, new residents", "https://secure.in.gov/bmv/licenses-permits-ids/new-indiana-residents"),
  ("NOAA U.S. climate normals (1991&ndash;2020)", "https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals"),
  ("Walk Score: New York", "https://www.walkscore.com/NY/New_York"),
  ("Indianapolis", "https://www.walkscore.com/IN/Indianapolis"),
  ("IndyGo Blue Line", "https://www.indygo.net/blue-line/"),
  ("Indianapolis International Airport flights", "https://www.ind.com/flights"),
  ("distance: OpenStreetMap routing", "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=40.7128%2C-74.0060%3B39.7684%2C-86.1581"),
  ("General information, not tax advice", ""),
 ],
 related=[
  ("/blog/moving-from-california-to-indianapolis/", "Moving from California to Indianapolis"),
  ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
  ("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
 ],
 cta=("Moving From New York?",
      "Tell us what you have in New York and what you want here, and we&rsquo;ll map out the areas that fit, including virtual tours if you&rsquo;re buying before you arrive.",
      [("/services/relocation-buyers/", "Explore Relocation Services →", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[
  ("/services/relocation-buyers/", "Relocation Buyers"),
  ("/blog/moving-to-indiana-checklist/", "Moving to Indiana Checklist"),
  ("/blog/indiana-property-tax-caps-explained/", "Indiana Property Tax Caps Explained"),
  ("/blog/relocating-to-indianapolis-virtual-home-tours/", "Buying With Virtual Home Tours"),
 ],
 link_from=[
  ("blog/living-in-indianapolis-pros-and-cons/index.html",
   'Weighing a move from New York? See how home prices, taxes and commutes compare in our <a href="/blog/moving-from-new-york-to-indianapolis/">New York to Indianapolis guide</a>.'),
 ],
 about={"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
