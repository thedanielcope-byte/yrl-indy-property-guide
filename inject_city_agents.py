#!/usr/bin/env python3
"""Show Your Realty Link agents on the city/neighborhood pages they serve.

Reads agents-roster.json; each agent's `areas` ([label, url]) are the pages they
chose in the hub. For every city/neighborhood page that one or more agents serve,
injects an agent tile (photo + name + phone) at the top of the sidebar, above the
"Get in Touch" card. Idempotent (marker-wrapped): re-running adds/updates/removes
tiles to match the current roster — so when an agent adds or drops an area in the
hub, the next sync updates the page automatically. HTML-only, no reflow.
"""
import os, re, html, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
AGENTS = json.load(open(os.path.join(ROOT, "agents-roster.json"), encoding="utf-8"))
BEGIN, END = "<!-- CITY-AGENTS -->", "<!-- /CITY-AGENTS -->"
MAXSHOW = 6

def esc(s):
    return html.escape(str(s or ""), quote=True)

# url -> {"label": str, "agents": [agent, ...]} (roster order preserved)
served = {}
for a in AGENTS:
    for area in (a.get("areas") or []):
        try:
            label, url = area[0], area[1]
        except (IndexError, TypeError):
            continue
        if not url:
            continue
        e = served.setdefault(url, {"label": label, "agents": []})
        e["agents"].append(a)

def row(a, first):
    digits = re.sub(r"\D", "", a.get("phone") or "")
    bt = "" if first else "border-top:1px solid var(--border);"
    phone = ('<a href="tel:%s" style="display:inline-block;margin-top:3px;font-size:.86rem;color:var(--red);font-weight:600;">&#128222; %s</a>'
             % (digits, esc(a.get("phone"))) if digits else "")
    return (
        '    <div style="display:flex;gap:12px;align-items:center;padding:12px 0;%s">\n'
        '     <img src="%s" alt="%s — Your Realty Link agent" width="58" height="58" loading="lazy" '
        'style="width:58px;height:58px;border-radius:50%%;object-fit:cover;object-position:top center;flex:0 0 auto;background:#ececec;">\n'
        '     <div style="min-width:0;line-height:1.3;">\n'
        '      <a href="/agents/%s/" style="font-weight:700;color:var(--dark);font-size:.95rem;">%s</a>\n'
        '      <span style="display:block;font-size:.76rem;color:var(--gray);">%s</span>\n'
        '      %s\n'
        '     </div>\n'
        '    </div>' % (bt, esc(a["photo"]), esc(a["name"]), esc(a["slug"]),
                        esc(a["name"]), esc(a.get("title")), phone))

def tile(label, agents):
    head = "Your Realty Link Agent in %s" % esc(label) if len(agents) == 1 \
        else "Your Realty Link Agents in %s" % esc(label)
    shown = agents[:MAXSHOW]
    rows = "\n".join(row(a, i == 0) for i, a in enumerate(shown))
    more = ""
    if len(agents) > MAXSHOW:
        more = ('\n    <a href="/agents/" style="display:block;margin-top:10px;font-size:.85rem;'
                'color:var(--red);font-weight:600;">+ %d more agents &rarr;</a>' % (len(agents) - MAXSHOW))
    return (
        '%s\n'
        '  <div class="sidebar-card">\n'
        '   <div class="sidebar-card-header">%s</div>\n'
        '   <div class="sidebar-card-body" style="padding-top:4px;">\n'
        '%s%s\n'
        '   </div>\n'
        '  </div>\n'
        '%s\n ' % (BEGIN, head, rows, more, END))

def page_url(path):
    rel = os.path.relpath(path, ROOT)
    return "/" + rel[:-len("index.html")]

pages = glob.glob(os.path.join(ROOT, "cities", "*", "*", "index.html")) \
    + glob.glob(os.path.join(ROOT, "neighborhoods", "*", "index.html"))

added = removed = 0
for path in pages:
    src = open(path, encoding="utf-8").read()
    stripped = re.sub(r"\s*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*",
                      "\n ", src, flags=re.DOTALL)
    had = stripped != src
    url = page_url(path)
    out = stripped
    if url in served:
        m = re.search(r'<aside class="content-sidebar">', stripped)
        if m:
            block = tile(served[url]["label"], served[url]["agents"])
            out = stripped[:m.end()] + "\n " + block + stripped[m.end():]
            added += 1
    else:
        if had:
            removed += 1
    if out != src:
        open(path, "w", encoding="utf-8").write(out)

print("Agent tiles: %d pages now show agents, %d stale tiles removed." % (added, removed))
print("Areas served by roster:", len(served),
      "->", sorted(page_url_.rstrip("/").split("/")[-1] for page_url_ in served))
