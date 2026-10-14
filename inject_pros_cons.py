#!/usr/bin/env python3
"""Honest "Pros and Cons of Living in <Town>" sections on the 8 biggest suburb pages.

Oct 2026 SEO audit: Niche/aggregators own "is <town> a good place to live"; none of our city
pages had pros/cons. Each section = 4 pros, 3 cons, who-it-suits, and a direct answer to
"Is <Town>, Indiana a good place to live?". Price ranges match city_guides_data.py; factual
claims beyond that were sourced (Census 2025 estimates, Indiana DOR county tax rates, INDOT /
city project pages, local news) and the main sources are linked under each section.
No safety/crime claims. Tax-difference dollar figures are simple arithmetic on DOR rates.

Marker-wrapped (<!-- PROS-CONS --> ... <!-- /PROS-CONS -->), inserted right after the
"Living in <Town>, Indiana" section. Idempotent — re-run to update.
"""
import re

START, END = "<!-- PROS-CONS -->", "<!-- /PROS-CONS -->"
DOR = ("https://www.in.gov/dor/files/dn01.pdf", "Indiana DOR county tax rates (2026)")
CENSUS = ("https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/cities/totals/sub-est2025_18.csv", "U.S. Census Bureau 2025 population estimates")

TOWNS = {
"johnson-county/greenwood": dict(name="Greenwood",
 pros=["Around 15 minutes to downtown Indianapolis via I-65 or US-31, one of the quickest commutes from the south suburbs.",
       "Homes typically run from the $250s to the $450s, and parts of the city sit in the sought-after <a href=\"/neighborhoods/center-grove-indiana/\">Center Grove</a> school district.",
       "Old Town&rsquo;s Craig Park hosts a summer concert series and the Freedom Festival, and the city runs Freedom Springs aquatic park.",
       "Johnson County&rsquo;s 1.40% local income tax is below Marion County&rsquo;s 2.02%, roughly $620 a year less per $100,000 of income."],
 cons=["The Louisville &amp; Indiana Railroad freight line runs through downtown, so expect occasional waits at crossings near Old Town.",
       "School district depends on the exact address &mdash; Center Grove, Greenwood Community or Clark-Pleasant &mdash; so check boundaries before you write an offer.",
       "Indianapolis plans to widen County Line Road along Greenwood&rsquo;s northern edge, but construction isn&rsquo;t expected to start until 2028."],
 who="Greenwood suits commuters who want south-side value, lots of shopping and dining, and a quick drive downtown. If you&rsquo;d rather have a quiet courthouse-square town, look at <a href=\"/cities/johnson-county/franklin-indiana-real-estate/\">Franklin</a>; for more brand-new construction, look at <a href=\"/cities/johnson-county/bargersville-indiana-real-estate/\">Bargersville</a>. Weighing it against the others? See <a href=\"/compare/greenwood-vs-franklin-vs-zionsville/\">Greenwood vs Franklin vs Zionsville</a>.",
 faq="Yes, for buyers who want value and a short commute. Greenwood sits about 15 minutes from downtown Indianapolis, homes typically range from the $250s to the $450s, and Old Town and Craig Park keep a busy community calendar. The tradeoffs are freight trains through Old Town, a road project on the north edge that&rsquo;s still years out, and school boundaries that vary by address, so verify the district before you buy.",
 sources=[DOR, ("https://southcountylineroad.com", "South County Line Road project"), ("https://www.indianapolismonthly.com/schools-2/public-schools-johnson-county/", "Indianapolis Monthly: Johnson County schools")]),

"hamilton-county/fishers": dict(name="Fishers",
 pros=["The Nickel Plate District anchors downtown with an amphitheater and farmers market, and the Fishers Event Center (home of the Indy Fuel) opened in late 2024.",
       "Hamilton Southeastern Schools serve the city, and the Conner Prairie living-history museum is inside city limits.",
       "Waterfront living around Geist Reservoir plus established neighborhoods give buyers real range.",
       "Hamilton County&rsquo;s 1.10% local income tax is the lowest in the Indianapolis metro, roughly $920 a year less per $100,000 of income than Marion County."],
 cons=["I-69 is the main commuter route, and INDOT&rsquo;s Clear Path 465 rebuild of the I-465/I-69 interchange is only wrapping up in late 2026.",
       "Prices start in the low $300s and run into the $600s and beyond, a step up from the south- and west-side suburbs.",
       "Fishers grew under 6% from 2020 to 2025 versus about 43% in Westfield, so brand-new detached homes are scarcer."],
 who="Fishers suits families who want Hamilton Southeastern Schools, a lively downtown district and easy I-69 access. Buyers set on new construction may find more choice in <a href=\"/cities/hamilton-county/westfield-indiana-real-estate/\">Westfield</a> or <a href=\"/cities/hancock-county/mccordsville-indiana-real-estate/\">McCordsville</a>.",
 faq="For many households, yes. Fishers pairs Hamilton Southeastern Schools with the Nickel Plate District, Geist Reservoir and one of the lowest county income tax rates in the metro. Expect prices from the low $300s into the $600s and beyond, and plan around I-69 rush-hour traffic. Buyers set on a brand-new build often find more options in faster-growing neighbors like Westfield.",
 sources=[DOR, CENSUS, ("https://fox59.com/indiana-news/indot-clear-path-465-project-to-be-completed-in-late-2026/amp/", "FOX59: Clear Path 465")]),

"hamilton-county/westfield": dict(name="Westfield",
 pros=["Grand Park, the nearly 400-acre sports campus, brings youth tournaments and green space to the city.",
       "The Monon Trail and Midland Trace Trail meet near downtown&rsquo;s Grand Junction Plaza, making Westfield a trail hub.",
       "Fast growth means lots of newer homes, from the Chatham Hills golf community to family neighborhoods near Grand Park.",
       "Westfield residents pay Hamilton County&rsquo;s 1.10% local income tax, versus 1.71% next door in Boone County."],
 cons=["The population jumped about 43% from 2020 to 2025, so construction &mdash; of roads, schools and neighborhoods &mdash; is constant.",
       "The &ldquo;32 Connects&rdquo; rebuild of SR-32 through downtown, which widens it and adds a roundabout, is targeted to wrap up in late 2026.",
       "Downtown Indianapolis is roughly 30 minutes away via US-31, and the biggest Grand Park tournament weekends draw 20,000+ visitors."],
 who="Westfield suits buyers who want new construction, youth sports and trails in Hamilton County. If you want a settled downtown or a shorter commute, <a href=\"/cities/hamilton-county/carmel-indiana-real-estate/\">Carmel</a> may fit better.",
 faq="Westfield is a strong fit if you want newer homes, Grand Park and trail access in Hamilton County, with prices typically from the $300s to the $600s. The flip side of being one of Indiana&rsquo;s fastest-growing cities is construction: roads, schools and downtown are still being built out, and the drive to downtown Indianapolis runs roughly 30 minutes via US-31.",
 sources=[CENSUS, DOR, ("https://youarecurrent.com/2025/11/04/paving-the-way-ind-32-reopens-through-downtown-westfield/", "Current: SR-32 through Westfield")]),

"hamilton-county/noblesville": dict(name="Noblesville",
 pros=["The historic courthouse square gives Noblesville a real, charming downtown.",
       "Lake living at Morse Reservoir, plus established communities like The Harbour and Sagamore.",
       "Ruoff Music Center, the region&rsquo;s big outdoor amphitheater, sits on the city&rsquo;s south side.",
       "Homes run from the $300s to the $600s, and residents pay Hamilton County&rsquo;s metro-low 1.10% local income tax."],
 cons=["SR-32/38 through downtown has long been a bottleneck; the city&rsquo;s Pleasant Street corridor project is meant to cut downtown traffic by about 30%.",
       "INDOT forecasts heavy congestion at SR-37&rsquo;s signalized intersections, and its interchange plan can&rsquo;t start construction before fall 2030.",
       "The drive downtown is about 30 minutes, and Ruoff concert nights add traffic around 146th Street and I-69."],
 who="Noblesville suits buyers who want small-town history, lake access and Noblesville Schools at a lower starting price than Carmel. Daily downtown commuters may prefer <a href=\"/cities/hamilton-county/carmel-indiana-real-estate/\">Carmel</a> or <a href=\"/cities/hamilton-county/fishers-indiana-real-estate/\">Fishers</a>.",
 faq="Yes, especially if you want history and water in one place. Noblesville offers a courthouse-square downtown, Morse Reservoir and homes from the $300s to the $600s, plus Hamilton County&rsquo;s lower income tax rate. The main tradeoff is traffic: downtown&rsquo;s state-road crossings and the SR-37 corridor are busy, and the drive to downtown Indianapolis takes about 30 minutes.",
 sources=[DOR, ("https://www.in.gov/indot/files/Public-Meeting-Presentation-5.7.26.pdf", "INDOT SR-37 public meeting (May 2026)"), ("https://www.wrtv.com/news/local-news/hamilton-county/noblesville/bridge-opens-as-first-phase-of-125m-noblesville-project", "WRTV: Pleasant Street project")]),

"hamilton-county/carmel": dict(name="Carmel",
 pros=["The walkable Arts &amp; Design District and the Palladium concert hall give Carmel a true downtown.",
       "The Monon Trail runs through the heart of the city and continues north into Westfield.",
       "Carmel Clay Schools are highly regarded.",
       "It&rsquo;s roughly 20 minutes to downtown via US-31/Meridian Street or Keystone Parkway, shorter than from Fishers, Noblesville or Westfield."],
 cons=["Homes typically start in the mid-$400s and run well over $1 million, so there are few starter homes.",
       "Carmel High School has about 5,200 students, the largest public high school in Indiana &mdash; some families love that, others find it too big.",
       "Expect ongoing road work: Carmel had about 158 roundabouts as of 2025, with more under construction."],
 who="Carmel suits buyers who want amenities, a walkable core and a short commute, and who have the budget for it. First-time buyers usually get more for their money in <a href=\"/cities/hamilton-county/noblesville-indiana-real-estate/\">Noblesville</a> or <a href=\"/cities/hamilton-county/westfield-indiana-real-estate/\">Westfield</a>.",
 faq="Carmel is one of the metro&rsquo;s most complete suburbs: a walkable Arts &amp; Design District, the Palladium, the Monon Trail, Carmel Clay Schools and a roughly 20-minute commute downtown. The tradeoff is cost &mdash; homes typically start in the mid-$400s and climb well over $1 million &mdash; and families should be comfortable with a very large high school and ongoing road projects.",
 sources=[("https://allk12.com/rankings/largest/indiana/level/high", "allk12: largest Indiana high schools"), ("https://www.planetizen.com/news/2026/06/137759-americas-roundabout-city-indiana", "Planetizen: Carmel roundabouts")]),

"boone-county/zionsville": dict(name="Zionsville",
 pros=["The brick-paved Main Street Village offers boutique shopping and dining in a genuine small-town setting.",
       "Zionsville Community Schools are among the state&rsquo;s top-rated.",
       "The paved Big-4 Rail Trail links the Village to nearby neighborhoods and parks.",
       "Wooded estates and golf living at Holliday Farms, about 25 minutes from downtown via I-65 and Michigan Road."],
 cons=["Homes run from the mid-$400s to over $1 million, and even with Indiana&rsquo;s 1% homestead tax cap, bills grow with home price.",
       "Boone County&rsquo;s local income tax rose to 1.71% on October 1, 2026, versus 1.10% in Hamilton County &mdash; roughly $610 more a year per $100,000 of income.",
       "Growth is pressing in: neighboring Whitestown grew about 53% from 2020 to 2025, and INDOT&rsquo;s &ldquo;421 Forward&rdquo; plan calls for rebuilding Michigan Road."],
 who="Zionsville suits buyers who put schools, character and lot size first and have the budget. Buyers who need entry-level prices often look next door in <a href=\"/cities/boone-county/whitestown-indiana-real-estate/\">Whitestown</a>. Weighing it against the others? See <a href=\"/compare/greenwood-vs-franklin-vs-zionsville/\">Greenwood vs Franklin vs Zionsville</a>.",
 faq="For buyers who put schools and small-town character first, Zionsville is a standout: a brick-paved Village, Zionsville Community Schools, wooded lots and the Big-4 Rail Trail. It&rsquo;s also among the metro&rsquo;s priciest towns, with homes from the mid-$400s to over $1 million, and Boone County&rsquo;s income tax runs higher than Hamilton County&rsquo;s. Downtown Indianapolis is about 25 minutes away.",
 sources=[DOR, ("https://payroll.org/news-resources/news/news-detail/2026/09/30/one-indiana-county-has-tax-rate-change-effective-october-1", "Boone County rate change (Oct 2026)"), CENSUS]),

"hendricks-county/avon": dict(name="Avon",
 pros=["Homes typically run from the $250s to the $450s, strong value for the west side.",
       "Avon Community School Corporation serves the town, with family neighborhoods along US-36 and County Road 100 N.",
       "IU Health West Hospital is right in town on Ronald Reagan Parkway.",
       "The population grew about 17% from 2020 to 2025, so newer neighborhoods offer plenty of choice."],
 cons=["US-36 (Rockville Road) is the main road through Avon, and INDOT&rsquo;s widening plan won&rsquo;t start its first phase until 2030.",
       "Hendricks County&rsquo;s 1.70% local income tax is higher than Hamilton County&rsquo;s 1.10%, though below Marion County&rsquo;s 2.02%.",
       "Avon has no traditional downtown yet; the Easton Grey project with its Riverwalk District broke ground in 2024 and is still being built."],
 who="Avon suits west-side families who want newer homes, solid schools and value within about 25 minutes of downtown. Buyers who want a historic, walkable square should look at <a href=\"/cities/hendricks-county/danville-indiana-real-estate/\">Danville</a>.",
 faq="Avon is a good fit for west-side buyers who want newer homes and value. Prices typically run from the $250s to the $450s, Avon Community School Corporation serves the town, and IU Health West Hospital sits on Ronald Reagan Parkway. Expect US-36 congestion, a higher county income tax than Hamilton County, and a town center that&rsquo;s still taking shape.",
 sources=[DOR, CENSUS, ("https://mirrorindy.org/avon-indianapolis-lane-widening-project-public-comment/", "Mirror Indy: US-36 widening")]),

"johnson-county/franklin": dict(name="Franklin",
 pros=["A beautifully restored courthouse square and the 1922 Artcraft Theatre give downtown real character.",
       "Franklin College gives the town a genuine small college-town feel.",
       "Homes typically run from the $200s to the $400s.",
       "Johnson County&rsquo;s 1.40% local income tax is well below Marion County&rsquo;s 2.02%."],
 cons=["Downtown Indianapolis is about 30 minutes away via I-65 or US-31, roughly double the drive from Greenwood.",
       "The Louisville &amp; Indiana Railroad freight line runs through downtown, so waiting at crossings is part of in-town life.",
       "Franklin grew about 6% from 2020 to 2025 versus about 24% in nearby Bargersville, so there are fewer new-construction choices."],
 who="Franklin suits buyers who want small-town, county-seat character and value and don&rsquo;t mind a longer drive. Daily downtown commuters or buyers set on new construction may prefer <a href=\"/cities/johnson-county/greenwood-indiana-real-estate/\">Greenwood</a> or <a href=\"/cities/johnson-county/bargersville-indiana-real-estate/\">Bargersville</a>. Weighing it against the others? See <a href=\"/compare/greenwood-vs-franklin-vs-zionsville/\">Greenwood vs Franklin vs Zionsville</a>.",
 faq="Yes, if you want small-town character at a lower price. Franklin offers a restored courthouse square, the Artcraft Theatre, Franklin College and homes from the $200s to the $400s. The tradeoffs are a longer commute (about 30 minutes to downtown Indianapolis), fewer new-construction choices than faster-growing neighbors, and freight trains that cross downtown streets.",
 sources=[DOR, CENSUS]),
}


def block(t):
    li = lambda xs: "\n".join(f"  <li>{x}</li>" for x in xs)
    src = " &middot; ".join(f'<a href="{u}" target="_blank" rel="noopener">{l}</a>' for u, l in t["sources"])
    n = t["name"]
    return f"""{START}
 <h2 id="pros-cons">Pros and Cons of Living in {n}</h2>
 <div class="pros-cons" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin:16px 0;">
 <div class="info-box" style="margin:0;"><strong>Pros</strong>
 <ul style="margin:8px 0 0;padding-left:20px;">
{li(t['pros'])}
 </ul></div>
 <div class="info-box" style="margin:0;"><strong>Cons</strong>
 <ul style="margin:8px 0 0;padding-left:20px;">
{li(t['cons'])}
 </ul></div>
 </div>
 <p><strong>Who it&rsquo;s best for:</strong> {t['who']}</p>
 <h3>Is {n}, Indiana a good place to live?</h3>
 <p>{t['faq']}</p>
 <p style="font-size:.85rem;color:var(--gray);">Sources: {src}</p>
{END}
"""


done = 0
for key, t in TOWNS.items():
    p = f"cities/{key}-indiana-real-estate/index.html"
    s = open(p, encoding="utf-8", newline="").read()
    b = block(t)
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda m: b, s, flags=re.S)
    else:
        h = s.index(f"<h2>Living in {t['name']}, Indiana</h2>")
        nxt = s.index("<h2", h + 10)
        cm = s.rfind("<!--", h, nxt)            # e.g. <!-- HOME PRICES --> right before the next h2
        at = cm if cm != -1 and s[cm:nxt].strip().endswith("-->") else nxt
        at = s.rfind("\n", 0, at) + 1
        s = s[:at] + b + s[at:]
    open(p, "w", encoding="utf-8", newline="").write(s)
    done += 1
print(f"pros/cons sections on {done} city pages")
