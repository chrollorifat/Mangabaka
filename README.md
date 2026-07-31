# MangaBaka Stats Card

A dynamic SVG stats card for your MangaBaka library, deployable on GitHub Pages with automatic daily updates.

![Demo](https://via.placeholder.com/850x420/0f0f1a/ffffff?text=MangaBaka+Stats+Card+Preview)

## Features

- **Total library entries** - See your complete manga collection size
- **Chapters & volumes read** - Track your reading progress
- **Average rating** - View your rating patterns
- **Status distribution** - Visual breakdown of Reading, Completed, Paused, Dropped, Plan to Read
- **Media type breakdown** - Manga, Manhwa, Manhua, Novel statistics
- **Top 5 genres & tags** - Discover your reading preferences
- **Auto-updates daily** - Scheduled GitHub Actions keep your stats fresh
- **Beautiful SVG design** - Gradient backgrounds, glow effects, and modern styling

## Quick Start

### Step 1: Fork This Repository

Click the "Fork" button at the top right of this repository to create your own copy.

### Step 2: Get Your MangaBaka API Key

1. Go to [MangaBaka](https://mangabaka.org)
2. Log in to your account
3. Navigate to **Account Settings** → **API**
4. Copy your API key

### Step 3: Add API Key as GitHub Secret

1. Go to your forked repository on GitHub
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret** button
5. Enter the following:
   - **Name**: `MANGABAKA_API_KEY`
   - **Value**: Paste your API key from Step 2
6. Click **Add secret**

### Step 4: Enable GitHub Pages

1. Still in your repository **Settings**
2. In the left sidebar, click **Pages**
3. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions** (recommended)
4. GitHub will automatically configure the rest

### Step 5: Trigger First Build

1. Click on the **Actions** tab in your repository
2. You may see a message about workflows needing permission - click **I understand my workflows, go ahead and enable them**
3. Click on the **Deploy to GitHub Pages** workflow
4. Click **Run workflow** dropdown → **Run workflow**
5. Wait ~1 minute for the deployment to complete
6. When you see a green checkmark ✓, your card is ready!

### Step 6: Access Your Card

Your stats card will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg
```

Replace `YOUR_USERNAME` with your GitHub username and `YOUR_REPO_NAME` with your repository name (usually `mangabaka-stats-card`).

## Usage Examples

### GitHub Profile README

Add this to your profile's `README.md`:

```markdown
![MangaBaka Stats](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg)
```

### AniList Bio

```markdown
![MangaBaka Stats](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg)
```

### Website or Forum

```html
<img src="https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg" alt="MangaBaka Stats" />
```

### Discord (in embeds or bots that support images)

```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg
```

### Markdown Links

```markdown
[![MangaBaka Stats](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg)](https://mangabaka.org/u/YOUR_USERNAME)
```

## Project Structure

```
mangabaka-stats-card/
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions workflow for auto-deployment
├── build.js                # Build script that fetches data and generates SVG
├── dist/
│   └── card.svg            # Generated stats card (output directory)
├── card.svg                # Generated stats card (also copied to root)
├── package.json            # Project configuration
├── .gitignore              # Git ignore rules
├── .nojekyll               # Prevents Jekyll processing on GitHub Pages
└── README.md               # This file
```

## How It Works

1. **GitHub Actions** runs the deployment workflow:
   - On every push to the `main` branch
   - Daily at midnight UTC (configurable)
   - Manually via the Actions tab

2. The **build script** (`build.js`) executes:
   - Fetches your profile information from MangaBaka API
   - Retrieves all your library entries (up to 1000)
   - Computes statistics (totals, averages, distributions)
   - Generates a beautiful SVG card with your data

3. The generated card is deployed to **GitHub Pages** for public access

4. Your card URL can be embedded anywhere that supports images

## Customization

### Change Update Frequency

Edit `.github/workflows/deploy.yml` to modify the cron schedule:

```yaml
schedule:
  # Run daily at 00:00 UTC (default)
  - cron: '0 0 * * *'
  
  # Run every 6 hours (uncomment to use)
  # - cron: '0 */6 * * *'
  
  # Run weekly on Sundays at midnight (uncomment to use)
  # - cron: '0 0 * * 0'
```

Cron syntax: `minute hour day month weekday`

### Modify Card Design

Edit the `generateSVG()` function in `build.js` to customize:

- **Colors**: Change gradient stops, bar colors, text colors
- **Layout**: Adjust positioning, sizes, spacing
- **Typography**: Modify font sizes, weights, families
- **Content**: Add new statistics, remove existing ones
- **Effects**: Adjust glow, opacity, shadows

Example color change:
```javascript
// Find this line in build.js
const colors = ['#FF6B9D', '#C44569', '#F8B500', '#4ECDC4', '#556270'];
// Replace with your preferred colors
const colors = ['#yourColor1', '#yourColor2', ...];
```

### Increase Entry Limit

By default, the script fetches up to 1000 entries (10 pages × 100 per page). To increase:

Edit `build.js`, line 36:
```javascript
if (page > 10) break; // Change 10 to a higher number
```

⚠️ **Warning**: Higher limits may cause longer build times or API rate limiting.

## Troubleshooting

### Build Fails with "MANGABAKA_API_KEY environment variable is not set"

**Solution:**
- Verify you added the secret correctly
- Go to **Settings** → **Secrets and variables** → **Actions**
- Ensure the secret name is exactly `MANGABAKA_API_KEY` (case-sensitive)
- Check that the value doesn't have extra spaces

### API Returns 401 Unauthorized

**Causes:**
- Invalid or expired API key
- API key doesn't have proper permissions

**Solution:**
1. Go to MangaBaka → Account Settings → API
2. Generate a new API key
3. Update the GitHub secret with the new key
4. Re-run the workflow

### Card Shows Empty or Zero Values

**Possible causes:**
- Your MangaBaka library is empty
- API key has incorrect permissions
- Network issue during build

**Solution:**
1. Verify your library has entries on MangaBaka
2. Check GitHub Actions logs for specific errors
3. Try regenerating your API key

### GitHub Pages Not Updating

**Solutions:**
1. Check **Actions** tab for workflow status
2. Look for red X (failed) or yellow circle (running)
3. Click on the failed workflow to see error details
4. Clear browser cache: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
5. Wait a few minutes for GitHub Pages to propagate

### Workflow Doesn't Run Automatically

**Solution:**
1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Save changes
4. Manually trigger a workflow run

### Rate Limiting Issues

If you hit MangaBaka API rate limits:

1. Reduce update frequency in `deploy.yml`
2. Decrease the page limit in `build.js`
3. Contact MangaBaka support for higher limits

## Manual Build (Local Testing)

Test the card generation locally before pushing:

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Set your API key as environment variable
export MANGABAKA_API_KEY="your-api-key-here"

# Run the build
npm run build

# The card.svg file will be generated
# Open it in a browser to preview
open card.svg  # macOS
xdg-open card.svg  # Linux
start card.svg  # Windows
```

## Privacy Notes

- Your API key is stored securely as a GitHub secret
- The key is only used during the build process
- The generated SVG contains only public statistics
- No sensitive data is exposed in the card
- GitHub Actions logs are visible only to repository collaborators

## API Reference

### MangaBaka Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/my/profile` | GET | Fetch user profile (nickname, avatar, etc.) |
| `/v1/my/library` | GET | Fetch library entries (paginated, 100 per page) |

### Required Headers

```http
x-api-key: YOUR_API_KEY
```

### Response Format

The build script handles pagination automatically and aggregates all entries.

## Contributing

Feel free to:
- Fork and customize the card design
- Submit pull requests with improvements
- Report bugs or suggest features
- Share your customized versions

## License

MIT License - Feel free to modify, distribute, and use in your projects!

## Support

If you encounter issues:

1. **Check the logs**: Go to **Actions** tab → Click on workflow → Review output
2. **Review troubleshooting**: See the [Troubleshooting](#troubleshooting) section above
3. **Verify API key**: Ensure your MangaBaka API key is valid and active
4. **Open an issue**: Create a new issue on this repository with details

## Credits

- Built for the MangaBaka community
- Inspired by GitHub Stats Card projects
- Made with ❤️ by manga readers, for manga readers

---

**マンガバカ (MangaBaka)** - Your manga tracking companion

*Last updated: $(date)*
