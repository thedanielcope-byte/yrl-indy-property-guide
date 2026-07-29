#!/usr/bin/env python3
"""
Brand rename: "Indy Property Guide" -> "Your Realty Link" across the whole site.

The header currently shows two competing brand lines ("Indy Property Guide" +
"Powered by Your Realty Link"); the copyright, footer prose and legal pages repeat
the pattern. A blind swap would produce "Your Realty Link - Powered by Your Realty
Link" / "Your Realty Link and Your Realty Link" redundancy, so the compound phrases
are collapsed FIRST (ordered rules), then the remaining standalone brand name is
swapped globally.

Not touched: hyphenated PDF filenames (CRM email links), dev config, JS comments.

DRY RUN by default.  Apply with:  python3 rebrand-yrl.py --apply
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {".git", "node_modules", ".next", ".wrangler"}
apply = "--apply" in sys.argv

# Ordered (old -> new). Specific/compound phrases first, global catch-all last.
RULES = [
    # --- legal-page grammar (collapse "X and Your Realty Link" cleanly) ---
    ("How Indy Property Guide and Your Realty Link collect, use, and protect your information.",
     "How Your Realty Link collects, uses, and protects your information."),
    ("Indy Property Guide and Your Realty Link provide this website",
     "Your Realty Link provides this website"),
    ("how Indy Property Guide (janetgiles.com), operated by Your Realty Link, collects",
     "how Your Realty Link (janetgiles.com) collects"),
    ("Indy Property Guide and Your Realty Link",
     "Your Realty Link"),
    # --- footer brand prose (drop redundant "powered by Your Realty Link") ---
    ("Indy Property Guide is your source for Central Indiana real estate information, powered by Your Realty Link ",
     "Your Realty Link is your source for Central Indiana real estate information "),
    ("Indy Property Guide is your source for Central Indiana real estate, powered by Your Realty Link ",
     "Your Realty Link is your source for Central Indiana real estate "),
    # --- footer copyright line (drop "Indy Property Guide - Powered by") ---
    ("2026 Indy Property Guide &middot; Powered by ", "2026 "),
    ("2026 Indy Property Guide · Powered by ", "2026 "),
    # --- header lockup: name + descriptor tagline (not a second brand) ---
    ('<span class="site-name">Indy Property Guide</span>',
     '<span class="site-name">Your Realty Link</span>'),
    ('<span class="site-tagline">Powered by Your Realty Link</span>',
     '<span class="site-tagline">Central Indiana Real Estate</span>'),
    # --- catch-all: every remaining standalone brand name ---
    ("Indy Property Guide", "Your Realty Link"),
]

# Redundancy patterns that must NOT survive the rename.
BAD = [
    "Your Realty Link · Powered by Your Realty Link",
    "Your Realty Link &middot; Powered by Your Realty Link",
    "Your Realty Link and Your Realty Link",
    "Your Realty Link, operated by Your Realty Link",
    "Indy Property Guide",  # nothing should remain
]

files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if f.endswith(".html"):
            files.append(os.path.join(dp, f))

rule_hits = {i: 0 for i in range(len(RULES))}
files_changed = 0
bad_after = {}

for path in files:
    with open(path, encoding="utf-8") as fh:
        orig = fh.read()
    txt = orig
    for i, (old, new) in enumerate(RULES):
        c = txt.count(old)
        if c:
            rule_hits[i] += c
            txt = txt.replace(old, new)
    if txt != orig:
        files_changed += 1
        for b in BAD:
            n = txt.count(b)
            if n:
                bad_after[b] = bad_after.get(b, 0) + n
        if apply:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(txt)

print(("APPLIED" if apply else "DRY RUN") + f":  Indy Property Guide  ->  Your Realty Link")
print(f"html files scanned: {len(files)}   files changed: {files_changed}\n")
print("per-rule replacements:")
for i, (old, new) in enumerate(RULES):
    label = old if len(old) <= 52 else old[:49] + "..."
    print(f"  {rule_hits[i]:>5}  {label}")
print("\nredundancy / leftover scan (must all be 0):")
if bad_after:
    for b, n in bad_after.items():
        print(f"  !!!! {n:>4}  {b}")
else:
    print("  clean - no redundant phrases, no leftover 'Indy Property Guide'")
if not apply:
    print("\nDRY RUN - nothing written. Re-run with --apply.")
