export default async function handler(req, res) {
  try {
    const url = 'https://mangabaka.org';
    const token = 'mb-RNjmCUpjzyPWoMSUGIjeDzNunzIIidQGOvaEgQewhyPpgiKOfbRVcDHrmDfcjquY';

    const dataResponse = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });

    if (!dataResponse.ok) throw new Error('MangaBaka API denied access');
    const stats = await dataResponse.json();

    // Direct mapping checks for both common variations
    let rawCompletion = stats.completion_rate !== undefined ? stats.completion_rate : stats.completionRate;
    let rawFinished = stats.finished_rate !== undefined ? stats.finished_rate : stats.finishedRate;
    let rawRereads = stats.total_rereads !== undefined ? stats.total_rereads : stats.totalRereads;

    // Apply values or fall back to your profile defaults
    const completionRate = rawCompletion !== undefined ? `${rawCompletion}%` : "36.8%";
    const finishedRate = rawFinished !== undefined ? `${rawFinished}%` : "66.7%";
    const totalRereads = rawRereads !== undefined ? rawRereads : "1";

    const svg = `
    <svg width="450" height="120" viewBox="0 0 450 120" fill="none" xmlns="http://w3.org">
      <style>
        .base { font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; }
        .title { font-size: 14px; fill: #3db4f2; }
        .label { font-size: 12px; fill: #8ba0b2; font-weight: 500; }
        .value { font-size: 18px; fill: #edf1f5; font-weight: 700; }
        .card { fill: #0b1622; stroke: #112233; stroke-width: 2; rx: 10px; }
      </style>
      <rect width="450" height="120" class="card" />
      <text x="20" y="30" class="base title">MangaBaka Reading Profile</text>
      
      <text x="20" y="65" class="base label">Completion Rate</text>
      <text x="20" y="90" class="base value">${completionRate}</text>
      
      <text x="170" y="65" class="base label">Finished Rate</text>
      <text x="170" y="90" class="base value">${finishedRate}</text>
      
      <text x="320" y="65" class="base label">Total Rereads</text>
      <text x="320" y="90" class="base value">${totalRereads}</text>
    </svg>
    `;

    res.setHeader('Content-Type', 'image/svg+xml');
    res.setHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
    res.status(200).send(svg);

  } catch (error) {
    // Fixed string interpretation error layout
    res.setHeader('Content-Type', 'image/svg+xml');
    res.status(200).send('<svg xmlns="http://w3.org" width="450" height="120"><rect width="450" height="120" fill="#0b1622" rx="10"/><text x="20" y="65" fill="#ff4d4d" font-family="sans-serif" font-weight="bold">Processing Error</text></svg>');
  }
}
