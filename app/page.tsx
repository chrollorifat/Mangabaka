export default function Home() {
  return (
    <main style={{ padding: '40px', fontFamily: 'system-ui, sans-serif' }}>
      <h1>MangaBaka Stats Card</h1>
      <p>Your dynamic stats card is ready!</p>
      <p>Use this URL to embed your stats card:</p>
      <code style={{ display: 'block', background: '#f0f0f0', padding: '10px', borderRadius: '4px', marginTop: '10px' }}>
        https://your-domain.com/api/card
      </code>
      <h2 style={{ marginTop: '30px' }}>How to use:</h2>
      <ul>
        <li>Add the image URL to your GitHub profile README</li>
        <li>Embed it in your personal website</li>
        <li>Share it on social media</li>
        <li>Use it in forum signatures</li>
      </ul>
      <h3 style={{ marginTop: '30px' }}>Example usage in Markdown:</h3>
      <pre style={{ background: '#f0f0f0', padding: '10px', borderRadius: '4px' }}>
{`![My MangaBaka Stats](https://your-domain.com/api/card)`}
      </pre>
    </main>
  );
}
