import { resolve, dirname } from 'path';
import { writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { getFullValuation } from './rentcast.js';
import { generatePDF } from './pdf-report.js';
import { buildEmailHTML, buildAgentNotificationHTML } from './email-report.js';
import { sendEmail, isEmailConfigured } from './mailer.js';
import { config } from './config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

function formatCurrency(n) {
  if (n == null) return 'N/A';
  return '$' + Math.round(n).toLocaleString('en-US');
}

export async function runValuation(address, homeownerEmail) {
  console.log('\n=== Your Realty Link — Property Valuation ===\n');
  console.log(`Address: ${address}`);
  if (homeownerEmail) console.log(`Homeowner: ${homeownerEmail}`);
  console.log('');

  const data = await getFullValuation(address);

  console.log('\n--- RESULTS ---');
  console.log(`Property:   ${data.address}`);
  console.log(`Estimate:   ${formatCurrency(data.estimate)}`);
  console.log(`Range:      ${formatCurrency(data.rangeLow)} — ${formatCurrency(data.rangeHigh)}`);
  console.log(`Beds/Bath:  ${data.bedrooms || '?'} / ${data.bathrooms || '?'}`);
  console.log(`Sq Ft:      ${data.squareFootage ? data.squareFootage.toLocaleString() : 'N/A'}`);
  console.log(`Year Built: ${data.yearBuilt || 'N/A'}`);
  console.log(`Last Sale:  ${formatCurrency(data.lastSalePrice)}`);
  console.log(`Comps:      ${data.comparables.length} found`);
  console.log('');

  // Generate PDF
  console.log('  Generating PDF report...');
  const pdfBuffer = await generatePDF(data);

  const slug = data.addressLine1.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
  const date = new Date().toISOString().slice(0, 10);
  const filename = `valuation-${slug}-${date}.pdf`;
  const filepath = resolve(__dirname, '..', 'reports', filename);
  writeFileSync(filepath, pdfBuffer);
  console.log(`  PDF saved: reports/${filename}`);

  // Send emails if configured
  if (isEmailConfigured()) {
    const emailHTML = buildEmailHTML(data);

    if (homeownerEmail) {
      console.log('  Sending report to homeowner...');
      await sendEmail({
        to: homeownerEmail,
        subject: `Your Property Valuation Report — ${data.addressLine1}`,
        html: emailHTML,
        attachments: [{ filename, content: pdfBuffer, contentType: 'application/pdf' }],
      });
    }

    console.log('  Sending notification to agent...');
    await sendEmail({
      to: config.agent.email,
      subject: `[LEAD] New Valuation: ${data.addressLine1} — ${formatCurrency(data.estimate)}`,
      html: buildAgentNotificationHTML(data, homeownerEmail || 'CLI run (no email)'),
      attachments: [{ filename, content: pdfBuffer, contentType: 'application/pdf' }],
    });
  } else {
    console.log('  Email not configured — report saved locally only.');
    console.log('  To enable email, set RESEND_API_KEY or SMTP_* in .env');
  }

  // Save HTML version too
  const htmlPath = resolve(__dirname, '..', 'reports', filename.replace('.pdf', '.html'));
  writeFileSync(htmlPath, buildEmailHTML(data));
  console.log(`  HTML saved: reports/${filename.replace('.pdf', '.html')}`);

  console.log('\n  Done!\n');
  return data;
}

// CLI mode
const args = process.argv.slice(2);
if (args.length > 0 && !args[0].startsWith('--server')) {
  const address = args[0];
  const email = args[1] || null;
  runValuation(address, email).catch(err => {
    console.error('\nError:', err.message);
    process.exit(1);
  });
} else if (args.length === 0) {
  console.log(`
╔══════════════════════════════════════════════════════╗
║  Your Realty Link — Property Valuation Tool          ║
╚══════════════════════════════════════════════════════╝

Usage:

  CLI Mode (run a single valuation):
    node src/index.js "123 Main St, Indianapolis, IN 46227"
    node src/index.js "123 Main St, Indianapolis, IN 46227" homeowner@email.com

  Server Mode (webhook listener for WPForms):
    node src/server.js

  The PDF and HTML reports are saved to the reports/ folder.
  Configure email in .env to auto-send reports.
`);
}
