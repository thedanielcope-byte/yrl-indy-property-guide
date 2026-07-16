import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STORE = resolve(__dirname, '..', 'subscribers.json');

export const DEFAULT_INTERVAL_DAYS = 30;

export function storePath() {
  return STORE;
}

export function loadSubscribers() {
  if (!existsSync(STORE)) return [];
  const raw = readFileSync(STORE, 'utf-8').trim();
  if (!raw) return [];
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    throw new Error(`subscribers.json is not valid JSON — refusing to continue (${err.message})`);
  }
  if (!Array.isArray(parsed)) throw new Error('subscribers.json must contain a JSON array');
  return parsed;
}

export function saveSubscribers(list) {
  writeFileSync(STORE, JSON.stringify(list, null, 2) + '\n');
}

export function makeId(address, email) {
  const slug = String(address).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-+$)/g, '');
  return `${slug}::${String(email).toLowerCase()}`;
}

export function findSubscriber(list, address, email) {
  const id = makeId(address, email);
  return list.find(s => s.id === id) || null;
}

/**
 * Days since an ISO timestamp. Returns Infinity when never set,
 * so a never-sent subscriber always reads as due.
 */
export function daysSince(iso) {
  if (!iso) return Infinity;
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return Infinity;
  return (Date.now() - then) / 86400000;
}

export function isDue(sub) {
  if (sub.active === false) return false;
  return daysSince(sub.lastSentAt) >= (sub.intervalDays || DEFAULT_INTERVAL_DAYS);
}

/**
 * Build a new subscriber record from a fresh valuation.
 * The current estimate becomes both the enrolled baseline and the last-seen value.
 */
export function newSubscriber({ address, email, name, intervalDays }, data) {
  const now = new Date().toISOString();
  return {
    id: makeId(data.address || address, email),
    name: name || '',
    email,
    address: data.address || address,
    addressLine1: data.addressLine1 || '',
    city: data.city || '',
    intervalDays: intervalDays || DEFAULT_INTERVAL_DAYS,
    active: true,
    enrolledAt: now,
    enrolledEstimate: data.estimate,
    lastSalePrice: data.lastSalePrice || null,
    lastSaleDate: data.lastSaleDate || null,
    lastEstimate: data.estimate,
    lastCheckedAt: now,
    lastSentAt: null,
    history: [{ date: now, estimate: data.estimate }],
  };
}

/**
 * Equity deltas for one update cycle.
 * vsLast     — movement since the previous report (the "what changed" number)
 * vsEnrolled — movement since they joined the tracker
 * vsPurchase — equity gained since they bought (only when a last sale price is known)
 */
export function computeDeltas(sub, current) {
  function delta(from) {
    if (from == null || !current) return null;
    const amount = current - from;
    return { amount, pct: from ? (amount / from) * 100 : null, from };
  }
  return {
    current,
    vsLast: delta(sub.lastEstimate),
    vsEnrolled: delta(sub.enrolledEstimate),
    vsPurchase: delta(sub.lastSalePrice),
  };
}

/** A move worth the agent's attention: >= 2.5% or >= $10k in either direction. */
export function isNotable(deltas) {
  const d = deltas.vsLast;
  if (!d) return false;
  return Math.abs(d.amount) >= 10000 || (d.pct != null && Math.abs(d.pct) >= 2.5);
}
