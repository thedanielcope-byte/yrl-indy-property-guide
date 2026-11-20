#!/usr/bin/env python3
"""Add a "file your homestead deduction" line to each county hub, linking to that county's section of
/blog/how-to-file-homestead-deduction-indiana-by-county/ (Nov 2026).

Marker-wrapped (<!-- HOMESTEAD-LINK --> ... <!-- /HOMESTEAD-LINK -->), inserted just before the
<!-- SELLING --> section. Idempotent: re-running refreshes the block. Counties come from the post's
COUNTIES list so the anchors always match.
"""
import glob, importlib.util, re

POST = "how-to-file-homestead-deduction-indiana-by-county"
spec = importlib.util.spec_from_file_location("p", f"fresh_posts/{POST}.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
NAMES = [c["n"] for c in m.COUNTIES]
START, END = "<!-- HOMESTEAD-LINK -->", "<!-- /HOMESTEAD-LINK -->"

done = missing = 0
for n in NAMES:
    s = n.lower() + "-county"
    p = f"counties/{s}-indiana-real-estate/index.html"
    try:
        t = open(p, encoding="utf-8").read()
    except FileNotFoundError:
        print("missing page", p); missing += 1; continue
    block = (f'{START}\n <p><strong>Just bought a home in {n} County?</strong> File your homestead deduction with the {n} County '
             f'Auditor by January 15 of the year the taxes are due; it&rsquo;s the biggest property tax break most Indiana '
             f'homeowners get. Here&rsquo;s <a href="/blog/{POST}/#{s}">how to file in {n} County</a>.</p>\n {END}')
    if START in t:
        t2 = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, t, count=1, flags=re.S)
    elif "<!-- SELLING -->" in t:
        t2 = t.replace("<!-- SELLING -->", block + "\n\n <!-- SELLING -->", 1)
    else:
        print("no anchor", p); missing += 1; continue
    if t2 != t:
        open(p, "w", encoding="utf-8").write(t2); done += 1
print(f"homestead links — updated: {done} | missing/no anchor: {missing} | counties: {len(NAMES)}")
