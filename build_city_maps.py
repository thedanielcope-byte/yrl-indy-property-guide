#!/usr/bin/env python3
"""Generate one real street-map image per city (Geoapify Static Maps), stored
once at assets/img/citymaps/<key>.webp and reused on homepage cards, guide PDFs,
and city-page heroes.

Two phases (key via env GEOAPIFY_KEY; the key is a build-time secret and is
NEVER written into the repo or the site):
    python3 build_city_maps.py geocode   # -> city_coords.json (+ validation table)
    python3 build_city_maps.py maps      # reads city_coords.json -> webp images
"""
import os, re, sys, json, glob, html, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("GEOAPIFY_KEY", "").strip()
COORDS = os.path.join(ROOT, "city_coords.json")
OUTDIR = os.path.join(ROOT, "assets", "img", "citymaps")

STYLE = "osm-bright-smooth"
ZOOM = 12
W, H = 480, 210                     # retina-ish; cards crop via object-fit: cover
PIN = "%23c03926"                   # brand red

# Page-hero backgrounds: a dark map (readable under a light navy scrim), wide, no
# pin (text sits over it). Cities zoom in; counties zoom out to show the area.
HERO_STYLE = "dark-matter-brown"
HERO_W, HERO_H = 1280, 460
CITY_HERO_ZOOM = 12
COUNTY_HERO_ZOOM = 10
COUNTY_COORDS = os.path.join(ROOT, "county_coords.json")
HERO_DIR = os.path.join(OUTDIR, "heroes")
COUNTY_DIR = os.path.join(OUTDIR, "counties")

# central-Indiana sanity box (looser than the query filter) for validation
IN_BOX = dict(lat=(38.2, 40.9), lon=(-87.6, -84.7))


def clean(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()

def clean_county(county):
    c = county.replace(" Seat", "")
    c = re.sub(r"\s*[&/].*$", "", c)
    c = re.sub(r"^(NW|NE|SW|SE|N|S|E|W)\s+", "", c).replace(" Co.", " County").strip()
    if not c.endswith("County"):
        c += " County"
    return c

def cities():
    data = json.load(open(os.path.join(ROOT, "homepage-cities-available.json"), encoding="utf-8"))
    for c in data:
        c["county_clean"] = clean_county(c["county"])
    return data

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read()


def geocode():
    if not KEY: sys.exit("Set GEOAPIFY_KEY in the environment.")
    out = json.load(open(COORDS, encoding="utf-8")) if os.path.exists(COORDS) else {}
    flags = []
    for c in cities():
        k = c["key"]
        if k in out and out[k].get("lat"):
            continue
        q = urllib.parse.quote(f"{c['name']}, {c['county_clean']}, Indiana")
        url = (f"https://api.geoapify.com/v1/geocode/search?text={q}&format=json&limit=1"
               f"&bias=proximity:-86.15,39.77&filter=rect:-88.1,37.8,-84.8,41.8&apiKey={KEY}")
        try:
            res = json.loads(get(url)).get("results", [])
        except Exception as e:
            flags.append(f"{c['name']}: request failed ({e})"); continue
        if not res:
            flags.append(f"{c['name']}: NO RESULT"); continue
        r = res[0]
        lat, lon = r.get("lat"), r.get("lon")
        state, county = r.get("state"), r.get("county")
        ok_box = IN_BOX["lat"][0] <= lat <= IN_BOX["lat"][1] and IN_BOX["lon"][0] <= lon <= IN_BOX["lon"][1]
        ok_state = (state == "Indiana")
        ok_cty = (county or "").replace(" County", "") in c["county_clean"]
        if not (ok_box and ok_state):
            flags.append(f"{c['name']}: state={state} county={county} lat={lat} lon={lon} (OUTSIDE central IN)")
        elif not ok_cty:
            flags.append(f"{c['name']}: got county={county}, expected {c['county_clean']} (verify)")
        out[k] = dict(name=c["name"], lat=lat, lon=lon, state=state, county=county)
    json.dump(out, open(COORDS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"geocoded {len(out)}/{len(cities())} cities -> city_coords.json")
    print("\n=== FLAGS (verify these) ===" if flags else "no flags — all within central Indiana ✓")
    for f in flags: print("  ⚠ " + f)


def maps():
    if not KEY: sys.exit("Set GEOAPIFY_KEY in the environment.")
    from PIL import Image
    import io
    os.makedirs(OUTDIR, exist_ok=True)
    coords = json.load(open(COORDS, encoding="utf-8"))
    done = 0
    for k, c in coords.items():
        lat, lon = c.get("lat"), c.get("lon")
        if not lat: continue
        url = (f"https://maps.geoapify.com/v1/staticmap?style={STYLE}&width={W}&height={H}"
               f"&center=lonlat:{lon},{lat}&zoom={ZOOM}"
               f"&marker=lonlat:{lon},{lat};type:material;color:{PIN};size:medium&apiKey={KEY}")
        try:
            raw = get(url)
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img.save(os.path.join(OUTDIR, f"{k}.webp"), "WEBP", quality=82, method=6)
            done += 1
        except Exception as e:
            print(f"  ✗ {k}: {e}")
    print(f"generated {done} city maps -> assets/img/citymaps/*.webp")


def _save_webp(url, path):
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(get(url))).convert("RGB")
    img.save(path, "WEBP", quality=80, method=6)


def city_heroes():
    """Wide dark street map per city for the page-hero background (no pin)."""
    if not KEY: sys.exit("Set GEOAPIFY_KEY in the environment.")
    os.makedirs(HERO_DIR, exist_ok=True)
    coords = json.load(open(COORDS, encoding="utf-8"))
    done = 0
    for k, c in coords.items():
        if not c.get("lat"): continue
        url = (f"https://maps.geoapify.com/v1/staticmap?style={HERO_STYLE}&width={HERO_W}&height={HERO_H}"
               f"&center=lonlat:{c['lon']},{c['lat']}&zoom={CITY_HERO_ZOOM}&apiKey={KEY}")
        try:
            _save_webp(url, os.path.join(HERO_DIR, f"{k}-hero.webp")); done += 1
        except Exception as e:
            print(f"  ✗ {k}: {e}")
    print(f"generated {done} city hero maps -> assets/img/citymaps/heroes/*-hero.webp")


def county_list():
    return sorted(os.path.basename(os.path.dirname(p)).replace("-indiana-real-estate", "")
                  for p in glob.glob(os.path.join(ROOT, "counties", "*", "index.html")))


def counties():
    """Geocode each county (centroid) and render a zoomed-out dark hero map."""
    if not KEY: sys.exit("Set GEOAPIFY_KEY in the environment.")
    os.makedirs(COUNTY_DIR, exist_ok=True)
    cc = json.load(open(COUNTY_COORDS, encoding="utf-8")) if os.path.exists(COUNTY_COORDS) else {}
    for slug in county_list():
        name = slug.replace("-", " ").title()          # e.g. "Hamilton County"
        if slug not in cc or not cc[slug].get("lat"):
            q = urllib.parse.quote(f"{name}, Indiana, USA")
            url = (f"https://api.geoapify.com/v1/geocode/search?text={q}&format=json&limit=1"
                   f"&bias=proximity:-86.15,39.77&filter=rect:-88.1,37.8,-84.8,41.8&apiKey={KEY}")
            try:
                r = json.loads(get(url)).get("results", [])
            except Exception as e:
                print(f"  ✗ geocode {name}: {e}"); continue
            if not r: print(f"  ✗ geocode {name}: no result"); continue
            cc[slug] = dict(name=name, lat=r[0]["lat"], lon=r[0]["lon"], state=r[0].get("state"))
    json.dump(cc, open(COUNTY_COORDS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    done = 0
    for slug, c in cc.items():
        if not c.get("lat"): continue
        url = (f"https://maps.geoapify.com/v1/staticmap?style={HERO_STYLE}&width={HERO_W}&height={HERO_H}"
               f"&center=lonlat:{c['lon']},{c['lat']}&zoom={COUNTY_HERO_ZOOM}&apiKey={KEY}")
        try:
            _save_webp(url, os.path.join(COUNTY_DIR, f"{slug}-hero.webp")); done += 1
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
    print(f"geocoded/rendered {done} county hero maps -> assets/img/citymaps/counties/*-hero.webp")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "geocode"
    {"geocode": geocode, "maps": maps, "heroes": city_heroes, "counties": counties}[mode]()
