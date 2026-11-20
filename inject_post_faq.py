#!/usr/bin/env python3
"""Add a visible FAQ + FAQPage JSON-LD to blog posts that don't have one (Nov 2026 SEO audit:
"55 blog posts have no FAQPage schema").

Data: post-faqs.json  {slug: [{"q": ..., "a": ...}]}  (plain text; every answer uses only facts
already stated in that post; no "free buyer agency" wording). Edit the JSON and re-run.

Per post it maintains three marker-wrapped pieces (idempotent, re-runnable):
  <!-- POST-FAQ -->     visible <h2 id="faq"> + <details class="faq-item"> list, just above the
                        post's closing CTA block (site pattern used by build_fresh_posts.py posts)
  <!-- POST-FAQ-TOC --> "FAQ" entry at the end of the sidebar "In This Article" list
  <!-- POST-FAQ-LD -->  FAQPage JSON-LD before </head>
If a post already has its own visible Q&A section (id="faq" with <p><strong>Question?</strong>
answers, e.g. the VA loans post), only the JSON-LD is added, built from that visible section.
Posts that already carry FAQPage schema outside these markers are skipped.

  python3 inject_post_faq.py          # apply
  python3 inject_post_faq.py --check  # report only
"""
import html, json, re, sys

CHECK = "--check" in sys.argv
DATA = json.load(open("post-faqs.json", encoding="utf-8"))
M = {k: (f"<!-- {k} -->", f"<!-- /{k} -->") for k in ("POST-FAQ", "POST-FAQ-TOC", "POST-FAQ-LD")}


def strip(s, key):
    a, b = M[key]
    tail = r"\n(?:[ \t]*\n)?" if key == "POST-FAQ" else r"\n?"   # the visible block is followed by one blank line
    return re.sub(r"[ \t]*" + re.escape(a) + r".*?" + re.escape(b) + tail, "", s, flags=re.S)


def vis(t):   # plain text -> HTML text
    t = html.escape(t, quote=False).replace(" - ", " &mdash; ")
    return re.sub(r"(?<=\w)'(?=\w)|'(?=\s|$)", "&rsquo;", t)


def ld_text(t):
    return t.replace(" - ", " — ").replace("'", "’")


def existing_qa(s):
    """Q&A pairs from a hand-written <h2 id="faq"> section of <p><strong>Q?</strong> A</p>."""
    m = re.search(r'<h2 id="faq">.*?</h2>(.*?)(?=<h2|<!-- CTA|<div class="cta-block">)', s, re.S)
    if not m:
        return []
    out = []
    for q, a in re.findall(r"<p><strong>([^<]+\?)</strong>\s*(.*?)</p>", m.group(1), re.S):
        a = html.unescape(re.sub(r"<[^>]+>", "", a)).strip()
        out.append((html.unescape(q).strip(), a))
    return out


done = skipped = 0
for slug, qas in DATA.items():
    p = f"blog/{slug}/index.html"
    try:
        s = open(p, encoding="utf-8").read()
    except FileNotFoundError:
        print("  missing", p); continue
    orig = s
    for k in M:
        s = strip(s, k)
    if '"FAQPage"' in s:
        print("  skip (already has FAQPage)", slug); skipped += 1; continue

    own = existing_qa(s) if 'id="faq"' in s else []
    if own:
        pairs = own
    else:
        if 'id="faq"' in s:
            print("  skip (id=faq taken, no parsable Q&A)", slug); skipped += 1; continue
        pairs = [(x["q"], x["a"]) for x in qas]
        # visible block above the closing CTA (and its <!-- CTA BLOCK --> comment, if present)
        art = s.find("<article")
        cta = s.find('<div class="cta-block">', art)
        if art < 0 or cta < 0:
            print("  skip (no CTA block)", slug); skipped += 1; continue
        line = s.rfind("\n", 0, cta) + 1
        indent = re.match(r"[ \t]*", s[line:]).group(0)
        prev = s.rfind("\n", 0, line - 1) + 1
        if s[prev:line].strip().startswith("<!-- CTA"):
            line = prev
        a, b = M["POST-FAQ"]
        rows = "".join(f'{indent}<details class="faq-item"><summary>{vis(q)}</summary>'
                       f'<div class="faq-answer"><p>{vis(t)}</p></div></details>\n' for q, t in pairs)
        block = f'{indent}{a}\n{indent}<h2 id="faq">Frequently Asked Questions</h2>\n{rows}{indent}{b}\n\n'
        s = s[:line] + block + s[line:]
        # sidebar TOC entry
        toc = s.find('<div class="toc">')
        if toc > 0:
            ol = s.find("</ol>", toc)
            if ol > 0 and 'href="#faq"' not in s[toc:ol]:
                a, b = M["POST-FAQ-TOC"]
                ls = s.rfind("\n", 0, ol) + 1
                ind = re.match(r"[ \t]*", s[ls:]).group(0)
                s = s[:ls] + f'{ind}{a}<li><a href="#faq">FAQ</a></li>{b}\n' + s[ls:]

    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": ld_text(q), "acceptedAnswer": {"@type": "Answer", "text": ld_text(t)}}
        for q, t in pairs]}
    a, b = M["POST-FAQ-LD"]
    head = s.index("</head>")
    s = s[:head] + f'{a}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>{b}\n' + s[head:]

    if s != orig:
        done += 1
        if not CHECK:
            open(p, "w", encoding="utf-8").write(s)
print(("would update" if CHECK else "updated"), done, "posts; skipped", skipped)
