#!/usr/bin/env python3
"""
set-hero.py — add (or replace) a hero photo on any page.

Drop a source photo in, point it at a page, and this does the rest: resizes,
strips EXIF, writes an optimised WebP + JPEG fallback into assets/img/heroes/,
wires the page's hero to use it, and adds a preload hint so the image doesn't
hurt LCP.

Pages without a hero photo keep the existing navy gradient automatically —
nothing breaks, so photos can be added one at a time.

    # add a hero to the Carmel city page
    python3 set-hero.py ~/Photos/carmel-arts-district.jpg cities/hamilton-county/carmel-indiana-real-estate

    # nudge the focal point (default is "center 55%")
    python3 set-hero.py ~/Photos/geist.jpg neighborhoods/geist-reservoir-indianapolis --pos "center 35%"

    # remove a hero photo (page falls back to the gradient)
    python3 set-hero.py --remove cities/hamilton-county/carmel-indiana-real-estate

    # list pages that currently have a hero photo
    python3 set-hero.py --list

After running, commit the new files. (bump-assets.py is only needed for CSS/JS.)
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
HERO_DIR = os.path.join(ROOT, "assets", "img", "heroes")
# Heroes sit under a heavy dark scrim, so fine detail is mostly hidden and they
# tolerate far more compression than a normal photo. These settings land a
# typical hero around 200-300KB, which keeps LCP healthy.
WIDTH = 1600
JPEG_QUALITY = 68
WEBP_QUALITY = 60

PRELOAD_MARK = "<!-- hero-preload -->"


def process_image(src, slug):
    """Resize + strip metadata; write webp and jpg. Returns (webp_rel, jpg_rel)."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow is required:  pip3 install Pillow --break-system-packages")

    os.makedirs(HERO_DIR, exist_ok=True)
    im = Image.open(src)

    # Honour EXIF rotation, then drop all metadata by rebuilding the image.
    try:
        from PIL import ImageOps
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass
    im = im.convert("RGB")

    if im.width > WIDTH:
        h = round(im.height * WIDTH / im.width)
        im = im.resize((WIDTH, h), Image.LANCZOS)

    jpg_path = os.path.join(HERO_DIR, slug + ".jpg")
    webp_path = os.path.join(HERO_DIR, slug + ".webp")
    im.save(jpg_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    im.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=6)

    def kb(p):
        return round(os.path.getsize(p) / 1024)

    print("  %-42s %dx%d  %dKB" % ("assets/img/heroes/%s.webp" % slug, im.width, im.height, kb(webp_path)))
    print("  %-42s %dx%d  %dKB" % ("assets/img/heroes/%s.jpg" % slug, im.width, im.height, kb(jpg_path)))
    if kb(webp_path) > 400:
        print("  NOTE: webp is over 400KB — consider a smaller/simpler source image.")
    return "/assets/img/heroes/%s.webp" % slug, "/assets/img/heroes/%s.jpg" % slug


def strip_hero(html):
    """Remove any existing hero-photo wiring so the page falls back to gradient."""
    html = re.sub(r'\n?\s*' + re.escape(PRELOAD_MARK) + r'.*?\n', '\n', html, flags=re.S)
    html = html.replace('<section class="page-hero has-photo"', '<section class="page-hero"')
    html = re.sub(r'(<section class="page-hero")\s+style="[^"]*--hero-img[^"]*"', r'\1', html)
    return html


def apply_hero(page_dir, webp, jpg, pos):
    path = os.path.join(ROOT, page_dir, "index.html")
    if not os.path.isfile(path):
        sys.exit("No such page: %s" % path)
    html = open(path, encoding="utf-8").read()
    html = strip_hero(html)

    if '<section class="page-hero"' not in html:
        sys.exit("No <section class=\"page-hero\"> found in %s" % page_dir)

    # image-set() lets the browser pick webp and fall back to jpg on its own
    img = ("image-set(url('%s') type('image/webp'), url('%s') type('image/jpeg'))" % (webp, jpg))
    style = '--hero-img: -webkit-%s; --hero-img: %s;' % (img, img)
    if pos:
        style += ' --hero-pos: %s;' % pos

    html = html.replace(
        '<section class="page-hero">',
        '<section class="page-hero has-photo" style="%s">' % style, 1)

    # preload the jpg (universally supported) so the LCP image starts early
    preload = '%s\n <link rel="preload" as="image" href="%s" fetchpriority="high">' % (PRELOAD_MARK, jpg)
    html = html.replace('<link rel="stylesheet" href="/assets/css/style.css">',
                        preload + '\n <link rel="stylesheet" href="/assets/css/style.css">', 1)

    open(path, "w", encoding="utf-8").write(html)
    print("  wired -> %s/index.html" % page_dir)


def list_heroes():
    found = []
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        if any(s in dirpath for s in (".git", "node_modules")):
            continue
        if "index.html" not in filenames:
            continue
        p = os.path.join(dirpath, "index.html")
        if 'page-hero has-photo' in open(p, encoding="utf-8").read():
            found.append(os.path.relpath(dirpath, ROOT))
    if not found:
        print("No pages currently use a hero photo (all using the gradient fallback).")
    else:
        print("%d page(s) with a hero photo:" % len(found))
        for f in sorted(found):
            print("  " + f)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("source", nargs="?", help="path to the source photo")
    ap.add_argument("page", nargs="?", help="page dir, e.g. cities/hamilton-county/carmel-indiana-real-estate")
    ap.add_argument("--pos", default=None, help='focal point, e.g. "center 35%%" (default: center 55%%)')
    ap.add_argument("--slug", default=None, help="output filename stem (default: derived from page)")
    ap.add_argument("--remove", metavar="PAGE", help="remove the hero photo from PAGE")
    ap.add_argument("--list", action="store_true", help="list pages using a hero photo")
    a = ap.parse_args()

    if a.list:
        return list_heroes()

    if a.remove:
        path = os.path.join(ROOT, a.remove, "index.html")
        if not os.path.isfile(path):
            sys.exit("No such page: %s" % path)
        html = open(path, encoding="utf-8").read()
        open(path, "w", encoding="utf-8").write(strip_hero(html))
        print("Removed hero photo from %s (now using the gradient fallback)." % a.remove)
        return

    if not a.source or not a.page:
        ap.print_help()
        sys.exit(1)
    if not os.path.isfile(a.source):
        sys.exit("Source image not found: %s" % a.source)

    page = a.page.strip("/")
    slug = a.slug or re.sub(r'[^a-z0-9]+', '-', page.lower()).strip('-')
    print("Processing hero for /%s/" % page)
    webp, jpg = process_image(a.source, slug)
    apply_hero(page, webp, jpg, a.pos)
    print("Done. Review it locally, then commit the new files.")


if __name__ == "__main__":
    main()
