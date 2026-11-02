#!/usr/bin/env python3
"""Quick whole-site health check before committing a batch of generated pages:
broken internal links, duplicate titles on indexable pages, meta descriptions over 160
characters, pages missing GA4 or the favicon tags, and iCloud-style "name 2.ext" dupes.
Usage: python3 site_scan.py [root]
"""
import collections, html, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
pages = {}
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if not d.startswith(".") and d != "node_modules"]
    for f in fn:
        if f.endswith(".html"):
            p = os.path.join(dp, f)
            pages[os.path.relpath(p, root)] = open(p, encoding="utf-8", errors="replace").read()


def exists(u):
    u = u.split("#")[0].split("?")[0]
    if not u.startswith("/"):
        return True
    p = os.path.join(root, u.lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))


broken = collections.Counter(); titles = collections.defaultdict(list)
longd, nog, noi, dup = [], [], [], []
for rel, s in pages.items():
    if " 2." in rel:
        dup.append(rel)
    for m in re.finditer(r'(?:href|src)="(/[^"]*)"', s):
        if not exists(m.group(1)):
            broken[(rel, m.group(1))] += 1
    if 'http-equiv="refresh"' in s:
        continue
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    if t and "noindex" not in s[:5000]:
        titles[html.unescape(t.group(1).strip())].append(rel)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if d and len(html.unescape(d.group(1))) > 160:
        longd.append(rel)
    if "<head" in s and "G-SNV86NLT23" not in s and "google" not in rel:
        nog.append(rel)
    if "assets/css/style.css" in s and 'rel="icon"' not in s:
        noi.append(rel)
dt = {k: v for k, v in titles.items() if len(v) > 1}
print(f"pages {len(pages)} | broken links {len(broken)} {list(broken)[:5]} | duplicate titles {len(dt)} {list(dt.items())[:3]} | "
      f"desc>160 {len(longd)} {longd[:3]} | no GA {len(nog)} {nog[:3]} | no favicon {len(noi)} {noi[:3]} | dupes {dup[:3]}")
