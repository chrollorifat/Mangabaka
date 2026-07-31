"""
MangaBaka Stats Card Generator - API Client Module

This module handles all communication with the MangaBaka API.
It's responsible for:
- Fetching user profile information
- Fetching library entries with pagination support
- Error handling for network failures and API errors

We use the `requests` library for HTTP calls because it's:
- More Pythonic than urllib (standard library)
- Has better error handling
- Easier to read and maintain
"""

from typing import Any, Optional
import requests  # type: ignore[import-untyped]


class MangaBakaAPIError(Exception):
    """
    Custom exception for MangaBaka API errors.
    
    We create custom exceptions to:
    - Provide clearer error messages
    - Make debugging easier
    - Allow specific error handling in the calling code
    
    Example usage:
        try:
            api.fetch_profile()
        except MangaBakaAPIError as e:
            print(f"API failed: {e}")
    """
    pass


class MangaBakaClient:
    """
    Client class for interacting with the MangaBaka API.
    
    This class encapsulates all API-related logic, following the
    Single Responsibility Principle - it only handles API communication.
    
    Attributes:
        base_url (str): The base URL of the MangaBaka API
        api_key (str): The authentication API key
        session (requests.Session): A persistent session for efficiency
        
    Why use a class here?
        - Encapsulates related data (url, key) and methods
        - Allows reuse across multiple API calls
        - Makes testing easier (can mock the client)
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.mangabaka.org") -> None:
        """
        Initialize the MangaBaka API client.
        
        Args:
            api_key: Your MangaBaka API key (required for authentication)
            base_url: The API base URL (defaults to official API)
            
        Raises:
            ValueError: If api_key is empty or None
            
        Note on type hints:
            - `-> None` means this method doesn't return anything (it's a constructor)
            - We explicitly type all parameters for better IDE support
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty. Please set MANGABAKA_API_KEY.")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        
        # Create a session object for connection pooling
        # This is more efficient than making new connections for each request
        self.session = requests.Session()
        
        # Set up default headers that will be sent with every request
        self.session.headers.update({
            'x-api-key': self.api_key,
            'Accept': 'application/json',  # Tell API we want JSON responses
            'User-Agent': 'MangaBaka-Stats-Card/1.0'  # Identify our application
        })
    
    def _make_request(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Internal helper method to make HTTP GET requests.
        
        This method centralizes error handling so we don't repeat
        try-except blocks in every API call.
        
        Args:
            endpoint: The API endpoint (e.g., '/v1/my/profile')
            params: Optional query parameters as a dictionary
            
        Returns:
            The parsed JSON response as a dictionary
            
        Raises:
            MangaBakaAPIError: If the request fails for any reason
            
        Why the underscore prefix?
            In Python, a leading underscore indicates a "private" method
            (internal implementation detail). It's a convention, not enforced.
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Use timeout to prevent hanging indefinitely
            # 30 seconds is reasonable for most API calls
            response = self.session.get(url, params=params, timeout=30)
            
            # Raise an exception for HTTP error status codes (4xx, 5xx)
            # This is important: a 404 or 500 won't raise by default!
            response.raise_for_status()
            
            # Parse and return the JSON response
            return response.json()
            
        except requests.exceptions.Timeout:
            # Network took too long
            raise MangaBakaAPIError(
                f"Request to {endpoint} timed out after 30 seconds. "
                "Please check your internet connection."
            )
        except requests.exceptions.ConnectionError:
            # Network unreachable
            raise MangaBakaAPIError(
                f"Cannot connect to {endpoint}. "
                "Please check your internet connection or the API server status."
            )
        except requests.exceptions.HTTPError as e:
            # HTTP error status (4xx, 5xx)
            # Ensure status_code is an integer for comparison
            status_code = e.response.status_code if e.response else 0
            
            if status_code == 401:
                raise MangaBakaAPIError(
                    "Authentication failed (401). Your API key may be invalid or expired."
                )
            elif status_code == 403:
                raise MangaBakaAPIError(
                    "Access forbidden (403). Your API key may not have required permissions."
                )
            elif status_code >= 500:
                raise MangaBakaAPIError(
                    f"Server error ({status_code}). The MangaBaka API may be temporarily down."
                )
            else:
                raise MangaBakaAPIError(
                    f"HTTP error {status_code} when accessing {endpoint}"
                )
        except ValueError as e:
            # Invalid JSON response
            raise MangaBakaAPIError(
                f"Invalid JSON response from {endpoint}: {e}"
            )
    
    def fetch_profile(self) -> dict[str, Any]:
        """
        Fetch the current user's profile information.
        
        Returns:
            Dictionary containing profile data (nickname, etc.)
            
        Raises:
            MangaBakaAPIError: If the API request fails
            
        Example:
            client = MangaBakaClient("your-api-key")
            profile = client.fetch_profile()
            print(profile['data']['nickname'])
        """
        return self._make_request("/v1/my/profile")
    
    def fetch_library_page(self, page: int, limit: int = 100) -> dict[str, Any]:
        """
        Fetch a single page of library entries.
        
        The MangaBaka API uses pagination to limit response sizes.
        Each page can contain up to 100 entries by default.
        
        Args:
            page: Page number (1-indexed)
            limit: Number of entries per page (max 100)
            
        Returns:
            Dictionary containing 'data' (list of entries) and 'pagination' info
        """
        return self._make_request(
            "/v1/my/library",
            params={"limit": limit, "page": page}
        )
    
    def fetch_all_library_entries(self, max_pages: int = 10) -> list[dict[str, Any]]:
        """
        Fetch ALL library entries by automatically handling pagination.
        
        This method loops through pages until:
        - No more entries are returned
        - No 'next' page indicator exists
        - Maximum page limit is reached (safety measure)
        
        Args:
            max_pages: Maximum number of pages to fetch (default: 10 = 1000 entries)
                      This prevents infinite loops and excessive API calls
            
        Returns:
            List of all library entry dictionaries
            
        Why return a list instead of generator?
            - We need the full dataset for statistics computation
            - Makes the API simpler for callers
            - Memory usage is acceptable for typical manga libraries
        """
        all_entries: list[dict[str, Any]] = []
        current_page = 1
        
        while current_page <= max_pages:
            # Fetch one page of data
            response_data = self.fetch_library_page(current_page)
            
            # Extract the entries from the response
            # Use .get() for safe access - returns [] if 'data' key missing
            entries = response_data.get("data", [])
            
            # If no entries, we've reached the end
            if not entries:
                break
            
            # Add these entries to our collection
            all_entries.extend(entries)
            
            # Check if there's a next page
            pagination = response_data.get("pagination", {})
            if not pagination.get("next"):
                break  # No more pages
            
            current_page += 1
        
        return all_entries
    
    def close(self) -> None:
        """
        Close the session and release resources.
        
        This is good practice but not strictly required since
        the script exits shortly after. Included for completeness
        and to teach proper resource management.
        """
        self.session.close()
    
    def __enter__(self) -> 'MangaBakaClient':
        """Enable use as a context manager (with statement)."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Automatically close session when exiting context."""
        self.close()
