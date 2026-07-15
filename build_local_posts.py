#!/usr/bin/env python3
"""Surface tagged blog posts on the geo pages they belong to (build-time, static HTML).

Reads data/local-post-tags.json (post slug -> [geo page paths]) and blog/index.html
(for post title/category/excerpt/image), then injects a "Local News & Updates from
[Place]" section into each geo page between idempotent markers. Re-run any time the
tag index or blog index changes.

Usage:  python3 build_local_posts.py
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TAGS = os.path.join(ROOT, "data", "local-post-tags.json")
BLOG_INDEX = os.path.join(ROOT, "blog", "index.html")
START = "<!-- LOCAL-POSTS-START -->"
END = "<!-- LOCAL-POSTS-END -->"
MAX_CARDS = 6

NBHD_NAME = {
 "mass-ave": "Mass Ave", "herron-morton-place": "Herron-Morton Place",
 "fall-creek-place": "Fall Creek Place", "old-northside": "Old Northside",
 "chatham-arch": "Chatham Arch", "lockerbie-square": "Lockerbie Square",
 "fletcher-place": "Fletcher Place", "geist-reservoir": "Geist Reservoir",
 "eagle-creek": "Eagle Creek", "broad-ripple": "Broad Ripple",
 "meridian-kessler": "Meridian-Kessler", "fountain-square": "Fountain Square",
 "pike-township": "Pike Township", "warren-township": "Warren Township",
}
COMMUNITY_NAME = {
 "holliday-farms-zionsville": "Holliday Farms", "chatham-hills-westfield": "Chatham Hills",
 "bridgewater-club-westfield": "The Bridgewater Club", "sagamore-noblesville": "Sagamore",
 "windermere-fishers": "Windermere", "avalon-fishers": "Avalon of Fishers",
 "village-of-westclay-carmel": "Village of WestClay", "brookshire-carmel": "Brookshire",
 "irishmans-run-zionsville": "Irishman's Run", "kensington-grove-greenwood": "Kensington Grove",
}
CITY_NAME = {"mccordsville": "McCordsville"}

def tc(s):
    return " ".join(w.capitalize() for w in s.split("-"))

def place_name(path):
    p = path.strip("/").split("/")
    if p[0] == "counties":
        return tc(p[1].replace("-county-indiana-real-estate", "")) + " County"
    if p[0] == "cities":
        s = p[2].replace("-indianapolis-real-estate", "").replace("-indiana-real-estate", "")
        return CITY_NAME.get(s, tc(s))
    if p[0] == "neighborhoods":
        s = p[1].replace("-indianapolis", "")
        return NBHD_NAME.get(s, tc(s))
    if p[0] == "communities":
        return COMMUNITY_NAME.get(p[1], tc(p[1]))
    return tc(p[-1])

def parse_blog_index():
    """slug -> {title, cat, excerpt, img, url} from blog/index.html cards."""
    h = open(BLOG_INDEX, encoding="utf-8").read()
    posts = {}
    for m in re.finditer(r'<div class="blog-card">(.*?)</div>\s*</div>', h, re.S):
        blk = m.group(1)
        img = re.search(r'<img src="([^"]+)"', blk)
        cat = re.search(r'<div class="blog-card-cat">([^<]+)</div>', blk)
        title = re.search(r'<h3>(.*?)</h3>', blk, re.S)
        exc = re.search(r'<p>(.*?)</p>', blk, re.S)
        href = re.search(r'href="/blog/([^/]+)/"', blk)
        if not href:
            continue
        posts[href.group(1)] = {
            "img": img.group(1) if img else "",
            "cat": cat.group(1).strip() if cat else "",
            "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else "",
            "excerpt": re.sub(r"\s+", " ", exc.group(1)).strip() if exc else "",
            "url": f"/blog/{href.group(1)}/",
        }
    return posts

def card(p):
    img = f' style="background-image:url(\'{p["img"]}\')"' if p["img"] else ""
    cat = f'<span class="local-post-cat">{html.escape(p["cat"])}</span>' if p["cat"] else ""
    return (f'<a class="local-post-card" href="{p["url"]}">'
            f'<span class="local-post-img"{img}></span>'
            f'<span class="local-post-body">{cat}'
            f'<h3>{p["title"]}</h3><p>{p["excerpt"]}</p>'
            f'<span class="local-post-more">Read more &rarr;</span></span></a>')

def section(place, cards):
    inner = "\n    ".join(cards)
    return (f'\n{START}\n <section class="local-posts">\n'
            f'  <h2>Local News &amp; Updates from {html.escape(place)}</h2>\n'
            f'  <p class="lp-sub">Recent guides and local content from the Your Realty Link team.</p>\n'
            f'  <div class="local-posts-grid">\n    {inner}\n  </div>\n'
            f'  <p class="local-posts-all"><a href="/blog/">Browse the full Indianapolis real estate blog &rarr;</a></p>\n'
            f' </section>\n{END}\n ')

def inject(path, sec_html):
    full = os.path.join(ROOT, path.strip("/"), "index.html")
    if not os.path.isfile(full):
        return "missing"
    h = open(full, encoding="utf-8").read()
    if START in h and END in h:                       # replace existing block
        h = re.sub(re.escape(START) + r".*?" + re.escape(END), sec_html.strip(), h, flags=re.S)
    elif "</main>" in h:                               # insert before </main>
        h = h.replace("</main>", sec_html + "</main>", 1)
    else:
        return "no-anchor"
    open(full, "w", encoding="utf-8").write(h)
    return "ok"

def main():
    tags = {k: v for k, v in json.load(open(TAGS)).items() if not k.startswith("_")}
    posts = parse_blog_index()
    # geo path -> list of post metadata
    geo = {}
    missing_meta = []
    for slug, paths in tags.items():
        if slug not in posts:
            missing_meta.append(slug); continue
        for gp in paths:
            geo.setdefault(gp, []).append(posts[slug])
    results = {}
    for gp, plist in geo.items():
        plist = plist[:MAX_CARDS]
        r = inject(gp, section(place_name(gp), [card(p) for p in plist]))
        results[r] = results.get(r, 0) + 1
    print(f"geo pages updated: {results.get('ok',0)}  | missing pages: {results.get('missing',0)}  | no-anchor: {results.get('no-anchor',0)}")
    if missing_meta:
        print("WARNING — tagged slugs not found in blog/index.html:", missing_meta)
    print(f"total tagged posts: {len(tags)}  | geo pages touched: {len(geo)}")

if __name__ == "__main__":
    main()
