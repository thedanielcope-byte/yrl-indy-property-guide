#!/usr/bin/env python3
"""Add an "every community" line to each county hub so ALL of the county's
incorporated cities & towns are shown — not just the ones with their own page.
Cities that have a page stay as the linked cards above; the remaining
incorporated towns are named in a marker-wrapped note with a county-wide search
link. Idempotent, HTML-only. Town lists come from county_towns.json.
"""
import os, re, html, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = "<!-- COUNTY-ALL-TOWNS -->", "<!-- /COUNTY-ALL-TOWNS -->"
SEARCH = "https://yourrealtylink.com/property-search"

TOWNS = json.load(open(os.path.join(ROOT, "county_towns.json"), encoding="utf-8"))


def card_names(t):
    return re.findall(r'class="city-card"><h3>([^<]+)</h3>', t)


def county_key(slug):
    # "hancock-county" -> "Hancock", "bartholomew-county" -> "Bartholomew"
    return slug.replace("-county", "").replace("-", " ").title()


def main():
    hubs = sorted(glob.glob(os.path.join(ROOT, "counties", "*", "index.html")))
    # every town that already has a card ANYWHERE (so a shared town with a page
    # in its primary county isn't re-listed as text in a neighbor county)
    global_carded = set()
    for h in hubs:
        global_carded.update(card_names(open(h, encoding="utf-8").read()))

    done = 0
    for hub in hubs:
        slug = os.path.basename(os.path.dirname(hub))            # hamilton-county-indiana-real-estate
        cslug = slug.replace("-indiana-real-estate", "")          # hamilton-county
        key = county_key(cslug)
        cname = key + " County"
        src = open(hub, encoding="utf-8").read()
        shown = set(card_names(src))
        full = TOWNS.get(key, [])
        add = []
        for t in full:
            if t == "Indianapolis":                               # the county's core, not an "other" town
                continue
            if t in shown or t in global_carded or t in add:
                continue
            add.append(t)

        # strip any prior block
        src = re.sub(r"\s*" + re.escape(BEGIN) + r".*?" + re.escape(END), "", src, flags=re.DOTALL)

        if add:
            names = ", ".join(html.escape(t) for t in add)
            block = (f'\n {BEGIN}\n'
                     f' <p class="county-towns-note" style="font-size:.95rem;color:#6e6e70;margin:14px 0 0;">'
                     f'<strong>Your Realty Link serves every {html.escape(cname)} community.</strong> '
                     f'Beyond the cities above, that includes {names}. '
                     f'<a href="{SEARCH}">Search homes anywhere in {html.escape(cname)} &rarr;</a></p>\n'
                     f' {END}')
            m = re.search(r'\n\s*<!-- MARKET -->', src)
            if m:
                src = src[:m.start()] + block + src[m.start():]
            else:
                continue
            done += 1
        open(hub, "w", encoding="utf-8").write(src)

    print("added 'every community' line to %d county hubs" % done)


if __name__ == "__main__":
    main()
