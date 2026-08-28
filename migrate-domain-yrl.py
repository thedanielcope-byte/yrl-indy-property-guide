#!/usr/bin/env python3
"""
Domain migration: janetgiles.com -> yourrealtylink.com (domain-only, no rebrand).
Third domain move for this same GitHub-Pages SEO site
(indypropertyguide.com -> janetgiles.com -> yourrealtylink.com).

Swaps every hardcoded domain reference (canonicals, og:url, JSON-LD url/item,
sitemap <loc>, robots.txt, any absolute janetgiles.com hrefs) and the GitHub
Pages CNAME file. Brand text is untouched.

NOTE: this only swaps the DOMAIN. The separate `remap_yrl_links.py` handles the
outbound yourrealtylink.com links (property-search / /content/*) that become dead
when Agent3000 is retired. Run BOTH at cutover.

DRY RUN by default — prints what would change, writes nothing.
Apply with:   python3 migrate-domain-yrl.py --apply

DO NOT apply/push until yourrealtylink.com DNS points at GitHub Pages AND the new
IDX is live/wired — otherwise the site loses its property search.
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = "janetgiles.com"
NEW = "yourrealtylink.com"
EXTS = (".html", ".xml", ".txt", ".js", ".json", ".md")
SKIP_DIRS = {".git", "node_modules", ".next", ".wrangler"}
SKIP_FILES = {"migrate-domain.py", "migrate-domain-yrl.py", "remap_yrl_links.py"}

apply = "--apply" in sys.argv

changed_files, total_occ, per_file = 0, 0, []
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
        if fn == "CNAME" and content.strip() == OLD:
            n = max(n, 1)
        if n == 0:
            continue
        changed_files += 1; total_occ += n
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
print("\nCNAME:", "updated" if apply else f"will change '{OLD}' -> '{NEW}'")
if not apply:
    print("\nDRY RUN — nothing written. Re-run with --apply at cutover.")
