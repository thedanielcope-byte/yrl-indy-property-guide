#!/usr/bin/env python3
"""Make /search/?q=... filter the Displet IDX embed.

The site's search boxes (homepage hero, agent pages) send the typed text to
/search/?q=<text>. This injects a marker-wrapped block into search/index.html that
parses q and rebuilds the iframe's base_query (base64 of Displet property filters).

Filters verified against the live embed (Oct 2026):
  street_address=<tokens>   token-prefix match on the street address only, case-insensitive
                            ("1255 franklin" finds "1255 N Franklin Road"); a street suffix or
                            city word that isn't in the MLS address returns nothing, so both
                            are stripped before sending
  city=<name>               case-insensitive
  postal_code=<zip>
  listing_id=<MLS #>
(`query=`, `address=`, `street_name=`, `mls_id=` are ignored by the embed.)

City names come from county_towns.json. Idempotent: re-run after editing that file
or the search page. The iframe itself is left untouched, so with no q (or no JS)
the page shows the full All-MLS feed exactly as before.
"""
import json, re, sys

PAGE = "search/index.html"
START, END = "<!-- IDX-QUERY -->", "<!-- /IDX-QUERY -->"
S_START, S_END = "<!-- IDX-QUERY-JS -->", "<!-- /IDX-QUERY-JS -->"
EMBED_BASE = "https://cms.mysolidearth.com/embed/websites/36/resources/138"
USER_ID = "6024260"

towns = json.load(open("county_towns.json"))
cities = sorted({t.strip() for lst in towns.values() for t in lst if t.strip()})
city_map = {re.sub(r"[^a-z0-9 ]", " ", c.lower()).strip(): c for c in cities}

STATUS = f"""{START}
 <div id="idxQuery" hidden style="margin:0 0 14px;padding:12px 16px;background:#f7f7f7;border:1px solid #e2e2e2;border-radius:10px;font-size:.95rem;color:#1a1a1a;">
 <span id="idxQueryText" style="font-weight:600;"></span>
 <span style="color:#6e6e70;"> Don&rsquo;t see it? Use the search bar in the listings below (address, MLS #, or location), or <a href="/search/" style="color:#c03926;font-weight:600;">show all listings</a>.</span>
 </div>
{END}
"""

SCRIPT = f"""{S_START}
<script>
(function(){{
 var raw=(new URLSearchParams(location.search).get('q')||'').trim();
 if(!raw) return;
 var CITIES={json.dumps(city_map, separators=(',', ':'))};
 var SUFFIX=/^(dr|drive|st|street|rd|road|ave|avenue|ln|lane|ct|court|blvd|boulevard|way|pl|place|cir|circle|pkwy|parkway|trl|trail|ter|terrace)$/;
 var FILLER=/^(homes|houses|house|home|for|sale|near|listings|real|estate|properties|property)$/;
 var s=raw.toLowerCase().replace(/[^a-z0-9#\\s]/g,' ').replace(/\\s+/g,' ').trim();
 var f={{}}, label='';
 var mls=s.match(/^(?:mls\\s*#?\\s*|#\\s*)?(\\d{{8}})$/);
 if(mls){{ f.listing_id=mls[1]; label='Showing MLS # '+mls[1]+'.'; }}
 else{{
  var hasDigit=/\\d/.test(s);
  var t=s.replace(/#/g,' ').split(' ').filter(function(w){{ return w && w!=='in' && w!=='indiana' && (hasDigit || !FILLER.test(w)); }});
  var zip='', city='';
  if(t.length && /^\\d{{5}}$/.test(t[t.length-1]) && (t.length===1 || t.length>2 || !/^\\d+$/.test(t[0]))) zip=t.pop();
  for(var n=Math.min(3,t.length); n>0 && !city; n--){{
   var cand=t.slice(t.length-n).join(' '), rest=t.slice(0,t.length-n);
   if(CITIES[cand] && (rest.length===0 || rest.some(function(w){{ return !/^\\d+$/.test(w); }}))){{ city=CITIES[cand]; t=rest; }}
  }}
  if(t.length>1 && SUFFIX.test(t[t.length-1])) t.pop();
  var street=t.join(' ');
  if(street) f.street_address=street;
  if(city) f.city=city;
  if(zip) f.postal_code=zip;
  if(street) label='Showing listings matching \\u201c'+street+'\\u201d'+(city?' in '+city:'')+(zip?' ('+zip+')':'')+'.';
  else if(city) label='Showing listings in '+city+(zip?' ('+zip+')':'')+'.';
  else if(zip) label='Showing listings in ZIP '+zip+'.';
 }}
 var parts=[]; for(var k in f) parts.push(k+'='+f[k]);
 if(!parts.length) return;
 var frame=document.querySelector('.idx-embed iframe');
 if(!frame) return;
 frame.src='{EMBED_BASE}?base_query[Property]='+encodeURIComponent(btoa(parts.join('&')))+'&user_id={USER_ID}';
 var box=document.getElementById('idxQuery');
 if(box){{ document.getElementById('idxQueryText').textContent=label; box.hidden=false; }}
}})();
</script>
{S_END}
"""

html = open(PAGE, encoding="utf-8").read()

# status line: just before the embed wrapper
if START in html:
    html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda m: STATUS, html, flags=re.S)
else:
    anchor = ' <div class="idx-embed">'
    if anchor not in html:
        sys.exit("idx-embed anchor not found in " + PAGE)
    html = html.replace(anchor, STATUS + anchor, 1)

# script: right after the iframe closes, so it runs as soon as the iframe is parsed
if S_START in html:
    html = re.sub(re.escape(S_START) + r".*?" + re.escape(S_END) + r"\n", lambda m: SCRIPT, html, flags=re.S)
else:
    m = re.search(r'<div class="idx-embed">.*?</iframe>\n', html, re.S)
    if not m:
        sys.exit("iframe not found in " + PAGE)
    html = html[:m.end()] + SCRIPT + html[m.end():]

open(PAGE, "w", encoding="utf-8").write(html)
print(f"search query handler injected into {PAGE} ({len(city_map)} city names)")
