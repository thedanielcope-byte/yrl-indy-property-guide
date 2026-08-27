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
SEARCH_BASE = "https://yourrealtylink.com/property-search"    # YRL's Agent3000 IDX
EMBED_SNIPPET = ""            # paste the dedicated IDX widget/iframe here for embed mode


def _url(param, value):
    return "%s?%s=%s" % (SEARCH_BASE, param, quote_plus(str(value)))

def city_search_url(city):        return _url("city", city)          # confirmed
def county_search_url(county):    return _url("county", county)      # value = county name, e.g. "Hamilton"
def subdivision_search_url(name): return _url("subdivision", name)   # deferred to embed mode
