"""
SVG Generator Module for MangaBaka Stats Card.

Generates a modern, responsive SVG dashboard with:
- Dynamic height calculation to prevent element overlap
- Modern "Midnight Aurora" color theme
- Comprehensive statistics display
- Activity heatmap (last 7 days)
- Genre distribution and reading status breakdowns

Design Principles:
1. **Responsive**: Uses viewBox for perfect scaling on any screen
2. **No Overlaps**: Careful Y-coordinate spacing between sections
3. **Clean Typography**: High contrast, readable fonts
4. **Modern Aesthetics**: Glassmorphism, gradients, ambient lighting
"""

from typing import List, Dict
from dataclasses import dataclass
from src.stats_processor import LibraryStats


@dataclass(frozen=True)
class Colors:
    """
    Midnight Aurora Color Palette.
    Deep indigo/slate background with vibrant sky blue, purple, and pink accents.
    """
    # Background gradient
    bg_start: str = "#0f172a"      # Deep slate
    bg_end: str = "#1e1b4b"        # Midnight indigo
    
    # Text colors
    text_primary: str = "#f8fafc"   # Bright white
    text_secondary: str = "#94a3b8" # Muted slate
    text_muted: str = "#64748b"     # Darker slate
    
    # Accent gradients
    accent_1: str = "#38bdf8"       # Sky blue
    accent_2: str = "#818cf8"       # Indigo
    accent_3: str = "#c084fc"       # Purple
    accent_4: str = "#f472b6"       # Pink
    
    # Card backgrounds
    card_bg: str = "rgba(30, 41, 59, 0.7)"
    card_border: str = "rgba(148, 163, 184, 0.1)"
    
    # Status-specific colors
    status_reading: str = "#38bdf8"
    status_completed: str = "#4ade80"
    status_plan: str = "#c084fc"
    status_dropped: str = "#f87171"
    status_paused: str = "#fbbf24"


# Layout constants
WIDTH: int = 1200  # Full-width canvas for better screen utilization
PADDING: int = 60  # Generous side padding
GAP: int = 40      # Extra-large gap between major sections


def _fmt_num(val: float) -> str:
    """Format numbers: whole numbers with commas, decimals with 1 place."""
    if val == int(val):
        return f"{int(val):,}"
    return f"{val:,.1f}"


def _truncate(text: str, max_len: int) -> str:
    """Truncate long text with ellipsis to prevent overflow."""
    if not text or len(text) <= max_len:
        return text or "Unknown"
    return text[:max_len-3] + "..."


def generate_svg(stats: LibraryStats, username: str) -> str:
    """
    Generate complete SVG card with all sections.
    
    Layout Structure (vertical rows with careful spacing):
    ┌─────────────────────────────────────────┐
    │ ROW 1: HEADER (Title + User + Donut)    │ 160px
    ├─────────────────────────────────────────┤
    │ ROW 2: PRIMARY STATS (4 cards)          │ 120px
    ├─────────────────────────────────────────┤
    │ ROW 3: TOP GENRES (Bar chart)           │ 180px
    ├────── 40px SPACING BUFFER ──────────────┤
    │ ROW 4: READING STATUS (Progress bars)   │ 160px
    ├─────────────────────────────────────────┤
    │ ROW 5: METRICS (3 rate cards)           │ 110px
    ├─────────────────────────────────────────┤
    │ ROW 6: ACTIVITY HEATMAP (7 days)        │ 100px
    └─────────────────────────────────────────┘
    
    Args:
        stats: Processed library statistics
        username: User's display name
        
    Returns:
        Complete SVG string
    """
    # Calculate total height dynamically
    # Each row height + gaps + padding
    HEIGHT = 160 + 120 + 180 + 40 + 160 + 110 + 100 + 40
    
    # Start SVG with responsive viewBox
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="100%" height="auto" '
        f'font-family="\'Segoe UI\', Roboto, sans-serif">'
    ]
    
    # === DEFINITIONS: Gradients & Filters ===
    svg.append(f'''
    <defs>
        <!-- Background Gradient -->
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{Colors.bg_start}"/>
            <stop offset="100%" stop-color="{Colors.bg_end}"/>
        </linearGradient>
        
        <!-- Accent Gradient (Blue to Purple) -->
        <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{Colors.accent_1}"/>
            <stop offset="100%" stop-color="{Colors.accent_3}"/>
        </linearGradient>
        
        <!-- Glow Filter for Ambient Effects -->
        <filter id="glow">
            <feGaussianBlur stdDeviation="40" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        
        <!-- Text Styles -->
        <style>
            .section-title {{ font-size: 18px; fill: {Colors.text_primary}; font-weight: bold; }}
            .card-label {{ font-size: 14px; fill: {Colors.text_secondary}; font-weight: 600; }}
            .card-value {{ font-size: 32px; fill: url(#accentGrad); font-weight: bold; }}
            .metric-main {{ font-size: 26px; fill: {Colors.text_primary}; font-weight: bold; }}
            .metric-sub {{ font-size: 13px; fill: {Colors.text_secondary}; }}
            .bar-label {{ font-size: 14px; fill: {Colors.text_secondary}; }}
            .bar-value {{ font-size: 14px; fill: {Colors.text_primary}; font-weight: bold; }}
        </style>
    </defs>
    ''')
    
    # === BACKGROUND ===
    svg.append(f'<rect width="100%" height="100%" fill="url(#bgGrad)"/>')
    
    # Ambient orbs for depth (large blurred circles)
    svg.append(f'<circle cx="150" cy="150" r="200" fill="{Colors.accent_2}" opacity="0.12" filter="url(#glow)"/>')
    svg.append(f'<circle cx="{WIDTH-150}" cy="{HEIGHT-150}" r="250" fill="{Colors.accent_3}" opacity="0.10" filter="url(#glow)"/>')
    
    # === ROW 1: HEADER (y=20) ===
    y = 20
    svg.append(f'''
    <g transform="translate(0, {y})">
        <!-- Main Title -->
        <text x="{PADDING}" y="0" font-size="42" font-weight="bold" fill="{Colors.text_primary}">MangaBaka Stats</text>
        <text x="{PADDING}" y="35" font-size="18" fill="{Colors.text_secondary}">Comprehensive Library Analytics</text>
        
        <!-- Decorative Separator Line -->
        <line x1="{PADDING}" y1="55" x2="{WIDTH-PADDING-200}" y2="55" stroke="{Colors.card_border}" stroke-width="1"/>
        
        <!-- Avatar Circle -->
        <circle cx="{PADDING+30}" cy="110" r="28" fill="url(#accentGrad)"/>
        <text x="{PADDING+30}" y="120" text-anchor="middle" font-size="22" font-weight="bold" fill="#fff">{username[0].upper() if username else '?'}</text>
        
        <!-- Username -->
        <text x="{PADDING+75}" y="105" font-size="24" font-weight="600" fill="{Colors.text_primary}">@{username}</text>
        <text x="{PADDING+75}" y="130" font-size="16" fill="{Colors.text_secondary}">Total Entries: {stats.total:,}</text>
        
        <!-- Mini Donut Chart (Right Side) -->
        <g transform="translate({WIDTH-PADDING-100}, 40)">
            <circle cx="60" cy="60" r="50" fill="none" stroke="{Colors.card_border}" stroke-width="10"/>
            <circle cx="60" cy="60" r="50" fill="none" stroke="url(#accentGrad)" stroke-width="10" 
                    stroke-dasharray="220 314" stroke-linecap="round" transform="rotate(-90 60 60)"/>
            <text x="60" y="65" text-anchor="middle" font-size="14" fill="{Colors.text_primary}">Active</text>
        </g>
    </g>
    ''')
    
    y = 160  # Move to next row
    
    # === ROW 2: PRIMARY STATS (4 Cards) ===
    card_w = 240
    card_h = 90
    start_x = PADDING
    
    def stat_card(label: str, value: str, idx: int) -> str:
        x = start_x + idx * (card_w + 20)
        return f'''
        <g transform="translate({x}, {y})">
            <rect width="{card_w}" height="{card_h}" rx="12" fill="{Colors.card_bg}" stroke="{Colors.card_border}" stroke-width="1"/>
            <text x="20" y="35" class="card-label">{label}</text>
            <text x="20" y="65" class="card-value">{value}</text>
        </g>
        '''
    
    svg.append(stat_card("CHAPTERS READ", _fmt_num(stats.chapters), 0))
    svg.append(stat_card("VOLUMES READ", _fmt_num(stats.volumes), 1))
    svg.append(stat_card("AVG SCORE", f"{stats.avg_rating:.1f}/10", 2))
    svg.append(stat_card("REREADS", str(stats.rereads), 3))
    
    y = 160 + 120  # Move to next row
    
    # === ROW 3: TOP GENRES (Bar Chart) ===
    top_genres = stats.top_genres[:5]  # Already sorted in processor
    max_count = top_genres[0][1] if top_genres else 1
    bar_h = 24
    bar_gap = 12
    label_w = 140
    max_bar_w = WIDTH - PADDING*2 - label_w - 50
    
    genre_bars = []
    for i, (genre, count) in enumerate(top_genres):
        bar_w = (count / max_count) * max_bar_w
        ypos = i * (bar_h + bar_gap)
        display_name = _truncate(genre, 18)
        
        genre_bars.append(f'''
        <g transform="translate({PADDING}, {ypos})">
            <text x="0" y="18" class="bar-label">{display_name}</text>
            <rect x="{label_w}" y="2" width="{bar_w}" height="{bar_h}" rx="4" fill="url(#accentGrad)" opacity="0.85"/>
            <text x="{label_w + bar_w + 8}" y="18" class="bar-value">{count}</text>
        </g>
        ''')
    
    svg.append(f'''
    <g transform="translate(0, {y})">
        <text x="{PADDING}" y="0" class="section-title">TOP GENRES</text>
        {''.join(genre_bars)}
    </g>
    ''')
    
    y = 160 + 120 + 180 + 40  # Add extra 40px spacing buffer!
    
    # === ROW 4: READING STATUS (Progress Bars) ===
    status_data = [
        ("Reading", stats.reading, Colors.status_reading),
        ("Completed", stats.completed, Colors.status_completed),
        ("Plan to Read", stats.plan_to_read, Colors.status_plan),
        ("Dropped", stats.dropped, Colors.status_dropped),
        ("Paused", stats.paused, Colors.status_paused),
    ]
    
    total_status = sum(s[1] for s in status_data) or 1
    bar_h_status = 10
    row_gap_status = 28
    max_bar_w_status = WIDTH - PADDING*2 - 200
    
    status_svg_parts = []
    for i, (label, count, color) in enumerate(status_data):
        pct = (count / total_status) * 100
        bar_w = (pct / 100) * max_bar_w_status
        ypos = i * row_gap_status
        
        status_svg_parts.append(f'''
        <g transform="translate({PADDING}, {ypos})">
            <text x="0" y="12" class="bar-label">{label}</text>
            <rect x="130" y="4" width="{bar_w}" height="{bar_h_status}" rx="5" fill="{color}"/>
            <text x="{130 + bar_w + 8}" y="13" class="bar-value">{count} ({pct:.1f}%)</text>
        </g>
        ''')
    
    svg.append(f'''
    <g transform="translate(0, {y})">
        <text x="{PADDING}" y="0" class="section-title">READING STATUS</text>
        {''.join(status_svg_parts)}
    </g>
    ''')
    
    y = 160 + 120 + 180 + 40 + 160  # Next row
    
    # === ROW 5: METRICS (3 Cards) ===
    metric_w = 340
    metric_h = 80
    
    comp_rate = (stats.completed / stats.total * 100) if stats.total > 0 else 0
    succ_rate = (stats.completed / (stats.completed + stats.dropped) * 100) if (stats.completed + stats.dropped) > 0 else 0
    avg_chaps = f"{stats.avg_chapters_per_day:.2f}" if stats.avg_chapters_per_day else "0.00"
    
    metrics = [
        ("COMPLETION RATE", f"{comp_rate:.1f}%", f"{stats.completed}/{stats.total}"),
        ("SUCCESS RATIO", f"{succ_rate:.1f}%", "Completed vs Dropped"),
        ("AVG CHAPS/DAY", avg_chaps, "Last 30 Days"),
    ]
    
    metric_cards = []
    for i, (title, main, sub) in enumerate(metrics):
        x = PADDING + i * (metric_w + 20)
        metric_cards.append(f'''
        <g transform="translate({x}, {y})">
            <rect width="{metric_w}" height="{metric_h}" rx="12" fill="{Colors.card_bg}" stroke="{Colors.card_border}" stroke-width="1"/>
            <text x="20" y="25" font-size="13" fill="{Colors.text_secondary}" font-weight="600" letter-spacing="0.5">{title}</text>
            <text x="20" y="55" class="metric-main">{main}</text>
            <text x="20" y="72" class="metric-sub">{sub}</text>
        </g>
        ''')
    
    svg.append(''.join(metric_cards))
    
    y = 160 + 120 + 180 + 40 + 160 + 110  # Next row
    
    # === ROW 6: ACTIVITY HEATMAP (7 Days) ===
    activity = stats.activity_last_7_days or [0] * 7
    max_act = max(activity) or 1
    square_size = 50
    square_gap = 15
    
    heatmap_squares = []
    for i, count in enumerate(activity):
        x = PADDING + i * (square_size + square_gap)
        opacity = 0.2 + (0.8 * (count / max_act))
        
        heatmap_squares.append(f'''
        <g transform="translate({x}, {y})">
            <rect width="{square_size}" height="{square_size}" rx="8" fill="{Colors.accent_2}" opacity="{opacity}"/>
            <text x="{square_size/2}" y="{square_size/2 + 5}" text-anchor="middle" font-size="16" font-weight="bold" fill="#fff">{count}</text>
            <text x="{square_size/2}" y="{square_size + 15}" text-anchor="middle" font-size="11" fill="{Colors.text_secondary}">Day {i+1}</text>
        </g>
        ''')
    
    svg.append(f'''
    <g transform="translate(0, {y})">
        <text x="{PADDING}" y="-20" class="section-title">ACTIVITY (LAST 7 DAYS)</text>
        {''.join(heatmap_squares)}
    </g>
    ''')
    
    # Close SVG
    svg.append('</svg>')
    
    return ''.join(svg)
