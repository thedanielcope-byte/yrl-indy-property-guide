#!/usr/bin/env python3
"""Inject the newest N blog posts into the homepage "Latest From the Blog" section.

Reads blog/index.html (cards are newest-first) and rewrites the content between
<!-- HOME-RECENT-POSTS --> and <!-- /HOME-RECENT-POSTS --> on index.html. Idempotent.
Run after finalize_new_posts.py (or any time a new post publishes) so the homepage
always shows the latest posts. Post metadata (img/category/title/excerpt/url) comes
straight from the blog-index cards, so no fabrication.

Usage:  python3 build_home_recent_posts.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_INDEX = os.path.join(ROOT, "blog", "index.html")
HOME = os.path.join(ROOT, "index.html")
N = 4
START, END = "<!-- HOME-RECENT-POSTS -->", "<!-- /HOME-RECENT-POSTS -->"

def parse_latest(n):
    h = open(BLOG_INDEX, encoding="utf-8").read()
    posts = []
    for m in re.finditer(r'<div class="blog-card">(.*?)</div>\s*</div>', h, re.S):
        blk = m.group(1)
        href = re.search(r'href="(/blog/[^"]+)"', blk)
        if not href:
            continue
        img = re.search(r'<img src="([^"]+)"', blk)
        cat = re.search(r'blog-card-cat">([^<]+)</div>', blk)
        title = re.search(r'<h3>(.*?)</h3>', blk, re.S)
        exc = re.search(r'<p>(.*?)</p>', blk, re.S)
        posts.append({
            "url": href.group(1),
            "img": img.group(1) if img else "",
            "cat": cat.group(1).strip() if cat else "",
            "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else "",
            "excerpt": re.sub(r"\s+", " ", exc.group(1)).strip() if exc else "",
        })
        if len(posts) >= n:
            break
    return posts

def card(p):
    # title/excerpt come from the blog index already display-ready (do not re-escape)
    img = (f'<img class="hp-img" src="{p["img"]}" alt="{html.escape(p["title"], quote=True)}" loading="lazy">'
           if p["img"] else '<span class="hp-img"></span>')
    cat = f'<span class="hp-cat">{p["cat"]}</span>' if p["cat"] else ''
    return (f'<a class="home-post-card" href="{p["url"]}">{img}'
            f'<span class="hp-body">{cat}<h3>{p["title"]}</h3>'
            f'<p>{p["excerpt"]}</p><span class="hp-more">Read more &rarr;</span></span></a>')

def main():
    posts = parse_latest(N)
    grid = ('\n <div class="home-posts-grid">\n  '
            + "\n  ".join(card(p) for p in posts)
            + '\n </div>\n ')
    idx = open(HOME, encoding="utf-8").read()
    if START not in idx or END not in idx:
        raise SystemExit("HOME-RECENT-POSTS markers not found in index.html")
    idx = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 START + grid + END, idx, flags=re.S)
    open(HOME, "w", encoding="utf-8").write(idx)
    print(f"injected {len(posts)} recent posts:", [p["url"] for p in posts])

if __name__ == "__main__":
    main()
