import { config } from './config.js';

function formatCurrency(n) {
  if (n == null) return 'N/A';
  return '$' + Math.round(n).toLocaleString('en-US');
}

function formatDate(d) {
  if (!d) return 'N/A';
  return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

export function buildEmailHTML(data) {
  const compsHTML = data.comparables.slice(0, 5).map(c => `
    <tr>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:13px;color:#1a1a1a;">${c.address || 'N/A'}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:13px;font-weight:bold;color:#c03926;">${formatCurrency(c.price)}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:12px;color:#6e6e70;">
        ${[c.bedrooms ? `${c.bedrooms}bd` : '', c.bathrooms ? `${c.bathrooms}ba` : '', c.squareFootage ? `${c.squareFootage.toLocaleString()}sf` : ''].filter(Boolean).join(' / ')}
      </td>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:12px;color:#6e6e70;">${formatDate(c.saleDate)}</td>
    </tr>
  `).join('');

  return `
<!DOCTYPE html>
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
        <h1 style="margin:0;color:#ffffff;font-size:22px;">Property Valuation Report</h1>
        <p style="margin:4px 0 0;color:rgba(255,255,255,0.85);font-size:12px;">Prepared by ${config.agent.name}, ${config.agent.title} — ${config.brokerage.name}</p>
      </td>
    </tr></table>
  </td></tr>

  <!-- Address -->
  <tr><td style="padding:28px 32px 0;">
    <p style="margin:0;font-size:18px;font-weight:bold;color:#1a1a1a;">${data.addressLine1}</p>
    <p style="margin:4px 0 0;font-size:14px;color:#6e6e70;">${data.city}, ${data.state} ${data.zipCode}</p>
    <p style="margin:4px 0 0;font-size:11px;color:#999;">Report generated ${formatDate(data.generatedAt)}</p>
  </td></tr>

  <!-- Value Estimate -->
  <tr><td style="padding:20px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f7f7f7;border-left:4px solid #c03926;border-radius:4px;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#6e6e70;">Estimated Market Value</p>
        ${data.estimate
          ? `<p style="margin:6px 0 0;font-size:32px;font-weight:bold;color:#1a1a1a;">${formatCurrency(data.estimate)}</p>
             <p style="margin:6px 0 0;font-size:13px;color:#6e6e70;">Range: ${formatCurrency(data.rangeLow)} — ${formatCurrency(data.rangeHigh)}</p>`
          : `<p style="margin:6px 0 0;font-size:16px;font-weight:bold;color:#1a1a1a;">Contact us for a personalized valuation</p>`
        }
      </td></tr>
    </table>
  </td></tr>

  <!-- Property Details -->
  <tr><td style="padding:0 32px 20px;">
    <h2 style="margin:0 0 12px;font-size:16px;color:#c03926;border-bottom:1px solid #c03926;padding-bottom:8px;">Property Details</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td width="50%" style="padding:6px 0;font-size:12px;color:#6e6e70;">Bedrooms</td>
        <td width="50%" style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${data.bedrooms || 'N/A'}</td>
      </tr>
      <tr>
        <td style="padding:6px 0;font-size:12px;color:#6e6e70;">Bathrooms</td>
        <td style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${data.bathrooms || 'N/A'}</td>
      </tr>
      <tr>
        <td style="padding:6px 0;font-size:12px;color:#6e6e70;">Square Feet</td>
        <td style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${data.squareFootage ? data.squareFootage.toLocaleString() : 'N/A'}</td>
      </tr>
      <tr>
        <td style="padding:6px 0;font-size:12px;color:#6e6e70;">Lot Size</td>
        <td style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${data.lotSize ? data.lotSize.toLocaleString() + ' sq ft' : 'N/A'}</td>
      </tr>
      <tr>
        <td style="padding:6px 0;font-size:12px;color:#6e6e70;">Year Built</td>
        <td style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${data.yearBuilt || 'N/A'}</td>
      </tr>
      <tr>
        <td style="padding:6px 0;font-size:12px;color:#6e6e70;">Property Type</td>
        <td style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${data.propertyType || 'N/A'}</td>
      </tr>
      <tr>
        <td style="padding:6px 0;font-size:12px;color:#6e6e70;">Last Sale Price</td>
        <td style="padding:6px 0;font-size:13px;font-weight:bold;color:#1a1a1a;">${formatCurrency(data.lastSalePrice)}</td>
      </tr>
    </table>
  </td></tr>

  ${data.comparables.length > 0 ? `
  <!-- Comparable Sales -->
  <tr><td style="padding:0 32px 20px;">
    <h2 style="margin:0 0 12px;font-size:16px;color:#c03926;border-bottom:1px solid #c03926;padding-bottom:8px;">Comparable Sales</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr style="background:#f7f7f7;">
        <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6e6e70;text-transform:uppercase;">Address</th>
        <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6e6e70;text-transform:uppercase;">Price</th>
        <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6e6e70;text-transform:uppercase;">Details</th>
        <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6e6e70;text-transform:uppercase;">Sold</th>
      </tr>
      ${compsHTML}
    </table>
  </td></tr>
  ` : ''}

  <!-- CTA -->
  <tr><td style="padding:10px 32px 24px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#c03926;border-radius:6px;">
      <tr><td style="padding:24px 28px;text-align:center;">
        <p style="margin:0 0 6px;color:#ffffff;font-size:16px;font-weight:bold;">Want a More Accurate Valuation?</p>
        <p style="margin:0 0 16px;color:rgba(255,255,255,0.85);font-size:13px;">This estimate is based on public data. A personalized Comparative Market Analysis (CMA) from your local expert considers condition, upgrades, and current market activity.</p>
        <a href="https://yourrealtylink.com/contact" style="display:inline-block;background:#ffffff;color:#c03926;font-weight:bold;font-size:14px;padding:12px 28px;border-radius:4px;text-decoration:none;">Request a Free CMA</a>
      </td></tr>
    </table>
  </td></tr>

  <!-- Agent -->
  <tr><td style="padding:0 32px 24px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td width="70" style="padding:16px 16px 16px 0;border-top:1px solid #eee;vertical-align:middle;">
          <img src="${config.brokerage.logo}" alt="${config.brokerage.name}" width="60" style="display:block;">
        </td>
        <td style="padding:16px 0;border-top:1px solid #eee;vertical-align:middle;">
          <p style="margin:0;font-size:15px;font-weight:bold;color:#1a1a1a;">${config.agent.name}, ${config.agent.title}</p>
          <p style="margin:4px 0 0;font-size:13px;color:#6e6e70;">${config.brokerage.name}</p>
          <p style="margin:4px 0 0;font-size:13px;color:#6e6e70;">${config.agent.phone} | ${config.agent.email}</p>
          <p style="margin:4px 0 0;font-size:12px;"><a href="${config.brokerage.website}" style="color:#c03926;">${config.brokerage.website}</a></p>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- Disclaimer -->
  <tr><td style="padding:16px 32px;background:#f7f7f7;border-top:1px solid #eee;">
    <p style="margin:0;font-size:9px;color:#999;line-height:1.4;">
      DISCLAIMER: This valuation report is an estimate based on publicly available data and comparable sales.
      It is not a formal appraisal and should not be used as such. Actual market value may vary based on property
      condition, improvements, market conditions, and other factors. For an accurate assessment, contact us for a
      personalized Comparative Market Analysis (CMA). ${config.brokerage.name}, ${config.brokerage.address}.
    </p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>`;
}

export function buildAgentNotificationHTML(data, homeownerEmail) {
  return `
<h2 style="color:#c03926;">New Valuation Request</h2>
<p><strong>Property:</strong> ${data.address}</p>
<p><strong>Homeowner Email:</strong> ${homeownerEmail}</p>
<p><strong>Estimated Value:</strong> ${data.estimate ? formatCurrency(data.estimate) : 'Not available'}</p>
<p><strong>Range:</strong> ${formatCurrency(data.rangeLow)} — ${formatCurrency(data.rangeHigh)}</p>
<p><strong>Details:</strong> ${data.bedrooms || '?'} bed / ${data.bathrooms || '?'} bath / ${data.squareFootage ? data.squareFootage.toLocaleString() + ' sqft' : '?'}</p>
<p><strong>Year Built:</strong> ${data.yearBuilt || 'N/A'}</p>
<p><strong>Last Sale:</strong> ${formatCurrency(data.lastSalePrice)} on ${formatDate(data.lastSaleDate)}</p>
<hr>
<p>The homeowner has been sent their valuation report. Follow up to offer a personalized CMA.</p>`;
}
