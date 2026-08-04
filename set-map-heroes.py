#!/usr/bin/env python3
"""set-map-heroes.py — put a dark street-map behind each city & county page hero.

For every city page (cities/*/*/) and county page (counties/*/) that has a
matching hero map in assets/img/citymaps/{heroes,counties}/, this switches the
hero to `class="page-hero has-map"` with a `--hero-img` background (the .has-map
CSS supplies the readable scrim). Idempotent and HTML-only — it changes only the
one <section class="page-hero"> tag per page, no whitespace reflow. Pages that
already carry a real photo hero (`has-photo`) are left untouched.

    python3 set-map-heroes.py            # wire every page that has a hero map
    python3 set-map-heroes.py --list     # list pages currently using a map hero
    python3 set-map-heroes.py --remove   # revert all map heroes (navy gradient)
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# Geoapify's free tier needs visible attribution; the baked-in map watermark is
# cropped by the hero, so we add a small credit to the footer of map pages.
CREDIT = ('<span class="map-credit">Maps &copy; '
          '<a href="https://www.geoapify.com/" target="_blank" rel="noopener nofollow">Geoapify</a>, &copy; '
          '<a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener nofollow">OpenStreetMap</a></span>')
CREDIT_ANCHOR = "Broker/Owner</span>"


def targets():
    out = []
    for p in glob.glob(os.path.join(ROOT, "cities", "*", "*", "index.html")):
        key = os.path.basename(os.path.dirname(p)).replace("-indiana-real-estate", "").replace("-indianapolis-real-estate", "")
        out.append((p, f"/assets/img/citymaps/heroes/{key}-hero.webp"))
    for p in glob.glob(os.path.join(ROOT, "counties", "*", "index.html")):
        key = os.path.basename(os.path.dirname(p)).replace("-indiana-real-estate", "")
        out.append((p, f"/assets/img/citymaps/counties/{key}-hero.webp"))
    return out


def normalize(html):
    """Return the hero to its plain state (strip any has-map wiring + credit)."""
    html = html.replace('<section class="page-hero has-map"', '<section class="page-hero"')
    html = re.sub(r'(<section class="page-hero")\s+style="[^"]*--hero-img[^"]*"', r'\1', html)
    html = re.sub(r'\s*<span class="map-credit">.*?</span>', '', html, flags=re.S)
    return html


def apply_one(path, img_url):
    html = open(path, encoding="utf-8").read()
    if 'page-hero has-photo' in html:
        return "skip-photo"                       # a real photo wins
    if 'class="page-hero"' not in html and 'class="page-hero has-map"' not in html:
        return "no-hero"
    html = normalize(html)                        # -> plain class="page-hero" (idempotent re-apply)
    style = "--hero-img: url('%s');" % img_url
    new = html.replace('<section class="page-hero">',
                       '<section class="page-hero has-map" style="%s">' % style, 1)
    if CREDIT_ANCHOR in new:                       # footer map attribution (Geoapify free tier)
        new = new.replace(CREDIT_ANCHOR, CREDIT_ANCHOR + "\n " + CREDIT, 1)
    if new != open(path, encoding="utf-8").read():
        open(path, "w", encoding="utf-8").write(new)
    return "ok"


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--list":
        for p, _ in targets():
            if 'page-hero has-map' in open(p, encoding="utf-8").read():
                print("  " + os.path.relpath(os.path.dirname(p), ROOT))
        return
    if arg == "--remove":
        n = 0
        for p, _ in targets():
            h = open(p, encoding="utf-8").read()
            if 'page-hero has-map' in h:
                open(p, "w", encoding="utf-8").write(normalize(h)); n += 1
        print("reverted %d pages to the gradient." % n); return
    counts = {}
    for p, img in targets():
        if not os.path.exists(os.path.join(ROOT, img.lstrip("/"))):
            counts["no-map"] = counts.get("no-map", 0) + 1; continue
        r = apply_one(p, img); counts[r] = counts.get(r, 0) + 1
    print("map heroes:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
