export default async function handler(req, res) {
  // Define your exact values right here as a guaranteed backup!
  let completionRate = "36.8%";
  let finishedRate = "66.7%";
  let totalRereads = "1";

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

    if (dataResponse.ok) {
        const stats = await dataResponse.json();
        
        // If the API gives a valid response, dynamically overwrite the values
        let rawCompletion = stats.completion_rate !== undefined ? stats.completion_rate : stats.completionRate;
        let rawFinished = stats.finished_rate !== undefined ? stats.finished_rate : stats.finishedRate;
        let rawRereads = stats.total_rereads !== undefined ? stats.total_rereads : stats.totalRereads;

        if (rawCompletion !== undefined) completionRate = `${rawCompletion}%`;
        if (rawFinished !== undefined) finishedRate = `${rawFinished}%`;
        if (rawRereads !== undefined) totalRereads = rawRereads;
    }
  } catch (error) {
      // Network failures or empty API responses are quietly skipped 
      // The script safely defaults to your specific profile stats below
  }

  // Generate the high-quality visual SVG banner 
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

  // Serve the visual graphic directly to the browser or profile page
  res.setHeader('Content-Type', 'image/svg+xml');
  res.setHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
  res.status(200).send(svg);
}
