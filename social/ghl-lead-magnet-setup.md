# GHL Setup — Lead Magnet Guides (Buyer's & Seller's)

The two new guides use the **same webhook** your existing lead magnets already post to, so
no new webhook is needed. Each submission includes a `lead_magnet` field you can branch on.

## What the form sends to GHL

Both guide forms POST JSON to:
`https://services.leadconnectorhq.com/hooks/iOT1nopTL5CnKPq44zFI/webhook-trigger/b82bea0a-88fa-4cd5-9ad5-9fa3f05e7d50`

Fields:
| Field | Buyer's Guide | Seller's Guide |
|---|---|---|
| `first_name`, `last_name`, `email`, `phone` | (from form) | (from form) |
| `lead_magnet` | `central-indiana-buyers-guide` | `central-indiana-sellers-guide` |
| `interest_type` | `Buyer` | `Seller` |
| `source_page`, `source_url`, `submitted_at` | (auto) | (auto) |

The site already delivers the PDF instantly on the thank-you page, so GHL's job is
**(1) capture + tag, (2) email a copy, (3) start a nurture sequence.**

## One-time GHL workflow

1. **Trigger:** Inbound Webhook (the URL above) — or reuse your existing lead-magnet workflow and add branches.
2. **Create/Update Contact** from the mapped fields.
3. **Tag by branch** on `lead_magnet`:
   - `central-indiana-buyers-guide` → tag `Guide: Buyer` + `Buyer Lead`
   - `central-indiana-sellers-guide` → tag `Guide: Seller` + `Seller Lead`
4. **Send delivery email** (below) with the PDF link.
5. **Add to a nurture workflow** (buyer track vs seller track).

### PDF links to use in the emails
- Buyer's Guide: `https://indypropertyguide.com/resources/central-indiana-buyers-guide/download/Central-Indiana-Home-Buyers-Guide.pdf`
- Seller's Guide: `https://indypropertyguide.com/resources/central-indiana-sellers-guide/download/Central-Indiana-Home-Sellers-Guide.pdf`

## Delivery email — Buyer's Guide
**Subject:** Your Central Indiana Home Buyer's Guide 🏡

Hi {{contact.first_name}},

Thanks for grabbing the Central Indiana Home Buyer's Guide! Here it is:

**→ Download the Buyer's Guide (PDF)**  ← link the URL above

Inside you'll find the full buying process, every financing option (including down-payment
help), where to buy by county and school district, and how to make a winning offer in Indiana.

Have a question as you read — or want to talk through your budget and the right neighborhoods?
Just reply here, or call/text me at 317-201-6323.

Daniel Cope, Real Estate Broker
Your Realty Link · yourrealtylink.com

## Delivery email — Seller's Guide
**Subject:** Your Central Indiana Home Seller's Guide 💰

Hi {{contact.first_name}},

Thanks for requesting the Central Indiana Home Seller's Guide! Here it is:

**→ Download the Seller's Guide (PDF)**  ← link the URL above

Inside: how to price right the first time, prep & staging that returns real value, the
marketing plan that drives competing offers, and what Indiana sellers pay at closing.

Curious what your home is worth in today's market? I'll put together a free, no-obligation
comparative market analysis — just reply or call/text me at 317-201-6323.

Daniel Cope, Real Estate Broker
Your Realty Link · yourrealtylink.com

## Suggested nurture (light touch, both tracks)
- Day 0: delivery email (above)
- Day 2: "Did you get a chance to read it?" + one helpful tip + soft CTA (call/valuation)
- Day 5: relevant blog link (buyer → first-time buyer guide / schools; seller → staging / what's my home worth)
- Day 9: personal check-in from Daniel
- Day 14+: monthly market-update newsletter

## Reusable for per-city guides (phase 3)
When we build per-city guides, they'll use the **same webhook** with
`lead_magnet = <city>-buyers-guide` / `<city>-sellers-guide`. Just add branches/tags per city
(or a single "City Guide" tag + a `city` field) and reuse the same delivery/nurture emails
with the city name swapped in.
