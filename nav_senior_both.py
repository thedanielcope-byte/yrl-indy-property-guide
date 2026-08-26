#!/usr/bin/env python3
"""Move 'Senior Living' out of Meet Our Agents and back into BOTH the Buyers and
Sellers dropdowns (it serves downsizing sellers and 55+ buyers). Market Updates
stays in Local Resources. HTML-only, idempotent, site-wide."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1) remove Senior Living from Meet Our Agents
old_ma = ' <a href="/services/referral-program/">Referral Program</a>\n <a href="/senior-living/">Senior Living</a>\n </div>'
new_ma = ' <a href="/services/referral-program/">Referral Program</a>\n </div>'

# 2) add Senior Living to Sellers (specialty-situations group)
old_sell = (' <a href="/services/for-sale-by-owner/">For Sale By Owner</a>\n'
            ' <div class="nav-submenu-divider"></div>\n'
            ' <a href="/services/seller-closing-checklist/">Closing Checklist</a>')
new_sell = (' <a href="/services/for-sale-by-owner/">For Sale By Owner</a>\n'
            ' <a href="/senior-living/">Senior Living</a>\n'
            ' <div class="nav-submenu-divider"></div>\n'
            ' <a href="/services/seller-closing-checklist/">Closing Checklist</a>')

# 3) add Senior Living to Buyers (last group)
old_buy = (' <a href="/services/relocation-buyers/">Relocating to Indianapolis</a>\n'
           ' <a href="/services/buyer-closing-checklist/">Closing Checklist</a>')
new_buy = (' <a href="/services/relocation-buyers/">Relocating to Indianapolis</a>\n'
           ' <a href="/senior-living/">Senior Living</a>\n'
           ' <a href="/services/buyer-closing-checklist/">Closing Checklist</a>')

PAIRS = [("meet-agents", old_ma, new_ma), ("sellers", old_sell, new_sell), ("buyers", old_buy, new_buy)]
counts = {k: 0 for k, _, _ in PAIRS}
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read(); orig = s
    for key, old, new in PAIRS:
        if old in s:
            s = s.replace(old, new); counts[key] += 1
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
for k in counts:
    print("%-14s applied on %d pages" % (k, counts[k]))
