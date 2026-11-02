#!/usr/bin/env python3
"""Ping IndexNow (Bing, Copilot, Yandex, etc.) with changed URLs so new and updated pages
are recrawled within minutes instead of days.

  python3 indexnow_ping.py --all                 # every URL in sitemap.xml
  python3 indexnow_ping.py --changed BASE HEAD   # HTML files changed between two git commits
  python3 indexnow_ping.py URL [URL ...]

The key file is the 32-hex-character .txt at the site root (its contents = the key); the
GitHub Action .github/workflows/indexnow.yml runs --changed after every push to main.
Redirect stubs and noindex pages are skipped.
"""
import glob, json, os, re, subprocess, sys, urllib.request

SITE = "https://yourrealtylink.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
keys = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "*.txt"))
        if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(p))]
if not keys:
    sys.exit("no IndexNow key file found")
KEY = keys[0]


def url_for(path):
    path = path.replace("\\", "/")
    if not path.endswith(".html"):
        return None
    f = os.path.join(ROOT, path)
    if not os.path.exists(f):
        return None
    head = open(f, encoding="utf-8", errors="replace").read(6000)
    if 'http-equiv="refresh"' in head or re.search(r'<meta name="robots" content="[^"]*noindex', head):
        return None
    if path == "index.html":
        return SITE + "/"
    if path.endswith("/index.html"):
        return f"{SITE}/{path[:-len('index.html')]}"
    return None


def submit(urls):
    urls = sorted(set(u for u in urls if u))
    if not urls:
        print("nothing to submit"); return
    for i in range(0, len(urls), 10000):
        batch = urls[i:i + 10000]
        body = json.dumps({"host": "yourrealtylink.com", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": batch}).encode()
        req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"IndexNow: {r.status} for {len(batch)} URLs")
        except urllib.error.HTTPError as e:
            print(f"IndexNow: HTTP {e.code} {e.read()[:200]!r} for {len(batch)} URLs")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--all"]:
        sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
        submit(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm))
    elif a[:1] == ["--changed"] and len(a) == 3:
        out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", a[1], a[2]],
                             capture_output=True, text=True, cwd=ROOT).stdout.split()
        submit(url_for(p) for p in out)
    elif a:
        submit(a)
    else:
        sys.exit(__doc__)
