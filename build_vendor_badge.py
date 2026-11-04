#!/usr/bin/env python3
"""Preferred Vendor badge (Nov 2026 backlink outreach).

- Renders assets/img/badges/yrl-preferred-vendor.png (light) and -dark.png at 2x
  (shown at 320x120) with headless Chrome, then pngquant.
- Builds /vendors/badge/ (noindex, not in the sitemap): badge previews, copy-paste
  HTML, a text-link option, where to paste it, and the fine print. The badge is
  optional and never a condition of being listed (RESPA: no thing of value is
  exchanged for a listing or a link), and it uses the brand name as anchor text.
- Adds a one-line pointer to the badge page on /vendors/ (VENDOR-BADGE markers).
  Re-run after build_vendors.py. Idempotent.
"""
import base64, html, os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
SRC = "vendors/index.html"
OUT = "vendors/badge/index.html"
URL = "https://yourrealtylink.com/vendors/badge/"
IMG_DIR = "assets/img/badges"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BADGE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:320px;height:120px;overflow:hidden;background:transparent}
.b{width:320px;height:120px;border-radius:14px;display:flex;align-items:center;gap:16px;padding:0 20px 0 16px;font-family:Inter,-apple-system,'Segoe UI',Roboto,sans-serif}
.light{background:#fff;border:1.5px solid #e2ddd9}
.dark{background:#1c1a19;border:1.5px solid #1c1a19}
.chip{flex:0 0 auto;width:104px;height:56px;border-radius:9px;background:#fff;display:flex;align-items:center;justify-content:center}
.chip img{width:96px;height:auto;display:block}
.t{display:flex;flex-direction:column;gap:3px;min-width:0}
.k{font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
.n{font-family:'Playfair Display',Georgia,serif;font-size:23px;font-weight:700;line-height:1.05;white-space:nowrap}
.s{font-size:11px;font-weight:500}
.light .k{color:#c03926}.light .n{color:#1a1a1a}.light .s{color:#6e6e70}
.dark .k{color:#f08a76}.dark .n{color:#fff}.dark .s{color:#bdb7b3}
.light .chip{border:1px solid #efe9e6}
"""


def render_badges():
    os.makedirs(IMG_DIR, exist_ok=True)
    logo = base64.b64encode(open("assets/img/yrl-logo.png", "rb").read()).decode()
    for theme, name in (("light", "yrl-preferred-vendor.png"), ("dark", "yrl-preferred-vendor-dark.png")):
        page = (f'<!doctype html><html><head><meta charset="utf-8">'
                f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=Playfair+Display:wght@700&display=block" rel="stylesheet">'
                f'<style>{BADGE_CSS}</style></head><body><div class="b {theme}">'
                f'<div class="chip"><img src="data:image/png;base64,{logo}" alt=""></div>'
                f'<div class="t"><span class="k">Preferred Vendor</span><span class="n">Your Realty Link</span>'
                f'<span class="s">Central Indiana Real Estate</span></div></div></body></html>')
        tmp = f"/tmp/yrl-badge-{theme}.html"
        open(tmp, "w").write(page)
        out = os.path.abspath(os.path.join(IMG_DIR, name))
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        "--force-device-scale-factor=2", "--window-size=320,120", "--virtual-time-budget=6000",
                        "--screenshot=" + out, "file://" + tmp], capture_output=True)
        subprocess.run(["pngquant", "--quality=80-98", "--force", "--ext", ".png", out], capture_output=True)
        print("badge", name, os.path.exists(out))


def snippet(img, alt="Your Realty Link Preferred Vendor"):
    return (f'<a href="https://yourrealtylink.com/vendors/" target="_blank" rel="noopener" title="{alt}">'
            f'<img src="https://yourrealtylink.com/assets/img/badges/{img}" alt="{alt}" width="320" height="120" style="max-width:100%;height:auto;"></a>')


TEXT_LINK = '<a href="https://yourrealtylink.com/vendors/">Your Realty Link Preferred Vendor</a>'

PAGE_CSS = """
.badge-wrap { max-width: 860px; margin: 0 auto; padding: 10px 0 48px; }
.badge-wrap h2 { color: #13294a; font-size: 1.3rem; margin: 2.2rem 0 .5rem; }
.badge-wrap p { max-width: 68ch; }
.badge-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 18px; margin-top: 14px; }
.badge-card { background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 12px; }
.badge-card.on-dark { background: #f3f1ef; }
.badge-card h3 { font-size: 1rem; color: #13294a; margin: 0; }
.badge-card img { max-width: 100%; height: auto; display: block; }
.badge-code { width: 100%; min-height: 96px; font: 12.5px/1.45 ui-monospace, SFMono-Regular, Menlo, monospace; color: #1a1a1a; background: #f7f7f7; border: 1px solid var(--border); border-radius: 8px; padding: 10px; resize: vertical; }
.badge-copy { align-self: flex-start; background: var(--red); color: #fff; border: 0; border-radius: 8px; padding: 9px 16px; font-weight: 600; font-size: .9rem; cursor: pointer; }
.badge-copy:focus-visible { outline: 3px solid #13294a; outline-offset: 2px; }
.badge-steps { padding-left: 1.2rem; display: grid; gap: 6px; }
.badge-fine { font-size: .9rem; color: var(--mid); border-top: 1px solid var(--border); padding-top: 14px; margin-top: 28px; }
"""


def build_page():
    s = open(SRC, encoding="utf-8").read()
    title = "Preferred Vendor Badge for Your Website | Your Realty Link"
    desc = "For businesses on the Your Realty Link Preferred Vendors list: an optional badge and copy-paste code to show the listing on your own website."
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    s = s.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">', 1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, s, count=1)
    for prop, val in (("og:title", title), ("og:description", desc), ("og:url", URL)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + html.escape(val), s, count=1)
    for nm, val in (("description", desc), ("twitter:title", title), ("twitter:description", desc)):
        s = re.sub(rf'(<meta name="{nm}" content=")[^"]*', lambda m: m.group(1) + html.escape(val), s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: """<script type="application/ld+json">
 { "@context": "https://schema.org", "@graph": [
 { "@type": "WebPage", "url": "https://yourrealtylink.com/vendors/badge/", "name": "Preferred Vendor Badge" },
 { "@type": "BreadcrumbList", "itemListElement": [
 { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://yourrealtylink.com/" },
 { "@type": "ListItem", "position": 2, "name": "Preferred Vendors", "item": "https://yourrealtylink.com/vendors/" },
 { "@type": "ListItem", "position": 3, "name": "Preferred Vendor Badge", "item": "https://yourrealtylink.com/vendors/badge/" } ] }
 ] }
 </script>""", s, count=1, flags=re.S)
    s = re.sub(r"(<style>).*?(</style>)", lambda m: m.group(1) + PAGE_CSS + m.group(2), s, count=1, flags=re.S)
    hero = ('<section class="page-hero">\n <div class="container">\n <h1>Preferred Vendor Badge</h1>\n'
            ' <p class="hero-sub">For the local businesses on our <a href="/vendors/" style="color:inherit;text-decoration:underline;">Preferred Vendors</a> list: '
            'an optional badge you can add to your website so your customers can see you&rsquo;re a trusted Your Realty Link partner.</p>\n </div>\n</section>')
    s = re.sub(r'<section class="page-hero.*?</section>', lambda m: hero, s, count=1, flags=re.S)

    def card(label, img, cls=""):
        code = snippet(img)
        return (f' <div class="badge-card{cls}">\n <h3>{label}</h3>\n <img src="/{IMG_DIR}/{img}" alt="Your Realty Link Preferred Vendor badge, {label.lower()}" width="320" height="120">\n'
                f' <textarea class="badge-code" readonly aria-label="HTML code for the {label.lower()}">{html.escape(code)}</textarea>\n'
                f' <button type="button" class="badge-copy">Copy code</button>\n </div>')
    main = f"""<div class="container">
 <div class="badge-wrap">

 <h2>Pick a badge</h2>
 <p>Copy the code and paste it into your website wherever you list partners, credentials or affiliations. The badge links to our Preferred Vendors page, where your business is listed.</p>
 <div class="badge-grid">
{card("Light badge", "yrl-preferred-vendor.png")}
{card("Dark badge", "yrl-preferred-vendor-dark.png", " on-dark")}
 </div>

 <h2>Prefer a text link?</h2>
 <div class="badge-card">
 <textarea class="badge-code" readonly aria-label="HTML code for a text link" style="min-height:60px;">{html.escape(TEXT_LINK)}</textarea>
 <button type="button" class="badge-copy">Copy code</button>
 </div>

 <h2>Where to paste it</h2>
 <ol class="badge-steps">
 <li><strong>WordPress:</strong> add a <em>Custom HTML</em> block (or widget) to your footer, About or Partners page and paste the code.</li>
 <li><strong>Wix:</strong> use <em>Embed Code &rarr; Embed HTML</em> and paste the code.</li>
 <li><strong>Squarespace:</strong> add a <em>Code</em> block and paste the code.</li>
 <li><strong>Anything else:</strong> send the code to whoever manages your site, or email us and we&rsquo;ll help.</li>
 </ol>

 <p class="badge-fine">Adding the badge is optional. Your listing on our <a href="/vendors/">Preferred Vendors</a> page doesn&rsquo;t depend on it, and no one pays or receives anything for a listing or a link. To update your listing or ask a question, email <a href="mailto:indy@yourrealtylink.com">indy@yourrealtylink.com</a>.</p>

 </div>
</div>
<script>
document.querySelectorAll('.badge-copy').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var t = b.parentNode.querySelector('.badge-code'); t.select();
    var done = function () {{ b.textContent = 'Copied'; setTimeout(function () {{ b.textContent = 'Copy code'; }}, 1800); }};
    if (navigator.clipboard) {{ navigator.clipboard.writeText(t.value).then(done, function () {{ document.execCommand('copy'); done(); }}); }}
    else {{ document.execCommand('copy'); done(); }}
  }});
}});
</script>

"""
    i = s.index("</section>", s.index('<section class="page-hero">')) + len("</section>")
    j = s.index("<footer")
    s = s[:i] + "\n\n" + main + s[j:]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(s)
    print("built", OUT)


def link_from_vendors():
    s = open(SRC, encoding="utf-8").read()
    s = re.sub(r"<!-- VENDOR-BADGE -->.*?<!-- /VENDOR-BADGE -->\n", "", s, flags=re.S)
    anchor = ' <div class="cta-block" style="margin-top:28px;">'
    if anchor not in s:
        print("  no CTA anchor on /vendors/"); return
    note = ('<!-- VENDOR-BADGE -->\n <p class="vd-disclaimer">Listed here? <a href="/vendors/badge/">Get our Preferred Vendor badge</a> '
            'for your website (optional).</p>\n<!-- /VENDOR-BADGE -->\n')
    s = s.replace(anchor, note + anchor, 1)
    open(SRC, "w", encoding="utf-8").write(s)
    print("linked from /vendors/")


if __name__ == "__main__":
    render_badges()
    build_page()
    link_from_vendors()
