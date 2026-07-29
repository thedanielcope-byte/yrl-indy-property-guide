#!/usr/bin/env python3
"""
Site-wide social-link refresh + add Reviews nav link.

- Facebook  CSIRealtyTeam            -> yourrealtylink        (href + JSON-LD sameAs)
- LinkedIn  /in/thedanielcope/       -> /company/your-realty-link-llc/ (href + sameAs)
- Twitter   twitter.com/janetgiles   -> YouTube @yourrealtylink (presentation-aware: glyph/styled/plain)
- Instagram anchor  -> append a Google Business Profile link right after it (footer glyph pages only)
- Nav: add a "Reviews" link (before About), once per page.

DRY RUN by default.  Apply with:  python3 social-reviews-update.py --apply
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {".git", "node_modules", ".next", ".wrangler"}
apply = "--apply" in sys.argv

GOOGLE = "https://share.google/kcy70YdMXrZGTg3GF"
YT = "https://www.youtube.com/@yourrealtylink"

def convert_twitter(m):
    attrs = m.group(1)
    if "aria-label=" in attrs:
        return f'<a href="{YT}" target="_blank" rel="noopener" aria-label="YouTube">yt</a>'
    if "style=" in attrs:
        return f'<a href="{YT}" target="_blank" rel="noopener" style="color:#c03926; font-weight:600; font-size:.9rem;">YouTube</a>'
    return f'<a href="{YT}" target="_blank" rel="noopener">YouTube</a>'

def append_google_after_instagram(m):
    whole = m.group(0); attrs = m.group(1)
    # only footer glyph rows (aria-label) get the extra Google icon
    if "aria-label=" in attrs:
        return whole + f'\n <a href="{GOOGLE}" target="_blank" rel="noopener" aria-label="Google Business Profile">G</a>'
    return whole

TW_RE = re.compile(r'<a href="https://twitter\.com/janetgiles"([^>]*)>.*?</a>')
IG_RE = re.compile(r'<a href="https://www\.instagram\.com/IndianapolisRealEstate"([^>]*)>.*?</a>')

counts = {"fb":0,"li":0,"tw":0,"goog":0,"nav":0}
files_changed = 0

def process(path):
    global files_changed
    with open(path, encoding="utf-8") as fh:
        orig = fh.read()
    t = orig
    c_fb = t.count("https://www.facebook.com/CSIRealtyTeam")
    t = t.replace("https://www.facebook.com/CSIRealtyTeam", "https://www.facebook.com/yourrealtylink")
    c_li = t.count("https://www.linkedin.com/in/thedanielcope/")
    t = t.replace("https://www.linkedin.com/in/thedanielcope/", "https://www.linkedin.com/company/your-realty-link-llc/")
    t, c_tw = TW_RE.subn(convert_twitter, t)
    # count instagram anchors that will gain a Google sibling (footer glyph only)
    c_goog = len([m for m in IG_RE.finditer(t) if "aria-label=" in m.group(1)])
    t = IG_RE.sub(append_google_after_instagram, t)
    # nav Reviews link (idempotent: only if page has no /reviews/ link yet, and has the About nav link)
    c_nav = 0
    if 'href="/reviews/"' not in t and '<a href="/about/">About</a>' in t:
        t = t.replace('<a href="/about/">About</a>', '<a href="/reviews/">Reviews</a>\n <a href="/about/">About</a>', 1)
        c_nav = 1
    counts["fb"]+=c_fb; counts["li"]+=c_li; counts["tw"]+=c_tw; counts["goog"]+=c_goog; counts["nav"]+=c_nav
    if t != orig:
        files_changed += 1
        if apply:
            with open(path,"w",encoding="utf-8") as fh: fh.write(t)

for dp,dn,fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if f.endswith(".html"):
            process(os.path.join(dp,f))

print(("APPLIED" if apply else "DRY RUN"))
print(f"files changed: {files_changed}")
print(f"  facebook href/sameAs updated : {counts['fb']}")
print(f"  linkedin href/sameAs updated : {counts['li']}")
print(f"  twitter -> youtube anchors   : {counts['tw']}")
print(f"  google icon added (footers)  : {counts['goog']}")
print(f"  Reviews nav link added       : {counts['nav']}")
# leftover scan
left_tw = 0; left_fb = 0
for dp,dn,fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if f.endswith(".html"):
            with open(os.path.join(dp,f),encoding="utf-8") as fh: c=fh.read()
            if not apply: continue
            left_tw += c.count("twitter.com/janetgiles")
            left_fb += c.count("facebook.com/CSIRealtyTeam")
if apply:
    print(f"\nleftover twitter/janetgiles: {left_tw}  |  leftover facebook/CSIRealtyTeam: {left_fb} (both should be 0)")
else:
    print("\nDRY RUN — nothing written.")
