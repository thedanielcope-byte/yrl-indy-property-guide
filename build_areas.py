#!/usr/bin/env python3
"""Build area pages (townships / school-district areas) from the Pike Township page shell.

Oct 2026 SEO audit gap: only Pike and Warren townships had pages. Adds Perry Township (the
office's own township), Center Grove (White River Twp, Johnson County), Franklin Township and
Decatur Township. Facts were verified from district / Indy Parks / Wikipedia / INDOT sources;
prices are ranges from ZIP-level closed-sale data (Oct 2026), rounded conservatively.

Re-runnable (rebuilds each page). Afterwards run: inject_city_agents.py (sidebar agent tiles).
Adds each page to sitemap.xml and the /neighborhoods/ hub if missing.
"""
import html, json, os, re
from geo_titles import geo_title

TEMPLATE = "neighborhoods/pike-township-indianapolis/index.html"
SITE = "https://yourrealtylink.com"


def comm(slug):
    """Community link label from the community page's <title>."""
    p = f"communities/{slug}/index.html"
    t = re.search(r"<title>(.*?)</title>", open(p, encoding="utf-8").read()).group(1)
    return (f"/communities/{slug}/", html.unescape(re.sub(r" Homes for Sale.*$", "", t)))


def must(url):
    p = url.strip("/") + "/index.html"
    if not os.path.exists(p):
        raise SystemExit("missing link target: " + url)
    return url


AREAS = [
 dict(slug="perry-township-indianapolis", name="Perry Township", kind="Indianapolis",
  focus="perry township indianapolis homes",
  desc="Perry Township homes for sale on Indianapolis&rsquo;s south side: Southport, Homecroft, University Heights and Glenns Valley, generally from the $150s.",
  place=("Perry Township, Indianapolis", "Marion County, Indiana"),
  sub="Indianapolis&rsquo;s south-side township &mdash; Southport, Homecroft, University Heights and Glenns Valley, with established homes, practical prices and quick interstate access. It&rsquo;s home turf for our team.",
  badges=["📍 South Indianapolis", "🎓 Perry Township Schools", "🏡 $150s – high $300s", "~15–25 min to Downtown Indy"],
  qa_lead="<strong>Perry Township</strong> is Indianapolis&rsquo;s south-side township, about 15&ndash;25 minutes from downtown, with homes that generally range from the $150s to the high $300s. It includes Southport, Homecroft and University Heights and is served mainly by the MSD of Perry Township. Your Realty Link&rsquo;s office is on Southport Road, right in the township.",
  facts=[("Location", "South Indianapolis, Marion County"), ("Typical home prices", "$150s &ndash; high $300s"), ("Schools", "MSD of Perry Township"), ("Drive to downtown Indy", "~15&ndash;25 min")],
  zip="46227",
  intro="Perry Township covers the heart of Indianapolis&rsquo;s south side. It runs from Center Township south to the Johnson County line, with the White River as its western edge, and it&rsquo;s one of the city&rsquo;s largest townships, with more than 120,000 residents. It wraps around the small independent communities of <a href=\"/cities/marion-county/southport-indiana-real-estate/\">Southport</a> and <a href=\"/cities/marion-county/homecroft-indiana-real-estate/\">Homecroft</a>, the University of Indianapolis campus in University Heights, and wooded Glenns Valley in the southwest. Buyers get what the south side is known for: established neighborhoods, practical prices and quick interstate access. It&rsquo;s home turf for us, too. The Your Realty Link office is at 2302 E Southport Rd, right in the township.",
  living="Life in Perry Township is about convenience and community. Everyday shopping runs along US-31 and Madison Avenue, and Greenwood Park Mall sits just across County Line Road on the township&rsquo;s southern edge. Perry Park on Stop 11 Road has the only indoor ice rink in the Indy Parks system, plus a seasonal outdoor pool, courts and a playground. Glenns Valley Nature Park on Bluff Road offers wooded trails and bird watching. The University of Indianapolis brings campus events and a college-neighborhood feel to the north end of the township, and Perry Township is home to one of the largest Burmese-American communities in the country. Housing ranges from 1920s bungalows in Homecroft to mid-century ranches and larger homes on wooded lots in Glenns Valley.",
  prices="Perry Township is one of the more attainable places to buy in Marion County. Homes generally range from the $150s for smaller ranches and starter homes to the high $300s, and some larger or updated homes reach the $400s, particularly in southwest Perry. Much of the housing went up during the township&rsquo;s big growth years of the 1950s and &rsquo;60s, so ranch homes on established lots are common, with older bungalows near Homecroft and University Heights. Homes that are well prepared and accurately priced draw steady interest from first-time and value-focused buyers, and investors watch the area closely too.",
  schools="Most of Perry Township is served by the <a href=\"/schools/perry-township-schools/\">Metropolitan School District of Perry Township</a>, which runs the area&rsquo;s public elementary and middle schools and two high schools, Perry Meridian High School and Southport High School. <a href=\"/schools/roncalli-high-school/\">Roncalli High School</a>, a private Catholic school, is also in the township, and the City of Beech Grove has its own district. High school assignment depends on the address, so we recommend confirming assigned schools with the district for any home you&rsquo;re considering.",
  commute="Downtown Indianapolis is roughly 15 to 25 minutes away, depending on where you live, via I-65, US-31, Madison Avenue or I-465. I-69 runs along the township&rsquo;s west side and connects directly to I-465, which makes trips to the airport and the southwest suburbs simple.",
  agent="Your Realty Link is based in Perry Township, and our team works with buyers and sellers across the south side. Whether you want a starter ranch near Southport, a bungalow in Homecroft or a wooded lot in Glenns Valley, we bring local knowledge, full MIBOR MLS access and a proven marketing plan for sellers.",
  faqs=[("Is Southport part of Perry Township?", "Yes. Southport and Homecroft are small independent communities inside Perry Township, and both are served by the MSD of Perry Township."),
        ("Which high schools serve Perry Township?", "Perry Meridian High School and Southport High School, depending on the address. Roncalli High School is a private Catholic option in the township."),
        ("What do homes cost in Perry Township?", "Homes generally range from the $150s to the high $300s, with some larger or updated homes in the $400s."),
        ("How far is downtown Indianapolis from Perry Township?", "About 15 to 25 minutes, via I-65, US-31, Madison Avenue or I-465.")],
  comms=["sunshine-gardens-southport", "university-heights-southport", "homecroft-historic-district-homecroft", "southern-dunes-southport", "glenns-valley-southport", "southdale-southport"],
  explore=[("/cities/marion-county/southport-indiana-real-estate/", "Southport"), ("/cities/marion-county/homecroft-indiana-real-estate/", "Homecroft"),
           ("/cities/marion-county/beech-grove-indiana-real-estate/", "Beech Grove"), ("/cities/johnson-county/greenwood-indiana-real-estate/", "Greenwood")],
  resources=[("https://www.perryschools.org", "MSD of Perry Township"), ("https://parks.indy.gov/parks/perry-park/", "Perry Park (Indy Parks)"),
             ("https://parks.indy.gov/parks/glenns-valley-nature-park/", "Glenns Valley Nature Park"), ("https://www.indy.gov", "City of Indianapolis (indy.gov)")]),

 dict(slug="center-grove-indiana", name="Center Grove", kind="Indiana",
  focus="center grove homes for sale",
  desc="Center Grove homes for sale in White River Township, Johnson County: western Greenwood and Bargersville, newer neighborhoods, generally high $200s to the $500s.",
  place=("Center Grove (White River Township)", "Johnson County, Indiana"),
  sub="The Center Grove school district area of White River Township &mdash; western Greenwood, most of Bargersville and the land between &mdash; with newer neighborhoods and active new construction.",
  badges=["📍 Johnson County", "🎓 Center Grove Schools", "🏡 High $200s – $500s+", "~25–40 min to Downtown Indy"],
  qa_lead="<strong>Center Grove</strong> is the name buyers use for White River Township in northwest Johnson County &mdash; the area served by the Center Grove Community School Corporation, including western Greenwood and most of Bargersville. Homes generally range from the high $200s to the $500s, with estate communities higher, and downtown Indianapolis is about 25&ndash;40 minutes away.",
  facts=[("Location", "White River Twp, Johnson County"), ("Typical home prices", "High $200s &ndash; $500s+"), ("Schools", "Center Grove Community Schools"), ("Drive to downtown Indy", "~25&ndash;40 min")],
  zip="46143",
  intro="Center Grove isn&rsquo;t a town on the map. It&rsquo;s the name buyers use for White River Township in northwest Johnson County, the area served by the Center Grove Community School Corporation. It takes in western <a href=\"/cities/johnson-county/greenwood-indiana-real-estate/\">Greenwood</a>, most of <a href=\"/cities/johnson-county/bargersville-indiana-real-estate/\">Bargersville</a> and the unincorporated land between them, about 15 miles south of downtown Indianapolis. More than 52,000 people live here, and it has become one of the south side&rsquo;s most requested places to buy, for its newer neighborhoods, family-focused community and the district itself. Our team helps buyers and sellers throughout the Center Grove area, from established subdivisions to new-construction communities.",
  living="Daily life in Center Grove centers on State Road 135, where groceries, restaurants and services line the road from Smith Valley Road south toward Bargersville. Independence Park on Morgantown Road has an accessible playground, walking trails, basketball courts and picnic shelters, and the Johnson County Public Library&rsquo;s White River Branch is close by. On weekends, Mallow Run Winery near Bargersville hosts summer concerts on the lawn, and Bargersville&rsquo;s local spots round out the dining scene. For bigger shopping trips, Greenwood Park Mall and the US-31 corridor are a short drive east. School activities and youth sports are a big part of community life.",
  prices="Center Grove carries a premium over much of Johnson County because so many buyers target the district. Homes generally range from the high $200s for older ranches and smaller homes to the $500s for larger and newer two-stories, and most sales land in the $300s and $400s. Estate and custom communities such as Aberdeen, Shadowood and Claybourne go well beyond that. Most of the housing is newer, and new construction is still active in communities like Bellingham, Sawyer Walk and Berry Chase. Buyers should be pre-approved and ready to act on well-priced homes.",
  schools="The <a href=\"/schools/center-grove-schools/\">Center Grove Community School Corporation</a> serves White River Township with six elementary schools, two middle schools and Center Grove High School. The district gives the area its name and drives much of local demand. Not every Greenwood address is in Center Grove, and small sections of Bargersville are served by Franklin Community Schools, so we recommend confirming school assignment with the district for any specific home.",
  commute="Most commuters use I-69, the upgraded former State Road 37, which now connects directly to I-465 and has an interchange at Smith Valley Road. Others take State Road 135 or US-31 north. Depending on where you live and on traffic, the drive downtown typically runs about 25 to 40 minutes.",
  agent="Our Southport Road office is a short drive north of Center Grove, and our team helps buyers and sellers across the district. Whether you want new construction, an established subdivision near Stones Crossing or a larger lot toward Bargersville, we bring local knowledge, full MIBOR MLS access and a proven marketing plan for sellers.",
  faqs=[("Is Center Grove a city?", "No. Center Grove is the name of the school district and of the White River Township area it serves, which includes western Greenwood and most of Bargersville."),
        ("Is every Greenwood home in Center Grove schools?", "No. Only parts of western Greenwood are in the Center Grove district, so confirm school assignment by address."),
        ("What do homes cost in Center Grove?", "Homes generally range from the high $200s to the $500s, and estate communities like Aberdeen and Shadowood run higher."),
        ("Is there new construction in Center Grove?", "Yes. Communities such as Bellingham, Sawyer Walk, Highland Knoll, Lone Pine Farms and Berry Chase have offered new construction.")],
  comms=["enclave-at-stones-crossing-greenwood", "lone-pine-farms-greenwood", "berry-chase-greenwood", "scottsdale-estates-greenwood", "bellingham-bargersville", "sawyer-walk-bargersville", "highland-knoll-bargersville", "aberdeen-bargersville", "shadowood-bargersville", "claybourne-bargersville"],
  explore=[("/cities/johnson-county/greenwood-indiana-real-estate/", "Greenwood"), ("/cities/johnson-county/bargersville-indiana-real-estate/", "Bargersville"),
           ("/schools/greenwood-christian-academy/", "Greenwood Christian Academy")],
  resources=[("https://www.centergrove.k12.in.us", "Center Grove Community School Corporation"), ("https://www.visitindy.com/directory/mallow-run-winery/", "Mallow Run Winery")]),

 dict(slug="franklin-township-indianapolis", name="Franklin Township", kind="Indianapolis",
  focus="franklin township indianapolis homes",
  desc="Franklin Township homes for sale in southeast Indianapolis: newer subdivisions, historic Acton and Wanamaker, Franklin Central schools, the $200s to $400s.",
  place=("Franklin Township, Indianapolis", "Marion County, Indiana"),
  sub="Southeast Indianapolis with a suburban feel &mdash; newer subdivisions, historic Acton and Wanamaker, room to spread out and Franklin Township schools, all inside Marion County.",
  badges=["📍 Southeast Indianapolis", "🎓 Franklin Township Schools", "🏡 $200s – $400s+", "~20–30 min to Downtown Indy"],
  qa_lead="<strong>Franklin Township</strong> is the southeast corner of Marion County, part of Indianapolis but suburban in feel, about 20&ndash;30 minutes from downtown. Homes generally range from the $200s to the $400s, with larger homes and acreage higher, and the whole township is served by the Franklin Township Community School Corporation.",
  facts=[("Location", "Southeast Indianapolis, Marion County"), ("Typical home prices", "$200s &ndash; $400s+"), ("Schools", "Franklin Township Community Schools"), ("Drive to downtown Indy", "~20&ndash;30 min")],
  zip="46239",
  intro="Franklin Township is the southeast corner of Marion County, with Perry Township to the west, Warren Township to the north and the Johnson County line to the south. It&rsquo;s part of the City of Indianapolis but feels more like a suburb. The population has more than doubled in recent decades as new subdivisions filled in around old farm roads, while historic crossroads communities like Acton and Wanamaker keep a small-town flavor. Buyers come for newer homes, room to spread out and the Franklin Township Community School Corporation, all without leaving Marion County.",
  living="Franklin Township mixes suburban convenience with real green space. Southeastway Park, a 188-acre Indy Parks nature park near the I-74 Acton Road exit, has woods, prairies, a pond and Buck Creek. Franklin Township Community Park on Edgewood Avenue has nature trails, a pond and a playground. The township&rsquo;s history runs deep: Acton grew up beside the railroad in the 1850s, and Wanamaker was laid out along the old Michigan Road, today&rsquo;s Southeastern Avenue corridor. Newer grocery and retail development has followed the housing growth, so everyday errands stay close to home.",
  prices="Franklin Township homes generally range from the $200s for established homes to the $400s for larger and newer two-stories, and bigger homes and acreage properties toward Acton reach higher. Most of the housing growth has come west of Franklin Road, where newer subdivisions dominate, while farther east family farms and larger lots keep a rural feel. That gives buyers real range: newer suburban homes, older homes near the historic town centers and country properties, all inside Marion County.",
  schools="The whole township is served by the <a href=\"/schools/franklin-township-schools/\">Franklin Township Community School Corporation</a>. Its single high school, Franklin Central High School, serves students from across the township, and the district&rsquo;s reputation is a major reason families choose the southeast side. Elementary assignments depend on the address and can shift as the area grows, so confirm current school assignments with the district for any home you&rsquo;re considering.",
  commute="Franklin Township has interstate access on several sides: I-65 and I-465 to the west and north, and I-74 to the northeast. Southport Road and Franklin Road handle local traffic. Downtown Indianapolis is roughly 20 to 30 minutes away, depending on your starting point.",
  agent="Our Southport Road office is just west of Franklin Township, and our team helps buyers and sellers across the southeast side. Whether you want a newer two-story, a home near historic Acton or Wanamaker, or a property with room to roam, we bring local knowledge, full MIBOR MLS access and a proven marketing plan.",
  faqs=[("Is Franklin Township part of Indianapolis?", "Yes. Franklin Township is within the consolidated City of Indianapolis, in the southeast corner of Marion County."),
        ("Which high school serves Franklin Township?", "Franklin Central High School, the only high school in the Franklin Township Community School Corporation."),
        ("What do homes cost in Franklin Township?", "Homes generally range from the $200s to the $400s, and larger homes and acreage near Acton run higher."),
        ("Are there parks in Franklin Township?", "Yes. Southeastway Park (188 acres, near the I-74 Acton Road exit) and Franklin Township Community Park on Edgewood Avenue.")],
  comms=["hickory-run-indianapolis", "fields-at-new-bethel-indianapolis", "emerald-preserve-indianapolis", "palermo-gardens-indianapolis", "crossroads-at-southport-indianapolis", "grayson-indianapolis", "hunters-crossing-indianapolis", "franklin-parke-estates-indianapolis", "moeller-estates-at-wildwood-farms-indianapolis", "villas-at-quail-run-indianapolis"],
  explore=[("/cities/marion-county/beech-grove-indiana-real-estate/", "Beech Grove"), ("/cities/marion-county/southport-indiana-real-estate/", "Southport"),
           ("/cities/johnson-county/greenwood-indiana-real-estate/", "Greenwood"), ("/cities/hancock-county/new-palestine-indiana-real-estate/", "New Palestine"),
           ("/neighborhoods/warren-township-indianapolis/", "Warren Township")],
  resources=[("https://www.ftcsc.org", "Franklin Township Community School Corporation"), ("https://parks.indy.gov/parks/southeastway-park/", "Southeastway Park (Indy Parks)"),
             ("https://www.indy.gov", "City of Indianapolis (indy.gov)")]),

 dict(slug="decatur-township-indianapolis", name="Decatur Township", kind="Indianapolis",
  focus="decatur township indianapolis homes",
  desc="Decatur Township homes for sale in southwest Indianapolis: Camby, Valley Mills and new construction near the airport, generally the high $100s to the $300s.",
  place=("Decatur Township, Indianapolis", "Marion County, Indiana"),
  sub="Southwest Indianapolis near the airport &mdash; Camby, Valley Mills and West Newton, established neighborhoods and fast-growing new-construction communities at approachable prices.",
  badges=["📍 Southwest Indianapolis", "✈️ Near the Airport", "🏡 High $100s – $300s+", "~15–25 min to Downtown Indy"],
  qa_lead="<strong>Decatur Township</strong> is the southwest corner of Marion County, home to the Indianapolis International Airport terminal and fast-growing subdivisions around Camby. Homes generally range from the high $100s to the $300s, with new construction from the high $200s into the low $400s, and downtown is about 15&ndash;25 minutes away.",
  facts=[("Location", "Southwest Indianapolis, Marion County"), ("Typical home prices", "High $100s &ndash; $300s+"), ("Schools", "MSD of Decatur Township"), ("Drive to downtown Indy", "~15&ndash;25 min")],
  zip="46221",
  intro="Decatur Township is the southwest corner of Marion County, the land west of the White River, with Wayne Township to the north. It&rsquo;s home to the main terminal of Indianapolis International Airport, the AmeriPlex business park, and a mix of established neighborhoods and fast-growing subdivisions around <a href=\"/cities/marion-county/camby-indiana-real-estate/\">Camby</a> and Valley Mills. Between 2000 and 2020, Decatur&rsquo;s population grew faster than all but one of Marion County&rsquo;s nine townships. The appeal is newer homes at approachable prices, room to breathe and quick access to I-465 and I-70.",
  living="Southwestway Park is Decatur Township&rsquo;s outdoor anchor: a large Indy Parks property along the White River with mountain bike trails, marked horseback trails, sports fields and Winding River Golf Course, plus Mann Hill, the second-highest point in Marion County. Golfers have a second option at the Links at Heartland Crossing, a public 18-hole course in Camby. Everyday shopping and dining line Kentucky Avenue (State Road 67), and the township&rsquo;s history shows in Valley Mills and West Newton, a Quaker-settled community laid out in 1851. Much of the township is still farmland, which gives many neighborhoods a quieter, more open feel than you&rsquo;d expect this close to the airport and downtown.",
  prices="Decatur Township is one of Marion County&rsquo;s most approachable markets for buyers who want a newer home. Prices generally run from the high $100s for older homes in the established northern neighborhoods to the $300s, and new construction from national builders typically runs from the high $200s into the low $400s. Ranches and mid-century homes are common in the north, while Camby-area subdivisions are largely newer, and master-planned <a href=\"/communities/heartland-crossing-camby/\">Heartland Crossing</a> adds pools, parks and a golf course to the mix.",
  schools="Most of Decatur Township is served by the <a href=\"/schools/decatur-township-schools/\">Metropolitan School District of Decatur Township</a>, whose high school is Decatur Central High School on Kentucky Avenue. Some neighborhoods near the county line, including parts of Heartland Crossing, are served by <a href=\"/schools/mooresville-consolidated-schools/\">Mooresville Consolidated Schools</a> instead. School assignment really does depend on the address, so confirm it with the district before you buy.",
  commute="Downtown Indianapolis is roughly 10 to 15 miles away, typically about 15 to 25 minutes via Kentucky Avenue, I-465 or I-70. The airport terminal is right in the township, and the Ronald Reagan Parkway links AmeriPlex to I-70, a plus for anyone working in the area&rsquo;s logistics and distribution corridor.",
  agent="Our team helps buyers and sellers throughout Decatur Township and the southwest side. Whether you&rsquo;re comparing new-construction communities in Camby, looking at an established ranch near Valley Mills or relocating close to the airport, we bring local knowledge, full MIBOR MLS access and a proven marketing plan for sellers.",
  faqs=[("How close is Decatur Township to the airport?", "Very close. The main terminal of Indianapolis International Airport is inside Decatur Township."),
        ("Which high school serves Decatur Township?", "Mostly Decatur Central High School (MSD of Decatur Township). Some Heartland Crossing sections are in the Mooresville district, so confirm by address."),
        ("What do homes cost in Decatur Township?", "Homes generally range from the high $100s to the $300s, and new construction runs from the high $200s into the low $400s."),
        ("Where is the outdoor recreation in Decatur Township?", "Southwestway Park, with mountain biking, horse trails and Mann Hill, plus golf at Winding River and the Links at Heartland Crossing.")],
  comms=["heartland-crossing-camby", "village-at-heartland-crossing-camby", "parks-at-decatur-camby", "oberlin-at-camby-village-camby", "trotters-landing-camby", "noble-heights-camby", "glenwood-camby"],
  explore=[("/cities/marion-county/camby-indiana-real-estate/", "Camby"), ("/cities/hendricks-county/plainfield-indiana-real-estate/", "Plainfield"),
           ("/cities/morgan-county/mooresville-indiana-real-estate/", "Mooresville")],
  resources=[("https://www.decaturproud.org", "MSD of Decatur Township"), ("https://parks.indy.gov/parks/southwestway-park/", "Southwestway Park (Indy Parks)"),
             ("https://www.indy.gov", "City of Indianapolis (indy.gov)")]),
 dict(slug='wayne-township-indianapolis',
  name='Wayne Township',
  kind='Indianapolis',
  focus='wayne township indianapolis homes',
  desc='Wayne Township homes for sale on Indianapolis&rsquo;s west side: Ben Davis, Chapel Hill, Eagledale and Haughville, around Speedway, from the $100s to $300s.',
  place=('Wayne Township, Indianapolis', 'Marion County, Indiana'),
  sub='Indianapolis&rsquo;s west side &mdash; Ben Davis, Chapel Hill, Eagledale, historic Haughville and the neighborhoods around Speedway, with established homes, approachable prices and quick interstate access.',
  badges=['📍 West Indianapolis', '🎓 Wayne Twp, Speedway &amp; IPS Schools', '🏡 $100s – $300s', '~10–25 min to Downtown Indy'],
  qa_lead='<strong>Wayne Township</strong> is Indianapolis&rsquo;s west-side township, wrapped around the Town of Speedway and about 10&ndash;25 minutes from downtown. Homes generally range from the $100s to the $300s. Most of the township is served by the MSD of Wayne Township and Ben Davis High School, while Speedway has its own district and the older east side is in Indianapolis Public Schools.',
  facts=[('Location', 'West Indianapolis, Marion County'), ('Typical home prices', '$100s &ndash; $300s'), ('Schools', 'MSD of Wayne Township (most areas)'), ('Drive to downtown Indy', '~10&ndash;25 min')],
  zip='46214',
  intro='Wayne Township is the heart of Indianapolis&rsquo;s west side. It stretches from 38th Street south to Troy Avenue and the airport, and from Belmont Avenue west to Raceway Road at the Hendricks County line, and it had nearly 150,000 residents in the 2020 Census. Inside it sit the Town of <a href="/cities/marion-county/speedway-indiana-real-estate/">Speedway</a>, home of the Indianapolis Motor Speedway, and the southern half of <a href="/cities/marion-county/clermont-indiana-real-estate/">Clermont</a>. The Park Fletcher office and industrial park sits near the airport. Neighborhoods run from historic Haughville and 1950s Eagledale to Chapel Hill, Ben Davis and newer subdivisions near the county line. Buyers come for established homes, approachable prices and quick interstate access.',
  living='The Indianapolis Motor Speedway and its museum are the township&rsquo;s best-known landmark, in the Town of Speedway. Krannert Park on High School Road has an Indy Parks family center with an indoor pool, a fitness room, a stocked fishing pond and trails, and Thatcher Park on Vermont Street adds a year-round indoor pool and a walking trail. Eagle Creek Park is a short drive north, just across 38th Street. On the east side, Haughville is a National Register historic district with the city&rsquo;s oldest continuously operating library branch, and the former Central State Hospital grounds now hold new homes and the Indiana Medical History Museum. Marian University sits on Cold Spring Road, and everyday shopping lines West Washington Street, 10th Street, Rockville Road and Crawfordsville Road.',
  prices='Prices in Wayne Township vary a lot by neighborhood, and most sales over the past year fell between about $100,000 and the high $200s. On the near west side, older Haughville homes can sell for under $100,000, and Eagledale&rsquo;s 1950s homes mostly sell from around $100,000 into the low $200s. Mid-century homes in Chapel Hill and the Ben Davis area typically run from the high $100s to the high $200s. Subdivisions built from the late 1960s through the early 2000s, such as Chapel Glen, Sunningdale Commons and Drake Landing, generally sell from the $250s into the $300s, and Avon Creek Estates reaches the high $300s. Newer homes at Central State have sold from the $250s to the $340s.',
  schools='Most of the township is served by the Metropolitan School District of Wayne Township: 11 elementary schools, the Chapel Hill and Lynhurst 7th &amp; 8th Grade Centers, the Ben Davis Ninth Grade Center, Ben Davis High School, Ben Davis University High School and the Area 31 Career Center. The Town of Speedway has its own <a href="/schools/school-town-of-speedway/">School Town of Speedway</a>, and older east-side neighborhoods such as Haughville, Eagledale and Central State, roughly a third of the township&rsquo;s homes, are in <a href="/schools/indianapolis-public-schools/">Indianapolis Public Schools</a>. Assignment depends on the exact address, so confirm schools with the district before you buy.',
  commute='Three interstates serve Wayne Township. I-465 runs north&ndash;south through the township, I-70 heads southwest toward the airport, and I-74 angles northwest toward Brownsburg, while Washington Street (US-40), Rockville Road and Crawfordsville Road (US-136) carry local traffic. Downtown is roughly 10 to 25 minutes away. IndyGo&rsquo;s Blue Line rapid-transit route, now under construction along Washington Street, is expected to open around 2028.',
  agent='Our team helps buyers and sellers across Wayne Township, from Haughville and Eagledale to Chapel Hill, Ben Davis and the newer subdivisions near the county line. Whether you want a first home, a mid-century ranch or more space on the northwest side, we bring local knowledge, full MIBOR MLS access and a proven marketing plan.',
  faqs=[('Is Speedway part of Wayne Township?', 'Yes. The Town of Speedway sits inside Wayne Township, but it&rsquo;s an independent excluded town with its own government and its own school district, the School Town of Speedway.'), ('Which schools serve Wayne Township?', 'Most addresses are in the MSD of Wayne Township, whose high school is Ben Davis High School. Speedway has its own district, and parts of the east side, including Haughville and Eagledale, are in Indianapolis Public Schools.'), ('What do homes cost in Wayne Township?', 'Most homes sell from the $100s to the $300s. Some older near-west-side homes sell for under $100,000, and a few newer subdivisions reach the high $300s.'), ('Is Eagle Creek Park in Wayne Township?', 'No. Eagle Creek Park and its reservoir sit just north of 38th Street in Pike Township, a short drive from Wayne Township&rsquo;s northern neighborhoods.')],
  comms=['eagledale-indianapolis', 'chapel-hill-indianapolis', 'chapel-glen-indianapolis', 'west-wood-indianapolis', 'speedway-woods-indianapolis', 'avon-creek-estates-indianapolis', 'villages-at-drake-landing-indianapolis', 'sunningdale-commons-indianapolis', 'cameron-meadows-indianapolis', 'central-state-indianapolis', 'speedway-city-speedway', 'speedway-manor-speedway', 'speedway-estates-speedway', 'meadowood-speedway', 'tansel-woods-clermont'],
  explore=[('/cities/marion-county/speedway-indiana-real-estate/', 'Speedway'), ('/cities/marion-county/clermont-indiana-real-estate/', 'Clermont'), ('/neighborhoods/eagle-creek-indianapolis/', 'Eagle Creek'), ('/cities/hendricks-county/avon-indiana-real-estate/', 'Avon'), ('/cities/hendricks-county/plainfield-indiana-real-estate/', 'Plainfield')],
  resources=[('https://www.wayne.k12.in.us', 'MSD of Wayne Township'), ('https://parks.indy.gov/parks/krannert-park/', 'Krannert Park (Indy Parks)'), ('https://www.indy.gov', 'City of Indianapolis (indy.gov)')]),
 dict(slug='washington-township-indianapolis',
  name='Washington Township',
  kind='Indianapolis',
  focus='washington township indianapolis homes',
  desc='Washington Township homes for sale in north Indianapolis: Broad Ripple, Meridian-Kessler, Nora and Butler-Tarkington, from the low $100s to $1M+.',
  place=('Washington Township, Indianapolis', 'Marion County, Indiana'),
  sub='North-central Indianapolis from 38th Street to 96th Street &mdash; Broad Ripple, Meridian-Kessler, Butler-Tarkington and Nora, with the Monon Trail, the White River and homes from bungalows to estates.',
  badges=['📍 North-Central Indianapolis', '🎓 Washington Twp &amp; IPS Schools', '🏡 Low $100s – $1M+', '~10–25 min to Downtown Indy'],
  qa_lead='<strong>Washington Township</strong> is north-central Indianapolis, running from 38th Street to 96th Street and taking in Broad Ripple, Meridian-Kessler, Butler-Tarkington and Nora. Homes range from condos in the low $100s to estates well past $1M, with most single-family homes in the $250s to $500s. Most of the township is served by the MSD of Washington Township, the southern part by Indianapolis Public Schools, and downtown is about 10&ndash;25 minutes away.',
  facts=[('Location', 'North-central Indianapolis, Marion County'), ('Typical home prices', 'Low $100s &ndash; $1M+'), ('Schools', 'MSD of Washington Township; IPS in the south'), ('Drive to downtown Indy', '~10&ndash;25 min')],
  zip='46220',
  intro='Washington Township is the north-central slice of Marion County. It runs from 38th Street north to 96th Street and the Hamilton County line, with Pike Township to the west and Lawrence Township to the east, and it sits entirely within the City of Indianapolis. Nearly 139,000 people lived here at the 2020 Census. The township takes in some of the city&rsquo;s best-known neighborhoods, including <a href="/neighborhoods/broad-ripple-indianapolis/">Broad Ripple</a>, <a href="/neighborhoods/meridian-kessler-indianapolis/">Meridian-Kessler</a>, <a href="/neighborhoods/butler-tarkington-indianapolis/">Butler-Tarkington</a> and <a href="/neighborhoods/nora-indianapolis/">Nora</a>, plus seven small included towns such as <a href="/cities/marion-county/meridian-hills-indiana-real-estate/">Meridian Hills</a>, Williams Creek and Rocky Ripple. Buyers come for established, tree-lined streets, trail access and a short drive downtown.',
  living='Outdoor access is a big part of life here. The Monon Trail runs the full length of the township, from 38th Street through Broad Ripple and Nora to 96th Street, and the Central Canal Towpath follows the canal from Broad Ripple past Butler University and Newfields. Along the White River, Holliday Park has 95 acres of woods, trails and gardens, Marott Park adds more than 100 acres of nature preserve, and Broad Ripple Park has a family center, pool and dog park. Culture is close by, too: Newfields (home of the Indianapolis Museum of Art), Butler&rsquo;s Hinkle Fieldhouse, the Indianapolis Art Center and the Indiana State Fairgrounds are all in the township. Everyday shopping clusters in Broad Ripple Village, Glendale Town Center, Nora and the Fashion Mall at Keystone.',
  prices='Washington Township covers a wide price range. Condos and smaller homes start in the low $100s. Most single-family homes sell in the $250s to $500s, from early-20th-century bungalows in Meridian-Kessler and Butler-Tarkington to 1950s and &rsquo;60s ranches in Nora and Greenbriar. Smaller river cottages in Ravenswood and Rocky Ripple add another option, though flood zones matter there. Prices climb along the North Meridian Street corridor, and estate homes in Meridian Hills, Williams Creek, Crows Nest and gated Sycamore Springs often pass $1M. Location, lot, school district and condition all move value here, so pricing really goes street by street.',
  schools='Most of Washington Township is served by the <a href="/schools/msd-washington-township/">Metropolitan School District of Washington Township</a>, which runs eight elementary schools, three middle schools (Eastwood, Northview and Westlane) and North Central High School. The southern part of the township, including Broad Ripple Village, Meridian-Kessler and Butler-Tarkington, is in <a href="/schools/indianapolis-public-schools/">Indianapolis Public Schools</a>. The small included towns, such as Rocky Ripple, Crows Nest, Meridian Hills and Williams Creek, are in Washington Township schools. Private options in the township include <a href="/schools/park-tudor-school/">Park Tudor School</a> and <a href="/schools/bishop-chatard-high-school/">Bishop Chatard High School</a>. District lines don&rsquo;t follow neighborhood names neatly, so confirm the district and assigned schools for any address.',
  commute='The township starts about four miles north of downtown, so most drives run roughly 10 to 25 minutes, depending on where you live. Meridian Street, College Avenue and Keystone Avenue are the main routes south, and I-465 crosses the north end of the township. IndyGo&rsquo;s Red Line rapid bus runs from 66th Street and College Avenue down College to downtown, and the Monon Trail offers a car-free route south toward downtown.',
  agent='Our team helps buyers and sellers across Washington Township, from Broad Ripple condos and Meridian-Kessler bungalows to Nora ranches and estate homes along North Meridian Street. Whether you&rsquo;re sorting out IPS and Washington Township school lines or pricing a one-of-a-kind home, we bring local knowledge, full MIBOR MLS access and a proven marketing plan.',
  faqs=[('Which school district serves Washington Township?', 'Most of it is in the MSD of Washington Township (North Central High School). The southern part, including Broad Ripple Village, Meridian-Kessler and Butler-Tarkington, is in Indianapolis Public Schools, so confirm by address.'), ('Is Washington Township part of Indianapolis?', 'Yes. It&rsquo;s one of Marion County&rsquo;s nine townships and lies entirely within Indianapolis. It also contains seven small included towns, such as Meridian Hills, Williams Creek and Rocky Ripple, that keep their own town governments.'), ('What do homes cost in Washington Township?', 'Condos start in the low $100s, most single-family homes sell in the $250s to $500s, and estate homes in areas like Meridian Hills and Williams Creek run past $1M.'), ('Where are the parks and trails in Washington Township?', 'The Monon Trail runs the length of the township, the Central Canal Towpath links Broad Ripple with Butler University and Newfields, and Holliday Park, Marott Park and Broad Ripple Park sit along the White River.')],
  comms=['ravenswood-indianapolis', 'rocky-ripple-indianapolis', 'greenbriar-indianapolis', 'sycamore-springs-indianapolis', 'newport-bay-indianapolis', 'williams-creek-indianapolis', 'broad-ripple-village-broad-ripple', 'warfleigh-broad-ripple', 'canterbury-broad-ripple', 'meridian-kessler-broad-ripple', 'meridian-hills'],
  explore=[('/cities/marion-county/meridian-hills-indiana-real-estate/', 'Meridian Hills'), ('/neighborhoods/castleton-indianapolis/', 'Castleton'), ('/cities/hamilton-county/carmel-indiana-real-estate/', 'Carmel'), ('/neighborhoods/pike-township-indianapolis/', 'Pike Township'), ('/cities/marion-county/lawrence-indiana-real-estate/', 'Lawrence')],
  resources=[('https://www.msdwt.k12.in.us', 'MSD of Washington Township'), ('https://www.myips.org', 'Indianapolis Public Schools'), ('https://parks.indy.gov/parks/holliday-park/', 'Holliday Park (Indy Parks)')],
  hoods=[('/neighborhoods/broad-ripple-indianapolis/', 'Broad Ripple'), ('/neighborhoods/meridian-kessler-indianapolis/', 'Meridian-Kessler'), ('/neighborhoods/butler-tarkington-indianapolis/', 'Butler-Tarkington'), ('/neighborhoods/nora-indianapolis/', 'Nora')]),
 dict(slug='lawrence-township-indianapolis',
  name='Lawrence Township',
  kind='Indianapolis',
  focus='lawrence township indianapolis homes',
  desc='Lawrence Township homes for sale in northeast Indianapolis: Lawrence, Fort Ben, Castleton, Oaklandon and the Geist shore, mostly the $150s to the $500s.',
  place=('Lawrence Township, Indianapolis', 'Marion County, Indiana'),
  sub='Northeast Marion County&rsquo;s township &mdash; the City of Lawrence and Fort Ben, Castleton, Oaklandon and the Geist shoreline, with everything from 1950s ranches to new construction and lake homes.',
  badges=['📍 Northeast Indianapolis', '🎓 Lawrence Township Schools', '🏡 $150s – $500s+', '~20–30 min to Downtown Indy'],
  qa_lead='<strong>Lawrence Township</strong> is the northeast corner of Marion County, about 20&ndash;30 minutes from downtown Indianapolis. It takes in the City of Lawrence (including Fort Ben and Oaklandon), most of Castleton and the Marion County side of Geist Reservoir, and most homes sell from the $150s to the $500s. Most of the township is served by the MSD of Lawrence Township.',
  facts=[('Location', 'Northeast Indianapolis, Marion County'), ('Typical home prices', '$150s &ndash; $500s+'), ('Schools', 'MSD of Lawrence Township'), ('Drive to downtown Indy', '~20&ndash;30 min')],
  zip='46236',
  intro='Lawrence Township is the northeast corner of Marion County, running from about 38th Street north to 96th Street and east to the Hancock County line. More than 120,000 people live here. About two-fifths of the township is the <a href="/cities/marion-county/lawrence-indiana-real-estate/">City of Lawrence</a>, home to the former Fort Benjamin Harrison, historic Oaklandon and Indian Lake. The rest is part of Indianapolis, including most of <a href="/neighborhoods/castleton-indianapolis/">Castleton</a>, the I-69 and Fall Creek corridor and much of the Marion County side of <a href="/neighborhoods/geist-reservoir-indianapolis/">Geist Reservoir</a>. That gives buyers real range in one township: 1950s ranches, older wooded neighborhoods, 1990s subdivisions, new construction and lake homes, mostly within Lawrence Township schools.',
  living='Green space is a big part of life here. Fort Harrison State Park, 1,700 acres on land that was once part of Fort Benjamin Harrison, has trails and fishing along Fall Creek and an 18-hole golf course, and Lawrence&rsquo;s Fort Ben Cultural Campus hosts concerts and shows around the historic Theater at the Fort. To the west, Skiles Test Nature Park has more than 80 acres of trails with a link to the Fall Creek Greenway, and Sahm Park near 91st Street adds a golf course, disc golf and courts. Castleton Square handles big shopping trips, and Pendleton Pike carries everyday shopping through Lawrence. In the northeast, the Marion County shoreline of Geist Reservoir brings lake living, while Oaklandon, founded along the railroad in 1849, keeps a small historic district.',
  prices='Lawrence Township covers a wide price range. Over the past year, most homes sold between the $150s and the $500s, and a typical sale landed in the high $200s. The most affordable options are 1950s and &rsquo;60s ranches near the township&rsquo;s southern edge, often in the $100s to low $200s. Lawrence&rsquo;s 1990s subdivisions around Sunnyside and Oaklandon generally run from the mid-$200s to the high $300s, and new construction from Lennar and Arbor Homes sits in a similar range. Around Castleton and north of Fort Harrison, established neighborhoods trade mostly in the $200s to $400s, with condos for less. Homes near the Geist shoreline are a market of their own, often from the $500s to well over $1 million.',
  schools='Most of the township is served by the <a href="/schools/msd-lawrence-township/">Metropolitan School District of Lawrence Township</a>, which runs Early Learning Centers, 11 elementary schools, two middle schools and two high schools: Lawrence Central on East 56th Street and Lawrence North on Hague Road. High school boundaries aren&rsquo;t a simple north&ndash;south split, and some areas near the township&rsquo;s southern edge are assigned to <a href="/schools/indianapolis-public-schools/">Indianapolis Public Schools</a>, so confirm schools by address. Private options in the township include <a href="/schools/cathedral-high-school/">Cathedral High School</a> and <a href="/schools/heritage-christian-school/">Heritage Christian School</a>.',
  commute='Downtown Indianapolis is roughly 12 to 15 miles away, usually 20 to 30 minutes by car depending on where you start and the traffic. I-465 runs through the township&rsquo;s west side and I-69 crosses its northwest corner at Castleton, while Pendleton Pike and Binford Boulevard handle many local trips. IndyGo&rsquo;s Purple Line rapid-transit buses, running since October 2024, link Lawrence to downtown via Post Road and 38th Street.',
  agent='Our team helps buyers and sellers across Lawrence Township, from Fort Ben and Oaklandon to Castleton and the Geist shoreline. Whether you&rsquo;re weighing a 1950s ranch, a 1990s subdivision near Fort Harrison State Park or new construction on the east side, we bring local knowledge, full MIBOR MLS access and a proven marketing plan for sellers.',
  faqs=[('Is Lawrence Township the same as the City of Lawrence?', 'No. The City of Lawrence is its own city, one of Marion County&rsquo;s four excluded cities, and covers about two-fifths of the township, including Fort Ben, Oaklandon and Indian Lake. The rest of the township, including most of Castleton and much of the Geist area, is part of Indianapolis.'), ('Which high schools serve Lawrence Township?', 'Lawrence Central and Lawrence North, both in the MSD of Lawrence Township. Assignment depends on the address, and some areas near the township&rsquo;s southern edge are in Indianapolis Public Schools, so confirm by address.'), ('What do homes cost in Lawrence Township?', 'Most homes sell from the $150s to the $500s, with a typical sale in the high $200s. Homes near the Geist shoreline can run well over $1 million.'), ('How far is Lawrence Township from downtown Indianapolis?', 'Roughly 12 to 15 miles, usually 20 to 30 minutes by car via I-69, I-465 or Pendleton Pike. IndyGo&rsquo;s Purple Line also links Lawrence with downtown.')],
  comms=['clifton-trace-indianapolis', 'lantern-hills-indianapolis', 'brendonwood-indianapolis', 'castleton-farms-indianapolis', 'silver-stream-lawrence', 'kensington-farms-lawrence', 'watson-farms-lawrence', 'oakland-hills-at-geist-lawrence', 'fort-harrison-lawrence', 'oaklandon-lawrence', 'winding-ridge-lawrence', 'lawrence-woods-lawrence', 'feather-cove-geist', 'admirals-bay-geist', 'admirals-pointe-geist', 'diamond-pointe-geist', 'the-anchorage-geist', 'masthead-at-geist'],
  explore=[('/cities/marion-county/lawrence-indiana-real-estate/', 'Lawrence'), ('/neighborhoods/castleton-indianapolis/', 'Castleton'), ('/neighborhoods/geist-reservoir-indianapolis/', 'Geist Reservoir'), ('/cities/hamilton-county/fishers-indiana-real-estate/', 'Fishers'), ('/cities/hancock-county/mccordsville-indiana-real-estate/', 'McCordsville'), ('/neighborhoods/warren-township-indianapolis/', 'Warren Township')],
  resources=[('https://www.ltschools.org', 'MSD of Lawrence Township'), ('https://www.in.gov/dnr/state-parks/parks-lakes/fort-harrison-state-park/', 'Fort Harrison State Park (Indiana DNR)'), ('https://www.cityoflawrence.org', 'City of Lawrence')]),
]

SIBLINGS = [("/neighborhoods/perry-township-indianapolis/", "Perry Township"), ("/neighborhoods/center-grove-indiana/", "Center Grove"),
            ("/neighborhoods/franklin-township-indianapolis/", "Franklin Township"), ("/neighborhoods/decatur-township-indianapolis/", "Decatur Township"),
            ("/neighborhoods/pike-township-indianapolis/", "Pike Township"),
            ("/neighborhoods/warren-township-indianapolis/", "Warren Township"), ("/neighborhoods/wayne-township-indianapolis/", "Wayne Township"),
            ("/neighborhoods/washington-township-indianapolis/", "Washington Township"), ("/neighborhoods/lawrence-township-indianapolis/", "Lawrence Township")]


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def build(a, tpl):
    url = f"{SITE}/neighborhoods/{a['slug']}/"
    path = f"/neighborhoods/{a['slug']}/"
    title = geo_title(a["name"], a["kind"])
    name = a["name"]
    desc = a["desc"]
    s = tpl
    s = re.sub(r"<!-- ═+\n YOAST SEO FIELDS.*?═+ -->",
               f"<!-- Area page — built by build_areas.py · focus keyword: {a['focus']} -->", s, count=1, flags=re.S)
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop, val in (("og:title", title), ("og:description", desc), ("og:url", url)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", desc), ("twitter:title", title), ("twitter:description", desc)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)

    faqs = a["faqs"] + [(f"How do I search homes for sale in {name}?",
                         f"Use the Your Realty Link property search to browse active MIBOR MLS listings in and around {name}, or call our team for a tailored search.")]
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "url": url, "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"]}},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": SITE, "logo": "/assets/img/yrl-logo.png",
         "telephone": "317-997-7404", "email": "indy@yourrealtylink.com",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis",
                     "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US"},
         "areaServed": {"@type": "Place", "name": a["place"][0], "containedIn": a["place"][1]}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": text(ans)}} for q, ans in faqs]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Indianapolis Neighborhoods", "item": SITE + "/neighborhoods/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n </script>', s, count=1, flags=re.S)

    s = s.replace(" Pike Township\n </div>\n</nav>", f" {name}\n </div>\n</nav>", 1)
    s = re.sub(r"<h1>.*?</h1>", f"<h1>{name} &amp; <em>Homes for Sale</em></h1>", s, count=1)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) + a["sub"] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<div class="hero-badges">.*?</div>', lambda m: '<div class="hero-badges">\n' + "\n".join(
        f' <span class="hero-badge">{b}</span>' for b in a["badges"]) + '\n </div>', s, count=1, flags=re.S)
    s = s.replace("Updated August 2026</p>", "Updated October 2026</p>", 1)

    facts = "\n".join(f" <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in a["facts"])
    facts += f'\n <div><dt>Search listings</dt><dd><a href="/search/?q={a["zip"]}">Search homes in {a["zip"]} &rarr;</a></dd></div>'
    faq_html = "\n".join(f' <details class="faq-item">\n <summary>{q}</summary>\n <div class="faq-answer">\n <p>{ans}</p>\n </div>\n </details>' for q, ans in faqs)
    comms = [comm(c) for c in a["comms"]]
    comm_block = ""
    if a.get("hoods"):   # neighborhoods inside the area that already have their own guide pages
        comm_block += (f' <h2>Neighborhoods in {name}</h2>\n <p>Our neighborhood guides inside {name}:</p>\n <div class="city-grid">\n' +
                       "".join(f' <a href="{must(u)}" class="city-card">{html.escape(l, quote=False)} <span class="arrow">&rsaquo;</span></a>\n' for u, l in a["hoods"]) +
                       ' </div>\n')
    if comms:
        comm_block += (f' <h2>Communities &amp; Subdivisions in {name}</h2>\n <p>A few of the neighborhoods buyers ask us about most:</p>\n <div class="city-grid">\n' +
                      "".join(f' <a href="{must(u)}" class="city-card">{html.escape(l, quote=False)} <span class="arrow">&rsaquo;</span></a>\n' for u, l in comms) +
                      ' </div>\n <p>Browse all <a href="/communities/">Central Indiana communities</a>.</p>\n')
    explore = [(must(u), l) for u, l in a["explore"]] + [(u, l) for u, l in SIBLINGS if u != path]
    res = "\n".join(f'    <li><a href="{u}" target="_blank" rel="noopener">{l} ↗</a></li>' for u, l in a["resources"] if l)
    main = f"""<main class="content-main">
 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">{name} Real Estate at a Glance</p>
 <p class="qa-lead">{a['qa_lead']}</p>
 <dl class="qa-facts">
{facts}
 </dl>
</div>
<!-- QA-END -->
 <!-- INTRO -->
 <p>{a['intro']}</p>
 <!-- LIVING -->
 <h2>Living in {name}</h2>
 <p>{a['living']}</p>
 <!-- HOME PRICES -->
 <h2>{name} Home Prices &amp; Real Estate Market</h2>
 <p>{a['prices']}</p>
 <div class="info-box">
 <strong>Thinking about selling in {name}?</strong> Your Realty Link provides free comparative market analyses for homeowners across Central Indiana. <a href="/services/free-home-valuation/" target="_blank" rel="noopener">Get your free home valuation →</a>
 </div>
 <!-- SCHOOLS -->
 <h2>Schools in {name}</h2>
 <p>{a['schools']}</p>
 <!-- COMMUTE -->
 <h2>Commute from {name} to Downtown Indianapolis</h2>
 <p>{a['commute']}</p>
{comm_block} <!-- WORK WITH AN AGENT -->
 <h2>Work With a {name} Real Estate Agent</h2>
 <p>{a['agent']} Call our team at <a href="tel:3179977404">317-997-7404</a> or start your search online.</p>
 <!-- CTA BLOCK 1 -->
 <div class="cta-block">
 <h3>Ready to Search Homes in {name}?</h3>
 <p>Browse active MIBOR MLS listings in and around {name}.</p>
 <div class="btn-group">
 <a href="/search/?q={a['zip']}" class="btn btn-white">Search {name} Homes →</a>
 <a href="/services/free-home-valuation/" class="btn btn-outline" target="_blank" rel="noopener">Get a Free Home Valuation</a>
 <a href="/schedule/" class="btn btn-outline">📅 Schedule a Free Consultation</a>
 </div>
 </div>
 <!-- FAQ -->
 <section class="faq-section">
 <h2>Frequently Asked Questions — {name}</h2>
{faq_html}
 </section>
 <!-- CTA BLOCK 2 -->
 <div class="cta-block cta-block-light">
 <h3>Selling a Home in {name}?</h3>
 <p>Get a free, no-obligation home valuation from Your Realty Link and see what your {name} home is worth in today&rsquo;s market.</p>
 <div class="btn-group">
 <a href="/services/free-home-valuation/" class="btn btn-primary" target="_blank" rel="noopener">Get a Free Valuation</a>
 <a href="/contact/" class="btn btn-outline">Contact Your Realty Link</a>
 </div>
 </div>
 <hr class="divider">
 <h3>Explore Nearby Areas</h3>
 <ul>
 <li><a href="/neighborhoods/">All Indianapolis Neighborhoods &amp; Areas</a></li>
{chr(10).join(f' <li><a href="{u}">{l}</a></li>' for u, l in explore)}
 </ul>
   <div class="info-box" style="margin-top:24px;">
   <strong>Helpful Local Resources</strong>
   <ul style="margin:10px 0 0; padding-left:20px;">
{res}
   </ul>
   </div>
 </main>"""
    s = re.sub(r'<main class="content-main">.*?</main>', lambda m: main, s, count=1, flags=re.S)
    s = re.sub(r"<!-- CITY-AGENTS -->.*?<!-- /CITY-AGENTS -->", "<!-- CITY-AGENTS -->\n<!-- /CITY-AGENTS -->", s, count=1, flags=re.S)
    return s


def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    sm = open("sitemap.xml", encoding="utf-8").read()
    hub = open("neighborhoods/index.html", encoding="utf-8").read()
    for a in AREAS:
        out = f"neighborhoods/{a['slug']}"
        os.makedirs(out, exist_ok=True)
        open(f"{out}/index.html", "w", encoding="utf-8").write(build(a, tpl))
        url = f"{SITE}/neighborhoods/{a['slug']}/"
        if url not in sm:
            sm = sm.replace("</urlset>", f" <url>\n <loc>{url}</loc>\n <lastmod>2026-10-14</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.8</priority>\n </url>\n</urlset>")
        print("built", out, "|", text(geo_title(a["name"], a["kind"])), "| desc", len(text(a["desc"])))
    anchor = '<a href="/neighborhoods/pike-township-indianapolis/" class="city-card">Pike Township <span class="arrow">›</span></a>'
    cards = [f'<a href="/neighborhoods/{a["slug"]}/" class="city-card">{a["name"]} <span class="arrow">›</span></a>'
             for a in AREAS if f'/neighborhoods/{a["slug"]}/' not in hub]
    if cards and anchor in hub:
        hub = hub.replace(anchor, anchor + "".join("\n " + c for c in cards), 1)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    open("neighborhoods/index.html", "w", encoding="utf-8").write(hub)


if __name__ == "__main__":
    main()
