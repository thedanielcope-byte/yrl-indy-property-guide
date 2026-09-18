#!/usr/bin/env python3
"""
build_press.py — Your Realty Link newsroom / press releases.

Reads press-releases.json and writes:
  /press/index.html            — newsroom hub (all releases, newest first) + CollectionPage schema
  /press/<slug>/index.html     — one wire-format release per entry + NewsArticle JSON-LD

Self-contained + idempotent (mirrors glossary.py / build_market_update.py): pulls the
canonical <header> and <footer> and the tail from index.html so nav/footer stay in sync,
reuses the CSS ?v= hash, and keeps sitemap.xml in sync (adds new URLs, refreshes lastmod).

NOTE: builds each <head> from scratch, so run inject_gtag.py afterwards to add the GA4 tag
to the new pages (same convention as the other from-scratch generators).

Usage: python3 build_press.py
"""
import os, re, json, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://yourrealtylink.com"

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
CANON_HDR = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
CANON_FTR = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
TAIL = src[src.index('</footer>') + len('</footer>'):src.index('</body>')]
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)

# Verified from CLAUDE.md. Boilerplate is a DRAFT pending Janet's sign-off.
BOILERPLATE = ("Your Realty Link is a full-service real estate brokerage headquartered in "
  "Indianapolis, Indiana, and a member of the Metropolitan Indianapolis Board of Realtors "
  "(MIBOR). Led by Principal Broker and Owner Janet Giles-Schultz, the independent brokerage "
  "serves buyers, sellers, and investors across Central Indiana.")
CONTACT = dict(name="Janet Giles-Schultz", title="Principal Broker and Owner, Your Realty Link",
               email="janet@yourrealtylink.com", phone="317-997-7404", web="yourrealtylink.com")

def esc(s):
    return html.escape(s, quote=False)

STYLE = """<style>
 .pr-wrap{max-width:760px;margin:0 auto;}
 .pr-wrap h1{font-size:2rem;line-height:1.2;color:#1a1a1a;margin:6px 0 14px;}
 .pr-line{font-size:.78rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#c03926;margin:0 0 12px;}
 .pr-sub{font-size:1.14rem;color:#6e6e70;font-weight:500;line-height:1.5;margin:0 0 26px;}
 .pr-body p{color:#33333a;line-height:1.75;margin:0 0 18px;font-size:1.02rem;}
 .pr-body blockquote{margin:22px 0;padding:2px 0 2px 20px;border-left:3px solid #c03926;color:#1a1a1a;font-size:1.06rem;line-height:1.7;font-style:italic;}
 .pr-body blockquote cite{display:block;margin-top:8px;font-style:normal;font-weight:600;font-size:.95rem;color:#6e6e70;}
 .pr-meta{margin-top:34px;padding-top:22px;border-top:1px solid #e6e6e6;color:#6e6e70;font-size:.95rem;line-height:1.7;}
 .pr-meta h2{font-size:1rem;color:#1a1a1a;margin:18px 0 6px;}
 .pr-meta a{color:#c03926;}
 .pr-end{text-align:center;color:#b0b0b0;letter-spacing:.35em;margin:28px 0 0;font-weight:700;}
 .pr-hublist{list-style:none;padding:0;margin:26px 0 0;display:flex;flex-direction:column;gap:16px;}
 .pr-card{display:block;background:#fff;border:1px solid #e6e6e6;border-radius:12px;padding:22px 24px;text-decoration:none;box-shadow:0 2px 10px rgba(0,0,0,.05);transition:transform .15s,box-shadow .15s;}
 .pr-card:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.10);}
 .pr-card .d{font-size:.8rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#c03926;}
 .pr-card h2{font-size:1.2rem;color:#1a1a1a;margin:6px 0 6px;line-height:1.35;}
 .pr-card p{color:#6e6e70;margin:0;font-size:.98rem;line-height:1.6;}
 .pr-card .r{display:inline-block;margin-top:12px;color:#c03926;font-weight:700;font-size:.92rem;}
 .pr-intro{color:#6e6e70;line-height:1.7;max-width:760px;}
</style>"""

def head(title, desc, canon, schema, ogtype="website"):
    t, d = esc(title), esc(desc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{t}</title>
 <meta name="description" content="{d}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="{canon}">
 <meta property="og:title" content="{t}">
 <meta property="og:description" content="{d}">
 <meta property="og:url" content="{canon}">
 <meta property="og:image" content="{SITE}/assets/img/og-home.jpg">
 <meta property="og:type" content="{ogtype}">
 <meta property="og:site_name" content="Your Realty Link">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:title" content="{t}">
 <meta name="twitter:description" content="{d}">
 <meta name="twitter:image" content="{SITE}/assets/img/og-home.jpg">
 <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400..800;1,400..700&display=swap">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 {STYLE}
</head>
<body>
"""

def render_blocks(blocks, dateline):
    out, first = [], True
    for b in blocks:
        if "p" in b:
            txt = esc(b["p"])
            if first:
                txt = f"<strong>{esc(dateline)} &mdash;</strong> {txt}"
                first = False
            out.append(f"<p>{txt}</p>")
        elif "quote" in b:
            q = b["quote"]
            out.append(f"<blockquote>&ldquo;{esc(q['text'])}&rdquo;<cite>&mdash; {esc(q['attribution'])}</cite></blockquote>")
    return "\n".join(out)

def release_page(r):
    canon = f"{SITE}/press/{r['slug']}/"
    dateline = f"{r['dateline_city']}, {r['date_ap']}"
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": r["headline"], "description": r["meta_desc"],
        "datePublished": r["date"], "dateModified": r["date"],
        "url": canon, "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
        "image": f"{SITE}/assets/img/og-home.jpg",
        "author": {"@type": "Organization", "name": "Your Realty Link", "url": SITE},
        "publisher": {"@type": "Organization", "name": "Your Realty Link",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/yrl-logo.png"}},
    }
    tel = re.sub(r"\D", "", CONTACT["phone"])
    body = f"""{CANON_HDR}
<main>
<section class="section">
 <div class="container">
 <nav class="breadcrumbs"><a href="/">Home</a> &rsaquo; <a href="/press/">Press</a> &rsaquo; <span>{esc(r['headline'])}</span></nav>
 <div class="pr-wrap">
 <p class="pr-line">{esc(r['release_line'])}</p>
 <h1>{esc(r['headline'])}</h1>
 <p class="pr-sub">{esc(r['subhead'])}</p>
 <div class="pr-body">
{render_blocks(r['blocks'], dateline)}
 <p>For more information, visit <a href="{r['cta_url']}">{esc(r['cta_label'])}</a>.</p>
 </div>
 <div class="pr-meta">
 <h2>About Your Realty Link</h2>
 <p>{esc(BOILERPLATE)}</p>
 <h2>Media Contact</h2>
 <p>{esc(CONTACT['name'])}<br>{esc(CONTACT['title'])}<br><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a> &nbsp;|&nbsp; <a href="tel:{tel}">{CONTACT['phone']}</a><br><a href="{SITE}/">{CONTACT['web']}</a></p>
 </div>
 <p class="pr-end">###</p>
 </div>
 </div>
</section>
</main>
{CANON_FTR}
{TAIL}</body>
</html>
"""
    return head(r["meta_title"], r["meta_desc"], canon, schema, ogtype="article") + body

def hub_page(releases):
    canon = f"{SITE}/press/"
    desc = ("Official press releases and news from Your Realty Link, a full-service MIBOR real "
            "estate brokerage serving buyers, sellers, and investors across Central Indiana.")
    items = []
    cards = []
    for i, r in enumerate(releases):
        url = f"/press/{r['slug']}/"
        d = datetime.date.fromisoformat(r["date"]).strftime("%B %-d, %Y")
        items.append({"@type": "ListItem", "position": i + 1, "url": SITE + url, "name": r["headline"]})
        cards.append(
            f'<a class="pr-card" href="{url}"><span class="d">{d}</span>'
            f'<h2>{esc(r["headline"])}</h2><p>{esc(r["subhead"])}</p>'
            f'<span class="r">Read the release &rsaquo;</span></a>')
    schema = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Press & News — Your Realty Link", "description": desc, "url": canon,
        "publisher": {"@type": "Organization", "name": "Your Realty Link", "url": SITE},
        "mainEntity": {"@type": "ItemList", "itemListElement": items},
    }
    body = f"""{CANON_HDR}
<main>
<section class="section">
 <div class="container">
 <nav class="breadcrumbs"><a href="/">Home</a> &rsaquo; <span>Press</span></nav>
 <div class="pr-wrap">
 <h1>Press &amp; News</h1>
 <p class="pr-intro">Official announcements from Your Realty Link — new resources, programs, and milestones from our Central Indiana brokerage. For media inquiries, contact {esc(CONTACT['name'])} at <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>.</p>
 <div class="pr-hublist">
{chr(10).join(cards)}
 </div>
 </div>
 </div>
</section>
</main>
{CANON_FTR}
{TAIL}</body>
</html>
"""
    return head("Press & News | Your Realty Link", desc, canon, schema) + body

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

def update_sitemap(urls):
    sp = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sp):
        return
    sm = open(sp, encoding="utf-8").read()
    today = datetime.date.today().isoformat()
    added = 0
    for u in urls:
        if f"<loc>{u}</loc>" in sm:
            continue
        entry = f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n"
        sm = sm.replace("</urlset>", entry + "</urlset>")
        added += 1
    open(sp, "w", encoding="utf-8").write(sm)
    return added

def main():
    releases = json.load(open(os.path.join(ROOT, "press-releases.json"), encoding="utf-8"))
    releases.sort(key=lambda r: r["date"], reverse=True)
    write("press/index.html", hub_page(releases))
    urls = [f"{SITE}/press/"]
    for r in releases:
        write(f"press/{r['slug']}/index.html", release_page(r))
        urls.append(f"{SITE}/press/{r['slug']}/")
    added = update_sitemap(urls)
    print(f"press — built hub + {len(releases)} release page(s); sitemap +{added} URL(s)")

if __name__ == "__main__":
    main()
