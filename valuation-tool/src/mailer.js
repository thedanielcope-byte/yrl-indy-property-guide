import { createTransport } from 'nodemailer';
import { config } from './config.js';

let transporter = null;

function getTransporter() {
  if (transporter) return transporter;

  if (config.email.resendKey) {
    transporter = createTransport({
      host: 'smtp.resend.com',
      port: 465,
      secure: true,
      auth: { user: 'resend', pass: config.email.resendKey },
    });
  } else if (config.email.smtpHost) {
    transporter = createTransport({
      host: config.email.smtpHost,
      port: config.email.smtpPort,
      secure: config.email.smtpPort === 465,
      auth: { user: config.email.smtpUser, pass: config.email.smtpPass },
    });
  } else {
    return null;
  }

  return transporter;
}

export async function sendEmail({ to, subject, html, attachments }) {
  const t = getTransporter();
  if (!t) {
    console.log('  [EMAIL] No email service configured — skipping send.');
    console.log(`  [EMAIL] Would have sent to: ${to}`);
    console.log(`  [EMAIL] Subject: ${subject}`);
    return null;
  }

  const from = config.email.resendKey
    ? `${config.agent.name} <onboarding@resend.dev>`
    : `${config.agent.name} <${config.agent.email}>`;

  const result = await t.sendMail({ from, to, subject, html, attachments });
  console.log(`  [EMAIL] Sent to ${to}: ${result.messageId || 'OK'}`);
  return result;
}

export function isEmailConfigured() {
  return !!(config.email.resendKey || config.email.smtpHost);
}
