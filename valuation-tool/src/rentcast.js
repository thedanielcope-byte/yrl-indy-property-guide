import { config } from './config.js';

const headers = {
  'Accept': 'application/json',
  'X-Api-Key': config.rentcast.apiKey,
};

async function apiGet(endpoint, params) {
  const url = new URL(`${config.rentcast.baseUrl}${endpoint}`);
  for (const [k, v] of Object.entries(params)) {
    if (v != null) url.searchParams.set(k, v);
  }
  const res = await fetch(url, { headers });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`RentCast ${endpoint} failed (${res.status}): ${body}`);
  }
  return res.json();
}

export async function getFullValuation(address) {
  console.log(`  Fetching property data for: ${address}`);

  const avm = await apiGet('/avm/value', { address });

  if (!avm || !avm.price) {
    throw new Error('Could not find property data. Please verify the address and try again.');
  }

  const subject = avm.subjectProperty || {};
  const comps = avm.comparables || [];

  return {
    address: subject.formattedAddress || address,
    addressLine1: subject.addressLine1 || address.split(',')[0],
    city: subject.city || '',
    state: subject.state || 'IN',
    zipCode: subject.zipCode || '',
    county: subject.county || '',

    estimate: avm.price,
    rangeLow: avm.priceRangeLow || Math.round(avm.price * 0.95),
    rangeHigh: avm.priceRangeHigh || Math.round(avm.price * 1.05),

    bedrooms: subject.bedrooms || null,
    bathrooms: subject.bathrooms || null,
    squareFootage: subject.squareFootage || null,
    lotSize: subject.lotSize || null,
    yearBuilt: subject.yearBuilt || null,
    propertyType: subject.propertyType || null,
    lastSaleDate: subject.lastSaleDate || null,
    lastSalePrice: subject.lastSalePrice || null,

    comparables: comps.slice(0, 5).map(c => ({
      address: c.formattedAddress || c.addressLine1,
      price: c.price,
      saleDate: c.listedDate || c.removedDate,
      bedrooms: c.bedrooms,
      bathrooms: c.bathrooms,
      squareFootage: c.squareFootage,
      lotSize: c.lotSize,
      yearBuilt: c.yearBuilt,
      distance: c.distance,
      daysOnMarket: c.daysOnMarket,
      status: c.status,
      propertyType: c.propertyType,
    })),

    generatedAt: new Date().toISOString(),
  };
}
