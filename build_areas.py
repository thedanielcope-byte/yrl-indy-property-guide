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
  comms=[],
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
  schools="Most of Decatur Township is served by the <a href="/schools/decatur-township-schools/">Metropolitan School District of Decatur Township</a>, whose high school is Decatur Central High School on Kentucky Avenue. Some neighborhoods near the county line, including parts of Heartland Crossing, are served by <a href=\"/schools/mooresville-consolidated-schools/\">Mooresville Consolidated Schools</a> instead. School assignment really does depend on the address, so confirm it with the district before you buy.",
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
]

SIBLINGS = [("/neighborhoods/perry-township-indianapolis/", "Perry Township"), ("/neighborhoods/center-grove-indiana/", "Center Grove"),
            ("/neighborhoods/franklin-township-indianapolis/", "Franklin Township"), ("/neighborhoods/decatur-township-indianapolis/", "Decatur Township"),
            ("/neighborhoods/pike-township-indianapolis/", "Pike Township")]


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
    if comms:
        comm_block = (f' <h2>Communities &amp; Subdivisions in {name}</h2>\n <p>A few of the neighborhoods buyers ask us about most:</p>\n <div class="city-grid">\n' +
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
