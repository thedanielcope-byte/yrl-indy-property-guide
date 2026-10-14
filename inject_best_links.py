#!/usr/bin/env python3
"""Internal links into the /best/ ranking pages (idempotent, marker-wrapped).

The /best/ pages reach page 1 fast but had 1-6 inbound links each. This adds:
  1. City pages: "<City> in Our Indianapolis Rankings" — every /best/ page whose
     main content links to that city page (a pick or a mention).        <!-- BEST-RANKINGS --> ... <!-- /BEST-RANKINGS -->
  2. /best/ pages: "More Indianapolis-Area Rankings" — all sibling rankings.
                                                   <!-- MORE-RANKINGS --> ... <!-- /MORE-RANKINGS -->
  3. Homepage: one "Popular rankings" line in the School District / Community section.
                                                   <!-- HOME-RANKINGS --> ... <!-- /HOME-RANKINGS -->
Re-run after build_best.py or after adding/regenerating city pages.
"""
import glob, html, re

def read(p): return open(p, encoding="utf-8", newline="").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)
def strip(t): return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()

def upsert(s, start, end, block, place):
    """Replace an existing marker block, else insert via place(s, block_text)."""
    text = f"{start}\n{block}{end}\n"
    if start in s:
        return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n", lambda m: text, s, flags=re.S)
    return place(s, text)

# ---- collect the rankings and the city pages each one features
best = []
for p in sorted(glob.glob("best/*/index.html")):
    s = read(p)
    url = "/" + p[: -len("index.html")]
    h1 = strip(re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1))
    main = s[s.find("<main"): s.find("</main>")]
    cities = sorted(set(re.findall(r'href="(/cities/[^"#?]+/)"', main)))
    best.append(dict(url=url, title=h1, cities=cities, path=p))

def card(href, label):
    return f' <a href="{href}" class="city-card">{html.escape(label, quote=False)} <span class="arrow">&rsaquo;</span></a>\n'

# ---- 1. city pages
featured = {}
for b in best:
    for c in b["cities"]:
        featured.setdefault(c, []).append(b)

def place_city(s, text):
    for anchor, after in (("<!-- /COMPARE-SUBURBS -->\n", True), (" <!-- CITY-COMMUNITIES -->", False),
                          ("<!-- LOCAL-POSTS-START -->", False), ("<!-- CITY-AGENTS -->", False)):
        if anchor in s:
            i = s.index(anchor) + (len(anchor) if after else 0)
            return s[:i] + text + s[i:]
    return None

city_done = city_skip = 0
for c, items in sorted(featured.items()):
    p = c.lstrip("/") + "index.html"
    try:
        s = read(p)
    except FileNotFoundError:
        continue
    m = re.search(r"<title>(.*?)(?:, IN |, Indianapolis | Indiana | Indianapolis )", s)
    name = html.unescape(m.group(1)) if m else "This town"
    block = (' <hr class="divider">\n'
             f' <h2 id="rankings">{html.escape(name, quote=False)} in Our Indianapolis Rankings</h2>\n'
             f' <p>You&rsquo;ll find {html.escape(name, quote=False)} in these Central Indiana guides:</p>\n'
             ' <div class="city-grid">\n' + "".join(card(b["url"], b["title"]) for b in items) +
             ' </div>\n <p>See all <a href="/best/">Indianapolis-area rankings</a>.</p>\n')
    new = upsert(s, "<!-- BEST-RANKINGS -->", "<!-- /BEST-RANKINGS -->", block, place_city)
    if new is None:
        city_skip += 1; print("  no anchor:", p); continue
    if new != s:
        write(p, new); city_done += 1

# ---- 2. sibling links on each /best/ page
best_done = 0
for b in best:
    s = read(b["path"])
    others = [o for o in best if o["url"] != b["url"]]
    block = ('<section class="more-rankings" style="margin-top:36px;">\n'
             '<h2>More Indianapolis-Area Rankings</h2>\n<div class="city-grid">\n' +
             "".join(card(o["url"], o["title"]) for o in others) +
             '</div>\n<p>See all <a href="/best/">Indianapolis-area rankings</a>.</p>\n</section>\n')
    anchor = "</main><!-- /content-main -->"
    new = upsert(s, "<!-- MORE-RANKINGS -->", "<!-- /MORE-RANKINGS -->", block,
                 lambda s, t: s.replace(anchor, t + anchor, 1) if anchor in s else None)
    if new and new != s:
        write(b["path"], new); best_done += 1

# ---- 3. homepage line
HOME_PICKS = [("/best/indianapolis-suburbs-for-families/", "Best suburbs for families"),
              ("/best/most-affordable-indianapolis-suburbs/", "Most affordable suburbs"),
              ("/best/best-indianapolis-suburbs-for-retirees/", "Best suburbs for retirees"),
              ("/best/best-indianapolis-suburbs-for-young-professionals/", "Best areas for young professionals"),
              ("/best/", "All rankings")]
s = read("index.html")
line = (' <p class="home-rankings" style="text-align:center;margin:26px auto 0;max-width:900px;">'
        '<strong>Popular rankings:</strong> ' +
        " &middot; ".join(f'<a href="{u}">{t}</a>' for u, t in HOME_PICKS) + '</p>\n')
anchor = " </div>\n</section>\n\n<!-- ABOUT YRL -->"
new = upsert(s, " <!-- HOME-RANKINGS -->", " <!-- /HOME-RANKINGS -->", line,
             lambda s, t: s.replace(anchor, t + anchor, 1) if anchor in s else None)
home = "updated" if new and new != s else ("unchanged" if new else "NO ANCHOR")
if new and new != s:
    write("index.html", new)

print(f"rankings: {len(best)} | city pages updated: {city_done} (no anchor: {city_skip}) | best pages updated: {best_done} | homepage: {home}")
