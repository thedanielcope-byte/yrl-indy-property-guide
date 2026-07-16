#!/usr/bin/env python3
"""
Cache-bust local CSS/JS by content hash.

GitHub Pages serves /assets/css/style.css with cache-control: max-age=600 from a
fixed URL, so browsers and CDN nodes can serve a stale stylesheet against fresh
HTML. Appending ?v=<hash-of-file-contents> gives changed assets a brand-new URL
that no cache can answer from, while unchanged assets keep their URL (and stay
cached, which is what we want).

Run this after ANY change to a file in assets/css or assets/js, then commit:

    python3 bump-assets.py

Idempotent: re-running with no asset changes rewrites nothing.
"""
import hashlib
import os
import re
import sys
from glob import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

ASSETS = [
    "assets/css/style.css",
    "assets/js/site-enhancements.js",
    "assets/js/lead-form.js",
    "assets/js/valuation-form.js",
]

SKIP_PARTS = ("node_modules", os.sep + "reports" + os.sep)


def short_hash(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]


def main():
    os.chdir(ROOT)

    versions = {}
    for rel in ASSETS:
        if not os.path.isfile(rel):
            print(f"  WARN missing asset, skipping: {rel}")
            continue
        versions["/" + rel] = short_hash(rel)

    if not versions:
        print("No assets found — nothing to do.")
        return 1

    print("Asset versions:")
    for path, ver in versions.items():
        print(f"  {ver}  {path}")

    # (href|src)="/assets/...(?v=old)?"  ->  same path with the current hash
    patterns = [
        (
            re.compile(r'((?:href|src)=")' + re.escape(path) + r'(?:\?v=[^"]*)?(")'),
            r"\g<1>" + path + "?v=" + ver + r"\g<2>",
        )
        for path, ver in versions.items()
    ]

    changed = scanned = 0
    for page in glob("**/*.html", recursive=True):
        if any(part in page for part in SKIP_PARTS):
            continue
        scanned += 1
        with open(page, encoding="utf-8") as fh:
            html = fh.read()
        original = html
        for pattern, repl in patterns:
            html = pattern.sub(repl, html)
        if html != original:
            with open(page, "w", encoding="utf-8") as fh:
                fh.write(html)
            changed += 1

    print(f"\nScanned {scanned} HTML files, updated {changed}.")
    if changed == 0:
        print("Everything already on the current hashes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
