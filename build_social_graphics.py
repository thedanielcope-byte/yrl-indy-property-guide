#!/usr/bin/env python3
"""Generate the month's branded Facebook graphics (1080x1080) for Your Realty Link.
Clones the HTML->PNG-via-headless-Chrome engine from build_market_social.py:
base64-inlined logo, brand palette (#c03926 / #1a1a1a / #6e6e70 / warm #f7f3ef),
Playfair Display + Libre Franklin. Five card templates (spotlight / tip / compare /
explainer / cta). Post 01 reuses the real market graphic. Output ->
assets/img/social/2026-09/NN-slug.png.

    python3 build_social_graphics.py
"""
import os, base64, subprocess, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCRATCH = "/private/tmp/claude-501/-Users-danielcope-Library-Mobile-Documents-com-apple-CloudDocs-Claude-YRL/26f905d9-f2dc-48a5-9205-1e23c0b750ad/scratchpad"
OUTDIR = os.path.join(ROOT, "assets/img/social/2026-09")
LOGO = base64.b64encode(open(os.path.join(ROOT, "assets/img/yrl-logo.png"), "rb").read()).decode()
FOOT_META = "<b>Your Realty Link</b> &middot; Janet Giles, Principal Broker<br>317-997-7404 &middot; MIBOR member"

SHELL = """<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Libre+Franklin:wght@400;500;600;700;800&display=swap">
<style>
 *{margin:0;padding:0;box-sizing:border-box}
 body{width:1080px;height:1080px;overflow:hidden;font-family:"Libre Franklin",system-ui,sans-serif;background:#f7f3ef;color:#1e1a17}
 .card{width:1080px;height:1080px;padding:66px 66px 58px;display:flex;flex-direction:column;position:relative}
 .card::after{content:"";position:absolute;right:-150px;top:-150px;width:440px;height:440px;border-radius:50%;background:rgba(192,57,38,.06)}
 .top{display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:2}
 .logo{height:62px}
 .eyebrow{text-align:right;font-size:20px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#c03926;line-height:1.4;max-width:520px}
 h1{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:78px;line-height:1.02;margin:40px 0 0;color:#17130f;position:relative;z-index:2}
 h1 em{font-style:normal;color:#c03926}
 h1.sm{font-size:64px}
 .rule{width:100px;height:7px;background:#c03926;border-radius:4px;margin:26px 0 0;position:relative;z-index:2}
 .body{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2;padding:8px 0}
 .pill{display:inline-block;align-self:flex-start;background:#fff;border:2px solid #c03926;color:#c03926;font-weight:800;font-size:26px;padding:12px 26px;border-radius:999px;margin-bottom:34px}
 ul.bul{list-style:none;display:flex;flex-direction:column;gap:24px}
 ul.bul li{font-size:34px;font-weight:600;line-height:1.32;padding-left:52px;position:relative;color:#2a2420}
 ul.bul li::before{content:"";position:absolute;left:0;top:12px;width:22px;height:22px;border-radius:6px;background:#c03926}
 ol.num{list-style:none;counter-reset:n;display:flex;flex-direction:column;gap:26px}
 ol.num li{counter-increment:n;font-size:33px;font-weight:600;line-height:1.3;padding-left:74px;position:relative;color:#2a2420}
 ol.num li::before{content:counter(n);position:absolute;left:0;top:-4px;width:48px;height:48px;border-radius:14px;background:#17130f;color:#fff;font-family:"Playfair Display",serif;font-weight:800;font-size:26px;display:flex;align-items:center;justify-content:center}
 .cols{display:flex;align-items:stretch;gap:0;margin-top:8px}
 .cols .col{flex:1;background:#fff;border:1px solid #ece4dc;border-radius:20px;padding:30px 30px;box-shadow:0 6px 22px rgba(40,25,20,.05)}
 .cols .col h3{font-family:"Playfair Display",serif;font-size:40px;color:#c03926;margin-bottom:14px}
 .cols .col p{font-size:26px;font-weight:500;color:#4a423c;line-height:1.42}
 .cols .vs{display:flex;align-items:center;font-family:"Playfair Display",serif;font-weight:800;font-size:38px;color:#6e6e70;padding:0 22px}
 .take{font-size:28px;font-weight:600;color:#2a2420;line-height:1.4;margin-top:30px}
 .take b{color:#c03926}
 .def{font-size:36px;font-weight:500;color:#2a2420;line-height:1.5}
 .def b{color:#17130f;font-weight:800}
 .lead{font-size:36px;font-weight:500;color:#2a2420;line-height:1.45}
 .bigcta{margin-top:38px;background:#c03926;color:#fff;border-radius:18px;padding:26px 32px;font-size:34px;font-weight:800;align-self:flex-start}
 .foot{background:#17130f;border-radius:18px;padding:24px 32px;display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}
 .foot .cta{color:#fff;font-size:26px;font-weight:800}
 .foot .cta b{color:#e0644f}
 .foot .meta{color:#c9bfb6;font-size:18px;font-weight:600;text-align:right;line-height:1.4}
 .foot .meta b{color:#fff}
</style>
<div class="card">
 <div class="top"><img class="logo" src="data:image/png;base64,__LOGO__"><div class="eyebrow">__EYEBROW__</div></div>
 <h1 class="__H1CLASS__">__HEADLINE__</h1>
 <div class="rule"></div>
 <div class="body">__BODY__</div>
 <div class="foot"><div class="cta">__CTA__</div><div class="meta">__META__</div></div>
</div>"""

def bullets(items):
    return '<ul class="bul">' + "".join("<li>%s</li>" % i for i in items) + "</ul>"
def numbered(items):
    return '<ol class="num">' + "".join("<li>%s</li>" % i for i in items) + "</ol>"
def spotlight_body(pill, items):
    return ('<div class="pill">%s</div>' % pill) + bullets(items)
def compare_body(a, adesc, b, bdesc, take):
    return ('<div class="cols"><div class="col"><h3>%s</h3><p>%s</p></div>'
            '<div class="vs">vs</div><div class="col"><h3>%s</h3><p>%s</p></div></div>'
            '<div class="take">%s</div>') % (a, adesc, b, bdesc, take)
def explain_body(text):
    return '<p class="def">%s</p>' % text
def cta_body(lead, big):
    return ('<p class="lead">%s</p><div class="bigcta">%s</div>') % (lead, big)

# ---- the 16 posts (post 01 = real market graphic, copied) -------------------
CARDS = [
 (2,"geist-spotlight","Community Spotlight &middot; Geist","Geist <em>Reservoir</em>","",
   spotlight_body("Homes from the $350s to $900s+",
    ["Waterfront living on a 1,900-acre reservoir","Boating, private docks &amp; a resort-style lifestyle","Minutes to Fishers, Geist shopping &amp; top schools"]),
   "Explore Geist &rarr; <b>yourrealtylink.com</b>"),
 (3,"bidding-war","Buyer Tip","How to win a <em>bidding war</em>","",
   numbered(["Get fully underwritten &mdash; not just pre-qualified","Keep the offer clean: fewer contingencies win","Lean on a local agent who knows the seller&rsquo;s priorities"]),
   "More buyer tips &rarr; <b>yourrealtylink.com</b>"),
 (4,"living-in-carmel","Suburb Spotlight &middot; Hamilton County","Living in <em>Carmel</em>","",
   spotlight_body("Homes from the $400s to $1M+",
    ["Walkable Arts &amp; Design District and the Palladium","Nationally ranked Carmel Clay Schools","Roundabouts, the Monon Trail &amp; top-tier amenities"]),
   "Carmel guide &rarr; <b>yourrealtylink.com</b>"),
 (5,"kill-a-sale","Seller Tip","5 things that quietly <em>kill a sale</em>","",
   numbered(["Overpricing in the first week","Skipping the small repairs buyers notice","Dark photos and cluttered, un-staged rooms"]),
   "The full five &rarr; <b>yourrealtylink.com</b>"),
 (6,"carmel-vs-fishers","Suburb vs Suburb","Carmel <em>vs</em> Fishers","sm",
   compare_body("Carmel","$400s&ndash;$1M+ &middot; Carmel Clay Schools &middot; arts &amp; walkability",
                "Fishers","$300s&ndash;$600s &middot; Hamilton Southeastern &middot; more home per dollar",
                "Budget over the $400s and want walkable culture? <b>Carmel.</b> Want more house in a top district? <b>Fishers.</b>"),
   "Full comparison &rarr; <b>yourrealtylink.com</b>"),
 (7,"village-westclay","Community Spotlight &middot; Carmel","Village of <em>WestClay</em>","",
   spotlight_body("Homes from the $500s to $2M+",
    ["A walkable, master-planned village in Carmel","Parks, shops &amp; a genuine town-center feel","Inside top-rated Carmel Clay Schools"]),
   "Explore WestClay &rarr; <b>yourrealtylink.com</b>"),
 (8,"earnest-money","Real Estate, Explained","What is <em>earnest money?</em>","",
   explain_body("A good-faith deposit &mdash; usually <b>1&ndash;2%</b> &mdash; you put down when your offer is accepted. It tells the seller you&rsquo;re serious, sits in <b>escrow</b> (not the seller&rsquo;s pocket), and is credited back toward your down payment or closing costs at the finish line."),
   "More terms &rarr; <b>yourrealtylink.com/glossary</b>"),
 (9,"fall-in-central-indiana","Living Here &middot; Fall 2026","Fall is the <em>best season</em> here","",
   bullets(["Farmers markets and fall festivals across the suburbs","Apple orchards, corn mazes &amp; cider mills","A calmer home-shopping season &mdash; less competition"]),
   "Find your suburb &rarr; <b>yourrealtylink.com</b>"),
 (10,"down-payment-help","Finance &middot; First-Time Buyers","You may need <em>less down</em> than you think","sm",
   numbered(["Indiana programs offer real down-payment help","FHA &amp; USDA options for lower down payments","Plenty of buyers get in for far less than 20%"]),
   "See your options &rarr; <b>yourrealtylink.com</b>"),
 (11,"mccordsville","Suburb Spotlight &middot; Hancock County","<em>McCordsville</em> is booming","",
   spotlight_body("Homes from the $280s to $500s",
    ["One of Central Indiana&rsquo;s fastest-growing towns","New construction + the walkable McCord Square","Mt. Vernon schools and quick I-69 access"]),
   "McCordsville homes &rarr; <b>yourrealtylink.com</b>"),
 (12,"free-buyer-guide","Free Download","Free <em>home buyer&rsquo;s guide</em>","",
   cta_body("Get our free, city-specific guide &mdash; the local market, neighborhoods, schools, and every step from offer to keys. No cost, no obligation.",
            "Grab yours &rarr; yourrealtylink.com/resources"),
   "Free download &rarr; <b>yourrealtylink.com</b>"),
 (13,"whats-your-home-worth","For Sellers","What&rsquo;s your home <em>worth?</em>","",
   cta_body("Not a metro average &mdash; <b>your</b> home. Get a free, no-obligation valuation from a local MIBOR broker who actually knows your neighborhood.",
            "Free valuation &rarr; yourrealtylink.com"),
   "Free home valuation &rarr; <b>yourrealtylink.com</b>"),
 (14,"new-construction","Buyer Tip &middot; New Construction","New construction: <em>the fine print</em>","",
   numbered(["The builder&rsquo;s rep works for the builder &mdash; bring your own agent","Lock upgrades &amp; timelines in writing","Budget for blinds, fencing &amp; landscaping the quote skips"]),
   "New-build help &rarr; <b>yourrealtylink.com</b>"),
 (15,"fifty-five-plus","Lifestyle &middot; 55+ Living","<em>Right-sizing</em> after 55","",
   spotlight_body("Low-maintenance, single-level living",
    ["Active-adult communities across Central Indiana","One-level floor plans and lock-and-leave ease","Downsize without leaving the area you love"]),
   "55+ communities &rarr; <b>yourrealtylink.com</b>"),
 (16,"fall-move","Fall 2026","Thinking about a <em>move this fall?</em>","",
   cta_body("Buying, selling, or just curious what your home is worth &mdash; we&rsquo;re a local, full-service MIBOR team, and we&rsquo;d love to help.",
            "Let&rsquo;s talk &rarr; yourrealtylink.com"),
   "yourrealtylink.com &middot; <b>317-997-7404</b>"),
]

os.makedirs(OUTDIR, exist_ok=True)
# post 01: reuse the real market graphic
mkt = os.path.join(ROOT, "assets/img/market-reports/latest/central-indiana.png")
if os.path.exists(mkt):
    shutil.copy(mkt, os.path.join(OUTDIR, "01-market-update.png"))
    print("  ok 01-market-update (copied real market graphic)")

ok = 1
for num, slug, eyebrow, headline, h1cls, body, cta in CARDS:
    html = (SHELL.replace("__LOGO__", LOGO).replace("__EYEBROW__", eyebrow)
                 .replace("__H1CLASS__", h1cls).replace("__HEADLINE__", headline)
                 .replace("__BODY__", body).replace("__CTA__", cta).replace("__META__", FOOT_META))
    hp = os.path.join(SCRATCH, "sg_%02d.html" % num)
    open(hp, "w").write(html)
    out = os.path.join(OUTDIR, "%02d-%s.png" % (num, slug))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1080",
                    "--virtual-time-budget=2800", "--screenshot=" + out, "file://" + hp],
                   capture_output=True)
    if os.path.exists(out):
        ok += 1; print("  ok %02d-%s" % (num, slug))
print("rendered %d/16 -> %s" % (ok, os.path.relpath(OUTDIR, ROOT)))
