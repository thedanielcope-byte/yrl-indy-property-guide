#!/usr/bin/env python3
"""
Agent landing pages + /agents/ directory generator.

Roster source: agents-roster.json (exported from the YRL hub agent directory).
Run:  python3 agent-pages.py
- writes /agents/<slug>/index.html for every agent
- (re)builds the /agents/ directory hub page with a card per agent
Re-run any time the roster changes.
"""
import os, re, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
AGENTS = json.load(open(os.path.join(ROOT, "agents-roster.json"), encoding="utf-8"))
SEARCH_URL = "https://yourrealtylink.com/property-search"

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
CANON_HDR = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
CANON_FTR = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
TAIL = src[src.index('</footer>') + len('</footer>'):src.index('</body>')]
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)

GRID_CSS = """
 .agent-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(185px,1fr)); gap:22px; margin:8px 0; }
 .agent-card { display:block; text-decoration:none; background:#fff; border:1px solid #e6e6e6; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.05); transition:transform .15s, box-shadow .15s; }
 .agent-card:hover { transform:translateY(-3px); box-shadow:0 6px 20px rgba(0,0,0,.12); text-decoration:none; }
 .agent-card img { width:100%; aspect-ratio:1/1; object-fit:cover; object-position:top center; display:block; background:#ececec; }
 .agent-card .ac-body { padding:13px 15px; }
 .agent-card .ac-name { font-weight:700; color:#1a1a1a; font-size:1rem; }
 .agent-card .ac-title { font-size:.82rem; color:#6e6e70; margin-top:2px; }
 .agent-card .ac-cta { color:#c03926; font-weight:600; font-size:.82rem; margin-top:8px; display:inline-block; }
 .team-photo { width:100%; max-width:920px; display:block; margin:0 auto 22px; border-radius:14px; }
"""

AGENT_CSS = """
 .agent-layout { display:grid; grid-template-columns:300px 1fr; gap:40px; align-items:start; }
 .agent-photo { width:100%; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,.12); display:block; background:#ececec; }
 .agent-contact { margin-top:18px; display:flex; flex-direction:column; gap:10px; }
 .agent-contact a.btn-primary, .agent-contact a.btn-secondary { text-align:center; display:block; }
 .agent-reach { font-size:.9rem; color:#6e6e70; margin-top:10px; line-height:1.9; }
 .chips { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0; }
 .chip { background:#f2f2f2; color:#444; border-radius:20px; padding:6px 14px; font-size:.85rem; }
 @media (max-width:760px){ .agent-layout{ grid-template-columns:1fr; } }
"""

def esc(s): return html.escape(str(s or ""), quote=True)

def slugify(name):
    s = name.lower().replace("&", " ")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def first_name(name):
    return name.replace("&", "and").split()[0]

def bio(a):
    n, first, t = a["name"], first_name(a["name"]), a["title"]
    if a.get("lead"):
        return [f"{n} is the Broker–Owner of Your Realty Link, leading a local boutique team of 20+ agents across Central Indiana. Under Janet's leadership, the brokerage has built its reputation on straight talk, strong marketing, and putting clients first — every single time.",
                "Whether you're buying, selling, or investing anywhere in the Indianapolis metro, Janet and the Your Realty Link team bring deep local knowledge and full MLS access to every transaction."]
    if "Referral" in t:
        return [f"{n} is a referral partner of Your Realty Link. Connect with {first} and the Your Realty Link team to get matched with the right agent for your buying, selling, or investment goals anywhere in Central Indiana."]
    if "Commercial" in t:
        return [f"{n} is a Commercial Broker and leads marketing for Your Realty Link, working with clients on commercial and residential real estate across the Indianapolis metro and Central Indiana. Reach out to {first} to talk through your next move with the local knowledge and full-MLS reach of the Your Realty Link team."]
    return [f"{n} is a REALTOR® with Your Realty Link, helping buyers and sellers across the Indianapolis metro and Central Indiana. Reach out to {first} to start your home search, price your home, or talk through your next move — backed by the local knowledge and full MLS access of the Your Realty Link team."]

def clean_site(url):
    if not url: return None
    u = url.strip()
    label = re.sub(r"^https?://(www\.)?", "", u).rstrip("/")
    if not u.startswith("http"): u = "https://" + u
    return u, label

def card(a):
    return (f'<a href="/agents/{a["slug"]}/" class="agent-card">'
            f'<img src="{a["photo"]}" alt="{esc(a["name"])} — Your Realty Link" width="300" height="300" loading="lazy">'
            f'<div class="ac-body"><div class="ac-name">{esc(a["name"])}</div>'
            f'<div class="ac-title">{esc(a["title"])}</div>'
            f'<span class="ac-cta">View Profile →</span></div></a>')

def hub_page(agents):
    cards = "\n ".join(card(a) for a in agents)
    desc = "Meet the Your Realty Link team — 20+ experienced Central Indiana real estate agents, led by Broker-Owner Janet Giles. Find your agent, view their profile, and start your home search."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Our Agents | Your Realty Link</title>
 <meta name="description" content="{esc(desc)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="https://janetgiles.com/agents/">
 <meta property="og:title" content="Our Agents | Your Realty Link">
 <meta property="og:description" content="{esc(desc)}">
 <meta property="og:url" content="https://janetgiles.com/agents/">
 <meta property="og:type" content="website">
 <script type="application/ld+json">
 {{ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
 {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://janetgiles.com/" }},
 {{ "@type": "ListItem", "position": 2, "name": "Our Agents", "item": "https://janetgiles.com/agents/" }} ] }}
 </script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" rel="stylesheet">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 <style>{GRID_CSS}</style>
</head>
<body>
{CANON_HDR}
<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>›</span> Our Agents</div>
</nav>
<section class="page-hero">
 <div class="container">
 <h1>Our Agents</h1>
 <p class="hero-sub">Meet the Your Realty Link team — a local boutique brokerage of 20+ experienced Central Indiana real estate experts, led by Broker-Owner Janet Giles.</p>
 <div class="hero-badges">
 <span class="hero-badge">🏡 20+ Agents</span>
 <span class="hero-badge">📍 All 17 Central Indiana Counties</span>
 <span class="hero-badge">⭐ 5.0 on Google</span>
 </div>
 </div>
</section>
<main>
 <section class="section">
 <div class="container">
 <p>Our agents are seasoned, tech-savvy, and relentless about getting the right result — whether you're buying your first home, selling a longtime family property, or building an investment portfolio. Click any agent below to view their profile and start your home search with them.</p>
 <div class="agent-grid">
 {cards}
 </div>
 <div class="cta-block" style="margin-top:40px;">
 <h2>Not sure who to reach out to?</h2>
 <p>Tell us what you're looking for and we'll connect you with the right Your Realty Link agent for your goals and your part of Central Indiana.</p>
 <div class="cta-buttons">
 <a href="/contact/" class="btn-primary">Contact Us</a>
 <a href="/schedule/" class="btn-secondary">Schedule a Free Consultation</a>
 <a href="{SEARCH_URL}" target="_blank" rel="noopener" class="btn-secondary">Search Homes</a>
 </div>
 </div>
 </div>
 </section>
</main>
{CANON_FTR}
{TAIL}</body>
</html>
"""

def agent_page(a):
    first = first_name(a["name"])
    tel = re.sub(r"\D", "", a["phone"])
    bio_html = "\n   ".join(f"<p>{esc(p)}</p>" for p in bio(a))
    site = clean_site(a.get("website"))
    site_html = f'<br>Website: <a href="{site[0]}" target="_blank" rel="noopener">{esc(site[1])}</a>' if site else ""
    desc = f'{a["name"]}, {a["title"]} at Your Realty Link — a Central Indiana real estate professional. Search homes, get a free valuation, or contact {first} today.'
    schema = {
        "@context": "https://schema.org", "@type": "RealEstateAgent",
        "name": a["name"], "jobTitle": a["title"], "image": a["photo"],
        "telephone": a["phone"], "email": a["email"],
        "url": f"https://janetgiles.com/agents/{a['slug']}/",
        "worksFor": {"@type": "RealEstateAgent", "name": "Your Realty Link", "url": "https://yourrealtylink.com"},
        "areaServed": "Central Indiana",
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(a['name'])} — {esc(a['title'])} | Your Realty Link</title>
 <meta name="description" content="{esc(desc)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="https://janetgiles.com/agents/{a['slug']}/">
 <meta property="og:title" content="{esc(a['name'])} — {esc(a['title'])} | Your Realty Link">
 <meta property="og:description" content="{esc(desc)}">
 <meta property="og:url" content="https://janetgiles.com/agents/{a['slug']}/">
 <meta property="og:type" content="profile">
 <meta property="og:image" content="{a['photo']}">
 <script type="application/ld+json">
 {json.dumps(schema, indent=1)}
 </script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" rel="stylesheet">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 <style>{AGENT_CSS}</style>
</head>
<body>
{CANON_HDR}
<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>›</span> <a href="/agents/">Our Agents</a> <span>›</span> {esc(a['name'])}</div>
</nav>
<section class="page-hero">
 <div class="container">
 <h1>{esc(a['name'])}</h1>
 <p class="hero-sub">{esc(a['title'])} · Your Realty Link · Central Indiana Real Estate</p>
 <div class="hero-badges">
 <span class="hero-badge">📞 {esc(a['phone'])}</span>
 <span class="hero-badge">✉️ {esc(a['email'])}</span>
 <span class="hero-badge">🏡 Your Realty Link</span>
 </div>
 </div>
</section>
<main>
 <section class="section">
 <div class="container">
 <div class="agent-layout">
 <aside class="agent-side">
 <img src="{a['photo']}" alt="{esc(a['name'])} — Your Realty Link" class="agent-photo">
 <div class="agent-contact">
 <a href="{SEARCH_URL}" target="_blank" rel="noopener" class="btn-primary">Search Homes with {esc(first)} →</a>
 <a href="mailto:{a['email']}?subject=Real%20Estate%20Inquiry%20%E2%80%94%20Your%20Realty%20Link" class="btn-secondary">Email {esc(first)}</a>
 <a href="/services/free-home-valuation/" class="btn-secondary">Free Home Valuation</a>
 <p class="agent-reach">Call or text <a href="tel:{tel}">{esc(a['phone'])}</a><br><a href="mailto:{a['email']}">{esc(a['email'])}</a>{site_html}</p>
 </div>
 </aside>
 <div class="agent-main">
 <h2>About {esc(first)}</h2>
 {bio_html}
 <p style="margin-top:26px;"><a href="/agents/">← Back to our agents</a></p>
 </div>
 </div>
 </div>
 </section>
</main>
{CANON_FTR}
{TAIL}</body>
</html>
"""

FEATURED_POSTS = [
    ("Best School Districts in the Indianapolis Suburbs", "/blog/best-school-districts-in-the-indianapolis-suburbs/"),
    ("New Construction Communities in the Indy Suburbs", "/blog/new-construction-communities-indianapolis-suburbs/"),
    ("Things to Do in Carmel, Indiana", "/blog/things-to-do-in-carmel-indiana-local-guide/"),
]
PREMIUM = {"daniel-cope"}  # slugs that get the full mini-site layout

def expertise_for(a):
    if a.get("expertise"): return a["expertise"]
    t = a["title"]
    if "Commercial" in t: return ["Commercial Real Estate", "Investment Property", "Residential Buying & Selling", "Listing Marketing", "New Construction"]
    if a.get("lead") or "Broker" in t: return ["Listings & Marketing", "Buyer & Seller Representation", "Investment Property", "Relocation", "New Construction"]
    return ["Buyer Representation", "Home Selling", "First-Time Buyers", "Relocation", "Investment Property"]

PREMIUM_CSS = """
 .ah-grid { display:grid; grid-template-columns:230px 1fr; gap:34px; align-items:center; }
 .ah-photo { width:100%; border-radius:14px; box-shadow:0 6px 22px rgba(0,0,0,.28); display:block; }
 .ah-title { font-size:1.05rem; color:rgba(255,255,255,.9); margin:2px 0 6px; }
 .ah-tag { color:rgba(255,255,255,.8); margin:0 0 18px; max-width:560px; }
 .ah-cta { display:flex; flex-wrap:wrap; gap:12px; }
 .ah-cta a { font-weight:600; font-size:.95rem; padding:12px 22px; border-radius:8px; text-decoration:none; }
 .ah-cta .btn-primary { background:var(--red); color:#fff; }
 .ah-cta .btn-ghost { background:rgba(255,255,255,.12); color:#fff; border:1px solid rgba(255,255,255,.4); }
 .agent-search { background:linear-gradient(135deg,rgba(38,38,40,.82) 0%,rgba(22,22,24,.86) 100%), url('/assets/img/heroes/home.jpg') center 58%/cover no-repeat; color:#fff; padding:74px 0; text-align:center; }
 .agent-search h2 { color:#fff; }
 .agent-search p { color:rgba(255,255,255,.85); margin:6px auto 20px; max-width:560px; }
 .asr-bar { display:flex; max-width:640px; margin:0 auto; background:#fff; border-radius:10px; overflow:hidden; box-shadow:0 6px 20px rgba(0,0,0,.22); }
 .asr-bar input { flex:1; border:0; padding:15px 18px; font-size:1rem; outline:none; color:#1a1a1a; }
 .asr-bar button { border:0; background:var(--red); color:#fff; font-weight:600; font-size:1rem; padding:0 26px; cursor:pointer; }
 .asr-links { margin-top:16px; font-size:.92rem; color:rgba(255,255,255,.92); }
 .asr-links a { color:#fff; text-decoration:underline; margin:0 7px; white-space:nowrap; }
 .sect-alt { background:#f7f7f7; }
 .exp-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:14px; margin-top:8px; }
 .exp-card { background:#fff; border:1px solid #e6e6e6; border-left:4px solid var(--red); border-radius:10px; padding:16px 18px; font-weight:600; color:#1a1a1a; }
 .rev-strip { text-align:center; background:#fff; border:1px solid #e6e6e6; border-radius:14px; padding:26px; box-shadow:0 2px 12px rgba(0,0,0,.05); }
 .rev-strip .stars { color:#f5b301; font-size:1.6rem; letter-spacing:3px; }
 .rev-strip .big { font-family:var(--font-serif,Georgia,serif); font-size:2rem; font-weight:700; color:#1a1a1a; }
 .blog-cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:18px; margin-top:8px; }
 .blog-card { display:block; text-decoration:none; background:#fff; border:1px solid #e6e6e6; border-radius:12px; padding:20px 22px; box-shadow:0 2px 10px rgba(0,0,0,.05); transition:transform .15s, box-shadow .15s; }
 .blog-card:hover { transform:translateY(-3px); box-shadow:0 6px 18px rgba(0,0,0,.12); text-decoration:none; }
 .blog-card .bc-tag { font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--red); font-weight:700; }
 .blog-card h3 { font-size:1.02rem; color:#1a1a1a; margin:6px 0 0; line-height:1.35; }
 .agent-work-form { max-width:620px; }
 .area-links { margin-top:10px; }
 .area-links a { display:inline-block; background:#fff; border:1px solid #d6d6d6; border-radius:20px; padding:8px 16px; margin:8px 8px 0 0; color:var(--red); font-weight:600; font-size:.9rem; text-decoration:none; transition:all .15s; }
 .area-links a:hover { background:var(--red); color:#fff; border-color:var(--red); text-decoration:none; }
 .valuation-tool-card { max-width:560px; margin:0 auto; background:#fff; border-radius:16px; padding:34px 30px; box-shadow:0 4px 24px rgba(0,0,0,.08); }
 .valuation-tool-card h2 { text-align:center; font-size:1.5rem; color:#1a1a1a; margin:0 0 8px; }
 .valuation-tool-sub { text-align:center; color:#6e6e70; font-size:15px; margin:0 0 24px; }
 .valuation-tool-card label { display:block; font-size:13px; font-weight:600; color:#1a1a1a; margin-bottom:5px; }
 .valuation-tool-card .required { color:var(--red); }
 .valuation-tool-card input { width:100%; padding:13px 16px; font-size:15px; border-radius:10px; border:1.5px solid #ddd; margin-bottom:16px; box-sizing:border-box; }
 .valuation-tool-card input:focus { border-color:var(--red); outline:none; box-shadow:0 0 0 3px rgba(192,57,38,.1); }
 .valuation-tool-card .form-row { display:flex; gap:12px; }
 .valuation-tool-card .form-row > div { flex:1; }
 .valuation-tool-card button[type=submit] { width:100%; background:var(--red); color:#fff; border:0; padding:15px 24px; font-size:16px; font-weight:600; border-radius:10px; cursor:pointer; margin-top:4px; }
 .valuation-tool-card .form-note { text-align:center; margin-top:12px; font-size:12px; color:#6e6e70; }
 .valuation-result-card { background:#fff; border:2px solid var(--red); border-radius:10px; padding:28px; margin-top:24px; text-align:center; }
 .valuation-result-card h3 { color:#6e6e70; font-size:13px; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px; }
 .valuation-estimate { font-size:40px; font-weight:700; color:#1a1a1a; }
 .valuation-range { font-size:15px; color:#6e6e70; margin:6px 0 0; }
 .valuation-address { font-size:14px; color:#6e6e70; margin:12px 0 20px; padding-bottom:18px; border-bottom:1px solid #e6e6e6; }
 .valuation-details-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:12px; margin:16px 0; }
 .val-detail-item { background:#f7f7f7; border-radius:6px; padding:12px 8px; }
 .val-detail-label { font-size:11px; color:#6e6e70; text-transform:uppercase; letter-spacing:.5px; }
 .val-detail-value { font-size:17px; font-weight:700; color:#1a1a1a; margin-top:4px; }
 .valuation-comps { text-align:left; margin-top:22px; }
 .valuation-comps h4 { color:var(--red); font-size:15px; border-bottom:2px solid var(--red); padding-bottom:8px; }
 .comp-card { background:#f7f7f7; border-radius:6px; padding:12px 16px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; }
 .comp-address { font-weight:600; color:#1a1a1a; font-size:14px; }
 .comp-price { font-weight:700; color:var(--red); font-size:16px; }
 .comp-meta { font-size:12px; color:#6e6e70; width:100%; }
 .valuation-cta { margin-top:24px; padding-top:18px; border-top:1px solid #e6e6e6; }
 .valuation-cta p { font-size:14px; color:#6e6e70; margin-bottom:14px; }
 .valuation-cta .btn-red { display:inline-block; background:var(--red); color:#fff; padding:12px 24px; border-radius:6px; font-weight:600; text-decoration:none; margin:4px 8px; }
 .valuation-cta .btn-outline { display:inline-block; padding:12px 24px; border:2px solid var(--red); color:var(--red); font-weight:600; border-radius:6px; text-decoration:none; margin:4px 8px; }
 .valuation-cta .btn-outline:hover { background:var(--red); color:#fff; }
 @media (max-width:680px){ .ah-grid{ grid-template-columns:1fr; text-align:center; } .ah-photo{ max-width:220px; margin:0 auto; } .ah-cta{ justify-content:center; } }
"""

def premium_agent_page(a):
    first = first_name(a["name"]); tel = re.sub(r"\D", "", a["phone"])
    bio_html = "\n   ".join(f"<p>{esc(p)}</p>" for p in bio(a))
    exp = "".join(f'<div class="exp-card">{esc(x)}</div>' for x in expertise_for(a))
    areas = a.get("areas") or []
    areas_html = ('<h3 style="margin-top:30px;">Cities &amp; Neighborhoods ' + esc(first) + ' Serves</h3>\n <p style="color:#6e6e70;margin:2px 0 4px;">Explore the areas ' + esc(first) + ' works in most:</p>\n <div class="area-links">' + "".join(f'<a href="{u}">{esc(l)}</a>' for l, u in areas) + '</div>') if areas else ''
    posts = "".join(f'<a class="blog-card" href="{u}"><span class="bc-tag">From our blog</span><h3>{esc(t)}</h3></a>' for t, u in FEATURED_POSTS)
    mailto = f"mailto:{a['email']}?subject=Real%20Estate%20Inquiry%20%E2%80%94%20Your%20Realty%20Link"
    site = clean_site(a.get("website"))
    desc = f'{a["name"]}, {a["title"]} at Your Realty Link. Search Central Indiana homes, explore {first}’s expertise, and get in touch to buy, sell, or invest.'
    schema = {"@context":"https://schema.org","@type":"RealEstateAgent","name":a["name"],"jobTitle":a["title"],"image":a["photo"],"telephone":a["phone"],"email":a["email"],"url":f"https://janetgiles.com/agents/{a['slug']}/","worksFor":{"@type":"RealEstateAgent","name":"Your Realty Link","url":"https://yourrealtylink.com"},"areaServed":"Central Indiana"}
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{esc(a['name'])} — {esc(a['title'])} | Your Realty Link</title>
 <meta name="description" content="{esc(desc)}">
 <meta name="robots" content="index, follow">
 <link rel="canonical" href="https://janetgiles.com/agents/{a['slug']}/">
 <meta property="og:title" content="{esc(a['name'])} — {esc(a['title'])} | Your Realty Link">
 <meta property="og:description" content="{esc(desc)}">
 <meta property="og:url" content="https://janetgiles.com/agents/{a['slug']}/">
 <meta property="og:type" content="profile">
 <meta property="og:image" content="{a['photo']}">
 <script type="application/ld+json">
 {json.dumps(schema, indent=1)}
 </script>
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400..700&display=swap" rel="stylesheet">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 <style>{PREMIUM_CSS}</style>
</head>
<body>
{CANON_HDR}
<nav class="breadcrumbs" aria-label="Breadcrumb">
 <div class="container"><a href="/">Home</a> <span>›</span> <a href="/agents/">Our Agents</a> <span>›</span> {esc(a['name'])}</div>
</nav>

<section class="page-hero">
 <div class="container">
 <div class="ah-grid">
 <img class="ah-photo" src="{a['photo']}" alt="{esc(a['name'])} — Your Realty Link">
 <div class="ah-info">
 <h1>{esc(a['name'])}</h1>
 <p class="ah-title">{esc(a['title'])} · Your Realty Link · Central Indiana</p>
 <p class="ah-tag">Helping buyers, sellers, and investors across the Indianapolis metro with local knowledge, straight talk, and full MLS access.</p>
 <div class="ah-cta">
 <a class="btn-primary" href="#work-with">Work With {esc(first)}</a>
 <a class="btn-ghost" href="{mailto}">Email {esc(first)}</a>
 <a class="btn-ghost" href="tel:{tel}">Call / Text {esc(a['phone'])}</a>
 </div>
 </div>
 </div>
 </div>
</section>

<section class="agent-search">
 <div class="container">
 <h2>Search Central Indiana Homes with {esc(first)}</h2>
 <p>Browse every active MLS listing across Indianapolis and the surrounding metro — updated daily.</p>
 <form class="asr-bar" onsubmit="event.preventDefault(); window.location.href='/search/';" role="search">
 <input type="text" placeholder="Search by city, ZIP code, or neighborhood..." aria-label="Search homes" autocomplete="off">
 <button type="submit">Search Homes</button>
 </form>
 <div class="asr-links"><span>Popular:</span> <a href="/cities/hamilton-county/carmel-indiana-real-estate/">Carmel</a> <a href="/cities/hamilton-county/fishers-indiana-real-estate/">Fishers</a> <a href="/cities/johnson-county/greenwood-indiana-real-estate/">Greenwood</a> <a href="/cities/hendricks-county/avon-indiana-real-estate/">Avon</a> <a href="/cities/boone-county/zionsville-indiana-real-estate/">Zionsville</a></div>
 </div>
</section>

<main>
 <section class="section">
 <div class="container" style="max-width:820px;">
 <h2>About {esc(first)}</h2>
 {bio_html}
 <p class="agent-reach" style="color:#6e6e70;margin-top:14px;">Call or text <a href="tel:{tel}">{esc(a['phone'])}</a> · <a href="{mailto}">{esc(a['email'])}</a>{(' · <a href="'+site[0]+'" target="_blank" rel="noopener">'+esc(site[1])+'</a>') if site else ''}</p>
 </div>
 </section>

 <section class="section sect-alt">
 <div class="container">
 <h2>{esc(first)}&rsquo;s Areas of Expertise</h2>
 <div class="exp-grid">{exp}</div>
 {areas_html}
 </div>
 </section>

 <section class="section">
 <div class="container">
 <div class="valuation-tool-card">
 <h2>What&rsquo;s Your Home Worth?</h2>
 <p class="valuation-tool-sub">Get an instant estimate from {esc(first)} — backed by real comparable sales data.</p>
 <form class="ipg-valuation-form">
 <input type="hidden" name="source" value="agent-{a['slug']}">
 <input type="hidden" name="tags" value="agent-lead,agent-{a['slug']},valuation">
 <input type="hidden" name="source_page" value="agents/{a['slug']}">
 <input type="hidden" name="interest_type" value="Home Valuation — Agent: {esc(a['name'])}">
 <label for="val-address">Property Address <span class="required">*</span></label>
 <input type="text" id="val-address" name="address" required placeholder="123 Main St, Indianapolis, IN 46227" autocomplete="street-address">
 <div class="form-row">
 <div><label for="val-name">Name</label><input type="text" id="val-name" name="name" placeholder="Your name"></div>
 <div><label for="val-phone">Phone</label><input type="tel" id="val-phone" name="phone" placeholder="317-555-1234"></div>
 </div>
 <label for="val-email">Email <span class="required">*</span></label>
 <input type="email" id="val-email" name="email" required placeholder="you@example.com">
 <button type="submit">Get My Home Value →</button>
 <p class="form-note">Instant estimate on screen · Detailed report emailed to you · No obligation</p>
 </form>
 <div id="valuation-results" style="display:none;">
 <div class="valuation-result-card">
 <h3>Your Estimated Home Value</h3>
 <div class="valuation-estimate" id="val-estimate"></div>
 <div class="valuation-range" id="val-range"></div>
 <div class="valuation-address" id="val-address-display"></div>
 <div class="valuation-details-grid" id="val-details"></div>
 <div class="valuation-comps" id="val-comps-section" style="display:none;">
 <h4>Comparable Properties</h4>
 <div id="val-comps-list"></div>
 </div>
 <div class="valuation-cta">
 <p>This is an automated estimate. For a precise valuation based on your home&rsquo;s condition and upgrades, reach out to {esc(first)} for a personalized CMA.</p>
 <a href="tel:{tel}" class="btn-red">Call {esc(a['phone'])}</a>
 <a href="{mailto}" class="btn-outline">Email {esc(first)}</a>
 </div>
 </div>
 </div>
 </div>
 </div>
 </section>

 <section class="section sect-alt">
 <div class="container">
 <div class="rev-strip">
 <div class="stars">★★★★★</div>
 <div class="big">5.0 on Google</div>
 <p style="color:#444;margin:6px 0 14px;">Your Realty Link clients consistently rate the team 5 stars for responsive, no-pressure service.</p>
 <a href="/reviews/" class="btn-secondary">Read our reviews →</a>
 </div>
 </div>
 </section>

 <section class="section sect-alt">
 <div class="container">
 <h2>Helpful Reading</h2>
 <div class="blog-cards">{posts}</div>
 </div>
 </section>

 <section class="section" id="work-with">
 <div class="container" style="max-width:820px;">
 <h2>Work With {esc(a['name'])}</h2>
 <p>Tell {esc(first)} what you're looking for and you'll get a personal reply — no pressure, no obligation.</p>
 <form class="ipg-lead-form agent-work-form">
 <input type="hidden" name="source" value="agent-{a['slug']}">
 <input type="hidden" name="tags" value="agent-lead,agent-{a['slug']}">
 <input type="hidden" name="source_page" value="agents/{a['slug']}">
 <input type="hidden" name="interest_type" value="Agent: {esc(a['name'])} ({esc(a['title'])})">
 <div class="form-row">
 <div><label for="wname">Name *</label><input type="text" id="wname" name="name" required placeholder="Your name"></div>
 <div><label for="wphone">Phone *</label><input type="tel" id="wphone" name="phone" required placeholder="317-555-1234"></div>
 </div>
 <label for="wemail">Email *</label>
 <input type="email" id="wemail" name="email" required placeholder="you@example.com">
 <label for="wmsg">How can {esc(first)} help?</label>
 <textarea id="wmsg" name="message" placeholder="Buying, selling, investing, or just have a question…"></textarea>
 <button type="submit">Send to {esc(first)} →</button>
 <p class="form-note">No spam · No obligation · You'll hear back personally</p>
 </form>
 </div>
 </section>
</main>
{CANON_FTR}
{TAIL}<script src="/assets/js/lead-form.js?v=406824a0"></script>
<script src="/assets/js/valuation-form.js?v=044c32e3"></script>
</body>
</html>
"""

# assign slugs
for a in AGENTS:
    a["slug"] = slugify(a["name"])

os.makedirs(os.path.join(ROOT, "agents"), exist_ok=True)
open(os.path.join(ROOT, "agents", "index.html"), "w", encoding="utf-8").write(hub_page(AGENTS))
for a in AGENTS:
    d = os.path.join(ROOT, "agents", a["slug"])
    os.makedirs(d, exist_ok=True)
    builder = premium_agent_page if a["slug"] in PREMIUM else agent_page
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(builder(a))

print(f"built /agents/ hub + {len(AGENTS)} agent pages (premium: {sorted(PREMIUM)})")
for a in AGENTS:
    print("  /agents/%s/  — %s (%s)" % (a["slug"], a["name"], a["title"]))
