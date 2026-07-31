#!/usr/bin/env python3
"""
Agent landing pages + /agents/ directory generator.

Add each agent to AGENTS, run:  python3 agent-pages.py
- writes /agents/<slug>/index.html for every agent
- (re)builds the /agents/ directory hub page with a card per agent

To add the roster later: append dicts to AGENTS and re-run. Idempotent.
"""
import os, re, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))

AGENTS = [
    {
        "slug": "daniel-cope",
        "name": "Daniel Cope",
        "title": "Principal Broker",
        "photo": "https://assets.cdn.filesafe.space/MbY1ICQ6HdzVOrgFncoI/media/699cdf483730806ca89406e5.png",
        "phone": "317-201-6323",
        "email": "info@yourrealtylink.com",
        "search_url": "https://yourrealtylink.com/property-search",
        "bio": [
            "Daniel Cope is a licensed Indiana real estate broker and the principal broker of Your Realty Link, with years of experience helping Central Indiana residents buy, sell, and invest in real estate. With deep local roots, Daniel has built a reputation for straight talk, market knowledge, and putting clients first — every single time.",
            "Daniel's story is a Central Indiana story. He knows the neighborhoods, the school districts, the commute corridors, and the communities that make this region special. Whether a client is buying their first home in Greenwood or selling a longtime family property in Carmel, Daniel brings the same level of care and expertise to every transaction.",
        ],
        "specialties": ["Buyer Representation", "Listings & Marketing", "Investment Property", "Relocation", "First-Time Buyers"],
    },
]

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
CANON_HDR = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
CANON_FTR = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
TAIL = src[src.index('</footer>') + len('</footer>'):src.index('</body>')]
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)

GRID_CSS = """
 .agent-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:22px; margin:8px 0; }
 .agent-card { display:block; text-decoration:none; background:#fff; border:1px solid #e6e6e6; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.05); transition:transform .15s, box-shadow .15s; }
 .agent-card:hover { transform:translateY(-3px); box-shadow:0 6px 20px rgba(0,0,0,.12); text-decoration:none; }
 .agent-card img { width:100%; aspect-ratio:1/1; object-fit:cover; display:block; background:#ececec; }
 .agent-card .ac-body { padding:13px 15px; }
 .agent-card .ac-name { font-weight:700; color:#1a1a1a; font-size:1rem; }
 .agent-card .ac-title { font-size:.83rem; color:#6e6e70; margin-top:2px; }
 .agent-card .ac-cta { color:#c03926; font-weight:600; font-size:.83rem; margin-top:8px; display:inline-block; }
"""

AGENT_CSS = """
 .agent-layout { display:grid; grid-template-columns:300px 1fr; gap:40px; align-items:start; }
 .agent-photo { width:100%; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,.12); display:block; }
 .agent-contact { margin-top:18px; display:flex; flex-direction:column; gap:10px; }
 .agent-contact a.btn-primary, .agent-contact a.btn-secondary { text-align:center; display:block; }
 .agent-reach { font-size:.9rem; color:#6e6e70; margin-top:10px; line-height:1.8; }
 .chips { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0; }
 .chip { background:#f2f2f2; color:#444; border-radius:20px; padding:6px 14px; font-size:.85rem; }
 @media (max-width:760px){ .agent-layout{ grid-template-columns:1fr; } }
"""

def esc(s): return html.escape(s, quote=True)

def card(a):
    return (f'<a href="/agents/{a["slug"]}/" class="agent-card">'
            f'<img src="{a["photo"]}" alt="{esc(a["name"])} — Your Realty Link" width="300" height="300" loading="lazy">'
            f'<div class="ac-body"><div class="ac-name">{esc(a["name"])}</div>'
            f'<div class="ac-title">{esc(a["title"])}</div>'
            f'<span class="ac-cta">View Profile →</span></div></a>')

def hub_page(agents):
    cards = "\n ".join(card(a) for a in agents)
    desc = "Meet the Your Realty Link team — 20+ experienced Central Indiana real estate agents. Find your agent, view their profile, and start your home search with them."
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
 <p class="hero-sub">Meet the Your Realty Link team — a local boutique brokerage of 20+ experienced Central Indiana real estate experts.</p>
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
 <a href="https://yourrealtylink.com/property-search" target="_blank" rel="noopener" class="btn-secondary">Search Homes</a>
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
    first = a["name"].split()[0]
    tel = re.sub(r"\D", "", a["phone"])
    bio_html = "\n   ".join(f"<p>{esc(p)}</p>" for p in a["bio"])
    chips = "".join(f'<span class="chip">{esc(s)}</span>' for s in a.get("specialties", []))
    desc = f'{a["name"]}, {a["title"]} at Your Realty Link — a Central Indiana real estate expert. Search homes, get a free valuation, or contact {first} today.'
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
 <span class="hero-badge">🏡 MIBOR Agent</span>
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
 <a href="{a['search_url']}" target="_blank" rel="noopener" class="btn-primary">Search Homes with {esc(first)} →</a>
 <a href="/contact/" class="btn-secondary">Contact {esc(first)}</a>
 <a href="/services/free-home-valuation/" class="btn-secondary">Free Home Valuation</a>
 <p class="agent-reach">Call or text <a href="tel:{tel}">{esc(a['phone'])}</a><br><a href="mailto:{a['email']}">{esc(a['email'])}</a></p>
 </div>
 </aside>
 <div class="agent-main">
 <h2>About {esc(first)}</h2>
 {bio_html}
 <h3>Specialties</h3>
 <div class="chips">{chips}</div>
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

# write hub
os.makedirs(os.path.join(ROOT, "agents"), exist_ok=True)
open(os.path.join(ROOT, "agents", "index.html"), "w", encoding="utf-8").write(hub_page(AGENTS))
# write agent pages
for a in AGENTS:
    d = os.path.join(ROOT, "agents", a["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(agent_page(a))

print(f"built /agents/ hub + {len(AGENTS)} agent page(s): {[a['slug'] for a in AGENTS]}")
