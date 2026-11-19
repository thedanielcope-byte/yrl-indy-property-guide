"""What county is it in? Indianapolis-area towns and neighborhoods by county (Nov 2026).

Search evidence (GSC/Bing, Nov 2026): "what county is fishers indiana in" 53 impr @10.7, "zionsville county"
35 @23.6, "what county is broad ripple in" 24 @10, "what county is zionsville in" 22 @23, "what county is
noblesville in" 20 @11; Bing "hamilton county indiana county seat".

Sources and verification (checked Nov 19 2026):
- TOWN LISTS: county_towns.json (123 unique incorporated places across our 17 counties) checked row by row
  against the U.S. Census Bureau 2020 place-by-county file (st18_in_place_by_county2020.txt). Every row
  matched. The Census file adds two county parts the JSON leaves out: Jamestown also lies in Hendricks
  County and Edinburgh also lies in Bartholomew County; both are shown. City vs. town labels are the
  Census legal names; no name/type changed between the 2020 file and the Vintage 2025 estimates file.
- MULTI-COUNTY SPLITS: Census Vintage 2025 subcounty population estimates (sub-est2025_18.csv, place
  parts, SUMLEV 157): Cumberland Hancock 5,535 / Marion 2,531; Edinburgh Johnson 3,987 / Bartholomew 393 /
  Shelby 195; Shirley Hancock 628 / Henry 223; St. Paul Decatur 595 / Shelby 379; Jamestown Boone 938 /
  Hendricks 22; Elwood Madison 8,518 / Tipton 7; Chesterfield Madison 2,517 / Delaware 6. Same file:
  Plainfield 38,574, Brownsburg 34,089, Danville 13,415; Seymour 22,450, Brownstown 3,154; North Vernon
  6,559, Vernon 232; Southport 2,094.
- COUNTY SEATS: in.gov DCS county list ("with county seats") for all 17 counties: Marion-Indianapolis,
  Hamilton-Noblesville, Johnson-Franklin, Hendricks-Danville, Boone-Lebanon, Hancock-Greenfield,
  Madison-Anderson, Shelby-Shelbyville, Morgan-Martinsville, Montgomery-Crawfordsville, Decatur-Greensburg,
  Brown-Nashville, Putnam-Greencastle, Parke-Rockville, Bartholomew-Columbus, Jackson-Brownstown,
  Jennings-Vernon. Matches inject_county_faq.py SEATS and our county hubs.
- UNIGOV: Encyclopedia of Indianapolis "Structure of Unigov" (took effect Jan 1 1970; city grew from 82 to
  402 sq mi; nine townships remain separate; eleven public school districts remain), "Excluded Cities"
  (Beech Grove, Lawrence, Southport, and the town of Speedway; residents vote for mayor + City-County
  Council and pay countywide taxes; Southport annexed land just before Unigov to qualify), "Included
  Towns". Census lists 11 included towns today (10 + Cumberland), matching Wikipedia's Unigov article.
- CUMBERLAND 2027: Town of Cumberland HB 1131 page (excluded from Unigov effective Jan 1 2027; stays a
  town); IBJ Jan 31 2025 on the bill. The town page and other reports give different signing dates, so
  no signing date is stated.
- TOWNSHIPS: Marion County town/township pairs come from DLGF 2026 certified tax district names (e.g.
  "BEECH GROVE PERRY", "CLERMONT WAYNE", "TOWN OF SPEEDWAY" 914, "CITY OF SOUTHPORT" 513) plus Wikipedia
  township articles. Neighborhoods: Broad Ripple, Meridian-Kessler, Nora in Washington Twp; Irvington in
  Warren Twp; Fountain Square in Center Twp; Castleton mostly Lawrence Twp (partly Washington); Geist in
  Lawrence Twp (Marion side); Eagle Creek Park in Pike Twp; Camby in Decatur Twp, and the Camby area also
  reaches Hendricks and Morgan counties (Wikipedia, Decatur Township). Broad Ripple a town 1884, annexed
  1922; Irvington a town 1873, annexed 1902; Castleton dissolved as a town Nov 1991 (Encyclopedia).
- GEIST: reservoir in Marion, Hamilton and Hancock counties, mainly NE Indianapolis and SE Fishers with
  small portions in Lawrence, Fortville and McCordsville (Wikipedia; Encyclopedia of Indianapolis).
- TAXES: DLGF 2026 Certified Tax Rates by District (gross rate per $100 AV): Carmel 2.0167, Fishers
  2.1994, Noblesville City 2.5549, Indianapolis-Center 2.7291, Speedway 3.1302, Beech Grove-Center 4.2369,
  Cumberland Marion side 3.8817, Cumberland Hancock side (Buck Creek Twp) 3.1218. DLGF Citizen's Guide
  defines a taxing district. Caps 1%/2% per DLGF circuit-breaker fact sheet. County income tax rates from
  DOR Departmental Notice #1 eff. Oct 1 2026 (Hamilton 1.10, Johnson 1.40, Hendricks 1.70, Shelby 1.70,
  Boone 1.71, Hancock 1.94, Marion 2.02, Madison 2.25, Morgan 2.72). Center Grove schools serve parts of
  western Greenwood and most of Bargersville (Wikipedia).
Consistent with inject_county_faq.py: Plainfield is not the Hendricks seat (Danville is); Monrovia is in
Morgan; Shirley, Elwood, Chesterfield and Cumberland span two counties; Geist straddles Marion/Hamilton.
Found but NOT fixed here (other files): the Plainfield city page still calls Plainfield the county seat,
the North Vernon page's schools line calls North Vernon the county seat (Vernon is), and the Jamestown and
Edinburgh city-page FAQs don't mention their second/third counties.
Dropped: Center Grove as a table row (it's a school district, not a place; mentioned in text only);
directional labels (NE Morgan etc.) and population for every town.
"""


def _c(county, slug, kind="indiana"):
    return f"/cities/{county}-county/{slug}-{kind}-real-estate/"


def _hub(county):
    return f"/counties/{county}-county-indiana-real-estate/"


def _nb(slug):
    return f"/neighborhoods/{slug}/"


def _name(n, href):
    return f'<a href="{href}">{n}</a>' if href else n


def _table(rows, head=("City or town", "Type", "Notes")):
    body = "\n".join(" <tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    th = "".join(f"<th>{h}</th>" for h in head)
    return f' <table class="data-table">\n <thead><tr>{th}</tr></thead>\n <tbody>\n{body}\n </tbody>\n </table>'


def _county(rows):
    # rows: (name, type, note, href)
    return _table([(_name(n, h), t, note) for n, t, note, h in rows])


SEAT = "<strong>County seat</strong>"

# ---------------------------------------------------------------- county seats
_SEATS = [
    ("Bartholomew", "bartholomew", "Columbus", _c("bartholomew", "columbus")),
    ("Boone", "boone", "Lebanon", _c("boone", "lebanon")),
    ("Brown", "brown", "Nashville", _c("brown", "nashville")),
    ("Decatur", "decatur", "Greensburg", _c("decatur", "greensburg")),
    ("Hamilton", "hamilton", "Noblesville", _c("hamilton", "noblesville")),
    ("Hancock", "hancock", "Greenfield", _c("hancock", "greenfield")),
    ("Hendricks", "hendricks", "Danville", _c("hendricks", "danville")),
    ("Jackson", "jackson", "Brownstown", None),
    ("Jennings", "jennings", "Vernon", None),
    ("Johnson", "johnson", "Franklin", _c("johnson", "franklin")),
    ("Madison", "madison", "Anderson", _c("madison", "anderson")),
    ("Marion", "marion", "Indianapolis", "/indianapolis-real-estate/"),
    ("Montgomery", "montgomery", "Crawfordsville", _c("montgomery", "crawfordsville")),
    ("Morgan", "morgan", "Martinsville", _c("morgan", "martinsville")),
    ("Parke", "parke", "Rockville", _c("parke", "rockville")),
    ("Putnam", "putnam", "Greencastle", _c("putnam", "greencastle")),
    ("Shelby", "shelby", "Shelbyville", _c("shelby", "shelbyville")),
]
_SEATS_TABLE = _table([(f'<a href="{_hub(s)}">{c} County</a>', _name(seat, h)) for c, s, seat, h in _SEATS],
                      head=("County", "County seat"))

# ---------------------------------------------------------------- Marion County
_MARION = [
    ("Indianapolis", "All nine", "County seat; consolidated city-county", "/indianapolis-real-estate/"),
    ("Beech Grove", "Center, Franklin, Perry, Warren", "Excluded city", _c("marion", "beech-grove")),
    ("Clermont", "Pike, Wayne", "Included town", _c("marion", "clermont")),
    ("Crows Nest", "Washington", "Included town", None),
    ("Cumberland", "Warren", "Included town; excluded from Jan. 1, 2027; also in Hancock County", _c("hancock", "cumberland")),
    ("Homecroft", "Perry", "Included town", _c("marion", "homecroft")),
    ("Lawrence", "Lawrence", "Excluded city", _c("marion", "lawrence")),
    ("Meridian Hills", "Washington", "Included town", _c("marion", "meridian-hills")),
    ("North Crows Nest", "Washington", "Included town", None),
    ("Rocky Ripple", "Washington", "Included town", None),
    ("Southport", "Perry", "Excluded city", _c("marion", "southport")),
    ("Speedway", "Wayne", "Excluded town", _c("marion", "speedway")),
    ("Spring Hill", "Washington", "Included town", None),
    ("Warren Park", "Warren", "Included town", None),
    ("Williams Creek", "Washington", "Included town", None),
    ("Wynnedale", "Washington", "Included town", None),
]
_MARION_TABLE = _table([(_name(n, h), t, s) for n, t, s, h in _MARION], head=("City or town", "Township", "Status"))

_TWP = {t: _nb(f"{t.lower()}-township-indianapolis") for t in
        ("Center", "Decatur", "Franklin", "Lawrence", "Perry", "Pike", "Warren", "Washington", "Wayne")}

_HOODS = [
    ("Broad Ripple", _c("marion", "broad-ripple", "indianapolis"), "Washington", "A town from 1884 until Indianapolis annexed it in 1922"),
    ("Irvington", _c("marion", "irvington", "indianapolis"), "Warren", "A town from 1873 until Indianapolis annexed it in 1902"),
    ("Fountain Square", _nb("fountain-square-indianapolis"), "Center", "Near-southeast side, close to downtown"),
    ("Castleton", _nb("castleton-indianapolis"), "Lawrence", "Mostly Lawrence Township; a town until it dissolved in 1991"),
    ("Eagle Creek", _c("marion", "eagle-creek", "indianapolis"), "Pike", "Northwest side, around Eagle Creek Park"),
    ("Geist", _c("marion", "geist"), "Lawrence", "The reservoir also reaches Hamilton and Hancock counties"),
    ("Meridian-Kessler", _nb("meridian-kessler-indianapolis"), "Washington", "North side"),
    ("Nora", _nb("nora-indianapolis"), "Washington", "North side"),
    ("Camby", _c("marion", "camby"), "Decatur", "The Camby area also reaches Hendricks and Morgan counties"),
]
_HOODS_TABLE = _table([(f'<a href="{h}">{n}</a>', f'<a href="{_TWP[t]}">{t}</a>', note) for n, h, t, note in _HOODS],
                      head=("Neighborhood", "Township", "What to know"))
_TWP_LINKS = ", ".join(f'<a href="{_TWP[t]}">{t}</a>' for t in _TWP)

# ---------------------------------------------------------------- suburban counties
_HAMILTON = _county([
    ("Arcadia", "Town", "", _c("hamilton", "arcadia")),
    ("Atlanta", "Town", "", _c("hamilton", "atlanta")),
    ("Carmel", "City", "", _c("hamilton", "carmel")),
    ("Cicero", "Town", "", _c("hamilton", "cicero")),
    ("Fishers", "City", "", _c("hamilton", "fishers")),
    ("Noblesville", "City", SEAT, _c("hamilton", "noblesville")),
    ("Sheridan", "Town", "", _c("hamilton", "sheridan")),
    ("Westfield", "City", "", _c("hamilton", "westfield")),
])
_BOONE = _county([
    ("Advance", "Town", "", None),
    ("Jamestown", "Town", "A sliver (about 20 residents) is in Hendricks County", _c("boone", "jamestown")),
    ("Lebanon", "City", SEAT, _c("boone", "lebanon")),
    ("Thorntown", "Town", "", _c("boone", "thorntown")),
    ("Ulen", "Town", "", None),
    ("Whitestown", "Town", "", _c("boone", "whitestown")),
    ("Zionsville", "Town", "", _c("boone", "zionsville")),
])
_HENDRICKS = _county([
    ("Amo", "Town", "", None),
    ("Avon", "Town", "", _c("hendricks", "avon")),
    ("Brownsburg", "Town", "", _c("hendricks", "brownsburg")),
    ("Clayton", "Town", "", _c("hendricks", "clayton")),
    ("Coatesville", "Town", "", _c("hendricks", "coatesville")),
    ("Danville", "Town", SEAT, _c("hendricks", "danville")),
    ("Jamestown", "Town", "Almost entirely in Boone County", _c("boone", "jamestown")),
    ("Lizton", "Town", "", None),
    ("North Salem", "Town", "", None),
    ("Pittsboro", "Town", "", _c("hendricks", "pittsboro")),
    ("Plainfield", "Town", "Largest town, but not the county seat", _c("hendricks", "plainfield")),
    ("Stilesville", "Town", "", None),
])
_MORGAN = _county([
    ("Bethany", "Town", "", None),
    ("Brooklyn", "Town", "", _c("morgan", "brooklyn")),
    ("Martinsville", "City", SEAT, _c("morgan", "martinsville")),
    ("Monrovia", "Town", "", _c("morgan", "monrovia")),
    ("Mooresville", "Town", "", _c("morgan", "mooresville")),
    ("Morgantown", "Town", "", None),
    ("Paragon", "Town", "", None),
])
_JOHNSON = _county([
    ("Bargersville", "Town", "", _c("johnson", "bargersville")),
    ("Edinburgh", "Town", "Small parts are in Bartholomew and Shelby counties", _c("johnson", "edinburgh")),
    ("Franklin", "City", SEAT, _c("johnson", "franklin")),
    ("Greenwood", "City", "", _c("johnson", "greenwood")),
    ("New Whiteland", "Town", "", _c("johnson", "new-whiteland")),
    ("Prince&rsquo;s Lakes", "Town", "", _c("johnson", "princes-lakes")),
    ("Trafalgar", "Town", "", _c("johnson", "trafalgar")),
    ("Whiteland", "Town", "", _c("johnson", "whiteland")),
])
_SHELBY = _county([
    ("Edinburgh", "Town", "Mostly in Johnson County", _c("johnson", "edinburgh")),
    ("Fairland", "Town", "", _c("shelby", "fairland")),
    ("Morristown", "Town", "", _c("shelby", "morristown")),
    ("St. Paul", "Town", "Also in Decatur County, where most residents live", None),
    ("Shelbyville", "City", SEAT, _c("shelby", "shelbyville")),
    ("Waldron", "Unincorporated", "Census-designated place, not a town", _c("shelby", "waldron")),
])
_HANCOCK = _county([
    ("Cumberland", "Town", "West side is in Marion County; about two-thirds of residents live on the Hancock side", _c("hancock", "cumberland")),
    ("Fortville", "Town", "", _c("hancock", "fortville")),
    ("Greenfield", "City", SEAT, _c("hancock", "greenfield")),
    ("McCordsville", "Town", "", _c("hancock", "mccordsville")),
    ("New Palestine", "Town", "", _c("hancock", "new-palestine")),
    ("Shirley", "Town", "The smaller east side is in Henry County", _c("hancock", "shirley")),
    ("Spring Lake", "Town", "", None),
    ("Wilkinson", "Town", "", None),
])
_MADISON = _county([
    ("Alexandria", "City", "", _c("madison", "alexandria")),
    ("Anderson", "City", SEAT, _c("madison", "anderson")),
    ("Chesterfield", "Town", "A tiny part is in Delaware County", _c("madison", "chesterfield")),
    ("Country Club Heights", "Town", "", None),
    ("Edgewood", "Town", "", None),
    ("Elwood", "City", "A tiny part is in Tipton County", _c("madison", "elwood")),
    ("Frankton", "Town", "", _c("madison", "frankton")),
    ("Ingalls", "Town", "", _c("madison", "ingalls")),
    ("Lapel", "Town", "", _c("madison", "lapel")),
    ("Markleville", "Town", "", None),
    ("Orestes", "Town", "", None),
    ("Pendleton", "Town", "", _c("madison", "pendleton")),
    ("River Forest", "Town", "", None),
    ("Summitville", "Town", "", None),
    ("Woodlawn Heights", "Town", "", None),
])

# ---------------------------------------------------------------- outer counties
_MONTGOMERY = _county([
    ("Alamo", "Town", "", None),
    ("Crawfordsville", "City", SEAT, _c("montgomery", "crawfordsville")),
    ("Darlington", "Town", "", None),
    ("Ladoga", "Town", "", None),
    ("Linden", "Town", "", None),
    ("New Market", "Town", "", None),
    ("New Richmond", "Town", "", None),
    ("New Ross", "Town", "", None),
    ("Waveland", "Town", "", None),
    ("Waynetown", "Town", "", None),
    ("Wingate", "Town", "", None),
])
_PUTNAM = _county([
    ("Bainbridge", "Town", "", None),
    ("Cloverdale", "Town", "", _c("putnam", "cloverdale")),
    ("Fillmore", "Town", "", None),
    ("Greencastle", "City", SEAT, _c("putnam", "greencastle")),
    ("Roachdale", "Town", "", None),
    ("Russellville", "Town", "", None),
])
_PARKE = _county([
    ("Bloomingdale", "Town", "", None),
    ("Marshall", "Town", "", None),
    ("Mecca", "Town", "", None),
    ("Montezuma", "Town", "", None),
    ("Rockville", "Town", SEAT, _c("parke", "rockville")),
    ("Rosedale", "Town", "", None),
])
_BROWN = _county([
    ("Bean Blossom", "Unincorporated", "Community in Jackson Township", _c("brown", "bean-blossom")),
    ("Nashville", "Town", SEAT + "; the county&rsquo;s only incorporated town", _c("brown", "nashville")),
])
_BARTHOLOMEW = _county([
    ("Clifford", "Town", "", None),
    ("Columbus", "City", SEAT, _c("bartholomew", "columbus")),
    ("Edinburgh", "Town", "Mostly in Johnson County", _c("johnson", "edinburgh")),
    ("Elizabethtown", "Town", "", None),
    ("Hartsville", "Town", "", None),
    ("Hope", "Town", "", None),
    ("Jonesville", "Town", "", None),
])
_JACKSON = _county([
    ("Brownstown", "Town", SEAT, None),
    ("Crothersville", "Town", "", None),
    ("Medora", "Town", "", None),
    ("Seymour", "City", "Largest community, but not the county seat", _c("jackson", "seymour")),
])
_JENNINGS = _county([
    ("North Vernon", "City", "Largest community, but not the county seat", _c("jennings", "north-vernon")),
    ("Vernon", "Town", SEAT, None),
])
_DECATUR = _county([
    ("Greensburg", "City", SEAT, _c("decatur", "greensburg")),
    ("Millhousen", "Town", "", None),
    ("New Point", "Town", "", None),
    ("St. Paul", "Town", "Also in Shelby County", None),
    ("Westport", "Town", "", _c("decatur", "westport")),
])

# ---------------------------------------------------------------- two-county towns
_SPLIT_TABLE = _table([
    (_name("Cumberland", _c("hancock", "cumberland")), "Hancock &amp; Marion", "5,535 Hancock &middot; 2,531 Marion"),
    (_name("Edinburgh", _c("johnson", "edinburgh")), "Johnson, Bartholomew &amp; Shelby", "3,987 Johnson &middot; 393 Bartholomew &middot; 195 Shelby"),
    (_name("Shirley", _c("hancock", "shirley")), "Hancock &amp; Henry", "628 Hancock &middot; 223 Henry"),
    ("St. Paul", "Decatur &amp; Shelby", "595 Decatur &middot; 379 Shelby"),
    (_name("Jamestown", _c("boone", "jamestown")), "Boone &amp; Hendricks", "938 Boone &middot; 22 Hendricks"),
    (_name("Elwood", _c("madison", "elwood")), "Madison &amp; Tipton", "8,518 Madison &middot; 7 Tipton"),
    (_name("Chesterfield", _c("madison", "chesterfield")), "Madison &amp; Delaware", "2,517 Madison &middot; 6 Delaware"),
], head=("Town", "Counties", "Residents by county (2025 est.)"))

# ---------------------------------------------------------------- tax rates
_RATES_TABLE = _table([
    (_name("Carmel", _c("hamilton", "carmel")), "Hamilton", "$2.02"),
    (_name("Fishers", _c("hamilton", "fishers")), "Hamilton", "$2.20"),
    (_name("Noblesville", _c("hamilton", "noblesville")) + " (city)", "Hamilton", "$2.55"),
    ("Indianapolis, Center Township", "Marion", "$2.73"),
    (_name("Speedway", _c("marion", "speedway")), "Marion", "$3.13"),
    (_name("Beech Grove", _c("marion", "beech-grove")) + ", Center Township", "Marion", "$4.24"),
    (_name("Cumberland", _c("hancock", "cumberland")) + ", Hancock side (Buck Creek Twp.)", "Hancock", "$3.12"),
    ("Cumberland, Marion side", "Marion", "$3.88"),
], head=("Taxing district", "County", "2026 gross rate per $100 of assessed value"))

_INCOME_TABLE = _table([
    ("Hamilton", "1.10%"), ("Johnson", "1.40%"), ("Hendricks", "1.70%"), ("Shelby", "1.70%"), ("Boone", "1.71%"),
    ("Hancock", "1.94%"), ("Marion", "2.02%"), ("Madison", "2.25%"), ("Morgan", "2.72%"),
], head=("County you live in on January 1", "County income tax (2026)"))


def _h3(county, slug, line, table):
    return (f' <h3>{county} County</h3>\n <p>{line} See our <a href="{_hub(slug)}">{county} County real estate guide</a>.</p>\n'
            f'{table}\n')


_SUBURBAN = "\n".join([
    _h3("Hamilton", "hamilton", "County seat: <strong>Noblesville</strong>. North of Indianapolis, and home to Carmel, Fishers and Westfield.", _HAMILTON),
    _h3("Boone", "boone", "County seat: <strong>Lebanon</strong>. Northwest of Indianapolis, and home to Zionsville and Whitestown.", _BOONE),
    _h3("Hendricks", "hendricks", "County seat: <strong>Danville</strong>. West of Indianapolis, and home to Avon, Brownsburg and Plainfield.", _HENDRICKS),
    _h3("Morgan", "morgan", "County seat: <strong>Martinsville</strong>. Southwest of Indianapolis, and home to Mooresville.", _MORGAN),
    _h3("Johnson", "johnson", "County seat: <strong>Franklin</strong>. South of Indianapolis, and home to Greenwood. Center Grove isn&rsquo;t a "
        "town: it&rsquo;s the school district that serves parts of western Greenwood and most of Bargersville (see our "
        '<a href="/neighborhoods/center-grove-indiana/">Center Grove guide</a>).', _JOHNSON),
    _h3("Shelby", "shelby", "County seat: <strong>Shelbyville</strong>. Southeast of Indianapolis.", _SHELBY),
    _h3("Hancock", "hancock", "County seat: <strong>Greenfield</strong>. East of Indianapolis, and home to McCordsville, Fortville and New Palestine.", _HANCOCK),
    _h3("Madison", "madison", "County seat: <strong>Anderson</strong>. Northeast of Indianapolis, bordering Hamilton and Hancock counties.", _MADISON),
])

_OUTER = "\n".join([
    _h3("Montgomery", "montgomery", "County seat: <strong>Crawfordsville</strong>.", _MONTGOMERY),
    _h3("Putnam", "putnam", "County seat: <strong>Greencastle</strong>.", _PUTNAM),
    _h3("Parke", "parke", "County seat: <strong>Rockville</strong>.", _PARKE),
    _h3("Brown", "brown", "County seat: <strong>Nashville</strong>.", _BROWN),
    _h3("Bartholomew", "bartholomew", "County seat: <strong>Columbus</strong>.", _BARTHOLOMEW),
    _h3("Jackson", "jackson", "County seat: <strong>Brownstown</strong>.", _JACKSON),
    _h3("Jennings", "jennings", "County seat: <strong>Vernon</strong>.", _JENNINGS),
    _h3("Decatur", "decatur", "County seat: <strong>Greensburg</strong>.", _DECATUR),
])


HOMESTEAD = "/blog/indiana-homestead-exemption-lower-property-taxes/"

POST = dict(
 slug="what-county-is-it-in-indianapolis-area-towns-by-county",
 title="What County Is It In? Indianapolis-Area Towns by County",
 headline="What County Is It In? Indianapolis-Area Towns and Neighborhoods by County",
 h1_html="What County Is It In? <em>Indianapolis-Area Towns by County</em>",
 desc=("What county is Fishers, Zionsville or Broad Ripple in? Every Indianapolis-area city and town by "
       "county, plus county seats and towns that cross county lines."),
 date="2026-11-19", month="November 2026", category="Relocation", eyebrow="RELOCATION",
 focus="indianapolis area towns by county",
 hero_sub=("Every city and town around Indianapolis by county, plus the neighborhoods people mistake for towns, "
           "the county seats and why the county matters when you buy."),
 badges=["Relocation", "17 Counties", "Updated November 2026"], read_min=11,
 card_title="What County Is It In?", card_sub="Indianapolis-area towns and neighborhoods by county, with every county seat.",
 qa_heading="Quick Answer: Which County Is It In?",
 qa_lead=("<strong>What county is Fishers, Indiana in?</strong> Hamilton County, along with Carmel, Westfield and "
          "Noblesville, which is the county seat. Zionsville is in Boone County, Greenwood is in Johnson County and "
          "Avon is in Hendricks County. Broad Ripple isn&rsquo;t a town at all: it&rsquo;s an Indianapolis "
          "neighborhood in Marion County. (Checked against Census and state sources, November 2026.)"),
 qa_facts=[("Fishers, Carmel, Westfield, Noblesville", "Hamilton County (seat: Noblesville)"),
           ("Zionsville, Whitestown, Lebanon", "Boone County (seat: Lebanon)"),
           ("Broad Ripple, Irvington, Fountain Square", "Marion County, part of Indianapolis"),
           ("Greenwood, Franklin, Bargersville", "Johnson County (seat: Franklin)"),
           ("Avon, Plainfield, Brownsburg", "Hendricks County (seat: Danville)"),
           ("Cumberland", "Marion and Hancock counties")],
 toc=[("county-seats", "County Seats Around Indianapolis"), ("marion-county", "Marion County and Unigov"),
      ("neighborhoods", "Neighborhoods People Mistake for Towns"), ("suburban-counties", "Towns in the Suburban Counties"),
      ("outer-counties", "Towns in the Outer Counties"), ("two-counties", "Towns That Cross County Lines"),
      ("why-it-matters", "Why the County Matters When You Buy"), ("check-an-address", "How to Check Any Address")],
 body=f"""
 <p>&ldquo;What county is that in?&rdquo; is one of the most common questions we get from people moving to Central Indiana, and it&rsquo;s a fair one. Fishers and Indianapolis share a border but not a county, Broad Ripple sounds like a town but isn&rsquo;t one, and a few towns sit in two counties at once. Below is every incorporated city and town in the 17 counties our team covers, grouped by county, with the county seats marked and links to our guide for each place. The town lists come from the U.S. Census Bureau, and the county seats from the State of Indiana. If you&rsquo;re still choosing where to live, start with our <a href="/blog/moving-to-indianapolis-relocation-guide/">Indianapolis relocation guide</a>.</p>

 <h2 id="county-seats">County Seats Around Indianapolis</h2>
 <p>The county seat is where the courthouse and most county offices are, including the auditor, assessor, treasurer and recorder you&rsquo;ll deal with as a homeowner. Here are the seats for all 17 counties, according to the State of Indiana:</p>
{_SEATS_TABLE}
 <p>Three seats trip people up because they aren&rsquo;t the county&rsquo;s biggest town. <strong>Plainfield is not the Hendricks County seat; Danville is</strong>, even though Plainfield (about 38,600 residents) and Brownsburg (about 34,100) are both larger than Danville (about 13,400), according to Census Bureau estimates for 2025. In Jackson County, Seymour (about 22,500) is the biggest city, but the seat is Brownstown (about 3,200). And in Jennings County, the seat is the town of Vernon (about 230), not North Vernon (about 6,600).</p>

 <h2 id="marion-county">Marion County: Indianapolis and Unigov</h2>
 <p>Indianapolis and Marion County have run as one consolidated government, known as <strong>Unigov</strong>, since January 1, 1970. Unigov grew the city from about 82 square miles to 402 and made almost all of the county part of Indianapolis, with one mayor elected countywide and a single City-County Council (Encyclopedia of Indianapolis). Three things were left out of the merger, and they still matter when you buy:</p>
 <ul>
 <li><strong>Excluded cities.</strong> The cities of Beech Grove, Lawrence and Southport and the town of Speedway kept their own governments. They&rsquo;re in Marion County but not part of the City of Indianapolis, although their residents still vote for the mayor and City-County Council and pay countywide taxes. Southport only qualified because it annexed enough land to meet the population requirement just before Unigov took effect.</li>
 <li><strong>Included towns.</strong> Eleven towns are part of the consolidated city but keep a town government with limited powers.</li>
 <li><strong>Townships and schools.</strong> All nine townships remain separate governments, and eleven public school districts still operate inside the county.</li>
 </ul>
 <p>One change is coming: under a 2025 state law, Cumberland&rsquo;s Marion County side leaves the consolidated city and becomes an excluded town on <strong>January 1, 2027</strong>. Cumberland stays a town, and the change puts zoning, permits and code enforcement for its Marion County side in the town&rsquo;s hands (Town of Cumberland).</p>
{_MARION_TABLE}
 <p>The township matters because it&rsquo;s part of your property tax district and, in much of the county, it decides your public school district. Our guide to <a href="{_hub('marion')}">Marion County real estate</a> covers the county as a whole, and our <a href="/indianapolis-real-estate/">Indianapolis real estate guide</a> covers the city.</p>

 <h2 id="neighborhoods">Indianapolis Neighborhoods People Mistake for Towns</h2>
 <p>Plenty of names you&rsquo;ll see on listings are neighborhoods of Indianapolis, not separate towns. Every one of these is in <strong>Marion County</strong> and part of the City of Indianapolis (Geist and Camby also spill into neighboring counties). A few really were towns once:</p>
{_HOODS_TABLE}
 <p>So the answer to &ldquo;what county is Broad Ripple in?&rdquo; is Marion County: it&rsquo;s an Indianapolis neighborhood in Washington Township, and it hasn&rsquo;t been a separate town since 1922 (Encyclopedia of Indianapolis). Geist is the one name on this list that crosses county lines. Geist Reservoir sits mainly in northeast Indianapolis and southeast Fishers, so it touches Marion and Hamilton counties, with small portions reaching into Hancock County near Fortville and McCordsville. Our <a href="{_nb('geist-reservoir-indianapolis')}">Geist Reservoir guide</a> has more.</p>
 <p>Southport is the opposite case: it&rsquo;s a real city with its own government, but a small one, with about 2,100 residents. The Southport name is used much more widely across the south side, so a home described as &ldquo;in Southport&rdquo; may actually be in Indianapolis&rsquo;s Perry Township. The property record tells you which.</p>
 <p>Township names cause their own mix-ups. <strong>Franklin Township</strong> is an Indianapolis township in the southeast corner of Marion County, while the city of <a href="{_c('johnson', 'franklin')}">Franklin</a> is the Johnson County seat. <strong>Lawrence Township</strong> includes the city of <a href="{_c('marion', 'lawrence')}">Lawrence</a> but also Indianapolis neighborhoods such as Castleton and the Marion County side of Geist. Marion County&rsquo;s nine townships are {_TWP_LINKS}, and each link goes to our area guide.</p>

 <h2 id="suburban-counties">Towns in the Suburban Counties</h2>
 <p>Seven counties border Marion County: Boone, Hamilton, Hancock, Shelby, Johnson, Morgan and Hendricks. Madison County, to the northeast, rounds out the suburban ring. &ldquo;Type&rdquo; is each place&rsquo;s legal status as listed by the Census Bureau; in Indiana, a town can be bigger than a city (Zionsville and Plainfield are both towns).</p>

{_SUBURBAN}
 <h2 id="outer-counties">Towns in the Outer Counties</h2>
 <p>Our team also serves these more rural counties farther from the city. Many of their towns are small, and some don&rsquo;t have a guide on our site yet, but we still help buyers and sellers there.</p>

{_OUTER}
 <h2 id="two-counties">Towns That Cross County Lines</h2>
 <p>Seven cities and towns in our area sit in more than one county, according to the Census Bureau. In Elwood, Chesterfield and Jamestown the second county holds only a handful of residents, but Cumberland, St. Paul and Shirley have a real share on each side:</p>
{_SPLIT_TABLE}
 <p style="font-size:.85rem;color:var(--gray);">Source: U.S. Census Bureau, Vintage 2025 population estimates for city and town parts by county (2020 boundaries file for which counties each town touches).</p>
 <p>If you&rsquo;re buying in one of these towns, check the county for the exact address. It changes the property tax rate, the county income tax and which county offices you deal with, and in Cumberland&rsquo;s case, whether you&rsquo;re on the Indianapolis side of the line until 2027.</p>

 <h2 id="why-it-matters">Why the County Matters When You Buy</h2>
 <h3>Property taxes</h3>
 <p>Indiana sets property tax rates by <strong>taxing district</strong>, which the Department of Local Government Finance defines as all the local units (county, township, city or town, school corporation, library and others) that serve the same area. Two homes in the same county, or even the same town, can carry different rates:</p>
{_RATES_TABLE}
 <p style="font-size:.85rem;color:var(--gray);">Source: Indiana DLGF, 2026 certified tax rates by district (gross rates, rounded). Bills are figured on assessed value after deductions, minus credits.</p>
 <p>A higher rate doesn&rsquo;t raise every bill one-for-one, because Indiana caps a primary home&rsquo;s tax bill at <strong>1% of its assessed value</strong> once you file for the homestead deduction (2% for rentals and other residential property). That cap is why the <a href="{HOMESTEAD}">homestead deduction</a> is worth filing right after you close, and our guide to <a href="/blog/indiana-property-tax-caps-explained/">Indiana&rsquo;s property tax caps</a> explains how it works. The rate still matters for rentals and second homes, and in districts where the bill lands under the cap.</p>
 <h3>County income tax</h3>
 <p>Every Indiana county adds its own income tax on top of the state&rsquo;s, based on the county you live in on January 1. Around Indianapolis, the 2026 rates range from 1.10% in Hamilton County to 2.72% in Morgan County (Indiana Department of Revenue, rates effective October 1, 2026):</p>
{_INCOME_TABLE}
 <p>On a $100,000 household income, the gap between Hamilton and Marion counties is roughly $900 a year before exemptions. Our <a href="/blog/cost-of-living-in-indianapolis/">cost of living breakdown</a> puts that next to rents and home prices.</p>
 <h3>County offices, schools and vehicles</h3>
 <ul>
 <li><strong>Homestead deduction:</strong> you file it with the county auditor, and filing by January 15 gets it onto that year&rsquo;s tax bills. Our <a href="{HOMESTEAD}">homestead guide</a> walks through it.</li>
 <li><strong>Assessed value:</strong> your property record and assessed value come from the county assessor&rsquo;s office, and appeals start there too (see <a href="/blog/how-to-appeal-your-property-tax-assessment-in-indiana/">how to appeal your assessment</a>).</li>
 <li><strong>Schools:</strong> school districts follow their own boundaries, not county or town lines. Marion County alone has eleven. Confirm the district for the exact address with our <a href="/schools/">Central Indiana schools guide</a>.</li>
 <li><strong>Vehicles:</strong> some counties add a county excise surtax or wheel tax when you register a vehicle, so your county affects what you pay at the BMV. Our <a href="/blog/moving-to-indiana-checklist/">moving to Indiana checklist</a> covers the BMV deadlines.</li>
 </ul>

 <h2 id="check-an-address">How to Check the County for Any Address</h2>
 <p>Don&rsquo;t rely on the mailing address. The city name the Postal Service assigns doesn&rsquo;t always match the town or county a home is in, and names like Camby, Geist and Southport are used across several jurisdictions. The reliable check is the county&rsquo;s own property record: search the address on the county assessor&rsquo;s or GIS site (the State of Indiana&rsquo;s county map links to every county&rsquo;s website), and the record will show the county, township and taxing district. If you&rsquo;re looking at a specific home, our team can check it with you before you make an offer.</p>
 """,
 faqs=[
  ("What county is Fishers, Indiana in?",
   "Fishers is in Hamilton County, just northeast of Indianapolis. Carmel, Westfield and Noblesville are in Hamilton County too, and Noblesville is the county seat. The city of Fishers lies entirely within Hamilton County."),
  ("What county is Zionsville, Indiana in?",
   "Zionsville is in Boone County, northwest of Indianapolis. Lebanon is the Boone County seat, and Whitestown, Thorntown and Jamestown are also in Boone County. Zionsville is a town, not a city, even though it has more than 30,000 residents."),
  ("What county is Broad Ripple in?",
   "Broad Ripple is in Marion County. It's a neighborhood of the City of Indianapolis in Washington Township, not a separate town. It was its own town from 1884 until Indianapolis annexed it in 1922."),
  ("What is the county seat of Hamilton County, Indiana?",
   "Noblesville is the county seat of Hamilton County. The county's courthouse and most county offices are there, even though Carmel and Fishers are larger cities."),
  ("Is Plainfield the county seat of Hendricks County?",
   "No. Danville is the county seat of Hendricks County. Plainfield is the county's largest town, with about 38,600 residents in 2025, but it isn't the seat."),
  ("Is Beech Grove part of Indianapolis?",
   "Beech Grove is in Marion County but isn't part of the City of Indianapolis. It's one of four excluded communities under Unigov, along with Lawrence, Southport and Speedway, that keep their own governments. Their residents still vote for the Indianapolis mayor and City-County Council and pay countywide taxes. Cumberland's Marion County side joins them on January 1, 2027."),
 ],
 sources=[
  ("U.S. Census Bureau, 2020 places by county (Indiana)", "https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/st18_in_place_by_county2020.txt"),
  ("U.S. Census Bureau, Vintage 2025 city and town population estimates", "https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html"),
  ("Indiana Department of Child Services, county list with county seats", "https://www.in.gov/dcs/overview/contact-us/local-dcs-offices/county-list/"),
  ("Encyclopedia of Indianapolis, structure of Unigov", "https://indyencyclopedia.org/structure-of-unigov/"),
  ("Encyclopedia of Indianapolis, excluded cities", "https://indyencyclopedia.org/excluded-cities/"),
  ("Encyclopedia of Indianapolis, included towns", "https://indyencyclopedia.org/included-towns/"),
  ("Town of Cumberland, HB 1131", "https://www.town.cumberland.in.us/government/hb1131.php"),
  ("Indianapolis Business Journal on Cumberland and Unigov", "https://www.ibj.com/articles/cumberland-seeks-through-state-legislation-to-split-from-unigov"),
  ("Encyclopedia of Indianapolis: Broad Ripple", "https://indyencyclopedia.org/broad-ripple/"),
  ("Irvington", "https://indyencyclopedia.org/irvington/"),
  ("Castleton", "https://indyencyclopedia.org/castleton/"),
  ("Southport", "https://indyencyclopedia.org/southport/"),
  ("Geist Reservoir", "https://indyencyclopedia.org/geist-reservoir/"),
  ("Wikipedia: Geist Reservoir", "https://en.wikipedia.org/wiki/Geist_Reservoir"),
  ("Washington Township", "https://en.wikipedia.org/wiki/Washington_Township,_Marion_County,_Indiana"),
  ("Warren Township", "https://en.wikipedia.org/wiki/Warren_Township,_Marion_County,_Indiana"),
  ("Lawrence Township", "https://en.wikipedia.org/wiki/Lawrence_Township,_Marion_County,_Indiana"),
  ("Pike Township", "https://en.wikipedia.org/wiki/Pike_Township,_Marion_County,_Indiana"),
  ("Center Township", "https://en.wikipedia.org/wiki/Center_Township,_Marion_County,_Indiana"),
  ("Decatur Township (Camby)", "https://en.wikipedia.org/wiki/Decatur_Township,_Marion_County,_Indiana"),
  ("Bean Blossom", "https://en.wikipedia.org/wiki/Bean_Blossom,_Indiana"),
  ("Center Grove schools", "https://en.wikipedia.org/wiki/Center_Grove_Community_School_Corporation"),
  ("Indiana DLGF, 2026 certified tax rates by district", "https://www.in.gov/dlgf/files/2026-reports/2026_Certifed_Tax_Rates_by_District.pdf"),
  ("Indiana DLGF, citizen&rsquo;s guide to property tax", "https://www.in.gov/dlgf/understanding-your-tax-bill/citizens-guide-to-property-tax/"),
  ("Indiana DLGF, property tax caps", "https://www.in.gov/dlgf/files/user-guides/251113-Fact-Sheet-Circuit-Breaker-Caps.pdf"),
  ("Indiana DLGF, deductions and credits", "https://www.in.gov/dlgf/deductions-and-credits/"),
  ("Indiana Department of Revenue, 2026 county tax rates", "https://www.in.gov/dor/files/dn01.pdf"),
  ("Indiana BMV, county excise and wheel taxes", "https://www.in.gov/bmv/fees-taxes/vehicle-registration-fees-and-taxes/county-vehicle-excise-tax-and-wheel-tax/"),
  ("State of Indiana county map", "https://www.in.gov/counties/"),
 ],
 related=[("/blog/moving-to-indianapolis-relocation-guide/", "Moving to Indianapolis: Relocation Guide"),
          ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
          (HOMESTEAD, "Indiana Homestead Deduction Guide")],
 cta=("Not Sure Which County a Home Is In?",
      "Send us the address. Our team will help you confirm the county, taxing district and school district, and what they mean for your taxes, before you make an offer.",
      [("/schedule/", "Book a Free Call →", "btn-white"), ("/search/", "Search Homes for Sale", "btn-outline")]),
 resources=[("/areas/", "Cities and Areas We Serve"),
            ("/schools/", "Central Indiana School Districts"),
            ("/blog/indiana-property-tax-caps-explained/", "Indiana Property Tax Caps Explained"),
            ("/blog/moving-to-indiana-checklist/", "Moving to Indiana Checklist")],
 link_from=[
  ("counties/hamilton-county-indiana-real-estate/index.html",
   '<strong>Which county is it in?</strong> Fishers, Carmel, Westfield and Noblesville, the county seat, are all in Hamilton County. Our <a href="/blog/what-county-is-it-in-indianapolis-area-towns-by-county/">guide to Indianapolis-area towns by county</a> lists every town around Indianapolis, including the ones that cross county lines.'),
  ("counties/boone-county-indiana-real-estate/index.html",
   '<strong>Which county is it in?</strong> Zionsville, Whitestown, Thorntown and Lebanon, the county seat, are all in Boone County. See every town around Indianapolis in our <a href="/blog/what-county-is-it-in-indianapolis-area-towns-by-county/">guide to Indianapolis-area towns by county</a>.'),
 ],
 about={"@type": "AdministrativeArea", "name": "Central Indiana",
        "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
