#!/usr/bin/env python3
"""Regenerate the homepage hero 'Popular:' chips + 'Popular Cities Near
Indianapolis' cards. The city selection is edited by the broker in the hub
(Supabase hub_content -> get_yrl_homepage_cities RPC); this script pulls it,
caches it to homepage-cities.json, and falls back to that file if the hub is
unreachable. Facts (name/county/price) are pulled from each city page's
'at a glance' box so they stay accurate."""
import os, re, html, json, glob, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG_FILE = os.path.join(ROOT, "homepage-cities.json")

SB_URL = "https://wdvolamasztetwpitbwg.supabase.co"
SB_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
          "Indkdm9sYW1hc3p0ZXR3cGl0YndnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3Nzc2"
          "MTYsImV4cCI6MjA5MTM1MzYxNn0.uiGIaZwr88ZNtAobfSV-axlpXB3sos2Rcw3FiFm6JO8")

def load_cfg():
    """Prefer the hub-edited config (Supabase); cache it locally. On any error,
    use the last-known local cache so the build never fails on a hub hiccup."""
    try:
        req = urllib.request.Request(
            f"{SB_URL}/rest/v1/rpc/get_yrl_homepage_cities", data=b"{}", method="POST",
            headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
                     "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            remote = json.load(r)
        if isinstance(remote, dict) and remote.get("popular") and remote.get("nearby"):
            json.dump(remote, open(CFG_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("homepage cities: pulled from hub (Supabase)")
            return remote
        print("homepage cities: hub returned no config, using local cache")
    except Exception as e:
        print("homepage cities: hub unreachable (%s), using local cache" % e)
    return json.load(open(CFG_FILE, encoding="utf-8"))

cfg = load_cfg()

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
            info["key"] = k
            out.append(info)
    return out

def hc_map(c):
    """The card header: a real street map (with a baked-in pin) when we have one,
    else the gradient + emoji-pin fallback."""
    img = os.path.join(ROOT, "assets", "img", "citymaps", c["key"] + ".webp")
    if os.path.exists(img):
        return (f'<div class="hc-map"><img class="hc-mapimg" loading="lazy" '
                f'src="/assets/img/citymaps/{c["key"]}.webp" '
                f'alt="Map of {html.escape(c["name"])}, Indiana" width="480" height="210"></div>')
    return '<div class="hc-map"><span class="hc-pin">&#128205;</span></div>'

pop = resolve(cfg["popular"], cfg.get("popular_cap", 7))
near = resolve(cfg["nearby"], cfg.get("nearby_cap", 12))

chips = '<div class="hero-quick-links">\n <span>Popular:</span>\n' + \
    "".join(f' <a href="{c["url"]}" class="hero-quick-link">{html.escape(c["name"])}</a>\n' for c in pop) + ' </div>'

# Compact city-name buttons under the county map (was a big card grid — the
# broker asked to save homepage space). hc_map() is kept for possible reuse.
cards = '<div class="home-city-btns"><span class="hcb-label">Popular cities:</span>' + "".join(
    f'<a href="{c["url"]}" class="home-city-btn">{html.escape(c["name"])}</a>'
    for c in near) + '</div>'

def replace_between(text, name, block):
    """Swap the content between <!-- NAME --> ... <!-- /NAME --> markers.
    Idempotent and robust to nested tags inside the block (unlike a bare
    non-greedy regex, which broke once the cards gained inner <div>s)."""
    b, e = f"<!-- {name} -->", f"<!-- /{name} -->"
    pat = re.compile(re.escape(b) + r".*?" + re.escape(e), re.DOTALL)
    if not pat.search(text):
        raise SystemExit(f"marker {name} not found in index.html")
    return pat.sub(lambda m: f"{b}\n {block}\n {e}", text, count=1)

t = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
t = replace_between(t, "HOME-HERO-CHIPS", chips)
t = replace_between(t, "HOME-CITIES-GRID", cards)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(t)
print("homepage rebuilt: %d popular chips, %d city buttons" % (len(pop), len(near)))
