#!/usr/bin/env python3
"""
inject_gtag.py — add the Google Analytics 4 gtag.js snippet to the <head> of every
page site-wide. Idempotent: skips a page that already has the tag. Inserted right
after the <meta charset> line (keeps charset first, tag as high in <head> as Google
recommends).

Skips redirect stubs (meta-refresh) — they navigate away instantly, so a tag there
would never fire (and would risk double-counting the destination). Skips node_modules.

The snippet is ALSO baked into index.html's <head>, which most generators clone their
header from — so newly generated pages inherit it. Re-run this after a large generator
run to catch any page built from a scratch template (same convention as inject_idx.py).

Deferred load (Nov 2026): the dataLayer/config lines stay inline at the top of <head>,
but gtag.js itself (~180 KB, PageSpeed's top "unused JavaScript" item) is fetched after
the page has painted — on window load once the first LCP entry exists (3 s fallback;
browsers without the LCP API load it at window load) — or immediately on the first
tap/scroll/keypress. gtag() calls made before then are queued in dataLayer and replay
when it lands, so page_view and the click events in site-enhancements.js still fire.
Pages that still carry the old `<script async src=...gtag/js...>` block are upgraded in
place to the deferred block (exact match), so re-running this is all that's needed.

Usage: python3 inject_gtag.py [--dry]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
GA_ID = "G-SNV86NLT23"
MARKER = "<!-- Google tag (gtag.js) -->"

# The pre-Nov-2026 snippet (async gtag.js in <head>); upgraded in place to BLOCK.
OLD_BLOCK = (
    ' <!-- Google tag (gtag.js) -->\n'
    ' <script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
    ' <script>\n'
    ' window.dataLayer = window.dataLayer || [];\n'
    ' function gtag(){dataLayer.push(arguments);}\n'
    " gtag('js', new Date());\n"
    " gtag('config', '%s');\n"
    ' </script>\n'
) % (GA_ID, GA_ID)

BLOCK = (
    ' <!-- Google tag (gtag.js) -->\n'
    ' <script>\n'
    ' window.dataLayer = window.dataLayer || [];\n'
    ' function gtag(){dataLayer.push(arguments);}\n'
    " gtag('js', new Date());\n"
    " gtag('config', '%s');\n"
    ' </script>\n'
    ' <script>/* gtag.js loads after first paint or on first interaction; see inject_gtag.py */\n'
    " (function(w,d){var done=0,ev=['pointerdown','keydown','touchstart','scroll'];\n"
    " function load(){if(done)return;done=1;ev.forEach(function(e){w.removeEventListener(e,load,true)});"
    "var s=d.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=%s';d.head.appendChild(s)}\n"
    " ev.forEach(function(e){w.addEventListener(e,load,{capture:true,passive:true})});\n"
    " function painted(){var t=setTimeout(load,3000);try{if(PerformanceObserver.supportedEntryTypes.indexOf('largest-contentful-paint')>-1){"
    "new PerformanceObserver(function(l,o){o.disconnect();clearTimeout(t);setTimeout(load,0)}).observe({type:'largest-contentful-paint',buffered:true});return}}catch(e){}"
    "clearTimeout(t);load()}\n"
    " if(d.readyState==='complete')painted();else w.addEventListener('load',painted)})(window,document);\n"
    ' </script>\n'
) % (GA_ID, GA_ID)

CHARSET_RE = re.compile(r'(<meta\s+charset=["\']?[^>\'"]+["\']?\s*/?>\s*\n)', re.I)
HEAD_RE = re.compile(r'(<head[^>]*>\s*\n)', re.I)


def main():
    added = have = stub = skipped = no_head = upgraded = 0
    for dp, dns, fns in os.walk(ROOT):
        if ".git" in dp or "node_modules" in dp:
            continue
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            s = open(path, encoding="utf-8").read()
            if OLD_BLOCK in s:
                upgraded += 1
                if not DRY:
                    open(path, "w", encoding="utf-8").write(s.replace(OLD_BLOCK, BLOCK))
                continue
            if MARKER in s or ("gtag/js?id=" + GA_ID) in s:
                have += 1
                if '<script async src="https://www.googletagmanager.com/gtag/js' in s:
                    print("  ! old async gtag in an unexpected shape (left as is): " + os.path.relpath(path, ROOT))
                continue
            if 'http-equiv="refresh"' in s:
                stub += 1
                continue
            if CHARSET_RE.search(s):
                s2 = CHARSET_RE.sub(lambda m: m.group(1) + BLOCK, s, count=1)
            elif HEAD_RE.search(s):
                s2 = HEAD_RE.sub(lambda m: m.group(1) + BLOCK, s, count=1)
            else:
                no_head += 1
                print("  ! no <head>: " + os.path.relpath(path, ROOT))
                continue
            if s2 != s:
                added += 1
                if not DRY:
                    open(path, "w", encoding="utf-8").write(s2)
            else:
                skipped += 1

    tag = " (dry-run)" if DRY else ""
    print("\ngtag%s — added: %d | upgraded to deferred load: %d | already had it: %d | redirect stubs skipped: %d | no <head>: %d"
          % (tag, added, upgraded, have, stub, no_head))


if __name__ == "__main__":
    main()
