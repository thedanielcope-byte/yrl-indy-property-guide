import express from 'express';
import { config } from './config.js';
import { runValuation } from './index.js';
import { getFullValuation } from './rentcast.js';
import { generatePDF } from './pdf-report.js';
import { buildEmailHTML, buildAgentNotificationHTML } from './email-report.js';
import { sendEmail, isEmailConfigured } from './mailer.js';
import { writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  res.header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

function formatCurrency(n) {
  if (n == null) return 'N/A';
  return '$' + Math.round(n).toLocaleString('en-US');
}

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'yrl-valuation' });
});

// Main valuation endpoint — accepts JSON or form-encoded
app.post('/api/valuation', async (req, res) => {
  try {
    const body = req.body;

    // Extract address — handles WPForms webhook format and direct JSON
    const address = body.address
      || body.property_address
      || body.field_address
      || (body.fields && (body.fields.address || body.fields.property_address))
      || null;

    const homeownerEmail = body.email
      || body.homeowner_email
      || body.field_email
      || (body.fields && (body.fields.email || body.fields.homeowner_email))
      || null;

    const homeownerName = body.name
      || body.homeowner_name
      || body.field_name
      || (body.fields && (body.fields.name || body.fields.homeowner_name))
      || null;

    if (!address) {
      return res.status(400).json({ error: 'Missing address field' });
    }

    console.log(`\n[${new Date().toISOString()}] Valuation request: ${address} (${homeownerEmail || 'no email'})`);

    const data = await getFullValuation(address);

    // Generate PDF
    const pdfBuffer = await generatePDF(data);
    const slug = data.addressLine1.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
    const date = new Date().toISOString().slice(0, 10);
    const filename = `valuation-${slug}-${date}.pdf`;
    const filepath = resolve(__dirname, '..', 'reports', filename);
    writeFileSync(filepath, pdfBuffer);

    // Save HTML
    const htmlContent = buildEmailHTML(data);
    writeFileSync(filepath.replace('.pdf', '.html'), htmlContent);

    // Send emails
    if (isEmailConfigured()) {
      if (homeownerEmail) {
        await sendEmail({
          to: homeownerEmail,
          subject: `Your Property Valuation Report — ${data.addressLine1}`,
          html: htmlContent,
          attachments: [{ filename, content: pdfBuffer, contentType: 'application/pdf' }],
        });
      }

      await sendEmail({
        to: config.agent.email,
        subject: `[LEAD] New Valuation: ${data.addressLine1} — ${formatCurrency(data.estimate)}`,
        html: buildAgentNotificationHTML(data, homeownerEmail || 'No email provided'),
        attachments: [{ filename, content: pdfBuffer, contentType: 'application/pdf' }],
      });
    }

    // Return results for on-page display
    res.json({
      success: true,
      address: data.address,
      estimate: data.estimate,
      rangeLow: data.rangeLow,
      rangeHigh: data.rangeHigh,
      bedrooms: data.bedrooms,
      bathrooms: data.bathrooms,
      squareFootage: data.squareFootage,
      yearBuilt: data.yearBuilt,
      propertyType: data.propertyType,
      comparables: data.comparables.length,
      comparableDetails: data.comparables,
      reportFile: filename,
    });

    console.log(`  Completed: ${formatCurrency(data.estimate)} (${data.comparables.length} comps)`);
  } catch (err) {
    console.error('  Error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// GHL / generic webhook format
app.post('/webhook/valuation', async (req, res) => {
  // Immediately respond 200 so the webhook doesn't timeout
  res.json({ received: true });

  try {
    const body = req.body;
    const address = body.address || body.property_address || body.customData?.address || null;
    const email = body.email || body.contact?.email || null;

    if (!address) {
      console.log('  Webhook received but no address found:', JSON.stringify(body).slice(0, 200));
      return;
    }

    console.log(`\n[WEBHOOK] ${address} (${email || 'no email'})`);

    const data = await getFullValuation(address);
    const pdfBuffer = await generatePDF(data);
    const slug = data.addressLine1.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
    const date = new Date().toISOString().slice(0, 10);
    const filename = `valuation-${slug}-${date}.pdf`;
    writeFileSync(resolve(__dirname, '..', 'reports', filename), pdfBuffer);
    writeFileSync(resolve(__dirname, '..', 'reports', filename.replace('.pdf', '.html')), buildEmailHTML(data));

    if (isEmailConfigured()) {
      if (email) {
        await sendEmail({
          to: email,
          subject: `Your Property Valuation Report — ${data.addressLine1}`,
          html: buildEmailHTML(data),
          attachments: [{ filename, content: pdfBuffer, contentType: 'application/pdf' }],
        });
      }
      await sendEmail({
        to: config.agent.email,
        subject: `[LEAD] New Valuation: ${data.addressLine1} — ${formatCurrency(data.estimate)}`,
        html: buildAgentNotificationHTML(data, email || 'No email'),
        attachments: [{ filename, content: pdfBuffer, contentType: 'application/pdf' }],
      });
    }

    console.log(`  [WEBHOOK] Done: ${formatCurrency(data.estimate)}`);
  } catch (err) {
    console.error('  [WEBHOOK] Error:', err.message);
  }
});

const PORT = config.server.port;
app.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════════╗
║  Your Realty Link — Valuation Server                 ║
╠══════════════════════════════════════════════════════╣
║  Port: ${String(PORT).padEnd(46)}║
║  API:  POST /api/valuation                           ║
║  Hook: POST /webhook/valuation                       ║
║  Email: ${isEmailConfigured() ? 'Configured ✓'.padEnd(45) : 'Not configured (set .env)'.padEnd(45)}║
╚══════════════════════════════════════════════════════╝
  `);
});
