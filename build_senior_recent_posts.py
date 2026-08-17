#!/usr/bin/env python3
"""Inject the newest 'Senior Real Estate' blog posts into /senior-living/ between
<!-- SENIOR-RECENT-POSTS --> markers. Reads blog/index.html cards (newest-first),
filters by category, renders .sr-post cards. Idempotent — run after any new
senior post publishes (and after build_senior_living.py regenerates the page).
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_INDEX = os.path.join(ROOT, "blog", "index.html")
PAGE = os.path.join(ROOT, "senior-living", "index.html")
CATEGORY = "Senior Real Estate"
N = 6
START, END = "<!-- SENIOR-RECENT-POSTS -->", "<!-- /SENIOR-RECENT-POSTS -->"

def parse(cat, n):
    h = open(BLOG_INDEX, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<div class="blog-card">(.*?)</div>\s*</div>', h, re.S):
        blk = m.group(1)
        c = re.search(r'blog-card-cat">([^<]+)</div>', blk)
        if not c or c.group(1).strip() != cat:
            continue
        href = re.search(r'href="(/blog/[^"]+)"', blk)
        img = re.search(r'<img src="([^"]+)"', blk)
        title = re.search(r'<h3>(.*?)</h3>', blk, re.S)
        exc = re.search(r'<p>(.*?)</p>', blk, re.S)
        if not (href and title):
            continue
        out.append({
            "url": href.group(1),
            "img": img.group(1) if img else "",
            "cat": cat,
            "title": re.sub(r"\s+", " ", title.group(1)).strip(),
            "excerpt": re.sub(r"\s+", " ", exc.group(1)).strip() if exc else "",
        })
        if len(out) >= n:
            break
    return out

def card(p):
    img = (f'<img src="{p["img"]}" alt="{html.escape(p["title"], quote=True)}" loading="lazy">'
           if p["img"] else '<img alt="" loading="lazy">')
    return (f'<a class="sr-post" href="{p["url"]}">{img}'
            f'<span class="b"><span class="cat">{p["cat"]}</span>'
            f'<h4>{p["title"]}</h4><p>{p["excerpt"]}</p>'
            f'<span class="more">Read more &rarr;</span></span></a>')

def main():
    posts = parse(CATEGORY, N)
    grid = ('<div class="sr-blog-grid">\n  ' + "\n  ".join(card(p) for p in posts) + '\n </div>') \
           if posts else '<div class="sr-blog-grid"></div>'
    s = open(PAGE, encoding="utf-8").read()
    if START not in s or END not in s:
        raise SystemExit("markers not found in senior-living/index.html")
    s = re.sub(re.escape(START) + r".*?" + re.escape(END),
               START + "\n " + grid + "\n " + END, s, flags=re.S)
    open(PAGE, "w", encoding="utf-8").write(s)
    print(f"injected {len(posts)} senior posts:", [p["url"] for p in posts])

if __name__ == "__main__":
    main()
