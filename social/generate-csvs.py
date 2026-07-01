import csv
from datetime import datetime, timedelta

BASE_URL = "https://indypropertyguide.com/blog"

posts = [
    ("indianapolis-real-estate-market-update-2026", "Indianapolis Real Estate Market Update 2026", "The Indianapolis housing market is shifting in 2026. Home prices, inventory, buyer demand — we break it all down on IndyPropertyGuide.com so you can make smart moves whether you're buying or selling.\n\n#IndianapolisRealEstate #IndyHousingMarket #YourRealtyLink #CentralIndiana"),
    ("best-neighborhoods-to-buy-a-home-in-indianapolis", "Best Neighborhoods to Buy a Home in Indianapolis", "Where should you buy in Indianapolis? From Broad Ripple to Geist to Meridian-Kessler, we ranked the best neighborhoods for every type of buyer. Full guide on IndyPropertyGuide.com.\n\n#Indianapolis #HomeBuying #BestNeighborhoods #IndyRealEstate"),
    ("how-to-sell-your-home-fast-in-greenwood-indiana", "How to Sell Your Home Fast in Greenwood Indiana", "Thinking about selling in Greenwood? Pricing strategy, staging, and timing are everything. Our latest guide on IndyPropertyGuide.com walks you through exactly how to sell fast in Johnson County.\n\n#GreenwoodIndiana #SellYourHome #JohnsonCounty #YourRealtyLink"),
    ("first-time-home-buyer-guide-indianapolis-2026", "First Time Home Buyer Guide — Indianapolis 2026", "Buying your first home in Indianapolis? Don't go in blind. Our 2026 first-time buyer guide on IndyPropertyGuide.com covers everything from pre-approval to closing day.\n\n#FirstTimeHomeBuyer #Indianapolis #HomeBuying #IndyPropertyGuide"),
    ("living-in-carmel-indiana-what-to-know-before-you-move", "Living in Carmel Indiana", "Carmel, Indiana consistently ranks as one of the best places to live in America. But what's it really like? Schools, neighborhoods, home prices — all on IndyPropertyGuide.com.\n\n#CarmelIndiana #LivingInCarmel #HamiltonCounty #IndyRealEstate"),
    ("what-is-my-home-worth-in-indianapolis", "What Is My Home Worth?", "Curious what your Indianapolis home is worth right now? The answer might surprise you. Get the facts on home values and free CMA options at IndyPropertyGuide.com.\n\n#HomeValue #Indianapolis #FreeValuation #YourRealtyLink"),
    ("fishers-indiana-one-of-americas-best-places-to-live", "Fishers Indiana — Best Places to Live", "Fishers keeps landing on \"Best Places to Live\" lists — and for good reason. Great schools, growing downtown, and strong home values. Read more on IndyPropertyGuide.com.\n\n#FishersIndiana #BestPlacesToLive #HamiltonCounty #IndyHomes"),
    ("why-join-a-real-estate-team-instead-of-going-independent", "Why Join a Real Estate Team?", "Solo agent life getting tough? There's a reason top producers join teams. Better leads, broker support, and actual mentorship. See what Your Realty Link offers at IndyPropertyGuide.com.\n\n#RealEstateAgent #JoinOurTeam #YourRealtyLink #IndianapolisRealEstate"),
    ("buying-new-construction-in-central-indiana-pros-and-cons", "Buying New Construction — Pros and Cons", "New construction looks perfect in the model home. But there are things builders won't tell you. Our honest pros-and-cons guide is live on IndyPropertyGuide.com.\n\n#NewConstruction #HomeBuying #CentralIndiana #IndyPropertyGuide"),
    ("closing-costs-in-indiana-what-sellers-need-to-know", "Closing Costs for Indiana Sellers", "Selling your home in Indiana? Know exactly what closing costs to expect BEFORE you list. Our detailed breakdown is on IndyPropertyGuide.com — no surprises at the closing table.\n\n#ClosingCosts #SellingAHome #IndianaRealEstate #YourRealtyLink"),
    ("zionsville-indiana-small-town-luxury-living-near-indy", "Zionsville — Small Town Luxury", "Zionsville combines small-town charm with some of the finest homes in Central Indiana. Brick streets, top schools, and a village feel minutes from Indy. Explore it on IndyPropertyGuide.com.\n\n#ZionsvilleIndiana #LuxuryLiving #BooneCounty #IndyRealEstate"),
    ("investment-property-in-indianapolis-is-now-a-good-time", "Investment Property in Indianapolis", "Indianapolis continues to be one of the best markets in the country for real estate investors. Cash flow, appreciation, and affordability — read why on IndyPropertyGuide.com.\n\n#InvestmentProperty #Indianapolis #RealEstateInvesting #YourRealtyLink"),
    ("how-the-buyer-compensation-agreement-works-in-indiana", "Buyer Compensation Agreement Explained", "Confused about the new buyer compensation agreement in Indiana? You're not alone. We explain exactly how it works and what it means for you at IndyPropertyGuide.com.\n\n#BuyerAgent #IndianaRealEstate #HomeBuying #IndyPropertyGuide"),
    ("top-5-things-that-kill-a-home-sale-in-indianapolis", "5 Things That Kill a Home Sale", "Your home isn't selling? One of these 5 common mistakes might be the reason. Check IndyPropertyGuide.com for the full breakdown — and how to fix each one.\n\n#SellYourHome #Indianapolis #HomeSellingTips #YourRealtyLink"),
    ("avon-indiana-why-families-love-hendricks-county", "Why Families Love Avon Indiana", "Avon is one of Hendricks County's most popular family communities — and for good reason. Great schools, parks, and homes in the $250s-$450s. Full guide on IndyPropertyGuide.com.\n\n#AvonIndiana #HendricksCounty #FamilyFriendly #IndyHomes"),
    ("yrl-agent-commission-structure-what-you-need-to-know", "YRL Commission Structure", "Real estate agents: wondering what a competitive commission split looks like? Your Realty Link breaks down our structure and what agents actually keep. Details at IndyPropertyGuide.com.\n\n#RealEstateAgent #CommissionSplit #YourRealtyLink #JoinOurTeam"),
    ("mccordsville-indiana-hancock-countys-fastest-growing-city", "McCordsville — Hancock County's Boom Town", "McCordsville has gone from a quiet crossroads to one of Indiana's fastest-growing communities. New builds, Mt. Vernon schools, and easy I-70 access. Read more at IndyPropertyGuide.com.\n\n#McCordsville #HancockCounty #IndyGrowth #CentralIndiana"),
    ("home-staging-tips-for-indianapolis-sellers", "Home Staging Tips for Indy Sellers", "Staged homes sell faster and for more money — that's not opinion, it's data. Our top staging tips for Indianapolis sellers are on IndyPropertyGuide.com.\n\n#HomeStaging #SellYourHome #Indianapolis #RealEstateTips"),
    ("geist-reservoir-waterfront-homes-near-indianapolis", "Geist Reservoir — Waterfront Living", "Waterfront living just 20 minutes from downtown Indianapolis? That's Geist. Lakefront homes, boat docks, and a resort-like lifestyle. Explore the area on IndyPropertyGuide.com.\n\n#GeistReservoir #WaterfrontHomes #Indianapolis #LuxuryLiving"),
    ("indianapolis-housing-market-forecast-what-to-expect", "Indy Housing Market Forecast", "Where is the Indianapolis housing market headed? We share our honest forecast — what buyers and sellers should expect through the rest of 2026. Read it at IndyPropertyGuide.com.\n\n#HousingMarket #Indianapolis #MarketForecast #YourRealtyLink"),
    ("shelbyville-indiana-affordable-living-near-indianapolis", "Shelbyville — Affordable Living Near Indy", "Looking for affordable homes with easy access to Indianapolis? Shelbyville offers homes in the $150s-$300s and a genuine small-town community. Guide on IndyPropertyGuide.com.\n\n#ShelbyvilleIndiana #AffordableHomes #ShelbyCounty #IndyRealEstate"),
    ("how-to-choose-the-right-real-estate-agent-in-indianapolis", "How to Choose the Right Agent", "Not all real estate agents are the same. Here's what to look for — and what to avoid — when choosing an agent in Indianapolis. Full guide at IndyPropertyGuide.com.\n\n#RealEstateAgent #Indianapolis #HomeBuying #HomeSellingTips"),
    ("plainfield-indiana-hendricks-countys-retail-hub", "Plainfield — Hendricks County's Hub", "Plainfield has become the retail and logistics center of Hendricks County — but it's also a great place to live. Strong schools, parks, and growing neighborhoods. More at IndyPropertyGuide.com.\n\n#PlainfieldIndiana #HendricksCounty #IndySuburbs #HomeBuying"),
    ("my-home-expired-what-should-i-do-next", "My Listing Expired — Now What?", "Your home didn't sell. It's frustrating, but it's not the end. Here's exactly what to do next — and how a fresh strategy can change everything. Read it at IndyPropertyGuide.com.\n\n#ExpiredListing #SellYourHome #Indianapolis #YourRealtyLink"),
    ("why-fsbo-homes-sell-for-less-in-indianapolis", "Why FSBO Homes Sell for Less", "Thinking about selling your home yourself? The data shows FSBO homes in Indianapolis typically sell for significantly less. Here's why — and what to do instead. Full article on IndyPropertyGuide.com.\n\n#FSBO #ForSaleByOwner #Indianapolis #RealEstateTips"),
    ("selling-a-home-during-a-divorce-in-indiana", "Selling a Home During Divorce", "Going through a divorce and need to sell the house? It's one of the hardest parts of the process. We walk through Indiana-specific steps with care at IndyPropertyGuide.com.\n\n#DivorceRealEstate #SellingAHome #Indiana #YourRealtyLink"),
    ("probate-and-estate-home-sales-in-indianapolis", "Probate and Estate Home Sales", "Handling a loved one's estate and need to sell their home? The process can feel overwhelming. Our compassionate step-by-step guide is on IndyPropertyGuide.com.\n\n#EstateSale #Probate #Indianapolis #IndianaRealEstate"),
    ("down-payment-assistance-programs-in-indiana-2026", "Down Payment Assistance in Indiana", "Did you know Indiana has programs that can help cover your down payment? Many buyers qualify and don't even know it. Full breakdown at IndyPropertyGuide.com.\n\n#DownPayment #FirstTimeHomeBuyer #Indiana #HomeBuying"),
    ("brownsburg-indiana-racing-town-growing-suburbs", "Brownsburg — Racing Town, Growing Suburbs", "Home to Lucas Oil Raceway and some of Hendricks County's best neighborhoods, Brownsburg is booming. Schools, parks, and homes in the $250s-$450s. Read more at IndyPropertyGuide.com.\n\n#BrownsburgIndiana #HendricksCounty #IndySuburbs #HomesForSale"),
    ("noblesville-indiana-hamilton-countys-county-seat", "Noblesville — Hamilton County's Heart", "Noblesville blends historic charm with modern growth. The courthouse square, Ruoff Music Center, and neighborhoods for every budget. Explore it on IndyPropertyGuide.com.\n\n#NoblesvilleIndiana #HamiltonCounty #IndyRealEstate #CentralIndiana"),
    ("what-is-a-short-sale-in-indiana", "What Is a Short Sale in Indiana?", "A short sale can be a lifeline if you owe more than your home is worth. But the process is complex. We explain how it works in Indiana at IndyPropertyGuide.com.\n\n#ShortSale #IndianaRealEstate #SellingAHome #YourRealtyLink"),
    ("broad-ripple-indianapolis-most-vibrant-neighborhood", "Broad Ripple — Indy's Most Vibrant Neighborhood", "Art galleries, local restaurants, the Monon Trail, and a vibe you can't find anywhere else in Indianapolis. Broad Ripple is special. Neighborhood guide on IndyPropertyGuide.com.\n\n#BroadRipple #Indianapolis #NeighborhoodGuide #IndyHomes"),
    ("irvington-indianapolis-historic-charm-on-the-east-side", "Irvington — Historic Charm on Indy's East Side", "Irvington is one of Indianapolis's best-kept secrets — tree-lined streets, historic homes, and a tight-knit community. Discover it on IndyPropertyGuide.com.\n\n#Irvington #Indianapolis #HistoricHomes #EastSide"),
    ("va-loans-in-indiana-a-complete-guide-for-veterans", "VA Loans in Indiana — Veterans Guide", "Served our country? You've earned a VA loan with zero down payment. Our complete Indiana VA loan guide covers eligibility, benefits, and how to get started. At IndyPropertyGuide.com.\n\n#VALoan #Veterans #IndianaRealEstate #HomeBuying"),
    ("westfield-indiana-real-estate-home-of-grand-park", "Westfield — Home of Grand Park", "Grand Park put Westfield on the map, but the real estate market keeps families staying. Top schools, new builds, and a growing downtown. Full guide on IndyPropertyGuide.com.\n\n#WestfieldIndiana #GrandPark #HamiltonCounty #IndyRealEstate"),
    ("year-in-review-central-indiana-real-estate-2025", "Central Indiana Real Estate — 2025 Year in Review", "What happened in the Central Indiana real estate market in 2025? Price trends, inventory shifts, and lessons that matter for 2026. Full recap at IndyPropertyGuide.com.\n\n#YearInReview #CentralIndiana #RealEstateMarket #YourRealtyLink"),
    ("anderson-indiana-real-estate-guide", "Anderson Indiana Real Estate Guide", "Anderson offers some of the most affordable homes near Indianapolis with genuine small-city character. Our complete area guide is on IndyPropertyGuide.com.\n\n#AndersonIndiana #MadisonCounty #AffordableHomes #IndyRealEstate"),
    ("why-real-estate-agents-switch-brokerages-indianapolis", "Why Agents Switch Brokerages", "Feeling stuck at your current brokerage? You're not alone. Here's why Indianapolis agents are making the switch — and what to look for in your next home. Read it at IndyPropertyGuide.com.\n\n#RealEstateAgent #BrokerageSwitch #Indianapolis #YourRealtyLink"),
    ("multi-family-investing-indianapolis", "Multi-Family Investing in Indianapolis", "Duplexes, triplexes, and small apartment buildings — Indianapolis is one of the best markets in the country for multi-family investing. Full strategy guide on IndyPropertyGuide.com.\n\n#MultiFamilyInvesting #Indianapolis #RealEstateInvestor #CashFlow"),
    ("how-to-sell-a-home-with-tenants-in-indianapolis", "Selling a Home With Tenants", "Have tenants and need to sell? Indiana law, showing logistics, and investor vs. owner-occupant buyers — we cover it all on IndyPropertyGuide.com.\n\n#RentalProperty #SellYourHome #Indianapolis #LandlordTips"),
    ("should-i-sell-my-home-before-or-after-retirement", "Sell Before or After Retirement?", "Timing your home sale around retirement is a big financial decision. Tax implications, downsizing options, and market strategy — all on IndyPropertyGuide.com.\n\n#Retirement #SellingAHome #Downsizing #IndyRealEstate"),
    ("fha-loans-in-indiana-requirements-and-benefits", "FHA Loans in Indiana Explained", "FHA loans make homeownership possible with as little as 3.5% down. Credit scores, property requirements, and how to qualify — full guide on IndyPropertyGuide.com.\n\n#FHALoan #HomeBuying #Indiana #FirstTimeHomeBuyer"),
    ("how-long-does-it-take-to-sell-a-house-in-indianapolis", "How Long to Sell a House in Indy?", "From listing to closing — what's the realistic timeline for selling a home in Indianapolis? Pricing, condition, and seasonal factors all play a role. Details at IndyPropertyGuide.com.\n\n#SellYourHome #Indianapolis #RealEstateTips #YourRealtyLink"),
    ("rent-vs-buy-in-indianapolis-2026-comparison", "Rent vs Buy in Indianapolis — 2026", "Is it cheaper to rent or buy in Indianapolis right now? We compare the real numbers — monthly costs, equity, tax benefits, and break-even timelines. Read it at IndyPropertyGuide.com.\n\n#RentVsBuy #Indianapolis #HomeBuying #CentralIndiana"),
    ("whitestown-indiana-boone-countys-fastest-growing-town", "Whitestown — Boone County's Boom Town", "Whitestown is one of Indiana's fastest-growing communities. New construction, Zionsville schools, and the Anson development. Area guide at IndyPropertyGuide.com.\n\n#WhitestownIndiana #BooneCounty #NewConstruction #IndyGrowth"),
    ("pendleton-indiana-small-town-living-near-anderson", "Pendleton — Small Town Charm Near I-69", "Falls Park, a historic downtown, and affordable homes starting in the $200s. Pendleton is one of Madison County's hidden gems. Full guide on IndyPropertyGuide.com.\n\n#PendletonIndiana #MadisonCounty #SmallTownLiving #IndyRealEstate"),
    ("bargersville-indiana-johnson-countys-southern-charm", "Bargersville — Johnson County's Southern Charm", "Center Grove schools, rolling countryside, and new subdivisions — Bargersville is where families are moving for space and value. Explore it on IndyPropertyGuide.com.\n\n#BargersvilleIndiana #JohnsonCounty #CenterGrove #IndyHomes"),
]

# Schedule dates
# CSI Realty Team: Tuesdays 10:00 AM, Fridays 2:00 PM
# Your Realty Link: Wednesdays 11:00 AM, Saturdays 9:00 AM
start = datetime(2026, 7, 7)  # Monday

def get_schedule(day1_offset, time1, day2_offset, time2, count):
    """Generate schedule: 2 posts per week"""
    dates = []
    week_start = start
    i = 0
    while len(dates) < count:
        if i % 2 == 0:
            d = week_start + timedelta(days=day1_offset)
            dates.append(d.replace(hour=time1[0], minute=time1[1]))
        else:
            d = week_start + timedelta(days=day2_offset)
            dates.append(d.replace(hour=time2[0], minute=time2[1]))
            week_start += timedelta(weeks=1)
        i += 1
    return dates

csi_dates = get_schedule(1, (10, 0), 4, (14, 0), len(posts))   # Tue 10am, Fri 2pm
yrl_dates = get_schedule(2, (11, 0), 5, (9, 0), len(posts))    # Wed 11am, Sat 9am

def write_csv(filename, dates, posts_list):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['postAtSpecificTime (YYYY-MM-DD HH:mm:ss)', 'content', 'link (OGmetaUrl)', 'imageUrls', 'gifUrl', 'videoUrls', 'thumbnailUrl'])
        for i, (slug, title, copy) in enumerate(posts_list):
            dt = dates[i].strftime('%Y-%m-%d %H:%M:%S')
            link = f"{BASE_URL}/{slug}/"
            writer.writerow([dt, copy, link, '', '', '', ''])

outdir = "/Users/danielcope/Library/Mobile Documents/com~apple~CloudDocs/Claude/YRL/indypropertyguide/social"
write_csv(f"{outdir}/ghl-csi-realty-team.csv", csi_dates, posts)
write_csv(f"{outdir}/ghl-your-realty-link.csv", yrl_dates, posts)

print(f"CSI Realty Team: {len(posts)} posts, {csi_dates[0].strftime('%b %d')} - {csi_dates[-1].strftime('%b %d, %Y')}")
print(f"Your Realty Link: {len(posts)} posts, {yrl_dates[0].strftime('%b %d')} - {yrl_dates[-1].strftime('%b %d, %Y')}")
