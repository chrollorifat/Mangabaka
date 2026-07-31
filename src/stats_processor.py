"""
MangaBaka Stats Card Generator - Statistics Processor Module

This module handles all data processing and statistics computation.
It takes raw library entries and transforms them into meaningful statistics.

Key Python concepts demonstrated:
- Type hints with TypedDict for structured data
- Dataclasses for clean data containers
- Dictionary operations and comprehensions
- Safe handling of optional/missing data
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LibraryStats:
    """
    A dataclass to hold all computed statistics.
    
    Why use a dataclass?
        - Automatically generates __init__, __repr__, etc.
        - Provides clear structure for our statistics
        - Type-safe and IDE-friendly
        - More maintainable than a plain dictionary
    
    The frozen=True would make it immutable, but we don't use it here
    in case we need to modify stats later.
    """
    # Basic counts
    total: int = 0
    reading: int = 0
    completed: int = 0
    paused: int = 0
    dropped: int = 0
    plan_to_read: int = 0
    
    # Reading progress
    chapters: int = 0
    volumes: int = 0
    rereads: int = 0
    
    # Ratings
    rated: int = 0
    avg_rating: float = 0.0
    
    # Media types
    manga: int = 0
    manhwa: int = 0
    manhua: int = 0
    novel: int = 0
    
    # Content ratings
    safe: int = 0
    suggestive: int = 0
    erotica: int = 0
    pornographic: int = 0
    
    # Top items (lists of tuples: [(name, count), ...])
    top_genres: list[tuple[str, int]] = field(default_factory=list)
    top_tags: list[tuple[str, int]] = field(default_factory=list)


def _safe_get(dictionary: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary.
    
    This is a helper function to handle missing keys gracefully.
    While dict.get() exists, this makes the intent clearer in our context
    and allows us to add logging or validation later if needed.
    
    Args:
        dictionary: The dictionary to read from
        key: The key to look up
        default: Value to return if key is missing
        
    Returns:
        The value if key exists, otherwise the default
    """
    return dictionary.get(key, default)


def _count_by_field(entries: list[dict[str, Any]], field_name: str) -> dict[str, int]:
    """
    Count occurrences of each unique value for a given field.
    
    This is a reusable utility function that demonstrates:
    - Generic programming (works for any field)
    - Dictionary accumulation pattern
    - Handling nested data structures
    
    Args:
        entries: List of library entry dictionaries
        field_name: The field name to count (e.g., 'state', 'type')
        
    Returns:
        Dictionary mapping unique values to their counts
        
    Example:
        For field_name='state', might return:
        {'reading': 15, 'completed': 42, 'plan_to_read': 8}
    """
    counts: dict[str, int] = {}
    
    for entry in entries:
        # Get the value, skip if not present
        value = _safe_get(entry, field_name)
        if value is None:
            continue
        
        # Increment the count for this value
        # Using .get() with default 0 is a common Python idiom
        counts[value] = counts.get(value, 0) + 1
    
    return counts


def _count_nested_field(
    entries: list[dict[str, Any]], 
    parent_field: str, 
    child_field: str
) -> dict[str, int]:
    """
    Count occurrences of values in a nested field.
    
    Many MangaBaka fields are nested (e.g., entry['Series']['type']).
    This function handles that pattern safely.
    
    Args:
        entries: List of library entry dictionaries
        parent_field: The parent field name (e.g., 'Series')
        child_field: The child field to count (e.g., 'type')
        
    Returns:
        Dictionary mapping unique values to their counts
    """
    counts: dict[str, int] = {}
    
    for entry in entries:
        # Safely get the nested object
        parent_obj = _safe_get(entry, parent_field, {})
        if not isinstance(parent_obj, dict):
            continue
        
        # Get the child field value
        value = _safe_get(parent_obj, child_field)
        if value is None:
            continue
        
        counts[value] = counts.get(value, 0) + 1
    
    return counts


def _count_list_field(
    entries: list[dict[str, Any]], 
    parent_field: str, 
    list_field: str
) -> dict[str, int]:
    """
    Count occurrences of items in a list field within a nested object.
    
    Used for fields like genres and tags which are lists.
    
    Args:
        entries: List of library entry dictionaries
        parent_field: The parent field name (e.g., 'Series')
        list_field: The list field to iterate (e.g., 'genres')
        
    Returns:
        Dictionary mapping unique items to their counts
    """
    counts: dict[str, int] = {}
    
    for entry in entries:
        parent_obj = _safe_get(entry, parent_field, {})
        if not isinstance(parent_obj, dict):
            continue
        
        # Get the list, default to empty list
        items = _safe_get(parent_obj, list_field, [])
        if not isinstance(items, list):
            continue
        
        # Count each item in the list
        for item in items:
            if item:  # Skip empty strings/None
                counts[item] = counts.get(item, 0) + 1
    
    return counts


def _get_top_items(counts: dict[str, int], limit: int = 5) -> list[tuple[str, int]]:
    """
    Get the top N items by count, sorted in descending order.
    
    This demonstrates:
    - Sorting with a custom key
    - Dictionary.items() to get key-value pairs
    - List slicing
    
    Args:
        counts: Dictionary of {item: count}
        limit: Maximum number of items to return
        
    Returns:
        List of (item, count) tuples, sorted by count descending
    """
    # sorted() returns a new list
    # key=lambda x: x[1] means sort by the count (second element of tuple)
    # reverse=True gives us descending order (highest first)
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    # Return only the top N items
    return sorted_items[:limit]


def compute_statistics(entries: list[dict[str, Any]]) -> LibraryStats:
    """
    Compute all statistics from library entries.
    
    This is the main function of this module. It processes all entries
    and returns a structured statistics object.
    
    Args:
        entries: List of library entry dictionaries from the API
        
    Returns:
        LibraryStats object containing all computed statistics
        
    How it works:
        1. Count entries by status (reading, completed, etc.)
        2. Sum up chapters, volumes, and rereads
        3. Calculate average rating
        4. Count media types (manga, manhwa, etc.)
        5. Count content ratings
        6. Find top genres and tags
    """
    # Initialize counters
    total_entries = len(entries)
    
    # Count by status
    state_counts = _count_by_field(entries, 'state')
    
    # Count by media type (nested in Series object)
    type_counts = _count_nested_field(entries, 'Series', 'type')
    
    # Count by content rating (nested in Series object)
    content_counts = _count_nested_field(entries, 'Series', 'content_rating')
    
    # Count genres and tags (lists in Series object)
    genre_counts = _count_list_field(entries, 'Series', 'genres')
    tag_counts = _count_list_field(entries, 'Series', 'tags')
    
    # Calculate sums for numeric fields
    total_chapters = 0
    total_volumes = 0
    total_rereads = 0
    ratings: list[float] = []
    
    for entry in entries:
        # Use 0 as default for missing numeric fields
        # This is safer than None for arithmetic operations
        total_chapters += _safe_get(entry, 'progress_chapter', 0) or 0
        total_volumes += _safe_get(entry, 'progress_volume', 0) or 0
        total_rereads += _safe_get(entry, 'number_of_rereads', 0) or 0
        
        # Collect ratings for average calculation
        rating = _safe_get(entry, 'rating')
        if rating is not None:
            ratings.append(float(rating))
    
    # Calculate average rating
    # Using sum()/len() is more Pythonic than a manual loop
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0
    
    # Get top 5 genres and tags
    top_genres = _get_top_items(genre_counts, limit=5)
    top_tags = _get_top_items(tag_counts, limit=5)
    
    # Create and return the statistics object
    # Using keyword arguments for clarity
    return LibraryStats(
        total=total_entries,
        reading=state_counts.get('reading', 0),
        completed=state_counts.get('completed', 0),
        paused=state_counts.get('paused', 0),
        dropped=state_counts.get('dropped', 0),
        plan_to_read=state_counts.get('plan_to_read', 0),
        chapters=total_chapters,
        volumes=total_volumes,
        rereads=total_rereads,
        rated=len(ratings),
        avg_rating=avg_rating,
        manga=type_counts.get('manga', 0),
        manhwa=type_counts.get('manhwa', 0),
        manhua=type_counts.get('manhua', 0),
        novel=type_counts.get('novel', 0),
        safe=content_counts.get('safe', 0),
        suggestive=content_counts.get('suggestive', 0),
        erotica=content_counts.get('erotica', 0),
        pornographic=content_counts.get('pornographic', 0),
        top_genres=top_genres,
        top_tags=top_tags,
    )
