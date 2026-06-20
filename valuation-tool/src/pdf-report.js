import PDFDocument from 'pdfkit';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from './config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const logoPath = resolve(__dirname, 'logo.png');

const COLORS = {
  red: '#c03926',
  dark: '#1a1a1a',
  gray: '#6e6e70',
  lightBg: '#f7f7f7',
  white: '#ffffff',
};

function formatCurrency(n) {
  if (n == null) return 'N/A';
  return '$' + Math.round(n).toLocaleString('en-US');
}

function formatDate(d) {
  if (!d) return 'N/A';
  return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

export function generatePDF(data) {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({ size: 'LETTER', margin: 50 });
    const chunks = [];
    doc.on('data', c => chunks.push(c));
    doc.on('end', () => resolve(Buffer.concat(chunks)));
    doc.on('error', reject);

    const W = doc.page.width - 100;

    // --- HEADER with logo ---
    doc.rect(0, 0, doc.page.width, 100).fill(COLORS.red);

    try {
      doc.image(logoPath, 50, 12, { height: 75 });
    } catch {}

    doc.fill(COLORS.white).fontSize(20).font('Helvetica-Bold')
      .text('Property Valuation Report', 200, 25, { width: W - 150 });
    doc.fontSize(11).font('Helvetica')
      .text(`Prepared by ${config.brokerage.name}`, 200, 52, { width: W - 150 });
    doc.fontSize(9).font('Helvetica')
      .text(`${config.agent.name}, ${config.agent.title}  |  ${config.agent.phone}`, 200, 70, { width: W - 150 });

    // --- DATE + ADDRESS ---
    doc.fill(COLORS.dark).fontSize(10).font('Helvetica')
      .text(`Report Date: ${formatDate(data.generatedAt)}`, 50, 115, { width: W, align: 'right' });

    doc.fontSize(16).font('Helvetica-Bold').fill(COLORS.dark)
      .text(data.addressLine1, 50, 130);
    doc.fontSize(12).font('Helvetica').fill(COLORS.gray)
      .text(`${data.city}, ${data.state} ${data.zipCode}${data.county ? '  |  ' + data.county + ' County' : ''}`, 50, 152);

    // --- ESTIMATED VALUE BOX ---
    const valueY = 180;
    doc.rect(50, valueY, W, 80).fill(COLORS.lightBg);
    doc.rect(50, valueY, 4, 80).fill(COLORS.red);

    doc.fill(COLORS.gray).fontSize(11).font('Helvetica')
      .text('ESTIMATED MARKET VALUE', 70, valueY + 12);

    if (data.estimate) {
      doc.fill(COLORS.dark).fontSize(28).font('Helvetica-Bold')
        .text(formatCurrency(data.estimate), 70, valueY + 30);
      doc.fill(COLORS.gray).fontSize(11).font('Helvetica')
        .text(`Range: ${formatCurrency(data.rangeLow)} — ${formatCurrency(data.rangeHigh)}`, 70, valueY + 60);
    } else {
      doc.fill(COLORS.dark).fontSize(16).font('Helvetica-Bold')
        .text('Contact us for a personalized valuation', 70, valueY + 35);
    }

    // --- PROPERTY DETAILS ---
    const detailY = valueY + 100;
    doc.fill(COLORS.red).fontSize(14).font('Helvetica-Bold')
      .text('Property Details', 50, detailY);
    doc.moveTo(50, detailY + 18).lineTo(50 + W, detailY + 18).strokeColor(COLORS.red).lineWidth(1).stroke();

    const details = [
      ['Bedrooms', data.bedrooms || 'N/A'],
      ['Bathrooms', data.bathrooms || 'N/A'],
      ['Square Feet', data.squareFootage ? data.squareFootage.toLocaleString() : 'N/A'],
      ['Lot Size (sq ft)', data.lotSize ? data.lotSize.toLocaleString() : 'N/A'],
      ['Year Built', data.yearBuilt || 'N/A'],
      ['Property Type', data.propertyType || 'N/A'],
      ['Last Sale Date', formatDate(data.lastSaleDate)],
      ['Last Sale Price', formatCurrency(data.lastSalePrice)],
    ];

    let dy = detailY + 28;
    const colW = W / 2;
    for (let i = 0; i < details.length; i++) {
      const x = i % 2 === 0 ? 50 : 50 + colW;
      const y = dy + Math.floor(i / 2) * 22;
      doc.fill(COLORS.gray).fontSize(9).font('Helvetica').text(details[i][0], x, y, { width: 120 });
      doc.fill(COLORS.dark).fontSize(10).font('Helvetica-Bold').text(String(details[i][1]), x + 120, y, { width: 140 });
    }

    // --- COMPARABLE SALES ---
    if (data.comparables.length > 0) {
      const compY = dy + Math.ceil(details.length / 2) * 22 + 25;
      doc.fill(COLORS.red).fontSize(14).font('Helvetica-Bold')
        .text('Comparable Sales', 50, compY);
      doc.moveTo(50, compY + 18).lineTo(50 + W, compY + 18).strokeColor(COLORS.red).lineWidth(1).stroke();

      let cy = compY + 28;
      for (const comp of data.comparables.slice(0, 5)) {
        if (cy > 640) {
          doc.addPage();
          cy = 50;
        }

        doc.rect(50, cy, W, 55).fill(COLORS.lightBg);
        doc.fill(COLORS.dark).fontSize(10).font('Helvetica-Bold')
          .text(comp.address || 'N/A', 60, cy + 8, { width: W - 160 });
        doc.fill(COLORS.red).fontSize(12).font('Helvetica-Bold')
          .text(formatCurrency(comp.price), 50 + W - 140, cy + 6, { width: 130, align: 'right' });

        const meta = [
          comp.bedrooms ? `${comp.bedrooms} bed` : null,
          comp.bathrooms ? `${comp.bathrooms} bath` : null,
          comp.squareFootage ? `${comp.squareFootage.toLocaleString()} sqft` : null,
          comp.yearBuilt ? `Built ${comp.yearBuilt}` : null,
          comp.status || null,
          comp.daysOnMarket != null ? `${comp.daysOnMarket} DOM` : null,
          comp.distance != null ? `${comp.distance.toFixed(2)} mi` : null,
        ].filter(Boolean).join('  |  ');

        doc.fill(COLORS.gray).fontSize(8).font('Helvetica')
          .text(meta, 60, cy + 28, { width: W - 20 });

        cy += 63;
      }
    }

    // --- DISCLAIMER + FOOTER ---
    const footY = doc.page.height - 170;

    doc.moveTo(50, footY).lineTo(50 + W, footY).strokeColor('#dddddd').lineWidth(0.5).stroke();

    doc.fill(COLORS.gray).fontSize(7).font('Helvetica')
      .text(
        'DISCLAIMER: This valuation report is an estimate based on publicly available data and comparable sales. ' +
        'It is not a formal appraisal and should not be used as such. Actual market value may vary based on property ' +
        'condition, improvements, market conditions, and other factors. For an accurate assessment, contact us for a ' +
        'personalized Comparative Market Analysis (CMA).',
        50, footY + 8, { width: W }
      );

    // Agent contact block
    const contactY = footY + 55;
    doc.rect(50, contactY, W, 75).fill(COLORS.red);

    try {
      doc.image(logoPath, 60, contactY + 8, { height: 58 });
    } catch {}

    const textX = 135;
    doc.fill(COLORS.white).fontSize(14).font('Helvetica-Bold')
      .text(`${config.agent.name}`, textX, contactY + 10, { width: W - 95 });
    doc.fill(COLORS.white).fontSize(10).font('Helvetica')
      .text(`${config.agent.title} — ${config.brokerage.name}`, textX, contactY + 28, { width: W - 95 });
    doc.fill(COLORS.white).fontSize(10).font('Helvetica')
      .text(`${config.agent.phone}  |  ${config.agent.email}`, textX, contactY + 44, { width: W - 95 });
    doc.fill(COLORS.white).fontSize(9).font('Helvetica')
      .text(config.brokerage.website, textX, contactY + 58, { width: W - 95 });

    doc.end();
  });
}
