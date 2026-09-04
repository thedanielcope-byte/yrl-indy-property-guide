#!/usr/bin/env python3
"""
inject_twitter_cards.py — site-wide, idempotent Twitter Card completer.

Every page already has Open Graph tags, so Twitter can fall back to those — but an
explicit, COMPLETE twitter card (card + title + description + image) is the
best-practice signal. Several generators emit only a partial card (card+image, or
card only). This script ensures every page ends up with all four twitter:* tags,
deriving the values from the page's OWN og:* tags so titles/descriptions stay
per-page correct.

Two cases, both handled idempotently (head-only, marker-free):
  - No twitter:card at all  -> insert the full 4-tag block after <meta og:image>.
  - Partial card present     -> insert only the missing twitter:* tags after the
                                existing <meta twitter:card> line.

Usage: python3 inject_twitter_cards.py [--dry]
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv

OG_IMG = re.compile(r'[ \t]*<meta property="og:image" content="[^"]*">[ \t]*\n')
TW_CARD = re.compile(r'[ \t]*<meta name="twitter:card" content="[^"]*">[ \t]*\n')


def content_of(s, pattern):
    m = re.search(pattern, s)
    return m.group(1) if m else None


def derive(s):
    title = (content_of(s, r'<meta property="og:title" content="([^"]*)"')
             or content_of(s, r"<title>(.*?)</title>") or "Your Realty Link")
    title = re.sub(r"\s+", " ", title).strip()
    desc = (content_of(s, r'<meta property="og:description" content="([^"]*)"')
            or content_of(s, r'<meta name="description" content="([^"]*)"') or "")
    img = (content_of(s, r'<meta property="og:image" content="([^"]*)"')
           or "https://yourrealtylink.com/assets/img/og-default.png")
    return title, desc, img


def main():
    files = [f for f in glob.glob("**/index.html", recursive=True) if not f.startswith(".git")]
    full = completed = no_anchor = ok = 0
    for f in files:
        s = orig = open(f, encoding="utf-8", errors="ignore").read()
        title, desc, img = derive(s)
        if "twitter:card" not in s:
            m = OG_IMG.search(s)
            if not m:
                no_anchor += 1
                continue
            block = ('%s'
                     ' <meta name="twitter:card" content="summary_large_image">\n'
                     ' <meta name="twitter:title" content="%s">\n'
                     ' <meta name="twitter:description" content="%s">\n'
                     ' <meta name="twitter:image" content="%s">\n' % (m.group(0), title, desc, img))
            s = s[:m.start()] + block + s[m.end():]
            full += 1
        else:
            # complete a partial card: add only the missing twitter:* tags
            add = ""
            if "twitter:title" not in s:
                add += ' <meta name="twitter:title" content="%s">\n' % title
            if "twitter:description" not in s:
                add += ' <meta name="twitter:description" content="%s">\n' % desc
            if "twitter:image" not in s:
                add += ' <meta name="twitter:image" content="%s">\n' % img
            if not add:
                ok += 1
                continue
            m = TW_CARD.search(s)
            if not m:
                no_anchor += 1
                continue
            s = s[:m.end()] + add + s[m.end():]
            completed += 1

        if s != orig and not DRY:
            open(f, "w", encoding="utf-8").write(s)

    tag = " (dry-run)" if DRY else ""
    print("twitter cards%s — full block added: %d | partial completed: %d | already complete: %d | no anchor: %d"
          % (tag, full, completed, ok, no_anchor))


if __name__ == "__main__":
    main()
