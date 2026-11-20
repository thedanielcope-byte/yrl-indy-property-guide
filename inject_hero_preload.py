#!/usr/bin/env python3
"""Preload each page's hero background image so it paints sooner on mobile.

City, county and many service pages set their hero as a CSS background
(`style="--hero-img: url('...')"` or `image-set(...)`), which the browser only
discovers after style.css loads. PageSpeed (Nov 2026) showed the Carmel city page's
LCP at 13.6s on mobile for exactly this reason. This adds

    <!-- HERO-PRELOAD --><link rel="preload" as="image" href="..." fetchpriority="high"><!-- /HERO-PRELOAD -->

to the <head>, ABOVE the first font preload (the self-hosted font block from
inject_fonts.py; older pages: the fonts.googleapis.com preconnect). Generators copy the
range from that first font tag to the style.css link out of index.html (the FONTS grab),
so page-specific tags must sit outside it.

Marker-wrapped and idempotent: each run strips the old tag and re-adds it from the
page's current hero, so a changed hero image is picked up. Runs in the GitHub
Actions after inject_favicon.py.

    python3 inject_hero_preload.py          # apply
    python3 inject_hero_preload.py --check  # report only
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
START, END = "<!-- HERO-PRELOAD -->", "<!-- /HERO-PRELOAD -->"
HERO = re.compile(r'<section class="page-hero[^"]*"[^>]*--hero-img:\s*([^;"]+)')
URL = re.compile(r"""(/[^'")\s]+\.(?:webp|avif|jpe?g|png))""")
STRIP = re.compile(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n", re.S)
ANCHORS = ('<link rel="preload" href="/assets/fonts/',            # self-hosted fonts (Nov 2026)
           '<link rel="preconnect" href="https://fonts.googleapis.com">')  # older pages


def main():
    check = "--check" in sys.argv
    done = skipped = 0
    for f in sorted(glob.glob("**/index.html", recursive=True)):
        if f.startswith(("node_modules/", ".git/")):
            continue
        s = open(f, encoding="utf-8").read()
        if 'http-equiv="refresh"' in s:
            continue
        base = STRIP.sub("", s)
        m = HERO.search(base)
        if not m:
            if base != s and not check:
                open(f, "w", encoding="utf-8").write(base)
            continue
        u = URL.search(m.group(1))
        if not u:
            print("SKIP", f, "hero value not parsed:", m.group(1)[:60]); skipped += 1
            continue
        href = u.group(1)
        if re.search(r'<link rel="preload" as="image"[^>]*href="' + re.escape(href) + '"', base):
            continue  # page already preloads it by hand
        tag = f'{START}<link rel="preload" as="image" href="{href}" fetchpriority="high">{END}'
        i = next((j for j in (base.find(a) for a in ANCHORS) if j >= 0), -1)
        if i < 0:
            i = base.find("</head>")
        if i >= 0:
            i = base.rfind("\n", 0, i) + 1  # start of that line, so the tag gets its own line
            new = base[:i] + tag + "\n" + base[i:]
        else:
            print("SKIP", f, "no <head> anchor"); skipped += 1
            continue
        if new != s:
            done += 1
            if not check:
                open(f, "w", encoding="utf-8").write(new)
    print(f"{'would update' if check else 'updated'} {done} pages with a hero preload, skipped {skipped}")


if __name__ == "__main__":
    main()
