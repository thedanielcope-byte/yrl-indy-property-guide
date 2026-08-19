#!/usr/bin/env python3
"""Add a visible E-E-A-T reviewer/credential line to content pages, site-wide.

Inserts right after the hero-badges block (uniform across templates). Idempotent,
HTML-only (no whitespace reflow), div-balance-checked. Skips glossary/agents (own
author) and the homepage. Run with --apply; default is a dry run.

  python3 add_reviewed_line.py          # dry run: report matches
  python3 add_reviewed_line.py --apply  # write changes
"""
import os, re, sys

APPLY = "--apply" in sys.argv
BYLINE = ('<p class="hero-reviewed">✔ Reviewed by '
          '<a href="/agents/janet-giles/">Janet Giles-Schultz</a>, '
          'Principal Broker · MIBOR member · Updated August 2026</p>')

# content templates that benefit from the reviewer line
INCLUDE_TOP = {"counties", "cities", "services", "best", "compare", "guides",
               "neighborhoods", "blog", "market-updates", "communities", "schools",
               "resources"}
# never touch these (own author / deprioritized / regenerated)
SKIP_TOP = {"glossary", "agents"}

HERO_BADGES = re.compile(r'(<div class="hero-badges">.*?</div>)', re.DOTALL)

def eligible(rel):
    parts = rel.split(os.sep)
    top = parts[0]
    if top in SKIP_TOP:
        return False
    return top in INCLUDE_TOP

def process(path):
    h = open(path, encoding="utf-8").read()
    if "hero-reviewed" in h:
        return "skip-present"
    m = HERO_BADGES.search(h)
    if not m:
        return "skip-no-anchor"
    out = h[:m.end()] + BYLINE + h[m.end():]
    if out.count("<div") != out.count("</div>"):
        return "IMBALANCE"
    if APPLY:
        open(path, "w", encoding="utf-8").write(out)
    return "ok"

def main():
    stats = {}
    ok_files = []
    for dp, dn, fn in os.walk("."):
        if "/.git" in dp:
            continue
        for f in fn:
            if f != "index.html":
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, ".")
            if rel == "index.html" or not eligible(rel):
                continue
            r = process(path)
            stats[r] = stats.get(r, 0) + 1
            if r == "ok":
                ok_files.append(rel)
    print(("APPLIED" if APPLY else "DRY-RUN"), stats)
    for r in ok_files[:6]:
        print("   +", r)
    if len(ok_files) > 6:
        print(f"   … and {len(ok_files)-6} more")

if __name__ == "__main__":
    main()
