#!/usr/bin/env python3
"""
sync-roster.py — pull agent Specialties + Service Areas from the YRL hub.

The broker edits each agent's Specialties (expertise) and Service Areas (areas)
in the hub agent directory (yrlagent.com → Supabase `hub_content`). This script
pulls those two fields into agents-roster.json (matched by name) and rebuilds the
public agent pages, so the hub is the single source of truth for them.

Everything else in agents-roster.json (photo, lead flag, order, contact info) is
left untouched — only `expertise` and `areas` are synced.

Usage:
    python3 sync-roster.py          # pull, merge, rebuild pages
    python3 sync-roster.py --dry    # show what would change, write nothing
"""
import json, os, re, sys, subprocess, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ROSTER = os.path.join(ROOT, "agents-roster.json")

SB_URL = "https://wdvolamasztetwpitbwg.supabase.co"
SB_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
          "Indkdm9sYW1hc3p0ZXR3cGl0YndnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3Nzc2"
          "MTYsImV4cCI6MjA5MTM1MzYxNn0.uiGIaZwr88ZNtAobfSV-axlpXB3sos2Rcw3FiFm6JO8")
KEY = "yrl-agent-directory"

DRY = "--dry" in sys.argv


def norm(name):
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def fetch_remote():
    # Read the roster via a tightly-scoped, read-only RPC (get_yrl_roster).
    # The shared hub_content table's RLS hides this row from anon, so a plain
    # REST select returns nothing; the RPC exposes ONLY this one public row.
    url = f"{SB_URL}/rest/v1/rpc/get_yrl_roster"
    req = urllib.request.Request(
        url, data=b"{}", method="POST",
        headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        val = json.load(r)
    if not isinstance(val, list) or not val:
        raise SystemExit("get_yrl_roster returned no agents (expected a list)")
    return val


def clean_areas(areas):
    """Keep only well-formed [label, url] pairs."""
    out = []
    for a in areas or []:
        if isinstance(a, (list, tuple)) and len(a) >= 2 and a[0] and a[1]:
            out.append([str(a[0]), str(a[1])])
    return out


def main():
    remote = fetch_remote()
    rmap = {norm(a.get("name")): a for a in remote}

    local = json.load(open(ROSTER, encoding="utf-8"))
    changed, matched, unmatched = [], 0, []

    for a in local:
        r = rmap.get(norm(a.get("name")))
        if not r:
            unmatched.append(a.get("name"))
            continue
        matched += 1
        before = (a.get("expertise"), a.get("areas"))

        exp = [str(x) for x in (r.get("expertise") or []) if str(x).strip()]
        areas = clean_areas(r.get("areas"))

        # Mirror the hub: set when present, remove the key when empty so the
        # site falls back to defaults (expertise) / hides the section (areas).
        if exp:
            a["expertise"] = exp
        else:
            a.pop("expertise", None)
        if areas:
            a["areas"] = areas
        else:
            a.pop("areas", None)

        after = (a.get("expertise"), a.get("areas"))
        if before != after:
            changed.append(a.get("name"))

    print(f"matched {matched}/{len(local)} agents to the hub roster")
    if unmatched:
        print("  · no hub match (left as-is): " + ", ".join(n for n in unmatched if n))
    print(f"  · updated specialties/areas for {len(changed)} agent(s): "
          + (", ".join(changed) if changed else "none"))

    if DRY:
        print("\n--dry: no files written, no rebuild.")
        return

    with open(ROSTER, "w", encoding="utf-8") as f:
        json.dump(local, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote agents-roster.json")

    print("rebuilding agent pages…")
    subprocess.run([sys.executable, os.path.join(ROOT, "agent-pages.py")], check=True)
    print("\nDone. Review, then commit & push to publish.")


if __name__ == "__main__":
    main()
