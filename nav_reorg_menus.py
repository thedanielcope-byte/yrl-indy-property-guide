#!/usr/bin/env python3
"""Reorganize the Buyers & Sellers nav dropdowns site-wide:
 - group items with plain dividers
 - remove the duplicated 'Senior Living' + 'Market Updates' from both menus
 - move Market Updates into the Local Resources dropdown
 - move Senior Living into the Meet Our Agents dropdown
HTML-only, idempotent (each old string disappears after its replacement)."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1) Sellers: group + drop Senior Living/Market Updates
old_sell = (
 ' <a href="/services/sell-my-home/">Sell My Home</a>\n'
 ' <a href="/services/pricing-your-home/">Pricing Your Home</a>\n'
 ' <a href="/services/home-staging/">Home Staging</a>\n'
 ' <a href="/services/expired-listings/">Expired Listings</a>\n'
 ' <a href="/services/for-sale-by-owner/">For Sale By Owner</a>\n'
 ' <a href="/services/seller-closing-checklist/">Closing Checklist</a>\n'
 ' <a href="/senior-living/">Senior Living</a> <a href="/market-updates/">Market Updates</a>')
new_sell = (
 ' <a href="/services/sell-my-home/">Sell My Home</a>\n'
 ' <a href="/services/pricing-your-home/">Pricing Your Home</a>\n'
 ' <a href="/services/home-staging/">Home Staging</a>\n'
 ' <div class="nav-submenu-divider"></div>\n'
 ' <a href="/services/expired-listings/">Expired Listings</a>\n'
 ' <a href="/services/for-sale-by-owner/">For Sale By Owner</a>\n'
 ' <div class="nav-submenu-divider"></div>\n'
 ' <a href="/services/seller-closing-checklist/">Closing Checklist</a>')

# 2) Buyers: group + drop Senior Living/Market Updates
old_buy = (
 ' <a href="/services/home-buying-process/">The Home Buying Process</a>\n'
 ' <a href="/services/first-time-home-buyers/">First Time Buyers</a>\n'
 ' <a href="/services/buyer-representation/">Buyer Representation</a>\n'
 ' <a href="/services/new-construction/">New Construction</a>\n'
 ' <a href="/services/relocation-buyers/">Relocating to Indianapolis</a>\n'
 ' <a href="/services/mortgages/">Mortgages</a>\n'
 ' <a href="/services/down-payment-assistance/">Down Payment Help</a>\n'
 ' <a href="/services/buyer-closing-checklist/">Closing Checklist</a>\n'
 ' <a href="/senior-living/">Senior Living</a> <a href="/market-updates/">Market Updates</a>')
new_buy = (
 ' <a href="/services/home-buying-process/">The Home Buying Process</a>\n'
 ' <a href="/services/first-time-home-buyers/">First Time Buyers</a>\n'
 ' <a href="/services/buyer-representation/">Buyer Representation</a>\n'
 ' <div class="nav-submenu-divider"></div>\n'
 ' <a href="/services/mortgages/">Mortgages</a>\n'
 ' <a href="/services/down-payment-assistance/">Down Payment Help</a>\n'
 ' <div class="nav-submenu-divider"></div>\n'
 ' <a href="/services/new-construction/">New Construction</a>\n'
 ' <a href="/services/relocation-buyers/">Relocating to Indianapolis</a>\n'
 ' <a href="/services/buyer-closing-checklist/">Closing Checklist</a>')

# 3) Local Resources: add Market Updates
old_lr = ' <a href="/resources/">Free Guides &amp; Resources</a>\n </div>'
new_lr = ' <a href="/resources/">Free Guides &amp; Resources</a>\n <a href="/market-updates/">Market Updates</a>\n </div>'

# 4) Meet Our Agents: add Senior Living
old_ma = ' <a href="/services/referral-program/">Referral Program</a>\n </div>'
new_ma = ' <a href="/services/referral-program/">Referral Program</a>\n <a href="/senior-living/">Senior Living</a>\n </div>'

PAIRS = [("sellers", old_sell, new_sell), ("buyers", old_buy, new_buy),
         ("local-resources", old_lr, new_lr), ("meet-agents", old_ma, new_ma)]

counts = {k: 0 for k, _, _ in PAIRS}
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    orig = s
    for key, old, new in PAIRS:
        if old in s:
            s = s.replace(old, new)
            counts[key] += 1
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)

for k in counts:
    print("%-16s applied on %d pages" % (k, counts[k]))
