# GHL Workflow — Step by Step

How to build the automation that receives leads from indypropertyguide.com, tags them,
delivers the right PDF, and starts a nurture sequence.

**Time:** ~45 minutes for the first build, ~5 minutes per extra guide after that.

---

## Read this first — one critical thing

**Every form on the site posts to the same webhook URL:**

```
https://services.leadconnectorhq.com/hooks/iOT1nopTL5CnKPq44zFI/webhook-trigger/b82bea0a-88fa-4cd5-9ad5-9fa3f05e7d50
```

That includes **both**:

| Form type | Where | Sends `lead_magnet`? |
|---|---|---|
| **Lead-magnet forms** | the 4 `/resources/` pages | ✅ yes |
| **Sidebar contact forms** | 200+ city / county / service pages | ❌ no |

So **one workflow receives both kinds of lead.** The whole design below hangs on branching:
`lead_magnet` present = someone downloaded a guide. `lead_magnet` empty = a general enquiry.
Get that branch right and everything else is straightforward.

⚠️ **About the webhook URL:** GoHighLevel *generates* this URL when you create an Inbound
Webhook trigger — you can't type in your own. So:

- If a workflow already owns the URL above → **edit that workflow**, don't make a new one.
- If nothing owns it (it was deleted, or never finished) → you'll create a new workflow, GHL
  will give you a **different** URL, and **the site code has to be updated to match**.
  Send me the new URL and I'll update it everywhere in one commit.

---

## Step 0 — Find out if it's already live (2 minutes)

Before building anything:

1. Go to **https://indypropertyguide.com/resources/central-indiana-buyers-guide/**
2. Fill the form with your own name and email. Submit.
3. In GHL, check **Contacts**.

| What you see | What it means | Go to |
|---|---|---|
| Contact appears **and** you get an email | Fully built | Nothing to do — just add branches for other guides |
| Contact appears, **no** email | Webhook works, delivery missing | Step 4 |
| **Nothing** appears | Webhook is dead | Step 1 (and send me the new URL) |

---

## Step 1 — Create the workflow and capture the payload

1. GHL → **Automation → Workflows → + Create Workflow → Start from Scratch**
2. Name it: **`Website Leads — Master`**
3. Click **Add New Trigger → Inbound Webhook**
4. GHL shows you a **Webhook URL**. ⚠️ **Copy it.** If it does *not* match the URL at the top
   of this doc, send it to me — the site needs updating or nothing will arrive.
5. Leave this screen open. GHL is now listening.
6. In another tab, **submit the form again** on the buyer's guide page.
7. Back in GHL, click **Fetch Sample Request / Auto-detect**. Your submission appears.

**This step is not optional.** GHL can't map fields it has never seen. If you skip it, every
field dropdown later will be empty.

---

## Step 2 — Create the custom fields

GHL has `first_name`, `last_name`, `email` and `phone` built in. These three it does not:

**Settings → Custom Fields → Add Field** (all type *Single Line Text*, object *Contact*):

| Field name | Key |
|---|---|
| Lead Magnet | `lead_magnet` |
| Source Page | `source_page` |
| Interest Type | `interest_type` |

---

## Step 3 — Create or update the contact

Back in the workflow, **+ → Contact → Create/Update Contact**, and map:

| GHL field | Webhook value |
|---|---|
| First Name | `first_name` |
| Last Name | `last_name` |
| Email | `email` |
| Phone | `phone` |
| Lead Magnet *(custom)* | `lead_magnet` |
| Source Page *(custom)* | `source_page` |
| Interest Type *(custom)* | `interest_type` |

> **Note on the sidebar forms.** Those send a single combined `name` field instead of
> `first_name`/`last_name`. Map `name` → First Name for those; it's imperfect but workable.
> Tell me if you'd rather I split the sidebar forms into first/last to match — it's a quick change.

**Deduplication:** set the workflow to match on **email** so repeat downloaders update the
existing contact instead of creating duplicates.

---

## Step 4 — Branch by guide, tag, and deliver the PDF

Add **+ → If/Else**. Create one branch per guide, each testing the **Lead Magnet** field.

### Branch 1 — Buyer's Guide
**Condition:** `lead_magnet` **is** `central-indiana-buyers-guide`
**Actions:**
1. **Add Tag:** `Guide: Buyer's Guide`, `Buyer Lead`, `Website Lead`
2. **Send Email** — see template below
3. **Add to Workflow:** *Buyer Nurture* (Step 6)

### Branch 2 — Seller's Guide
**Condition:** `lead_magnet` **is** `central-indiana-sellers-guide`
**Actions:** Tag `Guide: Seller's Guide`, `Seller Lead`, `Website Lead` → send email → *Seller Nurture*

### Branch 3 — First-Time Buyer Checklist
**Condition:** `lead_magnet` **is** `buyer-checklist`
**Actions:** Tag `Guide: Buyer Checklist`, `Buyer Lead`, `First-Time Buyer`, `Website Lead` → email → *Buyer Nurture*

### Branch 4 — Home Selling Prep Guide
**Condition:** `lead_magnet` **is** `seller-guide`
**Actions:** Tag `Guide: Seller Prep`, `Seller Lead`, `Website Lead` → email → *Seller Nurture*

### Branch 5 — Everything else (the 200+ sidebar forms)
**Condition:** `lead_magnet` **is empty**
**Actions:**
1. **Add Tag:** `Website Lead`, `General Enquiry`
2. **Internal notification** to Daniel (email or SMS) — these are direct enquiries, not
   downloads, and deserve a faster human response than a guide download does
3. **Create Opportunity** in your pipeline at *New Lead*

---

## The four delivery emails

Send each **immediately** (no delay). Subject lines and copy below — paste as-is.

### 1. Buyer's Guide
**Subject:** Your Central Indiana Home Buyer's Guide 🏡

```
Hi {{contact.first_name}},

Thanks for grabbing the Central Indiana Home Buyer's Guide — here it is:

→ Download the Buyer's Guide (PDF)
https://indypropertyguide.com/resources/central-indiana-buyers-guide/download/Central-Indiana-Home-Buyers-Guide.pdf

Inside: the full buying process step by step, every financing option including
down-payment assistance, where to buy by county and school district, and how to
write an offer that actually wins.

Two things that help most buyers right away:
• Get pre-approved before you tour — https://indypropertyguide.com/services/mortgage-pre-approval/
• Compare areas side by side — https://indypropertyguide.com/compare/

Question as you read it? Just reply here, or call/text me at 317-201-6323.

Daniel Cope
Real Estate Broker · Your Realty Link
317-201-6323 · yourrealtylink.com
```

### 2. Seller's Guide
**Subject:** Your Central Indiana Home Seller's Guide 💰

```
Hi {{contact.first_name}},

Thanks for requesting the Central Indiana Home Seller's Guide — here it is:

→ Download the Seller's Guide (PDF)
https://indypropertyguide.com/resources/central-indiana-sellers-guide/download/Central-Indiana-Home-Sellers-Guide.pdf

Inside: how to price correctly from day one (the single biggest factor), what to
fix and what to skip, how we market on the MIBOR MLS, and what your closing costs
will actually look like.

When you're ready for a real number on your home — not an online estimate — I'll
prepare a free comparative market analysis. No cost, no obligation:
https://indypropertyguide.com/services/free-home-valuation/

Daniel Cope
Real Estate Broker · Your Realty Link
317-201-6323 · yourrealtylink.com
```

### 3. First-Time Buyer Checklist
**Subject:** Your First-Time Home Buyer Checklist ✅

```
Hi {{contact.first_name}},

Here's your First-Time Home Buyer Checklist:

→ Download the Checklist (PDF)
https://indypropertyguide.com/resources/buyer-checklist/download/First-Time-Home-Buyer-Checklist-Indy-Property-Guide.pdf

Print it, work down it, and you'll avoid the mistakes that trip up most first-time
buyers in Indiana.

One thing worth doing today: check whether you qualify for Indiana down payment
assistance. Most first-time buyers qualify for more help than they expect —
https://indypropertyguide.com/services/down-payment-assistance/

Buying your first home is genuinely a big deal. If anything is confusing, call or
text me — that's what I'm here for.

Daniel Cope
Real Estate Broker · Your Realty Link
317-201-6323 · yourrealtylink.com
```

### 4. Home Selling Prep Guide
**Subject:** Your Home Selling Prep Guide 🏠

```
Hi {{contact.first_name}},

Here's your Home Selling Prep Guide:

→ Download the Prep Guide (PDF)
https://indypropertyguide.com/resources/seller-guide/download/Home-Selling-Prep-Guide-Indy-Property-Guide.pdf

It walks through exactly what to do before you list — in the order that returns the
most per dollar. Most of it costs very little; the expensive renovations usually
aren't worth it.

When you want to know what your home is realistically worth, I'll put together a
free comparative market analysis:
https://indypropertyguide.com/services/free-home-valuation/

Daniel Cope
Real Estate Broker · Your Realty Link
317-201-6323 · yourrealtylink.com
```

---

## Step 5 — Publish and test each branch

1. Toggle the workflow from **Draft** to **Publish** (top right). *Nothing runs while it's in draft.*
2. Test **all four** guides — submit each form with a real address you can check:
   - /resources/central-indiana-buyers-guide/
   - /resources/central-indiana-sellers-guide/
   - /resources/buyer-checklist/
   - /resources/seller-guide/
3. Test **one sidebar form** (any city page) to confirm Branch 5 fires.

For each, confirm: contact created → correct tags → correct email received → PDF link works.

Use a real inbox you can check, not a fake address — you want to see the email as a lead sees it.

---

## Step 6 — Nurture sequences

Two separate workflows, each triggered by **Contact Tag added**.

### Buyer Nurture — trigger: tag `Buyer Lead`
| When | Send |
|---|---|
| Day 2 | "How much home can you actually afford?" → mortgage calculator + pre-approval |
| Day 5 | "Where should you buy?" → the Best-Of guides and comparisons |
| Day 9 | "What first-time buyers miss" → down payment assistance |
| Day 14 | Personal check-in from Daniel — plain text, no design, just "how's the search going?" |
| Day 21 | Market update + invitation to schedule a call |

### Seller Nurture — trigger: tag `Seller Lead`
| When | Send |
|---|---|
| Day 2 | "What's your home actually worth?" → free CMA |
| Day 5 | "The #1 mistake sellers make" → pricing guide |
| Day 9 | "What to fix before you list" → staging + prep |
| Day 14 | Personal check-in from Daniel |
| Day 21 | "Thinking about timing?" → market update + call invite |

**Add an exit condition to both:** remove the contact from nurture when they book an
appointment or reply. Nothing damages trust faster than automated "just checking in" emails
arriving after someone has already spoken to you.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Nothing arrives in GHL | Workflow is in **Draft**, or the webhook URL doesn't match the site's |
| Contact created, fields blank | You skipped the **Fetch Sample Request** step, or custom fields aren't mapped |
| Every lead lands in the same branch | If/Else is testing the wrong field — it must test **Lead Magnet**, not Interest Type |
| Duplicate contacts | Set deduplication to match on **email** |
| Emails not sending | Sending domain not verified in GHL Settings → Email Services |
| Sidebar leads misrouted | Branch 5 must test `lead_magnet` **is empty** and sit **last** |

---

## One thing to know about the gate

The PDFs sit at public URLs and the thank-you page links to them directly, so someone can
reach a guide without filling the form if they have the link. That's deliberate — it avoids
broken-download complaints and feels less grabby.

If you'd rather it be strict, say the word and I'll remove the download link from the
thank-you page so the **email becomes the only way to get the file**. That raises capture
quality but does cost you some goodwill when email delivery is slow.

---

## Adding a new guide later

When I build a new lead magnet, you only do three things:

1. Add an **If/Else branch** testing `lead_magnet` = the new slug (I'll tell you the slug)
2. Add the **tags** for it
3. Add the **delivery email** with the new PDF link

The webhook, contact mapping, and nurture sequences are already built — nothing else changes.
