#!/usr/bin/env python3
"""Full technical/SEO audit across every built page. Read-only: reports issues
grouped by category so they can be fixed. Covers title, meta description, H1,
canonical, viewport (mobile), OG image, JSON-LD schema validity, robots/noindex,
image alt text, broken internal links, and regressions from recent bulk edits."""
import os, re, json, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

SKIP = ("node_modules", "valuation-tool", ".git", "/YRL-Hub/")
pages = [p for p in glob.glob("**/*.html", recursive=True)
         if not any(s in ("/" + p) for s in SKIP)]

def rel(p): return p
def txt(pat, s, g=1, fl=re.S|re.I):
    m = re.search(pat, s, fl); return m.group(g).strip() if m else None

issues = {}
def add(cat, page, detail=""):
    issues.setdefault(cat, []).append((page, detail))

# build a set of existing local paths for link-checking
existing = set()
for p in glob.glob("**/*", recursive=True):
    existing.add("/" + p.replace("\\", "/"))

def target_exists(href):
    h = href.split("#")[0].split("?")[0]
    if not h.startswith("/"): return True            # external/anchor: skip
    if h in existing: return True
    h2 = h.rstrip("/")
    if h2 in existing: return True
    if (h2 + "/index.html") in existing: return True
    if (h.rstrip("/") + "/index.html") in existing: return True
    return False

NOINDEX_OK = ("/thank-you/", "/download/")           # intentionally noindex

for p in pages:
    s = open(p, encoding="utf-8").read()
    is_thankyou = any(x in ("/" + p) for x in NOINDEX_OK)

    # title
    t = txt(r"<title>(.*?)</title>", s)
    if not t: add("missing-title", p)
    elif len(t) > 65: add("title-too-long", p, f"{len(t)}c: {t[:70]}")

    # meta description
    d = txt(r'<meta name="description" content="(.*?)"', s)
    if not d and not is_thankyou: add("missing-meta-desc", p)
    elif d and len(d) > 165: add("meta-desc-too-long", p, f"{len(d)}c")
    elif d and len(d) < 70 and not is_thankyou: add("meta-desc-too-short", p, f"{len(d)}c: {d}")

    # H1
    h1s = re.findall(r"<h1[ >]", s)
    if len(h1s) == 0 and not is_thankyou: add("no-h1", p)
    elif len(h1s) > 1: add("multiple-h1", p, f"{len(h1s)} h1s")

    # canonical
    can = txt(r'<link rel="canonical" href="(.*?)"', s)
    if not can and not is_thankyou: add("missing-canonical", p)
    elif can and "janetgiles.com" not in can and not is_thankyou: add("canonical-wrong-domain", p, can)

    # viewport (mobile)
    if 'name="viewport"' not in s: add("missing-viewport", p)

    # OG image
    if 'property="og:image"' not in s and not is_thankyou: add("missing-og-image", p)

    # JSON-LD validity
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(block)
        except Exception as e: add("invalid-jsonld", p, str(e)[:50])

    # robots noindex on a page that should index
    if re.search(r'<meta name="robots"[^>]*noindex', s, re.I) and not is_thankyou:
        add("unexpected-noindex", p)

    # images without alt
    imgs = re.findall(r"<img\b[^>]*>", s, re.I)
    noalt = [i for i in imgs if not re.search(r'\balt=', i)]
    if noalt: add("img-no-alt", p, f"{len(noalt)} img(s)")

    # broken internal links
    for href in re.findall(r'href="(/[^"#]*)"', s):
        if href.startswith("/assets") or href.endswith((".css", ".js", ".png", ".jpg", ".webp", ".pdf", ".xml", ".ico")):
            if not target_exists(href): add("broken-asset-link", p, href)
            continue
        if not target_exists(href): add("broken-internal-link", p, href)

    # regressions from bulk edits
    if "&lt;p&gt;" in s or "&lt;em&gt;" in s or "&lt;a href" in s: add("entity-encoded-html", p)
    is_general = not any(x in ("/" + p) for x in ("/blog/", "/resources/", "/agents/"))
    if is_general:
        for bad in ("Daniel Cope and", "Call Daniel", "Talk to Daniel", "call Daniel"):
            if bad in s and "daniel-cope.jpg" not in s.split(bad)[0][-200:]:
                add("name-in-general-copy", p, bad); break
    if "coming soon" in s.lower(): add("coming-soon-stub", p)

# report
print(f"AUDITED {len(pages)} pages\n" + "="*60)
order = ["missing-title","title-too-long","missing-meta-desc","meta-desc-too-short","meta-desc-too-long",
         "no-h1","multiple-h1","missing-canonical","canonical-wrong-domain","missing-viewport","missing-og-image",
         "invalid-jsonld","unexpected-noindex","broken-internal-link","broken-asset-link","img-no-alt",
         "entity-encoded-html","name-in-general-copy","coming-soon-stub"]
clean = True
for cat in order:
    v = issues.get(cat)
    if not v: continue
    clean = False
    print(f"\n[{cat}] {len(v)}")
    for page, detail in v[:8]:
        print(f"   {page}  {detail}")
    if len(v) > 8: print(f"   … +{len(v)-8} more")
# any categories not in order
for cat, v in issues.items():
    if cat not in order:
        clean = False; print(f"\n[{cat}] {len(v)}")
        for page, detail in v[:8]: print(f"   {page}  {detail}")
if clean: print("\nNo issues found — clean.")
