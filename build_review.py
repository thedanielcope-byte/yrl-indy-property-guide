#!/usr/bin/env python3
"""
build_review.py — /review/ : a frictionless "leave us a review" landing page for the
review-request flow. Clients tap the link (texted/emailed after closing, or a printed QR)
and land here → one tap to the Google review dialog or Facebook.

Google-policy compliant: NO rating gate (everyone sees the same Google + Facebook buttons;
we don't route unhappy clients to a private form). noindex (client utility page, not for
search). Pulls header/footer/CSS hash from index.html like build_press.py; run inject_gtag.py
after (builds head from scratch).

Usage: python3 build_review.py
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://yourrealtylink.com"
GOOGLE_REVIEW = "https://search.google.com/local/writereview?placeid=ChIJVwJ1dGFda4gRADdrVWlDYtk"
FB_REVIEW = "https://www.facebook.com/yourrealtylink/reviews"

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
CANON_HDR = re.search(r'<header class="site-header">.*?</header>', src, re.DOTALL).group()
CANON_FTR = re.search(r'<footer class="site-footer">.*?</footer>', src, re.DOTALL).group()
TAIL = src[src.index('</footer>') + len('</footer>'):src.index('</body>')]
CSSHASH = re.search(r'style\.css\?v=([0-9a-f]+)', src).group(1)

TITLE = "Leave Us a Review | Your Realty Link"
DESC = "Share your experience with Your Realty Link — leave a quick Google or Facebook review. It takes about 30 seconds and helps other Central Indiana families."

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{TITLE}</title>
 <meta name="description" content="{DESC}">
 <meta name="robots" content="noindex, follow">
 <link rel="canonical" href="{SITE}/review/">
 <meta property="og:title" content="{TITLE}">
 <meta property="og:description" content="{DESC}">
 <meta property="og:url" content="{SITE}/review/">
 <meta property="og:image" content="{SITE}/assets/img/og-home.jpg">
 <meta property="og:type" content="website">
 <meta property="og:site_name" content="Your Realty Link">
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400..800;1,400..700&display=swap">
 <link rel="stylesheet" href="/assets/css/style.css?v={CSSHASH}">
 <style>
 .rev-wrap{{max-width:640px;margin:0 auto;text-align:center;}}
 .rev-stars{{font-size:2.4rem;letter-spacing:6px;color:#f5a623;margin:0 0 8px;}}
 .rev-wrap h1{{font-size:2rem;color:#1a1a1a;margin:0 0 14px;}}
 .rev-wrap p.lead{{font-size:1.12rem;color:#4a4a52;line-height:1.6;margin:0 0 30px;}}
 .rev-btns{{display:flex;flex-direction:column;gap:14px;max-width:420px;margin:0 auto 28px;}}
 .rev-btns a{{display:flex;align-items:center;justify-content:center;gap:10px;padding:18px 24px;border-radius:12px;font-weight:700;font-size:1.08rem;text-decoration:none;transition:transform .15s,box-shadow .15s;}}
 .rev-btns a:hover{{transform:translateY(-2px);box-shadow:0 8px 22px rgba(0,0,0,.14);}}
 .rev-google{{background:#c03926;color:#fff;}}
 .rev-fb{{background:#fff;color:#1b3a5c;border:2px solid #d6dbe2;}}
 .rev-note{{font-size:.95rem;color:#6e6e70;line-height:1.6;}}
 .rev-qr{{margin:34px auto 0;max-width:210px;}}
 .rev-qr img{{width:170px;height:170px;display:block;margin:0 auto 8px;border:1px solid #e6e6e6;border-radius:10px;padding:8px;background:#fff;}}
 .rev-qr p{{font-size:.82rem;color:#9a9a9a;margin:0;}}
 </style>
</head>
<body>
{CANON_HDR}
<main>
<section class="section">
 <div class="container">
 <div class="rev-wrap">
 <div class="rev-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
 <h1>How did we do?</h1>
 <p class="lead">If we helped you buy or sell, a quick review means the world to our team &mdash; and it helps other Central Indiana families find a broker they can trust. It takes about 30 seconds.</p>
 <div class="rev-btns">
 <a class="rev-google" href="{GOOGLE_REVIEW}" target="_blank" rel="noopener">&#11088; Leave a Google Review</a>
 <a class="rev-fb" href="{FB_REVIEW}" target="_blank" rel="noopener">Review us on Facebook</a>
 </div>
 <p class="rev-note">Thank you for trusting <strong>Your Realty Link</strong>. Questions or feedback anytime? Call us at <a href="tel:3179977404">317-997-7404</a> or email <a href="mailto:indy@yourrealtylink.com">indy@yourrealtylink.com</a>.</p>
 <div class="rev-qr">
 <img src="/assets/img/review-qr.png" alt="QR code linking to the Your Realty Link review page" loading="lazy" width="170" height="170">
 <p>Scan to open this page on your phone</p>
 </div>
 </div>
 </div>
</section>
</main>
{CANON_FTR}
{TAIL}</body>
</html>
"""

os.makedirs(os.path.join(ROOT, "review"), exist_ok=True)
open(os.path.join(ROOT, "review", "index.html"), "w", encoding="utf-8").write(page)
print("built /review/index.html")
