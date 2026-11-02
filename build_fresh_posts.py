#!/usr/bin/env python3
"""Build data-driven blog posts from fresh_posts/<slug>.py (Nov 2026 onward).

Each data file defines POST = dict(...) (see fresh_posts/README.md for the fields). The page
uses the relocation-guide shell, like build_living_indy.py: Quick Answer + Speakable,
Article/Breadcrumb/LocalBusiness graph, FAQPage schema, TOC, sources line, custom CTA and
related links. It also renders the card image (finalize_new_posts.py template), adds the
post to sitemap.xml and the top of /blog/, and adds an inbound link from each page listed
in link_from.

  python3 build_fresh_posts.py                 build every post in fresh_posts/
  python3 build_fresh_posts.py SLUG [SLUG...]  build only these
  python3 build_fresh_posts.py --check SLUG    validate + render to /tmp only (touches no site files)

Re-runnable. Afterwards run inject_gtag.py, inject_favicon.py, gloss_autolink.py . --apply.
"""
import base64, glob, html, importlib.util, json, os, re, subprocess, sys

SRC = "blog/moving-to-indianapolis-relocation-guide/index.html"
REQUIRED = ["slug", "title", "headline", "h1_html", "desc", "date", "month", "category", "eyebrow", "focus",
            "hero_sub", "badges", "read_min", "card_title", "card_sub", "qa_heading", "qa_lead", "qa_facts",
            "toc", "body", "faqs", "sources", "related", "cta", "resources"]


def load(slug):
    spec = importlib.util.spec_from_file_location(slug, f"fresh_posts/{slug}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.POST


def check(P):
    errs = []
    for k in REQUIRED:
        if k not in P:
            errs.append(f"missing field: {k}")
    if errs:
        return errs
    if len(P["title"]) > 60: errs.append(f"title {len(P['title'])} chars (max 60)")
    if not 120 <= len(P["desc"]) <= 160: errs.append(f"desc {len(P['desc'])} chars (want 120-160)")
    if len(P["faqs"]) < 4: errs.append("want at least 4 FAQs")
    if len(P["sources"]) < 2: errs.append("want at least 2 sources")
    ids = set(re.findall(r'<h2 id="([^"]+)"', P["body"])) | {"faq"}
    for a, _ in P["toc"]:
        if a not in ids: errs.append(f"toc anchor #{a} has no <h2 id> in body")
    hrefs = re.findall(r'href="(/[^"#?]*)', P["body"] + json.dumps(P["related"]) + json.dumps(P["cta"]) + json.dumps(P["resources"])
                       + "".join(t for _, t in P.get("link_from", [])))
    for h in sorted(set(hrefs) - {f"/blog/{P['slug']}/"}):
        f = h.lstrip("/")
        if not (os.path.exists(f) or os.path.exists(os.path.join(f, "index.html"))):
            errs.append(f"broken internal link: {h}")
    for p, _ in P.get("link_from", []):
        if not os.path.exists(p): errs.append(f"link_from page missing: {p}")
    low = (P["body"] + " ".join(a for _, a in P["faqs"])).lower()
    for bad in ("free buyer", "buyers pay nothing", "no cost to buyers", "costs buyers nothing", "always free"):
        if bad in low: errs.append(f"compliance: '{bad}' (buyer agency is not free)")
    for q, a in P["faqs"]:
        if "<" in q or "<" in a: errs.append("FAQ text must be plain text (no HTML)")
    if "__" in P["body"]: errs.append("leftover placeholder in body")
    return errs


def render_card(P, out):
    src = open("finalize_new_posts.py", encoding="utf-8").read()
    tpl = re.search(r'TPL = """(.*?)"""', src, re.S).group(1)
    logo = base64.b64encode(open("assets/img/yrl-logo.png", "rb").read()).decode()
    t = P["card_title"]
    fs = 72 if len(t) <= 34 else (60 if len(t) <= 48 else 50)
    keys = dict(logo=logo, eyebrow=P["eyebrow"], title=html.escape(t), sub=html.escape(P["card_sub"]), fs=fs, alt="", loc="")
    tmp = f"/tmp/yrl-card-{P['slug']}.html"
    open(tmp, "w").write(tpl.format(**keys))
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630", "--virtual-time-budget=3000",
                    "--screenshot=" + os.path.abspath(out), "file://" + tmp], capture_output=True)
    subprocess.run(["pngquant", "--quality=70-95", "--force", "--ext", ".png", out], capture_output=True)
    return os.path.exists(out)


def page(P):
    slug = P["slug"]; url = f"https://yourrealtylink.com/blog/{slug}/"
    img = f"/assets/img/blog/{slug}.png"; og = "https://yourrealtylink.com" + img
    s = open(SRC, encoding="utf-8").read()
    s = re.sub(r"<!-- YOAST:.*?-->", f"<!-- YOAST: Focus Keyword: {P['focus']} | Category: {P['category']} -->", s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(P['title'], quote=False)}</title>", s, count=1)
    T, D = html.escape(P["title"]), html.escape(P["desc"])
    for prop, val in (("og:title", T), ("og:description", D), ("og:url", url), ("og:image", og)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    for nm, val in (("description", D), ("twitter:title", T), ("twitter:description", D), ("twitter:image", og)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + val, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    art = {"@type": "Article", "headline": P["headline"], "description": P["desc"],
           "author": {"@type": "Person", "name": "Daniel Cope", "url": "https://yourrealtylink.com/agents/daniel-cope/", "jobTitle": "Real Estate Broker",
                      "worksFor": {"@type": "Organization", "name": "Your Realty Link"}},
           "publisher": {"@type": "Organization", "name": "Your Realty Link", "logo": {"@type": "ImageObject", "url": "/assets/img/yrl-logo.png"}},
           "image": og, "datePublished": P["date"], "dateModified": P.get("modified", P["date"]), "mainEntityOfPage": url,
           "about": P.get("about") or {"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}}}
    graph = {"@context": "https://schema.org", "@graph": [art,
        {"@type": "WebPage", "url": url, "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa-lead", ".qa-facts"]}},
        {"@type": ["LocalBusiness", "RealEstateAgent"], "name": "Your Realty Link", "url": "https://yourrealtylink.com", "telephone": "317-997-7404",
         "address": {"@type": "PostalAddress", "streetAddress": "2302 E Southport Rd", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46227"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yourrealtylink.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": P["headline"], "item": url}]}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P["faqs"]]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    assert len(blocks) >= 2
    new = ['<script type="application/ld+json">\n' + json.dumps(graph, indent=1, ensure_ascii=False) + '\n</script>',
           '<script type="application/ld+json">\n' + json.dumps(faqld, indent=1, ensure_ascii=False) + '\n</script>']
    for m, rep in reversed(list(zip(blocks[:2], new))):
        s = s[:m.start()] + rep + s[m.end():]
    for m in reversed(blocks[2:]):
        s = s[:m.start()] + s[m.end():]
    crumb = html.escape(P.get("crumb", P["headline"]), quote=False)
    s = re.sub(r"(<span>&rsaquo;</span>\s*<a href=\"/blog/\">Blog</a>\s*<span>&rsaquo;</span>\s*).*?(\s*</div>\s*</nav>)",
               lambda m: m.group(1) + crumb + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r"<h1>.*?</h1>", lambda m: f"<h1>{P['h1_html']}</h1>", s, count=1, flags=re.S)
    s = re.sub(r'(<p class="hero-sub">).*?(</p>)', lambda m: m.group(1) + P["hero_sub"] + m.group(2), s, count=1, flags=re.S)
    badges = "\n".join(f' <span class="hero-badge">{b}</span>' for b in P["badges"])
    s = re.sub(r'<div class="hero-badges">.*?</div>', lambda m: f'<div class="hero-badges">\n{badges}\n </div>', s, count=1, flags=re.S)
    s = re.sub(r"Updated [A-Z][a-z]+ 2026</p>", f"Updated {P['month']}</p>", s, count=1)
    s = re.sub(r'<div class="post-meta">.*?</div>', lambda m: f'<div class="post-meta">\n <span class="category-badge">{P["category"]}</span>\n <span>{P["month"]}</span>\n'
               f' <span>By Daniel Cope, Real Estate Broker &mdash; Your Realty Link</span>\n <span>~{P["read_min"]} min read</span>\n </div>', s, count=1, flags=re.S)
    qa = (f'<!-- QA-START -->\n<div class="quick-answer">\n <p class="qa-heading">{P["qa_heading"]}</p>\n <p class="qa-lead">{P["qa_lead"]}</p>\n'
          f' <dl class="qa-facts">\n' + "\n".join(f' <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in P["qa_facts"]) + '\n </dl>\n</div>\n<!-- QA-END -->\n')
    faq = "\n".join(f' <details class="faq-item">\n <summary>{html.escape(q, quote=False)}</summary>\n <div class="faq-answer">\n <p>{html.escape(a, quote=False)}</p>\n </div>\n </details>' for q, a in P["faqs"])
    src_line = " &middot; ".join(f'<a href="{u}" target="_blank" rel="noopener">{l}</a>' if u.startswith("http") else (f'<a href="{u}">{l}</a>' if u else l)
                                 for l, u in P["sources"])
    body = (f"\n{qa}\n{P['body'].strip()}\n\n <!-- FAQ -->\n <h2 id=\"faq\">Frequently Asked Questions</h2>\n{faq}\n\n"
            f' <p style="font-size:.85rem;color:var(--gray);">Sources: {src_line}</p>\n\n ')
    i = s.index("</div>", s.index('<div class="post-meta">')) + len("</div>")
    j = s.index("<!-- CTA -->")
    s = s[:i] + "\n" + body + s[j:]
    h3, p, btns = P["cta"]
    btn_html = "\n".join(f' <a href="{h}" class="btn {c}">{l}</a>' for h, l, c in btns)
    s = re.sub(r'<!-- CTA -->\s*<div class="cta-block">.*?<div class="btn-group">.*?</div>\s*</div>',
               lambda m: f'<!-- CTA -->\n <div class="cta-block">\n <h3>{h3}</h3>\n <p>{p}</p>\n <div class="btn-group">\n{btn_html}\n </div>\n </div>', s, count=1, flags=re.S)
    res = "\n".join(f' <li><a href="{h}">{l}</a></li>' for h, l in P["resources"])
    s = re.sub(r'(<h3>Related Resources</h3>\s*<ul>).*?(</ul>)', lambda m: m.group(1) + "\n" + res + "\n " + m.group(2), s, count=1, flags=re.S)
    toc = "\n".join(f' <li><a href="#{a}">{l}</a></li>' for a, l in P["toc"])
    s = re.sub(r'(<div class="toc">\s*<h4>In This Article</h4>\s*<ol>).*?(</ol>)', lambda m: m.group(1) + "\n" + toc + "\n " + m.group(2), s, count=1, flags=re.S)
    rel = "\n".join(f' <li><a href="{h}">{l}</a></li>' for h, l in P["related"])
    s = re.sub(r'(<div class="sidebar-card-header">Related Posts</div>\s*<div class="sidebar-card-body">\s*<ul class="contact-list">).*?(</ul>)',
               lambda m: m.group(1) + "\n" + rel + "\n " + m.group(2), s, count=1, flags=re.S)
    return s


def publish(P):
    slug = P["slug"]; url = f"https://yourrealtylink.com/blog/{slug}/"; img = f"/assets/img/blog/{slug}.png"
    if not os.path.exists(img.lstrip("/")):
        print("  card", render_card(P, img.lstrip("/")))
    os.makedirs(f"blog/{slug}", exist_ok=True)
    open(f"blog/{slug}/index.html", "w", encoding="utf-8").write(page(P))
    print("built", slug)
    sm = open("sitemap.xml", encoding="utf-8").read()
    if url not in sm:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>",
             f" <url>\n <loc>{url}</loc>\n <lastmod>{P['date']}</lastmod>\n <changefreq>monthly</changefreq>\n <priority>0.8</priority>\n </url>\n</urlset>"))
    bi = open("blog/index.html", encoding="utf-8").read()
    if f"/blog/{slug}/" not in bi:
        m = re.search(r'\n( *)<div class="blog-card">\s*<div class="blog-card-img">', bi)
        ind = m.group(1)
        card = (f'\n{ind}<div class="blog-card">\n <div class="blog-card-img"><img src="{img}" alt="{html.escape(P["focus"])}" loading="lazy"></div>\n'
                f' <div class="blog-card-body">\n <div class="blog-card-cat">{P["category"]}</div>\n <h3>{html.escape(P["headline"], quote=False)}</h3>\n'
                f' <p>{html.escape(P["desc"], quote=False)}</p>\n <a href="/blog/{slug}/" class="read-more">Read More →</a>\n </div>\n </div>\n')
        open("blog/index.html", "w", encoding="utf-8").write(bi[:m.start()] + card + bi[m.start():])
    for p, note in P.get("link_from", []):
        t = open(p, encoding="utf-8").read()
        if f"/blog/{slug}/" in t:
            continue
        note = f" <p>{note}</p>\n\n "
        if " <!-- FAQ -->" in t:
            t = t.replace(" <!-- FAQ -->", note + "<!-- FAQ -->", 1)
        elif "<!-- CTA -->" in t:
            t = t.replace("<!-- CTA -->", note + "<!-- CTA -->", 1)
        elif "<!-- CTA BLOCK -->" in t:
            t = t.replace("<!-- CTA BLOCK -->", note + "<!-- CTA BLOCK -->", 1)
        else:
            mm = re.search(r"<h2[^>]*>Frequently Asked Questions", t)
            if not mm:
                print("  no anchor in", p); continue
            t = t[:mm.start()] + note + t[mm.start():]
        open(p, "w", encoding="utf-8").write(t)
        print("  linked from", p)


def main():
    args = sys.argv[1:]
    if args and args[0] == "--check":
        ok = True
        for slug in args[1:]:
            P = load(slug); errs = check(P)
            print(slug, "OK" if not errs else "PROBLEMS:"); [print("  -", e) for e in errs]
            if not errs:
                out = f"/tmp/yrl-check-{slug}.html"; open(out, "w", encoding="utf-8").write(page(P))
                words = len(re.sub(r"<[^>]+>", " ", P["body"]).split())
                print(f"  rendered {out} ({words} words in body)")
            ok = ok and not errs
        sys.exit(0 if ok else 1)
    slugs = args or sorted(os.path.basename(f)[:-3] for f in glob.glob("fresh_posts/*.py") if not os.path.basename(f).startswith("_"))
    for slug in slugs:
        P = load(slug); errs = check(P)
        if errs:
            print(slug, "SKIPPED:", errs); continue
        publish(P)


if __name__ == "__main__":
    main()
