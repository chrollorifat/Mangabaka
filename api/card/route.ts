import { fetchAllEntries, computeStats, generateSVG } from '@/lib/stats';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export async function GET() {
  const API_KEY = process.env.MANGABAKA_API_KEY || '';
  const BASE_URL = 'https://api.mangabaka.org';

  try {
    // Fetch profile for nickname
    const profileResp = await fetch(`${BASE_URL}/v1/my/profile`, {
      headers: { 'x-api-key': API_KEY },
      cache: 'no-store',
    });

    let nickname = 'User';
    if (profileResp.ok) {
      const profile = await profileResp.json();
      nickname = profile.data?.nickname || profile.data?.preferred_username || 'User';
    }

    // Fetch library entries and compute stats
    const entries = await fetchAllEntries(API_KEY, BASE_URL);
    const stats = computeStats(entries);

    // Generate SVG card
    const svg = generateSVG(stats, nickname);

    return new Response(svg, {
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'public, max-age=300, stale-while-revalidate=600',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    console.error('Error generating card:', error);
    return new Response('Error generating card', { status: 500 });
  }
}
