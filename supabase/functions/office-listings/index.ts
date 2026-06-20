import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

const CACHE_TTL_MS = 4 * 60 * 60 * 1000; // 4 hours
let cachedData: { listings: Listing[]; fetchedAt: number } | null = null;

interface Listing {
  mlsNumber: string;
  price: string;
  bedsBaths: string;
  sqft: string;
  acres: string | null;
  city: string;
  image: string;
  detailUrl: string;
}

function parseListings(html: string): Listing[] {
  const listings: Listing[] = [];

  const cardPattern = /data-id="(\d+)"[\s\S]*?data-src="([^"]+)"[\s\S]*?<em[^>]*>([^<]+)<\/em>[\s\S]*?<ul>([\s\S]*?)<\/ul>/g;
  let match;

  while ((match = cardPattern.exec(html)) !== null) {
    const mlsNumber = match[1];
    const image = match[2].replace(/\\\//g, "/");
    const city = match[3].trim();
    const detailsHtml = match[4];

    const priceMatch = detailsHtml.match(/Price:<\/strong>\s*(\$[\d,]+)/);
    const bbMatch = detailsHtml.match(/Beds\/Baths:<\/strong>\s*([\d\s\/]+)/);
    const sqftMatch = detailsHtml.match(/Sq\. Feet:<\/strong>\s*([\d,]+)/);
    const acresMatch = detailsHtml.match(/Acres:<\/strong>\s*([\d.]+)/);

    if (mlsNumber && priceMatch) {
      listings.push({
        mlsNumber,
        price: priceMatch[1],
        bedsBaths: bbMatch ? bbMatch[1].trim() : "",
        sqft: sqftMatch ? sqftMatch[1].trim() : "",
        acres: acresMatch ? acresMatch[1].trim() : null,
        city,
        image,
        detailUrl: `https://yourrealtylink.com/listing/${mlsNumber}`,
      });
    }
  }

  return listings;
}

serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  try {
    if (cachedData && Date.now() - cachedData.fetchedAt < CACHE_TTL_MS) {
      return new Response(
        JSON.stringify({
          listings: cachedData.listings,
          cached: true,
          fetchedAt: new Date(cachedData.fetchedAt).toISOString(),
          count: cachedData.listings.length,
        }),
        { status: 200, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const response = await fetch(
      "https://yourrealtylink.com/template5/templates/blocks/featuredListings.php",
      {
        method: "POST",
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; IndyPropertyGuide/1.0)",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "id=MBR1322",
      }
    );

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const json = await response.json();
    const listings = parseListings(json.RESP || "");

    cachedData = { listings, fetchedAt: Date.now() };

    return new Response(
      JSON.stringify({
        listings,
        cached: false,
        fetchedAt: new Date().toISOString(),
        count: listings.length,
      }),
      { status: 200, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
    );
  } catch (error) {
    const fallback = cachedData ? cachedData.listings : [];
    return new Response(
      JSON.stringify({ error: error.message, listings: fallback, count: fallback.length }),
      { status: 500, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
    );
  }
});
