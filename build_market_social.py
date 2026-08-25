#!/usr/bin/env python3
"""Generate branded market-report social graphics (1080x1080) for the overall
MIBOR region + each of the 17 counties, from real MIBOR monthly figures.

Data is transcribed from the MIBOR Market Insights PDF (source, with attribution
on every graphic). Renders each region to assets/img/market-reports/<period>/.

    python3 build_market_social.py
"""
import os, base64, subprocess, shutil, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCRATCH = "/private/tmp/claude-501/-Users-danielcope-Library-Mobile-Documents-com-apple-CloudDocs-Claude-YRL/26f905d9-f2dc-48a5-9205-1e23c0b750ad/scratchpad"
PERIOD = "2026-07"
MONTH = "July 2026"
OUTDIR = os.path.join(ROOT, "assets/img/market-reports", PERIOD)

# region slug -> (display label, median$, median YoY%, closed sales, sales YoY%,
#                 median days on market, prior-year DOM, months supply)
DATA = {
 "central-indiana": ("Central Indiana · 17 Counties", 330000, 1.5, 3053, 6.1, "20", "16", 2.2),
 "bartholomew-county": ("Bartholomew County, IN", 297000, 18.8, 96, -4.0, "16.5", "8.5", 2.2),
 "boone-county":       ("Boone County, IN", 418000, -9.0, 137, 19.1, "27", "16", 1.6),
 "brown-county":       ("Brown County, IN", 330000, -34.3, 26, 18.2, "15", "39.5", 2.9),
 "decatur-county":     ("Decatur County, IN", 200000, -9.7, 25, 25.0, "34", "32", 2.6),
 "hamilton-county":    ("Hamilton County, IN", 489990, 1.4, 601, 4.3, "12", "13", 1.5),
 "hancock-county":     ("Hancock County, IN", 335000, -5.2, 160, 5.3, "32", "17", 2.3),
 "hendricks-county":   ("Hendricks County, IN", 363000, -0.6, 211, -16.3, "15", "22", 2.3),
 "jackson-county":     ("Jackson County, IN", 238450, 14.1, 42, 20.0, "18", "13", 2.5),
 "jennings-county":    ("Jennings County, IN", 200000, 1.5, 31, 6.9, "31", "18.5", 1.4),
 "johnson-county":     ("Johnson County, IN", 339900, 0.0, 268, 21.3, "26", "23", 2.0),
 "madison-county":     ("Madison County, IN", 236500, 12.7, 164, 5.8, "28", "15.5", 2.7),
 "marion-county":      ("Marion County · Indianapolis", 270000, 1.9, 1051, 9.6, "21", "16", 2.7),
 "montgomery-county":  ("Montgomery County, IN", 239950, 3.2, 50, -5.7, "10.5", "10.5", 1.7),
 "morgan-county":      ("Morgan County, IN", 318450, -2.0, 100, -1.0, "19.5", "24", 1.8),
 "parke-county":       ("Parke County, IN", 165000, -35.0, 9, 50.0, "36", "31", 4.1),
 "putnam-county":      ("Putnam County, IN", 307500, 17.1, 36, -10.0, "25.5", "35", 2.7),
 "shelby-county":      ("Shelby County, IN", 246000, -1.6, 46, 12.2, "29", "16.5", 2.6),
}

def money(n):  return "${:,}".format(n)
def pct(v):    return ("%.1f" % abs(v)).rstrip("0").rstrip(".")
def price_sub(yoy):
    if yoy > 0.5:  return "Up %s%% from last July" % pct(yoy)
    if yoy < -0.5: return "Down %s%% from last July" % pct(yoy)
    return "About flat vs. last July"
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
  <div class="tile"><div class="lab">Homes sold in July</div><div class="body"><div class="val">{sales}</div><div class="sub">{sales_sub}</div></div></div>
  <div class="tile"><div class="lab">Median days on market</div><div class="body"><div class="val">{dom} days</div><div class="sub">{dom_sub}</div></div></div>
  <div class="tile"><div class="lab">Months of supply</div><div class="body"><div class="val red">{months}</div><div class="sub">{months_sub}</div></div></div>
 </div>
 <div class="foot">
  <div class="cta">Full report &rarr; <b>janetgiles.com</b></div>
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
  <div class="cta">Full report &rarr; <b>janetgiles.com</b> &middot; 317-997-7404</div>
 </div>
 <div class="R">
  <div class="t"><div class="lab">Median sale price</div><div class="bd"><div class="val red">{median}</div><div class="sub">{median_sub}</div></div></div>
  <div class="t"><div class="lab">Homes sold in July</div><div class="bd"><div class="val">{sales}</div><div class="sub">{sales_sub}</div></div></div>
  <div class="t"><div class="lab">Median days on market</div><div class="bd"><div class="val">{dom} days</div><div class="sub">{dom_sub}</div></div></div>
  <div class="t"><div class="lab">Months of supply</div><div class="bd"><div class="val red">{months}</div><div class="sub">{months_sub}</div></div></div>
 </div>
</div>"""

os.makedirs(OUTDIR, exist_ok=True)
ok = 0
for slug, (label, med, med_yoy, sales, sales_yoy, dom, dom_prior, months) in DATA.items():
    html = TPL.format(
        logo=LOGO, month=MONTH, label=H.escape(label),
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
        logo=LOGO, month=MONTH, label=H.escape(label),
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
    if os.path.exists(out):
        ok += 1
        print("  ok", slug)
print("rendered %d/%d (square + banner) -> %s" % (ok, len(DATA), os.path.relpath(OUTDIR, ROOT)))

# mirror to a stable "latest/" folder so on-site embeds never go stale month to month
LATEST = os.path.join(ROOT, "assets/img/market-reports", "latest")
if os.path.isdir(LATEST):
    shutil.rmtree(LATEST)
shutil.copytree(OUTDIR, LATEST)
print("mirrored -> assets/img/market-reports/latest")
