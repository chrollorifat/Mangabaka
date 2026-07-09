# MangaBaka Stats Card

A dynamic SVG image card that displays your MangaBaka reading statistics. Deployable on Vercel as a serverless function.

## Features

- Dynamic fetching of your MangaBaka reading stats
- Beautiful, modern SVG card design with gradient accents
- Progress bars for completion and finished rates
- Multiple stats displayed: total manga, chapters, volumes, rereads, mean score, days read
- Graceful fallback values when API is unavailable
- CORS-enabled for embedding anywhere

## Stats Displayed

| Stat | Description |
|------|-------------|
| Completion Rate | Percentage of manga you've completed |
| Finished Rate | Percentage of manga fully finished |
| Mean Score | Your average manga rating |
| Days Read | Total days spent reading |
| Total Manga | Number of manga in your list |
| Chapters Read | Total chapters consumed |
| Volumes Read | Total volumes consumed |
| Rereads | Number of manga re-read |

## Deployment on Vercel

### 1. Get Your MangaBaka API Token

1. Log in to [MangaBaka](https://mangabaka.org)
2. Go to your account settings
3. Generate an API token

### 2. Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/Mangabaka&env=MANGABAKA_TOKEN&envDescription=Your+MangaBaka+API+Token)

Or deploy manually:

```bash
# Clone this repository
git clone https://github.com/yourusername/Mangabaka.git
cd Mangabaka

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### 3. Set Environment Variable

In your Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add `MANGABAKA_TOKEN` with your API token

## Usage

Once deployed, your card will be available at:

```
https://your-project.vercel.app/
```

### Embed in Markdown

```markdown
![MangaBaka Stats](https://your-project.vercel.app/)
```

### Embed in HTML

```html
<img src="https://your-project.vercel.app/" alt="MangaBaka Stats" />
```

### Embed in GitHub Profile README

```markdown
![MangaBaka Stats](https://your-project.vercel.app/)
```

## Local Development

```bash
# Install dependencies (if any)
npm install

# Run locally
vercel dev
```

## API Endpoint

The serverless function is located at `api/index.js` and handles:

- `GET /` - Returns the SVG image card

## Customization

You can customize the card by editing `api/index.js`:

- Change colors in the SVG gradients
- Adjust dimensions (width/height)
- Modify the stats displayed
- Change fonts and styling

## License

MIT
