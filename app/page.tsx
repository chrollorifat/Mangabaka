export default function Home() {
  const cardUrl = `${process.env.NEXT_PUBLIC_BASE_URL || 'https://your-app.vercel.app'}/api/card?username=cold`;

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            📚 MangaUpdates Stats Card
          </h1>
          <p className="text-gray-400 text-lg">
            Dynamic image card for your Anilist bio
          </p>
        </div>

        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10 mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Preview</h2>
          <img
            src={cardUrl}
            alt="Stats Card Preview"
            className="w-full rounded-xl shadow-2xl"
          />
        </div>

        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
          <h2 className="text-xl font-semibold text-white mb-4">Use in Anilist Bio</h2>
          <p className="text-gray-400 mb-4">
            Copy this Markdown and paste it in your Anilist profile bio:
          </p>
          <code className="block bg-black/50 rounded-lg p-4 text-green-400 text-sm break-all">
            {`![MangaUpdates Stats](${cardUrl})`}
          </code>
          <p className="text-gray-500 text-sm mt-4">
            💡 The card auto-updates every hour. You can also use{' '}
            <code className="text-cyan-400">?username=yourname</code> to show
            other users&apos; stats.
          </p>
        </div>
      </div>
    </main>
  );
}