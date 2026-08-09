#!/usr/bin/env python3
"""(Re)build /market-updates/ — the landing hub that lists every Market Updates
post, newest first. Scans the blog for category 'Market Updates', reuses the
site header/footer/CSS, and refreshes the page + sitemap entry. Idempotent."""
import os, re, glob, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "blog", "index.html")

src = open(TPL, encoding="utf-8").read()
def grab(p, s):
    m = re.search(p, s, re.S);
    if not m: raise SystemExit("extract failed: "+p[:30])
    return m.group(0)
HEAD = grab(r'<link rel="preconnect"[^\n]*googleapis.*?</style>', src) if re.search(r'</style>', src) else grab(r'<link rel="stylesheet" href="/assets/css/style\.css[^"]*">', src)
HEADER = grab(r'<header class="site-header">.*?</header>', src)
TAIL = grab(r'<footer class="site-footer">.*\Z', src)

MONTHS={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}
def sortkey(p):
    m=re.search(r'([A-Za-z]+)\s+(\d{4})', p["date"])
    if m and m.group(1) in MONTHS: return (int(m.group(2)), MONTHS[m.group(1)])
    y=re.search(r'(\d{4})', p["date"]); return (int(y.group(1)) if y else 0, 0)

posts=[]
for f in glob.glob(os.path.join(ROOT,"blog","*","index.html")):
    s=open(f,encoding="utf-8").read()
    if not re.search(r'class="category-badge">\s*Market Updates', s) and not re.search(r'class="hero-badge">Market Updates', s):
        continue
    slug=os.path.basename(os.path.dirname(f))
    t=re.search(r"<title>(.*?)</title>",s,re.S); title=html.unescape(t.group(1).split("|")[0].strip()) if t else slug
    d=re.search(r'name="description" content="(.*?)"',s,re.S); desc=html.unescape(d.group(1)) if d else ""
    dl=re.search(r'<span class="hero-badge">((?:January|February|March|April|May|June|July|August|September|October|November|December|Q[1-4])[^<]*)</span>',s)
    date=dl.group(1).strip() if dl else (re.search(r'(\d{4})',slug).group(1) if re.search(r'\d{4}',slug) else "")
    posts.append(dict(slug=slug,title=title,desc=desc,date=date))
posts.sort(key=sortkey, reverse=True)

cards=""
for p in posts:
    img=f'/assets/img/blog/{p["slug"]}.png'
    cards+=(f'\n <a class="blog-card" href="/blog/{p["slug"]}/">\n'
            f'  <div class="blog-card-img"><img src="{img}" alt="{html.escape(p["title"])}" loading="lazy"></div>\n'
            f'  <div class="blog-card-body">\n   <div class="blog-card-cat">Market Updates</div>\n'
            f'   <h3>{html.escape(p["title"])}</h3>\n   <p>{html.escape(p["desc"])}</p>\n'
            f'   <span class="read-more">Read the report &rarr;</span>\n  </div>\n </a>\n')

url="https://janetgiles.com/market-updates/"
page=f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Indianapolis Real Estate Market Updates | Your Realty Link</title>
 <meta name="description" content="Monthly Central Indiana real estate market updates from Your Realty Link — buyer vs seller conditions, price ranges by county, and what to do this month.">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="Indianapolis Real Estate Market Updates | Your Realty Link">
 <meta property="og:description" content="Monthly Central Indiana market updates — where the market stands for buyers and sellers.">
 <meta property="og:url" content="{url}">
 <meta property="og:type" content="website">
 <meta property="og:image" content="https://janetgiles.com/assets/img/blog/market-update.png">
 <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:image" content="https://janetgiles.com/assets/img/blog/market-update.png">
 <script type="application/ld+json">
 {{ "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {{"@type":"ListItem","position":1,"name":"Home","item":"https://janetgiles.com/"}},
  {{"@type":"ListItem","position":2,"name":"Market Updates","item":"{url}"}} ]}}
 </script>
 {HEAD}
</head>
<body>
{HEADER}
<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a> <span>&rsaquo;</span> Market Updates</div></nav>
<section class="page-hero"><div class="container">
 <h1>Central Indiana Market Updates</h1>
 <p class="hero-sub">A fresh read on the Indianapolis-area real estate market each month — buyer vs. seller conditions, price ranges by county, and what it means for your next move.</p>
 <div class="hero-badges"><span class="hero-badge">&#128197; Updated Monthly</span><span class="hero-badge">&#128205; All 17 Central Indiana Counties</span><span class="hero-badge">&#9993;&#65039; Free CMA on request</span></div>
</div></section>
<div class="container" style="padding:32px 0 8px;">
 <p style="max-width:70ch;color:var(--gray,#6e6e70);">Want the exact numbers for your home or neighborhood? A market average never tells your street&rsquo;s story &mdash; <a href="/services/free-home-valuation/">get a free, no-obligation home valuation</a> built on real, recent local sales.</p>
 <div class="blog-grid" style="margin-top:20px;">{cards}
 </div>
</div>
{TAIL}'''
os.makedirs(os.path.join(ROOT,"market-updates"),exist_ok=True)
open(os.path.join(ROOT,"market-updates","index.html"),"w",encoding="utf-8").write(page)
# sitemap
sm=os.path.join(ROOT,"sitemap.xml"); s=open(sm,encoding="utf-8").read()
if url not in s:
    s=s.replace("</urlset>",f"<url>\n  <loc>{url}</loc>\n  <changefreq>monthly</changefreq>\n  <priority>0.8</priority>\n</url>\n</urlset>")
    open(sm,"w",encoding="utf-8").write(s)
print(f"built /market-updates/ hub with {len(posts)} reports:", [p['slug'] for p in posts])
