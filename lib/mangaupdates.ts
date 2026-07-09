const BASE_URL = 'https://api.mangaupdates.com/v1';

export interface MangaUpdatesUser {
  user_id: number;
  name: string;
  avatar: string;
  last_active: string;
  status: string;
}

export interface ListEntry {
  series: {
    id: number;
    title: string;
  };
  status: string;
  volumes: number | null;
  chapters: number | null;
  last_read_volume: number | null;
  last_read_chapter: number | null;
  priority: string;
  time_added: string;
  time_updated: string;
  genres: { genre: string; spoiler: boolean }[];
}

export interface ListResponse {
  results: ListEntry[];
  total_hits: number;
  page: number;
  per_page: number;
  last_page: number;
}

export interface UserStats {
  username: string;
  avatar: string;
  total_series: number;
  total_chapters: number;
  total_volumes: number;
  status_breakdown: {
    reading: number;
    completed: number;
    on_hold: number;
    dropped: number;
    wish: number;
  };
  top_genres: { genre: string; count: number }[];
  last_active: string;
}

const STATUS_MAP: Record<string, keyof UserStats['status_breakdown']> = {
  'Reading': 'reading',
  'Completed': 'completed',
  'On Hold': 'on_hold',
  'Dropped': 'dropped',
  'Wish': 'wish',
};

async function fetchWithAuth(endpoint: string, apiKey: string, params: Record<string, string> = {}) {
  const url = new URL(`${BASE_URL}${endpoint}`);
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, value);
  });

  const res = await fetch(url.toString(), {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    next: { revalidate: 3600 }, // Cache for 1 hour
  });

  if (!res.ok) {
    throw new Error(`MangaUpdates API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function fetchUser(username: string, apiKey: string): Promise<MangaUpdatesUser> {
  return fetchWithAuth(`/users/${encodeURIComponent(username)}`, apiKey);
}

export async function fetchUserLists(
  username: string,
  apiKey: string,
  page: number = 1
): Promise<ListResponse> {
  return fetchWithAuth(`/users/${encodeURIComponent(username)}/lists`, apiKey, {
    page: page.toString(),
    per_page: '100',
  });
}

export async function fetchUserStats(username: string, apiKey: string): Promise<UserStats> {
  const [user, firstPage] = await Promise.all([
    fetchUser(username, apiKey),
    fetchUserLists(username, apiKey, 1),
  ]);

  const allEntries: ListEntry[] = [...firstPage.results];
  const totalPages = firstPage.last_page;

  // Fetch remaining pages
  if (totalPages > 1) {
    const remainingPages = Array.from({ length: totalPages - 1 }, (_, i) => i + 2);
    const pages = await Promise.all(
      remainingPages.map((page) => fetchUserLists(username, apiKey, page))
    );
    pages.forEach((p) => allEntries.push(...p.results));
  }

  // Calculate stats
  const status_breakdown: UserStats['status_breakdown'] = {
    reading: 0,
    completed: 0,
    on_hold: 0,
    dropped: 0,
    wish: 0,
  };

  let total_chapters = 0;
  let total_volumes = 0;
  const genreCounts: Record<string, number> = {};

  allEntries.forEach((entry) => {
    const statusKey = STATUS_MAP[entry.status];
    if (statusKey) {
      status_breakdown[statusKey]++;
    }

    if (entry.last_read_chapter) total_chapters += entry.last_read_chapter;
    if (entry.last_read_volume) total_volumes += entry.last_read_volume;

    entry.genres?.forEach((g) => {
      if (!g.spoiler) {
        genreCounts[g.genre] = (genreCounts[g.genre] || 0) + 1;
      }
    });
  });

  const top_genres = Object.entries(genreCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([genre, count]) => ({ genre, count }));

  return {
    username: user.name,
    avatar: user.avatar,
    total_series: allEntries.length,
    total_chapters,
    total_volumes,
    status_breakdown,
    top_genres,
    last_active: user.last_active,
  };
}