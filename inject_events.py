#!/usr/bin/env python3
"""Inject a 'Community Events and Local Calendar' section into each city page,
from community_events.json (post link-check). Idempotent (marker-wrapped),
HTML-only, no whitespace reflow. Links the official city site + verified event
calendars + real recurring events (season/month only)."""
import os, re, html, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "community-events.json"), encoding="utf-8"))

def page_dir(slug):
    hits = glob.glob(os.path.join(ROOT, "cities", "*", slug))
    return hits[0] if hits else None

BEGIN, END = "<!-- COMMUNITY-EVENTS -->", "<!-- /COMMUNITY-EVENTS -->"

def t(s):   # display text
    return html.escape(str(s or ""), quote=False)

def u(url):  # url for href attribute
    return str(url or "").replace("&", "&amp;")

def link(label, url):
    return '<a href="%s" target="_blank" rel="noopener">%s &#8599;</a>' % (u(url), t(label))

def join_natural(items):
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + ", and " + items[-1]

def build_section(c):
    city = c["city"]
    events = [e for e in (c.get("events") or []) if e.get("name")]
    cals = [l for l in (c.get("calendar_links") or []) if l.get("url")]
    official = c.get("official_site") or ""

    if events:
        intro = ("One of the joys of living in %s is the local calendar. From seasonal "
                 "festivals to farmers markets and community gatherings, here are a few "
                 "%s-area traditions worth knowing about, plus where to find what is "
                 "happening throughout the year." % (t(city), t(city)))
    else:
        intro = ("Part of what makes %s feel like home is its community life. Here is where "
                 "to find local events, festivals, and things to do in and around %s all "
                 "year long." % (t(city), t(city)))

    parts = [BEGIN,
             ' <hr class="divider">',
             ' <h2 id="community-events">Community Events &amp; Local Calendar in %s, Indiana</h2>' % t(city),
             ' <p>%s</p>' % intro]

    if events:
        lis = []
        for e in events:
            when = t(e.get("when", "")).strip()
            desc = t(e.get("desc", "")).strip()
            seg = " &mdash; %s." % when if when else ""
            if desc:
                seg += " " + desc
            lis.append("  <li><strong>%s</strong>%s</li>" % (t(e["name"]), seg))
        parts.append(" <ul>\n" + "\n".join(lis) + "\n </ul>")

    linkbits = [link(l["label"], l["url"]) for l in cals]
    if official:
        linkbits.append('the <a href="%s" target="_blank" rel="noopener">official %s website &#8599;</a>'
                        % (u(official), t(city)))
    if linkbits:
        parts.append(' <p><strong>Local event calendars:</strong> Stay up to date on what is '
                     'happening in and around %s through %s.</p>' % (t(city), join_natural(linkbits)))

    parts.append(' <p>Thinking about making %s home? <a href="/contact/">Contact Your Realty Link</a> '
                 'or <a href="https://yourrealtylink.com/property-search" target="_blank" rel="noopener">'
                 'search %s homes for sale</a>.</p>' % (t(city), t(city)))
    parts.append(END)
    return "\n".join(parts) + "\n\n "

def inject(pathdir, section):
    f = os.path.join(pathdir, "index.html")
    src = open(f, encoding="utf-8").read()
    # idempotent: strip old block
    src = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*", "", src, flags=re.DOTALL)
    # anchor 1: the divider before "Explore"
    m = re.search(r'<hr class="divider">\s*<h3>\s*Explore', src)
    if m:
        pos = m.start()
    else:
        m = re.search(r'<div class="info-box"', src)
        pos = m.start() if m else src.find("</main>")
    if pos < 0:
        return None
    out = src[:pos] + section + src[pos:]
    open(f, "w", encoding="utf-8").write(out)
    return True

updated = ev_pages = 0
warn = []
for c in DATA:
    slug = c["slug"]
    d = page_dir(slug)
    if not d:
        warn.append("no page dir for " + slug); continue
    section = build_section(c)
    ok = inject(d, section)
    if ok:
        updated += 1
        if c.get("events"):
            ev_pages += 1
    else:
        warn.append("no anchor in " + slug)

print("Injected events section into %d pages (%d have event lists, %d links-only)."
      % (updated, ev_pages, updated - ev_pages))
for w in warn:
    print("  WARN " + w)
