#!/usr/bin/env python3
"""Generate a fresh quarterly 'Indianapolis Real Estate Market Update' blog post.

Each quarter gets genuinely different, seasonally-appropriate content (spring
prep / peak season / fall / year-end) plus a metro price-tier snapshot in RANGES
— never fabricated exact medians, rates, or counts (per the site rule). An
optional NOTES line lets the broker drop in that quarter's real MIBOR figures.

Usage:
    python3 build_market_update.py Q3-2026
    python3 build_market_update.py Q4-2026 --notes "MIBOR: median ~\$XXX, inventory up N%"
Then run:  python3 blog-posts-glossary.py && python3 finalize_new_posts.py
(writes the post into blog-posts-new.json; the prior batch is already built).
"""
import sys, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

def esc(s): return s

# ── metro price-tier snapshot (RANGES only — matches the site's price language) ──
TIERS = [
    ("Hamilton County (Carmel, Fishers, Westfield, Noblesville)", "the $300s to well over $1M"),
    ("Boone County (Zionsville, Whitestown, Lebanon)", "the $250s to $1M+"),
    ("Hendricks County (Avon, Brownsburg, Plainfield, Danville)", "the $250s to the $450s"),
    ("Johnson County (Greenwood, Franklin, Bargersville)", "the $250s to the $450s"),
    ("Hancock County (McCordsville, Greenfield, Fortville)", "the $250s to the $500s"),
    ("Marion County / Indianapolis", "the $150s to the $500s and up"),
    ("Outlying &amp; rural communities", "the $150s to the $300s"),
]

# ── per-quarter seasonal content ──
Q = {
 1: dict(season="Winter into Spring", months="January–March",
   angle="the quiet winter window before the spring rush",
   driving="Inventory is typically at its lowest in the first quarter, but so is competition. The buyers who are out in January and February tend to be serious, and motivated sellers who list early often meet them with far less competition than they'd face in May. As the quarter closes, spring inventory begins to build and the market wakes up.",
   buyer="Winter is an underrated time to buy in Central Indiana. There's less competition, sellers are often more negotiable, and you're not fighting a dozen offers. Get fully pre-approved now so you're ready to move the moment the right home appears — spring will bring more choices but also more buyers.",
   seller="Listing before the spring flood can be a real advantage. A well-prepared, well-priced home in February or March often stands out precisely because there's so little else on the market. If a spring sale is your goal, now is the time to start prep and pricing conversations."),
 2: dict(season="Peak Spring &amp; Summer", months="April–June",
   angle="the busiest stretch of the Central Indiana real estate year",
   driving="The second quarter is peak season across the metro. Inventory is at its highest, but so is buyer demand — well-priced, move-in-ready homes in sought-after school districts can still draw multiple offers and move quickly. Families time their moves around the school calendar, which concentrates activity into these months.",
   buyer="This is the season of the most choices — and the most competition. Come in fully pre-approved with a clear budget, and be ready to act decisively on the right home. Lean on your agent to write a clean, competitive offer; in the strongest neighborhoods, preparation is what wins the house.",
   seller="Spring and early summer bring the largest buyer pool of the year — ideal conditions to sell. But more listings also means more competition, so pricing right from day one and presenting the home well (staging, photography, curb appeal) matters more than ever. Overpricing into a busy market still leads to a stale listing."),
 3: dict(season="Late Summer into Fall", months="July–September",
   angle="the transition from peak season toward the calmer fall market",
   driving="The third quarter starts strong and gradually cools as the school year begins and families settle in. Buyers still in the market after August are often serious and less distracted, and homes that lingered through the spring may see price adjustments. It's a window where prepared buyers and realistic sellers can both do well.",
   buyer="Late summer and early fall can be a sweet spot: still a healthy number of listings, but fewer competing buyers than the spring peak. Homes that sat over the summer may be ripe for negotiation. If you were outbid in the spring, this is a good time to look again with less pressure.",
   seller="If you're listing in Q3, price to today's market, not to spring's momentum. Serious fall buyers reward homes that are priced right and show well. Highlight energy efficiency and a move-in-ready condition — buyers this time of year are often trying to be settled before the holidays."),
 4: dict(season="Fall &amp; Year-End", months="October–December",
   angle="the calmer, opportunity-rich close of the year",
   driving="Fourth-quarter activity slows as the holidays approach, and inventory thins out. But the buyers who are looking in November and December are among the most motivated of the year — relocations, life changes, and tax-timing all drive genuine urgency. Less competition can mean real opportunity on both sides.",
   buyer="Year-end is quietly one of the best times to buy. Competition drops, sellers who are still listed are usually motivated, and you may have far more negotiating room than you would in spring. If you can move during the holidays, you can often buy on better terms.",
   seller="Don't assume you have to wait for spring. The buyers looking in Q4 are serious, and with so few homes on the market, a well-presented listing gets outsized attention. If your timing calls for a year-end move, a realistic price and warm, inviting presentation can absolutely get it sold."),
}

def quarter_of(period):
    m = re.match(r"Q([1-4])-(\d{4})", period, re.I)
    if not m: sys.exit("Period must look like Q3-2026")
    return int(m.group(1)), m.group(2)

def build(period, notes):
    qn, year = quarter_of(period)
    q = Q[qn]
    label = f"Q{qn} {year}"
    slug = f"indianapolis-market-update-{period.lower()}"
    tiers_html = "".join(f"<li><strong>{t}</strong> — homes generally range from {r}.</li>" for t, r in TIERS)
    notes_html = (f"<div class='callout'><strong>This quarter's numbers:</strong> {notes}</div>" if notes else "")

    intro = (f"<p>Welcome to the <strong>Indianapolis real estate market update for {label}</strong> — "
             f"our read on where Central Indiana stands as we move through {q['angle']}. Rather than chase a single "
             f"headline number, this update focuses on what actually matters for your decision: whether it favors "
             f"buyers or sellers right now, what's driving it, and what to do about it in the {q['months']} stretch. "
             f"For the latest official MIBOR figures on any specific city or neighborhood, our team is a call away.</p>")

    sections = [
        ["big-picture", f"The {label} Big Picture", [
            f"<p>Central Indiana remains one of the more balanced and affordable major metros in the Midwest, and "
            f"{q['season'].replace('&amp;','and')} brings its own rhythm. {q['driving']}</p>",
            "<p>Conditions vary a lot by price point and location — the entry-level and strong-school-district segments "
            "behave very differently from the luxury tier — so a metro-wide 'average' rarely tells your street's story. "
            "That's exactly where a local <a href='/services/free-home-valuation/'>home valuation</a> beats a headline.</p>",
            notes_html,
        ]],
        ["price-tiers", "Where Prices Stand Across the Metro", [
            "<p>A snapshot of typical price ranges by county (ranges, not exact averages — the right number for your "
            "home depends on its condition, updates, and exact location):</p>",
            f"<ul class='areas'>{tiers_html}</ul>",
            "<p>Want the precise, current picture for your address or target neighborhood? That's a quick, no-obligation "
            "<a href='/services/free-home-valuation/'>comparative market analysis</a> away.</p>",
        ]],
        ["buyers", f"What It Means for Buyers This Quarter", [
            f"<p>{q['buyer']}</p>",
            "<p>Whatever the season, the fundamentals hold: get <a href='/blog/pre-approval-vs-pre-qualification-indianapolis/'>"
            "properly pre-approved</a>, know your must-haves, and work with an agent who can move fast and negotiate hard. "
            "Explore <a href='/services/buyer-representation/'>buyer representation</a> to see how our team helps.</p>",
        ]],
        ["sellers", f"What It Means for Sellers This Quarter", [
            f"<p>{q['seller']}</p>",
            "<p>The two decisions that most affect your result never change: pricing right from day one and presenting "
            "the home well. See <a href='/services/pricing-your-home/'>pricing your home</a> and "
            "<a href='/services/home-staging/'>home staging</a> for how we approach both.</p>",
        ]],
        ["outlook", "The Bottom Line", [
            f"<p>Heading through {q['months']} {year}, Central Indiana continues to offer real value and steady demand "
            f"relative to the coasts — a market where well-prepared buyers and realistically-priced sellers both have "
            f"room to win. The key is acting on your own timeline and your own numbers, not a national headline.</p>",
            "<p>Curious what your home is worth, or what your budget buys in today's market? Our team gives you an "
            "honest, data-backed answer built on real, recent Central Indiana sales.</p>",
        ]],
    ]

    return {
        "slug": slug,
        "focus_kw": f"indianapolis real estate market update {year}",
        "seo_title": f"Indianapolis Market Update — {label} | Your Realty Link",
        "meta_desc": f"Indianapolis real estate market update for {label}: buyer vs seller conditions, price ranges by county, and what to do this quarter across Central Indiana.",
        "category": "Market Updates",
        "read_min": 7,
        "date_label": f"{q['months'].split(chr(8211))[0].strip()} {year}", "date_pub": f"{year}-{ {1:'01',2:'04',3:'07',4:'10'}[qn] }-01", "date_mod": f"{year}-{ {1:'01',2:'04',3:'07',4:'10'}[qn] }-01",
        "crumb": f"Indianapolis Market Update — {label}",
        "h1": f"Indianapolis Real Estate Market Update <em>— {label}</em>",
        "hero_sub": f"Where Central Indiana stands this quarter — buyer vs. seller conditions, price ranges by county, and what it means for your next move.",
        "hero_badges": ["Market Updates", f"{label}", "By Daniel Cope"],
        "schema_headline": f"Indianapolis Real Estate Market Update — {label}",
        "schema_desc": f"A {label} update on the Central Indiana real estate market: buyer and seller conditions, price ranges by county, and seasonal guidance.",
        "intro": intro,
        "sections": sections,
        "highlight": [f"A market update is only useful if it helps you decide. Forget the national headlines — the number that matters is what your specific home is worth, and what your budget buys on your street, right now.", "Daniel Cope, Real Estate Broker, Your Realty Link"],
        "faqs": [
            [f"Is it a buyer's or seller's market in Indianapolis in {label}?", f"It depends on price point and location. Central Indiana stays relatively balanced and affordable, but the entry-level and strong-school-district segments move faster than the luxury tier. A local comparative market analysis gives you the real answer for your situation."],
            ["Are home prices going up or down in Central Indiana?", "The metro has seen steady, sustained demand thanks to affordability and job growth, with conditions varying by area and price tier. Rather than a single trend, look at recent comparable sales in your specific neighborhood — that's what actually determines value."],
            ["When is the best time to buy or sell in Indianapolis?", "Spring brings the most listings and buyers; fall and winter bring less competition and often more negotiating room. The best time is really the one that fits your life — each season has genuine advantages our team can help you use."],
            ["How do I get current numbers for my neighborhood?", "Contact Your Realty Link for a free, no-obligation comparative market analysis. We'll pull real, recent MIBOR sales for your exact area so you're working from today's numbers, not a national average."],
        ],
        "cta_h3": f"Get Your {label} Home Value",
        "cta_p": "Skip the national headlines. Get a free, no-obligation home valuation built on real, recent Central Indiana sales — and know exactly where you stand this quarter.",
        "cta_btn1": ["Get My Free Valuation →", "/services/free-home-valuation/"],
        "cta_btn2": ["Talk to Our Team", "/contact/"],
        "related_res": [
            ["Free Home Valuation", "/services/free-home-valuation/"],
            ["Pricing Your Home", "/services/pricing-your-home/"],
            ["Buyer Representation", "/services/buyer-representation/"],
            ["What Is My Home Worth in Indianapolis?", "/blog/what-is-my-home-worth-in-indianapolis/"],
        ],
        "toc": [
            ["big-picture", "The Big Picture"],
            ["price-tiers", "Prices Across the Metro"],
            ["buyers", "For Buyers"],
            ["sellers", "For Sellers"],
            ["outlook", "The Bottom Line"],
            ["faq", "FAQ"],
        ],
        "related_posts": [
            ["What Is My Home Worth in Indianapolis?", "/blog/what-is-my-home-worth-in-indianapolis/"],
            ["Best Neighborhoods to Buy a Home in Indianapolis", "/blog/best-neighborhoods-to-buy-a-home-in-indianapolis/"],
            ["First Time Home Buyer Guide — Indianapolis 2026", "/blog/first-time-home-buyer-guide-indianapolis-2026/"],
        ],
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: build_market_update.py Q3-2026 [--notes \"...\"]")
    period = sys.argv[1]
    notes = ""
    if "--notes" in sys.argv:
        notes = sys.argv[sys.argv.index("--notes") + 1]
    post = build(period, notes)
    json.dump([post], open(os.path.join(ROOT, "blog-posts-new.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote blog-posts-new.json with 1 market-update post:", post["slug"])
    print("next: python3 blog-posts-glossary.py && python3 finalize_new_posts.py")
