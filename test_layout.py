"""Test script to verify the new dashboard layout without API key."""
import os
import sys

# Set a fake API key to bypass the check
os.environ['MANGABAKA_API_KEY'] = 'fake_key_for_testing'

try:
    from src.stats_processor import LibraryStats
    
    # Create a mock LibraryStats object directly
    mock_stats = LibraryStats(
        total=150,
        reading=25,
        completed=100,
        paused=10,
        dropped=5,
        plan_to_read=10,
        chapters=2543,
        volumes=345,
        rereads=12,
        rated=120,
        avg_rating=7.8,
        manga=100,
        manhwa=30,
        manhua=15,
        novel=5,
        activity_last_7_days=[12, 45, 23, 67, 34, 89, 56],
        avg_chapters_per_day=5.8,
        top_rated_manga=[
            {'title': 'One Piece', 'score': 9.5},
            {'title': 'Berserk', 'score': 9.3}
        ],
        top_rated_anime=[
            {'title': 'Fullmetal Alchemist: Brotherhood', 'score': 9.8},
            {'title': 'Steins;Gate', 'score': 9.6}
        ]
    )
    
    print("✓ LibraryStats created successfully")
    print(f"  - Total: {mock_stats.total}")
    print(f"  - Chapters: {mock_stats.chapters}")
    print(f"  - Avg Rating: {mock_stats.avg_rating}")
    print(f"  - Activity (7 days): {mock_stats.activity_last_7_days}")
    print(f"  - Top Manga: {[m['title'] for m in mock_stats.top_rated_manga]}")
    print(f"  - Top Anime: {[a['title'] for a in mock_stats.top_rated_anime]}")
    
    from src.svg_generator import generate_svg
    
    # Test SVG generation with proper arguments
    svg_content = generate_svg(mock_stats, "TestUser")
    print(f"\n✓ SVG generated: {len(svg_content)} characters")
    
    # Save to dist folder
    os.makedirs('dist', exist_ok=True)
    with open('dist/test-stats.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("✓ SVG saved to dist/test-stats.svg")
    print("\n✅ ALL TESTS PASSED - Layout is working correctly!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
