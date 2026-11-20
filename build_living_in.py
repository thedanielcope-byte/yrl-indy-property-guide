#!/usr/bin/env python3
"""Build "Living in <Town>, Indiana: Pros and Cons" blog pages for the 8 big suburbs.

Nov 2026 SEO audit: people search "living in <town>", "is <town> a good place to live",
"moving to <town>", and only aggregators answer well. Each page is assembled from data that
is already sourced in the repo, so nothing new is asserted here:
  - pros, cons, who-it-suits, "good place to live" answer, sources  <- inject_pros_cons.py TOWNS
  - price range, county, schools line, areas, commute, character   <- city_guides_data.py CITIES
  - county tax rate / local income tax / median tax bill            <- inject_tax_2027.py COUNTIES
  - county MIBOR figures (latest month)                             <- build_market_social.py DATA
  - school districts + private schools                              <- schools.json
  - community pages                                                 <- communities.json
  - events + official calendars                                     <- community-events.json
  - hand-written intro + slug + date + link_from                    <- living_in_data.py
Pages are rendered with build_fresh_posts.py's blog shell (Quick Answer, FAQ schema, card).
Carmel and Franklin reuse their existing "living in" post URLs; the other six are new.

Re-run after the monthly market routine to refresh the MIBOR line, or after editing any of
the data above:

    python3 build_living_in.py            build all 8
    python3 build_living_in.py --check    validate + render to /tmp only
Then run the usual injectors (inject_gtag, inject_favicon, inject_seo_overrides,
gloss_autolink, inject_hero_preload, refresh_sitemap_lastmod) and inject_pros_cons.py
(its city-page sections link here).
"""
import ast, html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import build_fresh_posts as bfp
from city_guides_data import CITIES
from living_in_data import TOWNS as LIVING

MODIFIED = "2026-11-19"
MONTH_LABEL = "November 2026"
MARION_LIT = 2.02


def _exec_head(path, stop):
    src = open(path, encoding="utf-8").read()
    ns = {}
    exec(src[:src.index(stop)], ns)
    return ns


PROS = _exec_head("inject_pros_cons.py", "def block")["TOWNS"]
TAX = {c: (r, l, m) for c, r, l, m in _exec_head("inject_tax_2027.py", "rows =")["COUNTIES"]}


def load_market():
    tree = ast.parse(open("build_market_social.py", encoding="utf-8").read())
    vals = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("DATA", "MONTH"):
            vals[node.targets[0].id] = ast.literal_eval(node.value)
    return vals["DATA"], vals["MONTH"]


MARKET, MKT_MONTH = load_market()
SCHOOLS = json.load(open("schools.json", encoding="utf-8"))
DISTRICTS = {d["slug"]: d for d in SCHOOLS["districts"]}
PRIVATE = {d["slug"]: d for d in SCHOOLS.get("private", [])} if isinstance(SCHOOLS.get("private"), list) else {}
COMMUNITIES = json.load(open("communities.json", encoding="utf-8"))["communities"]
EVENTS = {e["city"]: e for e in json.load(open("community-events.json", encoding="utf-8"))}
COMPARES = sorted(os.listdir("compare"))

STATS = ("STATS Indiana, 2026 certified tax rates (Indiana DLGF)", "https://www.stats.indiana.edu/web/profiles/tax_rates_2026/{county}.html")
DOR = ("Indiana DOR, county local income tax rates (2026)", "https://www.in.gov/dor/files/dn01.pdf")


def text(h):
    """HTML fragment -> plain text for FAQ answers."""
    return html.unescape(re.sub(r"<[^>]+>", "", h)).strip()


def page_exists(href):
    f = href.strip("/")
    return os.path.exists(os.path.join(f, "index.html"))


def school_name(slug):
    d = DISTRICTS.get(slug) or PRIVATE.get(slug)
    if d:
        return d["name"]
    # private schools may live only as pages; fall back to the page's H1
    p = f"schools/{slug}/index.html"
    if os.path.exists(p):
        m = re.search(r"<h1[^>]*>(.*?)</h1>", open(p, encoding="utf-8").read(), re.S)
        if m:
            return text(m.group(1))
    return slug.replace("-", " ").title()


def andjoin(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def pct(v):
    if abs(v) < 0.05:
        return "flat from a year earlier"
    return f"{'up' if v > 0 else 'down'} {abs(v):.1f}% from a year earlier"


def compare_label(slug):
    parts = slug.split("-vs-")
    return " vs ".join(p.replace("-", " ").title() for p in parts)


def build(key):
    L = LIVING[key]
    T = PROS[key]
    C = CITIES[L["city_key"]]
    name = T["name"]
    county = C["county"].replace(" County", "")
    county_slug = county.lower() + "-county"
    city_url = C["url"]
    county_url = f"/counties/{county_slug}-indiana-real-estate/"
    slug = L["slug"]
    price = C["price"]
    price_cap = price[4:] if price.startswith("the ") else price
    price_cap = price_cap[0].upper() + price_cap[1:]
    commute = C["commute"]
    commute_short = commute.replace(" to downtown Indianapolis", "")
    commute_short = commute_short[0].upper() + commute_short[1:]

    # ---- market + taxes ----
    _, med, med_yoy, sales, sales_yoy, dom, dom_prior, supply = MARKET[county_slug]
    rate, lit_s, bill = TAX[county]
    lit = float(lit_s.rstrip("%*"))
    diff = round((MARION_LIT - lit) * 1000 / 10) * 10
    lit_note = (f"{county} County&rsquo;s {lit:.2f}% local income tax (2026) is below Marion County&rsquo;s {MARION_LIT:.2f}%, "
                f"about ${diff:,.0f} a year less per $100,000 of income")
    if county == "Boone":
        lit_note += "; Boone County&rsquo;s rate rose from 1.70% to 1.71% on October 1, 2026"
    if county != "Hamilton":
        lit_note += f", though Hamilton County&rsquo;s 1.10% is lower still"
    lit_note += "."

    # ---- schools ----
    cs = SCHOOLS["city_schools"].get(name, {})
    def school_li(s):
        n = html.escape(school_name(s), quote=False)
        return f'<a href="/schools/{s}/">{n}</a>' if page_exists(f"/schools/{s}/") else n
    public = [school_li(s) for s in cs.get("public", [])]
    private = [school_li(s) for s in cs.get("private", [])]
    public_names = [school_name(s) for s in cs.get("public", [])]

    # ---- communities ----
    comms = [c for c in COMMUNITIES if c.get("city") == name and page_exists(f"/communities/{c['slug']}/")]
    comm_links = andjoin(f'<a href="/communities/{c["slug"]}/">{html.escape(c["name"], quote=False)}</a>' for c in comms[:8])

    # ---- events ----
    ev = EVENTS.get(name, {})
    ev_lis = "\n".join(f'  <li><strong>{html.escape(e["name"], quote=False)}</strong> ({html.escape(e["when"], quote=False)}): {html.escape(e["desc"], quote=False)}</li>'
                       for e in ev.get("events", []))
    cal = " &middot; ".join(f'<a href="{c["url"]}" target="_blank" rel="noopener">{html.escape(c["label"], quote=False)}</a>' for c in ev.get("calendar_links", []))
    official = ev.get("official_site")

    # ---- compares ----
    tslug = L["city_key"]
    comps = [c for c in COMPARES if re.search(rf"(^|-){tslug}(-|$)", c) and page_exists(f"/compare/{c}/")]
    comp_links = ", ".join(f'<a href="/compare/{c}/">{compare_label(c)}</a>' for c in comps)

    li = lambda xs: "\n".join(f"  <li>{x}</li>" for x in xs)
    areas = C["areas"]
    areas_txt = ", ".join(areas[:-1]) + " and " + areas[-1]

    body = f"""
 <p>{L['intro']}</p>

 <h2 id="pros">Pros of Living in {name}</h2>
 <ul>
{li(T['pros'])}
 </ul>

 <h2 id="cons">Cons of Living in {name}</h2>
 <ul>
{li(T['cons'])}
 </ul>

 <h2 id="cost">Cost of Living in {name}</h2>
 <p><strong>Home prices.</strong> Homes in {name} typically range from {price}. MIBOR reports the market by county: in {MKT_MONTH}, {county} County&rsquo;s median sale price was ${med:,.0f}, {pct(med_yoy)}, homes took a median {dom} days to sell (versus {dom_prior} a year earlier) and there were {supply:.1f} months of supply. Prices in {name} itself can run higher or lower than the county figure. See our <a href="/market-updates/">monthly market updates</a> for the latest numbers.</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>{county} County</th><th>Figure</th></tr></thead>
 <tbody>
 <tr><td>Local income tax (2026)</td><td>{lit:.2f}% (Marion County: {MARION_LIT:.2f}%)</td></tr>
 <tr><td>Property tax rate, middle district (2026)</td><td>{rate} per $100 of assessed value</td></tr>
 <tr><td>Median homeowner tax bill</td><td>{bill} a year (ACS 2020&ndash;2024)</td></tr>
 </tbody>
 </table>
 </div>
 <p><strong>Taxes.</strong> {lit_note} On property taxes, Indiana caps the bill on your primary home at 1% of its gross assessed value (not counting voter-approved referendums), and the homestead deduction lowers the taxable value, but only if it&rsquo;s filed. Our <a href="/blog/indiana-homestead-exemption-lower-property-taxes/">homestead exemption guide</a> explains how it works, and <a href="/blog/indiana-property-tax-caps-explained/#by-county">property taxes by county</a> compares the metro.</p>

 <h2 id="neighborhoods">Neighborhoods and Communities in {name}</h2>
 <p>Popular areas include {areas_txt}.</p>
 {f'<p>We profile {len(comms)} {name} communities, including {comm_links}. Browse them all in our <a href="/communities/">communities directory</a>.</p>' if comms else ''}

 <h2 id="schools">Schools in {name}</h2>
 <p>{html.escape(cs.get('note', ''), quote=False)}</p>
 {f'<p><strong>Public school districts:</strong> {", ".join(public)}.</p>' if public else ''}
 {f'<p><strong>Private schools in {name}:</strong> {", ".join(private)}.</p>' if private else ''}
 <p>School assignment follows the address, so confirm boundaries with the district before you write an offer. Our <a href="/schools/">Central Indiana schools guide</a> covers every district.</p>

 <h2 id="commute">Commute and Getting Around</h2>
 <p>{name} is {commute}. Rush-hour times run longer, so test-drive the commute at the hours you&rsquo;d actually drive it. Comparing drives? See the <a href="/best/indianapolis-suburbs-for-commuters/">best Indianapolis suburbs for commuters</a>.</p>

 <h2 id="things">Things to Do in {name}</h2>
 <p>Here&rsquo;s a sample of what fills the {name} calendar through the year:</p>
 {f'<ul>{chr(10)}{ev_lis}{chr(10)} </ul>' if ev_lis else ''}
 {f'<p>Event calendars: {cal}{" &middot; " if cal and official else ""}{f"<a href={chr(34)}{official}{chr(34)} target={chr(34)}_blank{chr(34)} rel={chr(34)}noopener{chr(34)}>official {name} website</a>" if official else ""}.</p>' if (cal or official) else ''}

 <h2 id="who">Who {name} Suits</h2>
 <p>{T['who']}</p>

 <h2 id="compare">How {name} Compares</h2>
 <p>{f'Side-by-side comparisons: {comp_links}.' if comp_links else ''} For the bigger picture, see <a href="/blog/living-in-indianapolis-pros-and-cons/">living in Indianapolis: pros and cons</a> and the <a href="/best/indianapolis-suburbs-for-families/">best Indianapolis suburbs for families</a>.</p>
 <p>Ready to look? Start with <a href="{city_url}">{name} real estate and homes for sale</a>, or <a href="/search/">search every active MIBOR listing</a>.</p>
"""
    body = re.sub(r"\n \n", "\n", body)

    cons_txt = " ".join(text(c) for c in T["cons"])
    faqs = [
        (f"Is {name}, Indiana a good place to live?", text(T["faq"])),
        (f"How much do homes cost in {name}?",
         f"Homes in {name} typically range from {price}. In {MKT_MONTH}, the median sale price across {county} County was ${med:,.0f} (MIBOR), "
         f"and prices in {name} itself can run higher or lower than the county figure."),
        (f"How far is {name} from downtown Indianapolis?", f"{name} is {commute}. Expect longer drives at rush hour."),
        (f"What school district is {name} in?",
         (cs.get("note") or f"{name} is served by {text(C['schools'])}.") + " Always confirm the district for a specific address."),
        (f"What are the downsides of living in {name}?", cons_txt),
        (f"Are taxes high in {name}?",
         text(lit_note) + " Property taxes on a primary home are capped at 1% of gross assessed value, not counting voter-approved referendums, "
         "and the homestead deduction lowers the taxable value once it's filed."),
    ]
    sources = [(l, u) for u, l in T["sources"]]
    if not any("dor" in u for _, u in sources):
        sources.append(DOR)
    sources += [(STATS[0], STATS[1].format(county=county)),
                (f"MIBOR REALTOR Association, {county} County ({MKT_MONTH})", "/market-updates/")]

    existing = os.path.exists(f"blog/{slug}/index.html") and L["date"] != MODIFIED
    P = dict(
        slug=slug,
        title=f"Living in {name}, Indiana: Pros and Cons (2026)",
        headline=f"Living in {name}, Indiana: Pros and Cons for 2026",
        crumb=f"Living in {name}, Indiana",
        h1_html=f"Living in {name}, Indiana: <em>Pros and Cons</em>",
        desc=f"Thinking about moving to {name}, Indiana? Honest 2026 pros and cons: home prices, taxes, schools, commute, neighborhoods and who it suits.",
        date=L["date"], month=MONTH_LABEL, category="City Guides", eyebrow="CITY GUIDES",
        focus=f"living in {name.lower()} indiana",
        hero_sub=f"An honest look at {name}: home prices, taxes, schools, the commute, neighborhoods and who it suits best, from a local {county} County team.",
        badges=["City Guides", "Updated for 2026", f"{county} County"],
        read_min=8,
        card_title=f"Living in {name}: Pros and Cons",
        card_sub=f"Prices, taxes, schools and commute in {name}, Indiana.",
        qa_heading=f"Living in {name} at a Glance",
        qa_lead=f"<strong>Is {name}, Indiana a good place to live?</strong> {T['faq']}",
        qa_facts=[
            ("Home prices", price_cap),
            (f"{county} County median sale price", f"${med:,.0f}, {pct(med_yoy)} (MIBOR, {MKT_MONTH})"),
            ("Commute downtown", commute_short),
            ("Public schools", " &middot; ".join(html.escape(n, quote=False) for n in public_names) or C["schools"]),
            ("Local income tax", f"{lit:.2f}% ({county} County, 2026) vs. {MARION_LIT:.2f}% in Marion County"),
        ],
        toc=[("pros", "Pros"), ("cons", "Cons"), ("cost", "Cost of Living"), ("neighborhoods", "Neighborhoods"),
             ("schools", "Schools"), ("commute", "Commute"), ("things", "Things to Do"), ("who", f"Who {name} Suits"),
             ("compare", "How It Compares")],
        body=body,
        faqs=faqs,
        sources=sources,
        related=[("/blog/living-in-indianapolis-pros-and-cons/", "Living in Indianapolis: Pros and Cons"),
                 ("/blog/cost-of-living-in-indianapolis/", "Cost of Living in Indianapolis"),
                 ("/best/indianapolis-suburbs-for-families/", "Best Indianapolis Suburbs for Families")],
        cta=(f"Thinking About Moving to {name}?",
             f"We&rsquo;ll walk you through {name} neighborhoods, school boundaries and what homes are really selling for, then set up a search that fits.",
             [("/schedule/", "Book a Free Call &rarr;", "btn-white"), (city_url, f"{name} Real Estate", "btn-outline")]),
        resources=[(city_url, f"{name} Real Estate"), (county_url, f"{county} County Real Estate"),
                   ("/schools/", "Central Indiana Schools"), ("/search/", "Search Homes for Sale")],
        about={"@type": "City", "name": name, "containedInPlace": {"@type": "State", "name": "Indiana"}},
        link_from=[(p, f'Weighing a move? Read our honest guide to <a href="/blog/{slug}/">living in {name}, Indiana: pros and cons</a>, with home prices, taxes, schools and the commute.')
                   for p in L["link_from"]],
    )
    if existing:
        P["modified"] = MODIFIED
    return P


def refresh_blog_card(P):
    """publish() only adds cards for new URLs; keep the existing card in sync for reused URLs."""
    f = "blog/index.html"
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<div class="blog-card">\s*<div class="blog-card-img"><img src="/assets/img/blog/' + re.escape(P["slug"]) + r'\.png"[^>]*></div>.*?class="read-more"',
                  s, re.S)
    if not m:
        return
    card = m.group(0)
    new = re.sub(r'(<img src="[^"]+" alt=")[^"]*', lambda x: x.group(1) + html.escape(P["focus"]), card, count=1)
    new = re.sub(r'<div class="blog-card-cat">.*?</div>', f'<div class="blog-card-cat">{P["category"]}</div>', new, count=1)
    new = re.sub(r"<h3>.*?</h3>", lambda x: f"<h3>{html.escape(P['headline'], quote=False)}</h3>", new, count=1, flags=re.S)
    new = re.sub(r"<p>.*?</p>", lambda x: f"<p>{html.escape(P['desc'], quote=False)}</p>", new, count=1, flags=re.S)
    if new != card:
        open(f, "w", encoding="utf-8").write(s.replace(card, new, 1))
        print("  refreshed blog card", P["slug"])


def main():
    check_only = "--check" in sys.argv
    bad = False
    for key in LIVING:
        P = build(key)
        errs = bfp.check(P)
        words = len(re.sub(r"<[^>]+>", " ", P["body"]).split())
        print(f"{P['slug']}: {'OK' if not errs else 'PROBLEMS'} ({words} words, title {len(P['title'])}, desc {len(P['desc'])})")
        for e in errs:
            print("  -", e)
        bad = bad or bool(errs)
        if errs:
            continue
        if check_only:
            open(f"/tmp/yrl-check-{P['slug']}.html", "w", encoding="utf-8").write(bfp.page(P))
        else:
            bfp.publish(P)
            refresh_blog_card(P)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
