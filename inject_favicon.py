#!/usr/bin/env python3
"""Add favicon / app-icon <link> tags to every page <head>. Idempotent.

The tags go just before the main stylesheet link, inside the head block that most
generators copy from index.html, so new pages pick them up automatically. Re-run after
any generator that builds <head> from scratch (wired into the GitHub Actions next to
inject_gtag.py). Icons live in /favicon.ico and /assets/img/icons/.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
STYLE = re.compile(r'(?m)^([ \t]*)<link rel="stylesheet" href="/assets/css/style\.css\?v=')
TAGS = ['<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icons/icon-192.png">',
        '<link rel="apple-touch-icon" href="/assets/img/icons/apple-touch-icon.png">']

added = had = nostyle = 0
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith(".") and d != "node_modules"]
    for f in fn:
        if not f.endswith(".html"):
            continue
        p = os.path.join(dp, f)
        s = open(p, encoding="utf-8", newline="").read()
        if 'rel="icon"' in s:
            had += 1; continue
        nl = "\r\n" if "\r\n" in s[:2000] else "\n"
        m = STYLE.search(s)
        if m:
            at, ind = m.start(), m.group(1)
        elif "assets/css/style.css" in s and "</head>" in s:   # one-line head blocks
            at, ind = s.index("</head>"), " "
        else:
            nostyle += 1; continue
        block = "".join(ind + t + nl for t in TAGS)
        open(p, "w", encoding="utf-8", newline="").write(s[:at] + block + s[at:])
        added += 1

print("favicon — added: %d | already had it: %d | no stylesheet link: %d" % (added, had, nostyle))
