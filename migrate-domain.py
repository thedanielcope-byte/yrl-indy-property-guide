#!/usr/bin/env python3
"""
Domain migration: indypropertyguide.com -> janetgiles.com (domain-only, no rebrand).

Swaps every hardcoded domain reference (canonicals, og:url, JSON-LD url/item,
sitemap <loc>, robots.txt, internal href links) and the GitHub Pages CNAME file.
The brand name "Indy Property Guide" (with spaces) is left untouched.

DRY RUN by default — prints what would change, writes nothing.
Apply with:   python3 migrate-domain.py --apply

DO NOT apply/push until janetgiles.com DNS points at GitHub Pages, or the live
site goes down (GitHub 301s the old domain to a domain that doesn't resolve yet).
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = "indypropertyguide.com"
NEW = "janetgiles.com"
EXTS = (".html", ".xml", ".txt", ".js", ".json", ".md")
SKIP_DIRS = {".git", "node_modules", ".next", ".wrangler"}
SKIP_FILES = {"migrate-domain.py"}

apply = "--apply" in sys.argv

changed_files = 0
total_occ = 0
per_file = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if fn in SKIP_FILES:
            continue
        if fn != "CNAME" and not fn.endswith(EXTS):
            continue
        path = os.path.join(dirpath, fn)
        try:
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        n = content.count(OLD)
        if fn == "CNAME":
            # CNAME holds just the bare domain
            if content.strip() == OLD:
                n = max(n, 1)
        if n == 0:
            continue
        changed_files += 1
        total_occ += n
        per_file.append((os.path.relpath(path, ROOT), n))
        if apply:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content.replace(OLD, NEW))

per_file.sort(key=lambda x: -x[1])
print(("APPLIED" if apply else "DRY RUN") + f":  {OLD}  ->  {NEW}")
print(f"files affected: {changed_files}   total occurrences: {total_occ}\n")
print("top files by occurrence:")
for rel, n in per_file[:12]:
    print(f"  {n:>4}  {rel}")
if len(per_file) > 12:
    print(f"  ... and {len(per_file)-12} more files")
print("\nCNAME:", "updated" if apply else "will change 'indypropertyguide.com' -> 'janetgiles.com'")
if not apply:
    print("\nThis was a DRY RUN — nothing written. Re-run with --apply when DNS is ready.")
