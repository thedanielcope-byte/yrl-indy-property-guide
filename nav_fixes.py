#!/usr/bin/env python3
"""Site-wide nav fixes + additions (idempotent, exact-string .replace):
 1. Buyers parent  -> /services/home-buying-process/
 2. Sellers parent -> /services/home-selling-process/
 3. Free Home Valuation item: /contact/ -> /services/free-home-valuation/
 4. add 'The Home Selling Process' to Sellers dropdown
 5. add Investment Properties + Land & Acreage to Buyers dropdown
 6. add School Districts + Communities + Neighborhoods to Local Resources
 7. add "We're Hiring — Join YRL" to Meet Our Agents
"""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

R = [
 # (label, old, new)
 ("buyers-parent",
  '<a href="/first-time-home-buyers-indianapolis/">Buyers</a>',
  '<a href="/services/home-buying-process/">Buyers</a>'),
 ("sellers-parent",
  '<a href="/sell-my-home-indianapolis/">Sellers</a>',
  '<a href="/services/home-selling-process/">Sellers</a>'),
 ("free-home-valuation",
  '<a href="/contact/">Free Home Valuation</a>',
  '<a href="/services/free-home-valuation/">Free Home Valuation</a>'),
 ("home-selling-process-item",
  ' <div class="nav-submenu-divider"></div>\n <a href="/services/sell-my-home/">Sell My Home</a>',
  ' <div class="nav-submenu-divider"></div>\n <a href="/services/home-selling-process/">The Home Selling Process</a>\n <a href="/services/sell-my-home/">Sell My Home</a>'),
 ("buyers-investment-land",
  ' <a href="/services/new-construction/">New Construction</a>\n <a href="/services/relocation-buyers/">Relocating to Indianapolis</a>',
  ' <a href="/services/new-construction/">New Construction</a>\n <a href="/services/investment-property/">Investment Properties</a>\n <a href="/homes-with-acreage-central-indiana/">Land &amp; Acreage</a>\n <a href="/services/relocation-buyers/">Relocating to Indianapolis</a>'),
 ("local-resources-add",
  ' <a href="/market-updates/">Market Updates</a>\n </div>',
  ' <a href="/market-updates/">Market Updates</a>\n <a href="/schools/">School Districts</a>\n <a href="/communities/">Communities &amp; Subdivisions</a>\n <a href="/neighborhoods/">Indianapolis Neighborhoods</a>\n </div>'),
 ("meet-agents-join",
  ' <a href="/services/referral-program/">Referral Program</a>\n </div>',
  ' <a href="/services/referral-program/">Referral Program</a>\n <a href="/services/join-yrl/">We&rsquo;re Hiring &mdash; Join YRL</a>\n </div>'),
]

counts = {k: 0 for k, _, _ in R}
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read(); orig = s
    for key, old, new in R:
        if old in s:
            s = s.replace(old, new); counts[key] += 1
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
for k, _, _ in R:
    print("%-26s applied on %d pages" % (k, counts[k]))
