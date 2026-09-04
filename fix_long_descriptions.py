#!/usr/bin/env python3
"""
fix_long_descriptions.py — trim over-length (>165 char) meta descriptions to <=160
so Google doesn't truncate them. Idempotent, in place, HEAD-ONLY (only the
<meta name="description"> value is touched; og:/twitter: left alone).

smart_trim keeps whole leading sentences up to ~160 chars (dropping a trailing CTA
sentence like "Get a free valuation."); if the first sentence alone is too long, it
cuts at a clean em-dash / comma / word boundary. Skips blog/ posts (their
descriptions come from Supabase via build-blog.py and must be fixed in the hub, not
here).

Usage: python3 fix_long_descriptions.py [--dry]
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
HI, LO = 160, 80


def smart_trim(d):
    d = d.strip()
    if len(d) <= 165:
        return d
    # 1) greedily keep whole leading sentences up to HI chars
    acc = ""
    for s in re.split(r'(?<=[.?!])\s+', d):
        cand = (acc + " " + s).strip() if acc else s
        if len(cand) > HI:
            break
        acc = cand
    if len(acc) >= LO:
        return acc
    # 2) first sentence too long: cut at a clean boundary before HI
    cut = d[:HI]
    for sep in (" — ", " – ", "; ", ", "):
        i = cut.rfind(sep)
        if i >= LO:
            return cut[:i].rstrip(" ,;—–-") + "."
    i = cut.rfind(" ")
    return (cut[:i] if i >= LO else cut).rstrip(" ,;—–-") + "."


def main():
    fixed = []
    for f in glob.glob("**/index.html", recursive=True):
        if f.startswith(".git") or f.startswith("blog/"):
            continue
        s = open(f, encoding="utf-8", errors="ignore").read()
        if re.search(r'noindex', s, re.I):
            continue
        m = re.search(r'(<meta name="description" content=")([^"]*)(">)', s)
        if not m or len(m.group(2)) <= 165:
            continue
        new = smart_trim(m.group(2))
        if new != m.group(2):
            s = s[:m.start(2)] + new + s[m.end(2):]
            fixed.append((f, len(m.group(2)), len(new)))
            if not DRY:
                open(f, "w", encoding="utf-8").write(s)

    tag = " (dry-run)" if DRY else ""
    print("meta descriptions trimmed%s: %d" % (tag, len(fixed)))
    for f, a, b in sorted(fixed, key=lambda x: -x[1]):
        print(f"   {a}->{b}  {f}")


if __name__ == "__main__":
    main()
