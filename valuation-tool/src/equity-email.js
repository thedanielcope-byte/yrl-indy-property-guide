import { config } from './config.js';

function formatCurrency(n) {
  if (n == null) return 'N/A';
  return '$' + Math.round(n).toLocaleString('en-US');
}

function formatDate(d) {
  if (!d) return '';
  return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/** "+$12,400 (+3.5%)" / "-$4,100 (-1.2%)" */
export function formatDelta(d) {
  if (!d || d.amount == null) return 'N/A';
  const sign = d.amount >= 0 ? '+' : '−';
  const abs = formatCurrency(Math.abs(d.amount));
  const pct = d.pct == null ? '' : ` (${d.amount >= 0 ? '+' : '−'}${Math.abs(d.pct).toFixed(1)}%)`;
  return `${sign}${abs.replace('$', '$')}${pct}`;
}

function deltaColor(d) {
  if (!d || d.amount == null) return '#6e6e70';
  if (d.amount > 0) return '#2e7d32';
  if (d.amount < 0) return '#c03926';
  return '#6e6e70';
}

function statRow(label, valueHTML) {
  return `
    <tr>
      <td style="padding:9px 0;font-size:12px;color:#6e6e70;border-bottom:1px solid #eee;">${label}</td>
      <td style="padding:9px 0;font-size:14px;font-weight:bold;text-align:right;border-bottom:1px solid #eee;">${valueHTML}</td>
    </tr>`;
}

/**
 * Homeowner-facing equity update.
 * Leads with the current value and what changed since the last report —
 * the two numbers a homeowner actually opens the email for.
 */
export function buildEquityEmailHTML(sub, data, deltas) {
  const firstName = (sub.name || '').trim().split(/\s+/)[0] || 'there';
  const vsLast = deltas.vsLast;
  const vsPurchase = deltas.vsPurchase;
  const isFirst = !sub.lastSentAt;

  const movementHTML = isFirst
    ? `<p style="margin:6px 0 0;font-size:13px;color:#6e6e70;">We'll track this for you and email you when it changes.</p>`
    : `<p style="margin:6px 0 0;font-size:15px;font-weight:bold;color:${deltaColor(vsLast)};">
         ${formatDelta(vsLast)} since your last update
       </p>`;

  const purchaseHTML = vsPurchase
    ? statRow('Equity gained since you bought',
        `<span style="color:${deltaColor(vsPurchase)};">${formatDelta(vsPurchase)}</span>`)
    : '';

  const enrolledHTML = (!isFirst && deltas.vsEnrolled)
    ? statRow('Change since you joined the tracker',
        `<span style="color:${deltaColor(deltas.vsEnrolled)};">${formatDelta(deltas.vsEnrolled)}</span>`)
    : '';

  const compsHTML = (data.comparables || []).slice(0, 3).map(c => `
    <tr>
      <td style="padding:8px 10px;border-bottom:1px solid #eee;font-size:12px;color:#1a1a1a;">${c.address || 'N/A'}</td>
      <td style="padding:8px 10px;border-bottom:1px solid #eee;font-size:12px;font-weight:bold;color:#c03926;text-align:right;">${formatCurrency(c.price)}</td>
    </tr>`).join('');

  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f7f7f7;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f7f7f7;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

  <!-- Header -->
  <tr><td style="background:#c03926;padding:24px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td width="80" style="vertical-align:middle;"><img src="${config.brokerage.logo}" alt="${config.brokerage.name}" width="70" style="display:block;"></td>
      <td style="vertical-align:middle;padding-left:16px;">
        <h1 style="margin:0;color:#ffffff;font-size:22px;">Your Home Value Update</h1>
        <p style="margin:4px 0 0;color:rgba(255,255,255,0.85);font-size:12px;">From ${config.agent.name}, ${config.agent.title} — ${config.brokerage.name}</p>
      </td>
    </tr></table>
  </td></tr>

  <!-- Greeting -->
  <tr><td style="padding:26px 32px 0;">
    <p style="margin:0;font-size:14px;color:#1a1a1a;">Hi ${firstName},</p>
    <p style="margin:8px 0 0;font-size:14px;color:#444;line-height:1.6;">
      ${isFirst
        ? `You're all set — here's the current estimated value of your home.`
        : `Here's this month's estimated value for your home.`}
    </p>
  </td></tr>

  <!-- Address -->
  <tr><td style="padding:18px 32px 0;">
    <p style="margin:0;font-size:17px;font-weight:bold;color:#1a1a1a;">${data.addressLine1}</p>
    <p style="margin:4px 0 0;font-size:13px;color:#6e6e70;">${data.city}, ${data.state} ${data.zipCode}</p>
  </td></tr>

  <!-- Current value + movement -->
  <tr><td style="padding:16px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f7f7f7;border-left:4px solid #c03926;border-radius:4px;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#6e6e70;">Estimated Value Today</p>
        <p style="margin:6px 0 0;font-size:32px;font-weight:bold;color:#1a1a1a;">${formatCurrency(deltas.current)}</p>
        ${movementHTML}
        <p style="margin:8px 0 0;font-size:12px;color:#6e6e70;">Range: ${formatCurrency(data.rangeLow)} — ${formatCurrency(data.rangeHigh)}</p>
      </td></tr>
    </table>
  </td></tr>

  <!-- Equity stats -->
  ${(purchaseHTML || enrolledHTML) ? `
  <tr><td style="padding:0 32px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      ${purchaseHTML}
      ${enrolledHTML}
    </table>
  </td></tr>` : ''}

  <!-- Comps -->
  ${compsHTML ? `
  <tr><td style="padding:16px 32px 0;">
    <h2 style="margin:0 0 10px;font-size:15px;color:#c03926;border-bottom:1px solid #c03926;padding-bottom:8px;">Recent Nearby Sales</h2>
    <table width="100%" cellpadding="0" cellspacing="0">${compsHTML}</table>
  </td></tr>` : ''}

  <!-- CTA -->
  <tr><td style="padding:24px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#1b3a5c;border-radius:6px;">
      <tr><td style="padding:22px 24px;text-align:center;">
        <p style="margin:0 0 6px;color:#ffffff;font-size:16px;font-weight:bold;">Thinking about selling?</p>
        <p style="margin:0 0 14px;color:rgba(255,255,255,0.85);font-size:13px;line-height:1.6;">
          This is an automated estimate — not a substitute for walking your home. For a real number based on
          your finishes, updates, and today's buyers, I'll prepare a free comparative market analysis.
        </p>
        <a href="tel:${config.agent.phone.replace(/-/g, '')}"
           style="display:inline-block;background:#c03926;color:#ffffff;text-decoration:none;font-weight:bold;font-size:14px;padding:12px 26px;border-radius:6px;">
          Call ${config.agent.name}: ${config.agent.phone}
        </a>
      </td></tr>
    </table>
  </td></tr>

  <!-- Footer -->
  <tr><td style="padding:0 32px 26px;">
    <p style="margin:0;font-size:11px;color:#999;line-height:1.6;">
      ${config.brokerage.name} · ${config.brokerage.address} · ${config.agent.phone}<br>
      Estimate generated ${formatDate(data.generatedAt)} from public records and recent comparable sales.
      Automated estimates can miss condition and upgrades — treat this as a starting point, not an appraisal.<br>
      Don't want these updates? Just reply "stop" and I'll take you off the list.
    </p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>`;
}

/** Internal alert so the agent can follow up while the number is still fresh. */
export function buildAgentEquityAlertHTML(sub, data, deltas) {
  return `
<h2 style="color:#c03926;font-family:Arial,sans-serif;">Home Value Tracker — notable movement</h2>
<table cellpadding="6" style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse;">
  <tr><td><b>Homeowner</b></td><td>${sub.name || '(no name)'} &lt;${sub.email}&gt;</td></tr>
  <tr><td><b>Property</b></td><td>${data.address}</td></tr>
  <tr><td><b>Value today</b></td><td><b>${formatCurrency(deltas.current)}</b></td></tr>
  <tr><td><b>Since last update</b></td><td style="color:${deltaColor(deltas.vsLast)};"><b>${formatDelta(deltas.vsLast)}</b></td></tr>
  <tr><td><b>Since enrolled</b></td><td>${formatDelta(deltas.vsEnrolled)}</td></tr>
  <tr><td><b>Since purchase</b></td><td>${deltas.vsPurchase ? formatDelta(deltas.vsPurchase) : 'unknown (no sale record)'}</td></tr>
  <tr><td><b>Enrolled</b></td><td>${formatDate(sub.enrolledAt)}</td></tr>
</table>
<p style="font-family:Arial,sans-serif;font-size:13px;color:#444;">
  Their equity moved enough to be worth a call. They just received this number by email.
</p>`;
}
