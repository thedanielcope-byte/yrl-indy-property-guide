#!/usr/bin/env python3
"""Add a "<Town> Housing Market" block with the county's latest MIBOR figures to every city page.

Reads DATA / MONTH from build_market_social.py (the monthly market routine updates that file
each month), so re-running this after the routine refreshes the figures keeps all city pages
current. MIBOR reports by county, so each town shows its county's numbers, labelled as such.

Marker-wrapped (<!-- CITY-MARKET --> ... <!-- /CITY-MARKET -->) and idempotent. The block sits
right after the first paragraph under the city's "Home Prices & Real Estate Market" heading.

    python3 inject_city_market.py          # apply
    python3 inject_city_market.py --check  # report only
"""
import ast, glob, html, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
START, END = "<!-- CITY-MARKET -->", "<!-- /CITY-MARKET -->"


def load_market():
    tree = ast.parse(open("build_market_social.py", encoding="utf-8").read())
    vals = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("DATA", "MONTH", "PERIOD"):
                vals[name] = ast.literal_eval(node.value)
    return vals["DATA"], vals["MONTH"]


def pct(v, unit="vs. a year earlier"):
    if abs(v) < 0.05:
        return f"flat {unit}"
    return f"{'up' if v > 0 else 'down'} {abs(v):.1f}% {unit}"


def supply_note(m):
    if m < 3:
        return "leans to sellers"
    if m < 5:
        return "moving toward balance"
    if m < 6.5:
        return "roughly balanced"
    return "leans to buyers"


def tile(label, value, sub):
    return (f'<div style="background:#fff;border:1px solid #e6e1dc;border-radius:12px;padding:12px;">'
            f'<div style="font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#6e6e70;">{label}</div>'
            f'<div style="font-size:1.3rem;font-weight:800;color:#1a1a1a;margin-top:4px;font-variant-numeric:tabular-nums;">{value}</div>'
            f'<div style="font-size:.85rem;color:#6e6e70;margin-top:2px;">{sub}</div></div>')


def block(city, county_slug, row, month):
    _, med, med_yoy, sales, sales_yoy, dom, dom_prior, supply = row
    county = county_slug.replace("-county", "").replace("-", " ").title()
    c_city, c_county = html.escape(city), html.escape(county)
    caveat = (f" With only {sales} sales in the county that month, the median can swing a lot from month to month."
              if sales < 60 else "")
    county_page = f"counties/{county_slug}-indiana-real-estate/index.html"
    county_link = (f' &middot; <a href="/counties/{county_slug}-indiana-real-estate/">{c_county} County real estate</a>'
                   if os.path.exists(county_page) else "")
    tiles = "".join([
        tile("Median sale price", f"${med:,.0f}", pct(med_yoy)),
        tile("Homes sold", f"{sales:,}", pct(sales_yoy)),
        tile("Median days on market", dom, f"{dom_prior} a year earlier"),
        tile("Months of supply", f"{supply:.1f}", supply_note(supply)),
    ])
    return f"""{START}
 <div class="city-market" style="margin:22px 0 26px;padding:20px;background:#f7f7f7;border-radius:16px;">
 <h3 style="margin:0 0 6px;">{c_city} Housing Market: {month} Numbers</h3>
 <p style="margin:0 0 14px;">{c_city} is in {c_county} County, and MIBOR reports the market by county, so these are {c_county} County&rsquo;s figures for {month}. Prices in {c_city} itself can run higher or lower.{caveat}</p>
 <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;">{tiles}</div>
 <p style="margin:12px 0 0;font-size:.85rem;color:#6e6e70;">Source: MIBOR REALTOR Association, {month}, single-family homes. Updated monthly. <a href="/market-updates/">Latest market update</a>{county_link}</p>
 </div>
{END}"""


def city_name(s):
    m = re.search(r"<h2[^>]*>([^<]*?) Home Prices", s)
    if m:
        return html.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip())
    m = re.search(r"<title>(.+?), IN ", s)
    return html.unescape(m.group(1)) if m else None


def main():
    check = "--check" in sys.argv
    data, month = load_market()
    done = skipped = 0
    for f in sorted(glob.glob("cities/*/*/index.html")):
        s = open(f, encoding="utf-8").read()
        if 'http-equiv="refresh"' in s:
            continue
        county_slug = f.split("/")[1]
        row = data.get(county_slug)
        city = city_name(s)
        if not row or not city:
            print("SKIP", f, "no county data" if not row else "no city name")
            skipped += 1
            continue
        new = block(city, county_slug, row, month)
        base = re.sub(r"\n ?" + re.escape(START) + r".*?" + re.escape(END), "", s, flags=re.S)
        if True:
            s = base
            m = re.search(r"<h2[^>]*>(?:(?!</h2>).)*?(?:Home Prices|Market)(?:(?!</h2>).)*?</h2>", s, re.S)
            if not m:
                print("SKIP", f, "no market heading"); skipped += 1; continue
            p_end = s.find("</p>", m.end())
            if p_end < 0:
                print("SKIP", f, "no paragraph"); skipped += 1; continue
            p_end += len("</p>")
            s2 = s[:p_end] + "\n " + new + s[p_end:]
        orig = open(f, encoding="utf-8").read()
        if s2 != orig:
            done += 1
            if not check:
                open(f, "w", encoding="utf-8").write(s2)
    print(f"{'would update' if check else 'updated'} {done} city pages, skipped {skipped}, figures: {month}")


if __name__ == "__main__":
    main()
