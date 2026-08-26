#!/usr/bin/env python3
"""Shared "New to the Area? Local Essentials" block — official links a new
Central Indiana resident needs after closing (BMV, USPS, voter registration,
homestead deduction, hospitals). Used on the utilities guide and the buyer
closing checklist. Self-contained (inline scoped <style>), so it drops into any
generated page without touching the global stylesheet.

All links verified official government / healthcare URLs (no fabrication)."""

ITEMS = [
 ("https://www.in.gov/bmv/", "Indiana BMV",
  "Register your vehicle and get an Indiana driver's license — new residents generally have 60 days."),
 ("https://tools.usps.com/find-location.htm", "Find Your Post Office",
  "Locate your new post office, and set up USPS mail forwarding to your new address."),
 ("https://indianavoters.in.gov/", "Register to Vote",
  "Update your Indiana voter registration once you're at your new address."),
 ("https://www.in.gov/dlgf/deductions-property-tax/", "Homestead Deduction",
  "Lower the property taxes on your primary home — file with your county auditor."),
 ("https://iuhealth.org/", "Local Hospitals",
  "Central Indiana's major systems: IU Health, Community Health Network, Ascension St. Vincent &amp; Franciscan Health."),
]

_STYLE = """<style>
.local-essentials { background: var(--light); border: 1px solid var(--border); border-radius: 14px; padding: 22px 24px; margin: 1.7rem 0; }
.local-essentials > h2 { margin: 0 0 4px; font-size: 1.2rem; color: #13294a; }
.local-essentials > p { margin: 0 0 14px; color: var(--mid); font-size: .92rem; }
.le-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
.le-item { display: block; background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 13px 15px; text-decoration: none; transition: border-color .15s, box-shadow .15s; }
.le-item:hover { border-color: var(--red); box-shadow: 0 4px 14px rgba(0,0,0,.06); }
.le-item strong { display: block; color: var(--red); font-size: .95rem; margin-bottom: 2px; }
.le-item span { color: #33373b; font-size: .83rem; line-height: 1.45; }
.le-note { font-size: .78rem; color: var(--mid); margin: 13px 0 0; }
</style>"""

def block():
    cards = "\n ".join(
        '<a class="le-item" href="%s" target="_blank" rel="noopener"><strong>%s &#8599;</strong>'
        '<span>%s</span></a>' % (url, name, desc)
        for url, name, desc in ITEMS)
    return (_STYLE + '\n<section class="local-essentials">\n'
            ' <h2 id="local-essentials">🧭 New to the Area? Local Essentials</h2>\n'
            ' <p>Just moved to Central Indiana? A few official links to help you get settled &mdash; beyond your utilities.</p>\n'
            ' <div class="le-grid">\n ' + cards + '\n </div>\n'
            ' <p class="le-note">Official government and healthcare links, provided for your convenience. '
            'Your Realty Link is not affiliated with them.</p>\n</section>')
