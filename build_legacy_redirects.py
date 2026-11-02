#!/usr/bin/env python3
"""Redirect stubs for old-site URLs that Search Console reports as 404 (Nov 2026 list).

GitHub Pages has no server redirects, so each old path gets a small page with a canonical
tag, noindex, an instant meta refresh and a JS replace (same pattern as the Sept 2026
Agent3000 stubs). Old blog posts point to the closest current page; archive, category and
paging URLs point to /blog/; old IDX listing pages point to /search/. /market-trends/
reads ?city= and sends visitors to that town's page (else the market-updates hub).
Never overwrites a real page. Re-runnable.
"""
import html, json, os

MAP = {
 # old blog posts -> closest current page
 "blog/homestead-and-mortgage-exemptions-deadline": "/blog/indiana-homestead-exemption-lower-property-taxes/",
 "blog/can-you-have-a-tax-lein-buy-a-home": "/glossary/lien/",
 "blog/the-top-reasons-to-use-a-realtor-when-buying-or-selling-a-house-in-indiana": "/compare/realtor-vs-fsbo/",
 "blog/southport-real-estate-small-town-charm-with-big-city-access": "/cities/marion-county/southport-indiana-real-estate/",
 "blog/3-questions-to-ask-before-buying-your-dream-home": "/services/home-buying-process/",
 "blog/downsizing-made-easy": "/services/downsizing/",
 "blog/is-downsizing-in-your-future": "/services/downsizing/",
 "blog/janet-giles-named-five-star-agent": "/agents/janet-giles/",
 "blog/the-current-state-of-the-real-estate-market-in-indy": "/market-updates/",
 "blog/indiana-real-estate-market-update-whats-happening-now": "/market-updates/",
 "blog/who-qualifies-for-an-fha-loan": "/services/fha-loan-buyers/",
 "blog/selling-your-home-top-questions-and-expert-answers": "/services/home-selling-process/",
 "blog/why-selling-your-home-right-now-could-be-a-smart-move": "/services/home-selling-process/",
 "blog/training-video-type-of-surveys": "/blog/property-survey-types-buying-home-indianapolis/",
 "blog/check-out-our-southside-office": "/contact/",
 "blog/small-rental-spaces-available-on-south-side-of-indy": "/contact/",
 "blog/interior-design-trends-to-make-your-home-look-more-expensive": "/blog/interior-paint-colors-indianapolis/",
 "blog/tips-to-make-your-home-beautiful-kid-friendly": "/blog/family-friendly-home-design-indianapolis/",
 "blog/why-isnt-your-home-selling-insights-here": "/services/expired-listings/",
 "blog/how-to-find-the-right-neighborhood-for-your-family": "/blog/choosing-a-neighborhood-indianapolis/",
 "blog/why-must-i-sign-a-buyer-agreement": "/glossary/buyers-agency-agreement/",
 "blog/how-can-personalized-consultations-from-your-realty-link-benefit-my-specific-real-estate-needs": "/schedule/",
 "blog/martin-house-by-frank-lloyd-wright-is-a-must-see-in-person": "/blog/",
 "blog/the-hottest-trend-barndominiums": "/blog/",
 "blog/the-ultimate-guide-to-keeping-your-house-cool-during-the-summer": "/blog/",
 "blog/5-questions-buyers-have-about-covid": "/blog/",
 "blog/barn-doors-is-the-trend-over": "/blog/",
 "blog/creative-ideas-for-decorating-your-home-on-a-budget": "/blog/",
 "blog/farmhouse-trend-gets-an-update": "/blog/",
 # old agent directory
 "agent-list": "/agents/",
}
ARCHIVES = ["0/0", "2018/1", "2019/1", "2019/12", "2021/1", "2021/1/page/1", "2021/2", "2021/3", "2021/5",
            "2023/6", "2023/7", "2023/8", "2023/9", "2023/12", "2024/5", "2024/6", "2024/7", "2025/4", "2025/11"]
for a in ARCHIVES:
    MAP["blog/archives/" + a] = "/blog/"
for c in ["Real Estate Career", "Market+Data", "Market Data", "Selling", "New Build", "Inspriation", "First Time Homebuyer"]:
    MAP["blog/category/" + c] = "/blog/"
MAP["blog/page/2"] = "/blog/"
for lid in ["21780790", "22121247", "22116609", "22115443", "22103112", "22080457", "21777342"]:
    MAP["listing/" + lid] = "/search/"
MAP["listing"] = "/search/"


def stub(dest, label):
    d = html.escape(dest)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={d}">
<link rel="canonical" href="https://yourrealtylink.com{d}">
<meta name="robots" content="noindex, follow">
<title>{html.escape(label)} | Your Realty Link</title>
<script>location.replace("{d}");</script>
</head>
<body>
<p>This page has moved to <a href="{d}">{html.escape(label)}</a>.</p>
</body>
</html>
'''


def label_for(dest):
    s = dest.strip("/").split("/")[-1] or "home"
    return {"blog": "the Your Realty Link blog", "search": "home search", "agents": "our agents", "contact": "contact us",
            "schedule": "schedule a consultation", "market-updates": "Indianapolis market updates"}.get(s, s.replace("-", " ").title())


made = skipped = 0
for path, dest in MAP.items():
    assert os.path.exists(dest.strip("/") + "/index.html") or dest == "/", dest
    f = os.path.join(path, "index.html")
    if os.path.exists(f) and 'http-equiv="refresh"' not in open(f, encoding="utf-8").read():
        skipped += 1; continue          # never overwrite a real page
    os.makedirs(path, exist_ok=True)
    open(f, "w", encoding="utf-8").write(stub(dest, label_for(dest)))
    made += 1

# /market-trends/?city=X  -> that town's page (else market updates)
towns = {}
for county in os.listdir("cities"):
    if os.path.isdir(f"cities/{county}"):
        for t in os.listdir(f"cities/{county}"):
            if t.endswith("-real-estate"):
                name = t.replace("-indiana-real-estate", "").replace("-indianapolis-real-estate", "")
                towns[name] = f"/cities/{county}/{t}/"
os.makedirs("market-trends", exist_ok=True)
open("market-trends/index.html", "w", encoding="utf-8").write(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://yourrealtylink.com/market-updates/">
<title>Indianapolis Market Updates | Your Realty Link</title>
<script>
(function () {{
  var T = {json.dumps(towns, separators=(",", ":"))};
  var c = (new URLSearchParams(location.search).get("city") || "").toLowerCase().trim().replace(/['’]/g, "").replace(/[^a-z0-9]+/g, "-");
  location.replace(T[c] || "/market-updates/");
}})();
</script>
<meta http-equiv="refresh" content="2; url=/market-updates/">
</head>
<body>
<p>Market data has moved to our <a href="/market-updates/">Indianapolis market updates</a>.</p>
</body>
</html>
''')
print(f"redirect stubs: {made} written, {skipped} skipped (real pages); market-trends router covers {len(towns)} towns")
