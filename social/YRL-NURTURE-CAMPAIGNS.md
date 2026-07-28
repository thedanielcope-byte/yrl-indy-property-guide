# YRL Nurture Campaigns — built in the Nomad Hub

Three email nurture sequences are built in your CRM (Supabase project `wdvolamasztetwpitbwg`,
`crm_campaigns` / `crm_campaign_steps`, `company_key = yrl`). They replace what would have
been GHL workflows.

**They are safe right now — nothing is sending.** Every campaign is `status = draft` and
`mode = simulate`, with **zero contacts enrolled**. No email goes out until you review the
copy and flip the switches yourself.

## What's built

| Campaign | Steps | Runs over | Feeds from |
|---|---|---|---|
| **YRL — Buyer Nurture** | 6 | 21 days | buyer guide, first-time-buyer checklist, buyer sidebar forms |
| **YRL — Seller Nurture** | 6 | 21 days | seller guide, seller/prep checklists, seller sidebar forms |
| **YRL — Relocation Nurture** | 6 | 27 days | moving guide + moving checklist |

All: warm lane (Resend), from `Daniel Cope, Your Realty Link <portal@nomadsystems.co>`,
reply-to `csirealtyteam@yourrealtylink.com`, 9am send, business days only, Indianapolis time.
Every email uses `{{first_name|there}}`, is written in your voice, links to the matching
site pages, and ends with a soft opt-out.

**Campaign IDs** (you'll need these to auto-enroll from forms):
- Buyer Nurture: `ca35664c-2ffc-498a-b3f3-dc78b75c1d75`
- Seller Nurture: `661eb57b-0c1a-4c17-8798-ec3af9370964`
- Relocation Nurture: `79ee05c4-1233-447a-82f1-113255c4d89e`

## Step 1 — Review the copy

In the Hub: **CRM → Sequences → open each campaign**. Read every step. This is your name and
your brand voice going out, so change anything that doesn't sound like you. The steps editor
lets you edit subject and body inline.

## Step 2 — Test in simulate mode

With `mode = simulate`, the engine runs the logic and logs what it *would* send without
actually sending. Enroll yourself (add your own contact to the sequence) and use **"Run engine
now"** to watch it step through. Confirm the merge tags fill in and the links work.

## Step 3 — Go live (per campaign, when you're happy)

Two switches per campaign:
1. `status`: **draft → active** (the scheduler only touches active campaigns)
2. `mode`: **simulate → live** (now it actually sends via Resend)

Do one campaign first (Buyer is the highest-volume), watch a real enrollment run a step or
two, then flip the others.

## Step 4 — Enroll leads (two ways)

**A. Bulk / manual (start here).** In the Hub → Contacts, filter YRL contacts by tag
(`lead-magnet`, or by `interest_type`), select them, and **Add to sequence**. Good for
enrolling the people who've already downloaded.

**B. Automatic on new downloads (the real engine).** The `capture-lead` endpoint accepts an
optional `campaign_id` and auto-enrolls. To make every new download drip automatically, each
lead-magnet form just needs to send the right `campaign_id`:
- buyer magnets (`central-indiana-buyers-guide`, `buyer-checklist`, `new-construction-checklist`) → Buyer campaign id
- seller magnets (`central-indiana-sellers-guide`, `seller-guide`, `home-sellers-checklist`) → Seller campaign id
- `moving-to-indianapolis-checklist` → Relocation campaign id

I can wire this into the forms in one pass whenever you say go — I held off so you can review
the copy first. (Auto-enroll still only *sends* once a campaign is `active` + `live`, so it's
safe to wire early.)

## Known limitation — reply auto-stop

The reply-detection poller (auto-stop a sequence when someone replies) needs the Gmail lane,
which isn't wired yet per your migration plan. So on the **warm lane, a reply won't
automatically pause the drip.** Until that's built:
- Watch replies to `csirealtyteam@yourrealtylink.com` and manually pause/unenroll anyone who
  responds or books a call — an automated "just checking in" after a real conversation is the
  one thing that damages trust.
- "Reply STOP" is honored via the suppression list / `do_not_email` — add anyone who asks.

## If you want to change timing

`crm_campaign_steps.delay_days` is the wait **before** each step (relative to the previous
one). Current cadence: day 0, +2, +3, +4, +5, +7 (buyer/seller); day 0, +3, +4, +5, +6, +9
(relocation). Edit in the steps editor.
