export default async function handler(req, res) {
    // Default fallback values
    let stats = {
        completionRate: "36.8%",
        finishedRate: "66.7%",
        totalRereads: "1",
        totalManga: "0",
        totalChapters: "0",
        totalVolumes: "0",
        meanScore: "0",
        daysRead: "0"
    };

    try {
        const token = process.env.MANGABAKA_TOKEN;
        
        if (!token) {
            console.warn('MANGABAKA_TOKEN environment variable not set. Using fallback values.');
        } else {
            const url = 'https://mangabaka.org/api/v1/user/stats';
            
            const dataResponse = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (dataResponse.ok) {
                const data = await dataResponse.json();
                
                // Map API response to our stats object
                if (data.completion_rate !== undefined) stats.completionRate = `${data.completion_rate}%`;
                else if (data.completionRate !== undefined) stats.completionRate = `${data.completionRate}%`;
                
                if (data.finished_rate !== undefined) stats.finishedRate = `${data.finished_rate}%`;
                else if (data.finishedRate !== undefined) stats.finishedRate = `${data.finishedRate}%`;
                
                if (data.total_rereads !== undefined) stats.totalRereads = String(data.total_rereads);
                else if (data.totalRereads !== undefined) stats.totalRereads = String(data.totalRereads);
                
                if (data.total_manga !== undefined) stats.totalManga = String(data.total_manga);
                else if (data.totalManga !== undefined) stats.totalManga = String(data.totalManga);
                
                if (data.total_chapters !== undefined) stats.totalChapters = String(data.total_chapters);
                else if (data.totalChapters !== undefined) stats.totalChapters = String(data.totalChapters);
                
                if (data.total_volumes !== undefined) stats.totalVolumes = String(data.total_volumes);
                else if (data.totalVolumes !== undefined) stats.totalVolumes = String(data.totalVolumes);
                
                if (data.mean_score !== undefined) stats.meanScore = String(data.mean_score);
                else if (data.meanScore !== undefined) stats.meanScore = String(data.meanScore);
                
                if (data.days_read !== undefined) stats.daysRead = String(data.days_read);
                else if (data.daysRead !== undefined) stats.daysRead = String(data.daysRead);
            } else {
                console.warn(`Mangabaka API returned status ${dataResponse.status}. Using fallback values.`);
            }
        }
    } catch (error) {
        console.error('Error fetching Mangabaka stats:', error.message);
    }

    // Parse percentage values for progress bars
    const completionNum = parseFloat(stats.completionRate) || 0;
    const finishedNum = parseFloat(stats.finishedRate) || 0;

    // Generate the high-quality visual SVG banner
    const svg = `
    <svg xmlns="http://www.w3.org/2000/2000" width="600" height="280" viewBox="0 0 600 280">
        <defs>
            <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#1e293b;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#3db4f2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.3"/>
            </filter>
        </defs>
        
        <!-- Background -->
        <rect width="100%" height="100%" fill="url(#bgGradient)" rx="16" />
        
        <!-- Accent line at top -->
        <rect x="0" y="0" width="600" height="4" fill="url(#accentGradient)" rx="16" />
        
        <!-- Title Section -->
        <text x="30" y="40" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="20" font-weight="700" fill="#f1f5f9">MangaBaka Reading Profile</text>
        <text x="30" y="60" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="12" fill="#64748b">Your personal manga statistics</text>
        
        <!-- Divider -->
        <line x1="30" y1="75" x2="570" y2="75" stroke="#334155" stroke-width="1" />
        
        <!-- Stats Grid - Row 1 -->
        <!-- Completion Rate -->
        <text x="30" y="105" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">COMPLETION RATE</text>
        <text x="30" y="130" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.completionRate}</text>
        <rect x="30" y="140" width="120" height="6" fill="#1e293b" rx="3" />
        <rect x="30" y="140" width="${Math.min(completionNum * 1.2, 120)}" height="6" fill="url(#accentGradient)" rx="3" />
        
        <!-- Finished Rate -->
        <text x="200" y="105" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">FINISHED RATE</text>
        <text x="200" y="130" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.finishedRate}</text>
        <rect x="200" y="140" width="120" height="6" fill="#1e293b" rx="3" />
        <rect x="200" y="140" width="${Math.min(finishedNum * 1.2, 120)}" height="6" fill="url(#accentGradient)" rx="3" />
        
        <!-- Mean Score -->
        <text x="370" y="105" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">MEAN SCORE</text>
        <text x="370" y="130" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.meanScore}</text>
        <text x="370" y="150" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="10" fill="#64748b">/ 10</text>
        
        <!-- Days Read -->
        <text x="500" y="105" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">DAYS READ</text>
        <text x="500" y="130" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.daysRead}</text>
        
        <!-- Divider -->
        <line x1="30" y1="170" x2="570" y2="170" stroke="#334155" stroke-width="1" />
        
        <!-- Stats Grid - Row 2 -->
        <!-- Total Manga -->
        <text x="30" y="200" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">TOTAL MANGA</text>
        <text x="30" y="225" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.totalManga}</text>
        
        <!-- Total Chapters -->
        <text x="160" y="200" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">CHAPTERS READ</text>
        <text x="160" y="225" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.totalChapters}</text>
        
        <!-- Total Volumes -->
        <text x="310" y="200" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">VOLUMES READ</text>
        <text x="310" y="225" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.totalVolumes}</text>
        
        <!-- Total Rereads -->
        <text x="460" y="200" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">REREADS</text>
        <text x="460" y="225" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="22" font-weight="700" fill="#f1f5f9">${stats.totalRereads}</text>
        
        <!-- Footer -->
        <text x="30" y="265" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="10" fill="#475569">Powered by MangaBaka API</text>
    </svg>
    `;

    // Serve the visual graphic directly to the browser or profile page
    res.setHeader('Content-Type', 'image/svg+xml');
    res.setHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.status(200).send(svg);
}
