"""
SVG Generator Module - Modern Responsive Dashboard

This module generates a beautiful, responsive SVG stats card with:
- Dynamic height calculation to prevent overlap
- Modern glassmorphism design
- Activity heatmap (last 7 days)
- Completion/Success rates
- Top rated manga picks
- Genre distribution bar chart
- Reading status breakdown

Key Design Principles:
1. **Dynamic Sizing**: Canvas expands vertically based on content
2. **Grid System**: Consistent spacing prevents visual clutter
3. **Component-Based**: Each section is independently built
4. **Responsive**: Works at any display size via viewBox
5. **No Overlaps**: Careful Y-coordinate calculation for each row
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
    reading: str = "#3b82f6"
    completed: str = "#10b981"
    planned: str = "#f59e0b"
    dropped: str = "#ef4444"
    paused: str = "#8b5cf6"


# Layout constants
CANVAS_WIDTH: int = 1200
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
    """Truncate text with ellipsis to prevent overflow."""
    if not text or len(text) <= max_len:
        return text or ""
    return text[:max_len-3] + "..."


def _heatmap_svg(data: List[int], x: int, y: int) -> str:
    """Generate 7-day activity heatmap squares."""
    # Ensure exactly 7 days
    days = (data + [0]*7)[:7]
    rects = []
    max_val = max(days) if days else 1
    for i, val in enumerate(days):
        cx = x + i * 40
        # Opacity based on activity level
        opacity = 0.3 if val == 0 else 0.4 + (min(val, max(max_val, 1))/max(max_val, 1))*0.6
        rects.append(
            f'<rect x="{cx}" y="{y}" width="30" height="30" rx="6" '
            f'fill="{Colors.accent_blue}" fill-opacity="{opacity}"/>'
            f'<text x="{cx+15}" y="{y+20}" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">{val}</text>'
        )
    return "\n".join(rects)


def _donut_svg(cx: int, cy: int, radius: int, status: Dict[str, int]) -> str:
    """Generate donut chart for status distribution."""
    total = sum(status.values())
    if total == 0:
        return ""
    
    colors_map = {
        'reading': Colors.reading,
        'completed': Colors.completed,
        'planned': Colors.planned,
        'dropped': Colors.dropped,
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
            f'stroke="{colors_map[key]}" stroke-width="20" '
            f'stroke-dasharray="{dash} {gap}" '
            f'transform="rotate({rotate - 90} {cx} {cy})" opacity="0.9"/>'
        )
        offset += dash
    
    return "\n".join(parts)


def generate_svg(stats: LibraryStats, username: str) -> str:
    """
    Generate complete SVG card with dynamic height and all sections.
    
    Args:
        stats: LibraryStats dataclass containing all computed statistics
        username: User's display name
        
    Layout rows (carefully calculated to prevent overlap):
    1. Header (user + donut): 140px
    2. Primary stats (4 cards): 100px  
    3. Genre bar chart: 140px
    4. Status breakdown: 140px
    5. Secondary stats (3 cards): 90px
    6. Heatmap: 80px
    7. Top picks: 120px
    """
    
    # Build status counts dict from individual fields
    status_counts = {
        'reading': stats.reading,
        'completed': stats.completed,
        'planned': stats.plan_to_read,
        'dropped': stats.dropped,
        'paused': stats.paused,
    }
    
    # Convert top_genres list of tuples to dict
    genre_counts = dict(stats.top_genres)
    
    # Row heights for dynamic layout - carefully spaced to prevent overlap
    ROWS = {
        'header': 140,
        'primary': 100,
        'genres': 140,
        'status': 140,
        'secondary': 90,
        'heatmap': 80,
        'picks': 120,
    }
    
    # Calculate total height dynamically
    total_height = (
        PADDING +
        ROWS['header'] + GRID_GAP +
        ROWS['primary'] + GRID_GAP +
        ROWS['genres'] + GRID_GAP +
        ROWS['status'] + GRID_GAP +
        ROWS['secondary'] + GRID_GAP +
        ROWS['heatmap'] + GRID_GAP +
        ROWS['picks'] +
        PADDING
    )
    
    svg = []
    
    # SVG Header with dynamic height and viewBox for responsiveness
    svg.append(
        f'<svg width="100%" height="auto" viewBox="0 0 {CANVAS_WIDTH} {total_height}" '
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
        .title{font-size:14px;fill:#94a3b8;font-weight:600;letter-spacing:0.5px}
        .value{font-size:24px;fill:#f8fafc;font-weight:700}
        .sub{font-size:12px;fill:#cbd5e1}
        .label{font-size:11px;fill:#64748b;font-weight:500}
        .section-title{font-size:16px;fill:#f8fafc;font-weight:bold}
      </style>
    </defs>
    ''')
    
    # Background
    svg.append(f'<rect width="100%" height="100%" fill="url(#bgGrad)" rx="{CARD_RADIUS}"/>')
    
    # Ambient glow effects for depth
    svg.append(f'<circle cx="{CANVAS_WIDTH-80}" cy="80" r="120" fill="#38bdf8" opacity="0.05"/>')
    svg.append(f'<circle cx="80" cy="{total_height-80}" r="100" fill="#818cf8" opacity="0.05"/>')
    
    y = PADDING
    
    # === ROW 1: Header (User Info + Donut) ===
    # Avatar circle
    svg.append(f'<circle cx="55" cy="{y+40}" r="35" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="3"/>')
    initial = username[0].upper() if username else '?'
    svg.append(f'<text x="55" y="{y+52}" text-anchor="middle" font-size="28" font-weight="bold" fill="#38bdf8">{initial}</text>')
    
    # Username & Total Entries
    username_truncated = _truncate(username, 20)
    total_entries = _format_num(stats.total)
    svg.append(f'<text x="110" y="{y+35}" font-size="20" font-weight="bold" fill="#f8fafc">@{username_truncated}</text>')
    svg.append(f'<text x="110" y="{y+60}" font-size="14" fill="#94a3b8">Total Entries: <tspan fill="#38bdf8" font-weight="bold">{total_entries}</tspan></text>')
    
    # Donut chart (right side)
    svg.append(_donut_svg(CANVAS_WIDTH-90, y+50, 50, status_counts))
    
    y += ROWS['header'] + GRID_GAP
    
    # === ROW 2: Primary Stats (4 cards) ===
    primary = [
        {'lbl': 'CHAPTERS READ', 'val': stats.chapters, 'color': Colors.accent_blue},
        {'lbl': 'VOLUMES READ', 'val': stats.volumes, 'color': Colors.accent_purple},
        {'lbl': 'AVG SCORE', 'val': stats.avg_rating, 'suffix': '/10', 'color': Colors.warning},
        {'lbl': 'REREADS', 'val': stats.rereads, 'color': Colors.success},
    ]
    
    card_w = (CANVAS_WIDTH - PADDING*2 - GRID_GAP*3) // 4
    
    for i, s in enumerate(primary):
        cx = PADDING + i * (card_w + GRID_GAP)
        val_str = f"{_format_num(s['val'])}{s.get('suffix', '')}"
        
        svg.append(f'<rect x="{cx}" y="{y}" width="{card_w}" height="80" rx="8" fill="url(#cardGrad)"/>')
        svg.append(f'<text x="{cx+card_w/2}" y="{y+26}" text-anchor="middle" class="title">{s["lbl"]}</text>')
        svg.append(f'<text x="{cx+card_w/2}" y="{y+60}" text-anchor="middle" class="value" fill="{s["color"]}">{val_str}</text>')
    
    y += ROWS['primary'] + GRID_GAP
    
    # === ROW 3: Genre Distribution (Bar Chart) ===
    svg.append(f'<text x="{PADDING}" y="{y}" class="section-title">TOP GENRES</text>')
    
    # Sort genres by count and take top 5
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    max_count = sorted_genres[0][1] if sorted_genres else 1
    
    gy = y + 25
    bar_height = 20
    bar_gap = 12
    label_width = 120
    max_bar_width = CANVAS_WIDTH - PADDING*2 - label_width - 60
    
    for genre_name, count in sorted_genres:
        display_name = _truncate(genre_name, 15)
        bar_width = (count / max_count) * max_bar_width if max_count > 0 else 0
        
        svg.append(f'<text x="{PADDING}" y="{gy+15}" font-size="12" fill="#94a3b8">{display_name}</text>')
        svg.append(f'<rect x="{PADDING+label_width}" y="{gy+5}" width="{bar_width}" height="{bar_height}" rx="4" fill="{Colors.accent_blue}" opacity="0.8"/>')
        svg.append(f'<text x="{PADDING+label_width+bar_width+8}" y="{gy+19}" font-size="12" fill="#f8fafc">{count}</text>')
        gy += bar_height + bar_gap
    
    y += ROWS['genres'] + GRID_GAP
    
    # === ROW 4: Reading Status Breakdown ===
    svg.append(f'<text x="{PADDING}" y="{y}" class="section-title">READING STATUS</text>')
    
    sy = y + 25
    status_items = [
        ("Reading", stats.reading, Colors.reading),
        ("Completed", stats.completed, Colors.completed),
        ("Plan to Read", stats.plan_to_read, Colors.planned),
        ("Dropped", stats.dropped, Colors.dropped),
        ("Paused", stats.paused, Colors.paused),
    ]
    
    for s_name, s_count, s_color in status_items:
        if s_count == 0:
            continue
        pct = (s_count / stats.total * 100) if stats.total > 0 else 0
        bar_w = (pct / 100) * (CANVAS_WIDTH - PADDING*2 - 140)
        
        svg.append(f'<text x="{PADDING}" y="{sy+14}" font-size="12" fill="#94a3b8" width="100">{s_name}</text>')
        svg.append(f'<rect x="{PADDING+110}" y="{sy+4}" width="{bar_w}" height="10" rx="5" fill="{s_color}"/>')
        svg.append(f'<text x="{PADDING+110+bar_w+8}" y="{sy+14}" font-size="12" fill="#f8fafc">{s_count} ({pct:.1f}%)</text>')
        sy += 26
    
    y += ROWS['status'] + GRID_GAP
    
    # === ROW 5: Secondary Stats (Rates & Averages) ===
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
        svg.append(f'<text x="{cx+sec_w/2}" y="{y+24}" text-anchor="middle" class="title">{s["lbl"]}</text>')
        svg.append(f'<text x="{cx+sec_w/2}" y="{y+52}" text-anchor="middle" class="value" fill="{s["color"]}">{s["val"]}</text>')
        svg.append(f'<text x="{cx+sec_w/2}" y="{y+66}" text-anchor="middle" class="label">{s["sub"]}</text>')
    
    y += ROWS['secondary'] + GRID_GAP
    
    # === ROW 6: 7-Day Activity Heatmap ===
    activity = stats.activity_last_7_days
    svg.append(f'<text x="{PADDING}" y="{y}" class="section-title">ACTIVITY (LAST 7 DAYS)</text>')
    svg.append(_heatmap_svg(activity, PADDING, y+20))
    
    y += ROWS['heatmap'] + GRID_GAP
    
    # === ROW 7: Top Rated Manga ===
    top_manga = stats.top_rated_manga
    
    svg.append(f'<text x="{PADDING}" y="{y}" class="section-title">HIGHEST RATED MANGA</text>')
    
    py = y + 25
    # Split into two columns for better use of space
    col_w = (CANVAS_WIDTH - PADDING*2 - GRID_GAP) // 2
    
    def render_manga_picks(items: list, x_off: int) -> str:
        """Render top manga picks with score badges and details."""
        if not items:
            return f'<text x="{x_off}" y="{py+30}" class="label">No data available</text>'
        
        parts = []
        for idx, item in enumerate(items[:2]):
            yp = py + idx * 55
            score = item.get('score', 0)
            title = _truncate(item.get('title', 'Unknown'), 35)
            
            badge_col = Colors.success if score >= 8 else Colors.warning if score >= 6 else Colors.danger
            
            # Card background
            parts.append(f'<rect x="{x_off}" y="{yp}" width="{col_w}" height="45" rx="8" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.1)"/>')
            
            # Score badge
            parts.append(f'<rect x="{x_off+10}" y="{yp+8}" width="45" height="30" rx="6" fill="{badge_col}"/>')
            parts.append(f'<text x="{x_off+32}" y="{yp+22}" text-anchor="middle" font-size="16" fill="#fff" font-weight="bold">{score}</text>')
            parts.append(f'<text x="{x_off+32}" y="{yp+35}" text-anchor="middle" font-size="8" fill="#fff">SCORE</text>')
            
            # Title
            parts.append(f'<text x="{x_off+65}" y="{yp+22}" font-size="14" fill="#f8fafc" font-weight="bold">{title}</text>')
            parts.append(f'<text x="{x_off+65}" y="{yp+38}" font-size="11" fill="#94a3b8">Click to view details</text>')
        
        return "".join(parts)
    
    svg.append(render_manga_picks(top_manga, PADDING))
    
    svg.append('</svg>')
    return "".join(svg)
