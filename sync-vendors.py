#!/usr/bin/env python3
"""Pull the YRL hub vendor directory (Supabase hub_content 'yrl-vendors-state')
into vendors.json, which build_vendors.py renders. Mirrors sync-roster.py.

The broker curates vendors in the hub (yrl-vendors.html): each vendor has a
`site` flag (show on the public website) and a `featured` flag (⭐ pin to top).
This script snapshots the current directory; run it (then build_vendors.py) to
publish changes.

Usage:  python3 sync-vendors.py         # writes vendors.json
        python3 sync-vendors.py --dry   # print summary, write nothing
"""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "vendors.json")
SB_URL = "https://wdvolamasztetwpitbwg.supabase.co"
SB_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
          "Indkdm9sYW1hc3p0ZXR3cGl0YndnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3Nzc2"
          "MTYsImV4cCI6MjA5MTM1MzYxNn0.uiGIaZwr88ZNtAobfSV-axlpXB3sos2Rcw3FiFm6JO8")
DRY = "--dry" in sys.argv

def fetch():
    url = f"{SB_URL}/rest/v1/rpc/get_yrl_vendors"
    req = urllib.request.Request(url, data=b"{}", method="POST",
        headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        val = json.load(r)
    if not isinstance(val, dict) or "categories" not in val:
        raise SystemExit("get_yrl_vendors returned no vendor state")
    return val

def main():
    state = fetch()
    rows = []
    for cat in state.get("categories", []):
        cname = cat.get("name", "")
        for v in cat.get("vendors", []):
            if not (v.get("company") or "").strip():
                continue
            rows.append({
                "category": cname,
                "company": v.get("company", ""),
                "contact": v.get("contact") or "",
                "phone": v.get("phone") or "",
                "website": v.get("website") or "",
                "notes": v.get("notes") or "",
                # curation flags (default: shown, not featured)
                "site": v.get("site", True) is not False,
                "featured": bool(v.get("featured")),
            })
    shown = [r for r in rows if r["site"]]
    feat = [r for r in shown if r["featured"]]
    print(f"vendors: {len(rows)} total · {len(shown)} shown on site · {len(feat)} featured")
    if DRY:
        return
    json.dump(rows, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", os.path.relpath(OUT, ROOT))

if __name__ == "__main__":
    main()
