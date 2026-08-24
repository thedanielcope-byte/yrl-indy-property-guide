#!/usr/bin/env python3
"""Build blog posts authored in the YRL hub admin (Supabase `blog_posts`).

Reads published + due posts from Supabase, renders each into blog/<slug>/index.html
using the SAME head/header/footer/CSS as the hand-authored posts, and refreshes the
broker-post cards on blog/index.html (between the broker:start/end markers).

Public data only (anon key + RLS: status='published' AND publish_at <= now()), so this
is safe to run in CI. Run: python3 build-blog.py
"""
import os, re, html, json, urllib.request, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "blog", "what-is-my-home-worth-in-indianapolis", "index.html")
BLOG_INDEX = os.path.join(ROOT, "blog", "index.html")
CID = "cf007287-a76c-4c9a-bd33-051816db6322"
SB_URL = "https://wdvolamasztetwpitbwg.supabase.co"
SB_KEY = os.environ.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indkdm9sYW1hc3p0ZXR3cGl0YndnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3Nzc2MTYsImV4cCI6MjA5MTM1MzYxNn0.uiGIaZwr88ZNtAobfSV-axlpXB3sos2Rcw3FiFm6JO8")

src = open(TEMPLATE, encoding="utf-8").read()

def grab(pattern, s, flags=re.DOTALL):
    m = re.search(pattern, s, flags)
    if not m:
        raise SystemExit("Could not extract from template: " + pattern[:40])
    return m.group(0)

HEAD_ASSETS = grab(r'<link rel="preconnect"[^\n]*googleapis.*?</style>', src)
HEADER      = grab(r'<header class="site-header">.*?</header>', src)
TAIL        = grab(r'<footer class="site-footer">.*\Z', src)

def esc(s):
    return html.escape(str(s or ""), quote=True)

def slugify(s):
    s = re.sub(r'<[^>]+>', '', s or '')
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s or 'section'

def fetch_posts():
    url = (f"{SB_URL}/rest/v1/blog_posts?client_id=eq.{CID}"
           f"&status=eq.published&order=publish_at.desc&select=*")
    req = urllib.request.Request(url, headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.load(r)
    now = datetime.datetime.now(datetime.timezone.utc)
    live = []
    for p in rows:
        pa = p.get("publish_at")
        try:
            due = datetime.datetime.fromisoformat(pa.replace("Z", "+00:00")) <= now if pa else True
        except Exception:
            due = True
        if due:
            live.append(p)
    return live

VAL_CARD = ('<div class="sidebar-card">\n <div class="sidebar-card-header">Free Home Valuation</div>\n'
            ' <div class="sidebar-card-body">\n <p>Find out what your Central Indiana home is worth &mdash; no obligation.</p>\n'
            ' <a href="/services/free-home-valuation/" class="btn btn-primary btn-sm btn-full">Get My Valuation &rarr;</a>\n </div>\n</div>')
SEARCH_CARD = ('<div class="sidebar-card">\n <div class="sidebar-card-header">Search Indianapolis Homes</div>\n'
               ' <div class="sidebar-card-body">\n <p>Browse all active MLS listings in Central Indiana.</p>\n'
               ' <a href="https://yourrealtylink.com/property-search" class="btn btn-primary btn-sm btn-full" target="_blank" rel="noopener">Search All Listings &rarr;</a>\n </div>\n</div>')

def author_box(name):
    name = name or "Your Realty Link"
    initials = "".join(w[0] for w in re.findall(r"[A-Za-z]+", name)[:2]).upper() or "YRL"
    return (f'<div class="author-box">\n <div class="author-avatar">{esc(initials)}</div>\n'
            f' <div class="author-info">\n <h4>{esc(name)}</h4>\n'
            f' <p class="author-title">Your Realty Link &mdash; Central Indiana Real Estate</p>\n'
            f' <p>Your Realty Link is a local boutique brokerage serving buyers and sellers across Indianapolis and Central Indiana, led by Principal Broker Janet Giles-Schultz. '
            f'<a href="https://yourrealtylink.com" target="_blank" rel="noopener">Learn more &rarr;</a></p>\n'
            f' <p style="margin-top:8px;font-size:13px;">&#128222; <a href="tel:3179977404">317-997-7404</a> &nbsp;|&nbsp; <a href="mailto:info@yourrealtylink.com">info@yourrealtylink.com</a></p>\n </div>\n</div>')

def anchor_h2s(body):
    """Add id="" to each <h2> (for the TOC) and collect (id, text)."""
    toc = []
    def repl(m):
        inner = m.group(2)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        sid = slugify(text)
        toc.append((sid, text))
        attrs = m.group(1) or ""
        if "id=" in attrs:
            return m.group(0)
        return f'<h2{attrs} id="{sid}">{inner}</h2>'
    out = re.sub(r'<h2([^>]*)>(.*?)</h2>', repl, body or "", flags=re.DOTALL)
    return out, toc

def toc_html(toc):
    if len(toc) < 2:
        return ""
    lis = "\n".join(f' <li><a href="#{i}">{esc(l)}</a></li>' for i, l in toc)
    return f'<div class="toc">\n <h4>In This Article</h4>\n <ol>\n{lis}\n </ol>\n</div>'

def faq_block(faqs):
    faqs = [f for f in (faqs or []) if f.get("q")]
    if not faqs:
        return ""
    rows = "\n".join(
        f' <details class="faq-item"><summary>{esc(f["q"])}</summary><div class="faq-answer"><p>{esc(f.get("a",""))}</p></div></details>'
        for f in faqs)
    return f'\n <!-- FAQ -->\n <h2 id="faq">Frequently Asked Questions</h2>\n{rows}'

def faq_schema(faqs):
    faqs = [f for f in (faqs or []) if f.get("q")]
    if not faqs:
        return ""
    items = ",\n ".join(
        f'{{ "@type": "Question", "name": "{esc(f["q"])}", "acceptedAnswer": {{ "@type": "Answer", "text": "{esc(f.get("a",""))}" }} }}'
        for f in faqs)
    return ('<script type="application/ld+json">\n'
            '{ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [\n '
            + items + '\n] }\n</script>')

def article_schema(p, url, date_pub):
    return ('<script type="application/ld+json">\n{\n "@context": "https://schema.org",\n'
            ' "@type": "Article",\n'
            f' "headline": "{esc(p["title"])}",\n'
            f' "description": "{esc(p.get("excerpt",""))}",\n'
            f' "author": {{ "@type": "Organization", "name": "{esc(p.get("author") or "Your Realty Link")}" }},\n'
            ' "publisher": { "@type": "Organization", "name": "Your Realty Link", "logo": { "@type": "ImageObject", "url": "/assets/img/yrl-logo.png" } },\n'
            f' "datePublished": "{date_pub}",\n "dateModified": "{date_pub}",\n'
            f' "mainEntityOfPage": "{url}"\n}}\n</script>')

def build(p):
    slug = p["slug"]
    url = f'https://janetgiles.com/blog/{slug}/'
    cover = p.get("cover_image") or "/assets/img/yrl-logo.png"
    og_img = cover if cover.startswith("http") else ("https://janetgiles.com" + cover)
    try:
        dt = datetime.datetime.fromisoformat((p.get("publish_at") or "").replace("Z", "+00:00"))
    except Exception:
        dt = datetime.datetime.now(datetime.timezone.utc)
    date_label = dt.strftime("%B %Y")
    date_pub = dt.strftime("%Y-%m-%d")
    author = p.get("author") or "Your Realty Link"
    words = len(re.sub(r'<[^>]+>', ' ', p.get("body_html") or "").split())
    read_min = p.get("read_min") or max(2, round(words / 200))

    body_anchored, toc = anchor_h2s(p.get("body_html") or "")

    lead_img = (f'\n <img src="{esc(cover)}" alt="{esc(p["title"])}" class="post-lead" '
                f'style="width:100%;border-radius:12px;margin:0 0 8px;">') if p.get("cover_image") else ""

    parts = [
        f' <div class="post-meta">\n <span class="category-badge">{esc(p.get("category","News"))}</span>\n'
        f' <span>{esc(date_label)}</span>\n <span>By {esc(author)}</span>\n <span>~{read_min} min read</span>\n </div>',
        lead_img,
        "\n " + body_anchored,
        faq_block(p.get("faqs")),
        '\n <!-- CTA -->\n <div class="cta-block">\n <h3>Thinking About Buying or Selling in Central Indiana?</h3>\n'
        ' <p>Your Realty Link is here to help — no pressure, just local expertise.</p>\n <div class="btn-group">\n'
        ' <a href="/contact/" class="btn btn-white">Contact Us &rarr;</a>\n'
        ' <a href="https://yourrealtylink.com/property-search" class="btn btn-outline" target="_blank" rel="noopener">Search Homes</a>\n </div>\n </div>',
        "\n " + author_box(author),
    ]
    article = '<article class="blog-body">\n' + "\n".join(x for x in parts if x) + '\n </article>'
    aside = '<aside class="blog-sidebar">\n ' + (toc_html(toc) + "\n " if toc_html(toc) else "") + VAL_CARD + "\n " + SEARCH_CARD + '\n </aside>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(p["title"])} | Your Realty Link</title>
 <meta name="description" content="{esc(p.get("excerpt",""))}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{url}">
 <meta property="og:title" content="{esc(p["title"])}">
 <meta property="og:description" content="{esc(p.get("excerpt",""))}">
 <meta property="og:url" content="{url}">
 <meta property="og:type" content="article">
 <meta property="og:image" content="{esc(og_img)}">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:image" content="{esc(og_img)}">
 {article_schema(p, url, date_pub)}
 {faq_schema(p.get("faqs"))}
 {HEAD_ASSETS}
</head>
<body>
{HEADER}
<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container">
 <a href="/">Home</a> <span>&rsaquo;</span> <a href="/blog/">Blog</a> <span>&rsaquo;</span> {esc(p["title"])}
 </div>
</nav>
<section class="page-hero">
 <div class="container">
 <h1>{esc(p["title"])}</h1>
 <p class="hero-sub">{esc(p.get("excerpt",""))}</p>
 <div class="hero-badges">
 <span class="hero-badge">{esc(p.get("category","News"))}</span>
 <span class="hero-badge">By {esc(author)}</span>
 </div>
 </div>
</section>
<div class="container">
 <div class="blog-wrap">
 {article}
 {aside}
 </div>
</div>
{TAIL}
'''

def card_html(p):
    cover = p.get("cover_image") or "/assets/img/yrl-logo.png"
    return (f'<div class="blog-card">\n'
            f' <div class="blog-card-img"><img src="{esc(cover)}" alt="{esc(p["title"])}" loading="lazy"></div>\n'
            f' <div class="blog-card-body">\n'
            f' <div class="blog-card-cat">{esc(p.get("category","News"))}</div>\n'
            f' <h3>{esc(p["title"])}</h3>\n'
            f' <p>{esc(p.get("excerpt",""))}</p>\n'
            f' <a href="/blog/{p["slug"]}/" class="read-more">Read More &rarr;</a>\n'
            f' </div>\n </div>')

def update_index(posts):
    h = open(BLOG_INDEX, encoding="utf-8").read()
    block = "<!--broker:start-->\n" + "\n".join(card_html(p) for p in posts) + "\n<!--broker:end-->"
    if "<!--broker:start-->" in h and "<!--broker:end-->" in h:
        h = re.sub(r'<!--broker:start-->.*?<!--broker:end-->', block, h, flags=re.DOTALL)
    else:
        # first run: insert the marker block right after the grid opens
        h = h.replace('<div class="blog-grid">', '<div class="blog-grid">\n' + block, 1)
    open(BLOG_INDEX, "w", encoding="utf-8").write(h)

def main():
    posts = fetch_posts()
    for p in posts:
        d = os.path.join(ROOT, "blog", p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build(p))
        print(f"  /blog/{p['slug']}/  — {p['title']}")
    update_index(posts)
    print(f"Done. {len(posts)} published post(s) built.")

if __name__ == "__main__":
    main()
