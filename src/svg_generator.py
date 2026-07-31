"""
SVG Generator Module - Modern Responsive Dashboard

This module generates a beautiful, responsive SVG stats card with:
- Dynamic height calculation to prevent overlap
- Modern glassmorphism design
- Activity heatmap (last 7 days)
- Completion/Success rates
- Top rated manga & anime picks

Key Design Principles:
1. **Dynamic Sizing**: Canvas expands vertically based on content
2. **Grid System**: Consistent spacing prevents visual clutter
3. **Component-Based**: Each section is independently built
4. **Responsive**: Works at any display size via viewBox
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import math
from src.stats_processor import LibraryStats


@dataclass(frozen=True)
class Colors:
    """Modern color palette - Deep Ocean theme."""
    bg_start: str = "#0f172a"
    bg_end: str = "#1e293b"
    card_bg: str = "#334155"
    text_primary: str = "#f8fafc"
    text_secondary: str = "#94a3b8"
    accent_blue: str = "#38bdf8"
    accent_purple: str = "#818cf8"
    success: str = "#4ade80"
    warning: str = "#facc15"
    danger: str = "#f87171"


# Layout constants
CANVAS_WIDTH: int = 900
PADDING: int = 30
GRID_GAP: int = 20
CARD_RADIUS: int = 12
FONT_FAMILY: str = "'Segoe UI', Roboto, sans-serif"


def _format_num(value: float) -> str:
    """Format numbers: integers with commas, floats with 1 decimal."""
    if value == int(value):
        return f"{int(value):,}"
    return f"{value:,.1f}"


def _truncate(text: str, max_len: int) -> str:
    """Truncate text with ellipsis."""
    if not text or len(text) <= max_len:
        return text or ""
    return text[:max_len-3] + "..."


def _heatmap_svg(data: List[int], x: int, y: int) -> str:
    """Generate 7-day activity heatmap squares."""
    # Ensure exactly 7 days
    days = (data + [0]*7)[:7]
    rects = []
    for i, val in enumerate(days):
        cx = x + i * 15
        # Opacity based on activity level (0-10 scale)
        opacity = 0.3 if val == 0 else 0.4 + (min(val, 10)/10)*0.6
        rects.append(
            f'<rect x="{cx}" y="{y}" width="12" height="12" rx="2" '
            f'fill="{Colors.accent_blue}" fill-opacity="{opacity}"/>'
        )
    return "\n".join(rects)


def _donut_svg(cx: int, cy: int, radius: int, status: Dict[str, int]) -> str:
    """Generate donut chart for status distribution."""
    total = sum(status.values())
    if total == 0:
        return ""
    
    colors_map = {
        'reading': Colors.accent_blue,
        'completed': Colors.success,
        'planned': Colors.warning,
        'dropped': Colors.danger,
    }
    
    parts = []
    offset = 0
    circumference = 2 * math.pi * radius
    
    for key in ['reading', 'completed', 'planned', 'dropped']:
        val = status.get(key, 0)
        if val == 0:
            continue
        
        frac = val / total
        dash = circumference * frac
        gap = circumference - dash
        rotate = (offset / circumference) * 360
        
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{colors_map[key]}" stroke-width="12" '
            f'stroke-dasharray="{dash} {gap}" '
            f'transform="rotate({rotate - 90} {cx} {cy})" opacity="0.9"/>'
        )
        offset += dash
    
    return "\n".join(parts)


def generate_svg(stats: LibraryStats, username: str) -> str:
    """
    Generate complete SVG card with dynamic height.
    
    Args:
        stats: LibraryStats dataclass containing all computed statistics
        username: User's display name
        
    Layout rows (calculated to prevent overlap):
    1. Header (user + donut): 140px
    2. Primary stats (4 cards): 100px  
    3. Secondary stats (3 cards): 90px
    4. Heatmap: 60px
    5. Top picks: 100px
    """
    
    # Convert dataclass to dict for easier access
    stats_dict = {
        'username': username,
        'total_entries': stats.total,
        'chapters_read': stats.chapters,
        'volumes_read': stats.volumes,
        'mean_score': stats.avg_rating,
        'reread_count': stats.rereads,
        'status_distribution': {
            'reading': stats.reading,
            'completed': stats.completed,
            'planned': stats.plan_to_read,
            'dropped': stats.dropped,
        },
        'avg_chapters_per_day': stats.avg_chapters_per_day,
        'activity_last_7_days': stats.activity_last_7_days,
        'top_rated_manga': stats.top_rated_manga,
        'top_rated_anime': stats.top_rated_anime,
    }
    
    # Row heights for dynamic layout
    ROWS = {
        'header': 140,
        'primary': 100,
        'secondary': 90,
        'heatmap': 60,
        'picks': 100,
    }
    
    # Calculate total height dynamically
    total_height = (
        PADDING +
        ROWS['header'] + GRID_GAP +
        ROWS['primary'] + GRID_GAP +
        ROWS['secondary'] + GRID_GAP +
        ROWS['heatmap'] + GRID_GAP +
        ROWS['picks'] +
        PADDING
    )
    
    svg = []
    
    # SVG Header with dynamic height
    svg.append(
        f'<svg width="{CANVAS_WIDTH}" height="{total_height}" '
        f'viewBox="0 0 {CANVAS_WIDTH} {total_height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="{FONT_FAMILY}">'
    )
    
    # Definitions
    svg.append('''
    <defs>
      <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a"/>
        <stop offset="100%" stop-color="#1e293b"/>
      </linearGradient>
      <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#334155" stop-opacity="0.6"/>
        <stop offset="100%" stop-color="#334155" stop-opacity="0.3"/>
      </linearGradient>
      <style>
        .title{font-size:12px;fill:#94a3b8;font-weight:600;letter-spacing:0.5px}
        .value{font-size:22px;fill:#f8fafc;font-weight:700}
        .sub{font-size:11px;fill:#cbd5e1}
        .label{font-size:10px;fill:#64748b;font-weight:500}
      </style>
    </defs>
    ''')
    
    # Background
    svg.append(f'<rect width="100%" height="100%" fill="url(#bgGrad)" rx="{CARD_RADIUS}"/>')
    
    # Ambient glow effects
    svg.append(f'<circle cx="{CANVAS_WIDTH-80}" cy="80" r="120" fill="#38bdf8" opacity="0.05"/>')
    svg.append(f'<circle cx="80" cy="{total_height-80}" r="100" fill="#818cf8" opacity="0.05"/>')
    
    y = PADDING
    
    # === ROW 1: Header (User Info + Donut) ===
    # Avatar
    svg.append(f'<circle cx="55" cy="{y+40}" r="28" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="2"/>')
    initial = username[0].upper() if username else '?'
    svg.append(f'<text x="55" y="{y+48}" text-anchor="middle" font-size="22" font-weight="bold" fill="#38bdf8">{initial}</text>')
    
    # Username & Total
    username_truncated = _truncate(username, 18)
    total_entries = _format_num(stats.total)
    svg.append(f'<text x="95" y="{y+32}" font-size="16" font-weight="bold" fill="#f8fafc">@{username_truncated}</text>')
    svg.append(f'<text x="95" y="{y+55}" font-size="12" fill="#94a3b8">Total Entries: <tspan fill="#38bdf8" font-weight="bold">{total_entries}</tspan></text>')
    
    # Donut chart (right side)
    svg.append(_donut_svg(CANVAS_WIDTH-90, y+50, 35, stats_dict['status_distribution']))
    
    y += ROWS['header'] + GRID_GAP
    
    # === ROW 2: Primary Stats (4 cards) ===
    primary = [
        {'lbl': 'CHAPTERS', 'val': stats.chapters, 'color': Colors.accent_blue},
        {'lbl': 'VOLUMES', 'val': stats.volumes, 'color': Colors.accent_purple},
        {'lbl': 'AVG SCORE', 'val': stats.avg_rating, 'suffix': '/10', 'color': Colors.warning},
        {'lbl': 'REREADS', 'val': stats.rereads, 'color': Colors.success},
    ]
    
    card_w = (CANVAS_WIDTH - PADDING*2 - GRID_GAP*3) // 4
    
    for i, s in enumerate(primary):
        cx = PADDING + i * (card_w + GRID_GAP)
        val_str = f"{_format_num(s['val'])}{s.get('suffix', '')}"
        
        svg.append(f'<rect x="{cx}" y="{y}" width="{card_w}" height="80" rx="8" fill="url(#cardGrad)"/>')
        svg.append(f'<text x="{cx+card_w/2}" y="{y+24}" text-anchor="middle" class="title">{s["lbl"]}</text>')
        svg.append(f'<text x="{cx+card_w/2}" y="{y+55}" text-anchor="middle" class="value" fill="{s["color"]}">{val_str}</text>')
    
    y += ROWS['primary'] + GRID_GAP
    
    # === ROW 3: Secondary Stats (Rates & Averages) ===
    total_ent = max(stats.total, 1)
    completed = stats.completed
    dropped = stats.dropped
    
    completion_rate = (completed / total_ent) * 100 if total_ent > 0 else 0
    success_rate = (completed / max(completed + dropped, 1)) * 100 if (completed + dropped) > 0 else 0
    avg_chap_day = stats.avg_chapters_per_day
    
    secondary = [
        {'lbl': 'COMPLETION RATE', 'val': f"{completion_rate:.1f}%", 'sub': f"{completed}/{stats.total}", 'color': Colors.accent_blue},
        {'lbl': 'SUCCESS RATIO', 'val': f"{success_rate:.1f}%", 'sub': 'Completed vs Dropped', 'color': Colors.success},
        {'lbl': 'AVG CHAPS/DAY', 'val': f"{avg_chap_day:.2f}", 'sub': 'Last 30 Days', 'color': Colors.warning},
    ]
    
    sec_w = (CANVAS_WIDTH - PADDING*2 - GRID_GAP*2) // 3
    
    for i, s in enumerate(secondary):
        cx = PADDING + i * (sec_w + GRID_GAP)
        svg.append(f'<rect x="{cx}" y="{y}" width="{sec_w}" height="70" rx="8" fill="url(#cardGrad)"/>')
        svg.append(f'<text x="{cx+sec_w/2}" y="{y+22}" text-anchor="middle" class="title">{s["lbl"]}</text>')
        svg.append(f'<text x="{cx+sec_w/2}" y="{y+48}" text-anchor="middle" class="value" fill="{s["color"]}">{s["val"]}</text>')
        svg.append(f'<text x="{cx+sec_w/2}" y="{y+63}" text-anchor="middle" class="label">{s["sub"]}</text>')
    
    y += ROWS['secondary'] + GRID_GAP
    
    # === ROW 4: 7-Day Activity Heatmap ===
    activity = stats.activity_last_7_days
    svg.append(f'<text x="{PADDING}" y="{y}" class="title">ACTIVITY (LAST 7 DAYS)</text>')
    svg.append(_heatmap_svg(activity, PADDING, y+12))
    
    y += ROWS['heatmap'] + GRID_GAP
    
    # === ROW 5: Top Picks (Manga & Anime) ===
    top_manga = stats.top_rated_manga
    top_anime = stats.top_rated_anime
    
    svg.append(f'<text x="{PADDING}" y="{y}" class="title">HIGHEST RATED</text>')
    
    py = y + 20
    col_w = (CANVAS_WIDTH - PADDING*2 - GRID_GAP) // 2
    
    def render_picks(items: list, x_off: int, title: str) -> str:
        if not items:
            return f'<text x="{x_off}" y="{py+18}" class="label">No data</text>'
        
        parts = [f'<text x="{x_off}" y="{py}" class="label" font-weight="bold">{title}</text>']
        for idx, item in enumerate(items[:2]):
            yp = py + 20 + idx * 20
            score = item.get('score', 0)
            name = _truncate(item.get('title', 'Unknown'), 28)
            
            badge_col = Colors.success if score >= 8 else Colors.warning if score >= 6 else Colors.danger
            parts.append(f'<rect x="{x_off}" y="{yp-8}" width="22" height="14" rx="3" fill="{badge_col}" fill-opacity="0.2"/>')
            parts.append(f'<text x="{x_off+11}" y="{py+2}" text-anchor="middle" font-size="9" font-weight="bold" fill="{badge_col}">{score}</text>')
            parts.append(f'<text x="{x_off+30}" y="{py+2}" font-size="10" fill="#cbd5e1">{name}</text>')
        
        return "".join(parts)
    
    svg.append(render_picks(top_manga, PADDING, "MANGA"))
    svg.append(render_picks(top_anime, PADDING + col_w + GRID_GAP, "ANIME"))
    
    svg.append('</svg>')
    return "".join(svg)
