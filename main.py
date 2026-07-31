"""
MangaBaka Stats Card Generator - Main Entry Point

This is the main script that orchestrates the entire card generation process.
It's designed to be run by GitHub Actions but can also be tested locally.

Key Python concepts demonstrated:
- Environment variables with os.environ
- Type hints throughout
- Comprehensive error handling with try-except
- Logging for debugging and monitoring
- Modular architecture (separation of concerns)
- Context managers for resource management

How to run:
    Local testing:
        export MANGABAKA_API_KEY="your-key-here"
        python main.py
    
    GitHub Actions:
        The workflow sets MANGABAKA_API_KEY automatically
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Import our custom modules
from src.api_client import MangaBakaClient, MangaBakaAPIError
from src.stats_processor import compute_statistics, LibraryStats
from src.svg_generator import generate_svg


def _setup_logging() -> None:
    """
    Configure logging for the application.
    
    Why use logging instead of print()?
        - Provides different severity levels (DEBUG, INFO, WARNING, ERROR)
        - Can be configured to output to files, consoles, etc.
        - Professional standard for production code
        - Easy to adjust verbosity without changing code
    
    In GitHub Actions, logs appear in the workflow output.
    """
    # Configure the root logger
    # format specifies how each log message appears
    # level sets the minimum severity to display
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def _get_api_key() -> str:
    """
    Retrieve the API key from environment variables.
    
    Security best practices:
        - Never hardcode secrets in source code
        - Use environment variables or secret managers
        - Validate that required secrets are present before proceeding
    
    Returns:
        The API key string
        
    Raises:
        SystemExit: If the API key is not set
    """
    api_key = os.environ.get('MANGABAKA_API_KEY', '')
    
    if not api_key or not api_key.strip():
        # Log an error message before exiting
        logging.error(
            "MANGABAKA_API_KEY environment variable is not set.\n"
            "Please set it in your GitHub repository secrets:\n"
            "  1. Go to Settings → Secrets and variables → Actions\n"
            "  2. Click 'New repository secret'\n"
            "  3. Name: MANGABAKA_API_KEY, Value: your-api-key"
        )
        # Exit with code 1 to indicate failure
        # GitHub Actions will mark the workflow as failed
        sys.exit(1)
    
    return api_key.strip()


def _get_nickname(client: MangaBakaClient) -> str:
    """
    Fetch the user's nickname from their profile.
    
    Args:
        client: The MangaBaka API client
        
    Returns:
        The user's nickname, or 'User' as fallback
        
    Note:
        We handle errors gracefully here - if we can't fetch the profile,
        we use a default name instead of failing completely.
    """
    try:
        logging.info("Fetching user profile...")
        profile_data = client.fetch_profile()
        
        # Safely extract the nickname from nested data
        # Using .get() prevents KeyError if keys are missing
        data = profile_data.get('data', {})
        nickname = data.get('nickname') or data.get('preferred_username') or 'User'
        
        logging.info(f"Found user: {nickname}")
        return nickname
        
    except MangaBakaAPIError as e:
        # Log warning but don't fail - we'll use default name
        logging.warning(f"Could not fetch profile: {e}. Using default name.")
        return 'User'


def _ensure_directory(directory: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path object representing the directory
        
    Why use pathlib.Path?
        - Modern Python (3.4+) way to handle file paths
        - Cross-platform (works on Windows, macOS, Linux)
        - More intuitive than os.path
        - Provides useful methods like .exists(), .mkdir()
    """
    if not directory.exists():
        # mkdir with parents=True creates parent directories if needed
        # exist_ok=True prevents error if directory already exists
        directory.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {directory}")


def _write_svg_file(svg_content: str, output_path: Path) -> None:
    """
    Write the SVG content to a file.
    
    Args:
        svg_content: The SVG string to write
        output_path: Where to save the file
        
    Note on encoding:
        We explicitly use UTF-8 encoding to ensure special characters
        (like Japanese text) are saved correctly.
    """
    # Open file in write mode with UTF-8 encoding
    # Using 'with' statement ensures file is properly closed even if error occurs
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    logging.info(f"SVG written to: {output_path}")


def main() -> None:
    """
    Main function that orchestrates the entire card generation process.
    
    Process flow:
        1. Get and validate API key
        2. Fetch user profile for nickname
        3. Fetch all library entries
        4. Compute statistics from entries
        5. Generate SVG card
        6. Save SVG to dist/ directory
        7. Also copy to root for convenience
    
    Error handling:
        - Catches API errors and provides helpful messages
        - Catches file I/O errors
        - Exits with appropriate codes for CI/CD
    """
    # Step 0: Setup
    _setup_logging()
    logging.info("=" * 50)
    logging.info("MangaBaka Stats Card Generator")
    logging.info("=" * 50)
    
    # Step 1: Get API key
    api_key = _get_api_key()
    
    # Step 2: Create API client using context manager
    # The 'with' statement ensures resources are cleaned up
    try:
        with MangaBakaClient(api_key) as client:
            # Step 3: Get user's nickname
            nickname = _get_nickname(client)
            
            # Step 4: Fetch all library entries
            logging.info("Fetching library entries...")
            entries = client.fetch_all_library_entries(max_pages=10)
            logging.info(f"Found {len(entries)} library entries")
            
            # Step 5: Compute statistics
            logging.info("Computing statistics...")
            stats = compute_statistics(entries)
            
            # Log some summary info
            logging.info(
                f"Stats computed: {stats.total} total, "
                f"{stats.chapters} chapters, "
                f"{stats.avg_rating} avg rating"
            )
            
            # Step 6: Generate SVG
            logging.info("Generating SVG card...")
            svg_content = generate_svg(stats, nickname)
            
            # Step 7: Determine output paths
            # __file__ is the path to this script
            # .parent gives us the directory containing this script
            script_dir = Path(__file__).parent
            dist_dir = script_dir / 'dist'
            dist_output = dist_dir / 'card.svg'
            root_output = script_dir / 'card.svg'
            
            # Step 8: Ensure output directory exists
            _ensure_directory(dist_dir)
            
            # Step 9: Write SVG files
            _write_svg_file(svg_content, dist_output)
            _write_svg_file(svg_content, root_output)
            
            # Step 10: Success!
            logging.info("=" * 50)
            logging.info("✓ Card generated successfully!")
            logging.info(f"  - Dist folder: {dist_output}")
            logging.info(f"  - Root folder: {root_output}")
            logging.info("=" * 50)
            
    except MangaBakaAPIError as e:
        # Handle API-specific errors
        logging.error(f"API Error: {e}")
        logging.error("Please check your API key and network connection.")
        sys.exit(1)
        
    except IOError as e:
        # Handle file system errors
        logging.error(f"File I/O Error: {e}")
        logging.error("Please check disk space and file permissions.")
        sys.exit(1)
        
    except Exception as e:
        # Catch-all for any unexpected errors
        # This ensures we always have some error output
        logging.exception(f"Unexpected error: {e}")
        sys.exit(1)


# This idiom ensures main() only runs when this file is executed directly,
# not when it's imported as a module (useful for testing).
if __name__ == '__main__':
    main()
