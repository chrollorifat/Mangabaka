# MangaBaka Stats Card

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/mangabaka-stats-card&env=MANGABAKA_API_KEY)

A dynamic SVG stats card for your MangaBaka library, deployable on Vercel and embeddable in AniList profiles. Generates beautiful, real-time statistics visualizations of your manga reading activity.

## ✨ Features

- **Total Library Entries** - Overview of your entire collection
- **Chapters & Volumes Read** - Track your reading progress
- **Average Rating** - Your mean rating across all rated series
- **Status Distribution** - Visual breakdown of Reading, Completed, Paused, Dropped, and Plan to Read
- **Media Type Breakdown** - Manga, Manhwa, Manhua, and Novel counts
- **Top 5 Genres & Tags** - Discover your reading preferences
- **Auto-updates** - Refreshes every 5 minutes to avoid API rate limiting
- **Beautiful SVG Design** - Gradient backgrounds, glow effects, and smooth animations

## 🚀 Quick Start

### 1. Deploy to Vercel

1. **Fork this repository** or clone it locally
2. **Get your MangaBaka API Key** from your account settings
3. **Set environment variable** in Vercel:
   - `MANGABAKA_API_KEY` = your MangaBaka API key
4. **Deploy** - Vercel will handle the rest!

### 2. Usage in AniList Bio

After deploying, your card will be available at:
```
https://your-project.vercel.app/api/card
```

Add this to your AniList bio:
```markdown
![MangaBaka Stats](https://your-project.vercel.app/api/card)
```

## 📊 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/card` | GET | Returns SVG image with your manga statistics |

### Response Headers

- `Content-Type`: `image/svg+xml`
- `Cache-Control`: `public, max-age=300, stale-while-revalidate=600`
- `Access-Control-Allow-Origin`: `*`

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MANGABAKA_API_KEY` | Yes | Your MangaBaka API key for authentication |

### Cache Settings

The card is cached for **5 minutes** (`max-age=300`) with a **stale-while-revalidate** window of 10 minutes to:
- Avoid API rate limiting
- Improve response times
- Reduce server load

## 🏗️ Project Structure

```
mangabaka-stats-card/
├── api/
│   └── card/
│       └── route.ts      # API endpoint handler
├── lib/
│   └── stats.ts          # Core statistics logic (refactored)
├── package.json
├── next.config.js
├── tsconfig.json
└── README.md
```

## 🔧 Development

### Prerequisites

- Node.js 18+ 
- npm or yarn
- A MangaBaka account with API access

### Local Setup

```bash
# Install dependencies
npm install

# Set environment variable
export MANGABAKA_API_KEY=your_api_key

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🎨 Customization

To customize the card appearance, edit the `generateSVG` function in `lib/stats.ts`:

- **Colors**: Modify the gradient definitions and color palettes
- **Layout**: Adjust the SVG viewBox and element positions
- **Fonts**: Change font families and sizes
- **Dimensions**: Update width and height variables

## 📈 Performance Optimizations

This project includes several performance improvements:

1. **Modular Architecture** - Separated concerns into reusable functions
2. **Single-pass Statistics** - Computes all stats in one iteration
3. **Efficient XML Escaping** - Uses lookup table for character replacement
4. **Pagination Limits** - Caps API requests to prevent timeout
5. **Early Termination** - Stops fetching when no more data
6. **Caching Strategy** - Balances freshness with API rate limits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- [MangaBaka](https://mangabaka.org) for providing the API
- Inspired by GitHub Stats and other profile readme generators

---

**Made with ❤️ for manga readers everywhere**
