#!/usr/bin/env python3
"""
inject_ai_answer.py — add a "Quick Answer" block + Speakable schema to informational
pages so answer engines (Google AI Overviews, etc.) can extract a direct answer.

Mirrors the format already winning AI-Overview citations on the /best/ and /utilities/
pages: a .quick-answer box (heading + .qa-lead direct answer + .qa-facts label/value
grid) reusing existing CSS (style.css:608-617, no new CSS), plus a WebPage/Speakable
JSON-LD block pointing at .qa-lead / .qa-facts.

Data: ai-answers.json — [{page, question, answer, facts:[{label,value}]}]. The answer/
value strings are inserted as HTML (they may contain <strong>/<a>), so they must be
trusted, accurate summaries of the page's OWN content (no new facts).

Idempotent (marker <!-- QA-START -->). Anchor: inserts after the blog <div class="post-meta">.
Validates each target's anchor + on-disk existence. Run after regenerating any target page.

Usage: python3 inject_ai_answer.py [--dry]
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
START, END = "<!-- QA-START -->", "<!-- QA-END -->"
META_ANCHOR = re.compile(r'(<div class="post-meta">.*?</div>)', re.S)


def block(rec):
    facts = "\n".join(" <div><dt>%s</dt><dd>%s</dd></div>" % (f["label"], f["value"]) for f in rec.get("facts", []))
    return (
        " %s\n<div class=\"quick-answer\">\n"
        " <p class=\"qa-heading\">Quick Answer</p>\n"
        " <p class=\"qa-lead\">%s</p>\n"
        " <dl class=\"qa-facts\">\n%s\n </dl>\n"
        "</div>\n %s\n" % (START, rec["answer"], facts, END))


def speakable(canon):
    j = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": canon,
                    "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"]}},
                   ensure_ascii=False)
    return ' <script type="application/ld+json">%s</script>\n' % j


def main():
    data = json.load(open(os.path.join(ROOT, "ai-answers.json"), encoding="utf-8"))
    done = skipped = noanchor = missing = 0
    for rec in data:
        idx = os.path.join(ROOT, rec["page"].strip("/"), "index.html")
        if not os.path.exists(idx):
            missing += 1; print("  ! missing:", rec["page"]); continue
        s = orig = open(idx, encoding="utf-8").read()
        if START in s:
            skipped += 1; continue
        if not META_ANCHOR.search(s):
            noanchor += 1; print("  ! no post-meta anchor:", rec["page"]); continue
        s = META_ANCHOR.sub(lambda m: m.group(1) + "\n" + block(rec), s, count=1)
        # add speakable schema before </head> if not already present
        if "SpeakableSpecification" not in s:
            canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
            if canon:
                s = s.replace("</head>", speakable(canon.group(1)) + "</head>", 1)
        if s != orig:
            done += 1
            if not DRY:
                open(idx, "w", encoding="utf-8").write(s)
    tag = " (dry-run)" if DRY else ""
    print("\nai-answer%s — added: %d | already had it: %d | no anchor: %d | missing: %d"
          % (tag, done, skipped, noanchor, missing))


if __name__ == "__main__":
    main()
