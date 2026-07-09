import { ImageResponse } from '@vercel/og';
import { NextRequest } from 'next/server';
import { fetchUserStats } from '@/lib/mangaupdates';
import { readFileSync } from 'fs';
import { join } from 'path';

export const runtime = 'nodejs';

// Load font
const fontPath = join(process.cwd(), 'public', 'fonts', 'Inter-Bold.ttf');
let fontBuffer: Buffer | null = null;

function getFont() {
  if (!fontBuffer) {
    fontBuffer = readFileSync(fontPath);
  }
  return fontBuffer;
}

// Color palette
const COLORS = {
  bg_start: '#0f0c29',
  bg_mid: '#302b63',
  bg_end: '#24243e',
  card_bg: 'rgba(255, 255, 255, 0.05)',
  card_border: 'rgba(255, 255, 255, 0.1)',
  text_primary: '#ffffff',
  text_secondary: '#a0aec0',
  accent: '#00d4ff',
  reading: '#4299e1',
  completed: '#48bb78',
  on_hold: '#ecc94b',
  dropped: '#f56565',
  wish: '#9f7aea',
  genre_bg: 'rgba(255, 255, 255, 0.1)',
};

function formatNumber(num: number): string {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k';
  }
  return num.toString();
}

function getStatusPercentage(
  count: number,
  total: number
): number {
  if (total === 0) return 0;
  return Math.round((count / total) * 100);
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const username = searchParams.get('username') || 'cold';
  const theme = searchParams.get('theme') || 'dark';

  const apiKey = process.env.MANGAUPDATES_API_KEY;
  if (!apiKey) {
    return new Response('API key not configured', { status: 500 });
  }

  try {
    const stats = await fetchUserStats(username, apiKey);

    const totalWithStatus =
      stats.status_breakdown.reading +
      stats.status_breakdown.completed +
      stats.status_breakdown.on_hold +
      stats.status_breakdown.dropped +
      stats.status_breakdown.wish;

    const font = getFont();

    return new ImageResponse(
      (
        <div
          style={{
            width: '100%',
            height: '100%',
            background: `linear-gradient(135deg, ${COLORS.bg_start} 0%, ${COLORS.bg_mid} 50%, ${COLORS.bg_end} 100%)`,
            display: 'flex',
            flexDirection: 'column',
            padding: '40px',
            fontFamily: 'Inter',
            boxSizing: 'border-box',
          }}
        >
          {/* Header */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '30px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              {/* Avatar */}
              <div
                style={{
                  width: '64px',
                  height: '64px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '28px',
                  fontWeight: 'bold',
                  color: 'white',
                  overflow: 'hidden',
                  border: '3px solid rgba(255,255,255,0.2)',
                }}
              >
                {stats.avatar ? (
                  <img
                    src={stats.avatar}
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    alt={stats.username}
                  />
                ) : (
                  stats.username.charAt(0).toUpperCase()
                )}
              </div>
              <div>
                <div
                  style={{
                    fontSize: '32px',
                    fontWeight: 'bold',
                    color: COLORS.text_primary,
                  }}
                >
                  {stats.username}
                </div>
                <div
                  style={{
                    fontSize: '14px',
                    color: COLORS.text_secondary,
                  }}
                >
                  MangaUpdates Stats
                </div>
              </div>
            </div>
            <div
              style={{
                fontSize: '14px',
                color: COLORS.accent,
                background: 'rgba(0, 212, 255, 0.1)',
                padding: '8px 16px',
                borderRadius: '20px',
                border: '1px solid rgba(0, 212, 255, 0.3)',
              }}
            >
               {stats.total_series} Series
            </div>
          </div>

          {/* Stats Grid */}
          <div
            style={{
              display: 'flex',
              gap: '16px',
              marginBottom: '30px',
            }}
          >
            {[
              { label: 'Manga Read', value: stats.total_series, icon: '📖' },
              { label: 'Chapters', value: formatNumber(stats.total_chapters), icon: '📄' },
              { label: 'Volumes', value: formatNumber(stats.total_volumes), icon: '' },
            ].map((stat, i) => (
              <div
                key={i}
                style={{
                  flex: 1,
                  background: COLORS.card_bg,
                  border: `1px solid ${COLORS.card_border}`,
                  borderRadius: '16px',
                  padding: '20px',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  backdropFilter: 'blur(10px)',
                }}
              >
                <div style={{ fontSize: '24px', marginBottom: '8px' }}>{stat.icon}</div>
                <div
                  style={{
                    fontSize: '28px',
                    fontWeight: 'bold',
                    color: COLORS.text_primary,
                  }}
                >
                  {stat.value}
                </div>
                <div
                  style={{
                    fontSize: '12px',
                    color: COLORS.text_secondary,
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                  }}
                >
                  {stat.label}
                </div>
              </div>
            ))}
          </div>

          {/* Status Breakdown */}
          <div
            style={{
              background: COLORS.card_bg,
              border: `1px solid ${COLORS.card_border}`,
              borderRadius: '16px',
              padding: '20px',
              marginBottom: '20px',
            }}
          >
            <div
              style={{
                fontSize: '14px',
                color: COLORS.text_secondary,
                marginBottom: '16px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
              }}
            >
              Reading Status
            </div>
            {[
              { label: 'Reading', count: stats.status_breakdown.reading, color: COLORS.reading },
              { label: 'Completed', count: stats.status_breakdown.completed, color: COLORS.completed },
              { label: 'On Hold', count: stats.status_breakdown.on_hold, color: COLORS.on_hold },
              { label: 'Dropped', count: stats.status_breakdown.dropped, color: COLORS.dropped },
              { label: 'Plan to Read', count: stats.status_breakdown.wish, color: COLORS.wish },
            ].map((status, i) => {
              const pct = getStatusPercentage(status.count, totalWithStatus);
              return (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    marginBottom: i < 4 ? '12px' : '0',
                    gap: '12px',
                  }}
                >
                  <div
                    style={{
                      width: '100px',
                      fontSize: '13px',
                      color: COLORS.text_secondary,
                      textAlign: 'right',
                    }}
                  >
                    {status.label}
                  </div>
                  <div
                    style={{
                      flex: 1,
                      height: '20px',
                      background: 'rgba(255,255,255,0.05)',
                      borderRadius: '10px',
                      overflow: 'hidden',
                      position: 'relative',
                    }}
                  >
                    <div
                      style={{
                        width: `${pct}%`,
                        height: '100%',
                        background: status.color,
                        borderRadius: '10px',
                        transition: 'width 0.3s',
                      }}
                    />
                  </div>
                  <div
                    style={{
                      width: '50px',
                      fontSize: '13px',
                      color: COLORS.text_primary,
                      fontWeight: 'bold',
                    }}
                  >
                    {pct}%
                  </div>
                </div>
              );
            })}
          </div>

          {/* Top Genres */}
          {stats.top_genres.length > 0 && (
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
              {stats.top_genres.map((genre, i) => (
                <div
                  key={i}
                  style={{
                    background: COLORS.genre_bg,
                    border: '1px solid rgba(255,255,255,0.15)',
                    borderRadius: '20px',
                    padding: '8px 20px',
                    fontSize: '14px',
                    color: COLORS.text_primary,
                    backdropFilter: 'blur(10px)',
                  }}
                >
                  {genre.genre}
                </div>
              ))}
            </div>
          )}
        </div>
      ),
      {
        width: 900,
        height: 450,
        fonts: [
          {
            name: 'Inter',
            data: font,
            style: 'normal',
            weight: 700,
          },
        ],
      }
    );
  } catch (error) {
    console.error('Error generating card:', error);
    return new ImageResponse(
      (
        <div
          style={{
            width: '100%',
            height: '100%',
            background: '#1a1a2e',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
            fontFamily: 'Inter',
          }}
        >
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⚠️</div>
          <div style={{ fontSize: '24px', color: 'white', fontWeight: 'bold' }}>
            Error Loading Stats
          </div>
          <div style={{ fontSize: '14px', color: '#a0aec0', marginTop: '8px' }}>
            {error instanceof Error ? error.message : 'Unknown error'}
          </div>
        </div>
      ),
      {
        width: 900,
        height: 450,
        fonts: [
          {
            name: 'Inter',
            data: fontBuffer || Buffer.from(''),
            style: 'normal',
            weight: 700,
          },
        ],
      }
    );
  }
}