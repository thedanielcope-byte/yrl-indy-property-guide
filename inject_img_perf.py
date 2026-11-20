#!/usr/bin/env python3
"""Image loading fixes PageSpeed flagged on mobile (Nov 2026). Idempotent.

1. "Local News & Updates" cards (build_local_posts.py, ~100 city/county/area pages):
       <span class="local-post-img" style="background-image:url('X')"></span>
   becomes
       <span class="local-post-img"><img src="X" alt="" width="1200" height="630" loading="lazy" decoding="async"></span>
   A CSS background starts downloading as soon as the card is laid out, so these
   40-60 KB PNGs were competing with the hero image for bandwidth on first load even
   though they sit far below the fold. A lazy <img> only loads near the viewport.
   style.css has `.local-post-img img { width:100%; height:100%; object-fit:cover }`,
   so the card looks the same. build_local_posts.py now emits this form directly;
   this pass keeps older pages (and anything a stale generator writes) in line.

2. Homepage hero: adds the 768w WebP (assets/img/heroes/yrl-office-768.webp) to the
   preload imagesrcset and the <picture> srcset, so a typical phone (412px wide at
   ~1.75-2x) gets a ~69 KB file instead of the 107 KB 960w one. index.html is
   hand-maintained, so this is a one-time edit; re-running is a no-op.

Runs in the GitHub Actions after the generators (next to inject_hero_preload.py).

    python3 inject_img_perf.py          # apply
    python3 inject_img_perf.py --check  # report only
"""
import html, os, re, struct, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

LOCAL_IMG = re.compile(r'<span class="local-post-img" style="background-image:url\(\'([^\'"]+)\'\)"></span>')

HERO_640 = "/assets/img/heroes/yrl-office-640.webp 640w, "
HERO_768 = "/assets/img/heroes/yrl-office-768.webp 768w, "


def img_wh(path):
    """(width, height) of a local PNG/JPEG/WebP from its header, or None."""
    try:
        with open(path, "rb") as fh:
            b = fh.read(65536)
    except OSError:
        return None
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        if b[12:16] == b"VP8X": return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
        if b[12:16] == b"VP8 ": return (struct.unpack("<H", b[26:28])[0] & 0x3fff, struct.unpack("<H", b[28:30])[0] & 0x3fff)
        if b[12:16] == b"VP8L":
            v = int.from_bytes(b[21:25], "little"); return ((v & 0x3fff) + 1, ((v >> 14) & 0x3fff) + 1)
    if b[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(b):
            if b[i] != 0xFF: i += 1; continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", b[i + 5:i + 9]); return (w, h)
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7: i += 2; continue
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None


_wh_cache = {}


def local_img_tag(src):
    if src not in _wh_cache:
        wh = img_wh(os.path.join(ROOT, src.lstrip("/"))) if src.startswith("/") else None
        _wh_cache[src] = wh or (1200, 630)  # blog share images are 1200x630
    w, h = _wh_cache[src]
    return (f'<span class="local-post-img"><img src="{html.escape(src, quote=True)}" alt="" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"></span>')


def fix_local_posts(s):
    return LOCAL_IMG.sub(lambda m: local_img_tag(m.group(1)), s)


def fix_home_hero(s):
    if HERO_768 in s or not os.path.exists(os.path.join(ROOT, "assets/img/heroes/yrl-office-768.webp")):
        return s
    return s.replace(HERO_640, HERO_640 + HERO_768)


def main():
    check = "--check" in sys.argv
    n_local = n_home = 0
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if not d.startswith(".") and d != "node_modules"]
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dp, fn)
            s = open(p, encoding="utf-8", newline="").read()
            new = s
            if 'class="local-post-img" style=' in new:
                new = fix_local_posts(new)
                if new != s:
                    n_local += 1
            if p == os.path.join(ROOT, "index.html"):
                before = new
                new = fix_home_hero(new)
                if new != before:
                    n_home += 1
            if new != s and not check:
                open(p, "w", encoding="utf-8", newline="").write(new)
    verb = "would update" if check else "updated"
    print(f"img perf — {verb}: local-post cards on {n_local} pages | homepage hero srcset: {n_home}")


if __name__ == "__main__":
    main()
