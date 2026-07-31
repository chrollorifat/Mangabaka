"""
MangaBaka Stats Card Generator - SVG Generator Module

This module handles the generation of the SVG stats card.
It takes computed statistics and creates a visually appealing SVG image.

Key Python concepts demonstrated:
- f-strings for string interpolation (modern Python 3.6+)
- Multi-line strings with triple quotes
- String formatting for XML/SVG generation
- Helper functions for DRY (Don't Repeat Yourself) principle
- Type hints for function parameters and return values

Why generate SVG instead of using a graphics library?
    - SVG is text-based, so no heavy dependencies like PIL/Pillow needed
    - Scales perfectly at any size
    - Easy to version control (it's just text)
    - GitHub Pages serves SVG natively
    - Smaller file sizes than PNG for this type of content
"""

from datetime import date
from typing import Any

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


def generate_svg(stats: LibraryStats, nickname: str) -> str:
    """
    Generate the complete SVG stats card.
    
    This is the main function of this module. It orchestrates all
    the helper functions to create a complete, beautiful SVG card.
    
    Args:
        stats: LibraryStats object containing all computed statistics
        nickname: User's display name
        
    Returns:
        Complete SVG document as a string
        
    Design decisions explained:
        1. Fixed dimensions (850x420): Consistent sizing for embedding
        2. Gradient background: Modern, visually appealing look
        3. Card layout: Organized into logical sections
        4. Color coding: Different colors for different data types
        5. Glow effects: Adds depth and visual interest
        6. Glassmorphism: Modern translucent card design with blur
        7. Compact layout: More info in less space with cleaner typography
    """
    # Define canvas dimensions - slightly taller for better spacing
    width = 850
    height = 400
    
    # Calculate maximum values for progress bar scaling
    # Using max() with fallback to 1 to prevent division by zero
    max_state = max(stats.reading, stats.completed, stats.paused, 
                    stats.dropped, stats.plan_to_read, 1)
    max_type = max(stats.manga, stats.manhwa, stats.manhua, stats.novel, 1)
    
    # Get today's date formatted nicely
    # strftime formats the date object as a string
    today = date.today().strftime("%b %d, %Y")
    
    # Generate the genre bars HTML
    genre_bars_svg = _generate_genre_bars(stats.top_genres)
    
    # Format numbers for display - concise formatting
    # Using :,.0f for integers with commas, :.1f for one decimal
    chapters_display = f"{stats.chapters:,.1f}" if stats.chapters % 1 != 0 else f"{int(stats.chapters):,}"
    volumes_display = f"{stats.volumes:,.1f}" if stats.volumes % 1 != 0 else f"{int(stats.volumes):,}"
    
    # Build the complete SVG document
    # Using triple-quoted string for multi-line literal content
    # and f-string interpolation for dynamic values
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- 
    SVG Definitions Section
    This defines reusable elements like gradients and filters
  -->
  <defs>
    <!-- Modern gradient: deep navy to soft purple -->
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0e27"/>
      <stop offset="50%" stop-color="#1a1f3a"/>
      <stop offset="100%" stop-color="#2d1b4e"/>
    </linearGradient>
    
    <!-- Vibrant accent gradient: coral to magenta -->
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff6b6b"/>
      <stop offset="100%" stop-color="#ee5aa7"/>
    </linearGradient>
    
    <!-- Soft glow filter for modern feel -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- Subtle grid pattern for texture -->
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#ffffff" stroke-width="0.5" opacity="0.04"/>
    </pattern>
    
    <!-- Glassmorphism card style -->
    <filter id="glass">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8"/>
    </filter>
  </defs>

  <!-- Background layer with modern gradient -->
  <rect width="{width}" height="{height}" fill="url(#bg)" rx="16"/>
  
  <!-- Grid pattern overlay for subtle texture -->
  <rect width="{width}" height="{height}" fill="url(#grid)" rx="16"/>
  
  <!-- Decorative corner accents -->
  <rect x="0" y="0" width="120" height="4" fill="url(#accent)" rx="2"/>
  <rect x="{width-120}" y="{height-4}" width="120" height="4" fill="url(#accent)" rx="2"/>

  <!-- Header Section - Cleaner, more compact -->
  <text x="35" y="42" fill="#ffffff" font-size="20" font-weight="700" 
        font-family="system-ui, -apple-system, sans-serif" filter="url(#glow)">
    {_escape_xml(nickname)}'s Manga Stats
  </text>
  <text x="35" y="60" fill="#ff8fa3" font-size="11" font-family="system-ui, sans-serif" opacity="0.9">
    {today} • mangabaka.org
  </text>

  <!-- Stats Cards Row (5 compact cards) -->
  <g transform="translate(35, 80)">
    <!-- Total Entries Card -->
    <rect x="0" y="0" width="95" height="60" rx="10" fill="#ffffff" opacity="0.06" 
          stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="47" y="22" fill="#ff6b6b" font-size="22" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.total:,}</text>
    <text x="47" y="42" fill="#a0a0c0" font-size="10" text-anchor="middle" 
          font-family="system-ui, sans-serif" opacity="0.85">Entries</text>

    <!-- Chapters Read Card -->
    <rect x="105" y="0" width="95" height="60" rx="10" fill="#ffffff" opacity="0.06" 
          stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="152" y="22" fill="#4ecdc4" font-size="22" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{chapters_display}</text>
    <text x="152" y="42" fill="#a0a0c0" font-size="10" text-anchor="middle" 
          font-family="system-ui, sans-serif" opacity="0.85">Chapters</text>

    <!-- Volumes Read Card -->
    <rect x="210" y="0" width="95" height="60" rx="10" fill="#ffffff" opacity="0.06" 
          stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="257" y="22" fill="#ffd93d" font-size="22" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{volumes_display}</text>
    <text x="257" y="42" fill="#a0a0c0" font-size="10" text-anchor="middle" 
          font-family="system-ui, sans-serif" opacity="0.85">Volumes</text>

    <!-- Average Rating Card -->
    <rect x="315" y="0" width="95" height="60" rx="10" fill="#ffffff" opacity="0.06" 
          stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="362" y="22" fill="#ee5aa7" font-size="22" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.avg_rating}</text>
    <text x="362" y="42" fill="#a0a0c0" font-size="10" text-anchor="middle" 
          font-family="system-ui, sans-serif" opacity="0.85">Rating</text>

    <!-- Rereads Card -->
    <rect x="420" y="0" width="95" height="60" rx="10" fill="#ffffff" opacity="0.06" 
          stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="467" y="22" fill="#95e1d3" font-size="22" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.rereads:,}</text>
    <text x="467" y="42" fill="#a0a0c0" font-size="10" text-anchor="middle" 
          font-family="system-ui, sans-serif" opacity="0.85">Rereads</text>
  </g>

  <!-- Status Distribution Section (Left Column) - More compact -->
  <g transform="translate(35, 160)">
    <text x="0" y="0" fill="#ffffff" font-size="12" font-weight="600" 
          font-family="system-ui, sans-serif" letter-spacing="0.5">STATUS</text>

    {_generate_status_bar_row("Reading", stats.reading, max_state, "#4ecdc4", 18)}
    {_generate_status_bar_row("Completed", stats.completed, max_state, "#95e1d3", 36)}
    {_generate_status_bar_row("Paused", stats.paused, max_state, "#ffd93d", 54)}
    {_generate_status_bar_row("Dropped", stats.dropped, max_state, "#ff6b6b", 72)}
    {_generate_status_bar_row("Planned", stats.plan_to_read, max_state, "#dda0dd", 90)}
  </g>

  <!-- Media Types Section (Middle Column) - More compact -->
  <g transform="translate(265, 160)">
    <text x="0" y="0" fill="#ffffff" font-size="12" font-weight="600" 
          font-family="system-ui, sans-serif" letter-spacing="0.5">TYPES</text>

    {_generate_type_bar_row("Manga", stats.manga, max_type, "#ffaaa5", 18)}
    {_generate_type_bar_row("Manhwa", stats.manhwa, max_type, "#95e1d3", 36)}
    {_generate_type_bar_row("Manhua", stats.manhua, max_type, "#ffd3b6", 54)}
    {_generate_type_bar_row("Novel", stats.novel, max_type, "#dda0dd", 72)}
  </g>

  <!-- Top Genres Section (Right Column) - Optimized layout -->
  <g transform="translate(480, 160)">
    <text x="0" y="0" fill="#ffffff" font-size="12" font-weight="600" 
          font-family="system-ui, sans-serif" letter-spacing="0.5">TOP GENRES</text>
    <g transform="translate(0, 16)">
      {genre_bars_svg}
    </g>
  </g>

  <!-- Minimal Footer -->
  <text x="35" y="{height - 18}" fill="#ff6b6b" font-size="9" font-weight="600" 
        font-family="system-ui, sans-serif" opacity="0.5">
    マンガバカ
  </text>
  <text x="{width - 35}" y="{height - 18}" fill="#6a6a8a" font-size="9" 
        text-anchor="end" font-family="system-ui, sans-serif">
    Auto-generated stats card
  </text>
</svg>'''
    
    return svg_content
