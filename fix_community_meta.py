#!/usr/bin/env python3
"""
fix_community_meta.py — one-time, idempotent SEO head-tag fixer for the existing
community detail pages.

build_communities.py preserves already-generated detail pages (so it never
rewrites them), and those pages also carry post-generation injections (IDX slots,
glossary autolinks, ~1,500-word bodies). So instead of regenerating, this script
surgically rewrites ONLY the <head> SEO tags in place, leaving the body intact:

  1. <title> + og:title  -> "{name} Homes for Sale in {city} | Your Realty Link"
     (the city disambiguates same-named communities in different cities and adds a
     geo keyword; when name == city we drop the redundant "in {city}").
  2. meta description     -> a <=160-char template (only when the current one is
     over 160 chars, so any already-good/hand-authored short description is kept).
  3. twitter:card block   -> added after og:type when missing.

The title/description logic mirrors build_communities.py so new pages and fixed
pages stay consistent. Safe to re-run.

Usage: python3 fix_community_meta.py [--dry]
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv


def esc(s):
    return html.escape(str(s or ""), quote=False)  # matches build_communities.esc


def disp(c):
    return c.get("short_name") or c["name"]         # matches build_communities.disp


def seo_for(name, city):
    if name.strip().lower() == city.strip().lower():
        title = "%s Homes for Sale | Your Realty Link" % name
        desc = ("%s, IN: homes for sale, schools, amenities, and price ranges. "
                "Search listings and get a free home valuation with Your Realty Link." % name)
    else:
        title = "%s Homes for Sale in %s | Your Realty Link" % (name, city)
        desc = ("%s in %s, IN: homes for sale, schools, amenities, and price ranges. "
                "Search listings and get a free valuation with Your Realty Link." % (name, city))
        if len(desc) > 160:
            desc = ("%s homes for sale in %s, IN — schools and price ranges. "
                    "Search listings and get a free valuation with Your Realty Link." % (name, city))
    return title, desc


TW_BLOCK = (
    ' <meta name="twitter:card" content="summary_large_image">\n'
    ' <meta name="twitter:title" content="%s">\n'
    ' <meta name="twitter:description" content="%s">\n'
    ' <meta name="twitter:image" content="https://yourrealtylink.com/assets/img/og-default.png">\n'
)


def main():
    data = json.load(open(os.path.join(ROOT, "communities.json"), encoding="utf-8"))
    comms = data["communities"]
    t_fixed = d_fixed = tw_added = missing = 0
    for c in comms:
        idx = os.path.join(ROOT, "communities", c["slug"], "index.html")
        if not os.path.exists(idx):
            missing += 1
            continue
        name, city = disp(c), c["city"]
        title, desc = seo_for(name, city)
        s = orig = open(idx, encoding="utf-8").read()

        # 1) <title> + og:title
        et = esc(title)
        new_s, n = re.subn(r"<title>.*?</title>", "<title>%s</title>" % et, s, count=1, flags=re.S)
        if n and new_s != s:
            t_fixed += 1
        s = new_s
        s = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', r"\g<1>%s\g<2>" % et, s, count=1)

        # 2) meta description — only replace when the current one is too long
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        if m and len(m.group(1)) > 160:
            s = s[:m.start()] + '<meta name="description" content="%s"' % esc(desc) + s[m.end():]
            d_fixed += 1

        # 3) twitter card after og:type (only if missing)
        if "twitter:card" not in s:
            s = re.sub(r'(<meta property="og:type" content="website">\n)',
                       r"\1" + (TW_BLOCK % (et, esc(desc))), s, count=1)
            if "twitter:card" in s:
                tw_added += 1

        if s != orig and not DRY:
            open(idx, "w", encoding="utf-8").write(s)

    tag = " (dry-run)" if DRY else ""
    print("community pages fixed%s:" % tag)
    print("  titles rewritten (added city):   %d" % t_fixed)
    print("  descriptions shortened (>160):   %d" % d_fixed)
    print("  twitter:card added:              %d" % tw_added)
    if missing:
        print("  (skipped %d communities with no built page)" % missing)


if __name__ == "__main__":
    main()
