#!/usr/bin/env python3
"""Swap Google Fonts for the self-hosted copies on every page. Idempotent.

Inter + Playfair Display now live in /assets/fonts/ (same files Google served; see
the @font-face block at the top of assets/css/style.css). Loading them from our own
origin saves mobile visitors two extra connections (fonts.googleapis.com for the CSS,
then fonts.gstatic.com for the files) and lets the two fonts every page needs arrive
alongside style.css, which removes most of the font-swap layout shift PageSpeed
flagged (CLS 0.2+ on community/contact pages, Nov 2026).

For each page that links /assets/css/style.css, this removes:
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    any Google Fonts stylesheet link for Inter / Playfair Display (async preload +
    <noscript> fallback, or a plain render-blocking <link rel="stylesheet">)
and puts PRELOAD (below) where the first of those tags was, so the FONTS grab range
(first font tag -> style.css link, copied out of index.html by the generators) keeps
the same shape. Google Fonts links that request any other family (e.g. the Libre
Franklin social-card templates) are left alone, as are pages without style.css.

Runs in the GitHub Actions after the generators (next to inject_hero_preload.py).

    python3 inject_fonts.py          # apply
    python3 inject_fonts.py --check  # report only
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_FILES = ["/assets/fonts/inter-latin.woff2", "/assets/fonts/playfair-display-latin.woff2"]
PRELOAD = [f'<link rel="preload" href="{u}" as="font" type="font/woff2" crossorigin>' for u in FONT_FILES]

PRECONNECT = re.compile(r'[ \t]*<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"(?: crossorigin(?:="[^"]*")?)?>[ \t]*\r?\n?')
# async pattern: <link rel="preload" as="style" href="GF" onload="..."><noscript><link rel="stylesheet" href="GF"></noscript>
GF_ASYNC = re.compile(r'[ \t]*<link rel="preload" as="style" href="(https://fonts\.googleapis\.com/css2\?[^"]+)"[^>]*>'
                      r'(?:<noscript><link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]+"></noscript>)?[ \t]*\r?\n?')
# plain stylesheet, either attribute order
GF_SHEET = re.compile(r'[ \t]*<link (?:rel="stylesheet" href="(https://fonts\.googleapis\.com/css2\?[^"]+)"|href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet")>[ \t]*\r?\n?')
OURS = re.compile(r'family=(Inter|Playfair\+Display)[:&]')


def only_site_families(url):
    fams = re.findall(r'family=([^:&]+)', url)
    return bool(fams) and all(f in ("Inter", "Playfair+Display") for f in fams)


def convert(s):
    if "/assets/css/style.css" not in s or "fonts.googleapis.com" not in s:
        return s
    hits = []
    for m in GF_ASYNC.finditer(s):
        if only_site_families(m.group(1)):
            hits.append((m.start(), m.end()))
    for m in GF_SHEET.finditer(s):
        if only_site_families(m.group(1) or m.group(2)):
            hits.append((m.start(), m.end()))
    if not hits:
        return s  # nothing we own (or another family is mixed in) -> leave the page alone
    hits += [(m.start(), m.end()) for m in PRECONNECT.finditer(s)]
    hits.sort()
    first = hits[0][0]
    line = s[first:hits[0][1]]
    indent = re.match(r'[ \t]*', line).group(0)
    nl = "\r\n" if "\r\n" in line else "\n"
    have_preload = all(p in s for p in PRELOAD)
    block = "" if have_preload else "".join(indent + p + nl for p in PRELOAD)
    out, pos = [], 0
    for a, b in hits:
        if a < pos:
            continue
        out.append(s[pos:a])
        if a == first:
            out.append(block)
        pos = b
    out.append(s[pos:])
    return "".join(out)


def main():
    check = "--check" in sys.argv
    changed = 0
    left = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if not d.startswith(".") and d != "node_modules"]
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dp, fn)
            s = open(p, encoding="utf-8", newline="").read()
            if 'http-equiv="refresh"' in s:
                continue
            new = convert(s)
            if new != s:
                changed += 1
                if not check:
                    open(p, "w", encoding="utf-8", newline="").write(new)
            if "fonts.googleapis.com" in new and "/assets/css/style.css" in new:
                left.append(os.path.relpath(p, ROOT))
    print(f"{'would update' if check else 'updated'} {changed} pages to self-hosted fonts")
    if left:
        print(f"{len(left)} page(s) still reference Google Fonts (other families, left as is):")
        for r in left[:20]:
            print("  ", r)


if __name__ == "__main__":
    main()
