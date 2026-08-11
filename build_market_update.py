#!/usr/bin/env python3
"""Generate + publish a fresh MONTHLY 'Indianapolis Real Estate Market Update'.

Self-contained and CI-safe (no headless Chrome): it writes the post HTML, reuses
one shared branded card image, inserts the blog-index card, and adds the sitemap
entry — so it can run unattended from a GitHub Action each month. Each month gets
a distinct seasonal angle + a rotating focus topic, plus an optional --notes slot
for that month's real MIBOR figures. Prices are RANGES only (never fabricated
exacts), per the site rule.

Usage:
    python3 build_market_update.py --auto                 # current month
    python3 build_market_update.py 2026-08                 # a specific month
    python3 build_market_update.py 2026-08 --notes "MIBOR: median ~$XXX, +N% YoY"
"""
import sys, os, json, re, shutil, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SHARED_IMG = os.path.join(ROOT, "assets/img/blog/market-update.png")

# The metro-wide update breaks prices down by county, so it surfaces (via the
# local-posts system) on every county hub it references. Only the CURRENT month's
# report is tagged — publishing next month's swaps it automatically.
COUNTY_HUBS = [f"/counties/{c}-county-indiana-real-estate/" for c in (
    "hamilton", "boone", "hendricks", "johnson", "hancock", "marion", "madison",
    "shelby", "morgan", "brown", "decatur", "bartholomew", "jackson", "jennings",
    "montgomery", "putnam", "parke")]

TIERS = [
    ("Hamilton County (Carmel, Fishers, Westfield, Noblesville)", "the $300s to well over $1M"),
    ("Boone County (Zionsville, Whitestown, Lebanon)", "the $250s to $1M+"),
    ("Hendricks County (Avon, Brownsburg, Plainfield, Danville)", "the $250s to the $450s"),
    ("Johnson County (Greenwood, Franklin, Bargersville)", "the $250s to the $450s"),
    ("Hancock County (McCordsville, Greenfield, Fortville)", "the $250s to the $500s"),
    ("Marion County / Indianapolis", "the $150s to the $500s and up"),
    ("Outlying &amp; rural communities", "the $150s to the $300s"),
]

MONTHS = {
 1:("January","the quiet winter window before the spring rush",
    "Inventory is at its lowest in January, but so is competition — the buyers out now are serious, and early-listing sellers meet them with far less to compete against.",
    "New year, new-home planning: winter is an underrated, lower-competition time to buy in Central Indiana. Get fully pre-approved so you're ready the moment the right home appears.",
    "Listing before the spring flood is a real edge — a well-priced home in the quiet season stands out. If a spring sale is the goal, start prep and pricing now."),
 2:("February","late winter, with the spring market starting to stir",
    "Inventory remains tight but buyer interest is building as spring approaches. Motivated sellers who list now often beat the March–May crowd.",
    "If you're buying, February still offers negotiating room before spring demand spikes. Lock financing and be ready to move.",
    "This is prime prep month. Handle repairs, staging, and photography now so you can list ahead of the spring surge and capture early, motivated buyers."),
 3:("March","the opening of the spring market",
    "Spring inventory begins to build and buyer activity accelerates. The market shifts from winter-quiet toward its busiest stretch.",
    "More homes are hitting the market — a great time to start touring seriously. Come pre-approved so you can compete as the pace picks up.",
    "Spring buyers are arriving. A move-in-ready, well-priced home listed in March can capture demand before inventory peaks."),
 4:("April","the heart of the spring selling season",
    "Peak season is here: the most listings and the most buyers of the year. Well-priced, move-in-ready homes in strong school districts can draw multiple offers.",
    "The most choices — and the most competition. Be pre-approved, decisive, and lean on your agent for a clean, competitive offer.",
    "Peak buyer demand makes this ideal to sell, but competition is high too — price right from day one and present the home at its best."),
 5:("May","peak spring, the busiest month of the market",
    "May typically sees the highest activity of the year, with families timing moves around the school calendar. Momentum favors well-prepared sellers and decisive buyers.",
    "Expect competition on the best homes. A strong pre-approval, a clean offer, and fast, informed decisions win in a busy May market.",
    "Maximum buyer traffic — but buyers still reward correct pricing and great presentation. Overpricing into a hot market still leads to a stale listing."),
 6:("June","early summer, with peak season carrying strong",
    "Demand stays high through June as families push to settle before the next school year. Inventory is healthy, and quality homes still move quickly.",
    "Still a competitive market with good selection. Stay ready and move quickly on the right home before the summer slowdown begins.",
    "June remains an excellent time to sell. Keep the home show-ready — motivated summer buyers are trying to close before fall."),
 7:("July","mid-summer, active but beginning its seasonal cool-down",
    "The market is still busy in July, though it gradually eases as summer winds on. Buyers still out are often serious and less distracted.",
    "Slightly less competition than the spring peak, with good selection remaining — a solid window to buy with a bit more breathing room.",
    "Homes that lingered through spring may need a price check. Realistic pricing and strong presentation keep a July listing moving."),
 8:("August","late summer, the back-to-school transition",
    "Activity starts strong and cools as the school year begins. Buyers still searching after August tend to be motivated, and some spring listings see price adjustments.",
    "A sweet spot: healthy inventory but fewer competing buyers than spring. If you were outbid earlier, look again now with less pressure.",
    "Price to today's market, not spring's momentum. Serious late-summer buyers reward homes that are priced right and show well."),
 9:("September","early fall, the calmer post-summer market",
    "The market settles into a steadier fall rhythm. Competition eases, and serious buyers aim to be settled before the holidays.",
    "Fewer competing buyers and motivated sellers make early fall a genuinely good time to buy — often with more negotiating room.",
    "Fall buyers are focused. A move-in-ready, well-priced home still sells well; highlight comfort and a smooth path to a pre-holiday close."),
 10:("October","the heart of the fall market",
    "Inventory begins to thin and activity slows from its summer highs, but committed buyers remain active ahead of winter.",
    "Less competition and motivated sellers can mean real opportunity and negotiating room this month.",
    "Don't wait for spring if your timing calls for fall — serious buyers are out, and a warm, well-presented home gets attention with less competition."),
 11:("November","late fall heading into the year-end slowdown",
    "Activity quiets as the holidays approach and inventory thins, but November buyers are among the most motivated of the year.",
    "Year-end can be one of the best times to buy — motivated sellers, little competition, and more room to negotiate.",
    "The few homes listed now get outsized attention from serious buyers. A realistic price and inviting presentation can absolutely sell before year-end."),
 12:("December","the year-end market, quiet but opportunity-rich",
    "December is the calmest month, with the fewest listings — but relocations, life changes, and tax timing drive genuine urgency among the buyers who are out.",
    "If you can move during the holidays, you can often buy on better terms with far less competition.",
    "Motivated year-end buyers are looking. With so little on the market, a well-presented home can shine — don't assume you must wait for spring."),
}

# Rotating focus topic so consecutive/annual updates stay differentiated
FOCUS = [
 ("Mortgage rates &amp; affordability","Where financing stands and how to shop lenders — see our <a href='/blog/pre-approval-vs-pre-qualification-indianapolis/'>pre-approval guide</a>."),
 ("New construction vs. resale","Central Indiana's builders stay active — weigh the tradeoffs in <a href='/blog/buying-new-construction-in-central-indiana-pros-and-cons/'>new construction pros &amp; cons</a>."),
 ("Which suburbs are moving fastest","School districts and commute drive demand — start with the <a href='/blog/best-neighborhoods-to-buy-a-home-in-indianapolis/'>best neighborhoods guide</a>."),
 ("Pricing &amp; the appraisal gap","Correct pricing protects your deal — see <a href='/blog/what-is-my-home-worth-in-indianapolis/'>what your home is worth</a>."),
 ("First-time &amp; move-up buyers","Programs and strategy for every stage — the <a href='/blog/first-time-home-buyer-guide-indianapolis-2026/'>first-time buyer guide</a> is a great start."),
 ("Selling smart this season","What actually moves the needle on offers — <a href='/blog/home-staging-tips-for-indianapolis-sellers/'>staging tips</a> and pricing."),
]

def esc(s): return s

def build_post(year, month, notes):
    y=int(year); m=int(month)
    name, angle, driving, buyer, seller = MONTHS[m]
    label=f"{name} {y}"
    slug=f"indianapolis-market-update-{name.lower()}-{y}"
    focus_t, focus_b = FOCUS[((y*12+m)) % len(FOCUS)]
    tiers="".join(f"<li><strong>{t}</strong> — homes generally range from {r}.</li>" for t,r in TIERS)
    notes_html=(f"<div class='callout'><strong>This month's numbers:</strong> {notes}</div>" if notes else "")
    intro=(f"<p>Here's the <strong>Indianapolis real estate market update for {label}</strong> — our read on where "
           f"Central Indiana stands as we move through {angle}. Instead of chasing one headline number, this focuses on "
           f"what matters for your decision: whether it favors buyers or sellers right now, what's driving it, and what "
           f"to do about it this month. For the latest official MIBOR figures on your specific area, our team is a call away.</p>")
    sections=[
     ["big-picture", f"The {label} Big Picture", [
        f"<p>Central Indiana remains one of the more balanced, affordable major metros in the Midwest, and {name} brings "
        f"its own rhythm. {driving}</p>",
        "<p>Conditions vary a lot by price point and location — entry-level and strong-school-district homes behave very "
        "differently from the luxury tier — so a metro-wide average rarely tells your street's story. That's where a local "
        "<a href='/services/free-home-valuation/'>home valuation</a> beats a headline.</p>",
        notes_html]],
     ["focus", f"This Month's Focus: {focus_t}", [
        f"<p>{focus_b} It's the theme we're watching most closely across Central Indiana this month, and it shapes the "
        f"advice below for both buyers and sellers.</p>"]],
     ["price-tiers", "Where Prices Stand Across the Metro", [
        "<p>Typical price ranges by county (ranges, not exact averages — your home's number depends on condition, updates, "
        "and exact location):</p>", f"<ul class='areas'>{tiers}</ul>",
        "<p>Want the precise, current picture for your address? That's a quick, no-obligation "
        "<a href='/services/free-home-valuation/'>comparative market analysis</a> away.</p>"]],
     ["buyers", "What It Means for Buyers", [ f"<p>{buyer}</p>",
        "<p>The fundamentals hold all year: get properly pre-approved, know your must-haves, and work with an agent who "
        "moves fast and negotiates hard. See <a href='/services/buyer-representation/'>buyer representation</a>.</p>"]],
     ["sellers", "What It Means for Sellers", [ f"<p>{seller}</p>",
        "<p>Two decisions drive your result: pricing right from day one and presenting the home well. See "
        "<a href='/services/pricing-your-home/'>pricing your home</a> and <a href='/services/home-staging/'>home staging</a>.</p>"]],
     ["bottom-line", "The Bottom Line", [
        f"<p>Through {name} {y}, Central Indiana keeps offering real value and steady demand relative to the coasts — a "
        f"market where prepared buyers and realistically-priced sellers both have room to win. Act on your own timeline "
        f"and your own numbers, not a national headline.</p>",
        "<p>Curious what your home is worth, or what your budget buys today? We'll give you an honest, data-backed answer "
        "built on real, recent Central Indiana sales.</p>"]],
    ]
    return {
     "slug":slug, "focus_kw":f"indianapolis real estate market update {name.lower()} {y}",
     "seo_title":f"Indianapolis Market Update — {label} | Your Realty Link",
     "meta_desc":f"Indianapolis real estate market update for {label}: buyer vs seller conditions, price ranges by county, and what to do this month across Central Indiana.",
     "category":"Market Updates", "read_min":6,
     "date_label":label, "date_pub":f"{y}-{m:02d}-01", "date_mod":f"{y}-{m:02d}-01",
     "crumb":f"Market Update — {label}",
     "h1":f"Indianapolis Real Estate Market Update <em>— {label}</em>",
     "hero_sub":"Where Central Indiana stands this month — buyer vs. seller conditions, price ranges by county, and what it means for your next move.",
     "hero_badges":["Market Updates", label, "By Daniel Cope"],
     "schema_headline":f"Indianapolis Real Estate Market Update — {label}",
     "schema_desc":f"A {label} update on the Central Indiana real estate market: buyer and seller conditions, price ranges by county, and seasonal guidance.",
     "intro":intro, "sections":sections,
     "highlight":["A market update is only useful if it helps you decide. Forget the national headlines — the number that matters is what your home is worth, and what your budget buys on your street, right now.","Daniel Cope, Real Estate Broker, Your Realty Link"],
     "faqs":[
       [f"Is it a buyer's or seller's market in Indianapolis in {label}?","It depends on price point and location. Central Indiana stays relatively balanced and affordable, but entry-level and strong-school-district homes move faster than the luxury tier. A local comparative market analysis gives you the real answer."],
       ["Are home prices going up or down in Central Indiana?","The metro has seen steady, sustained demand thanks to affordability and job growth, varying by area and price tier. Look at recent comparable sales in your specific neighborhood — that's what determines value."],
       ["When is the best time to buy or sell in Indianapolis?","Spring brings the most listings and buyers; fall and winter bring less competition and more negotiating room. The best time is the one that fits your life — each season has real advantages."],
       ["How do I get current numbers for my neighborhood?","Contact Your Realty Link for a free comparative market analysis. We'll pull real, recent MIBOR sales for your exact area so you're working from today's numbers."]],
     "cta_h3":f"Get Your {label} Home Value",
     "cta_p":"Skip the national headlines. Get a free, no-obligation home valuation built on real, recent Central Indiana sales — and know exactly where you stand.",
     "cta_btn1":["Get My Free Valuation →","/services/free-home-valuation/"],
     "cta_btn2":["Talk to Our Team","/contact/"],
     "related_res":[["Free Home Valuation","/services/free-home-valuation/"],["Pricing Your Home","/services/pricing-your-home/"],["Buyer Representation","/services/buyer-representation/"],["What Is My Home Worth in Indianapolis?","/blog/what-is-my-home-worth-in-indianapolis/"]],
     "toc":[["big-picture","The Big Picture"],["focus","This Month's Focus"],["price-tiers","Prices Across the Metro"],["buyers","For Buyers"],["sellers","For Sellers"],["bottom-line","The Bottom Line"],["faq","FAQ"]],
     "related_posts":[["What Is My Home Worth in Indianapolis?","/blog/what-is-my-home-worth-in-indianapolis/"],["Best Neighborhoods to Buy a Home in Indianapolis","/blog/best-neighborhoods-to-buy-a-home-in-indianapolis/"],["Indianapolis Housing Market Forecast","/blog/indianapolis-housing-market-forecast-what-to-expect/"]],
    }

def retag(slug):
    """Point the county-hub local-posts sections at THIS month's report. Removes any
    prior market-update tag so exactly the current month shows. Run build_local_posts.py
    afterward to inject it into the pages."""
    tp = os.path.join(ROOT, "data", "local-post-tags.json")
    data = json.load(open(tp, encoding="utf-8"))
    for k in [k for k in data if k.startswith("indianapolis-market-update-")]:
        del data[k]
    data[slug] = list(COUNTY_HUBS)
    with open(tp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"tagged {slug} -> {len(COUNTY_HUBS)} county hubs")

def _load_builder():
    src=open(os.path.join(ROOT,"blog-posts-glossary.py"),encoding="utf-8").read()
    cut=src.index('new_path = os.path.join(ROOT, "blog-posts-new.json")')  # stop before the file-writing loop
    ns={"__file__":os.path.join(ROOT,"blog-posts-glossary.py")}
    exec(compile(src[:cut],"bcg","exec"),ns)
    return ns["build"], ns["normalize"]

def publish(post):
    build, normalize = _load_builder()
    # HTML
    d=os.path.join(ROOT,"blog",post["slug"]); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"index.html"),"w",encoding="utf-8").write(normalize(build(post)))
    # shared card image copied to this slug (no Chrome needed)
    shutil.copyfile(SHARED_IMG, os.path.join(ROOT,"assets/img/blog",post["slug"]+".png"))
    # blog index card (idempotent)
    bi=os.path.join(ROOT,"blog/index.html"); t=open(bi,encoding="utf-8").read()
    if f'/blog/{post["slug"]}/' not in t:
        card=(f'\n <div class="blog-card">\n <div class="blog-card-img"><img src="/assets/img/blog/{post["slug"]}.png" '
              f'alt="{post["seo_title"].split("|")[0].strip().lower()}" loading="lazy"></div>\n <div class="blog-card-body">\n'
              f' <div class="blog-card-cat">{post["category"]}</div>\n <h3>{post["seo_title"].split("|")[0].strip()}</h3>\n'
              f' <p>{post["meta_desc"]}</p>\n <a href="/blog/{post["slug"]}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
        t=t.replace('<div class="blog-grid">\n','<div class="blog-grid">\n'+card,1)
        open(bi,"w",encoding="utf-8").write(t)
    # sitemap (idempotent)
    sm=open(os.path.join(ROOT,"sitemap.xml"),encoding="utf-8").read()
    loc=f'https://janetgiles.com/blog/{post["slug"]}/'
    if loc not in sm:
        blk=f"<url>\n  <loc>{loc}</loc>\n  <lastmod>{post['date_pub']}</lastmod>\n  <changefreq>monthly</changefreq>\n  <priority>0.7</priority>\n</url>\n"
        open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8").write(sm.replace("</urlset>",blk+"</urlset>"))
    # surface this month's report on the county hubs it references
    retag(post["slug"])
    print("published /blog/%s/" % post["slug"])

if __name__=="__main__":
    args=sys.argv[1:]
    notes=""
    if "--notes" in args: notes=args[args.index("--notes")+1]
    if "--auto" in args:
        now=datetime.date(2000,1,1)  # placeholder; real date injected by CI env below
        import time; lt=time.localtime(); y,m=lt.tm_year,lt.tm_mon
    else:
        period=next((a for a in args if re.match(r"\d{4}-\d{2}$",a)),None)
        if not period: sys.exit("Usage: build_market_update.py --auto | YYYY-MM [--notes \"...\"]")
        y,m=map(int,period.split("-"))
    publish(build_post(y,m,notes))
