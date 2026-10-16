#!/usr/bin/env python3
"""Generate branded market-report social graphics (1080x1080) for the overall
MIBOR region + each of the 17 counties, from real MIBOR monthly figures.

Data is transcribed from the MIBOR Market Insights PDF (source, with attribution
on every graphic). Renders each region to assets/img/market-reports/<period>/.

    python3 build_market_social.py
"""
import os, base64, subprocess, shutil, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SCRATCH = __import__("tempfile").mkdtemp(prefix="ms_")
PERIOD = "2026-09"
MONTH = "September 2026"
MON = MONTH.split()[0]
OUTDIR = os.path.join(ROOT, "assets/img/market-reports", PERIOD)

# region slug -> (display label, median$, median YoY%, closed sales, sales YoY%,
#                 median days on market, prior-year DOM, months supply)
DATA = {
 "central-indiana": ("Central Indiana · 17 Counties", 320000, 1.3, 2549, -3.5, "27", "20", 2.9),
 "bartholomew-county": ("Bartholomew County, IN", 295000, 5.4, 81, -15.6, "32", "21", 3.1),
 "boone-county":       ("Boone County, IN", 404949, 1.4, 128, 50.6, "21", "17", 2.0),
 "brown-county":       ("Brown County, IN", 412000, 10.9, 13, -45.8, "46", "22", 7.7),
 "decatur-county":     ("Decatur County, IN", 247000, -1.6, 26, -13.3, "60", "23", 2.3),
 "hamilton-county":    ("Hamilton County, IN", 487000, -2.2, 475, -1.7, "25.5", "16", 2.1),
 "hancock-county":     ("Hancock County, IN", 349100, -5.7, 139, 11.2, "43.5", "20.5", 2.7),
 "hendricks-county":   ("Hendricks County, IN", 370000, 5.7, 217, -15.6, "26", "19.5", 2.6),
 "jackson-county":     ("Jackson County, IN", 215000, -9.5, 31, -22.5, "13.5", "28", 4.0),
 "jennings-county":    ("Jennings County, IN", 233500, -5.5, 15, -21.1, "33", "36", 3.0),
 "johnson-county":     ("Johnson County, IN", 349900, 0.3, 215, -2.7, "32", "20", 2.6),
 "madison-county":     ("Madison County, IN", 218450, 27.0, 128, 2.4, "28", "13", 3.1),
 "marion-county":      ("Marion County · Indianapolis", 255000, 2.0, 873, -6.3, "24", "22", 3.5),
 "montgomery-county":  ("Montgomery County, IN", 200000, -3.6, 39, -2.5, "39", "16", 2.0),
 "morgan-county":      ("Morgan County, IN", 285000, -5.0, 72, 0.0, "18", "27", 3.1),
 "parke-county":       ("Parke County, IN", 169900, -32.0, 4, -55.6, "34.5", "10", 13.2),
 "putnam-county":      ("Putnam County, IN", 300000, 5.3, 45, 55.2, "26", "14", 2.7),
 "shelby-county":      ("Shelby County, IN", 230000, -9.5, 48, -9.4, "30.5", "26", 2.6),
}

def money(n):  return "${:,}".format(n)
def pct(v):    return ("%.1f" % abs(v)).rstrip("0").rstrip(".")
def price_sub(yoy):
    if yoy > 0.5:  return "Up %s%% from last %s" % (pct(yoy), MON)
    if yoy < -0.5: return "Down %s%% from last %s" % (pct(yoy), MON)
    return "About flat vs. last %s" % MON
def sales_sub(yoy):
    if yoy > 0.5:  return "Up %s%% year-over-year" % pct(yoy)
    if yoy < -0.5: return "Down %s%% year-over-year" % pct(yoy)
    return "About flat year-over-year"
def dom_sub(cur, prior):
    fc, fp = float(cur), float(prior)
    if fc > fp:  return "Up from %s a year ago" % prior
    if fc < fp:  return "Down from %s a year ago" % prior
    return "Same as a year ago"
def months_desc(m):
    if m < 3:   return "Still a seller-leaning market"
    if m < 5:   return "Moving toward balance"
    if m <= 7:  return "A balanced market"
    return "A buyer-leaning market"

LOGO = base64.b64encode(open(os.path.join(ROOT, "assets/img/yrl-logo.png"), "rb").read()).decode()

TPL = """<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Libre+Franklin:wght@400;500;600;700;800&display=swap">
<style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{width:1080px;height:1080px;overflow:hidden;font-family:"Libre Franklin",system-ui,sans-serif;background:#f7f3ef;color:#1e1a17}}
 .card{{width:1080px;height:1080px;padding:64px 64px 56px;display:flex;flex-direction:column;position:relative}}
 .card::after{{content:"";position:absolute;right:-140px;top:-140px;width:420px;height:420px;border-radius:50%;background:rgba(192,57,38,.06)}}
 .top{{display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:2}}
 .logo{{height:66px}}
 .eyebrow{{text-align:right;font-size:19px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#c03926;line-height:1.5;margin-top:6px}}
 .eyebrow span{{display:block;color:#6e6e70;font-weight:700;font-size:16px;letter-spacing:.06em}}
 h1{{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:74px;line-height:1;margin:36px 0 6px;color:#17130f}}
 h1 em{{font-style:normal;color:#c03926}}
 .rule{{width:96px;height:6px;background:#c03926;border-radius:3px;margin:14px 0 0}}
 .src{{font-size:18px;color:#6e6e70;font-weight:600;margin-top:18px;position:relative;z-index:2}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:26px;flex:1}}
 .tile{{background:#fff;border:1px solid #ece4dc;border-radius:20px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 6px 22px rgba(40,25,20,.05)}}
 .tile .lab{{background:#c03926;color:#fff;font-size:19px;font-weight:800;padding:16px 24px}}
 .tile .body{{padding:22px 24px 24px;display:flex;flex-direction:column;justify-content:center;flex:1}}
 .tile .val{{font-family:"Playfair Display",Georgia,serif;font-weight:800;font-size:54px;line-height:1.02;color:#17130f}}
 .tile .val.red{{color:#c03926}}
 .tile .sub{{font-size:19px;color:#6e6e70;margin-top:10px;line-height:1.4;font-weight:500}}
 .foot{{margin-top:34px;background:#17130f;border-radius:18px;padding:22px 30px;display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}}
 .foot .cta{{color:#fff;font-size:24px;font-weight:800}}
 .foot .cta b{{color:#e0644f}}
 .foot .meta{{color:#c9bfb6;font-size:17px;font-weight:600;text-align:right;line-height:1.4}}
 .foot .meta b{{color:#fff}}
</style>
<div class="card">
 <div class="top">
  <img class="logo" src="data:image/png;base64,{logo}">
  <div class="eyebrow">{month}<span>{label}</span></div>
 </div>
 <h1>Real Estate <em>Market Report</em></h1>
 <div class="rule"></div>
 <div class="src">Single-family homes · Source: MIBOR REALTOR&reg; Association</div>
 <div class="grid">
  <div class="tile"><div class="lab">Median sale price</div><div class="body"><div class="val red">{median}</div><div class="sub">{median_sub}</div></div></div>
  <div class="tile"><div class="lab">Homes sold in {mon}</div><div class="body"><div class="val">{sales}</div><div class="sub">{sales_sub}</div></div></div>
  <div class="tile"><div class="lab">Median days on market</div><div class="body"><div class="val">{dom} days</div><div class="sub">{dom_sub}</div></div></div>
  <div class="tile"><div class="lab">Months of supply</div><div class="body"><div class="val red">{months}</div><div class="sub">{months_sub}</div></div></div>
 </div>
 <div class="foot">
  <div class="cta">Full report &rarr; <b>yourrealtylink.com</b></div>
  <div class="meta"><b>Your Realty Link</b> &middot; Janet Giles, Broker<br>317-997-7404</div>
 </div>
</div>"""

BANNER = """<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Libre+Franklin:wght@400;500;600;700;800&display=swap">
<style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{width:1600px;height:600px;overflow:hidden;font-family:"Libre Franklin",system-ui,sans-serif;background:#f7f3ef;color:#1e1a17}}
 .b{{width:1600px;height:600px;padding:48px 54px;display:flex;gap:46px;position:relative}}
 .b::after{{content:"";position:absolute;left:-120px;bottom:-160px;width:380px;height:380px;border-radius:50%;background:rgba(192,57,38,.06)}}
 .L{{width:560px;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}}
 .L img{{height:60px;align-self:flex-start;margin-bottom:22px}}
 .eb{{font-size:17px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#c03926}}
 .eb span{{color:#6e6e70}}
 .L h1{{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:58px;line-height:1.02;margin:12px 0 0;color:#17130f}}
 .L h1 em{{font-style:normal;color:#c03926}}
 .rule{{width:84px;height:6px;background:#c03926;border-radius:3px;margin:18px 0 16px}}
 .src{{font-size:15px;color:#6e6e70;font-weight:600}}
 .cta{{margin-top:auto;font-size:19px;font-weight:800;color:#17130f;padding-top:20px}}
 .cta b{{color:#c03926}}
 .R{{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px;position:relative;z-index:2}}
 .t{{background:#fff;border:1px solid #ece4dc;border-radius:16px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 5px 18px rgba(40,25,20,.05)}}
 .t .lab{{background:#c03926;color:#fff;font-size:15px;font-weight:800;padding:11px 18px}}
 .t .bd{{padding:14px 18px 16px;display:flex;flex-direction:column;justify-content:center;flex:1}}
 .t .val{{font-family:"Playfair Display",Georgia,serif;font-weight:800;font-size:40px;line-height:1;color:#17130f}}
 .t .val.red{{color:#c03926}}
 .t .sub{{font-size:14px;color:#6e6e70;margin-top:7px;font-weight:500;line-height:1.35}}
</style>
<div class="b">
 <div class="L">
  <img src="data:image/png;base64,{logo}">
  <div class="eb">{month} <span>&middot; {label}</span></div>
  <h1>Real Estate<br><em>Market Report</em></h1>
  <div class="rule"></div>
  <div class="src">Single-family homes &middot; Source: MIBOR REALTOR&reg; Association</div>
  <div class="cta">Full report &rarr; <b>yourrealtylink.com</b> &middot; 317-997-7404</div>
 </div>
 <div class="R">
  <div class="t"><div class="lab">Median sale price</div><div class="bd"><div class="val red">{median}</div><div class="sub">{median_sub}</div></div></div>
  <div class="t"><div class="lab">Homes sold in {mon}</div><div class="bd"><div class="val">{sales}</div><div class="sub">{sales_sub}</div></div></div>
  <div class="t"><div class="lab">Median days on market</div><div class="bd"><div class="val">{dom} days</div><div class="sub">{dom_sub}</div></div></div>
  <div class="t"><div class="lab">Months of supply</div><div class="bd"><div class="val red">{months}</div><div class="sub">{months_sub}</div></div></div>
 </div>
</div>"""

# ---- downloadable 1-page PDF report (lead-magnet gated on the market-updates page) ----
PDFDIR = os.path.join(ROOT, "assets/pdf/market-reports", "latest")

def region_name(label):
    return label.split(",")[0].split("·")[0].strip()

def takeaway(name, med, med_yoy, dom, months):
    if med_yoy > 0.5:   t = "up %s%% year-over-year" % pct(med_yoy)
    elif med_yoy < -0.5: t = "down %s%% year-over-year" % pct(med_yoy)
    else:               t = "about flat year-over-year"
    if months < 3:   cond = "a seller-leaning market — inventory is still tight"
    elif months < 5: cond = "moving toward a balanced market"
    elif months <= 7: cond = "a balanced market"
    else:            cond = "a buyer-leaning market"
    return ("In %s, the median single-family home sold for %s (%s), in a median of %s days. "
            "At %s months of supply, it is %s." % (name, money(med), t, dom, ("%.1f" % months), cond))

PDF_TPL = """<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Libre+Franklin:wght@400;500;600;700&display=swap">
<style>
 @page{{size:letter;margin:0}}
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{font-family:"Libre Franklin",system-ui,sans-serif;color:#1e1a17}}
 .pg{{width:8.5in;min-height:11in;padding:.55in .6in;display:flex;flex-direction:column}}
 .hd{{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #c03926;padding-bottom:12px;margin-bottom:20px}}
 .hd img{{height:.5in}}
 .hd .m{{text-align:right;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#c03926;line-height:1.5}}
 h1{{font-family:"Playfair Display",serif;font-size:27px;margin:0 0 3px;color:#17130f}}
 .sub{{color:#6e6e70;font-size:12px;margin:0 0 18px}}
 .report{{width:100%;border-radius:12px;box-shadow:0 6px 18px rgba(0,0,0,.10)}}
 .take{{font-size:13.5px;color:#3a332e;line-height:1.65;margin:20px 0 0}}
 .cta{{margin-top:auto;background:#17130f;color:#fff;border-radius:12px;padding:16px 22px;font-size:13px;line-height:1.55}}
 .cta b{{color:#e0644f}}
</style>
<div class="pg">
 <div class="hd"><img src="data:image/png;base64,{logo}"><div class="m">{month}<br>{label}</div></div>
 <h1>{name} Market Report</h1>
 <p class="sub">Single-family homes &middot; Source: MIBOR REALTOR&reg; Association</p>
 <img class="report" src="data:image/png;base64,{img}">
 <p class="take">{take}</p>
 <div class="cta">Want your home&rsquo;s exact value &mdash; not a metro average? Get a free, no-obligation valuation at <b>yourrealtylink.com/services/free-home-valuation</b><br>Janet Giles-Schultz, Principal Broker &middot; Your Realty Link &middot; <b>317-997-7404</b></div>
</div>"""

# MARKET_GBP_ONLY=1 re-renders just the Google Business Profile cards (skips squares/banners/PDFs)
GBP_ONLY = bool(os.environ.get("MARKET_GBP_ONLY"))

os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(PDFDIR, exist_ok=True)
ok = 0
for slug, (label, med, med_yoy, sales, sales_yoy, dom, dom_prior, months) in ([] if GBP_ONLY else DATA.items()):
    html = TPL.format(
        logo=LOGO, month=MONTH, mon=MON, label=H.escape(label),
        median=money(med), median_sub=price_sub(med_yoy),
        sales="{:,}".format(sales), sales_sub=sales_sub(sales_yoy),
        dom=dom, dom_sub=dom_sub(dom, dom_prior),
        months=("%.1f" % months), months_sub=months_desc(months))
    hp = os.path.join(SCRATCH, "ms_%s.html" % slug)
    open(hp, "w").write(html)
    out = os.path.join(OUTDIR, slug + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1080",
                    "--virtual-time-budget=2500", "--screenshot=" + out, "file://" + hp],
                   capture_output=True)
    # wide banner (Facebook cover / blog hero)
    bhtml = BANNER.format(
        logo=LOGO, month=MONTH, mon=MON, label=H.escape(label),
        median=money(med), median_sub=price_sub(med_yoy),
        sales="{:,}".format(sales), sales_sub=sales_sub(sales_yoy),
        dom=dom, dom_sub=dom_sub(dom, dom_prior),
        months=("%.1f" % months), months_sub=months_desc(months))
    bhp = os.path.join(SCRATCH, "mb_%s.html" % slug)
    open(bhp, "w").write(bhtml)
    bout = os.path.join(OUTDIR, slug + "-banner.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1600,600",
                    "--virtual-time-budget=2500", "--screenshot=" + bout, "file://" + bhp],
                   capture_output=True)
    # downloadable 1-page PDF (embeds the just-rendered square graphic)
    if os.path.exists(out):
        img_b64 = base64.b64encode(open(out, "rb").read()).decode()
        name = region_name(label)
        phtml = PDF_TPL.format(logo=LOGO, month=MONTH, label=H.escape(label), name=H.escape(name),
                               img=img_b64, take=H.escape(takeaway(name, med, med_yoy, dom, months)))
        php = os.path.join(SCRATCH, "mp_%s.html" % slug)
        open(php, "w").write(phtml)
        ppdf = os.path.join(PDFDIR, slug + ".pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf=" + ppdf, "file://" + php], capture_output=True)
    if os.path.exists(out):
        ok += 1
        print("  ok", slug)
print("rendered %d/%d (square + banner) -> %s" % (ok, len(DATA), os.path.relpath(OUTDIR, ROOT)))

# ---- Google Business Profile card (1200x900, Google's 4:3 slot — no phone number) ----
GBPDIR = os.path.join(OUTDIR, "gbp-%s-%s" % (MON.lower(), MONTH.split()[1]))

GBP = """<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Libre+Franklin:wght@400;500;600;700;800&display=swap">
<style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{width:1200px;height:900px;overflow:hidden;font-family:"Libre Franklin",system-ui,sans-serif;background:#f7f3ef;color:#1e1a17}}
 .card{{width:1200px;height:900px;padding:56px 60px 52px;display:flex;flex-direction:column;position:relative}}
 .card::after{{content:"";position:absolute;right:-150px;top:-150px;width:440px;height:440px;border-radius:50%;background:rgba(192,57,38,.06)}}
 .top{{display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:2}}
 .logo{{height:62px}}
 .eyebrow{{text-align:right;font-size:18px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#c03926;line-height:1.5;margin-top:4px}}
 .eyebrow span{{display:block;color:#6e6e70;font-weight:700;font-size:15px;letter-spacing:.06em}}
 h1{{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:66px;line-height:1;margin:28px 0 6px;color:#17130f}}
 h1 em{{font-style:normal;color:#c03926}}
 .rule{{width:88px;height:6px;background:#c03926;border-radius:3px;margin:12px 0 0}}
 .src{{font-size:17px;color:#6e6e70;font-weight:600;margin-top:16px;position:relative;z-index:2}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:22px;flex:1}}
 .tile{{background:#fff;border:1px solid #ece4dc;border-radius:18px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 6px 20px rgba(40,25,20,.05)}}
 .tile .lab{{background:#c03926;color:#fff;font-size:18px;font-weight:800;padding:14px 22px}}
 .tile .body{{padding:20px 22px 22px;display:flex;flex-direction:column;justify-content:center;flex:1}}
 .tile .val{{font-family:"Playfair Display",Georgia,serif;font-weight:800;font-size:50px;line-height:1.02;color:#17130f}}
 .tile .val.red{{color:#c03926}}
 .tile .sub{{font-size:18px;color:#6e6e70;margin-top:9px;line-height:1.4;font-weight:500}}
 .foot{{margin-top:26px;background:#17130f;border-radius:16px;padding:20px 28px;display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}}
 .foot .cta{{color:#fff;font-size:22px;font-weight:800}}
 .foot .cta b{{color:#e0644f}}
 .foot .meta{{color:#c9bfb6;font-size:16px;font-weight:600;text-align:right}}
 .foot .meta b{{color:#fff}}
</style>
<div class="card">
 <div class="top">
  <img class="logo" src="data:image/png;base64,{logo}">
  <div class="eyebrow">{month}<span>{label}</span></div>
 </div>
 <h1>Real Estate <em>Market Report</em></h1>
 <div class="rule"></div>
 <div class="src">Single-family homes &middot; Source: MIBOR REALTOR&reg; Association</div>
 <div class="grid">
  <div class="tile"><div class="lab">Median sale price</div><div class="body"><div class="val red">{median}</div><div class="sub">{median_sub}</div></div></div>
  <div class="tile"><div class="lab">Homes sold in {mon}</div><div class="body"><div class="val">{sales}</div><div class="sub">{sales_sub}</div></div></div>
  <div class="tile"><div class="lab">Median days on market</div><div class="body"><div class="val">{dom} days</div><div class="sub">{dom_sub}</div></div></div>
  <div class="tile"><div class="lab">Months of supply</div><div class="body"><div class="val red">{months}</div><div class="sub">{months_sub}</div></div></div>
 </div>
 <div class="foot">
  <div class="cta">Full report &rarr; <b>yourrealtylink.com</b></div>
  <div class="meta"><b>Your Realty Link</b> &middot; Janet Giles, Broker</div>
 </div>
</div>"""

os.makedirs(GBPDIR, exist_ok=True)
gok = 0
for slug, (label, med, med_yoy, sales, sales_yoy, dom, dom_prior, months) in DATA.items():
    ghtml = GBP.format(
        logo=LOGO, month=MONTH, mon=MON, label=H.escape(label),
        median=money(med), median_sub=price_sub(med_yoy),
        sales="{:,}".format(sales), sales_sub=sales_sub(sales_yoy),
        dom=dom, dom_sub=dom_sub(dom, dom_prior),
        months=("%.1f" % months), months_sub=months_desc(months))
    ghp = os.path.join(SCRATCH, "mg_%s.html" % slug)
    open(ghp, "w").write(ghtml)
    gout = os.path.join(GBPDIR, slug + "-gbp.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,900",
                    "--virtual-time-budget=2500", "--screenshot=" + gout, "file://" + ghp],
                   capture_output=True)
    if os.path.exists(gout):
        gok += 1
print("rendered %d/%d GBP 1200x900 -> %s" % (gok, len(DATA), os.path.relpath(GBPDIR, ROOT)))

# mirror to a stable "latest/" folder so on-site embeds never go stale month to month
LATEST = os.path.join(ROOT, "assets/img/market-reports", "latest")
if not GBP_ONLY and os.path.isdir(LATEST):
    shutil.rmtree(LATEST)
if not GBP_ONLY:
    shutil.copytree(OUTDIR, LATEST, ignore=shutil.ignore_patterns("gbp-*"))
    print("mirrored -> assets/img/market-reports/latest")
