#!/usr/bin/env python3
"""Cross-link the /compare/ cluster: add a 'More Central Indiana Comparisons'
module (links to every sibling comparison) before </main> on each compare page.
Builds a full internal-link mesh so authority flows from the strong compare
pages (already page 1) to the weaker ones. Idempotent, div-balance-checked.

  python3 add_compare_related.py --apply
"""
import os, re, sys, glob

APPLY = "--apply" in sys.argv
SPECIAL = {"vs": "vs", "fsbo": "FSBO"}

def title(slug):
    words = []
    for w in slug.split("-"):
        words.append(SPECIAL.get(w, w.capitalize()))
    return " ".join(words)

pages = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob("compare/*/index.html"))

def module(self_slug):
    others = [s for s in pages if s != self_slug]
    cards = "\n".join(
        f' <a href="/compare/{s}/" class="city-card">{title(s)} <span class="arrow">›</span></a>'
        for s in others)
    return ('\n<!-- RELATED-COMPARES -->\n<section class="related-compares">\n'
            '<h2>More Central Indiana Comparisons</h2>\n'
            '<p>Weighing another pair of communities? Compare the metro\'s most-searched matchups:</p>\n'
            '<div class="compare-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:12px">\n'
            f'{cards}\n</div>\n</section>\n')

def process(path):
    slug = os.path.basename(os.path.dirname(path))
    h = open(path, encoding="utf-8").read()
    if "RELATED-COMPARES" in h:
        return "skip-present"
    i = h.find("</main>")
    if i < 0:
        return "skip-no-main"
    out = h[:i] + module(slug) + h[i:]
    if out.count("<div") != out.count("</div>"):
        return "IMBALANCE"
    if APPLY:
        open(path, "w", encoding="utf-8").write(out)
    return "ok"

stats = {}
for p in sorted(glob.glob("compare/*/index.html")):
    r = process(p)
    stats[r] = stats.get(r, 0) + 1
    if r == "ok":
        print("  +", os.path.relpath(p, "."))
print(("APPLIED" if APPLY else "DRY-RUN"), stats)
