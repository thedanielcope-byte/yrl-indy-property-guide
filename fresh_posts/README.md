# fresh_posts/

One file per blog post: `fresh_posts/<slug>.py` defining `POST = dict(...)`. Built by
`build_fresh_posts.py` (see its docstring). Files starting with `_` are ignored.

Fields (all required unless marked optional):

- slug: URL slug (`/blog/<slug>/`)
- title: `<title>`, max 60 chars, no site suffix
- headline: Article headline + blog card heading + breadcrumb
- h1_html: H1 inner HTML, e.g. `Cost of Living in Indianapolis: <em>2026 Breakdown</em>`
- desc: meta description, 120-160 chars
- date: `YYYY-MM-DD`; month: e.g. `November 2026`
- category: blog category label (Relocation, Buying a Home, Selling a Home, Mortgage &amp; Finance, Market Updates)
- eyebrow: card-image eyebrow, uppercase (e.g. `RELOCATION`)
- focus: focus keyword (also the card image alt text)
- hero_sub: one-sentence hero subtitle (HTML ok)
- badges: 3 short hero badges
- read_min: minutes to read (int)
- card_title / card_sub: text on the 1200x630 card image (title <= ~48 chars)
- qa_heading, qa_lead (HTML; start with `<strong>Question?</strong> answer`), qa_facts: list of (label, value) — 4-6 dated facts
- toc: list of (h2 id, label); every id needs `<h2 id="...">` in body ("faq" is added automatically)
- body: HTML after the Quick Answer: intro <p>, then <h2 id=...> sections (h3 ok). No FAQ (added automatically).
- faqs: list of (question, answer) plain text, 4-6
- sources: list of (label, url) — url may be "" for unlinked attribution or a /site path
- related: 3 (href, label) for the sidebar
- cta: (h3, p, [(href, label, "btn-white"|"btn-outline"), ...])
- resources: 3-4 (href, label) under "Related Resources"
- link_from (optional): list of (page path, sentence HTML) to add an inbound link
- about (optional): schema.org `about` object; crumb (optional): breadcrumb text
