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
    
    # Color palette for the bars (cycled if more than 5 genres)
    colors: list[str] = ['#FF6B9D', '#C44569', '#F8B500', '#4ECDC4', '#556270']
    
    # Get the maximum count for scaling (first item since it's sorted)
    max_count = top_genres[0][1] if top_genres else 1
    
    # Build each bar's SVG
    bars: list[str] = []
    
    for i, (name, count) in enumerate(top_genres):
        # Calculate bar width relative to max (max width = 120 units)
        bar_width = (count / max_count) * 120 if max_count > 0 else 0
        
        # Select color (cycle through palette using modulo)
        color = colors[i % len(colors)]
        
        # Vertical position based on index
        y_position = i * 18
        
        # Create the SVG elements for this genre
        # We use escaped name to handle special characters safely
        bar_svg = f'''
      <text x="0" y="{y_position}" fill="#a0a0b0" font-size="11" font-family="system-ui, sans-serif">{_escape_xml(name)}</text>
      <rect x="80" y="{y_position - 8}" width="{bar_width:.2f}" height="6" rx="3" fill="{color}" opacity="0.85"/>
      <text x="{85 + bar_width:.2f}" y="{y_position}" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">{count}</text>
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
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">{label}</text>
      <g transform="translate(60, 6)">
        <rect width="140" height="6" rx="3" fill="#ffffff" opacity="0.08"/>
        {_generate_progress_bar(value, max_value, color)}
      </g>
      <text x="210" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">{value}</text>
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
      <text x="0" y="12" fill="#a0a0b0" font-size="10" font-family="system-ui, sans-serif">{label}</text>
      <g transform="translate(60, 6)">
        <rect width="100" height="6" rx="3" fill="#ffffff" opacity="0.08"/>
        {_generate_progress_bar(value, max_value, color)}
      </g>
      <text x="170" y="12" fill="#d0d0e0" font-size="10" font-family="system-ui, sans-serif">{value}</text>
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
    """
    # Define canvas dimensions
    width = 850
    height = 420
    
    # Calculate maximum values for progress bar scaling
    # Using max() with fallback to 1 to prevent division by zero
    max_state = max(stats.reading, stats.completed, stats.paused, 
                    stats.dropped, stats.plan_to_read, 1)
    max_type = max(stats.manga, stats.manhwa, stats.manhua, stats.novel, 1)
    
    # Get today's date formatted nicely
    # strftime formats the date object as a string
    today = date.today().strftime("%B %d, %Y")
    
    # Generate the genre bars HTML
    genre_bars_svg = _generate_genre_bars(stats.top_genres)
    
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
    <!-- Background gradient: dark purple/blue theme -->
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f0f1a"/>
      <stop offset="50%" stop-color="#1a1a2e"/>
      <stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    
    <!-- Accent gradient: pink to red -->
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6B9D"/>
      <stop offset="100%" stop-color="#C44569"/>
    </linearGradient>
    
    <!-- Glow filter for text effects -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- Subtle dot pattern overlay -->
    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#ffffff" opacity="0.03"/>
    </pattern>
  </defs>

  <!-- Background layer -->
  <rect width="{width}" height="{height}" fill="url(#bg)" rx="12"/>
  
  <!-- Dot pattern overlay for texture -->
  <rect width="{width}" height="{height}" fill="url(#dots)" rx="12"/>
  
  <!-- Top accent bar -->
  <rect x="0" y="0" width="{width}" height="3" fill="url(#accent)" rx="1.5"/>

  <!-- Header Section -->
  <text x="30" y="45" fill="#ffffff" font-size="22" font-weight="700" 
        font-family="system-ui, sans-serif" filter="url(#glow)">
    {_escape_xml(nickname)}'s MangaBaka Stats
  </text>
  <text x="30" y="65" fill="#FF6B9D" font-size="12" font-family="system-ui, sans-serif" opacity="0.8">
    Library Overview • Updated {today}
  </text>

  <!-- Stats Cards Row (5 cards) -->
  <g transform="translate(30, 90)">
    <!-- Total Entries Card -->
    <rect x="0" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" 
          stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="55" y="25" fill="#FF6B9D" font-size="24" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.total}</text>
    <text x="55" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" 
          font-family="system-ui, sans-serif">Total Entries</text>

    <!-- Chapters Read Card -->
    <rect x="125" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" 
          stroke="#ffffff" stroke-opacity="0.06"/>
    <!-- Format chapters to max 1 decimal place to prevent overflow -->
    <!-- Using :.1f ensures at most one decimal (e.g., 1234.5 or 1234) -->
    <!-- The comma adds thousands separator for readability -->
    <text x="180" y="25" fill="#4ECDC4" font-size="24" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.chapters:,.1f}</text>
    <text x="180" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" 
          font-family="system-ui, sans-serif">Chapters Read</text>

    <!-- Volumes Read Card -->
    <rect x="250" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" 
          stroke="#ffffff" stroke-opacity="0.06"/>
    <!-- Format volumes to max 1 decimal place to prevent overflow -->
    <text x="305" y="25" fill="#F8B500" font-size="24" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.volumes:,.1f}</text>
    <text x="305" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" 
          font-family="system-ui, sans-serif">Volumes Read</text>

    <!-- Average Rating Card -->
    <rect x="375" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" 
          stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="430" y="25" fill="#C44569" font-size="24" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.avg_rating}</text>
    <text x="430" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" 
          font-family="system-ui, sans-serif">Avg Rating ({stats.rated})</text>

    <!-- Rereads Card -->
    <rect x="500" y="0" width="110" height="70" rx="8" fill="#ffffff" opacity="0.04" 
          stroke="#ffffff" stroke-opacity="0.06"/>
    <text x="555" y="25" fill="#A8E6CF" font-size="24" font-weight="700" 
          text-anchor="middle" font-family="system-ui, sans-serif">{stats.rereads}</text>
    <text x="555" y="45" fill="#a0a0b0" font-size="11" text-anchor="middle" 
          font-family="system-ui, sans-serif">Rereads</text>
  </g>

  <!-- Status Distribution Section (Left Column) -->
  <g transform="translate(30, 185)">
    <text x="0" y="0" fill="#ffffff" font-size="13" font-weight="600" 
          font-family="system-ui, sans-serif">Status Distribution</text>

    {_generate_status_bar_row("Reading", stats.reading, max_state, "#4ECDC4", 15)}
    {_generate_status_bar_row("Completed", stats.completed, max_state, "#A8E6CF", 35)}
    {_generate_status_bar_row("Paused", stats.paused, max_state, "#F8B500", 55)}
    {_generate_status_bar_row("Dropped", stats.dropped, max_state, "#FF6B9D", 75)}
    {_generate_status_bar_row("Plan to Read", stats.plan_to_read, max_state, "#DCEDC1", 95)}
  </g>

  <!-- Media Types Section (Middle Column) -->
  <g transform="translate(280, 185)">
    <text x="0" y="0" fill="#ffffff" font-size="13" font-weight="600" 
          font-family="system-ui, sans-serif">Media Types</text>

    {_generate_type_bar_row("Manga", stats.manga, max_type, "#FFAAA5", 15)}
    {_generate_type_bar_row("Manhwa", stats.manhwa, max_type, "#A8E6CF", 35)}
    {_generate_type_bar_row("Manhua", stats.manhua, max_type, "#FFD3B6", 55)}
    {_generate_type_bar_row("Novel", stats.novel, max_type, "#DCEDC1", 75)}
  </g>

  <!-- Top Genres Section (Right Column) -->
  <g transform="translate(500, 185)">
    <text x="0" y="0" fill="#ffffff" font-size="13" font-weight="600" 
          font-family="system-ui, sans-serif">Top Genres</text>
    <g transform="translate(0, 18)">
      {genre_bars_svg}
    </g>
  </g>

  <!-- Footer -->
  <text x="{width - 30}" y="{height - 15}" fill="#555570" font-size="10" 
        text-anchor="end" font-family="system-ui, sans-serif">
    mangabaka.org • Generated dynamically
  </text>

  <!-- Japanese branding -->
  <text x="30" y="{height - 15}" fill="#FF6B9D" font-size="10" font-weight="600" 
        font-family="system-ui, sans-serif" opacity="0.6">
    マンガバカ
  </text>
</svg>'''
    
    return svg_content
