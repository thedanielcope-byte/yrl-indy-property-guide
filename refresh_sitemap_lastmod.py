#!/usr/bin/env python3
"""Keep sitemap.xml <lastmod> honest: the date each page's CONTENT last changed.

Why: by Nov 2026, 93% of sitemap entries still said September even on pages that had
changed that week, because each generator only stamps the entries it creates. Google
learns to ignore lastmod that never moves.

"Content" = the page's visible text, minus <head>, <header>, <nav>, <footer>, scripts,
styles and the auto-generated MORE-ARTICLES / KEY-TERMS link blocks. Site-wide boilerplate edits (nav, footer, GA/favicon/preload tags, link
retargets) therefore don't bump the date; a new section, rewritten copy or refreshed
figures do.

State lives in sitemap-lastmod.json ({path: [content_hash, date]}). Each run:
  - page content unchanged since the stored hash -> keep the stored date
  - changed, or not seen before -> date of the file's last commit if the working copy
    matches HEAD, otherwise today (the change is about to be committed)
  - --backfill: ignore the state and walk git history per file to find the last
    commit where the content actually changed (slow; run once, or to repair)
Also drops sitemap entries whose page is now a redirect stub, noindex, or missing,
and lists indexable pages that aren't in the sitemap.

Runs in the GitHub Actions after the injectors (and locally after any generator).

    python3 refresh_sitemap_lastmod.py
    python3 refresh_sitemap_lastmod.py --backfill
    python3 refresh_sitemap_lastmod.py --check
"""
import datetime, glob, hashlib, html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
SITE = "https://yourrealtylink.com/"
STATE = "sitemap-lastmod.json"
DROP = re.compile(r"<(script|style|header|nav|footer|noscript|svg)\b.*?</\1>", re.S | re.I)
# Auto-generated cross-link blocks (inject_related_posts.py, inject_key_terms.py): refreshing
# them is linking, not content, so they don't bump lastmod either.
LINKBLOCKS = re.compile(r"<!-- (MORE-ARTICLES|KEY-TERMS) -->.*?<!-- /\1 -->", re.S)
URL_BLOCK = re.compile(r"[ \t]*<url>\s*<loc>(.*?)</loc>(.*?)</url>\n?", re.S)


def content_hash(src):
    body = LINKBLOCKS.sub(" ", src).split("<body", 1)[-1]
    body = DROP.sub(" ", body)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    return hashlib.sha1(" ".join(text.split()).encode()).hexdigest()[:16]


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def loc_to_file(loc):
    path = loc.replace(SITE, "", 1)
    if path in ("", "/"):
        return "index.html"
    return path.rstrip("/") + "/index.html" if not path.endswith(".html") else path


class Blobs:
    """One long-lived `git cat-file --batch` for reading old revisions quickly."""
    def __init__(self):
        self.p = subprocess.Popen(["git", "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def get(self, rev, path):
        self.p.stdin.write(f"{rev}:{path}\n".encode()); self.p.stdin.flush()
        header = self.p.stdout.readline().split()
        if len(header) < 3 or header[1] == b"missing":
            return None
        data = self.p.stdout.read(int(header[2])); self.p.stdout.read(1)
        return data.decode("utf-8", "replace")


def history_date(f, current, blobs):
    """Date of the newest commit whose version of f has different content than the one after it."""
    revs = [l.split() for l in git("log", "--format=%H %cs", "--", f).splitlines() if l.strip()]
    if not revs:
        return None
    if content_hash(blobs.get(revs[0][0], f) or "") != current:
        return None  # working copy differs from HEAD: changing now
    for (rev, date), older in zip(revs, revs[1:] + [None]):
        if older is None:
            return date  # first commit of the file
        prev = blobs.get(older[0], f)
        if prev is None or content_hash(prev) != current:
            return date
    return revs[-1][1]


def main():
    check, backfill = "--check" in sys.argv, "--backfill" in sys.argv
    today = datetime.date.today().isoformat()
    state = {} if backfill or not os.path.exists(STATE) else json.load(open(STATE))
    xml = open("sitemap.xml", encoding="utf-8").read()
    blobs = Blobs() if backfill else None
    seen, dropped, changed, new_state = set(), [], 0, {}

    def fix(m):
        nonlocal changed
        loc, inner = m.group(1).strip(), m.group(2)
        f = loc_to_file(loc)
        src = open(f, encoding="utf-8").read() if os.path.exists(f) else None
        if src is None or 'http-equiv="refresh"' in src or re.search(r'<meta name="robots" content="[^"]*noindex', src):
            dropped.append(loc)
            return ""
        seen.add(f)
        h = content_hash(src)
        old = state.get(f)
        if old and old[0] == h:
            date = old[1]
        elif backfill:
            date = history_date(f, h, blobs) or today
        else:
            dirty = git("status", "--porcelain", "--", f).strip()
            date = (not dirty and git("log", "-1", "--format=%cs", "--", f).strip()) or today
        new_state[f] = [h, date]
        if "<lastmod>" in inner:
            new_inner = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{date}</lastmod>", inner, count=1)
        else:
            new_inner = inner.replace("\n", f"\n <lastmod>{date}</lastmod>\n", 1) if "\n" in inner else f"<lastmod>{date}</lastmod>{inner}"
        if new_inner != inner:
            changed += 1
        return m.group(0).replace(inner, new_inner, 1)

    out = URL_BLOCK.sub(fix, xml)

    missing = []
    for f in glob.glob("**/index.html", recursive=True):
        if f in seen or f.startswith(("node_modules/", "valuation-tool/", "404")):
            continue
        s = open(f, encoding="utf-8").read()
        if 'http-equiv="refresh"' in s or re.search(r'<meta name="robots" content="[^"]*noindex', s):
            continue
        missing.append(f)

    if not check:
        open("sitemap.xml", "w", encoding="utf-8").write(out)
        with open(STATE, "w", encoding="utf-8") as fh:  # one URL per line keeps diffs readable
            fh.write("{\n" + ",\n".join(f'"{k}":["{v[0]}","{v[1]}"]' for k, v in sorted(new_state.items())) + "\n}\n")
    dates = sorted(v[1] for v in new_state.values())
    by_month = {}
    for d in dates:
        by_month[d[:7]] = by_month.get(d[:7], 0) + 1
    print(f"{'would update' if check else 'updated'} {changed} lastmod values; {len(new_state)} URLs; by month {by_month}")
    if dropped:
        print("dropped (redirect/noindex/missing):", ", ".join(dropped))
    if missing:
        print(f"{len(missing)} indexable pages not in sitemap:", ", ".join(sorted(missing)[:15]), "..." if len(missing) > 15 else "")


if __name__ == "__main__":
    main()
