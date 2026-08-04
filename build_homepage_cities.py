#!/usr/bin/env python3
"""Regenerate the homepage hero 'Popular:' chips + 'Popular Cities Near
Indianapolis' cards from homepage-cities.json (capped). Facts (name/county/price)
are pulled from each city page's 'at a glance' box so they stay accurate."""
import os, re, html, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(ROOT, "homepage-cities.json"), encoding="utf-8"))

def clean(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()

def city_info(key):
    hits = glob.glob(os.path.join(ROOT, "cities", "*", key + "-indiana-real-estate", "index.html")) \
        or glob.glob(os.path.join(ROOT, "cities", "*", key + "-indianapolis-real-estate", "index.html"))
    if not hits:
        return None
    p = hits[0]; t = open(p, encoding="utf-8").read()
    facts = dict((clean(a), clean(b)) for a, b in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", t, re.S))
    h1 = re.search(r"<h1>(.*?)</h1>", t, re.S)
    name = re.split(r" Indiana(?:polis)? ", clean(h1.group(1)))[0].strip() if h1 else key.title()
    price = clean(facts.get("Typical home prices", "")).replace("–", " – ").replace("  ", " ")
    url = "/" + os.path.relpath(os.path.dirname(p), ROOT) + "/"
    return dict(name=name, county=clean(facts.get("County", "")), price=price, url=url)

def resolve(keys, cap):
    out = []
    for k in keys[:cap]:
        info = city_info(k)
        if info:
            out.append(info)
    return out

pop = resolve(cfg["popular"], cfg.get("popular_cap", 7))
near = resolve(cfg["nearby"], cfg.get("nearby_cap", 12))

chips = '<div class="hero-quick-links">\n <span>Popular:</span>\n' + \
    "".join(f' <a href="{c["url"]}" class="hero-quick-link">{html.escape(c["name"])}</a>\n' for c in pop) + ' </div>'

cards = '<div class="home-cities-grid">\n' + "".join(
    f'  <a href="{c["url"]}" class="home-city-card"><div class="hc-map"><span class="hc-pin">&#128205;</span></div>'
    f'<div class="hc-body"><h3>{html.escape(c["name"])}</h3><span class="hc-county">{html.escape(c["county"])}</span>'
    f'<span class="hc-price">{html.escape(c["price"])}</span><span class="hc-arrow">&rarr;</span></div></a>\n'
    for c in near) + ' </div>'

t = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
t = re.sub(r'<div class="hero-quick-links">.*?</div>', lambda m: chips, t, count=1, flags=re.DOTALL)
t = re.sub(r'<div class="home-cities-grid">.*?</div>', lambda m: cards, t, count=1, flags=re.DOTALL)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(t)
print("homepage rebuilt: %d popular chips, %d city cards" % (len(pop), len(near)))
