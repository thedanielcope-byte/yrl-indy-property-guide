#!/usr/bin/env python3
"""
inject_related_posts.py — add a "More Articles" cross-link block to every blog post
so no post is an internal-linking orphan. The existing per-post "Related Posts"
sidebar is asymmetric (some posts are never anyone's target), leaving ~26 posts with
only the blog index linking to them.

Fix: order all posts by (category, title) and give each post a block linking to the
NEXT 4 posts in that global order (cyclically). Because the list is category-sorted,
those 4 are almost always same-category; because it's a full cycle, EVERY post is the
target of exactly 4 other posts → every post gains inbound links, including the
singleton-category posts. Marker-wrapped (<!-- MORE-ARTICLES -->), idempotent,
inserted before the author box. Reuses .city-grid/.city-card (no new CSS).

Head/body-safe (operates on deployed HTML; no Supabase fetch). Re-run any time.
NOTE: build-blog.py regenerates posts from Supabase and would drop this block, so
re-run this after any blog rebuild (or port the block into build-blog.py).

Usage: python3 inject_related_posts.py [--dry]
"""
import glob, os, re, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
START, END = "<!-- MORE-ARTICLES -->", "<!-- /MORE-ARTICLES -->"
ANCHOR = '<div class="author-box">'


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def main():
    posts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "blog", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(f))
        s = open(f, encoding="utf-8").read()
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        cat = re.search(r'<span class="category-badge">([^<]*)</span>', s)
        title = text(h1.group(1)) if h1 else slug.replace("-", " ").title()
        posts.append({"slug": slug, "file": f, "title": title,
                      "cat": html.unescape(cat.group(1)).strip() if cat else "News", "html": s})

    posts.sort(key=lambda p: (p["cat"].lower(), p["title"].lower()))
    n = len(posts)
    injected = no_anchor = 0
    for i, p in enumerate(posts):
        rel = [posts[(i + k) % n] for k in range(1, 5)]  # next 4, cyclic
        cards = "\n".join(
            ' <a href="/blog/%s/" class="city-card">%s <span class="arrow">&rsaquo;</span></a>'
            % (r["slug"], html.escape(r["title"], quote=False)) for r in rel)
        blk = (
            '%s\n <section class="section" style="padding-top:0;">\n <div class="container" style="max-width:900px;">\n'
            ' <h2>More Central Indiana Real Estate Reading</h2>\n'
            ' <div class="city-grid">\n%s\n </div>\n'
            ' <p style="margin-top:14px;"><a href="/blog/">Browse the full blog &rarr;</a></p>\n'
            ' </div>\n </section>\n %s\n ' % (START, cards, END))
        s = p["html"]
        if START in s:
            s = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: blk.strip(), s, flags=re.S)
        elif ANCHOR in s:
            s = s.replace(ANCHOR, blk + ANCHOR, 1)
        else:
            no_anchor += 1
            continue
        if s != p["html"]:
            injected += 1
            if not DRY:
                open(p["file"], "w", encoding="utf-8").write(s)

    tag = " (dry-run)" if DRY else ""
    print("related-posts blocks%s — posts updated: %d/%d | no anchor: %d" % (tag, injected, n, no_anchor))


if __name__ == "__main__":
    main()
