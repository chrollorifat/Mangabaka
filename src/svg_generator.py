"""
MangaBaka Stats Card Generator - SVG Generator Module

This module handles the generation of the SVG stats card.
It takes computed statistics and creates a visually appealing SVG image.

REDESIGNED: Modern Cyber-Glass Dashboard Aesthetic (2024)
=========================================================
This new design features:
- Asymmetric dashboard layout with left identity panel and right metrics grid
- Deep ocean gradient background with neon accent colors
- Glassmorphism effects with semi-transparent cards
- Donut chart for visual activity distribution
- Pill-shaped genre tags instead of bars
- Ambient lighting with blurred circles for depth
- Compact yet information-dense presentation

Key Python concepts demonstrated:
- f-strings for string interpolation (modern Python 3.6+)
- Dataclasses for structured color palettes
- Helper methods for modular SVG construction
- Type hints for function parameters and return values
- String formatting for XML/SVG generation

Why generate SVG instead of using a graphics library?
    - SVG is text-based, so no heavy dependencies like PIL/Pillow needed
    - Scales perfectly at any size
    - Easy to version control (it's just text)
    - GitHub Pages serves SVG natively
    - Smaller file sizes than PNG for this type of content
"""

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class ColorPalette:
    """
    Centralized color palette for consistent theming.
    
    Why use a dataclass?
        - Provides a clean way to group related constants
        - Auto-generates __init__, __repr__, etc.
        - Makes it easy to swap themes in the future
        - Type-safe: IDE can autocomplete color names
    """
    # Background colors
    bg_dark: str = "#0f172a"      # Deep slate
    bg_light: str = "#1e293b"     # Midnight blue
    
    # Accent colors (neon vibes)
    primary: str = "#38bdf8"      # Sky blue
    secondary: str = "#818cf8"    # Indigo
    coral: str = "#fb7185"        # Coral pink
    turquoise: str = "#2dd4bf"    # Turquoise
    amber: str = "#fbbf24"        # Amber
    
    # Text colors
    text_primary: str = "#f1f5f9"
    text_secondary: str = "#94a3b8"
    text_muted: str = "#64748b"
    
    # Card backgrounds (glassmorphism)
    card_bg: str = "#ffffff"
    card_opacity: float = 0.08


# Import our statistics dataclass
from src.stats_processor import LibraryStats


def _escape_xml(text: str) -> str:
    """
    Escape special XML characters to prevent invalid SVG.
    
    Why is this necessary?
        XML/SVG has special characters like <, >, &, ", ' that have
        special meaning. If user data contains these (e.g., a nickname
        with "&" in it), we must escape them to avoid breaking the SVG.
    
    Args:
        text: The raw text to escape
        
    Returns:
        Text with special characters replaced by XML entities
        
    Example:
        "Tom & Jerry" -> "Tom &amp; Jerry"
    """
    # Dictionary mapping characters to their XML entity equivalents
    escape_map: dict[str, str] = {
        '&': '&amp;',   # Must be first! Otherwise we'd double-escape
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    
    # Replace each special character
    # We iterate through the map items for clarity
    for char, entity in escape_map.items():
        text = text.replace(char, entity)
    
    return text


def _generate_progress_bar(value: int, max_value: int, color: str, width: float = 100.0) -> str:
    """
    Generate an SVG progress bar element.
    
    This demonstrates:
        - f-string formatting with expressions
        - Conditional logic to prevent division by zero
        - Reusable component generation
    
    Args:
        value: Current value (e.g., number of manga read)
        max_value: Maximum value for scaling (e.g., highest count)
        color: Hex color code for the bar
        width: Maximum width of the bar in SVG units
        
    Returns:
        SVG rect element as a string
    """
    # Calculate percentage, avoiding division by zero
    if max_value > 0:
        percentage = (value / max_value) * 100
    else:
        percentage = 0.0
    
    # Generate the SVG rectangle
    # rx=\"3\" gives rounded corners
    return f'<rect x="0" y="0" width="{percentage:.2f}" height="6" rx="3" fill="{color}"/>'


def _generate_genre_bars(top_genres: list[tuple[str, int]]) -> str:
    """
    Generate SVG elements for genre bars.
    
    This function creates a series of horizontal bars showing
    the top genres by count.
    
    Args:
        top_genres: List of (genre_name, count) tuples, sorted by count
        
    Returns:
        SVG group element containing all genre bars
    """
    if not top_genres:
        return ""
    
    # Modern color palette for the bars (cycled if more than 5 genres)
    # Using softer, more vibrant colors that work well on dark background
    colors: list[str] = ['#ff6b6b', '#4ecdc4', '#ffd93d', '#ee5aa7', '#95e1d3']
    
    # Get the maximum count for scaling (first item since it's sorted)
    max_count = top_genres[0][1] if top_genres else 1
    
    # Build each bar's SVG
    bars: list[str] = []
    
    # Limit to top 5 genres to prevent overflow
    limited_genres = top_genres[:5]
    
    for i, (name, count) in enumerate(limited_genres):
        # Calculate bar width relative to max (max width = 140 units)
        bar_width = (count / max_count) * 140 if max_count > 0 else 0
        
        # Select color (cycle through palette using modulo)
        color = colors[i % len(colors)]
        
        # Vertical position based on index (tighter spacing for compact design)
        y_position = i * 20
        
        # Truncate long genre names to fit
        display_name = name[:18] + "…" if len(name) > 18 else name
        
        # Create the SVG elements for this genre
        # We use escaped name to handle special characters safely
        bar_svg = f'''
      <text x="0" y="{y_position}" fill="#a0a0c0" font-size="10" font-family="system-ui, sans-serif" opacity="0.9">{_escape_xml(display_name)}</text>
      <rect x="90" y="{y_position - 7}" width="{bar_width:.2f}" height="5" rx="2.5" fill="{color}" opacity="0.75"/>
      <text x="{95 + bar_width:.2f}" y="{y_position}" fill="#d0d0e0" font-size="9" font-family="system-ui, sans-serif">{count}</text>
    '''
        bars.append(bar_svg)
    
    # Join all bars into a single string
    return ''.join(bars)


def _generate_status_bar_row(
    label: str,
    value: int,
    max_value: int,
    color: str,
    y_offset: int
) -> str:
    """
    Generate a single row of the status distribution section.
    
    This helper function follows the DRY principle - instead of
    repeating similar code 5 times for each status, we create
    a reusable function.
    
    Args:
        label: Display label (e.g., "Reading")
        value: Count for this status
        max_value: Maximum value across all statuses (for scaling)
        color: Hex color for the progress bar
        y_offset: Vertical position in pixels
        
    Returns:
        SVG group element for one status row
    """
    return f'''
    <g transform="translate(0, {y_offset})">
      <text x="0" y="10" fill="#a0a0c0" font-size="9" font-family="system-ui, sans-serif" opacity="0.85">{label}</text>
      <g transform="translate(65, 4)">
        <rect width="125" height="5" rx="2.5" fill="#ffffff" opacity="0.06"/>
        {_generate_progress_bar(value, max_value, color)}
      </g>
      <text x="200" y="10" fill="#d0d0e0" font-size="9" font-family="system-ui, sans-serif">{value}</text>
    </g>
'''


def _generate_type_bar_row(
    label: str,
    value: int,
    max_value: int,
    color: str,
    y_offset: int
) -> str:
    """
    Generate a single row of the media types section.
    
    Similar to _generate_status_bar_row but with different width
    for the progress bar area.
    
    Args:
        label: Display label (e.g., "Manga")
        value: Count for this type
        max_value: Maximum value across all types (for scaling)
        color: Hex color for the progress bar
        y_offset: Vertical position in pixels
        
    Returns:
        SVG group element for one type row
    """
    return f'''
    <g transform="translate(0, {y_offset})">
      <text x="0" y="10" fill="#a0a0c0" font-size="9" font-family="system-ui, sans-serif" opacity="0.85">{label}</text>
      <g transform="translate(65, 4)">
        <rect width="95" height="5" rx="2.5" fill="#ffffff" opacity="0.06"/>
        {_generate_progress_bar(value, max_value, color)}
      </g>
      <text x="170" y="10" fill="#d0d0e0" font-size="9" font-family="system-ui, sans-serif">{value}</text>
    </g>
'''




def _generate_donut_chart(
    reading: int,
    completed: int,
    paused: int,
    dropped: int,
    plan_to_read: int,
    size: int = 120,
    stroke_width: int = 12
) -> str:
    """
    Generate a donut chart showing activity distribution.
    
    This uses the SVG stroke-dasharray technique to create pie segments.
    Each segment's dash length is proportional to its percentage of the total.
    
    Why a donut chart?
        - Visual way to show proportions at a glance
        - More engaging than just numbers
        - Modern dashboard aesthetic
    
    How stroke-dasharray works:
        - The circle's circumference is 2 * π * r
        - We set dash length = (value / total) * circumference
        - Gap length = circumference - dash length
        - By rotating each segment, we create a pie chart
    
    Args:
        reading: Count of reading items
        completed: Count of completed items
        paused: Count of paused items
        dropped: Count of dropped items
        plan_to_read: Count of planned items
        size: Diameter of the chart in SVG units
        stroke_width: Width of the ring stroke
        
    Returns:
        SVG group element containing the donut chart
    """
    # Calculate total and handle edge case
    total = reading + completed + paused + dropped + plan_to_read
    if total == 0:
        return '<circle cx="60" cy="60" r="44" fill="none" stroke="#334155" stroke-width="12"/>'
    
    # Chart geometry
    radius = (size - stroke_width) / 2
    center = size / 2
    circumference = 2 * 3.14159 * radius
    
    # Define colors for each segment
    colors = ["#38bdf8", "#2dd4bf", "#fbbf24", "#fb7185", "#818cf8"]
    values = [reading, completed, paused, dropped, plan_to_read]
    
    # Build SVG segments
    segments: list[str] = []
    cumulative_percent = 0.0
    
    for i, (value, color) in enumerate(zip(values, colors)):
        if value == 0:
            continue
            
        # Calculate percentage and dash length
        percentage = value / total
        dash_length = percentage * circumference
        gap_length = circumference - dash_length
        
        # Calculate rotation offset (in degrees)
        rotation = cumulative_percent * 360
        
        # Create the circle segment with dash pattern
        # stroke-dasharray: [dash_length, gap_length]
        segment = f'''
        <circle cx="{center}" cy="{center}" r="{radius}" 
                fill="none" stroke="{color}" stroke-width="{stroke_width}"
                stroke-dasharray="{dash_length:.2f} {gap_length:.2f}"
                stroke-linecap="butt"
                transform="rotate({rotation - 90} {center} {center})"
                opacity="0.9"/>'''
        segments.append(segment)
        
        # Update cumulative percentage for next segment
        cumulative_percent += percentage
    
    # Add center text showing total
    center_text = f'<text x="{center}" y="{center + 4}" text-anchor="middle" fill="#f1f5f9" font-size="14" font-weight="700" font-family="system-ui, sans-serif">{total:,}</text>'
    center_label = f'<text x="{center}" y="{center + 18}" text-anchor="middle" fill="#94a3b8" font-size="9" font-family="system-ui, sans-serif">Total</text>'
    
    # Combine all elements
    return ''.join(segments) + center_text + center_label


def _generate_genre_tags(top_genres: list[tuple[str, int]], max_width: int = 300) -> str:
    """
    Generate pill-shaped tags for top genres.
    
    Unlike bars, tags are more compact and modern.
    They auto-wrap to multiple lines if needed.
    
    Args:
        top_genres: List of (genre_name, count) tuples
        max_width: Maximum width before wrapping (not used in simple version)
        
    Returns:
        SVG group element with genre tags
    """
    if not top_genres:
        return ""
    
    # Color palette for tags (vibrant neon colors)
    colors = ["#38bdf8", "#2dd4bf", "#fbbf24", "#fb7185", "#818cf8", "#a78bfa"]
    
    # Limit to top 6 genres for clean layout
    limited_genres = top_genres[:6]
    
    tags: list[str] = []
    x_pos = 0
    y_pos = 0
    row_height = 28
    tag_spacing = 8
    
    for i, (name, count) in enumerate(limited_genres):
        # Truncate very long names
        display_name = name[:15] + "…" if len(name) > 15 else name
        
        # Estimate tag width (rough approximation based on character count)
        tag_width = len(display_name) * 9 + 24  # ~9px per char + padding
        
        # Wrap to next line if exceeds max width
        if x_pos + tag_width > max_width and i > 0:
            x_pos = 0
            y_pos += row_height
        
        color = colors[i % len(colors)]
        
        # Create pill-shaped tag background
        tag_bg = f'<rect x="{x_pos}" y="{y_pos}" width="{tag_width}" height="22" rx="11" fill="{color}" opacity="0.15" stroke="{color}" stroke-width="1"/>'
        
        # Genre name text
        tag_text = f'<text x="{x_pos + tag_width/2}" y="{y_pos + 15}" text-anchor="middle" fill="{color}" font-size="10" font-weight="600" font-family="system-ui, sans-serif">{_escape_xml(display_name)}</text>'
        
        # Count badge (small circle with number)
        badge_x = x_pos + tag_width - 8
        badge_y = y_pos + 7
        count_badge = f'<circle cx="{badge_x}" cy="{badge_y}" r="9" fill="{color}"/><text x="{badge_x}" y="{badge_y + 3}" text-anchor="middle" fill="#0f172a" font-size="9" font-weight="700" font-family="system-ui, sans-serif">{count}</text>'
        
        tags.append(f'{tag_bg}{tag_text}{count_badge}')
        
        # Move x position for next tag
        x_pos += tag_width + tag_spacing
    
    return ''.join(tags)

def generate_svg(stats: LibraryStats, nickname: str) -> str:
    """
    Generate the complete SVG stats card with modern Cyber-Glass dashboard design.
    
    This is the main function of this module. It orchestrates all
    the helper functions to create a complete, beautiful SVG card.
    
    NEW DESIGN (2024): Asymmetric Dashboard Layout
    ===============================================
    - Left panel: User identity with avatar placeholder, hero stat, and donut chart
    - Right panel: Compact metric cards grid with chapters, volumes, score, rereads
    - Bottom: Pill-shaped genre tags and status/type summaries
    
    Args:
        stats: LibraryStats object containing all computed statistics
        nickname: User's display name
        
    Returns:
        Complete SVG document as a string
        
    Design decisions explained:
        1. Asymmetric layout (900x450): Modern dashboard aesthetic, more dynamic
        2. Deep ocean gradient: Professional yet vibrant (#0f172a → #1e293b)
        3. Neon accents: Sky blue, turquoise, amber for visual pop
        4. Glassmorphism cards: Semi-transparent with blur for depth
        5. Donut chart: Visual representation of reading activity mix
        6. Pill tags: Modern alternative to boring progress bars
        7. Ambient lighting: Blurred circles create atmospheric depth
    """
    # Define canvas dimensions - larger for dashboard layout
    width = 900
    height = 450
    
    # Initialize color palette
    colors = ColorPalette()
    
    # Calculate total for donut chart
    total_status = stats.reading + stats.completed + stats.paused + stats.dropped + stats.plan_to_read
    
    # Get today's date formatted nicely
    today = date.today().strftime("%b %d, %Y")
    
    # Format numbers for display - smart formatting (integers vs decimals)
    chapters_display = f"{stats.chapters:,.1f}" if stats.chapters % 1 != 0 else f"{int(stats.chapters):,}"
    volumes_display = f"{stats.volumes:,.1f}" if stats.volumes % 1 != 0 else f"{int(stats.volumes):,}"
    
    # Generate components
    donut_chart = _generate_donut_chart(
        stats.reading, stats.completed, stats.paused, 
        stats.dropped, stats.plan_to_read
    )
    genre_tags = _generate_genre_tags(stats.top_genres, max_width=380)
    
    # Build the complete SVG document
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- 
    MODERN CYBER-GLASS DASHBOARD DESIGN
    Generated by MangaBaka Stats Card (Python Edition)
  -->
  
  <defs>
    <!-- Deep ocean gradient background -->
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{colors.bg_dark}"/>
      <stop offset="100%" stop-color="{colors.bg_light}"/>
    </linearGradient>
    
    <!-- Neon accent gradients -->
    <linearGradient id="accent1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{colors.primary}"/>
      <stop offset="100%" stop-color="{colors.secondary}"/>
    </linearGradient>
    
    <linearGradient id="accent2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{colors.coral}"/>
      <stop offset="100%" stop-color="{colors.turquoise}"/>
    </linearGradient>
    
    <!-- Soft glow filter for text and elements -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- Glassmorphism blur effect -->
    <filter id="glassBlur">
      <feGaussianBlur in="SourceGraphic" stdDeviation="10"/>
    </filter>
    
    <!-- Subtle grid pattern -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ffffff" stroke-width="0.3" opacity="0.03"/>
    </pattern>
    
    <!-- Ambient light circles for depth -->
    <radialGradient id="ambient1">
      <stop offset="0%" stop-color="{colors.primary}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{colors.primary}" stop-opacity="0"/>
    </radialGradient>
    
    <radialGradient id="ambient2">
      <stop offset="0%" stop-color="{colors.coral}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{colors.coral}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  
  <!-- Background with gradient -->
  <rect width="{width}" height="{height}" fill="url(#bg)" rx="16"/>
  
  <!-- Grid overlay for texture -->
  <rect width="{width}" height="{height}" fill="url(#grid)" rx="16"/>
  
  <!-- Ambient lighting effects (large blurred circles) -->
  <circle cx="{width * 0.8}" cy="{height * 0.2}" r="180" fill="url(#ambient1)" filter="url(#glassBlur)"/>
  <circle cx="{width * 0.3}" cy="{height * 0.7}" r="150" fill="url(#ambient2)" filter="url(#glassBlur)"/>
  
  <!-- Decorative corner accents -->
  <rect x="0" y="0" width="140" height="4" fill="url(#accent1)" rx="2"/>
  <rect x="0" y="0" width="4" height="140" fill="url(#accent1)" rx="2"/>
  <rect x="{width-140}" y="{height-4}" width="140" height="4" fill="url(#accent2)" rx="2"/>
  <rect x="{width-4}" y="{height-140}" width="4" height="140" fill="url(#accent2)" rx="2"/>
  
  <!-- ========== LEFT PANEL: Identity & Activity Chart ========== -->
  <g transform="translate(40, 50)">
    <!-- Avatar circle placeholder -->
    <circle cx="40" cy="40" r="35" fill="#ffffff" opacity="0.08" stroke="{colors.primary}" stroke-width="2"/>
    <text x="40" y="50" text-anchor="middle" fill="{colors.text_primary}" font-size="32" font-weight="700" font-family="system-ui, sans-serif">{nickname[0].upper()}</text>
    
    <!-- Username -->
    <text x="0" y="95" fill="{colors.text_primary}" font-size="18" font-weight="700" font-family="system-ui, sans-serif" filter="url(#glow)">@{_escape_xml(nickname)}</text>
    <text x="0" y="115" fill="{colors.text_secondary}" font-size="11" font-family="system-ui, sans-serif">MangaBaka Statistics</text>
    
    <!-- Hero Stat: Total Entries -->
    <rect x="0" y="135" width="180" height="65" rx="12" fill="#ffffff" opacity="0.06" stroke="#ffffff" stroke-opacity="0.1"/>
    <text x="90" y="162" fill="{colors.primary}" font-size="36" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">{stats.total:,}</text>
    <text x="90" y="182" fill="{colors.text_secondary}" font-size="11" text-anchor="middle" font-family="system-ui, sans-serif" letter-spacing="0.5">TOTAL ENTRIES</text>
    
    <!-- Donut Chart: Activity Distribution -->
    <text x="0" y="230" fill="{colors.text_primary}" font-size="12" font-weight="600" font-family="system-ui, sans-serif" letter-spacing="0.5">ACTIVITY MIX</text>
    <g transform="translate(20, 245)">
      {donut_chart}
    </g>
    
    <!-- Chart legend -->
    <g transform="translate(0, 375)">
      <rect x="0" y="0" width="10" height="10" rx="2" fill="{colors.primary}"/><text x="16" y="9" fill="{colors.text_secondary}" font-size="9" font-family="system-ui, sans-serif">Reading</text>
      <rect x="60" y="0" width="10" height="10" rx="2" fill="{colors.turquoise}"/><text x="76" y="9" fill="{colors.text_secondary}" font-size="9" font-family="system-ui, sans-serif">Done</text>
      <rect x="110" y="0" width="10" height="10" rx="2" fill="{colors.amber}"/><text x="126" y="9" fill="{colors.text_secondary}" font-size="9" font-family="system-ui, sans-serif">Paused</text>
    </g>
  </g>
  
  <!-- ========== RIGHT PANEL: Metrics Grid ========== -->
  <g transform="translate(260, 50)">
    <!-- Top row: Chapters & Volumes -->
    <rect x="0" y="0" width="140" height="80" rx="12" fill="#ffffff" opacity="0.06" stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="70" y="28" fill="{colors.turquoise}" font-size="28" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">{chapters_display}</text>
    <text x="70" y="50" fill="{colors.text_secondary}" font-size="10" text-anchor="middle" font-family="system-ui, sans-serif">CHAPTERS</text>
    <text x="70" y="65" fill="{colors.text_muted}" font-size="9" text-anchor="middle" font-family="system-ui, sans-serif">Read</text>
    
    <rect x="155" y="0" width="140" height="80" rx="12" fill="#ffffff" opacity="0.06" stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="225" y="28" fill="{colors.amber}" font-size="28" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">{volumes_display}</text>
    <text x="225" y="50" fill="{colors.text_secondary}" font-size="10" text-anchor="middle" font-family="system-ui, sans-serif">VOLUMES</text>
    <text x="225" y="65" fill="{colors.text_muted}" font-size="9" text-anchor="middle" font-family="system-ui, sans-serif">Collected</text>
    
    <!-- Middle row: Score & Rereads -->
    <rect x="0" y="95" width="140" height="80" rx="12" fill="#ffffff" opacity="0.06" stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="70" y="123" fill="{colors.coral}" font-size="32" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">{stats.avg_rating}</text>
    <text x="70" y="145" fill="{colors.text_secondary}" font-size="10" text-anchor="middle" font-family="system-ui, sans-serif">AVG SCORE</text>
    <text x="70" y="160" fill="{colors.text_muted}" font-size="9" text-anchor="middle" font-family="system-ui, sans-serif">/ 10.0</text>
    
    <rect x="155" y="95" width="140" height="80" rx="12" fill="#ffffff" opacity="0.06" stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="225" y="123" fill="{colors.secondary}" font-size="28" font-weight="700" text-anchor="middle" font-family="system-ui, sans-serif">{stats.rereads:,}</text>
    <text x="225" y="145" fill="{colors.text_secondary}" font-size="10" text-anchor="middle" font-family="system-ui, sans-serif">REREADS</text>
    <text x="225" y="160" fill="{colors.text_muted}" font-size="9" text-anchor="middle" font-family="system-ui, sans-serif">Favorites</text>
    
    <!-- Currently Reading highlight -->
    <rect x="0" y="190" width="295" height="55" rx="12" fill="url(#accent1)" opacity="0.15" stroke="{colors.primary}" stroke-width="1"/>
    <text x="20" y="215" fill="{colors.text_primary}" font-size="11" font-weight="600" font-family="system-ui, sans-serif">CURRENTLY READING</text>
    <text x="275" y="215" fill="{colors.primary}" font-size="24" font-weight="700" text-anchor="end" font-family="system-ui, sans-serif">{stats.reading}</text>
    <text x="275" y="230" fill="{colors.text_secondary}" font-size="9" text-anchor="end" font-family="system-ui, sans-serif">titles in progress</text>
  </g>
  
  <!-- ========== BOTTOM SECTION: Genre Tags ========== -->
  <g transform="translate(40, 405)">
    <text x="0" y="0" fill="{colors.text_primary}" font-size="11" font-weight="600" font-family="system-ui, sans-serif" letter-spacing="0.5">FAVORITE GENRES</text>
    <g transform="translate(0, 12)">
      {genre_tags}
    </g>
  </g>
  
  <!-- ========== FOOTER ========== -->
  <text x="40" y="{height - 18}" fill="{colors.text_muted}" font-size="9" font-family="system-ui, sans-serif" opacity="0.5">MangaBaka - {today}</text>
  <text x="{width - 40}" y="{height - 18}" fill="{colors.text_muted}" font-size="9" text-anchor="end" font-family="system-ui, sans-serif" opacity="0.5">Auto-generated on GitHub Actions</text>
</svg>'''
    
    return svg_content
