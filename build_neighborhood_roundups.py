#!/usr/bin/env python3
"""
build_neighborhood_roundups.py — "Best Neighborhoods in <Town>, Indiana" roundups (Nov 2026).

One page per town with MIN_COMMS+ named communities in communities.json, at
/best/neighborhoods-in-<town>-indiana/. Built on the /best/ template (build_best.head + the same
chrome: Quick Answer + qa-facts, How We Chose These, At a Glance, FAQ + FAQPage schema), plus an
ItemList JSON-LD of the neighborhoods.

Nothing is invented: every name, type, price band, school district and highlight comes from
communities.json (the 10 hand-authored community pages have no data fields there, so EXISTING
carries facts copied from their own pages). Town character/commute come from city_guides_data.py.
Neighborhoods are GROUPED by type, not ranked.

Also maintains:
  - the "Best Neighborhoods by Town" section on /best/ (BEST-NEIGHBORHOODS markers)
  - sitemap entries for new URLs
Run after: python3 inject_community_siblings.py && python3 inject_city_communities.py, then the usual
inject chain (inject_gtag.py etc. — head is built from scratch).

Usage: python3 build_neighborhood_roundups.py [--check]
"""
import os, re, sys, json, glob, html, collections

import build_best as bb
import city_guides_data as cgd

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = bb.SITE
MIN_COMMS = 6
SKIP = {"Indianapolis"}          # city-wide neighborhoods live in the Indianapolis best-neighborhoods post + area guides
YEAR = "2026"

DATA = json.load(open(os.path.join(ROOT, "communities.json"), encoding="utf-8"))
SCHOOLS = json.load(open(os.path.join(ROOT, "schools.json"), encoding="utf-8"))["districts"]

# Facts for the hand-authored community pages (existing:true has no data in communities.json).
# Copied from each page's own price, "Living in" and "Schools" sections (Nov 2026).
EXISTING = {
    "village-of-westclay-carmel": dict(price_band="$400s to $1M+", type="traditional-neighborhood community", school_district="Carmel Clay Schools",
        highlights=["Walkable village center and shared greens", "Townhomes, cottages and custom homes", "Front-porch, sidewalk-first street design"]),
    "brookshire-carmel": dict(price_band="$300s to $600s", type="established golf community", school_district="Carmel Clay Schools",
        highlights=["Tree-lined, established streets with consistent lot sizes", "Anchored by the neighborhood golf club"]),
    "chatham-hills-westfield": dict(price_band="$500s to $2M+", type="luxury golf community", school_district="Westfield Washington Schools",
        highlights=["Upscale club with championship golf and dining", "Custom estate homes in a master-planned setting"]),
    "bridgewater-club-westfield": dict(price_band="$500s to $2M", type="luxury golf community", school_district="Westfield Washington Schools",
        highlights=["Member club with championship golf", "Polished, well-tended landscaping throughout"]),
    "windermere-fishers": dict(price_band="$300s to $700s+", type="golf community", school_district="Hamilton Southeastern Schools",
        highlights=["Built around Ironwood Golf Course", "Clubhouse, pool, tennis courts and walking trails", "Close to Geist Reservoir"]),
    "avalon-fishers": dict(price_band="$300s to $500s", type="established family subdivision", school_district="Hamilton Southeastern Schools",
        highlights=["Mature landscaping and community green space", "Everyday shopping close by"]),
    "holliday-farms-zionsville": dict(price_band="$700s to $2M+", type="luxury golf community", school_district="Zionsville Community Schools",
        highlights=["Pete Dye golf course", "Modern luxury homes on generous lots with high-end amenities"]),
    "irishmans-run-zionsville": dict(price_band="$600s to $1.5M", type="estate community", school_district="Zionsville Community Schools",
        highlights=["Estate homes on large, wooded homesites", "Minutes from Zionsville's brick Main Street"]),
    "sagamore-noblesville": dict(price_band="$400s to $1M+", type="golf community", school_district="Noblesville Schools",
        highlights=["Jack Nicklaus Signature golf course", "Homesites from villa lots to estate parcels approaching an acre"]),
    "kensington-grove-greenwood": dict(price_band="$300s to $600s", type="established family subdivision", school_district="Center Grove Community Schools",
        highlights=["Lots from about a third of an acre to about an acre", "Five-acre neighborhood park"]),
}

esc, plain = bb.esc, bb.plain
def disp(c): return c.get("short_name") or c["name"]
def kebab(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "").replace("’", "")).strip("-")
def slug_for(town): return f"neighborhoods-in-{kebab(town)}-indiana"
def url_for(town): return f"/best/{slug_for(town)}/"

CITY_DIRS = sorted(glob.glob(os.path.join(ROOT, "cities", "*", "*") + os.sep))
def city_url(town):
    k = kebab(town)
    for d in CITY_DIRS:
        b = os.path.basename(d.rstrip(os.sep))
        if b.startswith(k + "-"):
            return "/" + os.path.relpath(d, ROOT).replace(os.sep, "/").rstrip("/") + "/"
    return None

def county_url(county):
    p = f"counties/{kebab(county)}-county-indiana-real-estate/"
    return "/" + p if os.path.isdir(os.path.join(ROOT, p)) else None

def living_url(town):
    k = kebab(town)
    for s in (f"living-in-{k}-indiana-pros-and-cons", f"living-in-{k}-indiana-what-to-know-before-you-move", f"living-in-{k}-indiana"):
        if os.path.isfile(os.path.join(ROOT, "blog", s, "index.html")):
            return f"/blog/{s}/"
    return None

def compare_links(town, n=3):
    k = kebab(town)
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, "compare", "*", ""))):
        b = os.path.basename(d.rstrip(os.sep))
        parts = b.split("-vs-")
        if len(parts) == 2 and (parts[0] == k or parts[1] == k):
            other = parts[1] if parts[0] == k else parts[0]
            out.append((f"/compare/{b}/", f"{town} vs. {other.replace('-', ' ').title()}"))
    return out[:n]

# --- school district links -------------------------------------------------------------------
_STOP = {"community", "school", "schools", "corporation", "consolidated", "district", "city", "of", "the", "msd", "metropolitan", "united", "town", "corp"}
def _core(s): return frozenset(w for w in re.findall(r"[a-z]+", s.lower()) if w not in _STOP)
_SCHOOL_IDX = [(_core(d["name"]), d["slug"]) for d in SCHOOLS]
def school_link(name):
    if not name or ";" in name or " or " in name or "/" in name or "varies" in name:
        return esc(name) if name else "confirm by address"
    core = _core(name)
    for c, slug in _SCHOOL_IDX:
        if core and c == core and os.path.isdir(os.path.join(ROOT, "schools", slug)):
            return f'<a href="/schools/{slug}/">{esc(name)}</a>'
    return esc(name)

# --- price bands -----------------------------------------------------------------------------
_TOK = re.compile(r"(?:\b(low|mid|high|upper)[- ]?)?\$\s?(\d+(?:\.\d+)?)\s?(M|K|s)?(\+)?", re.I)
_QOFF = {"low": 0, "mid": 40, "high": 70, "upper": 70}
def price_vals(band):
    """-> (low_k, high_k, low_label, high_label) or None. '$300s to $1.5M+' -> (300, 1500, '$300s', '$1.5M+')."""
    if not band: return None
    toks = list(_TOK.finditer(band))
    if not toks: return None
    def val(m):
        n = float(m.group(2)); u = (m.group(3) or "").upper()
        base = n * 1000 if u == "M" else n
        return base + (_QOFF.get((m.group(1) or "").lower(), 0) if u != "M" else 0)
    def lab(m):
        q, n, u, plus = (m.group(1) or ""), m.group(2), (m.group(3) or ""), (m.group(4) or "")
        u = "M" if u.upper() == "M" else ("s" if u.lower() == "s" else "")
        return (f"{q.lower()}-" if q else "") + f"${n}{u}{plus}"
    lo, hi = toks[0], toks[-1]
    hi_lab = lab(hi) + ("+" if band.strip().endswith("+") and not lab(hi).endswith("+") else "")
    return val(lo), val(hi), lab(lo), hi_lab

# --- grouping --------------------------------------------------------------------------------
GROUPS = [  # key, h2, intro, best-for phrase
    ("established", "Established Family Neighborhoods", "Settled subdivisions with mature trees, neighborhood amenities and a track record.", "families who want an established neighborhood"),
    ("new", "New-Construction Communities", "Communities where builders are, or recently were, still building, so you can buy new or nearly new.", "buyers who want a new or nearly new home"),
    ("master", "Master-Planned Communities", "Larger planned communities with shared amenities designed in from the start.", "buyers who want built-in amenities"),
    ("golf", "Golf Communities", "Neighborhoods built around a golf course, with fairway and club-adjacent homes.", "golfers"),
    ("water", "Lake & Waterfront Neighborhoods", "Homes on or near the water, from private lakes to reservoir frontage.", "buyers who want to live on the water"),
    ("luxury", "Luxury & Estate Neighborhoods", "The top of the local market: custom and estate homes, larger lots, club amenities.", "luxury buyers"),
    ("custom", "Custom-Home Neighborhoods", "Neighborhoods of individually built homes on larger lots.", "custom-home buyers"),
    ("historic", "Historic Neighborhoods", "Older neighborhoods with original architecture and character.", "buyers who love older homes"),
    ("lowmaint", "Low-Maintenance, Condo & Townhome Communities", "Villas, condos and townhomes where an association handles much of the upkeep.", "buyers who want less upkeep"),
    ("55plus", "55+ Active-Adult Communities", "Age-restricted communities built for buyers 55 and older.", "buyers 55 and older"),
]
GMAP = {g[0]: g for g in GROUPS}

def tags(c):
    ty = (c.get("type") or "").lower()
    pv = price_vals(c.get("price_band"))
    lo = pv[0] if pv else 0
    t = []
    if "55" in ty or "active adult" in ty or "active-adult" in ty: t.append("55plus")
    if "luxury" in ty or "estate" in ty or lo >= 700: t.append("luxury")
    if "golf" in ty: t.append("golf")
    if any(k in ty for k in ("lake", "waterfront", "lakefront")): t.append("water")
    if any(k in ty for k in ("new-construction", "new construction", "newer")): t.append("new")
    if "master-planned" in ty or "traditional-neighborhood" in ty: t.append("master")
    if any(k in ty for k in ("low-maintenance", "villa", "condo", "townhome")): t.append("lowmaint")
    if "historic" in ty: t.append("historic")
    if "custom" in ty: t.append("custom")
    if not t: t.append("established")
    return t

PRIMARY_ORDER = ["55plus", "luxury", "golf", "water", "lowmaint", "new", "master", "historic", "custom", "established"]
def primary(c):
    t = tags(c)
    return next(k for k in PRIMARY_ORDER if k in t)

def best_for(c):
    t = tags(c)
    phrases = [GMAP[k][3] for k in PRIMARY_ORDER if k in t][:2]
    return (", " if any(" and " in p for p in phrases) else " and ").join(phrases)

def poss(name):
    return name + ("&rsquo;" if name.endswith("s") else "&rsquo;s")

_NOUNS = {"community", "subdivision", "neighborhood", "building", "district", "development", "estates", "area", "village", "communities"}
def noun_type(ty):
    ty = (ty or "neighborhood").strip()
    return ty if ty.split()[-1].lower() in _NOUNS else ty + " community"

def article(word):
    return "an" if word[:1].lower() in "aeiou" else "a"

def join_names(names):
    names = list(names)
    if len(names) <= 1: return "".join(names)
    if len(names) == 2: return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f" and {names[-1]}"

def sentence(s):
    s = s.strip().rstrip(".")
    return s[:1].upper() + s[1:] + "."

# --- page record -----------------------------------------------------------------------------
def build_record(town, comms, all_towns):
    for c in comms:
        if c["slug"] in EXISTING:
            for k, v in EXISTING[c["slug"]].items():
                c.setdefault(k, v)
    n = len(comms)
    county = collections.Counter(c["county"] for c in comms).most_common(1)[0][0]
    cu, cnty = city_url(town), county_url(county)
    priced = [(c, price_vals(c.get("price_band"))) for c in comms]
    priced = [(c, p) for c, p in priced if p]
    cheap = min(priced, key=lambda x: (x[1][0], x[1][1]))
    top = max([x for x in priced if x[0] is not cheap[0]] or priced, key=lambda x: (x[1][1], x[1][0]))
    lo_lab = min(priced, key=lambda x: x[1][0])[1][2]
    hi_lab = max(priced, key=lambda x: x[1][1])[1][3]
    # one name per district (the data spells some two ways, e.g. "... Schools" / "... School Corporation")
    by_core = collections.OrderedDict()
    for d in (c.get("school_district") for c in comms if c.get("school_district")):
        by_core.setdefault(_core(d), collections.Counter())[d] += 1
    districts = [cnt.most_common(1)[0][0] for _, cnt in sorted(by_core.items(), key=lambda kv: -sum(kv[1].values()))]
    clean_districts = [d for d in districts if not any(x in d for x in (";", " or ", "/", "varies"))]
    by_group = collections.OrderedDict((g[0], []) for g in GROUPS)
    for c in comms: by_group[primary(c)].append(c)
    for k in by_group: by_group[k].sort(key=lambda c: (price_vals(c.get("price_band")) or (9e9, 9e9))[:2])
    groups = [(k, v) for k, v in by_group.items() if v]
    g_new = [c for c in comms if "new" in tags(c)]
    g_master = [c for c in comms if "master" in tags(c) and c not in g_new]
    g_golf, g_water, g_lux = by_group["golf"], by_group["water"], by_group["luxury"]
    g_low = by_group["lowmaint"] + by_group["55plus"]

    city = cgd.CITIES.get(kebab(town))
    living, compares = living_url(town), compare_links(town)

    # Quick answer
    lead = (f"{poss(town)} named neighborhoods run from <strong>{esc(disp(cheap[0]))}</strong> (typically "
            f"{esc(cheap[0]['price_band'])}) to <strong>{esc(disp(top[0]))}</strong> ({esc(top[0]['price_band'])}).")
    picks, used = [], set()
    def pick(label, group, k):
        names = [c for c in group if c["slug"] not in used][:k]
        if names:
            used.update(c["slug"] for c in names)
            picks.append(f"{label}{join_names(esc(disp(c)) for c in names)}")
    pick("for new construction, look at ", g_new, 3)
    pick("for a master-planned community, ", g_master, 2)
    pick("for golf-course living, ", g_golf, 2)
    pick("for the water, ", g_water, 2)
    pick("for less upkeep, ", g_low, 2)
    if picks:
        lead += " " + sentence(picks[0] if len(picks) == 1 else (", and ".join(picks) if len(picks) == 2 else "; ".join(picks[:-1]) + "; and " + picks[-1]))
    if clean_districts:
        lead += f" Most are served by {esc(clean_districts[0])}" + (f" or {esc(clean_districts[1])}" if len(clean_districts) > 1 else "") + "."
    facts = [
        {"label": "Neighborhoods in this guide", "value": str(n)},
        {"label": "Typical prices", "value": f"{lo_lab} &ndash; {hi_lab}"},
        {"label": "Most affordable", "value": f'<a href="/communities/{cheap[0]["slug"]}/">{esc(disp(cheap[0]))}</a>'},
        {"label": "Top of the market", "value": f'<a href="/communities/{top[0]["slug"]}/">{esc(disp(top[0]))}</a>'},
    ]
    if clean_districts:
        facts.append({"label": "School district" + ("s" if len(clean_districts) > 1 else ""), "value": " &middot; ".join(school_link(d) for d in clean_districts[:2])})

    # Intro
    intro = []
    if city and "known for its local character" not in city["character"]:
        intro.append(f"{town} is {city['character']}. It&rsquo;s {city['commute']}, and homes across {town} typically range from "
                     f"{city['price']}.")
    else:
        intro.append(f"{town} sits in {county} County, and like most Central Indiana towns it&rsquo;s really a collection of distinct "
                     f"neighborhoods, each with its own price range, age of homes and amenities.")
    intro.append(f"This guide covers the {n} named neighborhoods and subdivisions in {town} that we track in our "
                 f'<a href="/communities/">Central Indiana communities directory</a>. They&rsquo;re grouped by the kind of home and '
                 f"lifestyle buyers usually ask us for, not ranked, because the best neighborhood depends on your budget, your schools "
                 f"and how you want to live. Each one links to its own page with more detail.")

    how_we_chose = [
        "Every neighborhood here is a real, named subdivision or community, researched from builder, HOA, county and listing "
        "sources for our communities directory. We group them by type (established, new construction, golf, waterfront, "
        "luxury and so on) instead of ranking them, since a great fit for a first-time buyer and a great fit for an estate-home "
        "buyer are different places.",
        "Price ranges are typical, rounded ranges, not appraisals; any single home can fall outside them. School districts are "
        "the district most of each neighborhood falls in, but boundaries can split a subdivision, so always confirm the "
        "assignment for a specific address. Nothing here is sponsored.",
    ]

    rows = [[f'<a href="/communities/{c["slug"]}/">{esc(disp(c))}</a>', esc((c.get("type") or "").capitalize() or "Neighborhood"),
             esc(c.get("price_band") or "Varies"), school_link(c.get("school_district"))]
            for k, v in groups for c in v]

    sections = []
    for k, v in groups:
        g = GMAP[k]
        items = []
        for c in v:
            ty = noun_type(c.get("type"))
            body = [f"{esc(c['name'])} is {article(ty)} {esc(ty)} in {esc(town)}"
                    + (f" with homes typically in the {esc(c['price_band'])}" if c.get("price_band") else "") + "."]
            if c.get("school_district"): body.append(f"Schools: {school_link(c['school_district'])}.")
            hl = "".join(f"<li>{esc(h.strip().rstrip('.'))}</li>" for h in (c.get("highlights") or [])[:4])
            items.append(
                f' <h3 id="{c["slug"]}"><a href="/communities/{c["slug"]}/">{esc(c["name"])}</a></h3>\n'
                f' <p><strong>Best for:</strong> {esc(best_for(c))}.</p>\n'
                f' <p>{" ".join(body)}</p>\n'
                + (f' <ul>{hl}</ul>\n' if hl else "")
                + f' <p><a href="/communities/{c["slug"]}/">See {esc(disp(c))} homes and details &rarr;</a></p>')
        sections.append(f' <h2 id="{k}">{esc(g[1])}</h2>\n <p>{esc(g[2])}</p>\n' + "\n".join(items))

    choose = [f"Start with budget and schools, then narrow by the kind of neighborhood you want."]
    if cu: choose.append(f'Our <a href="{cu}">{town} real estate guide</a> covers {town} as a whole, including commute, parks and the local market.')
    if living: choose.append(f'For the honest tradeoffs of the town itself, read <a href="{living}">living in {town}: pros and cons</a>.')
    if compares:
        choose.append("Weighing another suburb too? Compare " + join_names(f'<a href="{u}">{esc(t)}</a>' for u, t in compares) + ".")
    choose.append(f'When you&rsquo;re ready, <a href="/search/?q={town.replace(" ", "+")}">search homes in {town}</a> or ask us to set up tours of two or three neighborhoods back to back.')

    faqs = [
        {"q": f"What are the best neighborhoods in {town}, Indiana?",
         "a": f"It depends on what you want. In our guide, {poss(town)} neighborhoods range from {esc(disp(cheap[0]))} "
              f"({esc(cheap[0]['price_band'])}) to {esc(disp(top[0]))} ({esc(top[0]['price_band'])})"
              + (f"; for new construction, look at {join_names(esc(disp(c)) for c in g_new[:3])}" if g_new else "")
              + (f"; for golf-course living, {join_names(esc(disp(c)) for c in g_golf[:2])}" if g_golf else "")
              + (f"; for waterfront living, {join_names(esc(disp(c)) for c in g_water[:2])}" if g_water else "")
              + ". We group all " + str(n) + " by type above, with typical prices and schools for each."},
        {"q": f"What is the most affordable neighborhood in {town}?",
         "a": f"Of the {n} neighborhoods in this guide, {esc(disp(cheap[0]))} has the lowest typical price range, about "
              f"{esc(cheap[0]['price_band'])}. Prices vary by home, so ask us for a current market analysis on any address."},
    ]
    if g_new:
        faqs.append({"q": f"Which {town} neighborhoods have new construction?",
                     "a": f"In our guide, {join_names(esc(disp(c)) for c in g_new)} {'is' if len(g_new) == 1 else 'are'} new or newer construction. "
                          f"Builder inventory changes quickly, so check with us for which sections are still building."})
    if g_lux or g_golf:
        lx = (g_lux + g_golf)[:3]
        faqs.append({"q": f"Are there luxury or golf neighborhoods in {town}?",
                     "a": f"Yes. {join_names(esc(disp(c)) for c in lx)} {'is' if len(lx) == 1 else 'are'} among the {town} neighborhoods in our guide with "
                          f"luxury, estate or golf-course homes. Each has its own page with typical prices and amenities."})
    if clean_districts:
        faqs.append({"q": f"What school district serves {town} neighborhoods?",
                     "a": f"Most of the neighborhoods in this guide are served by {join_names(esc(d) for d in clean_districts[:3])}. Boundaries can split "
                          f"a subdivision, so confirm the school assignment for a specific address with the district."})
    faqs.append({"q": f"How do I search homes in a specific {town} neighborhood?",
                 "a": f"Use our MIBOR listing search and filter by {town}, or tell us which neighborhoods you like and we&rsquo;ll set up "
                      f"alerts and tours. Every neighborhood page in this guide also links to its listings."})

    county_peers = [t for t in all_towns if t != town and all_towns[t] == county]
    related = [(url_for(t), f"Best Neighborhoods in {t}") for t in county_peers[:5]] + [("/best/", "All Best Of Guides")]
    top_links = [(u, t) for u, t in [(cu, f"{town} Real Estate Guide"), (living, f"Living in {town}: Pros &amp; Cons"),
                                     (cnty, f"{county} County Real Estate"), ("/communities/", "All Communities &amp; Subdivisions")] if u]
    top_links = [(u, plain(t)) for u, t in top_links]

    title = f"Best Neighborhoods in {town}, Indiana ({YEAR})"
    meta_title = title + " | Your Realty Link" if len(title) + 19 <= 60 else title
    desc = (f"{n} of the best neighborhoods in {town}, Indiana, from {plain(esc(disp(cheap[0])))} to {plain(esc(disp(top[0])))}, "
            f"with typical prices, schools and what each one is best for.")
    if len(desc) > 160:
        desc = f"{n} neighborhoods in {town}, Indiana, grouped by type, with typical price ranges, school districts and what each one is best for."

    return {
        "slug": slug_for(town), "town": town, "county": county,
        "hub_card_label": f"Best Neighborhoods in {town}",
        "breadcrumb": f"Best Neighborhoods in {town}",
        "h1": f"Best Neighborhoods in <em>{esc(town)}, Indiana</em>",
        "meta_title": meta_title, "og_title": title, "meta_desc": desc,
        "faq_heading": f"Neighborhoods in {town}",
        "hero_sub": f"{n} {esc(town)} neighborhoods and subdivisions, grouped by what buyers usually want, with typical price ranges, schools and what each one is best for.",
        "badges": [f"&#128205; {esc(county)} County", f"&#127969; {n} neighborhoods", f"&#128176; {lo_lab} &ndash; {hi_lab}"],
        "quick_answer": {"lead": lead, "facts": facts},
        "intro": intro, "how_we_chose": how_we_chose,
        "at_a_glance": {"cols": ["Neighborhood", "Type", "Typical prices", "Schools"], "rows": rows},
        "sections": sections, "how_to_choose": " ".join(choose),
        "cta": {"h3": f"Want a Short List in {town}?",
                "p": f"Tell us your budget, schools and must-haves. We&rsquo;ll narrow {town} to two or three neighborhoods and set up tours."},
        "faqs": faqs,
        "sidebar": {"top_label": f"{town} Resources", "top_links": top_links, "related": related},
        "itemlist": [(c["name"], f"{SITE}/communities/{c['slug']}/") for k, v in groups for c in v],
    }

def render(r):
    """build_best's head + body, with the picks swapped for grouped sections and an ItemList added."""
    r2 = dict(r, picks=[])
    page = bb.head(r2) + bb.body(r2)
    # body() renders picks between the At a Glance table and "How to Choose"; ours go there instead.
    marker = " <h2>How to Choose</h2>"
    assert marker in page
    page = page.replace(marker, "\n\n".join(r["sections"]) + "\n\n" + marker, 1)
    items = ",\n".join(
        '  { "@type": "ListItem", "position": %d, "name": %s, "url": %s }' % (i, json.dumps(n, ensure_ascii=False), json.dumps(u))
        for i, (n, u) in enumerate(r["itemlist"], 1))
    ld = ('<script type="application/ld+json">\n{ "@context": "https://schema.org", "@type": "ItemList", "name": %s,\n "itemListElement": [\n%s\n ] }\n</script>\n'
          % (json.dumps(plain(r["breadcrumb"]) + ", Indiana", ensure_ascii=False), items))
    page = page.replace("</head>", ld + "</head>", 1)
    return page

HUB_START, HUB_END = "<!-- BEST-NEIGHBORHOODS -->", "<!-- /BEST-NEIGHBORHOODS -->"
def update_hub(recs):
    p = os.path.join(ROOT, "best", "index.html")
    t = open(p, encoding="utf-8").read()
    cards = "\n".join('  <a href="/best/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>' % (r["slug"], esc(r["town"]))
                      for r in sorted(recs, key=lambda r: r["town"]))
    block = (f"{HUB_START}\n <h2 id=\"neighborhoods\">Best Neighborhoods by Town</h2>\n"
             f" <p>Neighborhood-by-neighborhood guides for {len(recs)} Central Indiana towns: every named subdivision we track, grouped by type, "
             f"with typical prices and schools.</p>\n <div class=\"city-grid\">\n{cards}\n </div>\n {HUB_END}")
    if HUB_START in t:
        t2 = re.sub(re.escape(HUB_START) + r".*?" + re.escape(HUB_END), lambda _: block, t, count=1, flags=re.S)
    else:
        anchor = '\n\n <div class="cta-block">\n <h3>Not Sure Which Fits You?</h3>'
        assert anchor in t, "best hub anchor not found"
        t2 = t.replace(anchor, "\n\n " + block + anchor, 1)
    if t2 != t: open(p, "w", encoding="utf-8").write(t2)

def towns():
    by = collections.defaultdict(list)
    for c in DATA["communities"]:
        by[c["city"]].append(dict(c))
    return {t: v for t, v in by.items() if len(v) >= MIN_COMMS and t not in SKIP}

def main():
    check = "--check" in sys.argv
    T = towns()
    county_of = {t: collections.Counter(c["county"] for c in v).most_common(1)[0][0] for t, v in T.items()}
    recs = [build_record(t, v, county_of) for t, v in sorted(T.items())]
    for r in recs:
        print(f"{r['slug']:<48} {len(r['itemlist']):>3}  {r['meta_title']} [{len(r['meta_title'])}] desc {len(r['meta_desc'])}")
    if check: return
    for r in recs:
        d = os.path.join(ROOT, "best", r["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render(r))
    added = bb.update_sitemap([f"{SITE}/best/{r['slug']}/" for r in recs])
    update_hub(recs)
    print(f"neighborhood roundups — built {len(recs)}; sitemap +{added}; /best/ hub updated")

if __name__ == "__main__":
    main()
