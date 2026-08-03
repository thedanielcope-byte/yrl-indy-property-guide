#!/usr/bin/env python3
"""Finalize the new glossary blog posts authored in blog-posts-new.json:
   1. render a branded 1200x630 OG/card image per post (headless Chrome)
   2. insert a card at the top of blog/index.html (idempotent)
   3. add each post URL to sitemap.xml (idempotent)
Run AFTER blog-posts-glossary.py has generated the post HTML.
"""
import os, re, json, html, subprocess, base64

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCRATCH = "/private/tmp/claude-501/-Users-danielcope-Library-Mobile-Documents-com-apple-CloudDocs-Claude-YRL/26f905d9-f2dc-48a5-9205-1e23c0b750ad/scratchpad"

posts = json.load(open(os.path.join(ROOT, "blog-posts-new.json"), encoding="utf-8"))
logo = base64.b64encode(open(os.path.join(ROOT, "assets/img/yrl-logo.png"), "rb").read()).decode()

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

def card_title(p):
    # concise title for the image/card: seo_title minus the brand suffix
    t = p["seo_title"].split("|")[0].strip()
    return t

def sub_text(p):
    s = strip_tags(p.get("hero_sub", "")).strip()
    return (s[:96].rsplit(" ", 1)[0] + "…") if len(s) > 100 else s

TPL = """<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,'Segoe UI',Roboto,sans-serif}}
body{{width:1200px;height:630px;overflow:hidden}}
.card{{width:1200px;height:630px;background:linear-gradient(135deg,#1a1a1a 0%,#7a2418 55%,#c03926 100%);
 position:relative;color:#fff;padding:80px 88px;display:flex;flex-direction:column;justify-content:space-between}}
.card:before{{content:'';position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:rgba(255,255,255,.05)}}
.card:after{{content:'';position:absolute;right:120px;bottom:-180px;width:360px;height:360px;border-radius:50%;background:rgba(255,255,255,.04)}}
.top{{position:relative;z-index:2}}
.logo{{height:56px;background:#fff;padding:10px 16px;border-radius:10px}}
.eyebrow{{position:relative;z-index:2;font-size:22px;font-weight:800;letter-spacing:.16em;color:#ffd9d1}}
.title{{position:relative;z-index:2;font-size:{fs}px;line-height:1.05;font-weight:800;max-width:1000px;font-family:'Playfair Display',Georgia,serif;margin:14px 0 20px}}
.sub{{position:relative;z-index:2;font-size:28px;color:#f3d7d1;font-weight:500;max-width:940px}}
.foot{{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.25);padding-top:22px;font-size:22px;color:#f0dcd8}}
.foot b{{color:#fff}}
</style></head><body><div class=card>
<div class=top><img class=logo src="data:image/png;base64,{logo}"></div>
<div>
 <div class=eyebrow>{eyebrow}</div>
 <div class=title>{title}</div>
 <div class=sub>{sub}</div>
</div>
<div class=foot><span>yourrealtylink.com</span><span><b>Your Realty Link</b> · 317-997-7404</span></div>
</div></body></html>"""

def render_image(p):
    t = card_title(p)
    fs = 72 if len(t) <= 34 else (60 if len(t) <= 48 else 50)
    hp = os.path.join(SCRATCH, p["slug"] + ".card.html")
    open(hp, "w").write(TPL.format(logo=logo, eyebrow=html.escape(p["category"].upper()),
                                   title=html.escape(t), sub=html.escape(sub_text(p)), fs=fs))
    out = os.path.abspath(os.path.join(ROOT, "assets/img/blog", p["slug"] + ".png"))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630",
                    "--virtual-time-budget=3000", "--screenshot=" + out, "file://" + hp],
                   capture_output=True)
    return os.path.exists(out)

# 1) images
for p in posts:
    ok = render_image(p)
    print(("  img OK  " if ok else "  img MISSING ") + p["slug"])

# 2) blog index cards (idempotent; newest first)
bi = os.path.join(ROOT, "blog/index.html")
t = open(bi, encoding="utf-8").read()
cards = ""
for p in posts:
    if f'/blog/{p["slug"]}/' in t:
        continue
    alt = strip_tags(p["seo_title"].split("|")[0]).strip().lower()
    cards += (f'\n <div class="blog-card">\n'
              f' <div class="blog-card-img"><img src="/assets/img/blog/{p["slug"]}.png" alt="{alt}" loading="lazy"></div>\n'
              f' <div class="blog-card-body">\n'
              f' <div class="blog-card-cat">{p["category"]}</div>\n'
              f' <h3>{card_title(p)}</h3>\n'
              f' <p>{html.escape(p["meta_desc"])}</p>\n'
              f' <a href="/blog/{p["slug"]}/" class="read-more">Read More →</a>\n'
              f' </div>\n </div>\n')
if cards:
    t = t.replace('<div class="blog-grid">\n', '<div class="blog-grid">\n' + cards, 1)
    open(bi, "w", encoding="utf-8").write(t)
    print("blog index: inserted", cards.count("blog-card\">"), "cards")
else:
    print("blog index: cards already present")

# 3) sitemap (idempotent)
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
block = ""
for p in posts:
    loc = f'https://janetgiles.com/blog/{p["slug"]}/'
    if loc in sm:
        continue
    block += (f"<url>\n  <loc>{loc}</loc>\n  <lastmod>2026-08-03</lastmod>\n"
              f"  <changefreq>monthly</changefreq>\n  <priority>0.7</priority>\n</url>\n")
if block:
    sm = sm.replace("</urlset>", block + "</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
print("sitemap: added", block.count("<url>"), "blog URLs")
