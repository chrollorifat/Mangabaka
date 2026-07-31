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

### Option 1: One-Click Deploy (Recommended)

1. **Fork this repository** to your GitHub account

2. **Get your MangaBaka API key**:
   - Go to [MangaBaka](https://mangabaka.org)
   - Log in to your account
   - Navigate to Account Settings → API
   - Copy your API key

3. **Add your API key as a secret**:
   - Go to your forked repository on GitHub
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `MANGABAKA_API_KEY`
   - Value: Your API key from step 2
   - Click **Add secret**

4. **Enable GitHub Pages**:
   - Go to **Settings** → **Pages**
   - Under **Build and deployment**:
     - Source: **GitHub Actions**
   - GitHub will automatically configure the rest

5. **Trigger the first build**:
   - Go to **Actions** tab
   - Click on **Deploy to GitHub Pages** workflow
   - Click **Run workflow** → **Run workflow**
   - Wait ~1 minute for deployment

6. **Access your card**:
   - Your card will be available at:
   ```
   https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg
   ```

### Option 2: Manual Deployment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Install dependencies (minimal, no external packages needed)
npm install

# Set environment variable and build
export MANGABAKA_API_KEY="your-api-key-here"
npm run build

# The card.svg file will be generated in the root and dist/ folder
```

Then push the `dist/` folder to a `gh-pages` branch or use any static hosting service.

## Usage

### Embed in GitHub Profile

Add this to your `README.md`:

```markdown
![MangaBaka Stats](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg)
```

### Embed in AniList Bio

```markdown
![MangaBaka Stats](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg)
```

### Embed in Websites/Forums

```html
<img src="https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg" alt="MangaBaka Stats" />
```

### Direct Link

Share your stats card URL directly:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/card.svg
```

## Project Structure

```
mangabaka-stats-card/
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions workflow for auto-deployment
├── api/
│   └── card/
│       └── route.ts        # Original Next.js API route (kept for reference)
├── build.js                # Static build script that generates the SVG
├── dist/
│   └── card.svg            # Generated stats card (output directory)
├── card.svg                # Generated stats card (also copied to root)
├── package.json            # Project configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This file
```

## How It Works

1. **GitHub Actions** runs the deployment workflow on every push to `main` and daily at midnight UTC
2. The **build script** (`build.js`) fetches your MangaBaka library data using the API key
3. Statistics are computed from your library entries
4. A beautiful **SVG card** is generated with your stats
5. The card is deployed to **GitHub Pages** for public access

## Customization

### Update Frequency

Edit `.github/workflows/deploy.yml` to change the update schedule:

```yaml
schedule:
  # Run daily at 00:00 UTC
  - cron: '0 0 * * *'
  
  # Run every 6 hours
  # - cron: '0 */6 * * *'
  
  # Run weekly on Sundays
  # - cron: '0 0 * * 0'
```

### Card Design

Modify the `generateSVG()` function in `build.js` to customize:
- Colors and gradients
- Layout and positioning
- Font sizes and styles
- Additional statistics

## Troubleshooting

### Build Fails

**Error: MANGABAKA_API_KEY environment variable is not set**
- Make sure you added the secret correctly in GitHub Settings → Secrets and variables → Actions
- Secret name must be exactly `MANGABAKA_API_KEY`

**API returns 401 Unauthorized**
- Your API key might be invalid or expired
- Generate a new key from MangaBaka settings

**Card shows empty data**
- Ensure your MangaBaka library has entries
- Check that your API key has proper permissions

### GitHub Pages Not Updating

- Go to **Actions** tab and check if the workflow completed successfully
- Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
- GitHub Pages may take a few minutes to propagate changes

### Rate Limiting

The build script limits fetching to 10 pages (1000 entries max) to avoid API rate limits. If you have more entries, consider:
- Increasing the limit in `build.js` (line 73)
- Running updates less frequently

## API Reference

### MangaBaka API Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `GET /v1/my/profile` | Fetch user profile information |
| `GET /v1/my/library` | Fetch library entries (paginated) |

### Required Headers

```
x-api-key: YOUR_API_KEY
```

## License

MIT License - Feel free to modify and distribute!

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review GitHub Actions logs for error details
3. Ensure your MangaBaka API key is valid
4. Open an issue on this repository

---

**Made with ❤️ for MangaBaka users**

マンガバカ (MangaBaka) - Your manga tracking companion
