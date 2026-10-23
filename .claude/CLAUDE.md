# CLAUDE.md — Your Realty Link SEO Site
# yourrealtylink.com (formerly indypropertyguide.com → janetgiles.com)
# Last updated: September 2026

---

> ⚠️ **READ FIRST — CURRENT STATE (Sept 2026).** Everything from "PROJECT OVERVIEW" down is the ORIGINAL WordPress build plan and is now **largely HISTORICAL** (page templates and the build/blog lists are still a useful reference; the WordPress/Cloudways/Yoast stack, the `indypropertyguide.com`/`janetgiles.com` domains, and "no IDX" are not current). **This box is the source of truth for how the site actually works today:**
>
> - **Live site:** **`yourrealtylink.com`** — **static HTML on GitHub Pages** (repo `thedanielcope-byte/yrl-indy-property-guide`, site in dir `indypropertyguide/`; a push to `main` auto-deploys). ~1,160 pages. NOT WordPress.
> - **Domain migration COMPLETE:** lineage `indypropertyguide.com` → `janetgiles.com` → **`yourrealtylink.com`**. Both old domains **301 directly** to yourrealtylink.com (path-preserving, via Cloudflare) and **GSC Change of Address is filed for both**. Use `yourrealtylink.com` for ALL new URLs / canonicals / `og:url` / sitemap `<loc>` / CTAs. (The `.py` generators are fixed to emit it — a Sep-2026 bug had 25 generators still hardcoding `janetgiles.com`; corrected.)
> - **IDX search:** **Displet IDX Pro** embed is **LIVE** on `/search/` + the home-page office feed (confirmed working for US visitors; it returns 503 from the UK — a geo-block on MIBOR data, not a bug). All "Search Homes" links funnel to `/search/`. Per-city listings on city pages need a Displet **Premium** upgrade.
> - **How the site is built:** data-driven Python generators (`build_*.py`, reading JSON / `*_data.py`) + **idempotent, marker-wrapped injectors** (`inject_*.py`) that add/refresh sections on existing pages. Nav & footer are duplicated across every page → change them with site-wide `.replace()` scripts, HTML-only. **Never reflow whitespace or run broad text passes over `agent-pages.py` output.** Guard against iCloud dupes (`find . -name '* 2.*' -delete`) before committing generated batches.
> - **Agent directory:** `/agents/` hub + per-agent pages from `agent-pages.py` ← `agents-roster.json` ← the YRL hub (Supabase) via **`sync-roster.py`** (photos, bios, specialties, service areas). **Runs DAILY as a GitHub Action** (`.github/workflows/sync-agents.yml`) → broker edits in the hub reach the site automatically within a day. Headshots are optimized to ~600px JPEG (sips locally / Pillow on CI) and self-hosted at `assets/img/agents/<slug>.jpg`.
> - **Brand & compliance:** "Your Realty Link" / **Janet Giles-Schultz, Principal Broker** (renamed from "Indy Property Guide"). Site copy = brokerage/team voice; use "Daniel Cope" only on his own agent tile / bylines. **Never** advertise buyer agency as unconditionally free (a Buyer Representation Agreement is required). Never fabricate stats, community names, schools, or providers — verify or use ranges.
> - **Sept 2026 technical-SEO + performance cleanup (shipped):** 0 duplicate titles, complete Twitter cards site-wide, meta descriptions ≤160 chars, internal-linking orphans 88 → ~10, heading-hierarchy footer fix, images 168 MB → ~24 MB (resize + pngquant), 76 MB of orphaned source files removed, sitemap `lastmod` refreshed on all 1,026 URLs, all internal links valid.
> - **Sept 9 2026 — GSC/GBP analysis + off-page (see [[project_seo_audit]]):** GSC showed **56% of impressions were hitting OLD Agent3000 URLs that 404** (`/content/*`, `/property-search`, `/agent-search`, `/home-valuation`) — several still page 1. **Fixed with 20 meta-refresh redirect stubs** → the new pages (in the repo: `content/*/`, `property-search/`, `agent-search/`, `home-valuation/`; same pattern as `sell-my-home-indianapolis/`). Only ~230 of ~1,160 pages indexed (**810 "discovered, not indexed" = authority-bound**, not a bug); Dan requested indexing on the top ~20 money pages. Domain young but improving (avg pos ~26 → ~17). **Off-page:** citations handled via **BrightLocal**; **review-request flow BUILT Sep 27 2026** (`/review/` page → direct Google review link, QR codes, text/email templates — see `Review-Request-Playbook.md`); two playbooks delivered in the YRL root — `GBP-Optimization-Playbook.md` and `YRL-Backlink-Plan.md`. **Biggest remaining levers are OFF-PAGE + time** (reviews + local/editorial backlinks → authority → indexing). A few blog descriptions/titles remain Supabase-side (fix in the hub). GitHub Pages has NO server-side 301 → meta-refresh stubs are the redirect mechanism for legacy inbound URLs.
> - **Sept 19–27 2026 — things not to break:** **GA4** (`G-SNV86NLT23`) is on every page; any generator that builds `<head>` from scratch must be followed by `inject_gtag.py` (already wired into the 3 GitHub Actions). **Lead forms** use **Cloudflare Turnstile** (sitekey `0x4AAAAAAFBn_J2vobl7Yrk7`; secret = Supabase env `TURNSTILE_SECRET`) plus a honeypot in `assets/js/lead-form.js` / `valuation-form.js`; the Supabase `capture-lead` function is **shared by all of Dan's businesses** (scope any change by `company_key`) and rejects YRL leads without a valid token; lead `source` = `yourrealtylink.com`. The footer's **"Licensed in Indiana"** is MIBOR-required (firm name + state of licensure) — keep it; generators pull the footer from `index.html`. **`/review/`** = review-request page (noindex) → direct Google review link, place ID `ChIJVwJ1dGFda4gRADdrVWlDYtk`. Newer systems: `/press/` (`build_press.py`), `/best/` generator (`build_best.py`), AI-Overview Quick Answers (`inject_ai_answer.py` + `ai-answers.json`), `/compare/` pages retitled "Which Suburb Is Better?" with a front-loaded related pool. **GSC Sep 26:** 830 indexed, 333 discovered-not-indexed, AI Overviews ~276 impressions/day. Current status + open items: `REMAINING-TASKS.md`.
> - **Sept 28 – Oct 14 2026 — things not to break:** General contact email is **`indy@yourrealtylink.com`** (site-wide + footer + lead notifications via `crm_companies.notify_email`). **Site search:** search boxes send `/search/?q=…`; `inject_search_query.py` turns it into a Displet `base_query` filter (`street_address` / `city` / `postal_code` / `listing_id` — verified working); re-run it if `search/index.html` is rebuilt. **City + county titles** come from `geo_titles.py` ("<Town>, IN Homes for Sale & Real Estate"); `build_city.py` uses it. **`inject_best_links.py`** links the `/best/` rankings from city pages, each other and the homepage — re-run after `build_best.py` or new city pages. `/neighborhoods/southport-indianapolis/` is a redirect stub to the Southport city page. The 124 per-city `/resources/*-home-(buyers|sellers)-guide/` pages are **noindex + out of the sitemap** on purpose (thin lead-capture pages). Cal.com booking questions live in Cal.com (edit via the `cal-admin` Supabase function); answers flow to the CRM through `cal-webhook`. SEO audit (Oct 14): https://claude.ai/artifact/7pdjNp3pGo5eQf7bqgBQzv
> - **Oct 14 2026 audit follow-through — re-runnable builders/injectors:** `build_areas.py` (Perry / Center Grove / Franklin Twp / Decatur Twp area pages from the Pike shell), `build_probate.py`, `build_compare3.py` (3-way compare; skipped by `inject_compare_links.py`), `build_chicago_post.py`, plus marker injectors `inject_indiana_law.py` (INDIANA-LAW), `inject_pros_cons.py` (PROS-CONS, 8 suburbs), `inject_tax_2027.py` (TAX-2027), `inject_area_links.py` (AREA-LINK). **Franklin's price range is $200s–$400s** everywhere (incl. `city_guides_data.py`). Legal copy cites the 2026 Indiana Code — keep the "general information, not legal advice" lines. **Supabase:** `get_yrl_roster`, `get_yrl_vendors`, `get_yrl_agent_self`, `upsert_yrl_agent_self` are pinned to the YRL client id (`cf007287-…`) — `hub_content` keys are only unique per client, so never query a `yrl-*` key without `client_id`.

---

## 🎯 PROJECT OVERVIEW

Build a WordPress SEO site at **indypropertyguide.com** that:
- Ranks organically for Central Indiana real estate keywords
- Generates buyer, seller, investor, and agent recruiting leads
- Links every page back to **yourrealtylink.com** (main site) for IDX search, home valuation, and agent contact
- Is built on WordPress hosted on Cloudways with Yoast SEO, GeneratePress theme, Breeze cache, Smush, WPForms

**This site does NOT have IDX listings.** Every property search CTA links to yourrealtylink.com.

---

## 🏗️ TECH STACK

| Component | Tool |
|-----------|------|
| CMS | WordPress (Cloudways hosted) |
| Theme | GeneratePress |
| SEO Plugin | Yoast SEO |
| Cache | Breeze (Cloudways) |
| Images | Smush (compression) |
| Forms | WPForms Lite |
| Spam | Akismet |
| Header/Footer injection | WPCode |
| Domain | indypropertyguide.com |
| DNS | GoDaddy (A record → Cloudways IP) |

---

## 🎨 BRAND & DESIGN STANDARDS

### Colors
```
Primary Red:   #c03926
Gray:          #6e6e70
Dark:          #1a1a1a
White:         #ffffff
Light BG:      #f7f7f7
```

### Logo
```
URL: https://Agent3000.com/admin/upload/logos/MIBOR/MBR1322.png
Alt: Your Realty Link
```

### Contact Info (use on every page)
```
Brokerage:  Your Realty Link
Broker:     Janet Giles-Schultz
Phone:      317-997-7404
Email:      indy@yourrealtylink.com   (general contact, site-wide + in the footer since Sep 28 2026; also receives website lead notifications via crm_companies.notify_email; janet@ only for Janet personally — her agent page, press media contact, recruiting pages)
Address:    2302 E Southport Rd, Indianapolis, IN 46227
Main Site:  https://yourrealtylink.com
```

### Social Links
```
Facebook:  https://www.facebook.com/yourrealtylink
Twitter:   http://twitter.com/janetgiles
LinkedIn:  https://www.linkedin.com/in/janetgilesrealtor/
YouTube:   https://www.youtube.com/results?search_query=yourrealtylinkIndy
Pinterest: https://pinterest.com/realtor317
Instagram: http://www.instagram.com/IndianapolisRealEstate
```

---

## 📁 WORDPRESS CONFIGURATION (Already Done)

These settings are already configured — DO NOT change them:
- Permalinks: Post Name (`/%postname%/`)
- Homepage: static page titled "Home"
- Posts page: static page titled "Blog"
- Reading: "Discourage search engines" is UNCHECKED
- Yoast SEO: configured
- All plugins: active
- Header/footer: injected via WPCode

---

## 🗂️ WORDPRESS CATEGORIES (Already Created)

Create these if not already present:
1. Indianapolis Real Estate
2. Market Updates
3. Buying a Home
4. Selling a Home
5. Expired Listings
6. For Sale By Owner
7. Divorce & Estate Sales
8. Investment Properties
9. New Construction
10. Neighborhoods
11. City Guides
12. Mortgage & Finance
13. Join Our Team
14. Relocation
15. Senior Real Estate

---

## 📐 PAGE TEMPLATES

### Standard SEO Page Meta Requirements
Every page MUST have:
- **Yoast SEO Title**: `[Page Topic] | Indy Property Guide`
- **Yoast Meta Description**: 150–160 characters, include primary keyword
- **Focus Keyword**: set in Yoast
- **Schema**: LocalBusiness + RealEstateAgent on all pages
- **Internal links**: minimum 2 links to other pages on this site
- **CTA link**: minimum 1 link back to yourrealtylink.com

---

## 🏙️ TEMPLATE A — CITY PAGE

**Target word count:** 700–900 words
**URL pattern:** `/cities/[county-slug]/[city-slug]-indiana-real-estate/`
**Example:** `/cities/hamilton-county/carmel-indiana-real-estate/`

### Page Structure

```
H1: [City Name] Indiana Real Estate & Homes for Sale

[INTRO — 150 words]
Opening paragraph about the city. Cover: location relative to Indianapolis,
character/vibe, population, why people move here, what types of buyers YRL
serves in this area. Mention "Your Realty Link" naturally.

H2: Living in [City Name], Indiana
[100–150 words] Lifestyle, parks, restaurants, community feel, events,
what makes this city unique. Keep it conversational and local.

H2: [City Name] Home Prices & Real Estate Market
[100–150 words] General price ranges (do NOT use specific current prices —
say "homes typically range from the mid-$200s to the upper $400s" etc.
based on the city tier). Types of homes: ranch, two-story, new construction,
historic. Mention variety of neighborhoods.

H2: Schools in [City Name]
[80–100 words] Name the school district. Mention it's a top reason families
move here. Note elementary, middle, and high school presence without
listing specific school ratings (these change).

H2: Commute from [City Name] to Indianapolis
[60–80 words] Approximate drive time/miles to downtown Indianapolis.
Which highways serve the area (I-65, I-70, I-74, US-31, SR-37, SR-135,
etc. — pick the right ones per city). Mention commuter-friendly nature.

H2: Work With a [City Name] Real Estate Agent
[100 words] Introduce Your Realty Link. We serve buyers and sellers in
[City]. Janet Giles-Schultz leads a team of experienced MIBOR agents.
Whether buying or selling, YRL has local knowledge and a proven marketing
plan. End with CTA.

[FAQ SECTION — Yoast schema FAQ block]
3–4 questions. Examples:
Q: What is the average home price in [City]?
A: Homes in [City] typically range from [general range]. Contact YRL for
a free comparative market analysis.

Q: Is [City] a good place to buy a home?
A: Yes — [1–2 sentences about why].

Q: How do I search homes for sale in [City]?
A: Use the YRL property search at yourrealtylink.com to browse all
active MLS listings in [City].

[CTA BLOCK 1]
Button: "Search Homes in [City]" → https://yourrealtylink.com/property-search

[CTA BLOCK 2]
Button: "Get a Free Home Valuation in [City]" → https://yourrealtylink.com/home-valuation
```

### City Page Price Tier Guide
Use these approximate ranges when writing price content:

| City | Price Range Language |
|------|---------------------|
| Carmel, Zionsville | $400s to $1M+ |
| Fishers, Westfield, Noblesville | $300s to $600s |
| Greenwood, Avon, Brownsburg | $250s to $450s |
| Plainfield, Danville, Bargersville | $230s to $400s |
| Indianapolis (general) | $150s to $500s+ |
| Lawrence, Beech Grove | $150s to $320s |
| Shelbyville, Greenfield, Anderson | $150s to $300s |
| McCordsville, New Palestine | $280s to $500s |
| Mooresville, Martinsville | $200s to $380s |
| Rural/small towns | $120s to $280s |

---

## 🏛️ TEMPLATE B — COUNTY HUB PAGE

**Target word count:** 900–1,100 words
**URL pattern:** `/counties/[county-slug]-indiana-real-estate/`
**Example:** `/counties/hamilton-county-indiana-real-estate/`

### Page Structure

```
H1: [County Name] County Indiana Real Estate

[INTRO — 150 words]
County overview: size, location, number of cities/towns, character,
proximity to Indianapolis. Why people choose this county. Growth trends.

H2: Cities & Towns in [County Name] County
[Paragraph intro + grid or list of all cities with links to their city pages]
Link every city to its city page URL.

H2: [County Name] County Real Estate Market
[150 words] Market commentary: price trends, buyer demand, home styles
prevalent in the county. Mention whether it's growing, established, or
rural. Do NOT use specific dated stats.

H2: Why Buy a Home in [County Name] County
[150 words] Quality of life, school systems (name the main districts),
growth, affordability vs. Marion County. Activities, outdoor recreation,
employers.

H2: Selling Your Home in [County Name] County
[100 words] YRL seller services: free CMA, marketing plan, commission
structure, MIBOR MLS access. Link to home valuation page.

H2: Your Realty Link Serves [County Name] County
[100 words] Our team covers all of [County]. Janet Giles-Schultz and
YRL agents know this market. Ready to help buyers and sellers.

[CTA BLOCK]
Button: "Search Homes in [County]" → https://yourrealtylink.com/property-search
Button: "Get a Free Home Valuation" → https://yourrealtylink.com/home-valuation
Button: "Contact Your Realty Link" → https://yourrealtylink.com/contact
```

---

## 🛠️ TEMPLATE C — SERVICE PAGE

**Target word count:** 800–1,200 words (specialty situations: 1,000–1,500)
**URL pattern:** `/services/[service-slug]/`
**Example:** `/services/expired-listings/`

### Page Structure

```
H1: [Service Name] in Indianapolis & Central Indiana

[INTRO — 150 words]
Address the person's pain point or situation FIRST. Show empathy.
Then introduce Your Realty Link as the solution. Be specific to Indiana.

H2: [Describe Their Situation]
[150 words] Describe what they're going through. Validate it.
This is the "you're not alone" section.

H2: How Your Realty Link Helps
[150–200 words] Specific services YRL provides for this situation.
Concrete, action-oriented. Mention Janet Giles-Schultz by name.

H2: What to Expect When You Work With YRL
[150 words] Step-by-step what happens: initial call → CMA/consultation →
plan → execution. Reduces anxiety and builds confidence.

H2: Why Choose Your Realty Link for [Service]
[100 words] Experience, MIBOR membership, local knowledge, commission
structure, marketing plan. Differentiate from big box agents.

[FAQ — 3–4 questions with Yoast FAQ schema]
Anticipate their real questions. Be honest and helpful.

[CTA BLOCK — prominent]
Button: "Call Janet Giles-Schultz: 317-997-7404"
Button: "Contact Your Realty Link" → https://yourrealtylink.com/contact
Button: [relevant secondary CTA — search/valuation depending on service]
```

---

## 📝 TEMPLATE D — BLOG POST

**Target word count:** 900–1,400 words
**URL pattern:** `/blog/[post-slug]/`
**WordPress**: Posts → Add New → assign Category + Featured Image + Yoast fields

### Post Structure

```
[TITLE — include keyword naturally]
Use numbers when possible: "7 Things...", "5 Reasons...", "How to..."

[INTRO — 100–120 words]
Hook with a relatable scenario specific to Indianapolis/Indiana.
Tell them exactly what they'll learn. Include the focus keyword in
first 100 words.

[H2 — SECTION 1]
[150 words] First main point. Be specific to Central Indiana.

[H2 — SECTION 2]
[150 words] Second main point.

[H2 — SECTION 3 through 5–7]
[150 words each] Continue with remaining points.

[H2 — CONCLUSION / NEXT STEPS]
[100 words] Summarize key takeaway. Transition to CTA naturally.

[CTA BLOCK — end of every post]
"Ready to [buy/sell/invest] in Indianapolis? Contact Your Realty Link today."
Button or link to: https://yourrealtylink.com/contact OR
https://yourrealtylink.com/property-search OR
https://yourrealtylink.com/home-valuation
(choose the most relevant one per post)

[AUTHOR BOX]
Janet Giles-Schultz, Principal Broker — Your Realty Link
317-997-7404 | yourrealtylink.com
```

---

## 🔗 INTERNAL LINKING RULES

Follow these rules on EVERY page:

1. **City pages** → link to their county hub page + Indianapolis hub page
2. **County pages** → link to every city page within that county
3. **Service pages** → link to 2–3 relevant city pages
4. **Blog posts** → link to 2–3 city OR county OR service pages
5. **Every page** → at least 1 CTA linking to yourrealtylink.com
6. **Anchor text** → use descriptive keywords, never "click here"

### Key YRL Links (use these exactly)
```
Property Search:     https://yourrealtylink.com/property-search
Home Valuation:      https://yourrealtylink.com/home-valuation
Instant Valuation:   https://yourrealtylink.com/instant-home-valuation
Contact:             https://yourrealtylink.com/contact
Join Us:             https://yourrealtylink.com/content/join-us
New Construction:    https://yourrealtylink.com/content/new-construction
Mortgage Calculator: https://yourrealtylink.com/content/mortgage-calculator
Janet Bio:           https://yourrealtylink.com/content/janet-giles-principal-broker
```

---

## 📋 YOAST SEO FIELDS — FILL OUT ON EVERY PAGE

For every page/post, set these Yoast fields:

```
Focus Keyword:    [primary keyword for the page]
SEO Title:        [Page Name] | Indy Property Guide
                  (keep under 60 characters)
Meta Description: [150–160 chars including keyword, location, and value prop]
                  Example: "Looking to buy or sell a home in Carmel Indiana?
                  Your Realty Link connects you with top local agents.
                  Search all MLS listings and get a free home valuation."
```

---

## 🗺️ COMPLETE PAGE BUILD LIST

### PHASE 1 — Build First (Highest Priority)

#### Foundation Pages
| Page | URL | Template |
|------|-----|----------|
| Homepage | / | Custom |
| About Your Realty Link | /about/ | Custom |
| Contact | /contact/ | Custom |
| Blog Index | /blog/ | Auto (WordPress) |

#### Indianapolis Hub Pages
| Page | URL | Primary Keyword |
|------|-----|----------------|
| Indianapolis Real Estate | /indianapolis-real-estate/ | indianapolis real estate |
| Indianapolis Homes for Sale | /indianapolis-homes-for-sale/ | indianapolis homes for sale |
| Sell My Home Indianapolis | /sell-my-home-indianapolis/ | sell my home indianapolis |
| Indianapolis Real Estate Agent | /indianapolis-real-estate-agent/ | indianapolis real estate agent |
| First Time Home Buyers Indianapolis | /first-time-home-buyers-indianapolis/ | first time home buyer indianapolis |
| Indianapolis Investment Properties | /indianapolis-investment-properties/ | investment properties indianapolis |
| New Construction Indianapolis | /new-construction-indianapolis/ | new construction indianapolis |
| Indianapolis Luxury Homes | /indianapolis-luxury-homes/ | luxury homes indianapolis |

#### Phase 1 City Pages
| City | URL | County | Primary Keyword |
|------|-----|--------|----------------|
| Carmel | /cities/hamilton-county/carmel-indiana-real-estate/ | Hamilton | carmel in homes for sale |
| Fishers | /cities/hamilton-county/fishers-indiana-real-estate/ | Hamilton | fishers indiana real estate |
| Greenwood | /cities/johnson-county/greenwood-indiana-real-estate/ | Johnson | greenwood indiana homes for sale |
| Noblesville | /cities/hamilton-county/noblesville-indiana-real-estate/ | Hamilton | noblesville in real estate |
| Westfield | /cities/hamilton-county/westfield-indiana-real-estate/ | Hamilton | westfield indiana homes for sale |
| Avon | /cities/hendricks-county/avon-indiana-real-estate/ | Hendricks | avon indiana homes for sale |
| Brownsburg | /cities/hendricks-county/brownsburg-indiana-real-estate/ | Hendricks | brownsburg indiana real estate |
| Plainfield | /cities/hendricks-county/plainfield-indiana-real-estate/ | Hendricks | plainfield indiana homes |
| Zionsville | /cities/boone-county/zionsville-indiana-real-estate/ | Boone | zionsville in homes for sale |
| McCordsville | /cities/hancock-county/mccordsville-indiana-real-estate/ | Hancock | mccordsville indiana real estate |
| Southport | /cities/marion-county/southport-indiana-real-estate/ | Marion | southport indianapolis real estate |
| Shelbyville | /cities/shelby-county/shelbyville-indiana-real-estate/ | Shelby | shelbyville indiana homes for sale |
| Lawrence | /cities/marion-county/lawrence-indiana-real-estate/ | Marion | lawrence indiana real estate |
| Beech Grove | /cities/marion-county/beech-grove-indiana-real-estate/ | Marion | beech grove indiana homes for sale |
| Speedway | /cities/marion-county/speedway-indiana-real-estate/ | Marion | speedway indiana real estate |
| Franklin | /cities/johnson-county/franklin-indiana-real-estate/ | Johnson | franklin indiana real estate |

#### Phase 1 Service Pages (Highest Converting)
| Service | URL | Primary Keyword |
|---------|-----|----------------|
| Expired Listings | /services/expired-listings/ | expired listing agent indianapolis |
| For Sale By Owner | /services/for-sale-by-owner/ | for sale by owner indianapolis |
| Divorce Home Sale | /services/divorce-home-sale/ | selling a home during divorce indiana |
| Estate Sales / Probate | /services/estate-sales/ | estate sale home indianapolis |
| Inherited Property | /services/inherited-property/ | inherited home indianapolis sell |
| Pre-Foreclosure | /services/pre-foreclosure/ | avoid foreclosure indianapolis |
| Buyer Representation | /services/buyer-representation/ | buyer representation indianapolis |
| Seller Representation | /services/sell-my-home/ | sell my home indianapolis |
| Free Home Valuation | /services/free-home-valuation/ | home valuation indianapolis |
| Pricing Your Home | /services/pricing-your-home/ | how to price my home indianapolis |
| Sell Fast Indianapolis | /services/sell-fast/ | sell my house fast indianapolis |
| First Time Home Buyers | /services/first-time-home-buyers/ | first time home buyer indianapolis |
| FHA Loan Buyers | /services/fha-loan-buyers/ | fha loan homes indianapolis |
| VA Loan Buyers | /services/va-loan-buyers/ | va loan homes indianapolis |
| Relocation Buyers | /services/relocation-buyers/ | relocating to indianapolis |
| Buyer Compensation Agreement | /services/buyer-compensation-agreement/ | buyer compensation agreement indiana |
| Investment Property | /services/investment-property/ | investment property indianapolis |
| Rental Property | /services/rental-property/ | rental property indianapolis |
| New Construction Guide | /services/new-construction/ | new construction homes indianapolis |
| Builder Representation | /services/builder-representation/ | buyer agent new construction indianapolis |
| Mortgage Calculator | /services/mortgage-calculator/ | mortgage calculator indianapolis |
| Mortgage Pre-Approval | /services/mortgage-pre-approval/ | mortgage pre-approval indianapolis |
| Down Payment Assistance | /services/down-payment-assistance/ | down payment assistance indiana |
| Closing Costs Buyers | /services/closing-costs-buyers/ | closing costs buyer indiana |
| Closing Costs Sellers | /services/closing-costs-sellers/ | closing costs seller indiana |

---

### PHASE 2 — Build Second

#### County Hub Pages (All 17)
| County | URL | Primary Keyword |
|--------|-----|----------------|
| Marion County | /counties/marion-county-indiana-real-estate/ | marion county real estate |
| Hamilton County | /counties/hamilton-county-indiana-real-estate/ | hamilton county homes for sale |
| Johnson County | /counties/johnson-county-indiana-real-estate/ | johnson county real estate indiana |
| Hendricks County | /counties/hendricks-county-indiana-real-estate/ | hendricks county homes for sale |
| Hancock County | /counties/hancock-county-indiana-real-estate/ | hancock county real estate |
| Boone County | /counties/boone-county-indiana-real-estate/ | boone county homes for sale indiana |
| Madison County | /counties/madison-county-indiana-real-estate/ | madison county indiana real estate |
| Shelby County | /counties/shelby-county-indiana-real-estate/ | shelby county indiana homes |
| Morgan County | /counties/morgan-county-indiana-real-estate/ | morgan county indiana real estate |
| Montgomery County | /counties/montgomery-county-indiana-real-estate/ | montgomery county indiana real estate |
| Decatur County | /counties/decatur-county-indiana-real-estate/ | decatur county indiana homes |
| Brown County | /counties/brown-county-indiana-real-estate/ | brown county indiana real estate |
| Putnam County | /counties/putnam-county-indiana-real-estate/ | putnam county indiana homes |
| Parke County | /counties/parke-county-indiana-real-estate/ | parke county indiana real estate |
| Bartholomew County | /counties/bartholomew-county-indiana-real-estate/ | bartholomew county indiana real estate |
| Jackson County | /counties/jackson-county-indiana-real-estate/ | jackson county indiana real estate |
| Jennings County | /counties/jennings-county-indiana-real-estate/ | jennings county indiana real estate |

#### Phase 2 City Pages
| City | URL | County | Primary Keyword |
|------|-----|--------|----------------|
| Irvington | /cities/marion-county/irvington-indianapolis-real-estate/ | Marion | irvington indianapolis real estate |
| Broad Ripple | /cities/marion-county/broad-ripple-indianapolis-real-estate/ | Marion | broad ripple homes for sale |
| Geist | /cities/marion-county/geist-indiana-real-estate/ | Marion | geist indiana homes for sale |
| Eagle Creek | /cities/marion-county/eagle-creek-indianapolis-real-estate/ | Marion | eagle creek indianapolis homes |
| Danville | /cities/hendricks-county/danville-indiana-real-estate/ | Hendricks | danville indiana real estate |
| Pittsboro | /cities/hendricks-county/pittsboro-indiana-real-estate/ | Hendricks | pittsboro indiana homes |
| Arcadia | /cities/hamilton-county/arcadia-indiana-real-estate/ | Hamilton | arcadia indiana real estate |
| Cicero | /cities/hamilton-county/cicero-indiana-real-estate/ | Hamilton | cicero indiana homes for sale |
| Whitestown | /cities/boone-county/whitestown-indiana-real-estate/ | Boone | whitestown indiana real estate |
| Lebanon | /cities/boone-county/lebanon-indiana-real-estate/ | Boone | lebanon indiana homes for sale |
| Bargersville | /cities/johnson-county/bargersville-indiana-real-estate/ | Johnson | bargersville indiana real estate |
| Whiteland | /cities/johnson-county/whiteland-indiana-real-estate/ | Johnson | whiteland indiana homes |
| Greenfield | /cities/hancock-county/greenfield-indiana-real-estate/ | Hancock | greenfield indiana real estate |
| Fortville | /cities/hancock-county/fortville-indiana-real-estate/ | Hancock | fortville indiana homes for sale |
| New Palestine | /cities/hancock-county/new-palestine-indiana-real-estate/ | Hancock | new palestine indiana real estate |
| Cumberland | /cities/hancock-county/cumberland-indiana-real-estate/ | Hancock | cumberland indiana homes |
| Anderson | /cities/madison-county/anderson-indiana-real-estate/ | Madison | anderson indiana real estate |
| Pendleton | /cities/madison-county/pendleton-indiana-real-estate/ | Madison | pendleton indiana homes for sale |
| Lapel | /cities/madison-county/lapel-indiana-real-estate/ | Madison | lapel indiana real estate |
| Fairland | /cities/shelby-county/fairland-indiana-real-estate/ | Shelby | fairland indiana real estate |
| Morristown | /cities/shelby-county/morristown-indiana-real-estate/ | Shelby | morristown indiana homes |
| Mooresville | /cities/morgan-county/mooresville-indiana-real-estate/ | Morgan | mooresville indiana homes for sale |

#### Phase 2 Service Pages
| Service | URL | Primary Keyword |
|---------|-----|----------------|
| Home Staging | /services/home-staging/ | home staging indianapolis |
| Pre-Listing Prep | /services/pre-listing-prep/ | preparing home for sale indianapolis |
| Seller Net Sheet | /services/seller-net-sheet/ | seller closing costs indiana |
| Short Sale | /services/short-sale/ | short sale indianapolis |
| Job Relocation Sale | /services/job-relocation-sale/ | relocating selling home indianapolis |
| Vacant Home Sale | /services/vacant-home-sale/ | sell vacant home indianapolis |
| Rental Property Sale | /services/sell-rental-property/ | sell rental property indianapolis |
| Fix and Flip | /services/fix-and-flip/ | fix and flip indianapolis |
| Multi-Family | /services/multi-family/ | multi-family homes indianapolis |
| Move-Up Buyers | /services/move-up-buyers/ | move up homes indianapolis |
| Downsizing | /services/downsizing/ | downsizing home indianapolis |
| Luxury Home Buyers | /services/luxury-home-buyers/ | luxury homes indianapolis |
| New Home Communities | /services/new-home-communities/ | new home communities indianapolis |
| Home Equity | /services/home-equity/ | home equity indianapolis |
| USDA Loans | /services/usda-loans/ | usda loan indiana rural |
| Join Your Realty Link | /services/join-yrl/ | join real estate team indianapolis |
| Commission Structure | /services/commission-structure/ | real estate commission split indianapolis |
| Agent Training | /services/agent-training/ | real estate training indianapolis |
| Experienced Agents | /services/experienced-agents/ | experienced agent brokerage indianapolis |
| Brokerage Comparison | /services/brokerage-comparison/ | best real estate brokerage indianapolis |

#### Phase 2 Neighborhood Pages
| Neighborhood | URL | Primary Keyword |
|-------------|-----|----------------|
| Broad Ripple | /neighborhoods/broad-ripple-indianapolis/ | broad ripple homes for sale |
| Irvington | /neighborhoods/irvington-indianapolis/ | irvington indianapolis real estate |
| Geist Reservoir | /neighborhoods/geist-reservoir-indianapolis/ | geist indiana homes for sale |
| Southport (neighborhood) | /neighborhoods/southport-indianapolis/ | southport indianapolis real estate |
| Eagle Creek | /neighborhoods/eagle-creek-indianapolis/ | eagle creek indianapolis homes |
| Meridian-Kessler | /neighborhoods/meridian-kessler-indianapolis/ | meridian kessler homes for sale |
| Fountain Square | /neighborhoods/fountain-square-indianapolis/ | fountain square indianapolis homes |
| Castleton | /neighborhoods/castleton-indianapolis/ | castleton indianapolis homes |
| Pike Township | /neighborhoods/pike-township-indianapolis/ | pike township indianapolis real estate |
| Warren Township | /neighborhoods/warren-township-indianapolis/ | warren township homes for sale |

---

### PHASE 3 — Build Third

#### Phase 3 City Pages
| City | URL | County | Primary Keyword |
|------|-----|--------|----------------|
| Martinsville | /cities/morgan-county/martinsville-indiana-real-estate/ | Morgan | martinsville indiana real estate |
| Crawfordsville | /cities/montgomery-county/crawfordsville-indiana-real-estate/ | Montgomery | crawfordsville indiana real estate |
| Greensburg | /cities/decatur-county/greensburg-indiana-real-estate/ | Decatur | greensburg indiana real estate |
| Nashville | /cities/brown-county/nashville-indiana-real-estate/ | Brown | nashville indiana real estate |
| Edinburgh | /cities/johnson-county/edinburgh-indiana-real-estate/ | Johnson | edinburgh indiana real estate |
| Trafalgar | /cities/johnson-county/trafalgar-indiana-real-estate/ | Johnson | trafalgar indiana homes for sale |
| Sheridan | /cities/hamilton-county/sheridan-indiana-real-estate/ | Hamilton | sheridan indiana real estate |
| Clayton | /cities/hendricks-county/clayton-indiana-real-estate/ | Hendricks | clayton indiana real estate |
| Atlanta | /cities/hamilton-county/atlanta-indiana-real-estate/ | Hamilton | atlanta indiana real estate |
| Alexandria | /cities/madison-county/alexandria-indiana-real-estate/ | Madison | alexandria indiana real estate |
| Elwood | /cities/madison-county/elwood-indiana-real-estate/ | Madison | elwood indiana homes |
| Shirley | /cities/hancock-county/shirley-indiana-real-estate/ | Hancock | shirley indiana real estate |
| Thorntown | /cities/boone-county/thorntown-indiana-real-estate/ | Boone | thorntown indiana real estate |
| Jamestown | /cities/boone-county/jamestown-indiana-real-estate/ | Boone | jamestown indiana homes |
| Waldron | /cities/shelby-county/waldron-indiana-real-estate/ | Shelby | waldron indiana real estate |
| Monrovia | /cities/morgan-county/monrovia-indiana-real-estate/ | Morgan | monrovia indiana homes |
| Westport | /cities/decatur-county/westport-indiana-real-estate/ | Decatur | westport indiana homes |
| Bean Blossom | /cities/brown-county/bean-blossom-indiana-real-estate/ | Brown | bean blossom indiana homes |

#### Phase 3 Service Pages
| Service | URL | Primary Keyword |
|---------|-----|----------------|
| 1031 Exchange | /services/1031-exchange/ | 1031 exchange indianapolis indiana |
| Cash Flow Properties | /services/cash-flow-properties/ | cash flow real estate indianapolis |
| Off-Market Properties | /services/off-market-properties/ | off market homes indianapolis |
| Behind on Payments | /services/behind-on-payments/ | behind on mortgage payments indianapolis |
| Downsizing Estate | /services/downsizing-estate/ | downsizing large home indianapolis |
| Custom Home Building | /services/custom-home-building/ | custom home builder indianapolis |
| New Construction Negotiation | /services/new-construction-negotiation/ | negotiate new construction price indiana |
| Senior Home Buyers | /services/senior-buyers/ | senior home buyers indianapolis |
| Senior Home Sellers | /services/senior-sellers/ | senior home selling indianapolis |
| Part Time Agents | /services/part-time-agents/ | part time real estate agent indianapolis |

---

### PHASE 4 — Build Last

#### Phase 4 City Pages (Rural / BLC Counties)
| City | URL | County | Primary Keyword |
|------|-----|--------|----------------|
| Greencastle | /cities/putnam-county/greencastle-indiana-real-estate/ | Putnam | greencastle indiana real estate |
| Cloverdale | /cities/putnam-county/cloverdale-indiana-real-estate/ | Putnam | cloverdale indiana homes |
| Rockville | /cities/parke-county/rockville-indiana-real-estate/ | Parke | rockville indiana real estate |
| Columbus | /cities/bartholomew-county/columbus-indiana-real-estate/ | Bartholomew | columbus indiana homes for sale |
| Seymour | /cities/jackson-county/seymour-indiana-real-estate/ | Jackson | seymour indiana homes for sale |
| North Vernon | /cities/jennings-county/north-vernon-indiana-real-estate/ | Jennings | north vernon indiana homes |

#### Phase 4 Service Pages
| Service | URL | Primary Keyword |
|---------|-----|----------------|
| Portfolio Selling | /services/portfolio-selling/ | sell multiple properties indianapolis |
| Cash Home Buyers | /services/cash-buyers/ | cash home buyers indianapolis |
| Luxury Home Sellers | /services/luxury-home-sellers/ | sell luxury home indianapolis |
| New Construction by County | /services/new-construction-by-county/ | new homes hamilton county indiana |

---

## 📅 BLOG POST QUEUE — 90 DAYS

Build these in order. Create as WordPress Posts with Category, Featured Image, and Yoast fields filled.

| # | Title | Focus Keyword | Category | CTA Link |
|---|-------|--------------|----------|---------|
| 1 | Indianapolis Real Estate Market Update 2026 | indianapolis housing market 2026 | Market Updates | /property-search |
| 2 | Best Neighborhoods to Buy a Home in Indianapolis | best neighborhoods indianapolis | Neighborhoods | /property-search |
| 3 | How to Sell Your Home Fast in Greenwood Indiana | sell home fast greenwood in | Selling a Home | /home-valuation |
| 4 | First Time Home Buyer Guide — Indianapolis 2026 | first time home buyer indianapolis | Buying a Home | /property-search |
| 5 | Living in Carmel Indiana — What to Know Before You Move | living in carmel indiana | City Guides | /property-search |
| 6 | What Is My Home Worth in Indianapolis? | home value indianapolis | Selling a Home | /home-valuation |
| 7 | Fishers Indiana — One of America's Best Places to Live | fishers indiana real estate | City Guides | /property-search |
| 8 | Why Join a Real Estate Team Instead of Going Independent | join real estate team indianapolis | Join Our Team | /content/join-us |
| 9 | Buying New Construction in Central Indiana — Pros and Cons | new construction homes indianapolis | New Construction | /content/new-construction |
| 10 | Closing Costs in Indiana — What Sellers Need to Know | closing costs indiana seller | Selling a Home | /home-valuation |
| 11 | Zionsville Indiana — Small Town Luxury Living Near Indy | zionsville in homes for sale | City Guides | /property-search |
| 12 | Investment Property in Indianapolis — Is Now a Good Time? | investment property indianapolis | Investment Properties | /contact |
| 13 | How the Buyer Compensation Agreement Works in Indiana | buyer compensation agreement indiana | Buying a Home | /contact |
| 14 | Top 5 Things That Kill a Home Sale in Indianapolis | sell home indianapolis tips | Selling a Home | /home-valuation |
| 15 | Avon Indiana — Why Families Love Hendricks County | avon indiana homes for sale | City Guides | /property-search |
| 16 | YRL Agent Commission Structure — What You Need to Know | real estate commission split indianapolis | Join Our Team | /content/join-us |
| 17 | McCordsville Indiana — Hancock County's Fastest Growing City | mccordsville indiana real estate | City Guides | /property-search |
| 18 | Home Staging Tips for Indianapolis Sellers | home staging indianapolis | Selling a Home | /home-valuation |
| 19 | Geist Reservoir — Waterfront Homes Near Indianapolis | geist indiana homes for sale | Neighborhoods | /property-search |
| 20 | Indianapolis Housing Market Forecast — What to Expect | indianapolis housing market forecast | Market Updates | /property-search |
| 21 | Shelbyville Indiana — Affordable Living Near Indianapolis | shelbyville indiana homes for sale | City Guides | /property-search |
| 22 | How to Choose the Right Real Estate Agent in Indianapolis | best real estate agent indianapolis | Buying a Home | /contact |
| 23 | Plainfield Indiana — Hendricks County's Retail Hub | plainfield indiana real estate | City Guides | /property-search |
| 24 | My Home Expired — What Should I Do Next? | expired listing agent indianapolis | Expired Listings | /contact |
| 25 | Why FSBO Homes Sell for Less in Indianapolis | for sale by owner indianapolis | For Sale By Owner | /home-valuation |
| 26 | Selling a Home During a Divorce in Indiana | selling home during divorce indiana | Divorce & Estate Sales | /contact |
| 27 | Probate and Estate Home Sales in Indianapolis | estate sale home indianapolis | Divorce & Estate Sales | /contact |
| 28 | Down Payment Assistance Programs in Indiana 2026 | down payment assistance indiana | Mortgage & Finance | /content/mortgage-calculator |
| 29 | Brownsburg Indiana — Racing Town, Growing Suburbs | brownsburg indiana real estate | City Guides | /property-search |
| 30 | Noblesville Indiana — Hamilton County's County Seat | noblesville in real estate | City Guides | /property-search |
| 31 | What Is a Short Sale in Indiana? | short sale indianapolis | Selling a Home | /contact |
| 32 | Broad Ripple — Indianapolis's Most Vibrant Neighborhood | broad ripple homes for sale | Neighborhoods | /property-search |
| 33 | Irvington Indianapolis — Historic Charm on the East Side | irvington indianapolis real estate | Neighborhoods | /property-search |
| 34 | VA Loans in Indiana — A Complete Guide for Veterans | va loan homes indianapolis | Mortgage & Finance | /contact |
| 35 | Westfield Indiana Real Estate — Home of Grand Park | westfield indiana homes for sale | City Guides | /property-search |
| 36 | Year in Review — Central Indiana Real Estate 2025 | central indiana real estate 2025 | Market Updates | /contact |

---

## ✅ PER-PAGE CHECKLIST

Use this checklist every time you build a page:

- [ ] Title set correctly (includes keyword)
- [ ] URL/slug matches the pattern in this doc
- [ ] Template followed (correct H1, H2 structure)
- [ ] Word count meets minimum
- [ ] Yoast Focus Keyword set
- [ ] Yoast SEO Title set (under 60 chars)
- [ ] Yoast Meta Description set (150–160 chars)
- [ ] 2+ internal links to other pages on this site
- [ ] 1+ CTA link back to yourrealtylink.com
- [ ] Featured image set (for blog posts)
- [ ] Category assigned (for blog posts)
- [ ] Page published (not draft)

---

## ⚠️ IMPORTANT RULES

1. **Never make up specific stats** — avoid "median home price is $342,000" — these get outdated. Use ranges.
2. **Never claim IDX/listings exist on this site** — always send people to yourrealtylink.com for search.
3. **Always mention MIBOR** — Janet is a MIBOR member. Use "MLS" and "MIBOR" naturally.
4. **Keep YRL branding consistent** — "Your Realty Link" (not "YRL" in public-facing content), "Janet Giles-Schultz", "Principal Broker".
5. **Tone** — professional but warm. Not corporate. Think helpful local neighbor who knows real estate.
6. **Do not stuff keywords** — write for humans first. One keyword focus per page. Variations welcome.
7. **Do not duplicate content** — every city page must be uniquely written. Don't copy-paste and swap city name.
8. **Blog posts** — always end with a CTA. Never let a post just end.
9. **Specialty service pages** (expired, divorce, estate, inherited) — lead with empathy. These people are stressed.
10. **Permalinks** — always lowercase, hyphens only, no underscores, match the URL patterns in this doc exactly.

---

## 📊 TOTAL PAGE TARGETS

| Category | Count |
|----------|-------|
| Foundation / Hub Pages | 12 |
| County Hub Pages | 17 |
| City Pages | ~85 |
| Neighborhood Pages | 10 |
| Service Pages | 55 |
| Blog Posts (Year 1) | 100+ |
| **TOTAL** | **~275+** |

---

*This file is the single source of truth for building indypropertyguide.com.*
*Built for Your Realty Link — yourrealtylink.com — 317-997-7404*
*Janet Giles-Schultz, Principal Broker — 2302 E Southport Rd, Indianapolis IN 46227*
