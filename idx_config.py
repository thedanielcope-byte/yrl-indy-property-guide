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
# deep-links to /search/. DEEPLINK_PARAMS is off because the on-site /search/ page
# currently ignores query params (fixed All-MLS iframe).
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

def city_search_url(city):        return _url("city", city)          # confirmed
def county_search_url(county):    return _url("county", county)      # value = county name, e.g. "Hamilton"
def subdivision_search_url(name): return _url("subdivision", name)   # deferred to embed mode
