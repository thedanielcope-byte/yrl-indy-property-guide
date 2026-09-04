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
import json, os, re, shutil, subprocess, sys, urllib.request

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


def slugify(name):
    s = (name or "").lower().replace("&", " ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def pull_headshot(url, dest):
    """Download an agent's hub headshot and optimize it to a ~600px-wide JPEG,
    self-hosted at dest. Returns True on success. Uses macOS `sips`; if it isn't
    available, saves the raw download so the new photo is at least used."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".src"
    try:
        urllib.request.urlretrieve(url, tmp)
    except Exception as e:
        print(f"  ! headshot download failed ({os.path.basename(dest)}): {e}")
        return False
    sips = shutil.which("sips")
    if sips:
        r = subprocess.run([sips, "--resampleWidth", "600", "-s", "format", "jpeg",
                            "-s", "formatOptions", "82", tmp, "--out", dest],
                           capture_output=True, text=True)
        try:
            os.remove(tmp)
        except OSError:
            pass
        if r.returncode != 0:
            print(f"  ! sips resize failed ({os.path.basename(dest)})")
            return False
    else:
        shutil.move(tmp, dest)  # no sips (non-macOS): keep the raw file
        print(f"  · {os.path.basename(dest)} saved un-resized (sips not found)")
    return True


def main():
    remote = fetch_remote()
    by_email = {norm(r.get("email")): r for r in remote if norm(r.get("email"))}
    by_name = {norm(r.get("name")): r for r in remote}

    local = json.load(open(ROSTER, encoding="utf-8"))
    changed, matched, unmatched, photo_synced = [], 0, [], []

    for a in local:
        # Match on email first (stable if the agent renames), then name.
        r = by_email.get(norm(a.get("email"))) or by_name.get(norm(a.get("name")))
        if not r:
            unmatched.append(a.get("name"))
            continue
        matched += 1
        # Freeze the URL slug to the CURRENT name before any name change syncs in.
        a.setdefault("slug", slugify(a.get("name")))
        snap = lambda: (a.get("expertise"), a.get("areas"), a.get("bio"), a.get("tagline"),
                        a.get("name"), a.get("title"), a.get("phone"), a.get("photo"),
                        a.get("testimonials"), a.get("years"), a.get("designations"),
                        a.get("languages"), a.get("video"), a.get("gallery"))
        before = snap()

        exp = [str(x) for x in (r.get("expertise") or []) if str(x).strip()]
        areas = clean_areas(r.get("areas"))
        bio_txt = (r.get("bio") or "").strip()
        tagline = (r.get("tagline") or "").strip()
        # Hero identity fields (agent-editable via My Agent Info)
        r_name = (r.get("name") or "").strip()
        r_title = (r.get("title") or "").strip()
        r_phone = (r.get("phone") or "").strip()
        r_photo = (r.get("photo") or "").strip()
        if r_name:
            a["name"] = r_name
        if r_title:
            a["title"] = r_title
        if r_phone:
            a["phone"] = r_phone
        # Photo: when an agent uploads a headshot to the hub (ANY Supabase
        # hub-files/... URL — the old "headshots/" path or the new
        # "<user-id>/agent-photos/" path), download + optimize + self-host it at
        # /assets/img/agents/<slug>.jpg instead of hot-linking the heavy hub PNG.
        # Re-download only when the hub URL actually changes (tracked in photo_src);
        # non-hub URLs (legacy CDN) are left as-is.
        if r_photo and "hub-files/" in r_photo and r_photo != a.get("photo_src"):
            slug = a.get("slug") or slugify(a.get("name"))
            local_rel = "/assets/img/agents/%s.jpg" % slug
            if DRY:
                photo_synced.append(a.get("name"))
            elif pull_headshot(r_photo, os.path.join(ROOT, "assets", "img", "agents", "%s.jpg" % slug)):
                a["photo"] = local_rel
                a["photo_src"] = r_photo   # remember what we synced, so we don't refetch
                photo_synced.append(a.get("name"))
        # Enrichment fields (agent-editable): mirror the hub; drop when empty.
        for k in ("testimonials", "designations", "languages", "gallery"):
            v = r.get(k)
            if isinstance(v, list) and v:
                a[k] = v
            else:
                a.pop(k, None)
        for k in ("years", "video"):
            v = (r.get(k) or "").strip() if isinstance(r.get(k), str) else r.get(k)
            if v:
                a[k] = v
            else:
                a.pop(k, None)

        # Mirror the hub: set when present, remove the key when empty so the
        # site falls back to defaults (expertise/bio) / hides the section (areas).
        if exp:
            a["expertise"] = exp
        else:
            a.pop("expertise", None)
        if areas:
            a["areas"] = areas
        else:
            a.pop("areas", None)
        if bio_txt:
            a["bio"] = bio_txt
        else:
            a.pop("bio", None)
        if tagline:
            a["tagline"] = tagline
        else:
            a.pop("tagline", None)

        if before != snap():
            changed.append(a.get("name"))

    print(f"matched {matched}/{len(local)} agents to the hub roster")
    if unmatched:
        print("  · no hub match (left as-is): " + ", ".join(n for n in unmatched if n))
    print(f"  · updated specialties/areas/bio for {len(changed)} agent(s): "
          + (", ".join(changed) if changed else "none"))
    print(f"  · synced new headshot for {len(photo_synced)} agent(s): "
          + (", ".join(n for n in photo_synced if n) if photo_synced else "none"))

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
