#!/usr/bin/env python3
"""Write cloudflare-redirects.csv: a Cloudflare Bulk Redirects import built from the site's meta-refresh
redirect stubs (Nov 2026).

GitHub Pages can't send real 301s, so legacy URLs use meta-refresh stub pages. Once yourrealtylink.com's
DNS is proxied through Cloudflare (orange cloud, SSL mode Full — NOT Full (Strict), since GitHub Pages
may not renew its cert behind the proxy), import this CSV as a Bulk Redirect List and enable it with a
Bulk Redirect Rule. The stubs stay in the repo as a fallback.

LIVE since Nov 20 2026: zone proxied (SSL Full, automatic mode off, email obfuscation off), account
Bulk Redirect list `yrl_legacy_redirects` (133 rows) + rule "yourrealtylink legacy 301s". When you add a
stub, re-run this script and add the new rows to that list in the dashboard (Bulk Redirects > list >
Add items); importing the whole CSV again would collide with the existing rows.

CSV columns (Cloudflare format): source,target,status,preserve_query_string,include_subdomains,
subpath_matching,preserve_path_suffix. Each stub gets a with- and without-trailing-slash row;
/blog/archives/, /blog/category/ and /listing/ are subpath catch-alls; /market-trends/ is skipped
(its ?city= router needs the page); www -> apex is handled at the edge.
Re-run after adding stubs: python3 build_cf_redirects.py
"""
import re, glob, urllib.parse

H = "yourrealtylink.com"
PARENTS = {"/blog/archives/": "/blog/", "/blog/category/": "/blog/", "/listing/": "/search/"}
SKIP = {"/market-trends/"}
rows, seen = [], set()

def add(src, tgt, sub=False):
    if src in seen: return
    seen.add(src)
    rows.append(f"{H}{src},https://{H}{tgt},301,false,false,{'true' if sub else 'false'},false")

for p, t in PARENTS.items():
    add(p, t, sub=True); add(p.rstrip("/"), t)
for f in sorted(glob.glob("**/index.html", recursive=True)):
    s = open(f, encoding="utf-8", errors="ignore").read()
    m = re.search(r'<meta[^>]+http-equiv=["\']refresh["\'][^>]*>', s, re.I)
    if not m: continue
    tgt = re.search(r'url=([^"\'>]+)', m.group(), re.I).group(1).strip()
    path = "/" + f[:-len("index.html")]
    if path in SKIP or any(path.startswith(p) for p in PARENTS): continue
    enc = urllib.parse.quote(path, safe="/+")
    add(enc, tgt); add(enc.rstrip("/"), tgt)
rows.append(f"www.{H}/,https://{H}/,301,true,false,true,true")
open("cloudflare-redirects.csv", "w").write("\n".join(rows) + "\n")
print(f"cloudflare-redirects.csv — {len(rows)} rows")
