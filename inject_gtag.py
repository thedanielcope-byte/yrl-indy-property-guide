#!/usr/bin/env python3
"""
inject_gtag.py — add the Google Analytics 4 gtag.js snippet to the <head> of every
page site-wide. Idempotent: skips a page that already has the tag. Inserted right
after the <meta charset> line (keeps charset first, tag as high in <head> as Google
recommends).

Skips redirect stubs (meta-refresh) — they navigate away instantly, so a tag there
would never fire (and would risk double-counting the destination). Skips node_modules.

The snippet is ALSO baked into index.html's <head>, which most generators clone their
header from — so newly generated pages inherit it. Re-run this after a large generator
run to catch any page built from a scratch template (same convention as inject_idx.py).

Usage: python3 inject_gtag.py [--dry]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
GA_ID = "G-SNV86NLT23"
MARKER = "<!-- Google tag (gtag.js) -->"

BLOCK = (
    ' <!-- Google tag (gtag.js) -->\n'
    ' <script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
    ' <script>\n'
    ' window.dataLayer = window.dataLayer || [];\n'
    ' function gtag(){dataLayer.push(arguments);}\n'
    " gtag('js', new Date());\n"
    " gtag('config', '%s');\n"
    ' </script>\n'
) % (GA_ID, GA_ID)

CHARSET_RE = re.compile(r'(<meta\s+charset=["\']?[^>\'"]+["\']?\s*/?>\s*\n)', re.I)
HEAD_RE = re.compile(r'(<head[^>]*>\s*\n)', re.I)


def main():
    added = have = stub = skipped = no_head = 0
    for dp, dns, fns in os.walk(ROOT):
        if ".git" in dp or "node_modules" in dp:
            continue
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            s = open(path, encoding="utf-8").read()
            if MARKER in s or ("gtag/js?id=" + GA_ID) in s:
                have += 1
                continue
            if 'http-equiv="refresh"' in s:
                stub += 1
                continue
            if CHARSET_RE.search(s):
                s2 = CHARSET_RE.sub(lambda m: m.group(1) + BLOCK, s, count=1)
            elif HEAD_RE.search(s):
                s2 = HEAD_RE.sub(lambda m: m.group(1) + BLOCK, s, count=1)
            else:
                no_head += 1
                print("  ! no <head>: " + os.path.relpath(path, ROOT))
                continue
            if s2 != s:
                added += 1
                if not DRY:
                    open(path, "w", encoding="utf-8").write(s2)
            else:
                skipped += 1

    tag = " (dry-run)" if DRY else ""
    print("\ngtag%s — added: %d | already had it: %d | redirect stubs skipped: %d | no <head>: %d"
          % (tag, added, have, stub, no_head))


if __name__ == "__main__":
    main()
