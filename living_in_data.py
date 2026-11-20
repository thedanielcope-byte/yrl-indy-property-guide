"""Per-town config for build_living_in.py ("Living in <Town>, Indiana: Pros and Cons" pages).

Everything factual on those pages comes from data already sourced elsewhere in the repo
(inject_pros_cons.py, city_guides_data.py, inject_tax_2027.py, build_market_social.py,
schools.json, communities.json, community-events.json). The only hand-written text is the
`intro` below, which must stick to facts already in those files.

key = inject_pros_cons.py TOWNS key ("<county-slug>/<town-slug>").
slug: the blog URL. Carmel and Franklin reuse their existing "living in" posts (same intent,
existing rankings); the rest are new URLs.
link_from: older town posts that should point readers at the pros/cons page.
"""

TOWNS = {
"hamilton-county/carmel": dict(
 slug="living-in-carmel-indiana-what-to-know-before-you-move", date="2026-05-01", city_key="carmel",
 intro=("Carmel comes up in every conversation about Indianapolis suburbs: the roundabouts, the Palladium, the Monon Trail "
        "and a downtown you can actually walk. It&rsquo;s also the priciest of the big north-side suburbs, with homes that "
        "start in the mid-$400s. Here&rsquo;s what living there is really like in 2026, the good and the less good."),
 link_from=[]),
"hamilton-county/fishers": dict(
 slug="living-in-fishers-indiana-pros-and-cons", date="2026-11-19", city_key="fishers",
 intro=("Fishers is built around the Nickel Plate District downtown, Hamilton Southeastern Schools and waterfront living "
        "near Geist Reservoir, and it pays Hamilton County&rsquo;s metro-low income tax rate. It&rsquo;s a top pick for "
        "families, but it isn&rsquo;t the cheapest way into Hamilton County, and I-69 traffic is part of daily life."),
 link_from=["blog/fishers-indiana-one-of-americas-best-places-to-live/index.html"]),
"johnson-county/greenwood": dict(
 slug="living-in-greenwood-indiana-pros-and-cons", date="2026-11-19", city_key="greenwood",
 intro=("Greenwood is the south side&rsquo;s retail and dining hub, with a revitalized Old Town and one of the quickest "
        "commutes in the metro, about 15 minutes to downtown. It offers some of the best value around Indianapolis, but "
        "which school district you get depends on the exact street."),
 link_from=[]),
"hamilton-county/noblesville": dict(
 slug="living-in-noblesville-indiana-pros-and-cons", date="2026-11-19", city_key="noblesville",
 intro=("Noblesville is Hamilton County&rsquo;s county seat, and it feels like one: a historic courthouse square, lake living "
        "on Morse Reservoir and Ruoff Music Center on the south side. It costs less to get into than Carmel, and traffic "
        "through downtown and on SR-37 is the trade-off."),
 link_from=["blog/noblesville-indiana-hamilton-countys-county-seat/index.html"]),
"hamilton-county/westfield": dict(
 slug="living-in-westfield-indiana-pros-and-cons", date="2026-11-19", city_key="westfield",
 intro=("Westfield is one of Indiana&rsquo;s fastest-growing cities, home to Grand Park and a downtown still taking shape "
        "around Grand Junction Plaza, where the Monon and Midland Trace trails meet. That growth means plenty of newer "
        "homes, and plenty of construction."),
 link_from=["blog/westfield-indiana-real-estate-home-of-grand-park/index.html"]),
"boone-county/zionsville": dict(
 slug="living-in-zionsville-indiana-pros-and-cons", date="2026-11-19", city_key="zionsville",
 intro=("Zionsville is small-town luxury: a brick-paved Main Street, wooded lots and Zionsville Community Schools, among the "
        "state&rsquo;s top-rated. It&rsquo;s also one of the most expensive places to buy in the metro, and Boone "
        "County&rsquo;s local income tax went up on October 1, 2026."),
 link_from=["blog/zionsville-indiana-small-town-luxury-living-near-indy/index.html"]),
"hendricks-county/avon": dict(
 slug="living-in-avon-indiana-pros-and-cons", date="2026-11-19", city_key="avon",
 intro=("Avon is the west side&rsquo;s family suburb: newer neighborhoods, Avon Community School Corporation and homes that "
        "typically run from the $250s to the $450s. What it doesn&rsquo;t have yet is a traditional downtown, and US-36 "
        "carries most of the traffic."),
 link_from=["blog/avon-indiana-why-families-love-hendricks-county/index.html"]),
"johnson-county/franklin": dict(
 slug="living-in-franklin-indiana", date="2026-08-08", city_key="franklin",
 intro=("Franklin is Johnson County&rsquo;s county seat and a genuine small college town, with a restored courthouse square, "
        "the 1922 Artcraft Theatre and Franklin College. It&rsquo;s one of the better values on the south side if you "
        "don&rsquo;t mind a 30-minute drive downtown."),
 link_from=[]),
}
