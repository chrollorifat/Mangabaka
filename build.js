// Build script to generate static SVG card for GitHub Pages deployment
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Configuration from environment variables
const API_KEY = process.env.MANGABAKA_API_KEY || '';
const BASE_URL = 'https://api.mangabaka.org';

/**
 * Fetch all library entries from MangaBaka API
 * @param {string} apiKey - MangaBaka API key
 * @returns {Promise<Array>} Array of library entries
 */
async function fetchAllEntries(apiKey) {
  const entries = [];
  let page = 1;

  while (true) {
    const resp = await fetch(`${BASE_URL}/v1/my/library?limit=100&page=${page}`, {
      headers: { 'x-api-key': apiKey },
    });

    if (!resp.ok) break;
    const data = await resp.json();
    const items = data.data || [];
    if (items.length === 0) break;

    entries.push(...items);

    const pagination = data.pagination || {};
    if (!pagination.next) break;
    page++;
    if (page > 10) break; // Limit to 1000 entries max
  }

  return entries;
}

/**
 * Compute statistics from library entries
 * @param {Array} entries - Library entries
 * @returns {Object} Statistics object
 */
function computeStats(entries) {
  const states = {};
  const ratings = [];
  let chapters = 0;
  let volumes = 0;
  let rereads = 0;
  const types = {};
  const content = {};
  const genres = {};
  const tags = {};

  for (const e of entries) {
    states[e.state] = (states[e.state] || 0) + 1;
    if (e.rating !== null) ratings.push(e.rating);
    if (e.progress_chapter) chapters += e.progress_chapter;
    if (e.progress_volume) volumes += e.progress_volume;
    rereads += e.number_of_rereads || 0;

    const s = e.Series || {};
    if (s.type) types[s.type] = (types[s.type] || 0) + 1;
    if (s.content_rating) content[s.content_rating] = (content[s.content_rating] || 0) + 1;
    for (const g of s.genres || []) genres[g] = (genres[g] || 0) + 1;
    for (const t of s.tags || []) tags[t] = (tags[t] || 0) + 1;
  }

  const avgRating = ratings.length > 0
    ? Math.round((ratings.reduce((a, b) => a + b, 0) / ratings.length) * 10) / 10
    : 0;

  const sortEntries = (obj) =>
    Object.entries(obj).sort((a, b) => b[1] - a[1]).slice(0, 5);

  return {
    total: entries.length,
    reading: states['reading'] || 0,
    completed: states['completed'] || 0,
    paused: states['paused'] || 0,
    dropped: states['dropped'] || 0,
    plan_to_read: states['plan_to_read'] || 0,
    rated: ratings.length,
    avgRating,
    chapters,
    volumes,
    rereads,
    manga: types['manga'] || 0,
    manhwa: types['manhwa'] || 0,
    manhua: types['manhua'] || 0,
    novel: types['novel'] || 0,
    safe: content['safe'] || 0,
    suggestive: content['suggestive'] || 0,
    erotica: content['erotica'] || 0,
    pornographic: content['pornographic'] || 0,
    topGenres: sortEntries(genres),
    topTags: sortEntries(tags),
  };
}

/**
 * Escape special XML characters
 * @param {string} str - Input string
 * @returns {string} Escaped string
 */
function escapeXml(str) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&apos;'
  };
  return str.replace(/[&<>"']/g, m => map[m]);
}

function generateSVG(stats, nickname) {
  const width = 850;
  const height = 420;

  const bar = (val, max, color) => {
    const pct = max > 0 ? (val / max) * 100 : 0;
    return `<rect x="0" y="0" width="${pct}" height="6" rx="3" fill="${color}"/>`;
  };

  const maxState = Math.max(stats.reading, stats.completed, stats.paused, stats.dropped, stats.plan_to_read, 1);
  const maxType = Math.max(stats.manga, stats.manhwa, stats.manhua, stats.novel, 1);

  const genreBars = stats.topGenres.map(([name, count], i) => {
    const maxG = stats.topGenres[0][1];
    const pct = (count / maxG) * 120;
    const colors = ['#FF6B9D', '#C44569', '#F8B500', '#4ECDC4', '#556270'];
    return `
      <text x="0" y="${i * 18}" fill="#a0a0b0" font-size="11" font-family="system-ui, sans-serif">${escapeXml(name)}</text>
      <rect x="80" y="${i * 18 - 8}" width="${pct}" height="6" rx="3" fill="${colors[i % colors.length]}" opacity="0.85"/>
      <text x="${85 + pct}" y="${i * 18}" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${count}</text>
    `;
  }).join('');


  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f0f1a"/>
      <stop offset="50%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6B9D"/>
      <stop offset="100%" stop-color="#C44569"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#ffffff" opacity="0.03"/>
    </pattern>
  </defs>

  <rect width="${width}" height="${height}" fill="url(#bg)" rx="12"/>
  <rect width="${width}" height="${height}" fill="url(#dots)" rx="12"/>
  <rect x="0" y="0" width="${width}" height="3" fill="url(#accent)" rx="1.5"/>

  <text x="30" y="45" fill="#ffffff" font-size="22" font-weight="700" font-family="system-ui, sans-serif" filter="url(#glow)">
    ${escapeXml(nickname)}'s MangaBaka Stats
  </text>
  <text x="30" y="65" fill="#FF6B9D" font-size="12" font-family="system-ui, sans-serif" opacity="0.8">
    Library Overview • Updated ${new Date().toLocaleDateString()}
  </text>

  <g transform="translate(30, 90)">
    <rect x="0" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="55" y="25" fill="#FF6B9D" font-size="24" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">${stats.total}</text>
    <text x="55" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" font-family="system-ui, sans-serif">Total Entries</text>

    <rect x="125" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="180" y="25" fill="#4ECDC4" font-size="24" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">${stats.chapters.toLocaleString()}</text>
    <text x="180" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" font-family="system-ui, sans-serif">Chapters Read</text>

    <rect x="250" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="305" y="25" fill="#F8B500" font-size="24" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">${stats.volumes}</text>
    <text x="305" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" font-family="system-ui, sans-serif">Volumes Read</text>

    <rect x="375" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="430" y="25" fill="#C44569" font-size="24" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">${stats.avgRating}</text>
    <text x="430" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" font-family="system-ui, sans-serif">Avg Rating (${stats.rated})</text>

    <rect x="500" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="555" y="25" fill="#A8E6CF" font-size="24" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">${stats.rereads}</text>
    <text x="555" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" font-family="system-ui, sans-serif">Rereads</text>
  </g>

  <g transform="translate(30, 185)">
    <text x="0" y="0" fill="#ffffff" font-size="13" font-weight="600" font-family="system-ui, sans-serif">Status Distribution</text>

    <g transform="translate(0, 15)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Reading</text>
      <g transform="translate(60, 6)"><rect width="140" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.reading, maxState, '#4ECDC4')}</g>
      <text x="210" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.reading}</text>
    </g>

    <g transform="translate(0, 35)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Completed</text>
      <g transform="translate(60, 6)"><rect width="140" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.completed, maxState, '#A8E6CF')}</g>
      <text x="210" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.completed}</text>
    </g>

    <g transform="translate(0, 55)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Paused</text>
      <g transform="translate(60, 6)"><rect width="140" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.paused, maxState, '#F8B500')}</g>
      <text x="210" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.paused}</text>
    </g>

    <g transform="translate(0, 75)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Dropped</text>
      <g transform="translate(60, 6)"><rect width="140" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.dropped, maxState, '#FF6B9D')}</g>
      <text x="210" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.dropped}</text>
    </g>

    <g transform="translate(0, 95)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Plan to Read</text>
      <g transform="translate(60, 6)"><rect width="140" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.plan_to_read, maxState, '#DCEDC1')}</g>
      <text x="210" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.plan_to_read}</text>
    </g>
  </g>

  <g transform="translate(280, 185)">
    <text x="0" y="0" fill="#ffffff" font-size="13" font-weight="600" font-family="system-ui, sans-serif">Media Types</text>

    <g transform="translate(0, 15)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Manga</text>
      <g transform="translate(60, 6)"><rect width="100" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.manga, maxType, '#FFAAA5')}</g>
      <text x="170" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.manga}</text>
    </g>

    <g transform="translate(0, 35)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Manhwa</text>
      <g transform="translate(60, 6)"><rect width="100" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.manhwa, maxType, '#A8E6CF')}</g>
      <text x="170" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.manhwa}</text>
    </g>

    <g transform="translate(0, 55)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Manhua</text>
      <g transform="translate(60, 6)"><rect width="100" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.manhua, maxType, '#FFD3B6')}</g>
      <text x="170" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.manhua}</text>
    </g>

    <g transform="translate(0, 75)">
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">Novel</text>
      <g transform="translate(60, 6)"><rect width="100" height="6" rx="3" fill="#ffffff" opacity="0.08"/>${bar(stats.novel, maxType, '#DCEDC1')}</g>
      <text x="170" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">${stats.novel}</text>
    </g>
  </g>

  <g transform="translate(500, 185)">
    <text x="0" y="0" fill="#ffffff" font-size="13" font-weight="600" font-family="system-ui, sans-serif">Top Genres</text>
    <g transform="translate(0, 18)">
      ${genreBars}
    </g>
  </g>



  <text x="${width - 30}" y="${height - 15}" fill="#555570" font-size="10" text-anchor="end" font-family="system-ui, sans-serif">
    mangabaka.org • Generated dynamically
  </text>

  <text x="30" y="${height - 15}" fill="#FF6B9D" font-size="10" font-weight="600" font-family="system-ui, sans-serif" opacity="0.6">
    マンガバカ
  </text>
</svg>`;
}

async function main() {
  if (!API_KEY) {
    console.error('Error: MANGABAKA_API_KEY environment variable is not set');
    console.error('Please set it in your GitHub repository secrets');
    process.exit(1);
  }

  try {
    console.log('Fetching profile...');
    const profileResp = await fetch(`${BASE_URL}/v1/my/profile`, {
      headers: { 'x-api-key': API_KEY },
    });

    let nickname = 'User';
    if (profileResp.ok) {
      const profile = await profileResp.json();
      nickname = profile.data?.nickname || profile.data?.preferred_username || 'User';
    }

    console.log('Fetching library entries...');
    const entries = await fetchAllEntries(API_KEY);
    console.log(`Found ${entries.length} entries`);

    console.log('Computing statistics...');
    const stats = computeStats(entries);

    console.log('Generating SVG card...');
    const svg = generateSVG(stats, nickname);

    // Create output directory
    const outDir = join(__dirname, 'dist');
    if (!existsSync(outDir)) {
      mkdirSync(outDir, { recursive: true });
    }

    // Write SVG file
    const outputPath = join(outDir, 'card.svg');
    writeFileSync(outputPath, svg, 'utf-8');
    console.log(`Card generated successfully: ${outputPath}`);

    // Also copy to root for easy access
    const rootOutputPath = join(__dirname, 'card.svg');
    writeFileSync(rootOutputPath, svg, 'utf-8');
    console.log(`Card also copied to: ${rootOutputPath}`);

  } catch (error) {
    console.error('Error generating card:', error);
    process.exit(1);
  }
}

main();
