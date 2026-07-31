# MangaBaka Stats Card (Python Edition)

A dynamic SVG stats card for your MangaBaka library, built with Python and deployable on GitHub Pages with automatic daily updates.

![Demo](https://chrollorifat.github.io/Mangabaka/card.svg)

## 🎯 Project Overview

This project demonstrates **modern Python best practices** while creating a useful tool:
- ✅ Type hints throughout (Python 3.11+)
- ✅ Modular architecture with separation of concerns
- ✅ Comprehensive error handling
- ✅ PEP 8 compliant code
- ✅ Extensive documentation and comments
- ✅ Production-ready patterns

---

## 📚 Learning Guide: Python Concepts Used

This project is designed to be educational. Here are the key Python concepts you'll learn:

### 1. **Type Hints** (`typing` module)

Type hints make code more readable and help catch errors early:

```python
# Before (no types - unclear what this returns)
def fetch_profile():
    ...

# After (clear return type)
def fetch_profile(self) -> dict[str, Any]:
    """Fetch user profile data."""
    ...
```

**Why use type hints?**
- IDE autocomplete works better
- Catches bugs before runtime (with mypy)
- Documents function behavior
- Makes refactoring safer

### 2. **Dataclasses** (`dataclasses` module)

Dataclasses reduce boilerplate for data containers:

```python
from dataclasses import dataclass

@dataclass
class LibraryStats:
    total: int = 0
    chapters: int = 0
    avg_rating: float = 0.0
    top_genres: list[tuple[str, int]] = field(default_factory=list)
```

**Benefits:**
- Auto-generates `__init__`, `__repr__`, etc.
- Clear structure for data
- Type-safe and IDE-friendly

### 3. **Context Managers** (`with` statement)

Context managers ensure proper resource cleanup:

```python
# The session is automatically closed after use
with MangaBakaClient(api_key) as client:
    entries = client.fetch_all_library_entries()
# Session closed here, even if an error occurred
```

**Why use context managers?**
- Prevents resource leaks
- Cleaner than try/finally
- Professional pattern for files, network connections, etc.

### 4. **f-strings** (Formatted String Literals)

Modern string formatting (Python 3.6+):

```python
# Old way (hard to read)
svg = '<text>{}</text>'.format(nickname)

# New way (clear and concise)
svg = f'<text>{_escape_xml(nickname)}</text>'

# With expressions
svg = f'Width: {width}, Height: {height * 2}'

# Number formatting
svg = f'Chapters: {stats.chapters:,}'  # Adds commas: 1,234
```

### 5. **Pathlib** for File Paths

Modern path handling (better than `os.path`):

```python
from pathlib import Path

# Create paths intuitively
script_dir = Path(__file__).parent
output_file = script_dir / 'dist' / 'card.svg'

# Check existence
if output_file.exists():
    print("File exists!")

# Create directories
output_file.parent.mkdir(parents=True, exist_ok=True)
```

### 6. **Exception Handling**

Robust error handling with custom exceptions:

```python
class MangaBakaAPIError(Exception):
    """Custom exception for API errors."""
    pass

try:
    response = client.fetch_profile()
except MangaBakaAPIError as e:
    logging.error(f"API failed: {e}")
    sys.exit(1)
except IOError as e:
    logging.error(f"File error: {e}")
    sys.exit(1)
```

### 7. **Logging** (instead of print)

Professional logging for debugging and monitoring:

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Starting process...")      # Normal operation
logging.warning("Something unexpected")   # Warning but OK
logging.error("Something failed")         # Error occurred
logging.exception("Unexpected error")     # Error with stack trace
```

### 8. **Module Organization**

Clean separation of concerns:

```
src/
├── api_client.py      # API communication
├── stats_processor.py # Data processing
└── svg_generator.py   # SVG generation
main.py                # Entry point
```

**Why modular?**
- Easier to test individual components
- Clear responsibilities
- Reusable code
- Easier maintenance

---

## 🚀 Quick Start

### Step 1: Fork This Repository

Click the "Fork" button at the top right to create your own copy.

### Step 2: Get Your MangaBaka API Key

1. Go to [MangaBaka](https://mangabaka.org)
2. Log in to your account
3. Navigate to **Account Settings** → **API**
4. Copy your API key

### Step 3: Add API Key as GitHub Secret

1. Go to your forked repository on GitHub
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter:
   - **Name**: `MANGABAKA_API_KEY`
   - **Value**: Paste your API key
6. Click **Add secret**

### Step 4: Enable GitHub Pages

1. Still in **Settings**
2. Click **Pages** in the left sidebar
3. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions**

### Step 5: Trigger First Build

1. Click **Actions** tab
2. Enable workflows if prompted
3. Click **Deploy to GitHub Pages** workflow
4. Click **Run workflow** → **Run workflow**
5. Wait ~1 minute for deployment

### Step 6: Access Your Card

Your card will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg
```

---

## 📁 Project Structure

```
mangabaka-stats-card/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow (Python)
├── src/
│   ├── __init__.py             # Makes src a Python package
│   ├── api_client.py           # MangaBaka API communication
│   ├── stats_processor.py      # Statistics computation
│   └── svg_generator.py        # SVG card generation
├── dist/
│   └── card.svg                # Generated card (output)
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── .python-version             # Python version specification
├── .gitignore                  # Git ignore rules (Python-focused)
├── .nojekyll                   # Disable Jekyll processing
└── README.md                   # This file
```

### Architecture Explanation

**Why this structure?**

1. **`src/` directory**: Contains all source code modules
   - Separates library code from scripts
   - Makes imports cleaner (`from src.api_client import ...`)
   - Follows Python packaging conventions

2. **`api_client.py`**: Handles all HTTP communication
   - Single Responsibility Principle
   - Easy to mock for testing
   - Centralized error handling

3. **`stats_processor.py`**: Pure data processing
   - No side effects (doesn't write files or make network calls)
   - Easy to unit test
   - Reusable logic

4. **`svg_generator.py`**: Presentation layer
   - Separated from data processing
   - Easy to customize design without touching logic

5. **`main.py`**: Orchestration only
   - Thin wrapper that connects components
   - Handles environment setup and error reporting

---

## 🔧 Local Development

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export MANGABAKA_API_KEY="your-api-key-here"
# On Windows (PowerShell):
$env:MANGABAKA_API_KEY="your-api-key-here"

# Run the script
python main.py

# View the generated card
open card.svg  # macOS
xdg-open card.svg  # Linux
start card.svg  # Windows
```

### Running Tests (Future Enhancement)

```bash
# Install pytest for testing
pip install pytest

# Run tests
pytest
```

---

## 🎨 Customization

### Change Colors

Edit `src/svg_generator.py`:

```python
# Color palette for genre bars
colors: list[str] = ['#FF6B9D', '#C44569', '#F8B500', '#4ECDC4', '#556270']
# Replace with your colors:
colors = ['#yourColor1', '#yourColor2', ...]
```

### Modify Card Dimensions

In `src/svg_generator.py`:

```python
def generate_svg(stats: LibraryStats, nickname: str) -> str:
    width = 850  # Change width
    height = 420  # Change height
    ...
```

### Adjust Update Frequency

Edit `.github/workflows/deploy.yml`:

```yaml
schedule:
  # Daily at midnight UTC (default)
  - cron: '0 0 * * *'
  
  # Every 6 hours
  # - cron: '0 */6 * * *'
  
  # Weekly on Sundays
  # - cron: '0 0 * * 0'
```

### Increase Entry Limit

In `main.py`, modify the `max_pages` parameter:

```python
entries = client.fetch_all_library_entries(max_pages=10)  # 10 pages = 1000 entries
```

⚠️ **Warning**: Higher limits may cause longer build times or API rate limiting.

---

## 🐛 Troubleshooting

### "MANGABAKA_API_KEY environment variable is not set"

**Solution:**
1. Verify the secret is added correctly
2. Check spelling: must be exactly `MANGABAKA_API_KEY`
3. Ensure no extra spaces in the value
4. Re-run the workflow after adding the secret

### "Authentication failed (401)"

**Causes:**
- Invalid API key
- Expired API key

**Solution:**
1. Regenerate API key on MangaBaka
2. Update the GitHub secret
3. Re-run workflow

### "Request timed out"

**Possible causes:**
- Network issues
- MangaBaka API slow/down

**Solution:**
1. Wait and retry
2. Check MangaBaka status
3. Reduce `max_pages` if you have many entries

### Workflow Fails Silently

**Debug steps:**
1. Go to **Actions** tab
2. Click the failed workflow run
3. Expand the log output
4. Look for error messages

### Card Shows Default Name "User"

**Cause:** Profile fetch failed (non-critical error)

**Solution:**
1. Check workflow logs for warnings
2. Verify API key permissions
3. The card still works with default name

---

## 📖 Python Best Practices Demonstrated

### 1. **PEP 8 Style Guide**

- 4-space indentation
- Snake_case for functions/variables
- CamelCase for classes
- Maximum line length: 88 characters (Black formatter standard)

### 2. **Docstrings**

Every function has a docstring explaining:
- Purpose
- Parameters
- Return values
- Exceptions raised

```python
def compute_statistics(entries: list[dict[str, Any]]) -> LibraryStats:
    """
    Compute all statistics from library entries.
    
    Args:
        entries: List of library entry dictionaries
        
    Returns:
        LibraryStats object with computed values
    """
```

### 3. **Error Handling Hierarchy**

```python
# Specific exceptions first
except MangaBakaAPIError as e:
    ...
except IOError as e:
    ...
# General catch-all last
except Exception as e:
    ...
```

### 4. **Type Safety**

```python
# Explicit types for clarity
def _safe_get(dictionary: dict[str, Any], key: str, default: Any = None) -> Any:
    ...
```

### 5. **DRY Principle**

Reusable helper functions instead of repeated code:

```python
# Instead of repeating bar generation 5 times:
_generate_status_bar_row("Reading", stats.reading, max_state, "#4ECDC4", 15)
_generate_status_bar_row("Completed", stats.completed, max_state, "#A8E6CF", 35)
```

---

## 🔒 Security Notes

- **API keys are never committed** - stored as GitHub Secrets
- **Keys only used during build** - not exposed in generated SVG
- **HTTPS only** - all API calls use encrypted connections
- **Input sanitization** - XML escaping prevents injection attacks

---

## 📊 Performance Considerations

| Aspect | Implementation |
|--------|---------------|
| **HTTP** | Session reuse for connection pooling |
| **Pagination** | Automatic handling with max limit |
| **Memory** | Efficient data structures (dicts, lists) |
| **Dependencies** | Minimal (only `requests`) |
| **Build Time** | ~30-60 seconds typically |

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add unit tests
- [ ] Add more stat visualizations
- [ ] Support custom themes
- [ ] Add caching to reduce API calls
- [ ] Support multiple card sizes

---

## 📄 License

MIT License - Feel free to modify and distribute!

---

## 🙏 Credits

- Built for the MangaBaka community
- Inspired by GitHub Stats Card projects
- Made with ❤️ using modern Python

---

## 📚 Further Learning Resources

### Python Basics
- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

### Type Hints
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [mypy Documentation](https://mypy.readthedocs.io/)

### Best Practices
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Python Packaging User Guide](https://packaging.python.org/)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/actions)

---

**マンガバカ (MangaBaka)** - Your manga tracking companion

*Last updated: January 2025*
