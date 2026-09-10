#!/usr/bin/env python3
"""
inject_key_terms.py — add a curated "Real Estate Terms to Know" section (a grid of
the most relevant glossary links + a full-glossary link) to the consumer service +
Indianapolis hub + guide pages. Gives the glossary strong, topical internal inbound
links and helps readers with quick definitions in context.

Marker-wrapped (<!-- KEY-TERMS -->), idempotent, inserted right before
<footer class="site-footer">. Reuses .city-grid/.city-card (no new CSS), matching
inject_compare_links.py. Links are validated against on-disk pages before writing.

NOTE: 7 service pages are generated (home-buying-process, home-selling-process,
mortgages, buyer-/seller-closing-checklist, preferred-lenders, referral-program) —
re-run this AFTER those generators (same convention as inject_idx.py /
inject_city_communities.py). Recruiting/agent-facing service pages are intentionally
excluded (a buyer/seller glossary is off-topic there).

Usage: python3 inject_key_terms.py [--dry]
"""
import ast, json, os, re, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
START, END = "<!-- KEY-TERMS -->", "<!-- /KEY-TERMS -->"
ANCHOR = '<footer class="site-footer">'

# ---- slug -> display label, from the live glossary data ----
LABEL = {}
tree = ast.parse(open(os.path.join(ROOT, "glossary.py"), encoding="utf-8").read())
for n in tree.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "TERMS_BASE":
        for term, cat, d, link in ast.literal_eval(n.value):
            if link and link.startswith("/glossary/"):
                LABEL[link.strip("/").split("/")[-1]] = term
for p in json.load(open(os.path.join(ROOT, "glossary-pages.json"), encoding="utf-8")):
    LABEL[p["slug"]] = p["term"]           # cleaner labels win

# ---- term groups (glossary slugs; a few explicit service links as (label,url)) ----
GROUPS = {
 "buyer": ["pre-approval-vs-pre-qualification", "earnest-money", "contingency",
           "home-inspection", "home-appraisal", "escrow", "buyers-agency-agreement", "closing-day"],
 "seller": ["comparative-market-analysis", "days-on-market", "sellers-disclosure",
            "appraisal-gap", "list-to-sale-ratio", "contingency", "escrow", "closing-day"],
 "distressed": ["as-is-sale", "lien", "title-insurance", "deed", "contingency",
                "proof-of-funds", "earnest-money", ("Short Sale", "/services/short-sale/")],
 "investment": ["capitalization-rate", "cash-flow", "net-operating-income", "cash-on-cash-return",
                "after-repair-value", "gross-rent-multiplier", "1031-exchange", "house-hacking"],
 "newconstruction": ["builder-allowance", "spec-home", "model-home", "punch-list",
                     "certificate-of-occupancy", "builder-warranty", "lot-premium", "upgrades-and-options"],
 "hub": ["mls", "mibor", "comparative-market-analysis", "earnest-money",
         "contingency", "escrow", "home-inspection", "pre-approval-vs-pre-qualification"],
}

# ---- page (relative dir) -> group ----
SVC = {
 "buyer": ["buyer-representation", "first-time-home-buyers", "buyer-compensation-agreement",
           "buyer-closing-checklist", "mortgages", "mortgage-pre-approval", "mortgage-calculator",
           "down-payment-assistance", "fha-loan-buyers", "va-loan-buyers", "usda-loans",
           "relocation-buyers", "move-up-buyers", "luxury-home-buyers", "closing-costs-buyers",
           "home-buying-process", "preferred-lenders", "senior-buyers"],
 "seller": ["sell-my-home", "pricing-your-home", "home-selling-process", "home-staging",
            "for-sale-by-owner", "expired-listings", "seller-closing-checklist", "seller-net-sheet",
            "pre-listing-prep", "closing-costs-sellers", "sell-fast", "vacant-home-sale",
            "job-relocation-sale", "home-equity", "free-home-valuation", "open-houses",
            "senior-sellers", "downsizing", "luxury-home-sellers"],
 "distressed": ["foreclosures", "pre-foreclosure", "short-sale", "behind-on-payments",
                "divorce-home-sale", "estate-sales", "inherited-property", "downsizing-estate"],
 "investment": ["investment-property", "rental-property", "fix-and-flip", "1031-exchange",
                "multi-family", "cash-flow-properties", "off-market-properties",
                "sell-rental-property", "portfolio-selling", "cash-buyers"],
 "newconstruction": ["new-construction", "builder-representation", "new-home-communities",
                     "custom-home-building", "new-construction-negotiation", "new-construction-by-county"],
}
PAGE_GROUP = {}
for g, slugs in SVC.items():
    for s in slugs:
        PAGE_GROUP[f"services/{s}"] = g
# Indianapolis hub pages (all static)
PAGE_GROUP.update({
 "indianapolis-real-estate": "hub", "indianapolis-homes-for-sale": "hub",
 "indianapolis-real-estate-agent": "hub", "indianapolis-luxury-homes": "hub",
 "first-time-home-buyers-indianapolis": "buyer",
 "indianapolis-investment-properties": "investment",
 "new-construction-indianapolis": "newconstruction",
})
# guides
PAGE_GROUP.update({
 "guides/buying-a-home-in-indianapolis": "buyer",
 "guides/selling-a-home-in-indianapolis": "seller",
 "guides/indianapolis-real-estate-investing": "investment",
 "guides/moving-to-indianapolis": "hub",
})

CARD = ' <a href="%s" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'

def block_for(items):
    cards = "\n".join(CARD % (url, html.escape(label)) for label, url in items)
    return (
        "%s\n <hr class=\"divider\">\n"
        ' <section class="key-terms"><div class="container" style="max-width:900px;">\n'
        " <h2>Real Estate Terms to Know</h2>\n"
        " <p>New to the process? These quick explainers cover terms you'll run into:</p>\n"
        ' <div class="city-grid">\n%s\n </div>\n'
        ' <p>Browse all 150+ terms in our <a href="/glossary/">Central Indiana real estate glossary</a>.</p>\n'
        " </div></section>\n%s" % (START, cards, END))


def resolve(group, page_url):
    items = []
    for entry in GROUPS[group]:
        if isinstance(entry, tuple):
            label, url = entry
        else:
            url, label = f"/glossary/{entry}/", LABEL.get(entry, entry.replace("-", " ").title())
        if url == page_url:
            continue  # no self-link
        # validate target exists on disk
        rel = url.strip("/") + "/index.html"
        if not os.path.exists(os.path.join(ROOT, rel)):
            print(f"  ! skip unresolved target {url}")
            continue
        items.append((label, url))
    return items[:8]


def main():
    updated = skipped = no_anchor = 0
    for page, group in sorted(PAGE_GROUP.items()):
        idx = os.path.join(ROOT, page, "index.html")
        if not os.path.exists(idx):
            skipped += 1; print(f"  · no page: {page}"); continue
        s = orig = open(idx, encoding="utf-8").read()
        # skip redirect stubs
        if 'http-equiv="refresh"' in s:
            skipped += 1; continue
        items = resolve(group, "/" + page + "/")
        blk = block_for(items)
        if START in s:
            s = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: blk, s, flags=re.S)
        elif ANCHOR in s:
            s = s.replace(ANCHOR, blk + "\n" + ANCHOR, 1)
        else:
            no_anchor += 1; print(f"  ! no footer anchor: {page}"); continue
        if s != orig:
            updated += 1
            if not DRY:
                open(idx, "w", encoding="utf-8").write(s)

    tag = " (dry-run)" if DRY else ""
    print("\nkey-terms%s — pages updated: %d | skipped(no page/stub): %d | no anchor: %d | total targets: %d"
          % (tag, updated, skipped, no_anchor, len(PAGE_GROUP)))


if __name__ == "__main__":
    main()
