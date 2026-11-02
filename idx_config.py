#!/usr/bin/env python3
"""Single switch-point for IDX / MLS listings across the whole site.

The listings slot is injected site-wide by inject_idx.py and wrapped in
<!-- IDX-LISTINGS --> ... <!-- /IDX-LISTINGS --> markers, so it lives in ONE
place. To change or upgrade the IDX, edit THIS file and re-run inject_idx.py —
no per-page work.

  MODE = "deeplink"  (now)  -> each page links to YRL's live MLS search
                              (Agent3000 at yourrealtylink.com/property-search),
                              pre-filtered by city / county. Zero new cost.
  MODE = "embed"     (later) -> when Dan's dedicated IDX link is live, set
                              EMBED_SNIPPET to the vendor's widget/iframe code
                              and flip MODE. The same slot then renders a live
                              listings grid on every city/community/county/
                              neighborhood page. One config change + one re-run.

Confirmed working: the Agent3000 search honors ?city=<City> (GET form, the city
filter pre-selects from the URL). County/subdivision param value formats are
best-effort for the interim — worst case the search opens unfiltered.
"""
from urllib.parse import quote_plus

MODE = "deeplink"                                             # "deeplink" | "embed"
# LIVE (Sep 2026): Displet IDX Pro is provisioned. The full MLS search is embedded
# on the on-site /search/ page (Displet All-MLS feed, cms.mysolidearth.com, user
# 6024260 — domain-locked to yourrealtylink.com). Every city/county/community slot
# deep-links to /search/; city slots add ?q=<town>, which /search/ turns into a Displet
# city filter (inject_search_query.py). County/subdivision slots stay on the full search.
# FUTURE (per-city listings on each page): either make /search/ read a ?city= param
# and inject it into the Displet iframe src, or set MODE="embed" + EMBED_SNIPPET to a
# city-filtered Displet iframe — both need Displet's city/area field name (ask support).
SEARCH_BASE = "/search/"                                      # on-site Displet search hub
DEEPLINK_PARAMS = False                                       # /search/ ignores query params (fixed All-MLS embed)
EMBED_SNIPPET = ""            # paste a city-filtered Displet iframe here to switch to inline embeds


def _url(param, value):
    if not DEEPLINK_PARAMS:
        return SEARCH_BASE
    return "%s?%s=%s" % (SEARCH_BASE, param, quote_plus(str(value)))

_TOWNS = None


def _known_town(city):
    """True when /search/?q=<city> filters the Displet feed (see inject_search_query.py,
    which recognizes the towns in county_towns.json)."""
    global _TOWNS
    if _TOWNS is None:
        import json, os, re
        try:
            towns = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "county_towns.json")))
            _TOWNS = {re.sub(r"[^a-z0-9 ]", " ", t.lower()).strip() for lst in towns.values() for t in lst if t.strip()}
        except Exception:
            _TOWNS = set()
    import re
    return re.sub(r"[^a-z0-9 ]", " ", str(city or "").lower()).strip() in _TOWNS


def city_search_url(city):
    # Nov 2026: /search/ reads ?q= and filters by city (inject_search_query.py), so town
    # slots open that town's listings; unknown names fall back to the full search.
    from urllib.parse import quote
    zips = {"broad ripple": "46220", "irvington": "46219", "camby": "46113", "eagle creek": "46254"}   # not MLS cities
    if str(city or "").strip().lower() in zips:
        return "%s?q=%s" % (SEARCH_BASE, zips[str(city).strip().lower()])
    return "%s?q=%s" % (SEARCH_BASE, quote(str(city))) if _known_town(city) else SEARCH_BASE
def county_search_url(county):    return _url("county", county)      # value = county name, e.g. "Hamilton"
def subdivision_search_url(name): return _url("subdivision", name)   # deferred to embed mode
