#!/usr/bin/env python3
"""
inject_compare_links.py — cross-link each city page to the "X vs Y" comparison
pages that involve it. Fixes internal-linking orphans: the auto-generated compare
pages previously had only 1 inbound link (the /compare/ hub), so they were barely
crawled. Now every compare page is linked from BOTH cities it compares.

Marker-wrapped (<!-- COMPARE-SUBURBS -->), idempotent, mirrors the existing
CITY-COMMUNITIES cross-link block (reuses .city-grid/.city-card, no new CSS).
Matchups are derived from the actual /compare/<a>-vs-<b>/ directories (so it stays
in sync with build_compare.py), keeping only pairs where BOTH sides are real city
slugs — topic compares like new-construction-vs-resale are skipped.

Usage: python3 inject_compare_links.py [--dry]
"""
import glob, os, re, sys, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv

spec = importlib.util.spec_from_file_location("cg", os.path.join(ROOT, "city_guides_data.py"))
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
CITIES = cg.CITIES  # slug -> {name, url, ...}

START, END = "<!-- COMPARE-SUBURBS -->", "<!-- /COMPARE-SUBURBS -->"
# insert before the first of these anchors that exists on the page
ANCHORS = ["<!-- CITY-COMMUNITIES -->", "<!-- IDX-LISTINGS -->", '<section class="faq-section">']


def block_for(city, pairs):
    name = CITIES[city]["name"]
    cards = "\n".join(
        ' <a href="/compare/%s-vs-%s/" class="city-card">%s vs %s <span class="arrow">&rsaquo;</span></a>'
        % (a, b, CITIES[city]["name"], CITIES[other]["name"])
        for (a, b, other) in pairs)
    return (
        "%s\n"
        ' <hr class="divider">\n'
        ' <h2 id="compare">Compare %s to Nearby Suburbs</h2>\n'
        " <p>Deciding between %s and another Central Indiana suburb? See our side-by-side"
        " comparisons of home prices, schools, commute, and lifestyle:</p>\n"
        ' <div class="city-grid">\n%s\n </div>\n'
        ' <p>Browse all <a href="/compare/">Central Indiana suburb comparisons</a>.</p>\n'
        "%s" % (START, name, name, cards, END))


def main():
    # 1) derive city-vs-city matchups from the compare/ directories
    matchups = []
    for d in sorted(glob.glob(os.path.join(ROOT, "compare", "*-vs-*"))):
        slug = os.path.basename(d)
        m = re.match(r"^(.+)-vs-(.+)$", slug)
        if not m:
            continue
        a, b = m.group(1), m.group(2)
        if a in CITIES and b in CITIES:
            matchups.append((a, b))

    # 2) city slug -> list of (a, b, other_city) for every matchup it appears in
    by_city = {}
    for a, b in matchups:
        by_city.setdefault(a, []).append((a, b, b))
        by_city.setdefault(b, []).append((a, b, a))

    injected = skipped = no_anchor = 0
    for city, pairs in sorted(by_city.items()):
        rel = CITIES[city]["url"].strip("/")
        idx = os.path.join(ROOT, rel, "index.html")
        if not os.path.exists(idx):
            skipped += 1
            continue
        s = orig = open(idx, encoding="utf-8").read()
        blk = block_for(city, sorted(pairs))
        if START in s:  # idempotent: replace the existing block
            s = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: blk, s, flags=re.S)
        else:
            anchor = next((a for a in ANCHORS if a in s), None)
            if not anchor:
                no_anchor += 1
                continue
            s = s.replace(anchor, blk + "\n " + anchor, 1)
        if s != orig:
            injected += 1
            if not DRY:
                open(idx, "w", encoding="utf-8").write(s)

    tag = " (dry-run)" if DRY else ""
    print("compare cross-links%s — cities updated: %d | no page: %d | no anchor: %d | matchups: %d"
          % (tag, injected, skipped, no_anchor, len(matchups)))


if __name__ == "__main__":
    main()
