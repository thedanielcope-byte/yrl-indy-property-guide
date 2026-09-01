#!/usr/bin/env python3
"""
Cutover remap: the outbound yourrealtylink.com links that go DEAD when Agent3000
is retired and yourrealtylink.com becomes THIS site.

Two groups:
  1. Content links that have an equivalent page on this site  -> repoint (safe now).
  2. Property search (the IDX)                                -> repoint to the NEW IDX.
     Blocked until the new IDX URL is known. Set PROPERTY_SEARCH_TARGET at cutover.

ORDER AT CUTOVER: run `inject_idx.py` FIRST (it regenerates the marker-wrapped IDX
slot links from idx_config), THEN this script — so the slot links are already on
the new IDX and only the leftover hardcoded property-search links get remapped.

DRY RUN by default. Apply with:  python3 remap_yrl_links.py --apply
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
apply = "--apply" in sys.argv

# Interim IDX target: Displet feed not live yet, so leftover hardcoded property-search
# links go to MIBOR's public MLS search (matches the slot in idx_config.py). Swap to
# Displet's search URL when the feed is live.
PROPERTY_SEARCH_TARGET = "https://property.mibor.com/listings"

# (from, to) — longest/most-specific first so no prefix clobbers another
REMAPS = [
    ("https://yourrealtylink.com/content/mortgage-calculator", "/services/mortgages/"),
    ("https://yourrealtylink.com/content/new-construction",    "/services/new-construction/"),
    ("https://yourrealtylink.com/content/join-us",             "/services/join-yrl/"),
    ("https://yourrealtylink.com/instant-home-valuation",      "/services/free-home-valuation/"),
    ("https://yourrealtylink.com/home-valuation",              "/services/free-home-valuation/"),
    ("https://yourrealtylink.com/contact",                     "/contact/"),
]
if PROPERTY_SEARCH_TARGET:
    REMAPS.append(("https://yourrealtylink.com/property-search", PROPERTY_SEARCH_TARGET))

EXTS = (".html", ".xml", ".txt", ".js", ".json", ".md")
SKIP_DIRS = {".git", "node_modules", ".next", ".wrangler"}
SKIP_FILES = {"remap_yrl_links.py", "migrate-domain.py", "migrate-domain-yrl.py"}

totals = {frm: 0 for frm, _ in REMAPS}
changed_files = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if fn in SKIP_FILES or not fn.endswith(EXTS):
            continue
        path = os.path.join(dirpath, fn)
        try:
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new = content
        hit = False
        for frm, to in REMAPS:
            c = new.count(frm)
            if c:
                totals[frm] += c; hit = True
                new = new.replace(frm, to)
        if hit:
            changed_files += 1
            if apply:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)

print(("APPLIED" if apply else "DRY RUN") + f":  remap outbound yourrealtylink.com links")
print(f"files affected: {changed_files}\n")
for frm, to in REMAPS:
    print(f"  {totals[frm]:>5}  {frm}  ->  {to}")
if not PROPERTY_SEARCH_TARGET:
    print("\n  NOTE: property-search NOT remapped — set PROPERTY_SEARCH_TARGET to the new IDX first.")
if not apply:
    print("\nDRY RUN — nothing written. Re-run with --apply at cutover (after inject_idx.py).")
