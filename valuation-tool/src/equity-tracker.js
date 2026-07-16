/**
 * Home Value Tracker — recurring homeowner equity updates.
 *
 * Enroll a homeowner once, then run `npm run equity` on a schedule. Each run
 * re-prices every due property through RentCast, emails the homeowner what
 * changed, and pings the agent when a move is big enough to act on.
 *
 *   node src/equity-tracker.js enroll "123 Main St, Indianapolis, IN 46227" jane@x.com "Jane Smith"
 *   node src/equity-tracker.js run [--dry-run] [--force]
 *   node src/equity-tracker.js list
 *   node src/equity-tracker.js remove jane@x.com
 *
 * NOTE: every priced property costs one RentCast AVM call per run.
 */
import { getFullValuation } from './rentcast.js';
import { buildEquityEmailHTML, buildAgentEquityAlertHTML, formatDelta } from './equity-email.js';
import { sendEmail, isEmailConfigured } from './mailer.js';
import { config } from './config.js';
import {
  loadSubscribers, saveSubscribers, findSubscriber, newSubscriber,
  computeDeltas, isNotable, isDue, daysSince, storePath, DEFAULT_INTERVAL_DAYS,
} from './subscribers.js';

function money(n) {
  if (n == null) return 'N/A';
  return '$' + Math.round(n).toLocaleString('en-US');
}

async function cmdEnroll(address, email, name) {
  if (!address || !email) {
    console.error('Usage: enroll "<address>" <email> [name]');
    process.exit(1);
  }
  const list = loadSubscribers();
  if (findSubscriber(list, address, email)) {
    console.log(`Already enrolled: ${address} / ${email}`);
    return;
  }
  console.log(`Pricing ${address} ...`);
  const data = await getFullValuation(address);
  const sub = newSubscriber({ address, email, name }, data);

  // Guard against double-enrolling the same property once RentCast has
  // normalised the address into its canonical form.
  if (findSubscriber(list, sub.address, email)) {
    console.log(`Already enrolled (normalised): ${sub.address} / ${email}`);
    return;
  }
  list.push(sub);
  saveSubscribers(list);
  console.log(`Enrolled ${sub.addressLine1} — baseline ${money(data.estimate)}`);
  console.log(`Store: ${storePath()}`);
  console.log(`Run "npm run equity" to send their first update.`);
}

function cmdList() {
  const list = loadSubscribers();
  if (!list.length) return console.log('No subscribers yet. Use: enroll "<address>" <email> [name]');
  console.log(`\n${list.length} subscriber(s):\n`);
  for (const s of list) {
    const due = isDue(s) ? 'DUE' : `${Math.ceil((s.intervalDays || DEFAULT_INTERVAL_DAYS) - daysSince(s.lastSentAt))}d`;
    const status = s.active === false ? 'paused' : due;
    console.log(`  [${status.padEnd(6)}] ${(s.addressLine1 || s.address).padEnd(34)} ${String(s.email).padEnd(28)} last ${money(s.lastEstimate)}`);
  }
  console.log('');
}

function cmdRemove(email) {
  if (!email) { console.error('Usage: remove <email>'); process.exit(1); }
  const list = loadSubscribers();
  const kept = list.filter(s => String(s.email).toLowerCase() !== String(email).toLowerCase());
  if (kept.length === list.length) return console.log(`No subscriber with email ${email}`);
  saveSubscribers(kept);
  console.log(`Removed ${list.length - kept.length} subscriber(s) with email ${email}`);
}

async function cmdRun({ dryRun, force }) {
  const list = loadSubscribers();
  if (!list.length) return console.log('No subscribers yet.');

  const due = list.filter(s => force ? s.active !== false : isDue(s));
  console.log(`\n=== Home Value Tracker ===`);
  console.log(`${list.length} subscriber(s), ${due.length} due${force ? ' (forced)' : ''}${dryRun ? ' — DRY RUN (no emails, no writes)' : ''}\n`);
  if (!due.length) return console.log('Nothing due. Done.\n');

  if (!dryRun && !isEmailConfigured()) {
    console.error('Email is not configured (set RESEND_API_KEY or SMTP_* in .env). Refusing to run.');
    console.error('Use --dry-run to preview without sending.');
    process.exit(1);
  }

  let sent = 0, notable = 0, failed = 0;

  for (const sub of due) {
    try {
      console.log(`- ${sub.addressLine1 || sub.address}`);
      const data = await getFullValuation(sub.address);
      if (!data.estimate) throw new Error('no estimate returned');

      const deltas = computeDeltas(sub, data.estimate);
      const flagged = isNotable(deltas);
      console.log(`    now ${money(deltas.current)} | vs last ${formatDelta(deltas.vsLast)}${flagged ? '  <- notable' : ''}`);

      if (dryRun) continue;

      await sendEmail({
        to: sub.email,
        subject: `Your home value update — ${sub.addressLine1 || sub.address}`,
        html: buildEquityEmailHTML(sub, data, deltas),
      });
      sent++;

      if (flagged) {
        await sendEmail({
          to: config.agent.email,
          subject: `[EQUITY] ${sub.addressLine1} moved ${formatDelta(deltas.vsLast)} — ${money(deltas.current)}`,
          html: buildAgentEquityAlertHTML(sub, data, deltas),
        });
        notable++;
      }

      // Only record state after the homeowner email actually went out, so a
      // failed send is retried next run rather than silently skipped.
      const now = new Date().toISOString();
      sub.lastEstimate = data.estimate;
      sub.lastCheckedAt = now;
      sub.lastSentAt = now;
      if (data.lastSalePrice) sub.lastSalePrice = data.lastSalePrice;
      sub.history.push({ date: now, estimate: data.estimate });
      saveSubscribers(list);
    } catch (err) {
      failed++;
      console.error(`    FAILED: ${err.message}`);
    }
  }

  console.log(`\nDone. ${sent} update(s) sent, ${notable} agent alert(s), ${failed} failed.\n`);
}

const [cmd, ...args] = process.argv.slice(2);
const flags = new Set(args.filter(a => a.startsWith('--')));
const positional = args.filter(a => !a.startsWith('--'));

try {
  if (cmd === 'enroll') await cmdEnroll(positional[0], positional[1], positional[2]);
  else if (cmd === 'run') await cmdRun({ dryRun: flags.has('--dry-run'), force: flags.has('--force') });
  else if (cmd === 'list') cmdList();
  else if (cmd === 'remove') cmdRemove(positional[0]);
  else {
    console.log(`
Your Realty Link — Home Value Tracker

  enroll "<address>" <email> [name]   Add a homeowner (prices the property now as their baseline)
  run [--dry-run] [--force]           Send updates to everyone due (--force ignores the schedule)
  list                                Show subscribers and when each is next due
  remove <email>                      Remove a homeowner

Each subscriber is re-priced every ${DEFAULT_INTERVAL_DAYS} days by default.
Every priced property costs one RentCast AVM call per run.
`);
  }
} catch (err) {
  console.error('\nError:', err.message);
  process.exit(1);
}
