"""New construction homes in Westfield, Indiana (46074): communities, builders and what to know (Nov 2026).
Per-suburb spoke off /new-construction-communities-indianapolis/ (GSC Nov 2026: "new communities in 46074"
25 impressions at pos 8.7; "new communities indianapolis/indiana" variants ~150 at pos 11-14; hub 336 at pos 11).

Every community below was verified on the BUILDER'S OWN WEBSITE on Nov 19 2026 (pages downloaded and read;
status + "from" price as shown that day). "From" prices are the lowest base/starting price on the builder site;
the post rounds them to "from the $XXXs".
- Lennar Westfield city page https://www.lennar.com/new-homes/indiana/indianapolis/westfield (embedded data, all
  status ACTIVE): East Street Towns townhomes basePrice 353,995 (page: "Actively selling", $353,995-$427,490, lawn
  maintenance w/ irrigation + snow removal, near Clay Terrace/downtown, Monon Trail Elementary);
  The Towns at Chatham townhomes 399,845 (page /the-towns-at-chatham: $399,845-$499,995, near a 12-acre lake,
  included Sport and Social Membership to The Club at Chatham Hills, 1593 Hamilton Ridge Rd);
  Winterburg single-family 532,995 (page: $532,995-$599,675, pool, playground, sport courts; badge "New Section");
  Ravinia master-planned single-family (page /ravinia: "Actively selling", $482,995-$855,995, pool, trails, sport
  courts, 16691 Breton Rd).
- Pulte: Finley Creek https://www.pulte.com/homes/indiana/indianapolis/westfield/finley-creek-211698 ($521,990+,
  single-family, full 9-ft basements, side-load garages, "5 Minutes to Grand Park", Westfield-Washington schools;
  community address 19320 Finley Creek Dr, Westfield IN 46069 and a listed home shows "Sheridan, IN 46069").
  Towns at Union https://www.pulte.com/homes/indiana/indianapolis/westfield/towns-at-union-211413 ($381,990+,
  3-story townhomes, S. Union Street, walk/bike to downtown + Grand Junction Plaza, Monon/Midland Trace trails).
- Del Webb: Kimblewick https://www.delwebb.com/homes/indiana/indianapolis/westfield/kimblewick-by-del-webb-210598
  ($439,990+, 55+, ranch homes, "Final Section Now Selling", 13,000 sq ft clubhouse, indoor + outdoor pools,
  4+ miles of trails, "146th and 151st Street and Close Proximity to US-31").
- Fischer Homes https://www.fischerhomes.com/new-homes/indiana/westfield/ : Townes at Grand Park Village
  ("Actively Selling", from $362,990, three-story townhomes w/ optional elevator, across from Grand Park, walking
  distance to the Monon, exterior maintenance/lawn/snow); Wood Wind Landing ("Actively Selling", from $746,990,
  fairway + water views, clubhouse w/ pool + pickleball, golf-cart friendly, first-year Eagle Social Membership
  to Wood Wind Golf Club, ~5 min to US-31 and Grand Park); Lindley Ridge at Chatham Hills ("Final Opportunity",
  from $1,348,990, access to The Club at Chatham Hills). Fischer also promotes financing through its preferred lender.
- Estridge https://www.estridgehomes.com/new-homes/in/westfield/midland/9349/ : Midland ("starting from the
  $400,000's"; The Towns from $399,000, The Terraces from $439,900, Crawford Collection from $514,900; single-family,
  townhomes, villas; resort-style pool + splash pad, pickleball, beer garden, dog park; homes on Ditch Road; site
  advertised "Up to $25,000* in Estridge Cash" and "Rates as low as 4.250%*" on select homes).
  Chatham Hills https://www.estridgehomes.com/new-homes/in/westfield/chatham-hills/14229/ ("homes starting from
  $1,000,000", The Chatham Gallery; Pete Dye 18-hole course, clubhouse w/ bowling, indoor/outdoor pools, Monon access).
- Drees (server-rendered pages show status but not prices): Carramore
  https://www.dreeshomes.com/new-homes-indianapolis/westfield-in/carramore/carramore/ (single-family, banner
  "Final Opportunity"); Belle Crest .../westfield-in/belle-crest/belle-crest/ (ranch and two-story townhomes, banner
  "Customize Your Home, New Pricing!"). No price given in the post for either.
DROPPED (not verifiable as selling on the builder's own site, Nov 19 2026): Pulte Westchester, Hawthorne Ridge,
Wood Wind and Lancaster (community URLs now redirect to Pulte's Westfield page); Lennar Westgate, New Haven,
Aberdeen and Osborne Trails (URLs redirect to Lennar's Indianapolis page; not in Lennar's Westfield list);
Olthof Lindley Run/Atwater (site is client-rendered, couldn't read status/price); Harmony, Viking Meadows and
other communities.json entries (established, no builder page found). Aggregator-only names (Homes.com, Zillow,
NewHomeSource) were not used.

Other facts (checked Nov 19 2026):
- Census: 2010 count 30,068 (SUB-EST2020_18.csv, CENSUS2010POP); 2020 count 46,410 (QuickFacts / city's
  special-census release); 2025 special census 64,407 on Sept 15 2025 (Census official counts, Indiana 2025);
  July 1 2025 estimate 66,258 (Vintage 2025, sub-est2025_18.csv). Growth math is ours (2020->2025 count +38.8%).
- Grand Park: "400+ acre campus", 26 diamonds (grandpark.org/about). Colts.com: 2026 was "the eighth and final
  summer of Colts Camp at Grand Park"; camp moves to the Indiana Farm Bureau Football Center in Indianapolis in 2027.
- District name "Westfield Washington Schools" (wws.k12.in.us).
- Indiana DOR Departmental Notice #1 (eff. Oct 1 2026): state 2.95%, Hamilton County 0.011.
- Assessment date Jan 1, taxes payable the next year (Indiana assessment fact sheet for the Jan 1 2026 date,
  payable 2027; IC 6-1.1-2-1.5). Partially built homes are assessed as they stand on Jan 1.
- Agent registration: Lennar broker policy (register at initial contact; broker must accompany the buyer on the
  first visit, in person or virtual; co-op commissions vary by community). M/I Homes Indianapolis agent page
  (agent should be present at the first visit; registration good for 30 days; pays on procuring cause).
Compliance: buyer agency never described as free; builder compensation "often/typically" and "varies"; BRA required.
"""

_LEN = "https://www.lennar.com/new-homes/indiana/indianapolis/westfield"
_FIS = "https://www.fischerhomes.com/new-homes/indiana/westfield/"
_EST = "https://www.estridgehomes.com/new-homes/in/westfield/"
_PUL = "https://www.pulte.com/homes/indiana/indianapolis/westfield/"
_DRE = "https://www.dreeshomes.com/new-homes-indianapolis/westfield-in/"

_ROWS = [
    # (community, builder, home type, from-price, notes)
    ("East Street Towns", "Lennar", "Townhomes", "From the $350s",
     "Lawn care, irrigation and snow removal included; near Clay Terrace and downtown"),
    ("Townes at Grand Park Village", "Fischer Homes", "Three-story townhomes", "From the $360s",
     "Across from Grand Park, walking distance to the Monon; optional elevator"),
    ("Towns at Union", "Pulte", "Three-story townhomes", "From the $380s",
     "On S. Union Street, walk or bike to downtown and Grand Junction Plaza"),
    ("The Towns at Chatham", "Lennar", "Townhomes", "From the high $390s",
     "Near a 12-acre lake; includes a Sport and Social Membership at The Club at Chatham Hills"),
    ("Belle Crest", "Drees Homes", "Ranch and two-story townhomes", "Not posted",
     "Ask the builder for current pricing"),
    ("Midland", "Estridge", "Single-family, townhomes, villas", "From the high $390s",
     "Along Ditch Road; resort-style pool, splash pad, pickleball, beer garden"),
    ("Ravinia", "Lennar", "Single-family", "From the $480s",
     "Master-planned; pool, trails, playground, basketball and pickleball courts"),
    ("Finley Creek", "Pulte", "Single-family", "From the $520s",
     "Full 9-foot basements, side-load garages; Sheridan 46069 mailing address"),
    ("Winterburg", "Lennar", "Single-family", "From the $530s",
     "New section; pool, playground and sport courts"),
    ("Carramore", "Drees Homes", "Single-family", "Not posted",
     "Builder lists it as a final opportunity"),
    ("Wood Wind Landing", "Fischer Homes", "Single-family", "From the $740s",
     "Fairway and water views, clubhouse and pool; first-year social membership at Wood Wind Golf Club"),
    ("Lindley Ridge at Chatham Hills", "Fischer Homes", "Single-family", "About $1.35 million",
     "Final opportunity; access to The Club at Chatham Hills"),
    ("Chatham Hills (The Chatham Gallery)", "Estridge", "Single-family", "From $1 million",
     "Pete Dye golf course, clubhouse with bowling, indoor and outdoor pools, Monon access"),
    ("Kimblewick by Del Webb", "Del Webb", "Ranch homes, 55+", "From the $430s",
     "Final section; 13,000 sq. ft. clubhouse; between 146th and 151st streets near US-31"),
]
_TABLE = "\n".join(f" <tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in _ROWS)

POST = dict(
 slug="new-construction-homes-westfield-indiana",
 title="New Construction Homes in Westfield, IN (46074): 2026",
 headline="New Construction Homes in Westfield, Indiana: Communities, Builders & What to Know",
 h1_html="New Construction Homes in Westfield, Indiana: <em>Communities, Builders &amp; What to Know</em>",
 crumb="New Construction Homes in Westfield",
 desc=("New construction homes in Westfield, Indiana (46074): the builder communities selling now, starting prices, "
       "schools, taxes and how to register your agent."),
 date="2026-11-19", month="November 2026",
 category="New Construction", eyebrow="NEW CONSTRUCTION",
 focus="new construction homes westfield indiana",
 hero_sub="The builder communities selling in Westfield right now, what they start at, and what to know about contracts, inspections, incentives and bringing your own agent.",
 badges=["New Construction", "Westfield 46074", "Updated November 2026"],
 read_min=8,
 card_title="New Construction Homes in Westfield",
 card_sub="Communities, builders and what to know before you tour a model.",
 qa_heading="Westfield New Construction at a Glance",
 qa_lead=("<strong>Where can you buy a new construction home in Westfield?</strong> As of November 2026 we confirmed 14 "
          "builder communities selling in Westfield on the builders&rsquo; own websites, from Lennar, Pulte, Del Webb, "
          "Fischer Homes, Estridge and Drees. Townhomes start in the $350s, single-family homes in the $480s, and homes at "
          "Chatham Hills start at $1 million or more. Base prices don&rsquo;t include lot premiums or options, and many "
          "builders want your agent registered on your very first visit."),
 qa_facts=[
  ("Population", "64,407 (Sept. 2025 special census), up from 46,410 in 2020"),
  ("Townhomes from", "The $350s (East Street Towns, Lennar, Nov. 2026)"),
  ("Single-family from", "The $480s (Ravinia, Lennar, Nov. 2026)"),
  ("55+ new construction", "Kimblewick by Del Webb, from the $430s (Nov. 2026)"),
  ("Public schools", "Westfield Washington Schools"),
  ("Local income tax (2026)", "Hamilton County 1.10%, plus Indiana&rsquo;s 2.95%"),
 ],
 toc=[("why-westfield", "Why Westfield Keeps Building"), ("communities", "Communities Selling Now"),
      ("prices", "What New Construction Costs"), ("schools-taxes", "Schools and Taxes"),
      ("buying-from-a-builder", "How Buying From a Builder Works"), ("your-agent", "Bringing Your Own Agent"),
      ("incentives", "Incentives and Preferred Lenders"), ("work-with-us", "Touring Westfield With Our Team")],
 body=f"""
 <p>If you&rsquo;re searching for new construction in Westfield, you&rsquo;ll find plenty of it, and a lot of it changes month to month. Sections sell out, new ones open, and prices move. So we went to each builder&rsquo;s own website in November 2026 and listed only the communities we could confirm are selling now, with the starting prices the builders post. Here&rsquo;s who&rsquo;s building, what homes start at, and what to know before you walk into your first model. For the wider metro, see our hub of <a href="/new-construction-communities-indianapolis/">new construction communities around Indianapolis</a>.</p>

 <h2 id="why-westfield">Why Westfield Keeps Building</h2>
 <p>Few Indiana cities have grown like Westfield. The Census Bureau counted <strong>30,068</strong> residents in 2010 and <strong>46,410</strong> in 2020. A special census on September 15, 2025 counted <strong>64,407</strong>, about 39% more than in 2020, and the Bureau&rsquo;s separate July 2025 estimate put the city at 66,258. In other words, the population has more than doubled since 2010, and new neighborhoods are how the city made room.</p>
 <p>Much of that story starts with <strong>Grand Park</strong>, the city&rsquo;s 400-plus-acre youth sports campus with 26 diamonds and dozens of fields. One change to know: 2026 was the eighth and final summer of Colts training camp at Grand Park, and the Colts say camp moves to the Indiana Farm Bureau Football Center in Indianapolis in 2027. The tournaments, trails and the US-31 corridor are what keep drawing buyers. Our <a href="/cities/hamilton-county/westfield-indiana-real-estate/">Westfield real estate guide</a> covers the city as a whole.</p>
 <p>A note on ZIP codes: most of Westfield is 46074, but some newer neighborhoods on the edges carry other mailing ZIPs. Pulte&rsquo;s Finley Creek, for example, is in Westfield and Westfield Washington Schools but uses a Sheridan 46069 mailing address. Search by city and school district, not ZIP alone.</p>

 <h2 id="communities">Westfield New Construction Communities Selling Now</h2>
 <p>Every community below showed homes for sale on its builder&rsquo;s own website on November 19, 2026. Prices are the lowest starting price the builder posted that day, rounded down, and will change.</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Community</th><th>Builder</th><th>Home type</th><th>Starting price*</th><th>Worth knowing</th></tr></thead>
 <tbody>
{_TABLE}
 </tbody>
 </table>
 </div>
 <p style="font-size:.88rem;color:var(--gray);">*Per each builder&rsquo;s website as of November 2026. Drees&rsquo; pages didn&rsquo;t show pricing. Base prices exclude lot premiums, options and upgrades.</p>
 <h3>Townhomes and low-maintenance living</h3>
 <p>If you want something new without the yard work, Westfield has more choices than most suburbs. Lennar&rsquo;s East Street Towns and Fischer&rsquo;s Townes at Grand Park Village both include lawn care and snow removal, and Townes at Grand Park Village sits across the street from Grand Park. Pulte&rsquo;s Towns at Union is the pick if you want to walk to downtown Westfield&rsquo;s restaurants and Grand Junction Plaza.</p>
 <h3>Single-family neighborhoods</h3>
 <p>Lennar&rsquo;s Ravinia and Winterburg, Estridge&rsquo;s Midland and Pulte&rsquo;s Finley Creek cover most of the middle of the market, from the $480s into the $500s and up. Midland mixes single-family homes, townhomes and villas around a pool, beer garden and event space, and Finley Creek includes a full 9-foot basement, which is not standard in every Westfield community.</p>
 <h3>Golf and luxury</h3>
 <p>Fischer&rsquo;s <a href="/communities/wood-wind-westfield/">Wood Wind Landing</a> starts in the $740s with fairway and water views near Wood Wind Golf Club. At <a href="/communities/chatham-hills-westfield/">Chatham Hills</a>, Estridge&rsquo;s homes start at $1 million and Fischer&rsquo;s final homes at Lindley Ridge start around $1.35 million, while Lennar&rsquo;s Towns at Chatham give townhome buyers a way into the same club.</p>
 <h3>55 and older</h3>
 <p>Del Webb&rsquo;s Kimblewick is in its final section, with ranch homes from the $430s, a 13,000-square-foot clubhouse and more than 4 miles of walking trails. Lennar&rsquo;s earlier 55+ neighborhood, <a href="/communities/osborne-trails-westfield/">Osborne Trails</a>, no longer appears among Lennar&rsquo;s Westfield communities, so homes there are now typically resales. Compare more options in our <a href="/55-plus-communities-indianapolis/">55+ communities guide</a>.</p>

 <h2 id="prices">What New Construction Costs in Westfield</h2>
 <p>Based on what the builders posted in November 2026, here&rsquo;s the rough ladder: townhomes from the $350s to the $400s, single-family homes from the $480s through the $500s and $700s, and Chatham Hills homes at $1 million and up. That lines up with the $300s-to-$600s range for Westfield as a whole in our city guide, with new builds sitting toward the middle and top of it.</p>
 <p>The starting price is rarely the final price. A <a href="/glossary/lot-premium/">lot premium</a> for a pond, wooded or walkout lot, structural options like a finished basement or third garage bay, and <a href="/glossary/upgrades-and-options/">design-center upgrades</a> can add tens of thousands of dollars. Ask each builder for a fully optioned price on the plan and lot you actually want, and compare it with similar resale homes on the <a href="/search/">live MLS search</a>. See <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford</a> before you fall for a model.</p>

 <h2 id="schools-taxes">Schools and Property Taxes</h2>
 <p><strong>Schools.</strong> Westfield is served by <a href="/schools/westfield-washington-schools/">Westfield Washington Schools</a>, and builders including Lennar, Pulte and Drees list their Westfield communities in the district. The district is growing with the city, so school assignments can change as new buildings open. Confirm the assigned schools for a specific address with the district before you sign.</p>
 <p><strong>Income tax.</strong> Westfield is in Hamilton County, where the county income tax is 1.10% for 2026, on top of Indiana&rsquo;s 2.95% state rate, according to the Indiana Department of Revenue. That&rsquo;s among the lowest county rates around Indianapolis.</p>
 <p><strong>Property tax on a new build.</strong> Indiana assesses property as of January 1 and bills the following year, and a home that was only partly built on January 1 is assessed as it stood. That means the first tax bill on a brand-new home is often based on the lot or an unfinished house, and the bill typically climbs once the finished home is assessed. Budget for the full amount, not the first bill, and ask your lender how your escrow will adjust. Once you move in, file the <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">Indiana homestead deduction</a> so your primary home gets the 1% property tax cap. Compare counties in our guide to <a href="/blog/indiana-property-tax-caps-explained/">Indiana property tax caps</a>. This is general information, not tax advice.</p>

 <h2 id="buying-from-a-builder">How Buying From a Builder Works</h2>
 <p><strong>The builder&rsquo;s contract.</strong> Most production builders use their own purchase agreement, not the forms used in resale. These contracts often set earnest money and design deposits that can be non-refundable, give the builder flexibility on the completion date, limit what you can change after certain deadlines, and send disputes to arbitration. Read it all before you sign, and have it reviewed. Our <a href="/services/builder-representation/">builder representation</a> page explains what we look for.</p>
 <p><strong>Who the sales agent works for.</strong> The friendly sales consultant in the model home represents the builder. Their job is to sell that builder&rsquo;s homes at that builder&rsquo;s prices, and they won&rsquo;t tell you that a resale down the street is a better value or that another community has a stronger incentive.</p>
 <h3>Inspections on a brand-new home</h3>
 <p>New doesn&rsquo;t mean perfect. Production homes are built fast by many different trades, and city inspections check code minimums, not workmanship. Many buyers hire their own <a href="/glossary/home-inspection/">home inspector</a> for a pre-drywall inspection (while the framing, wiring and plumbing are still visible), a final inspection before closing, and another check before the builder&rsquo;s first-year <a href="/glossary/builder-warranty/">warranty</a> ends. Ask up front whether the builder allows outside inspectors and when; most do, but some limit timing or access.</p>

 <h2 id="your-agent">Bringing Your Own Agent: Register on the First Visit</h2>
 <p>This is the step buyers most often miss. Policies vary, but builders typically require your agent to register you, or to come with you, on your very first visit to a community. Lennar&rsquo;s published policy, for example, says your agent must be registered at your first contact and must accompany you on your first visit, in person or virtual. M/I Homes tells Indianapolis agents to be there for the client&rsquo;s first visit. If you tour a model alone and give your name, you may not be able to add an agent later.</p>
 <p>How your agent is paid is set in writing up front. A written Buyer Representation Agreement is required before we tour homes with you, including model homes, and it spells out our compensation. Builders often pay the buyer&rsquo;s agent compensation, but it varies by builder and community (Lennar notes its co-op commissions vary by community), so we&rsquo;ll confirm the terms for each community before you commit. Learn more about <a href="/services/buyer-representation/">buyer representation</a> and how we approach <a href="/services/new-construction/">new construction</a>.</p>

 <h2 id="incentives">Builder Incentives and Preferred Lenders</h2>
 <p>Incentives are where new construction can beat resale. In November 2026, Estridge&rsquo;s site advertised up to $25,000 in &ldquo;Estridge Cash&rdquo; and rates as low as 4.25% on select Midland homes, with conditions. Other builders run similar offers on quick move-in homes, and Fischer, Lennar and others promote financing through their own preferred or affiliated lenders.</p>
 <p>The fine print matters. Incentives are usually tied to using the builder&rsquo;s lender, closing by a deadline, or a specific home. Get a <a href="/glossary/loan-estimate/">Loan Estimate</a> from the builder&rsquo;s lender and from at least one outside lender, and compare the total cost, not just the rate. Ask whether the credit can go toward closing costs, a rate buydown or upgrades, and which helps you most. Our <a href="/services/new-construction-negotiation/">new construction negotiation</a> page covers what&rsquo;s usually on the table.</p>

 <h2 id="work-with-us">Touring Westfield With Our Team</h2>
 <p>Westfield gives you more new construction choices than almost anywhere in Central Indiana, which also makes it easy to overpay or miss a better fit a mile away. Call us before your first model visit. We&rsquo;ll register with the builder, compare communities and incentives side by side, weigh them against resale, and review the contract with you. Comparing suburbs too? See <a href="/compare/westfield-vs-fishers/">Westfield vs. Fishers</a> and <a href="/compare/carmel-vs-westfield/">Carmel vs. Westfield</a>, or <a href="/schedule/buyer-consultation/">book a buyer consultation</a> or call <a href="tel:3179977404">317-997-7404</a>.</p>
""",
 faqs=[
  ("What new construction communities are in Westfield, Indiana?",
   "As of November 2026, builders' own websites showed homes for sale in Westfield communities including Ravinia, Winterburg, East Street Towns and The Towns at Chatham by Lennar; Finley Creek and Towns at Union by Pulte; Kimblewick by Del Webb (55+); Townes at Grand Park Village, Wood Wind Landing and Lindley Ridge at Chatham Hills by Fischer Homes; Midland and Chatham Hills by Estridge; and Carramore and Belle Crest by Drees Homes. Sections sell out and new ones open often, so check with the builder or our team for current availability."),
  ("How much do new construction homes cost in Westfield?",
   "Based on builder websites in November 2026, townhomes start in the $350s, single-family homes start in the $480s, Wood Wind Landing starts in the $740s, and homes at Chatham Hills start at $1 million or more. Those are base prices. Lot premiums, structural options and design upgrades can add tens of thousands of dollars."),
  ("Do I need my own agent to buy new construction in Westfield?",
   "You don't have to, but the builder's sales consultant represents the builder, not you. If you want your own agent, register them on your first visit, because many builders typically require it; Lennar's policy, for example, requires your agent to accompany you on your first visit. Builders often pay the buyer's agent compensation, but it varies by builder and community, and a written Buyer Representation Agreement is required before your agent tours with you."),
  ("Is there a 55+ new construction community in Westfield?",
   "Yes. Kimblewick by Del Webb was selling its final section in November 2026, with ranch homes starting in the $430s, a 13,000-square-foot clubhouse and more than 4 miles of trails, between 146th and 151st streets near US-31. Lennar's Osborne Trails no longer appears among Lennar's Westfield communities, so homes there are now typically resales."),
  ("What school district serves new homes in Westfield?",
   "Westfield Washington Schools. Builders including Lennar, Pulte and Drees list their Westfield communities in the district, and Pulte shows its Finley Creek community there even though homes carry a Sheridan 46069 mailing address. Because the district is growing, confirm the assigned schools for a specific address with the district before you sign."),
  ("Should I get a home inspection on a brand-new house?",
   "Yes. City inspections check code minimums, not workmanship. Many buyers hire their own inspector for a pre-drywall inspection, a final inspection before closing, and another check before the first-year builder warranty ends. Ask the builder when outside inspectors are allowed before you sign."),
 ],
 sources=[
  ("Census Bureau, 2025 special census counts (Indiana)", "https://www.census.gov/programs-surveys/specialcensus/data_products/official_counts/indiana/2025.html"),
  ("Census Vintage 2025 city estimates", "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/cities/totals/sub-est2025_18.csv"),
  ("2010 Census count", "https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/cities/SUB-EST2020_18.csv"),
  ("2020 Census count (QuickFacts)", "https://www.census.gov/quickfacts/fact/table/westfieldcityindiana/POP010220"),
  ("Grand Park", "https://www.grandpark.org/about"),
  ("Colts 2026 training camp", "https://www.colts.com/news/2026-indianapolis-colts-training-camp-schedule-dates-tickets-start-location-joint-practice"),
  ("Westfield Washington Schools", "https://www.wws.k12.in.us/"),
  ("Indiana DOR county tax rates (Oct. 2026)", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana assessment fact sheet (Jan. 1, 2026 assessment date)", "https://secure.in.gov/counties/parke/files/2026/Assessment-Fact-Sheet-v.f2.pdf"),
  ("Lennar Westfield communities", _LEN),
  ("Pulte Finley Creek", _PUL + "finley-creek-211698"),
  ("Pulte Towns at Union", _PUL + "towns-at-union-211413"),
  ("Del Webb Kimblewick", "https://www.delwebb.com/homes/indiana/indianapolis/westfield/kimblewick-by-del-webb-210598"),
  ("Fischer Homes Westfield", _FIS),
  ("Estridge Midland", _EST + "midland/9349/"),
  ("Estridge Chatham Hills", _EST + "chatham-hills/14229/"),
  ("Drees Carramore", _DRE + "carramore/carramore/"),
  ("Drees Belle Crest", _DRE + "belle-crest/belle-crest/"),
  ("Lennar broker policy", "https://resourcecenter.lennar.com/lennar-news/our-broker-real-estate-agent-policy/"),
  ("M/I Homes Indianapolis agent information", "https://www.mihomes.com/agent/indianapolis-metro/agent-info"),
  ("builder websites checked November 19, 2026", ""),
 ],
 related=[
  ("/blog/buying-new-construction-in-central-indiana-pros-and-cons/", "Buying New Construction: Pros and Cons"),
  ("/blog/new-construction-communities-indianapolis-suburbs/", "New Construction Communities in the Suburbs"),
  ("/blog/westfield-indiana-real-estate-home-of-grand-park/", "Westfield Real Estate: Home of Grand Park"),
 ],
 cta=("Touring Westfield Model Homes?",
      "Call us before your first visit. We&rsquo;ll register with the builder, compare communities and incentives side by side, and review the builder&rsquo;s contract with you.",
      [("/services/builder-representation/", "New Construction Representation →", "btn-white"),
       ("/schedule/buyer-consultation/", "Book a Buyer Consultation", "btn-outline")]),
 resources=[
  ("/new-construction-communities-indianapolis/", "New Construction Communities Near Indianapolis"),
  ("/services/new-construction/", "New Construction Guide"),
  ("/schools/westfield-washington-schools/", "Westfield Washington Schools"),
  ("/55-plus-communities-indianapolis/", "55+ Communities Near Indianapolis"),
 ],
 link_from=[
  ("new-construction-communities-indianapolis/index.html",
   '<strong>Shopping in Westfield?</strong> See our <a href="/blog/new-construction-homes-westfield-indiana/">guide to new construction homes in Westfield, Indiana</a>, with the builder communities selling there now, their starting prices and how to register your agent.'),
  ("cities/hamilton-county/westfield-indiana-real-estate/index.html",
   'Looking at a brand-new home? Our <a href="/blog/new-construction-homes-westfield-indiana/">Westfield new construction guide</a> lists the builder communities selling now, from townhomes near downtown to golf-course homes at Chatham Hills.'),
 ],
 about={"@type": "City", "name": "Westfield", "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
