import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

function loadEnv() {
  try {
    const envPath = resolve(__dirname, '..', '.env');
    const content = readFileSync(envPath, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIndex = trimmed.indexOf('=');
      if (eqIndex === -1) continue;
      const key = trimmed.slice(0, eqIndex).trim();
      const value = trimmed.slice(eqIndex + 1).trim();
      if (!process.env[key]) process.env[key] = value;
    }
  } catch {}
}

loadEnv();

export const config = {
  rentcast: {
    apiKey: process.env.RENTCAST_API_KEY,
    baseUrl: 'https://api.rentcast.io/v1',
  },
  agent: {
    name: process.env.AGENT_NAME || 'Daniel Cope',
    title: process.env.AGENT_TITLE || 'Real Estate Broker',
    phone: process.env.AGENT_PHONE || '317-201-6323',
    email: process.env.AGENT_EMAIL || 'csirealtyteam@yourrealtylink.com',
  },
  brokerage: {
    name: process.env.BROKERAGE_NAME || 'Your Realty Link',
    phone: process.env.BROKERAGE_PHONE || '317-997-7404',
    address: process.env.BROKERAGE_ADDRESS || '2302 E Southport Rd, Indianapolis, IN 46227',
    website: process.env.BROKERAGE_WEBSITE || 'https://yourrealtylink.com',
    logo: 'https://Agent3000.com/admin/upload/logos/MIBOR/MBR1322.png',
  },
  email: {
    resendKey: process.env.RESEND_API_KEY,
    smtpHost: process.env.SMTP_HOST,
    smtpPort: parseInt(process.env.SMTP_PORT || '587'),
    smtpUser: process.env.SMTP_USER,
    smtpPass: process.env.SMTP_PASS,
  },
  server: {
    port: parseInt(process.env.PORT || '3100'),
    webhookSecret: process.env.WEBHOOK_SECRET,
  },
};
