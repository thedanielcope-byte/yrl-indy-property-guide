"""MIBOR listings: what MIBOR and the BLC MLS are, and how to search Central Indiana homes (Nov 2026).

Why this post: GSC (Nov 2026) shows /glossary/mibor/ at 900 impressions, position 8, 0 clicks;
"mibor listings" 114 impressions at 6.3; "mibor property search" 69 at 6.6; also "mibor homes for
sale" and "mibor mls".

Facts and sources (checked Nov 19 2026):
- Name: MIBOR REALTOR(R) Association (mibor.com title + About page). About page: MIBOR staff manage
  BLC(R) services; Board is REALTORS from across central Indiana. No county list on mibor.com.
- Size/founding: MIBOR boilerplate in its Aug 2026 release with the Indianapolis MPO: founded in
  1912, serves more than 10,000 REALTORS and real estate professionals throughout central Indiana.
- 17 counties: "About MIBOR Broker Listing Cooperative" boilerplate in the BLC/Gitcha release
  (EIN Presswire, Apr 28 2026; read via the RCN America Indiana reprint, original EIN page not
  found). It says the BLC provides listing services to subscribers in 17 counties across central
  Indiana and is owned by MIBOR REALTOR Association. The CubiCasa/BLC release reportedly says the
  same (403, not read). Counties are NOT named in the post: no official list found (third-party
  lists disagree: 11, 13, 17).
- BLC page (mibor.com/join-mibor/broker-listings-cooperative/): BLC is described as the member's
  multiple listing service (quoted once in the body); name reflects cooperation between listing and selling broker; Data License requires
  being a BLC Participant. Eligibility rules for subscribing are not stated there, so the post
  uses NAR's MLS policy for "who can log in".
- MIBOR "Comprehensive Listings" page: REALTORS keep BLC listings up to date incl. price changes
  and contract status; the BLC includes access to properties that may not be listed on public sites.
- MIBOR Buyers & Sellers page: a free real estate listing tool, search by general location or
  specific address, save favorite homes and share them; links to property.mibor.com ("Find a
  Home" menu), the Find a REALTOR directory and Market Insights. property.mibor.com itself sits behind a
  Cloudflare challenge (and is US-geo-restricted), so its features were not read directly. Open
  houses: described only as "our open houses page links to an upcoming open-house view", which is
  the URL already used on /services/open-houses/ (property.mibor.com/?openhousedaysin=90...).
- MIBOR Ethics page: MIBOR holds REALTOR members accountable to the Code of Ethics (complaints,
  Ombuds mediation, arbitration). Licensing is the Indiana Real Estate Commission (PLA), not MIBOR.
- Encyclopedia of Indianapolis (Markisohn 1994, rev. Apr 2021): 43 brokers organized in Jan 1912;
  the board introduced the city's first multiple listing service in 1914; renamed Metropolitan
  Indianapolis Board of Realtors (MIBOR) five years after the 1972 rename, i.e. 1977.
- NAR Handbook on Multiple Listing Policy, 2025 edition (PDF): IDX policy 7.58 lets participants
  display each other's listings on websites/apps; IDX downloads and displays refreshed at least every
  12 hours; displays must identify the listing firm; sellers can withhold listing/address from
  internet display and those can't appear via IDX; notice that data is not guaranteed accurate;
  access to MLS databases only for those expressly authorized by MLS rules; MLSs may hide fields
  meant for cooperating brokers (showing instructions, property security). Clear Cooperation
  (8.0): submit to the MLS within one business day of public marketing. The Nov 2025 changes for
  the 2026 handbook (PAG recommendations PDF) amend 7.58 only to drop the REALTOR-only IDX option;
  the 12-hour refresh and listing-firm display rules are untouched.
- NAR Multiple Listing Options for Sellers FAQ (Mar 25 2025): delayed marketing exempt listings,
  seller signs a disclosure, delayed through IDX and syndication for a period set by the local MLS,
  still available to other MLS participants to inform buyers, show and take offers; MLS public
  site counts as syndication; office exclusives aren't disseminated through the MLS. BLC's own
  delay period / coming-soon rules were not found, so the post stays general on those.
- Displet homepage: directly connected with partner MLSs, updates most listings every 60
  seconds (vendor claim, attributed in the post); powered by Solid Earth. Our search page (search/index.html):
  map and list view, price/bed/bath/property-type filters, register a free account to save
  favorites and get email alerts; homepage box sends /search/?q=. inject_search_query.py: q parsed
  into street_address (token-prefix, suffix stripped), city, postal_code, or listing_id (8 digits,
  optional "MLS #").
- Buyer agreements: NAR "Written Buyer Agreements 101" + NAR Settlement FAQs (Sep 5 2024): since
  Aug 17 2024 MLS participants working with a buyer need a written agreement before touring
  (in person or live virtual); must state compensation amount/rate, objectively ascertainable, not
  open-ended, commissions not set by law and fully negotiable. Not needed just to talk to an agent
  hosting an open house for the seller.
- No claims made about specific portals' refresh speeds or accuracy.
"""

NAR_HMLP = "https://www.nar.realtor/sites/default/files/2025-01/PDF-HMLP-2025-Handbook-on-Multiple-Listing-Policy-2025-01-23.pdf"

BODY = """
 <p>If you&rsquo;ve searched for &ldquo;MIBOR listings&rdquo; or &ldquo;MIBOR homes for sale,&rdquo; what you&rsquo;re really after is Central Indiana&rsquo;s multiple listing service: the shared database where local agents post the homes they list. Here&rsquo;s what MIBOR and its MLS actually are, why you can&rsquo;t log into the MLS yourself, how brokerage sites like ours show you the listings anyway, and how to search them quickly. Ready to look now? <a href="/search/">Search MIBOR listings on our home search</a>.</p>

 <h2 id="what-is-mibor">What Is MIBOR?</h2>
 <p><strong>MIBOR REALTOR&reg; Association</strong> is the professional association for REALTORS&reg; in Central Indiana. The name comes from the Metropolitan Indianapolis Board of Realtors, which the group adopted in 1977, but its roots go back to January 1912, when 43 local brokers organized the board that became MIBOR. Two years later, in 1914, that board introduced Indianapolis&rsquo;s first multiple listing service (Encyclopedia of Indianapolis).</p>
 <p>Today MIBOR says it serves more than 10,000 REALTORS&reg; and real estate professionals throughout central Indiana. It&rsquo;s a trade association, not a government agency. It doesn&rsquo;t issue real estate licenses (the Indiana Real Estate Commission does that), but it offers professional development, publishes local market insights, holds its members to the REALTOR&reg; Code of Ethics and owns the region&rsquo;s MLS. Our glossary entry on <a href="/glossary/mibor/">MIBOR</a> has the short version.</p>

 <h2 id="blc">The BLC: Central Indiana&rsquo;s MLS</h2>
 <p>MIBOR&rsquo;s MLS is called the <strong>Broker Listing Cooperative&reg;</strong>, or BLC&reg;. MIBOR describes it as &ldquo;your multiple listing service&rdquo; and says the name reflects the cooperation between the listing broker and the selling broker. According to the cooperative&rsquo;s April 2026 press materials, the BLC provides listing services to subscribers in <strong>17 counties across central Indiana</strong> and is owned by MIBOR REALTOR&reg; Association.</p>
 <p>The BLC is where member agents enter new listings, update price and status changes, and record sold prices. When a Central Indiana agent says a home is &ldquo;in the MLS,&rdquo; this is the system they mean, so &ldquo;MIBOR listings,&rdquo; &ldquo;MIBOR MLS&rdquo; and &ldquo;BLC listings&rdquo; all point to the same pool of homes. MIBOR says its members keep BLC listings current, including price changes and contract status, and that the BLC includes properties that may not appear on public sites. (More on why below.) For the basics, see <a href="/glossary/mls/">what an MLS is</a>.</p>
 <p>Nearly every agent-listed home ends up there for a reason: under the national <strong>Clear Cooperation</strong> policy that REALTOR&reg;-affiliated MLSs follow, a listing broker who markets a property to the public, with a yard sign, a flyer or a website, has to submit it to the MLS within one business day.</p>

 <h2 id="why-no-login">Why You Can&rsquo;t Log Into the MLS (and How IDX Works)</h2>
 <p>The BLC is a members-only system. National MLS policy says access to an MLS database can only go to people its rules expressly authorize, which generally means participating brokers and the licensees who work under them. Part of the reason is that a full MLS record holds details meant for agents rather than the public, such as showing instructions and property security information.</p>
 <p>That&rsquo;s where <strong>IDX</strong>, short for Internet Data Exchange, comes in. IDX is the MLS policy that lets brokerages display one another&rsquo;s listings on their own websites and apps, so you can browse the whole market on a broker&rsquo;s site instead of only that firm&rsquo;s listings. It comes with rules (NAR Handbook on Multiple Listing Policy):</p>
 <ul>
 <li><strong>Freshness.</strong> IDX data and the displays it feeds have to be refreshed at least every 12 hours.</li>
 <li><strong>Attribution.</strong> Each listing has to name the listing brokerage. That&rsquo;s why you&rsquo;ll see other firms&rsquo; names on homes in our search.</li>
 <li><strong>Seller choice.</strong> A seller can tell their listing broker to keep the listing, or just the address, off the internet. Those listings can&rsquo;t appear in IDX search.</li>
 <li><strong>Accuracy notice.</strong> IDX displays carry a notice that the MLS doesn&rsquo;t guarantee the data, which is one more reason to have an agent confirm the details.</li>
 </ul>
 <p>Our <a href="/search/">home search</a> is an IDX feed of BLC listings, powered by Displet, an IDX product from Solid Earth. Displet says it connects directly to its partner MLSs and updates most listings every 60 seconds.</p>

 <h2 id="mibor-search">Does MIBOR Have Its Own Public Home Search?</h2>
 <p>Yes. MIBOR&rsquo;s website links to a free listing search at <strong>property.mibor.com</strong>, where you can search by general location or a specific address, then save favorite homes and share them. MIBOR&rsquo;s site also has a Find a REALTOR&reg; directory and local market insights.</p>
 <p>For open houses, our <a href="/services/open-houses/">open houses page</a> links straight to an upcoming open-house view of MIBOR&rsquo;s search. Before you go, our guide to <a href="/blog/open-house-etiquette-indianapolis-buyers/">open house etiquette</a> covers what to expect when you walk in.</p>
 <p>Whichever public search you use, the listings come from the same BLC data. The difference is what happens next. On a brokerage site, the search is connected to agents who can confirm a home&rsquo;s status in the MLS, tell you about listings that aren&rsquo;t shown publicly and book the showing.</p>

 <h2 id="portals-vs-idx">National Portals vs. a Local IDX Search</h2>
 <p>Big national home-search sites also display MLS listings, and they&rsquo;re handy for browsing. But every site that shows listings, ours included, is displaying a copy of the MLS record that refreshes on a schedule. Here&rsquo;s where the gaps tend to show up:</p>
 <ul>
 <li><strong>Status changes.</strong> A home can go under contract in the morning and still look active on a site that hasn&rsquo;t refreshed yet. Central Indiana listings also move through statuses that mean different things; see <a href="/glossary/contingent-vs-pending/">contingent vs. pending</a>.</li>
 <li><strong>Delayed marketing.</strong> Under a national REALTOR&reg; MLS policy announced in March 2025, a seller can sign a disclosure asking to delay marketing of their listing through IDX and syndication for a period set by the local MLS. During that window the listing is still visible to other MLS members, who can tell their buyers about it, arrange showings and submit offers. It just doesn&rsquo;t appear on public search sites yet, including an MLS&rsquo;s own public site.</li>
 <li><strong>Pre-market and &ldquo;coming soon&rdquo; homes.</strong> Rules for homes that haven&rsquo;t hit the market are set locally by each MLS and do change, so the simplest approach is to ask your agent what&rsquo;s about to list in the areas you&rsquo;re watching.</li>
 <li><strong>Office exclusives.</strong> Some sellers choose not to share their listing through the MLS at all. Those homes won&rsquo;t appear in any IDX search; our page on <a href="/services/off-market-properties/">off-market properties</a> explains how buyers find them.</li>
 </ul>
 <p>Treat any listing site as a starting point. Before you plan your weekend around a home, have your agent check its status, price and showing availability in the BLC.</p>

 <h2 id="search-tips">How to Search MIBOR Listings on Our Site</h2>
 <p>Our <a href="/search/">MIBOR listing search</a> covers active BLC listings across Central Indiana in a map or list view. Type into the search box on our <a href="/">homepage</a>, or go straight to filtered results with a link like <a href="/search/?q=Greenwood">yourrealtylink.com/search/?q=Greenwood</a>. The search understands:</p>
 <ul>
 <li><strong>An address.</strong> A house number and street name are enough. You can skip the direction (N, S, E, W) and the street type (Rd, Ave, Dr), because the search matches the beginning of each word in the street address.</li>
 <li><strong>A city or town</strong>, such as <a href="/search/?q=Fishers">Fishers</a> or <a href="/search/?q=Beech%20Grove">Beech Grove</a>.</li>
 <li><strong>A ZIP code</strong>, such as <a href="/search/?q=46227">46227</a> on the south side.</li>
 <li><strong>An MLS number.</strong> Type the eight-digit listing number, with or without &ldquo;MLS #,&rdquo; to jump straight to that home.</li>
 </ul>
 <p>You can combine them, too, such as a street name plus a city or ZIP. If a search doesn&rsquo;t turn up what you expected, use the search bar inside the listings, which also takes an address, MLS number or location, or clear the filter and browse the full map. From there you can narrow results by price, bedrooms, bathrooms and property type.</p>
 <h3>Saved searches and alerts</h3>
 <p>Registering a free account on our search page lets you save favorite listings and get email alerts when new homes hit the market. If you&rsquo;d rather not set it up yourself, our team can build a search around your price range, must-haves and neighborhoods and send you new matches. Still deciding where to look? Our <a href="/communities/">communities</a> and <a href="/schools/">schools</a> guides help narrow it down.</p>

 <h2 id="next-steps">Found a Home You Like? What Happens Next</h2>
 <p>Searching is the easy part. When you&rsquo;re ready to see homes in person:</p>
 <ol>
 <li><strong>Get pre-approved.</strong> A lender&rsquo;s pre-approval tells you what you can spend and shows sellers you&rsquo;re ready. Here&rsquo;s <a href="/blog/pre-approval-vs-pre-qualification-indianapolis/">how pre-approval differs from pre-qualification</a>.</li>
 <li><strong>Sign a buyer agreement before touring.</strong> Since August 17, 2024, an MLS participant working with a buyer has to have a written agreement with that buyer before touring a home, in person or by live video. The agreement must spell out the amount or rate of your agent&rsquo;s compensation, can&rsquo;t be open-ended, and must say that commissions aren&rsquo;t set by law and are fully negotiable. Sellers sometimes agree to cover some or all of it, but that&rsquo;s negotiated deal by deal, so read the agreement and ask questions. Our <a href="/services/buyer-representation/">buyer representation</a> page and <a href="/blog/how-the-buyer-compensation-agreement-works-in-indiana/">guide to buyer agreements in Indiana</a> explain how it works with us.</li>
 <li><strong>Tour and compare.</strong> Your agent confirms status and showing instructions in the BLC, schedules showings and can pull recent sales so you know what similar homes actually sold for.</li>
 <li><strong>Make your offer.</strong> When the right one comes along, here&rsquo;s how to write <a href="/blog/making-a-winning-offer-on-a-home-indianapolis/">a strong offer</a>. Then follow our guide to <a href="/services/home-buying-process/">the home buying process</a> through inspection, appraisal and closing.</li>
 </ol>
 <p>Just talking with the agent who&rsquo;s hosting an open house for the seller doesn&rsquo;t require an agreement. Touring with an agent who represents you does.</p>

 <h2 id="our-take">Our Take</h2>
 <p>&ldquo;MIBOR listings&rdquo; are simply Central Indiana&rsquo;s MLS listings, and you don&rsquo;t need a membership to see them. Start with our <a href="/search/">home search</a>, save the homes you like, and when one is worth a closer look, let an agent confirm the details in the BLC and get you in the door. Your Realty Link is a MIBOR member brokerage, and our <a href="/agents/">agents</a> work in the BLC every day. <a href="/schedule/">Book a call with our team</a> to get started.</p>
"""

POST = dict(
 slug="mibor-listings-how-to-search-central-indiana-homes",
 title="MIBOR Listings: How to Search Central Indiana Homes",
 headline="MIBOR Listings: How to Search Every Home for Sale in Central Indiana",
 crumb="MIBOR Listings",
 h1_html="MIBOR Listings: <em>How to Search Central Indiana Homes</em>",
 desc=("What MIBOR and the BLC MLS are, why you can't log into the MLS yourself, and how to search "
       "Central Indiana homes by address, city, ZIP or MLS number."),
 date="2026-11-19", month="November 2026",
 category="Buying a Home", eyebrow="BUYING A HOME",
 focus="mibor listings",
 hero_sub="What MIBOR and its Broker Listing Cooperative&reg; MLS are, why the public can&rsquo;t log into the MLS, and how to search Central Indiana listings by address, city, ZIP or MLS number.",
 badges=["Buying a Home", "MIBOR and the MLS", "Search Tips"],
 read_min=8,
 card_title="MIBOR Listings: How to Search Them",
 card_sub="What MIBOR and the BLC MLS are, and how to search every listing.",
 qa_heading="MIBOR Listings at a Glance",
 qa_lead=("<strong>What are MIBOR listings?</strong> They&rsquo;re the homes for sale in the MIBOR Broker Listing Cooperative&reg; "
          "(BLC&reg;), the multiple listing service owned by MIBOR REALTOR&reg; Association for central Indiana. Only authorized "
          "members can log into the MLS itself, but brokerages display its listings to the public through IDX, so you can "
          "<a href=\"/search/\">search MIBOR listings on our site</a> by address, city, ZIP or MLS number."),
 qa_facts=[
  ("The association", "MIBOR REALTOR&reg; Association, founded 1912, 10,000+ members (MIBOR, 2026)"),
  ("The MLS", "Broker Listing Cooperative&reg; (BLC&reg;), 17 central Indiana counties (MIBOR BLC, April 2026)"),
  ("Who can log in", "Only users the MLS rules authorize, generally brokers and their agents (NAR MLS policy)"),
  ("How the public sees listings", "IDX displays, refreshed at least every 12 hours (NAR IDX policy)"),
  ("MIBOR&rsquo;s own search", "Free, at property.mibor.com: search by location or address (MIBOR, 2026)"),
  ("Before touring with an agent", "Signed written buyer agreement (NAR rule since Aug. 17, 2024)"),
 ],
 toc=[("what-is-mibor", "What Is MIBOR?"), ("blc", "The BLC: Central Indiana&rsquo;s MLS"),
      ("why-no-login", "Why You Can&rsquo;t Log Into the MLS"), ("mibor-search", "MIBOR&rsquo;s Public Search and Open Houses"),
      ("portals-vs-idx", "National Portals vs. a Local IDX Search"), ("search-tips", "How to Search Our Site"),
      ("next-steps", "Found a Home? What Happens Next"), ("our-take", "Our Take")],
 body=BODY,
 faqs=[
  ("What are MIBOR listings?",
   "MIBOR listings are the homes for sale in the MIBOR Broker Listing Cooperative (BLC), the multiple listing service owned by MIBOR REALTOR Association. According to the cooperative's April 2026 press materials, the BLC provides listing services to subscribers in 17 counties across central Indiana. Searches for MIBOR listings, MIBOR MLS and BLC listings all point to the same pool of homes."),
  ("Can I search the MIBOR MLS myself?",
   "Not directly. Access to the MLS is limited to users its rules authorize, generally brokers and the licensees who work for them. The public sees the same listings through IDX searches on brokerage websites, like the home search on yourrealtylink.com, or through MIBOR's own free public search at property.mibor.com."),
  ("Is MIBOR the same as the MLS?",
   "No. MIBOR REALTOR Association is the professional association for central Indiana REALTORS. The MLS is the Broker Listing Cooperative (BLC), which MIBOR owns. People often use the two names interchangeably."),
  ("Why does a home show as active online when it's already under contract?",
   "Listing sites display a copy of the MLS record that refreshes on a schedule. National MLS policy requires IDX displays to refresh at least every 12 hours, and other sites update on their own timelines, so a status change can take a while to show up. Ask your agent to confirm a home's status in the MLS before you plan a showing."),
  ("How do I find open houses in Central Indiana?",
   "The Open Houses page on yourrealtylink.com links straight to an upcoming open-house view of MIBOR's free public property search, and your agent can set up alerts for homes that match what you want. You don't need to sign anything just to talk with the agent hosting an open house for the seller."),
  ("Do I have to sign an agreement to tour a home with an agent?",
   "Yes. Since August 17, 2024, an MLS participant working with a buyer must have a written agreement with that buyer before touring a home, in person or by live video. The agreement must state the amount or rate of the agent's compensation, cannot be open-ended, and must say that commissions are not set by law and are fully negotiable."),
 ],
 sources=[
  ("MIBOR REALTOR&reg; Association, About", "https://www.mibor.com/about"),
  ("MIBOR, Broker Listing Cooperative&reg;", "https://www.mibor.com/join-mibor/broker-listings-cooperative/"),
  ("MIBOR, Buyers &amp; Sellers (public listing search)", "https://www.mibor.com/buyers-sellers/"),
  ("MIBOR, comprehensive listings in the BLC", "https://www.mibor.com/blog/buyers-sellers/why-do-i-need-a-realtor/comprehensive-database-of-listings/"),
  ("MIBOR, ethics", "https://www.mibor.com/buyers-sellers/ethics/"),
  ("MIBOR and Indianapolis MPO release, Aug. 2026 (MIBOR boilerplate)", "https://indympo.gov/affordability-concerns-surge-across-central-indiana-driving-declines-in-community-satisfaction/"),
  ("MIBOR Broker Listing Cooperative release, Apr. 28, 2026 (EIN Presswire reprint)", "https://rcnamericaindiana.blogspot.com/2026/04/mibor-broker-listing-cooperative.html"),
  ("Encyclopedia of Indianapolis, MIBOR REALTOR&reg; Association", "https://indyencyclopedia.org/mibor-realtor-r-association/"),
  ("NAR, Internet Data Exchange (IDX) policy", "https://www.nar.realtor/about-nar/policies/internet-data-exchange-idx"),
  ("NAR Handbook on Multiple Listing Policy, 2025 (IDX and Clear Cooperation)", NAR_HMLP),
  ("NAR, Multiple Listing Options for Sellers FAQ (Mar. 2025)", "https://nar.realtor/sites/default/files/2025-03/multiple-listing-offers-for-sellers-faq-2025-03-25.pdf"),
  ("NAR, Written Buyer Agreements 101", "https://www.nar.realtor/the-facts/written-buyer-agreements-101"),
  ("NAR Settlement FAQs (Sept. 2024)", "https://www.nar.realtor/sites/default/files/2024-10/nar-settlement-faq-2024-10-29.pdf"),
  ("Indiana Professional Licensing Agency, Real Estate Commission", "https://www.in.gov/pla/professions/real-estate-home/"),
  ("Displet IDX (Solid Earth)", "https://displet.com/"),
 ],
 related=[("/blog/how-the-buyer-compensation-agreement-works-in-indiana/", "How the Buyer Agreement Works in Indiana"),
          ("/blog/making-a-winning-offer-on-a-home-indianapolis/", "Making a Winning Offer in Indianapolis"),
          ("/blog/how-long-does-it-take-to-close-on-a-house-in-indiana/", "How Long Closing Takes in Indiana")],
 cta=("Ready to Search MIBOR Listings?",
      "Browse active Central Indiana listings by address, city, ZIP or MLS number, then let our team confirm the details in the BLC and set up your showings.",
      [("/search/", "Search Homes for Sale &rarr;", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[("/services/home-buying-process/", "The Home Buying Process"),
            ("/services/open-houses/", "Open Houses in Central Indiana"),
            ("/glossary/mls/", "What Is the MLS? (Glossary)"),
            ("/services/buyer-representation/", "Buyer Representation")],
 link_from=[
  ("glossary/mibor/index.html",
   "<strong>Want to search MIBOR listings yourself?</strong> Our guide to <a href=\"/blog/mibor-listings-how-to-search-central-indiana-homes/\">MIBOR listings and how to search them</a> explains the BLC MLS, why the public can&rsquo;t log into it, and how to search Central Indiana homes by address, city, ZIP or MLS number."),
  ("glossary/mls/index.html",
   "<strong>Searching Central Indiana?</strong> Here&rsquo;s <a href=\"/blog/mibor-listings-how-to-search-central-indiana-homes/\">how to search MIBOR listings</a>, the homes in MIBOR&rsquo;s Broker Listing Cooperative&reg; MLS, plus what IDX sites can and can&rsquo;t show you."),
 ],
 about={"@type": "Organization", "name": "MIBOR REALTOR Association", "url": "https://www.mibor.com/"},
)
