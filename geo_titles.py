#!/usr/bin/env python3
"""Buyer-intent titles for city and county pages.

Searchers type "<town> indiana homes for sale", so the title leads with that:
  Greenwood, IN Homes for Sale & Real Estate | Your Realty Link
  Broad Ripple, Indianapolis Homes for Sale | Your Realty Link   (Indianapolis neighborhoods)
  Jennings County, IN Homes for Sale & Real Estate                (suffix dropped when it would run long)
Google already shows "Your Realty Link" as the site name above each result, so the
" | Your Realty Link" suffix is dropped only when keeping it would pass MAX_LEN.

Run directly to retitle every existing city/county page (title, og:title, twitter:title).
Idempotent. build_city.py imports geo_title() so new city pages match.
"""
import glob, html, re

SUFFIX = " | Your Realty Link"
MAX_LEN = 62


def geo_title(name, kind="Indiana"):
    """name: display name (may contain HTML entities). kind: 'Indiana', 'Indianapolis' or 'County'."""
    if kind == "Indianapolis":
        base = f"{name}, Indianapolis Homes for Sale"
    elif kind == "County":
        base = f"{name} County, IN Homes for Sale &amp; Real Estate"
    else:
        base = f"{name}, IN Homes for Sale &amp; Real Estate"
    full = base + SUFFIX
    return full if len(html.unescape(full)) <= MAX_LEN else base


OLD = re.compile(r"<title>(.+?) (Indiana|Indianapolis) Real Estate \| Your Realty Link</title>")


def retitle(path):
    s = open(path, encoding="utf-8", newline="").read()
    m = OLD.search(s)
    if not m:
        return False
    name, kind = m.group(1), m.group(2)
    if path.startswith("counties/"):
        name, kind = re.sub(r" County$", "", name), "County"
    old_title = m.group(0)[len("<title>"):-len("</title>")]
    new_title = geo_title(name, kind)
    n_before = s.count(old_title)
    s = s.replace(f"<title>{old_title}</title>", f"<title>{new_title}</title>", 1)
    s = s.replace(f'property="og:title" content="{old_title}"', f'property="og:title" content="{new_title}"')
    s = s.replace(f'name="twitter:title" content="{old_title}"', f'name="twitter:title" content="{new_title}"')
    open(path, "w", encoding="utf-8", newline="").write(s)
    return (old_title, new_title, n_before - s.count(old_title))


if __name__ == "__main__":
    changed = 0
    for p in sorted(glob.glob("cities/*/*/index.html") + glob.glob("counties/*/index.html")):
        r = retitle(p)
        if r:
            changed += 1
            print(f"{r[2]}x  {html.unescape(r[1])}  ({len(html.unescape(r[1]))})")
    print(f"retitled {changed} pages")
