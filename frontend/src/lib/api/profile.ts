const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export type ProfileData = {
  nb_tracks: number;
  description_auto: string;
  top_3_emotions: string[];
  emotion_colors: Record<string, string>;
  genre_dominant: string;
  top_3_genres: string[];
  danse_moyenne: number;
  energie_moyenne: number;
};

export async function fetchUserProfile(sessionId: string): Promise<ProfileData> {
  if (!sessionId) {
    throw new Error("Session ID not found in localStorage");
  }

  console.log("Sending session_id in body:", sessionId);
  const response = await fetch(`${API_BASE_URL}get-user`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return {
    nb_tracks: data.recent_tracks_count,
    description_auto: data.description_auto || '',
    top_3_emotions: data.top_3_emotions || [],
    emotion_colors: data.emotion_colors || {},
    genre_dominant: data.genre_dominant || '',
    top_3_genres: data.top_3_genres || [],
    danse_moyenne: data.danse_moyenne || 0,
    energie_moyenne: data.energie_moyenne || 0,
  };
}