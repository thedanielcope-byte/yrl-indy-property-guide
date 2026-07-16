# Home Value Tracker — recurring homeowner equity alerts

This is the Your Realty Link version of the "homeowner report" engine that platforms like
Luxury Presence charge $250–$550/mo for. It reuses the valuation tool you already have
(RentCast AVM + Resend/SMTP mailer + brand email template), so there's no new platform and
no new subscription.

**The play:** enroll a homeowner once. Every 30 days they get an email showing what their
home is worth today, what changed since last month, and **how much equity they've gained
since they bought**. Every email ends in a CTA for a real CMA from Daniel. When someone's
value moves meaningfully, Daniel gets an alert so he can call while the number is fresh.

Past clients are the best list to start with — they already know Daniel, and the
"you've gained $135,000" number is what turns a past client into a listing.

---

## Quick start

```bash
cd valuation-tool

# 1. Enroll a homeowner (prices the property now — that's their baseline)
npm run enroll -- "1234 Broad Ripple Ave, Indianapolis, IN 46220" jane@example.com "Jane Smith"

# 2. Preview what would go out — no emails sent, nothing written
npm run equity:dry

# 3. Send for real
npm run equity

# See who's enrolled and when each is next due
npm run equity:list
```

## Commands

| Command | What it does |
|---|---|
| `node src/equity-tracker.js enroll "<address>" <email> [name]` | Add a homeowner; prices the property now as their baseline |
| `node src/equity-tracker.js run` | Send updates to everyone due |
| `node src/equity-tracker.js run --dry-run` | Price + print, but send nothing and write nothing |
| `node src/equity-tracker.js run --force` | Ignore the 30-day schedule and run everyone |
| `node src/equity-tracker.js list` | Show subscribers + days until next due |
| `node src/equity-tracker.js remove <email>` | Remove a homeowner |

## How it works

- **Due check** — a subscriber is due when it's been `intervalDays` (default **30**) since
  `lastSentAt`. Never-sent subscribers are always due, so a first run sends their welcome
  report. Set `active: false` on a record to pause someone without deleting them.
- **The numbers** — each run computes:
  - `vsLast` — movement since their previous report (the "what changed" number)
  - `vsEnrolled` — movement since they joined
  - `vsPurchase` — equity gained since they bought (only when RentCast knows the last sale price)
- **Agent alert** — if `vsLast` moves **≥ $10,000 or ≥ 2.5%** (up *or* down), Daniel gets a
  `[EQUITY]` email. Down moves matter too — that's a price-expectation conversation.
- **Failure handling** — state is only written *after* the homeowner's email actually sends,
  so a failed send is retried on the next run rather than silently skipped.

## Scheduling it

The tracker is a plain Node script — run it on any scheduler. Daily is fine; it only emails
people who are actually due.

**macOS / Linux cron** — every day at 9am:
```
0 9 * * * cd "/path/to/indypropertyguide/valuation-tool" && /usr/local/bin/node src/equity-tracker.js run >> /tmp/equity.log 2>&1
```

Because the store is a local JSON file, this needs to run somewhere consistent. Options:
1. **Daniel's Mac** via cron/launchd — simplest, zero cost, but only runs when the Mac is on.
2. **A small always-on host** (Render/Railway/a VPS) — reliable; needs the store on a volume.
3. **Move the store to Supabase** — you already have a Supabase project. This is the right
   answer if this becomes a real program; then a scheduled edge function can drive it.

Start with (1) to prove it works, move to (3) when the list grows.

## Wiring it to GHL

GHL stays the CRM and the system of record for the *relationship*; the tracker just owns the
*valuation loop*. Three ways to get people in, easiest first:

1. **Past clients (do this first).** Export past clients from GHL (name, email, property
   address) and enroll them. This is the highest-value list you have.
2. **Site valuation requests.** `assets/js/valuation-form.js` already posts every valuation
   request to the GHL webhook. Tag those contacts `home-value-tracker` in GHL, export
   periodically, and enroll them.
3. **Automatic (future).** `src/server.js` is already a webhook listener — point a GHL
   workflow at it to auto-enroll on tag-add, so no export step is needed.

Suggested GHL custom fields if you want the numbers visible on the contact record:
`tracker_enrolled_value`, `tracker_last_value`, `tracker_last_sent`.

## Costs

Every priced property is **one RentCast AVM call per run**. 100 homeowners on a monthly
cadence ≈ **100 calls/month** (plus one per enrollment). Check your RentCast plan's included
quota before enrolling a big list — `--dry-run` still makes the API calls, so it costs the
same as a real run.

## Data & compliance

- `subscribers.json` holds **homeowner PII** (names, emails, home addresses). It is
  **gitignored and must never be committed.** Back it up somewhere private.
- Every email includes a plain-English opt-out ("reply stop"). **Honor it** —
  `npm run equity:list` then `remove <email>`. Required under CAN-SPAM.
- The email states plainly that it's an automated estimate and not an appraisal. Keep that —
  it sets the right expectation and is what makes the CMA CTA land.
