#!/usr/bin/env python3
"""build_col_calculator.py: /cost-of-living-calculator-indianapolis/ (Nov 2026).

A salary-equivalence calculator (any U.S. metro, or a state's nonmetro areas, vs. the
Indianapolis metro, both directions, with a category breakdown), a $100,000 "popular
comparisons" table, and a Central Indiana section (pick-two-towns compare + sortable county
table) built only from figures already in this repo.

DATA SOURCE (price parities)
  U.S. Bureau of Economic Analysis (BEA), Regional Price Parities (RPPs). Latest year: 2024,
  published February 19, 2026 ("new statistics for 2024; revised statistics for 2008-2023").
    Table MARPP  "Regional price parities by MSA"     -> every metro area + U.S. nonmetro portion
    Table PARPP  "Regional price parities by portion" -> each state's nonmetropolitan portion
    Lines: 1 All items, 2 Goods, 3 Services: Housing (rents), 4 Services: Utilities, 5 Services: Other
    Downloads: https://apps.bea.gov/regional/zip/MARPP.zip  https://apps.bea.gov/regional/zip/PARPP.zip
    About:     https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area
  Metro areas follow OMB Bulletin 23-01 (July 21, 2023), so Indianapolis is BEA's
  "Indianapolis-Carmel-Greenwood, IN" (GeoFIPS 26900). States with no nonmetro portion
  (BEA reports 0.000: DE, DC, NJ, RI) are dropped.
  Cleaned to assets/data/rpp-<year>.json: one row per area, [GeoFIPS, name, kind, [line 1..5]],
  kind m = metro, n = state nonmetro portion, u = U.S. The page inlines that file.

CENTRAL INDIANA FIGURES (repo only, nothing invented)
  build_market_social.py  DATA / MONTH  MIBOR monthly county figures (updated by the monthly routine)
  inject_tax_2027.py      COUNTIES      2026 district-median property tax rate per $100 AV (DLGF via
                                        STATS Indiana) + 2026 county local income tax (Indiana DOR)
  city_guides_data.py     CITIES        typical price ranges for 62 towns (our city guides)
  Indianapolis's own range ("$150s to $500s+") is the site's standard tier, as used in
  fresh_posts/cost-of-living-in-indianapolis.py.

USAGE
  python3 build_col_calculator.py                 rebuild the page from the newest assets/data/rpp-*.json
  python3 build_col_calculator.py --download      fetch MARPP.zip + PARPP.zip from BEA, write
                                                  assets/data/rpp-<newest year>.json, then rebuild
  python3 build_col_calculator.py --from-dir DIR  same, from zips or extracted CSVs already in DIR
  A new BEA year = `python3 build_col_calculator.py --download` (one command). The zips are read
  in memory, never extracted. Re-run monthly after build_market_social.py gets the new MIBOR month.
  Afterwards: inject_gtag.py, inject_favicon.py, inject_seo_overrides.py, gloss_autolink.py . --apply,
  refresh_sitemap_lastmod.py.
"""
import ast, base64, csv, datetime, glob, html, importlib.util, io, json, math, os, re, subprocess, sys, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://yourrealtylink.com"
SLUG = "cost-of-living-calculator-indianapolis"
URL = f"{SITE}/{SLUG}/"
OUT = os.path.join(ROOT, SLUG, "index.html")
DATA_DIR = os.path.join(ROOT, "assets", "data")
OG_IMG = "/assets/img/social/cost-of-living-calculator.png"
INDY = "26900"
BEA_PAGE = "https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area"
ZIPS = {"MARPP": "https://apps.bea.gov/regional/zip/MARPP.zip", "PARPP": "https://apps.bea.gov/regional/zip/PARPP.zip"}
TABLE_NAMES = {"MARPP": "Regional price parities by MSA", "PARPP": "Regional price parities by portion"}
UPDATED = datetime.date.today().strftime("%B %Y")

TITLE = "Indianapolis Cost of Living Calculator | Your Realty Link"
DESC = ("Compare your salary with Indianapolis. Our cost of living calculator uses 2024 BEA price data "
        "for every U.S. metro, plus Central Indiana county costs.")

# Popular origin metros for the static $100,000 table, with our "moving from" guide where one exists.
def _g(slug, label):
    return (f"/blog/moving-from-{slug}-to-indianapolis/", label)
CA = _g("california", "California")
POPULAR = [("35620", _g("new-york", "New York")), ("31080", CA), ("16980", _g("chicago", "Chicago")),
           ("19100", None), ("26420", None), ("47900", None), ("37980", None), ("33100", None), ("12060", None),
           ("14460", None), ("38060", None), ("41860", CA), ("42660", None), ("19740", None), ("33460", None),
           ("41740", CA), ("12420", None), ("16740", None), ("34980", None), ("18140", _g("columbus", "Columbus")),
           ("17140", _g("cincinnati", "Cincinnati")), ("31140", _g("louisville", "Louisville")),
           ("41180", _g("st-louis", "St. Louis")), ("19820", _g("detroit", "Detroit"))]
# Extra search words so "nyc", "bay area", "vegas" etc. find the right metro.
ALIASES = {"35620": "nyc manhattan brooklyn queens bronx long island", "41860": "sf bay area", "41940": "silicon valley bay area",
           "31080": "la", "47900": "dc", "19100": "dfw", "37980": "philly", "33460": "twin cities", "29820": "vegas",
           "16980": "chicagoland", "14460": "cambridge"}


# ───────────────────────── BEA data: download / parse / clean ─────────────────────────

def _decode(b):
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1")


def _from_zip(blob, table):
    zf = zipfile.ZipFile(io.BytesIO(blob))
    out = {}
    for n in zf.namelist():
        if re.fullmatch(rf"{table}_[A-Z]+_\d{{4}}_\d{{4}}\.csv", os.path.basename(n)):
            out["csv"] = _decode(zf.read(n))
        elif os.path.basename(n) == f"{table}__Footnotes.html":
            out["notes"] = _decode(zf.read(n))
    if "csv" not in out:
        raise SystemExit(f"{table}: no {table}_*.csv inside the zip")
    return out


def fetch_tables(src_dir=None):
    tabs = {}
    for t, u in ZIPS.items():
        if src_dir:
            z = os.path.join(src_dir, f"{t}.zip")
            if os.path.isfile(z):
                tabs[t] = _from_zip(open(z, "rb").read(), t)
                continue
            hits = sorted(glob.glob(os.path.join(src_dir, "**", f"{t}_*_*_*.csv"), recursive=True))
            if not hits:
                raise SystemExit(f"{t}: no {t}.zip or {t}_*.csv in {src_dir}")
            d = {"csv": _decode(open(hits[-1], "rb").read())}
            notes = glob.glob(os.path.join(os.path.dirname(hits[-1]), f"{t}__Footnotes.html"))
            if notes:
                d["notes"] = _decode(open(notes[0], "rb").read())
            tabs[t] = d
        else:
            import urllib.request
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (data refresh script)"})
            with urllib.request.urlopen(req, timeout=90) as r:
                tabs[t] = _from_zip(r.read(), t)
            print(f"downloaded {u}")
    return tabs


def parse(text):
    rows = list(csv.reader(io.StringIO(text)))
    hdr = [h.strip() for h in rows[0]]
    recs = []
    for row in rows[1:]:
        if len(row) != len(hdr):
            continue  # trailing notes
        recs.append({h: c.strip().strip('"').strip() for h, c in zip(hdr, row)})
    years = [h for h in hdr if h.isdigit()]
    m = re.search(r"Last updated: ([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    return recs, years, (m.group(1) if m else None)


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f > 0 else None


def clean_name(n):
    n = re.sub(r"\s*\*$", "", n.strip())
    return n.replace(" (Metropolitan Statistical Area)", "")


def build_rpp(tabs):
    mrecs, years, updated = parse(tabs["MARPP"]["csv"])
    precs, _, p_updated = parse(tabs["PARPP"]["csv"])
    indy_rows = [r for r in mrecs if r["GeoFIPS"] == INDY and r["LineCode"] == "1"]
    if not indy_rows:
        raise SystemExit("Indianapolis (26900) missing from MARPP")
    year = max(y for y in years if num(indy_rows[0].get(y)))
    areas = {}

    def add(recs, keep):
        for r in recs:
            f = r["GeoFIPS"]
            if not keep(f) or not r["LineCode"].isdigit() or not 1 <= int(r["LineCode"]) <= 5:
                continue
            a = areas.setdefault(f, {"name": clean_name(r["GeoName"]), "vals": [None] * 5})
            a["vals"][int(r["LineCode"]) - 1] = num(r.get(year))

    add(mrecs, lambda f: True)                                      # all MSAs + U.S. + U.S. nonmetro
    add(precs, lambda f: f.endswith("999") and f != "00999")        # state nonmetro portions
    rows = []
    for f, a in areas.items():
        if any(v is None for v in a["vals"]):
            continue
        kind = "u" if f in ("00000", "00999") else ("n" if f.endswith("999") else "m")
        name = "United States (average)" if f == "00000" else a["name"]
        rows.append([f, name, kind, [round(v, 3) for v in a["vals"]]])
    rows.sort(key=lambda r: ({"u": 0}.get(r[2], 1), r[1].lower()))
    deline = None
    m = re.search(r"bulletin no\. ([\d-]+) issued ([A-Z][a-z]+ \d{1,2}, \d{4})", tabs["MARPP"].get("notes", ""), re.I)
    if m:
        deline = f"OMB Bulletin {m.group(1)} ({m.group(2)})"
    return {"source": "U.S. Bureau of Economic Analysis, Regional Price Parities", "source_url": BEA_PAGE,
            "tables": {t: TABLE_NAMES[t] + " (" + ZIPS[t] + ")" for t in ZIPS}, "year": int(year),
            "updated": updated or p_updated, "delineation": deline,
            "lines": ["All items", "Goods", "Services: Housing", "Services: Utilities", "Services: Other"],
            "indy": INDY, "areas": rows}


def write_rpp(d):
    os.makedirs(DATA_DIR, exist_ok=True)
    head = {k: v for k, v in d.items() if k != "areas"}
    body = json.dumps(head, ensure_ascii=False, indent=1)[:-2]
    body += ',\n "areas": [\n' + ",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in d["areas"]) + "\n ]\n}\n"
    p = os.path.join(DATA_DIR, f"rpp-{d['year']}.json")
    open(p, "w", encoding="utf-8").write(body)
    print(f"wrote {os.path.relpath(p, ROOT)}: {len(d['areas'])} areas, {d['year']} data (BEA updated {d['updated']})")


def load_rpp():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "rpp-*.json")))
    if not files:
        raise SystemExit("no assets/data/rpp-*.json yet: run with --download or --from-dir DIR")
    return json.load(open(files[-1], encoding="utf-8")), "/" + os.path.relpath(files[-1], ROOT)


# ───────────────────────── repo data (Central Indiana) ─────────────────────────

def ast_assign(path, names):
    tree = ast.parse(open(os.path.join(ROOT, path), encoding="utf-8").read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names:
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def load_cities():
    spec = importlib.util.spec_from_file_location("city_guides_data", os.path.join(ROOT, "city_guides_data.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CITIES


def central_indiana():
    mk = ast_assign("build_market_social.py", {"DATA", "MONTH"})
    tax = ast_assign("inject_tax_2027.py", {"COUNTIES"})["COUNTIES"]
    taxd = {}
    for name, rate, lit, _bill in tax:
        taxd[name.lower() + "-county"] = {"rate": float(rate.strip("$")), "inc": float(lit.strip("%*")), "star": lit.endswith("*")}
    counties = {}
    for slug, row in mk["DATA"].items():
        if slug == "central-indiana":
            continue
        _label, med, yoy, sales, _syoy, dom, _dprior, _sup = row
        c = {"name": slug.replace("-county", "").replace("-", " ").title(), "median": med, "yoy": yoy, "dom": dom,
             "url": f"/counties/{slug}-indiana-real-estate/"}
        if not os.path.exists(os.path.join(ROOT, c["url"].lstrip("/"), "index.html")):
            c["url"] = None
        c.update(taxd.get(slug, {}))
        counties[slug] = c
    towns = [{"k": "indianapolis", "name": "Indianapolis", "county": "marion-county", "note": "",
              "price": "$150s to $500s+", "url": "/indianapolis-real-estate/"}]
    for k, c in load_cities().items():
        m = re.match(r"/cities/([a-z-]+-county)/", c.get("url", ""))
        if not m or m.group(1) not in counties:
            continue
        p = re.sub(r"\bthe ", "", c.get("price", "")).strip()
        cname = counties[m.group(1)]["name"]
        note = "" if c.get("county", "") == f"{cname} County" else f"Spans more than one county; figures are {cname} County\u2019s"
        towns.append({"k": k, "name": c["name"], "county": m.group(1), "note": note,
                      "price": p[:1].upper() + p[1:] if p else "", "url": c["url"]})
    region = mk["DATA"].get("central-indiana")
    return counties, towns, mk["MONTH"], region


# ───────────────────────── formatting helpers ─────────────────────────

def money(n):
    return "${:,.0f}".format(n)


def round100(x):
    return int(math.floor(x / 100.0 + 0.5) * 100)


def diff_text(dest, origin, place):
    d = (dest / origin - 1) * 100
    if abs(d) < 0.05:
        return f"about the same in {place}"
    return f"{abs(d):.1f}% {'lower' if d < 0 else 'higher'} in {place}"


def rel(v, base=100.0, same="about the same as"):
    """95.696 vs 100 -> '4.3% below'. BEA puts every category on the all-items scale (U.S. all items = 100),
    so a category is compared with the U.S. figure for that same category (e.g. U.S. rents = 100.629)."""
    d = (v / base - 1) * 100
    if abs(d) < 0.05:
        return same
    return f"{abs(d):.1f}% {'below' if d < 0 else 'above'}"


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def short(name):
    return name.split(",")[0]


# ───────────────────────── page ─────────────────────────

def shell():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    hdr = re.search(r'<header class="site-header">.*?</header>', src, re.S).group()
    ftr = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group()
    fonts = re.search(r' (?:<link rel="preconnect" href="https://fonts\.googleapis\.com">|<link rel="preload" href="/assets/fonts/).*?<link rel="stylesheet" href="/assets/css/style\.css\?v=[0-9a-f]+">', src, re.S).group()
    tail = src[src.index("</footer>") + len("</footer>"):src.index("</body>")]
    if "lead-form.js" not in tail:  # the homepage has no form; this page does
        import hashlib
        v = hashlib.md5(open(os.path.join(ROOT, "assets/js/lead-form.js"), "rb").read()).hexdigest()[:8]
        tail = tail.replace('<script src="/assets/js/site-enhancements.js', f'<script src="/assets/js/lead-form.js?v={v}" defer></script>\n<script src="/assets/js/site-enhancements.js', 1)
    return hdr, ftr, fonts, tail


def render_card():
    out = os.path.join(ROOT, OG_IMG.lstrip("/"))
    if os.path.exists(out):
        return
    tpl = re.search(r'TPL = """(.*?)"""', open(os.path.join(ROOT, "finalize_new_posts.py"), encoding="utf-8").read(), re.S).group(1)
    logo = base64.b64encode(open(os.path.join(ROOT, "assets/img/yrl-logo.png"), "rb").read()).decode()
    tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"), "yrl-col-card.html")
    open(tmp, "w", encoding="utf-8").write(tpl.format(logo=logo, eyebrow="RELOCATION TOOL", title="Indianapolis Cost of Living Calculator",
                                                      sub="What your salary is worth in Indianapolis, for every U.S. metro.", fs=60))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630", "--virtual-time-budget=3000",
                    "--screenshot=" + out, "file://" + tmp], capture_output=True)
    subprocess.run(["pngquant", "--quality=70-95", "--force", "--ext", ".png", out], capture_output=True)
    print("share card", "rendered" if os.path.exists(out) else "FAILED (falls back to og-default.png)")


CSS = """
.col-wrap { max-width: 900px; margin: 0 auto; padding: 40px 0 10px; }
.col-calc { background: #fff; border: 1px solid var(--border); border-radius: 16px; padding: 24px 26px; box-shadow: 0 6px 22px rgba(0,0,0,.07); margin: 1.6rem 0 2rem; scroll-margin-top: 90px; }
.col-calc h2 { margin-top: 0; }
.col-dir { display: inline-flex; background: var(--light); border: 1px solid var(--border); border-radius: 999px; padding: 4px; margin: 0 0 16px; flex-wrap: wrap; }
.col-dir label { position: relative; cursor: pointer; }
.col-dir input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.col-dir span { display: block; padding: 8px 16px; border-radius: 999px; font-size: .88rem; font-weight: 600; color: var(--dark); }
.col-dir input:checked + span { background: var(--red); color: #fff; }
.col-dir input:focus-visible + span { outline: 2px solid var(--dark); outline-offset: 2px; }
.col-fields { display: grid; grid-template-columns: 1.6fr 1fr; gap: 14px; }
.col-field label { display: block; font-size: .8rem; font-weight: 700; color: var(--dark); margin-bottom: 5px; }
.col-field input { width: 100%; border: 1px solid #c9d6e4; border-radius: 9px; padding: 11px 12px; font-size: 1rem; font-family: inherit; color: var(--dark); background: #fff; box-sizing: border-box; }
.col-field input:focus { outline: none; border-color: var(--red); box-shadow: 0 0 0 3px rgba(192,57,38,.15); }
.col-combo { position: relative; }
.col-list { position: absolute; left: 0; right: 0; top: 100%; z-index: 30; margin: 4px 0 0; padding: 4px 0; list-style: none; background: #fff; border: 1px solid #c9d6e4; border-radius: 10px; box-shadow: 0 10px 28px rgba(0,0,0,.14); max-height: 300px; overflow-y: auto; }
.col-list li { padding: 9px 12px; font-size: .92rem; cursor: pointer; color: var(--dark); line-height: 1.35; margin: 0; }
.col-list li[aria-selected="true"], .col-list li:hover { background: var(--red-light); }
.col-list .col-tag { display: block; font-size: .72rem; color: var(--gray); }
.col-list .col-empty { cursor: default; color: var(--gray); }
.col-list .col-empty:hover { background: none; }
.col-money { position: relative; }
.col-money span { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--gray); font-weight: 600; }
.col-money input { padding-left: 26px; }
.col-out { background: linear-gradient(135deg,#13294a,#0d1e38); color: #fff; border-radius: 12px; padding: 20px 22px; margin-top: 16px; text-align: center; }
.col-from { font-size: .92rem; color: #c9d4e0; }
.col-num { font-family: var(--font-serif); font-size: clamp(2rem, 7vw, 2.7rem); font-weight: 800; display: block; line-height: 1.1; margin: 4px 0; }
.col-to { font-size: .95rem; color: #fff; font-weight: 600; }
.col-sum { font-size: .88rem; color: #c9d4e0; margin-top: 10px; }
.col-rev { font-size: .9rem; color: var(--dark); background: var(--light); border-radius: 10px; padding: 10px 14px; margin-top: 12px; }
.col-break { width: 100%; border-collapse: collapse; margin: 16px 0 6px; font-size: .9rem; }
.col-break th { text-align: left; font-size: .72rem; letter-spacing: .05em; text-transform: uppercase; color: var(--gray); font-weight: 700; padding: 8px 6px; border-bottom: 2px solid var(--border); }
.col-break td { padding: 10px 6px; border-bottom: 1px solid #eaeef3; vertical-align: middle; }
.col-break td.n { font-variant-numeric: tabular-nums; white-space: nowrap; }
.col-break .lo { color: var(--green); font-weight: 700; }
.col-break .hi { color: var(--red); font-weight: 700; }
.col-bar { position: relative; height: 8px; background: #eef2f7; border-radius: 4px; margin-top: 5px; min-width: 70px; }
.col-bar::after { content: ""; position: absolute; left: 50%; top: -2px; bottom: -2px; width: 1px; background: #9aa9bb; }
.col-bar i { position: absolute; top: 0; bottom: 0; border-radius: 4px; }
.col-note { font-size: .8rem; color: var(--gray); margin: 10px 0 0; }
.col-pick { border: 1px solid var(--red); color: var(--red); background: #fff; border-radius: 999px; padding: 5px 12px; font-size: .8rem; font-weight: 700; cursor: pointer; font-family: inherit; }
.col-pick:hover { background: var(--red); color: #fff; }
.col-guide { display: block; font-size: .78rem; font-weight: 600; margin-top: 2px; }
.col-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 18px 0 8px; position: relative; }
.col-table-wrap .data-table, .col-cmp thead th { position: relative; }
.col-table-wrap .data-table { margin: 0; }
.data-table.col-sortable th button { all: unset; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; }
.data-table.col-sortable th button::after { content: "\\2195"; opacity: .5; font-size: .85em; }
.data-table.col-sortable th[aria-sort="ascending"] button::after { content: "\\2191"; opacity: 1; }
.data-table.col-sortable th[aria-sort="descending"] button::after { content: "\\2193"; opacity: 1; }
.data-table.col-sortable th button:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }
.data-table td.n { font-variant-numeric: tabular-nums; }
.col-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 0; }
.col-chips button { border: 1px solid var(--border); background: #fff; color: var(--dark); border-radius: 999px; padding: 7px 14px; font-size: .85rem; font-weight: 600; cursor: pointer; font-family: inherit; }
.col-chips button[aria-pressed="true"] { background: var(--dark); border-color: var(--dark); color: #fff; }
.col-towns { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0 0; }
.col-towns label { display: block; font-size: .8rem; font-weight: 700; color: var(--dark); margin-bottom: 5px; }
.col-towns select { width: 100%; border: 1px solid #c9d6e4; border-radius: 9px; padding: 10px; font-size: .95rem; font-family: inherit; color: var(--dark); background: #fff; }
.col-cmp { width: 100%; border-collapse: collapse; margin: 14px 0 6px; font-size: .9rem; table-layout: fixed; }
.col-cmp th, .col-cmp td { padding: 10px 8px; border-bottom: 1px solid #eaeef3; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
.col-cmp thead th { font-size: 1rem; color: var(--dark); border-bottom: 2px solid var(--border); }
.col-cmp tbody th { font-size: .74rem; letter-spacing: .04em; text-transform: uppercase; color: var(--gray); font-weight: 700; width: 34%; }
.col-cmp td { font-weight: 600; color: var(--dark); font-variant-numeric: tabular-nums; }
.col-cmp td small { display: block; font-weight: 400; color: var(--gray); font-size: .78rem; margin-top: 2px; }
.col-src { font-size: .82rem; color: var(--gray); }
.col-sr { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
.col-related { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin: 12px 0 30px; }
@media (max-width: 640px) {
 .col-calc { padding: 18px 14px; }
 .col-fields { grid-template-columns: 1fr; }
 .col-dir { display: flex; }
 .col-dir label { flex: 1; text-align: center; }
 .col-dir span { padding: 8px 10px; font-size: .82rem; }
 .col-break { font-size: .82rem; }
 .col-break th, .col-break td { padding: 8px 3px; }
 .col-towns { grid-template-columns: 1fr; }
 .col-cmp { font-size: .84rem; }
 .col-cmp th, .col-cmp td { padding: 8px 5px; }
}
"""

JS = r"""
(function(){
 var D = JSON.parse(document.getElementById('col-data').textContent);
 var $ = function(id){ return document.getElementById(id); };
 var ST = {AL:'Alabama',AK:'Alaska',AZ:'Arizona',AR:'Arkansas',CA:'California',CO:'Colorado',CT:'Connecticut',DE:'Delaware',DC:'District of Columbia',FL:'Florida',GA:'Georgia',HI:'Hawaii',ID:'Idaho',IL:'Illinois',IN:'Indiana',IA:'Iowa',KS:'Kansas',KY:'Kentucky',LA:'Louisiana',ME:'Maine',MD:'Maryland',MA:'Massachusetts',MI:'Michigan',MN:'Minnesota',MS:'Mississippi',MO:'Missouri',MT:'Montana',NE:'Nebraska',NV:'Nevada',NH:'New Hampshire',NJ:'New Jersey',NM:'New Mexico',NY:'New York',NC:'North Carolina',ND:'North Dakota',OH:'Ohio',OK:'Oklahoma',OR:'Oregon',PA:'Pennsylvania',RI:'Rhode Island',SC:'South Carolina',SD:'South Dakota',TN:'Tennessee',TX:'Texas',UT:'Utah',VT:'Vermont',VA:'Virginia',WA:'Washington',WV:'West Virginia',WI:'Wisconsin',WY:'Wyoming'};
 var ABBR = {}; Object.keys(ST).forEach(function(k){ ABBR[ST[k]] = k; });
 function norm(s){ s = String(s).toLowerCase(); if (s.normalize) s = s.normalize('NFD').replace(/[\u0300-\u036f]/g, ''); return s.replace(/[^a-z0-9]+/g, ' ').trim(); }
 var KIND = {n: 'Rural and small-town areas outside metros', u: 'National benchmark', m: ''};
 var indy = null, items = [];
 D.areas.forEach(function(a){
  var it = {fips: a[0], name: a[1], kind: a[2], v: a[3]};
  if (it.fips === D.indy) { indy = it; return; }
  var extra = '';
  var m = it.name.match(/, ([A-Z]{2}(?:-[A-Z]{2})*)$/);
  if (m) m[1].split('-').forEach(function(s){ if (ST[s]) extra += ' ' + ST[s]; });
  var st = it.name.match(/^(.+) \(Nonmetropolitan Portion\)$/);
  if (st && ABBR[st[1]]) extra += ' ' + ABBR[st[1]];
  if (it.kind === 'n') extra += ' rural nonmetro nonmetropolitan small town';
  if (it.kind === 'u') extra += ' national average usa america';
  extra += ' ' + (D.alias[it.fips] || '');
  it.words = norm(it.name + extra).split(' ');
  it.key = norm(it.name);
  items.push(it);
 });
 var byFips = {}; items.forEach(function(it){ byFips[it.fips] = it; });
 function shortName(it){
  if (it === indy) return 'Indianapolis';
  if (it.fips === '00000') return 'the U.S. average';
  if (it.fips === '00999') return 'U.S. nonmetro areas';
  var st = it.name.match(/^(.+) \(Nonmetropolitan Portion\)$/);
  if (st) return 'nonmetro ' + st[1];
  return it.name.split(',')[0];
 }
 function fullName(it){ return it === indy ? 'Indianapolis' : it.name; }
 function fmt(n){ return '$' + Math.round(n).toLocaleString('en-US'); }
 function r100(n){ return Math.round(n / 100) * 100; }

 /* ── combobox ── */
 var input = $('col-area'), list = $('col-area-list'), sel = null, shown = [], active = -1;
 function filter(q){
  var t = norm(q).split(' ').filter(Boolean);
  if (!t.length) return items.slice();
  var qn = t.join(' ');
  var out = items.filter(function(it){ return t.every(function(tok){ return it.words.some(function(w){ return w.indexOf(tok) === 0; }); }); });
  out.sort(function(a, b){ var sa = a.key.indexOf(qn) === 0 ? 0 : 1, sb = b.key.indexOf(qn) === 0 ? 0 : 1; return sa - sb || (a.key < b.key ? -1 : 1); });
  return out;
 }
 function renderList(q){
  shown = filter(q).slice(0, 80); active = shown.length ? 0 : -1;
  list.innerHTML = '';
  if (!shown.length) {
   var e = document.createElement('li'); e.className = 'col-empty'; e.textContent = 'No match. Try a city name or a state.'; list.appendChild(e);
  }
  shown.forEach(function(it, i){
   var li = document.createElement('li');
   li.id = 'col-opt-' + i; li.setAttribute('role', 'option'); li.setAttribute('aria-selected', i === active ? 'true' : 'false');
   li.textContent = it.name;
   if (KIND[it.kind]) { var s = document.createElement('span'); s.className = 'col-tag'; s.textContent = KIND[it.kind]; li.appendChild(s); }
   li.addEventListener('mousedown', function(ev){ ev.preventDefault(); choose(it); });
   list.appendChild(li);
  });
  open(true); mark();
 }
 function mark(){
  for (var i = 0; i < list.children.length; i++) list.children[i].setAttribute('aria-selected', i === active ? 'true' : 'false');
  if (active >= 0) { input.setAttribute('aria-activedescendant', 'col-opt-' + active); var el = $('col-opt-' + active); if (el && el.scrollIntoView) el.scrollIntoView({block: 'nearest'}); }
  else input.removeAttribute('aria-activedescendant');
 }
 function open(on){ list.hidden = !on; input.setAttribute('aria-expanded', on ? 'true' : 'false'); }
 function choose(it){ sel = it; input.value = it.name; open(false); calc(); }
 input.addEventListener('input', function(){ renderList(input.value); });
 input.addEventListener('focus', function(){ input.select(); renderList(sel && input.value === sel.name ? '' : input.value); });
 input.addEventListener('click', function(){ var full = sel && input.value === sel.name; if (full) input.select(); if (list.hidden) renderList(full ? '' : input.value); });
 input.addEventListener('keydown', function(e){
  if (e.key === 'ArrowDown') { e.preventDefault(); if (list.hidden) renderList(''); else if (active < shown.length - 1) { active++; mark(); } }
  else if (e.key === 'ArrowUp') { e.preventDefault(); if (active > 0) { active--; mark(); } }
  else if (e.key === 'Enter') { if (!list.hidden && active >= 0) { e.preventDefault(); choose(shown[active]); } }
  else if (e.key === 'Escape') { open(false); if (sel) input.value = sel.name; }
 });
 input.addEventListener('blur', function(){ setTimeout(function(){ open(false); if (sel && input.value !== sel.name) input.value = sel.name; }, 120); });

 /* ── calculator ── */
 var salary = $('col-salary');
 function money(){ var n = parseFloat(String(salary.value).replace(/[^0-9.]/g, '')); return isFinite(n) ? n : NaN; }
 salary.addEventListener('input', calc);
 salary.addEventListener('blur', function(){ var n = money(); if (n > 0) salary.value = Math.round(n).toLocaleString('en-US'); });
 var dirs = document.getElementsByName('col-dir');
 for (var i = 0; i < dirs.length; i++) dirs[i].addEventListener('change', calc);
 var LABELS = [[0, 'All items'], [2, 'Housing (rents)'], [1, 'Goods'], [3, 'Utilities'], [4, 'Other services']];
 function pct(dest, origin){ return (dest / origin - 1) * 100; }
 function pctText(d){ return Math.abs(d) < 0.05 ? 'About the same' : Math.abs(d).toFixed(1) + '% ' + (d < 0 ? 'lower' : 'higher'); }
 function calc(){
  if (!sel) return;
  var to = !dirs[1].checked;
  $('col-area-label').textContent = to ? 'Where you live now' : 'Where you are moving';
  var origin = to ? sel : indy, dest = to ? indy : sel;
  var s = money();
  var ok = s > 0;
  var eq = ok ? s * dest.v[0] / origin.v[0] : 0;
  $('col-from').textContent = ok ? fmt(s) + ' in ' + fullName(origin) + ' is about the same as' : 'Enter a salary to see the result';
  $('col-num').textContent = ok ? fmt(r100(eq)) : '$\u2014';
  $('col-to').textContent = 'in ' + fullName(dest);
  var d = pct(dest.v[0], origin.v[0]);
  var gap = r100(Math.abs(eq - s));
  $('col-sum').textContent = Math.abs(d) < 0.05 ? 'Overall prices are about the same in both places.' :
   'Overall prices are ' + pctText(d).toLowerCase() + ' in ' + shortName(dest) + ' (' + D.year + ')' + (ok && gap ? ', so you would need about ' + fmt(gap) + ' ' + (d < 0 ? 'less' : 'more') + ' a year for the same standard of living.' : '.');
  var back = ok ? s * origin.v[0] / dest.v[0] : 0;
  $('col-rev').textContent = ok ? 'Going the other way: ' + fmt(s) + ' in ' + shortName(dest) + ' is about the same as ' + fmt(r100(back)) + ' in ' + shortName(origin) + '.' : '';
  $('col-rev').hidden = !ok;
  $('col-h-a').textContent = 'Indianapolis';
  $('col-h-b').textContent = to ? 'Your area' : 'New area';
  $('col-h-d').textContent = to ? 'In Indianapolis' : 'In the new area';
  var tb = $('col-break-body'); tb.innerHTML = '';
  LABELS.forEach(function(L){
   var k = L[0], dd = pct(dest.v[k], origin.v[k]);
   var tr = document.createElement('tr');
   var c0 = document.createElement('td'); c0.textContent = L[1];
   var c1 = document.createElement('td'); c1.className = 'n'; c1.textContent = indy.v[k].toFixed(1);
   var c2 = document.createElement('td'); c2.className = 'n'; c2.textContent = sel.v[k].toFixed(1);
   var c3 = document.createElement('td');
   var sp = document.createElement('span'); sp.className = Math.abs(dd) < 0.05 ? '' : (dd < 0 ? 'lo' : 'hi'); sp.textContent = pctText(dd);
   var bar = document.createElement('div'); bar.className = 'col-bar'; bar.setAttribute('aria-hidden', 'true');
   var b = document.createElement('i'); var w = Math.min(Math.abs(dd), 60) / 60 * 50;
   b.style.width = w + '%'; b.style.background = dd < 0 ? '#2e7d32' : '#c03926';
   if (dd < 0) b.style.right = '50%'; else b.style.left = '50%';
   bar.appendChild(b); c3.appendChild(sp); c3.appendChild(bar);
   tr.appendChild(c0); tr.appendChild(c1); tr.appendChild(c2); tr.appendChild(c3); tb.appendChild(tr);
  });
 }
 var q = (location.search.match(/[?&]from=(\d{5})/) || [])[1];
 choose(byFips[q] || byFips[D.dflt]);
 if (/[?&]dir=from/.test(location.search)) { dirs[1].checked = true; calc(); }
 var picks = document.querySelectorAll('.col-pick');
 for (var j = 0; j < picks.length; j++) {
  picks[j].hidden = false;
  picks[j].addEventListener('click', function(){
   var it = byFips[this.getAttribute('data-fips')]; if (!it) return;
   dirs[0].checked = true; salary.value = '100,000'; choose(it);
   $('calculator').scrollIntoView({behavior: 'smooth', block: 'start'});
  });
 }

 /* ── town compare ── */
 var C = D.counties, T = D.towns, tA = $('col-town-a'), tB = $('col-town-b');
 var groups = {};
 T.forEach(function(t, i){ (groups[t.county] = groups[t.county] || []).push(i); });
 var order = Object.keys(groups).sort(function(a, b){ return a === 'marion-county' ? -1 : b === 'marion-county' ? 1 : (a < b ? -1 : 1); });
 [tA, tB].forEach(function(s){
  order.forEach(function(g){
   var og = document.createElement('optgroup'); og.label = C[g].name + ' County';
   groups[g].slice().sort(function(a, b){ return a === 0 ? -1 : b === 0 ? 1 : (T[a].name < T[b].name ? -1 : 1); }).forEach(function(i){
    var o = document.createElement('option'); o.value = T[i].k; o.textContent = T[i].name; og.appendChild(o);
   });
   s.appendChild(og);
  });
 });
 tA.value = 'indianapolis'; tB.value = 'carmel';
 function town(k){ for (var i = 0; i < T.length; i++) if (T[i].k === k) return T[i]; return T[0]; }
 function cell(tr, txt, sub){ var td = document.createElement('td'); td.textContent = txt; if (sub) { var sm = document.createElement('small'); sm.textContent = sub; td.appendChild(sm); } tr.appendChild(td); }
 function towns(){
  var a = town(tA.value), b = town(tB.value), ca = C[a.county], cb = C[b.county];
  $('col-cmp-a').textContent = a.name; $('col-cmp-b').textContent = b.name;
  var rows = [
   ['County', function(t, c){ return [c.name + ' County', t.note]; }],
   ['Typical home prices', function(t){ return [t.price || '\u2014', 'General range from our town guide']; }],
   ['County median sale price', function(t, c){ return [fmt(c.median), D.month + ', MIBOR']; }],
   ['Change vs. a year earlier', function(t, c){ return [Math.abs(c.yoy) < 0.05 ? 'Flat' : (c.yoy > 0 ? 'Up ' : 'Down ') + Math.abs(c.yoy).toFixed(1) + '%', '']; }],
   ['Median days on market', function(t, c){ return [String(c.dom), D.month]; }],
   ['County local income tax', function(t, c){ return [c.inc != null ? c.inc.toFixed(2) + '%' : '\u2014', c.inc != null ? '2026, plus 2.95% state' : 'Not in our data']; }],
   ['Property tax rate', function(t, c){ return [c.rate != null ? '$' + c.rate.toFixed(2) + ' per $100' : '\u2014', c.rate != null ? '2026 district median, before deductions and the 1% cap' : 'Not in our data']; }]
  ];
  var tb = $('col-cmp-body'); tb.innerHTML = '';
  rows.forEach(function(r){
   var tr = document.createElement('tr'); var th = document.createElement('th'); th.scope = 'row'; th.textContent = r[0]; tr.appendChild(th);
   var x = r[1](a, ca), y = r[1](b, cb); cell(tr, x[0], x[1]); cell(tr, y[0], y[1]); tb.appendChild(tr);
  });
  var tr = document.createElement('tr'); var th = document.createElement('th'); th.scope = 'row'; th.textContent = 'Learn more'; tr.appendChild(th);
  [a, b].forEach(function(t){ var td = document.createElement('td'); var l = document.createElement('a'); l.href = t.url; l.textContent = t.name + ' guide \u203A'; td.appendChild(l); tr.appendChild(td); });
  tb.appendChild(tr);
 }
 tA.addEventListener('change', towns); tB.addEventListener('change', towns); towns();

 /* ── county table: sort + filter ── */
 var tbl = $('col-counties'), body = tbl.tBodies[0];
 var ths = tbl.tHead.rows[0].cells;
 for (var h = 0; h < ths.length; h++) (function(th, idx){
  var btn = th.querySelector('button'); if (!btn) return;
  btn.addEventListener('click', function(){
   var dir = th.getAttribute('aria-sort') === 'descending' ? 'ascending' : (th.getAttribute('aria-sort') === 'ascending' ? 'descending' : (idx === 0 ? 'ascending' : 'descending'));
   for (var z = 0; z < ths.length; z++) ths[z].removeAttribute('aria-sort');
   th.setAttribute('aria-sort', dir);
   var rs = Array.prototype.slice.call(body.rows);
   rs.sort(function(r1, r2){
    var v1 = r1.cells[idx].getAttribute('data-v'), v2 = r2.cells[idx].getAttribute('data-v');
    if (idx > 0) { v1 = v1 === '' ? null : +v1; v2 = v2 === '' ? null : +v2; if (v1 === null) return 1; if (v2 === null) return -1; }
    var c = v1 < v2 ? -1 : v1 > v2 ? 1 : 0; return dir === 'ascending' ? c : -c;
   });
   rs.forEach(function(r){ body.appendChild(r); });
  });
 })(ths[h], h);
 var chips = document.querySelectorAll('#col-chips button');
 function show(all){
  for (var r = 0; r < body.rows.length; r++) body.rows[r].hidden = !all && body.rows[r].getAttribute('data-core') !== '1';
  for (var c = 0; c < chips.length; c++) chips[c].setAttribute('aria-pressed', (chips[c].getAttribute('data-all') === '1') === all ? 'true' : 'false');
 }
 for (var c = 0; c < chips.length; c++) chips[c].addEventListener('click', function(){ show(this.getAttribute('data-all') === '1'); });
 $('col-chips').hidden = false;
 show(false);
})();
"""


def build(rpp, rpp_path):
    hdr, ftr, fonts, tail = shell()
    counties, towns, month, region = central_indiana()
    A = {r[0]: r for r in rpp["areas"]}
    I = A[INDY][3]
    U = A["00000"][3]  # U.S. average by category (all items = 100)
    year, upd = rpp["year"], rpp["updated"]
    indy_name = A[INDY][1]

    def eq100(f):
        return round100(100000 * I[0] / A[f][3][0])

    sf, chi, ny, la = "41860", "16980", "35620", "31080"
    for f in (sf, chi, ny, la):
        assert f in A, f

    # Quick answer + facts
    qa_lead = (f"<strong>How far does a salary go in Indianapolis?</strong> Prices in the Indianapolis metro run "
               f"{rel(I[0])} the national average, and housing (rents) runs {rel(I[2], U[2])} "
               f"(BEA, {year}). So $100,000 in the San Francisco metro buys about what {money(eq100(sf))} does here, and $100,000 in "
               f"Chicago about what {money(eq100(chi))} does. Pick your own metro and salary below.")
    facts = [("Overall prices", f"{I[0]:.1f} (U.S. = 100)"), ("Housing (rents)", f"{I[2]:.1f}, {rel(I[2], U[2])} U.S."),
             ("Goods", f"{I[1]:.1f}"), ("Utilities", f"{I[3]:.1f}"), ("Other services", f"{I[4]:.1f}"),
             ("Data", f"BEA Regional Price Parities, {year}")]
    qa_facts = "\n".join(f" <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)

    # Popular comparisons table (static, crawlable)
    pop = []
    for f, guide in POPULAR:
        if f not in A:
            continue
        pop.append((A[f], guide))
    pop.sort(key=lambda x: -x[0][3][0])
    pop_rows = []
    for a, guide in pop:
        f, name, _k, v = a
        g = f'<a class="col-guide" href="{guide[0]}">Moving from {guide[1]} guide &rsaquo;</a>' if guide else ""
        d0, d2 = (I[0] / v[0] - 1) * 100, (I[2] / v[2] - 1) * 100
        pop_rows.append(
            f' <tr><td>{html.escape(name)}{g}</td><td class="n">{v[0]:.1f}</td><td class="n"><strong>{money(eq100(f))}</strong></td>'
            f'<td class="n">{abs(d0):.1f}% {"lower" if d0 < 0 else "higher"}</td><td class="n">{abs(d2):.1f}% {"lower" if d2 < 0 else "higher"}</td>'
            f'<td><button type="button" class="col-pick" data-fips="{f}" hidden>Compare</button></td></tr>')
    pop_rows = "\n".join(pop_rows)

    # County table
    core = [s for s, c in counties.items() if "inc" in c]
    order = sorted(counties, key=lambda s: (s not in core, s != "marion-county", counties[s]["name"]))
    crow = []
    for s in order:
        c = counties[s]
        nm = f'<a href="{c["url"]}">{c["name"]}</a>' if c["url"] else c["name"]
        if s == "marion-county":
            nm += " (Indianapolis)"
        yoy = "Flat" if abs(c["yoy"]) < 0.05 else f'{"+" if c["yoy"] > 0 else "&minus;"}{abs(c["yoy"]):.1f}%'
        inc = f'{c["inc"]:.2f}%{"*" if c.get("star") else ""}' if "inc" in c else "&mdash;"
        rate = f'${c["rate"]:.2f}' if "rate" in c else "&mdash;"
        crow.append(f' <tr data-core="{1 if s in core else 0}"><td data-v="{html.escape(c["name"].lower())}">{nm}</td>'
                    f'<td class="n" data-v="{c["median"]}">{money(c["median"])}</td><td class="n" data-v="{c["yoy"]}">{yoy}</td>'
                    f'<td class="n" data-v="{c.get("inc", "")}">{inc}</td><td class="n" data-v="{c.get("rate", "")}">{rate}</td></tr>')
    crow = "\n".join(crow)
    mar, ham = counties["marion-county"], counties["hamilton-county"]
    reg_line = ""
    if region:
        ry = region[2]
        reg_line = (f" Across all 17 counties in MIBOR&rsquo;s region, the median was <strong>{money(region[1])}</strong> in {month}, "
                    f"{'flat' if abs(ry) < 0.05 else ('up' if ry > 0 else 'down') + f' {abs(ry):.1f}%'} from a year earlier.")

    # FAQs (plain text; same text in schema)
    def eqp(f):
        return money(eq100(f))
    chi_v = A[chi][3]
    ut = (I[3] / chi_v[3] - 1) * 100
    faqs = [
        ("How does the cost of living in Indianapolis compare with the national average?",
         f"The Bureau of Economic Analysis puts prices in the {indy_name} metro at {I[0]:.1f} for {year}, where the U.S. average is 100, so overall prices run {rel(I[0])} average. "
         f"Compared with the U.S. figure for each category, housing (rents) is {rel(I[2], U[2])}, utilities {rel(I[3], U[3])}, goods {rel(I[1], U[1])} and other services {rel(I[4], U[4])}."),
        ("What salary do I need in Indianapolis to match my current one?",
         f"Multiply your salary by the Indianapolis price level ({I[0]:.1f}) and divide by your current area's. For example, $100,000 in the New York metro ({A[ny][3][0]:.1f}) works out to about "
         f"{eqp(ny)} in Indianapolis, and $100,000 in the Los Angeles metro ({A[la][3][0]:.1f}) to about {eqp(la)}. The calculator on this page does the math for every U.S. metro area and each state's nonmetro areas."),
        ("Is Indianapolis cheaper than Chicago?",
         f"{'Yes' if I[0] < chi_v[0] else 'Not overall'}. In {year}, overall prices were {diff_text(I[0], chi_v[0], 'the Indianapolis metro')} than in the Chicago metro, and housing (rents) was "
         f"{diff_text(I[2], chi_v[2], 'Indianapolis')}, according to BEA. Utilities were about {abs(ut):.1f}% {'lower' if ut < 0 else 'higher'} in Indianapolis. $100,000 in Chicago works out to about {eqp(chi)} in Indianapolis."),
        ("What does this cost of living calculator leave out?",
         "Taxes, your own spending habits and differences within a metro. Regional Price Parities measure what goods and services cost, not income, sales or property taxes, which vary by state and, in Indiana, by county. "
         f"Housing is based on rents rather than home purchase prices, and every figure is a metro-wide average for {year}. Treat the result as a planning estimate, not financial advice."),
        ("Is it cheaper to live in Indianapolis or the suburbs?",
         f"It depends on which costs matter most to you. In {month}, the median sale price was {money(mar['median'])} in Marion County (Indianapolis) and {money(ham['median'])} in Hamilton County, according to MIBOR. "
         f"But Marion County's 2026 local income tax is {mar['inc']:.2f}%, compared with {ham['inc']:.2f}% in Hamilton County. The Central Indiana table on this page compares the surrounding counties side by side."),
        ("How often is this data updated?",
         f"BEA publishes Regional Price Parities once a year. The {year} figures, the latest available, were released on {upd}. The Central Indiana home prices come from MIBOR's monthly reports; this page shows {month}."),
    ]
    faq_html = "\n".join(f' <details class="faq-item">\n <summary>{html.escape(q, quote=False)}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in faqs)

    # Inline data for the JS
    data = {"year": year, "indy": INDY, "dflt": chi, "alias": {k: v for k, v in ALIASES.items() if k in A}, "month": month,
            "areas": rpp["areas"],
            "counties": {s: {k: c.get(k) for k in ("name", "median", "yoy", "dom", "inc", "rate")} for s, c in counties.items()},
            "towns": towns}
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    og = SITE + (OG_IMG if os.path.exists(os.path.join(ROOT, OG_IMG.lstrip("/"))) else "/assets/img/og-default.png")
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": "Indianapolis Cost of Living Calculator", "description": DESC,
         "dateModified": datetime.date.today().isoformat(), "inLanguage": "en-US",
         "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"]},
         "about": {"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}},
         "citation": {"@type": "Dataset", "name": f"Regional Price Parities by MSA and by portion ({year})", "url": BEA_PAGE,
                      "creator": {"@type": "GovernmentOrganization", "name": "U.S. Bureau of Economic Analysis"}}},
        {"@type": "WebApplication", "name": "Indianapolis Cost of Living Calculator", "url": URL + "#calculator",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": f"Compares a salary in any U.S. metro area with the Indianapolis metro using BEA Regional Price Parities ({year}).",
         "provider": {"@type": "Organization", "name": "Your Realty Link", "url": SITE}},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": SITE, "logo": "/assets/img/yrl-logo.png",
         "telephone": "317-997-7404", "email": "indy@yourrealtylink.com",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227", "addressCountry": "US"},
         "areaServed": "Central Indiana"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": "Cost of Living Calculator", "item": URL}]}]}

    T, Dd = html.escape(TITLE, quote=True), html.escape(DESC, quote=True)
    deline = f" Metro areas follow {rpp['delineation']}." if rpp.get("delineation") else ""
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{T}</title>
 <meta name="description" content="{Dd}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{URL}">
 <meta property="og:title" content="{T}">
 <meta property="og:description" content="{Dd}">
 <meta property="og:url" content="{URL}">
 <meta property="og:image" content="{og}">
 <meta property="og:image:width" content="1200">
 <meta property="og:image:height" content="630">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:title" content="{T}">
 <meta name="twitter:description" content="{Dd}">
 <meta name="twitter:image" content="{og}">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
{json.dumps(graph, indent=1, ensure_ascii=False)}
 </script>
{fonts}
 <style>{CSS} </style>
</head>
<body>

{hdr}

<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container">
 <a href="/">Home</a>
 <span>&rsaquo;</span>
 <a href="/guides/">Guides</a>
 <span>&rsaquo;</span>
 Cost of Living Calculator
 </div>
</nav>

<section class="page-hero">
 <div class="container">
 <h1>Indianapolis Cost of Living <em>Calculator</em></h1>
 <p class="hero-sub">See what your salary is worth in Indianapolis, or what an Indianapolis salary is worth where you&rsquo;re headed, using federal price data for every U.S. metro area. Then compare costs town by town across Central Indiana.</p>
 <div class="hero-badges">
 <span class="hero-badge">BEA {year} price data</span>
 <span class="hero-badge">Every U.S. metro</span>
 <span class="hero-badge">Central Indiana counties</span>
 </div><p class="hero-reviewed">&#10004; Reviewed by <a href="/agents/janet-giles/">Janet Giles-Schultz</a>, Principal Broker &middot; MIBOR member &middot; Updated {UPDATED}</p>
 </div>
</section>

<div class="container">
 <div class="col-wrap">

 <!-- QA-START -->
<div class="quick-answer">
 <p class="qa-heading">Quick Answer</p>
 <p class="qa-lead">{qa_lead}</p>
 <dl class="qa-facts">
{qa_facts}
 </dl>
</div>
<!-- QA-END -->

 <p>Thinking about a move, or weighing a job offer in Indianapolis? Pick the metro area you&rsquo;re comparing and enter a salary. The calculator uses the Bureau of Economic Analysis&rsquo;s Regional Price Parities, the federal government&rsquo;s measure of how prices differ from place to place, to show the salary that buys the same standard of living, plus how housing, goods, utilities and services compare. For rent, taxes and utility bills in dollars, see our <a href="/blog/cost-of-living-in-indianapolis/">cost of living in Indianapolis breakdown</a>.</p>

 <section class="col-calc" id="calculator" aria-labelledby="col-calc-h">
 <h2 id="col-calc-h">Salary Comparison Calculator</h2>
 <div class="col-dir" role="radiogroup" aria-label="Direction of your move">
 <label><input type="radio" name="col-dir" value="to" autocomplete="off" checked><span>Moving to Indianapolis</span></label>
 <label><input type="radio" name="col-dir" value="from" autocomplete="off"><span>Moving from Indianapolis</span></label>
 </div>
 <div class="col-fields">
 <div class="col-field col-combo">
 <label for="col-area" id="col-area-label">Where you live now</label>
 <input id="col-area" type="text" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="col-area-list" autocomplete="off" spellcheck="false" placeholder="Type a city or state, e.g. Chicago">
 <ul id="col-area-list" class="col-list" role="listbox" aria-label="Metro areas" hidden></ul>
 </div>
 <div class="col-field">
 <label for="col-salary">Annual salary</label>
 <div class="col-money"><span aria-hidden="true">$</span><input id="col-salary" type="text" inputmode="numeric" autocomplete="off" value="75,000"></div>
 </div>
 </div>
 <div aria-live="polite">
 <div class="col-out">
 <div class="col-from" id="col-from">Loading the calculator&hellip;</div>
 <span class="col-num" id="col-num">$&mdash;</span>
 <div class="col-to" id="col-to"></div>
 <div class="col-sum" id="col-sum"></div>
 </div>
 <div class="col-rev" id="col-rev" hidden></div>
 </div>
 <table class="col-break">
 <caption class="col-src" style="caption-side:bottom;text-align:left;padding-top:8px;">Price levels on BEA&rsquo;s scale, where U.S. prices overall = 100 ({year}). The difference column compares prices where you&rsquo;re moving with prices where you are now.</caption>
 <thead><tr><th scope="col">Category</th><th scope="col" id="col-h-a">Indianapolis</th><th scope="col" id="col-h-b">Your area</th><th scope="col" id="col-h-d">In Indianapolis</th></tr></thead>
 <tbody id="col-break-body"></tbody>
 </table>
 <noscript><div class="col-note"><strong>The calculator needs JavaScript.</strong> The popular comparisons table below shows the results for 24 large metros without it.</div></noscript>
 <div class="col-note">Estimates for planning, not financial advice. Based on {year} metro-wide prices; taxes and your own spending mix aren&rsquo;t included. <a href="#how-it-works">How this works</a>.</div>
 </section>

 <h2 id="popular">What $100,000 Is Worth in Indianapolis</h2>
 <p>Here&rsquo;s the same math for a $100,000 salary in some of the metros people most often move here from, sorted from most to least expensive. Tap <em>Compare</em> to load any of them into the calculator.</p>
 <div class="col-table-wrap">
 <table class="data-table">
 <thead><tr><th scope="col">Metro area</th><th scope="col">Price level</th><th scope="col">$100,000 there = in Indy</th><th scope="col">Overall prices in Indy</th><th scope="col">Housing (rents) in Indy</th><th scope="col"><span class="col-sr">Load into calculator</span></th></tr></thead>
 <tbody>
{pop_rows}
 </tbody>
 </table>
 </div>
 <p class="col-src">Source: U.S. Bureau of Economic Analysis, Regional Price Parities ({year}); U.S. = 100. Indianapolis = the {html.escape(indy_name)} metro ({I[0]:.1f}). Equivalent salaries rounded to the nearest $100.</p>

 <h2 id="central-indiana">Indianapolis vs. the Suburbs: Costs Across Central Indiana</h2>
 <p>BEA prices the whole metro as one number, but what you pay inside Central Indiana changes a lot from county to county. Home prices, local income tax and property tax rates all shift when you cross a county line, and they often pull in opposite directions: Marion County (Indianapolis) had a median sale price of {money(mar['median'])} in {month} against {money(ham['median'])} in Hamilton County, but its 2026 local income tax is {mar['inc']:.2f}% against Hamilton&rsquo;s {ham['inc']:.2f}%.{reg_line}</p>

 <h3>Compare Two Towns</h3>
 <div class="col-towns">
 <div><label for="col-town-a">First town</label><select id="col-town-a"></select></div>
 <div><label for="col-town-b">Second town</label><select id="col-town-b"></select></div>
 </div>
 <table class="col-cmp" aria-live="polite">
 <thead><tr><th scope="col"><span class="col-sr">Measure</span></th><th scope="col" id="col-cmp-a">Indianapolis</th><th scope="col" id="col-cmp-b">Carmel</th></tr></thead>
 <tbody id="col-cmp-body"></tbody>
 </table>
 <noscript><div class="col-note">Turn on JavaScript to compare towns; the county table below has the same figures.</div></noscript>

 <h3>County by County</h3>
 <p>Tap or click a column heading to sort; swipe the table sideways on a phone.</p>
 <div class="col-chips" id="col-chips" hidden>
 <button type="button" data-all="0" aria-pressed="true">Indianapolis + surrounding counties</button>
 <button type="button" data-all="1" aria-pressed="false">All 17 MIBOR counties</button>
 </div>
 <div class="col-table-wrap">
 <table class="data-table col-sortable" id="col-counties">
 <thead><tr><th scope="col"><button type="button">County</button></th><th scope="col"><button type="button">Median sale price ({month.split()[0][:3]} {month.split()[1]})</button></th><th scope="col"><button type="button">vs. a year earlier</button></th><th scope="col"><button type="button">Local income tax (2026)</button></th><th scope="col"><button type="button">Property tax rate per $100 (2026)</button></th></tr></thead>
 <tbody>
{crow}
 </tbody>
 </table>
 </div>
 <p class="col-src">Sources: MIBOR REALTOR&reg; Association, {month}, single-family homes (see our <a href="/market-updates/">latest market update</a>). Local income tax: <a href="https://www.in.gov/dor/files/dn01.pdf" target="_blank" rel="noopener">Indiana Department of Revenue</a>, 2026 county rates, added to the 2.95% state rate; *Boone County&rsquo;s rate rose from 1.70% to 1.71% on October 1, 2026. Property tax rate: 2026 certified rates, median taxing district, per $100 of assessed value (Indiana DLGF via <a href="https://www.stats.indiana.edu/web/profiles/tax_rates_2026/Hamilton.html" target="_blank" rel="noopener">STATS Indiana</a>); it applies after deductions, and a homestead&rsquo;s bill is capped at 1% of its assessed value, so see <a href="/blog/indiana-property-tax-caps-explained/">Indiana property tax caps explained</a>. Town price ranges are general ranges from our town guides, not current medians. &mdash; = not in our data.</p>

 <h2 id="how-it-works">How This Calculator Works</h2>
 <p><strong>The data.</strong> The U.S. Bureau of Economic Analysis publishes <a href="{BEA_PAGE}" target="_blank" rel="noopener">Regional Price Parities</a> (RPPs) for every metro area, plus the nonmetropolitan (rural and small-town) part of each state. Each one compares the local price level with the national average, set at 100. Indianapolis, which BEA defines as the {html.escape(indy_name)} metro, scores {I[0]:.1f} for {year}, so prices there run {rel(I[0])} average. Categories use the same scale, so the U.S. figure for rents, for example, is {U[2]:.1f} rather than exactly 100; every comparison uses the same category on both sides. This page uses the {year} figures, the latest available, released {upd} (BEA tables MARPP for metro areas and PARPP for nonmetro areas).{deline}</p>
 <p><strong>The math.</strong> Equivalent salary = your salary &times; (price level where you&rsquo;re going &divide; price level where you are). For a move from the San Francisco metro ({A[sf][3][0]:.1f}): $100,000 &times; {I[0]:.1f} &divide; {A[sf][3][0]:.1f} &asymp; {money(eq100(sf))}. Category differences use the same ratio for each category.</p>
 <p><strong>The categories.</strong> <em>Housing</em> is based on rents (BEA estimates housing price levels from tenant-occupied homes). <em>Goods</em> covers things you buy, such as food, clothing and household items. <em>Utilities</em> means electricity, gas, water and sewer. <em>Other services</em> is everything else, such as medical care, recreation and transportation services.</p>
 <p><strong>What it leaves out.</strong> Taxes aren&rsquo;t part of RPPs, and Indiana&rsquo;s flat 2.95% income tax plus county rates, a 7% sales tax and capped property taxes can change the picture a lot (our <a href="/blog/cost-of-living-in-indianapolis/">cost of living breakdown</a> covers them). The figures are metro-wide averages, so a specific neighborhood can cost more or less, home purchase prices aren&rsquo;t measured directly, and your own spending mix may differ from the average household&rsquo;s. Prices have moved since {year}, though the gaps between metros tend to change slowly. These are estimates for planning, not financial advice. The cleaned data behind the calculator is <a href="{rpp_path}">available as JSON</a>.</p>

 <div class="cta-block">
 <h3>Planning a Move to Indianapolis?</h3>
 <p>Tell us your budget and where you&rsquo;ll be working, and our team will show you which parts of the metro make the numbers work, whether you plan to rent first or buy right away.</p>
 <div class="btn-group">
 <a href="/schedule/" class="btn btn-white">Book a Free Call &rarr;</a>
 <a href="/search/" class="btn btn-outline">Search Homes for Sale</a>
 </div>
 </div>

 <section class="faq-section">
 <h2 id="faq">Frequently Asked Questions</h2>
{faq_html}
 </section>

 <h2 id="related">Related Guides</h2>
 <div class="col-related">
 <a href="/blog/cost-of-living-in-indianapolis/" class="city-card">Cost of Living in Indianapolis <span class="arrow">&rsaquo;</span></a>
 <a href="/blog/living-in-indianapolis-pros-and-cons/" class="city-card">Living in Indianapolis: Pros and Cons <span class="arrow">&rsaquo;</span></a>
 <a href="/guides/moving-to-indianapolis/" class="city-card">Moving to Indianapolis Guide <span class="arrow">&rsaquo;</span></a>
 <a href="/services/relocation-buyers/" class="city-card">Relocation Buyers <span class="arrow">&rsaquo;</span></a>
 <a href="/services/mortgages/" class="city-card">Mortgage Payment Calculator <span class="arrow">&rsaquo;</span></a>
 <a href="/compare/" class="city-card">Suburb vs. Suburb Comparisons <span class="arrow">&rsaquo;</span></a>
 </div>

 </div>
</div>

<section class="cta-form-section">
 <div class="container">
 <h2>Talk Through Your Move With Our Team</h2>
 <p>Share where you&rsquo;re coming from and what you want to spend, and a Your Realty Link agent will reach out. No obligation, no pressure.</p>
 <form class="ipg-lead-form">
 <input type="hidden" name="source_page" value="{SLUG}">
 <input type="hidden" name="interest_type" value="Relocating">
 <div class="form-row">
 <div><label for="sv-name">Name *</label><input type="text" id="sv-name" name="name" required placeholder="Your name"></div>
 <div><label for="sv-phone">Phone *</label><input type="tel" id="sv-phone" name="phone" required placeholder="317-555-1234"></div>
 </div>
 <label for="sv-email">Email *</label>
 <input type="email" id="sv-email" name="email" required placeholder="you@example.com">
 <label for="sv-message">How can we help?</label>
 <textarea id="sv-message" name="message" placeholder="Where you're moving from, your timing, the areas you're considering..."></textarea>
 <button type="submit">Send Message &rarr;</button>
 <p class="form-note">No spam &middot; No obligation &middot; We respond personally</p>
 </form>
 </div>
</section>

{ftr}
<script type="application/json" id="col-data">{data_json}</script>
<script>{JS}</script>
{tail}</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"built /{SLUG}/ ({len(page) // 1024} KB, {len(rpp['areas'])} areas, {len(towns)} towns, MIBOR {month})")

    sm_path = os.path.join(ROOT, "sitemap.xml")
    sm = open(sm_path, encoding="utf-8").read()
    if f"<loc>{URL}</loc>" not in sm:
        today = datetime.date.today().isoformat()
        sm = sm.replace("</urlset>", f"  <url>\n    <loc>{URL}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>")
        open(sm_path, "w", encoding="utf-8").write(sm)
        print("added sitemap entry")


def main():
    if "--download" in sys.argv or "--from-dir" in sys.argv:
        src = sys.argv[sys.argv.index("--from-dir") + 1] if "--from-dir" in sys.argv else None
        write_rpp(build_rpp(fetch_tables(src)))
    rpp, path = load_rpp()
    render_card()
    build(rpp, path)


if __name__ == "__main__":
    main()
