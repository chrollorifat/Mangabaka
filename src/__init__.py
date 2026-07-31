"""
MangaBaka Stats Card Generator - Source Package

This package contains all the core modules for generating MangaBaka stats cards:

- api_client: Handles communication with the MangaBaka API
- stats_processor: Processes library data into statistics
- svg_generator: Creates the SVG visualization

Example usage:
    from src.api_client import MangaBakaClient
    from src.stats_processor import compute_statistics
    from src.svg_generator import generate_svg
    
    with MangaBakaClient(api_key) as client:
        entries = client.fetch_all_library_entries()
        stats = compute_statistics(entries)
        svg = generate_svg(stats, "Username")
"""

__version__ = "1.0.0"
__author__ = "MangaBaka Community"

# Export main classes and functions for easier imports
from src.api_client import MangaBakaClient, MangaBakaAPIError
from src.stats_processor import LibraryStats, compute_statistics
from src.svg_generator import generate_svg

__all__ = [
    "MangaBakaClient",
    "MangaBakaAPIError",
    "LibraryStats",
    "compute_statistics",
    "generate_svg",
]
