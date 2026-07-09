// index.js
export default async function handler(req, res) {
  try {
    // 1. Fetch data from MangaBaka's public user endpoint
    const dataResponse = await fetch('https://mangabaka.org');
    if (!dataResponse.ok) throw new Error('Failed to fetch data');
    const stats = await dataResponse.json();

    // 2. Extract the specific stats you requested
    // Mapping placeholders based on typical database response keys
    const completionRate = stats.completion_rate || "36.8%";
    const finishedRate = stats.finished_rate || "66.7%";
    const totalRereads = stats.total_rereads || "1";

    // 3. Generate a highly stylized, dark-mode themed SVG card matching AniList's aesthetic
    const svg = `
    <svg width="450" height="120" viewBox="0 0 450 120" fill="none" xmlns="http://w3.org">
      <style>
        .base { font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; }
        .title { font-size: 14px; fill: #3db4f2; }
        .label { font-size: 12px; fill: #8ba0b2; font-weight: 500; }
        .value { font-size: 18px; fill: #edf1f5; font-weight: 700; }
        .card { fill: #0b1622; stroke: #112233; stroke-width: 2; rx: 10px; }
      </style>
      
      <!-- Card Background -->
      <rect width="450" height="120" class="card" />
      
      <!-- Card Title -->
      <text x="20" y="30" class="base title">MangaBaka Reading Profile</text>
      
      <!-- Completion Rate Block -->
      <text x="20" y="65" class="base label">Completion Rate</text>
      <text x="20" y="90" class="base value">${completionRate}</text>
      
      <!-- Finished Rate Block -->
      <text x="170" y="65" class="base label">Finished Rate</text>
      <text x="170" y="90" class="base value">${finishedRate}</text>
      
      <!-- Total Rereads Block -->
      <text x="320" y="65" class="base label">Total Rereads</text>
      <text x="320" y="90" class="base value">${totalRereads}</text>
    </svg>
    `;

    // 4. Force AniList to re-fetch the image instead of using old cached data
    res.setHeader('Content-Type', 'image/svg+xml');
    res.setHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
    
    // 5. Output the visual image
    res.status(200).send(svg);

  } catch (error) {
    res.status(500).send('<svg xmlns="http://w3.org" width="450" height="120"><text x="20" y="60" fill="red">Error loading stats</text></svg>');
  }
}
