# MangaBaka Stats Card

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/mangabaka-stats-card&env=MANGABAKA_API_KEY)

A dynamic SVG stats card for your MangaBaka library, deployable on Vercel. Generates beautiful, real-time statistics visualizations of your manga reading activity that you can embed anywhere!

## ✨ Features

- **Total Library Entries** - Overview of your entire collection
- **Chapters & Volumes Read** - Track your reading progress
- **Average Rating** - Your mean rating across all rated series
- **Status Distribution** - Visual breakdown of Reading, Completed, Paused, Dropped, and Plan to Read
- **Media Type Breakdown** - Manga, Manhwa, Manhua, and Novel counts
- **Top 5 Genres & Tags** - Discover your reading preferences
- **Auto-updates** - Refreshes every 5 minutes to avoid API rate limiting
- **Beautiful SVG Design** - Gradient backgrounds, glow effects, and smooth animations

## 🚀 Step-by-Step Deployment Guide

### Option 1: One-Click Deploy (Recommended)

1. **Click the "Deploy to Vercel" button** at the top of this README
2. **Connect your Git provider** (GitHub/GitLab/Bitbucket)
3. **Configure your project**:
   - Give your project a name (e.g., `mangabaka-stats`)
   - Set the environment variable:
     - Key: `MANGABAKA_API_KEY`
     - Value: Your MangaBaka API key
4. **Click "Deploy"**
5. Wait ~2 minutes for deployment to complete

### Option 2: Manual Deploy

#### Step 1: Get Your MangaBaka API Key

1. Go to [MangaBaka.org](https://mangabaka.org)
2. Log in to your account
3. Navigate to **Settings** → **API** or **Account Settings**
4. Generate or copy your API key

#### Step 2: Fork the Repository

1. Click **Fork** on the GitHub repository page
2. Clone your fork locally (optional):
   ```bash
   git clone https://github.com/YOUR_USERNAME/mangabaka-stats-card.git
   cd mangabaka-stats-card
   ```

#### Step 3: Deploy to Vercel

1. Go to [Vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your forked repository
4. **Configure Build Settings**:
   - Framework Preset: **Next.js** (auto-detected)
   - Root Directory: `./` (default)
   - Build Command: `next build` (default)
   - Output Directory: `.next` (default)
5. **Add Environment Variables**:
   - Click **"Environment Variables"**
   - Add: `MANGABAKA_API_KEY` = your_api_key_here
6. Click **"Deploy"**

#### Step 4: Verify Deployment

1. Once deployed, Vercel will show your project URL (e.g., `https://mangabaka-stats.vercel.app`)
2. Visit `https://your-project-url.vercel.app/api/card` to see your stats card
3. If you see an SVG image with your stats, deployment was successful!

### Option 3: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to project directory
cd mangabaka-stats-card

# Deploy
vercel --prod

# Set environment variable
vercel env add MANGABAKA_API_KEY your_api_key_here
```

## 📸 Using Your Stats Card

After deployment, your card is available at:
```
https://your-project-name.vercel.app/api/card
```

### Embed in GitHub Profile README

```markdown
![My MangaBaka Stats](https://your-project-name.vercel.app/api/card)
```

### Embed in Personal Website

```html
<img src="https://your-project-name.vercel.app/api/card" alt="My MangaBaka Stats" />
```

### Embed in Forum Signatures

Copy the image URL directly:
```
https://your-project-name.vercel.app/api/card
```

### Share on Social Media

The SVG format works great on Twitter, Discord, and most platforms that support images!

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
│       └── route.ts      # API endpoint handler (Edge Runtime)
├── app/
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page with usage instructions
├── lib/
│   └── stats.ts          # Core statistics logic (refactored)
├── types/
│   └── next.d.ts         # TypeScript type extensions
├── package.json
├── next.config.js
├── tsconfig.json
├── vercel.json           # Vercel configuration
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

Open [http://localhost:3000](http://localhost:3000) to see the landing page.
Visit [http://localhost:3000/api/card](http://localhost:3000/api/card) to see your stats card.

## 🎨 Customization

To customize the card appearance, edit the `generateSVG` function in `lib/stats.ts`:

- **Colors**: Modify the gradient definitions and color palettes
- **Layout**: Adjust the SVG viewBox and element positions
- **Fonts**: Change font families and sizes
- **Dimensions**: Update width and height variables

## 📈 Performance Optimizations

This project includes several performance improvements:

1. **Edge Runtime** - Runs on Vercel Edge for faster global response times
2. **Modular Architecture** - Separated concerns into reusable functions
3. **Single-pass Statistics** - Computes all stats in one iteration
4. **Efficient XML Escaping** - Uses lookup table for character replacement
5. **Pagination Limits** - Caps API requests to prevent timeout
6. **Early Termination** - Stops fetching when no more data
7. **Caching Strategy** - Balances freshness with API rate limits

## ❓ Troubleshooting

### Card shows "Error generating card"

1. Verify your `MANGABAKA_API_KEY` is set correctly in Vercel
2. Check Vercel Function logs for error details
3. Ensure your API key has proper permissions

### Deployment fails on Vercel

1. Make sure you're using Node.js 18+ runtime
2. Check that `next.config.js` doesn't have incompatible settings
3. Review Vercel build logs for specific errors

### Card appears blank or shows default values

1. Ensure your MangaBaka library has entries
2. Verify the API key is valid and not expired
3. Check browser console for CORS errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- [MangaBaka](https://mangabaka.org) for providing the API
- Inspired by GitHub Stats and other profile readme generators

---

**Made with ❤️ for manga readers everywhere**
