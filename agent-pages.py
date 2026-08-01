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
 <a href="/contact/" class="btn-secondary">Contact {esc(first)}</a>
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

# assign slugs
for a in AGENTS:
    a["slug"] = slugify(a["name"])

os.makedirs(os.path.join(ROOT, "agents"), exist_ok=True)
open(os.path.join(ROOT, "agents", "index.html"), "w", encoding="utf-8").write(hub_page(AGENTS))
for a in AGENTS:
    d = os.path.join(ROOT, "agents", a["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(agent_page(a))

print(f"built /agents/ hub + {len(AGENTS)} agent pages")
for a in AGENTS:
    print("  /agents/%s/  — %s (%s)" % (a["slug"], a["name"], a["title"]))
