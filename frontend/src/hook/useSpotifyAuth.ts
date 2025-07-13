import { useState, useEffect, useCallback } from "react";

const CLIENT_ID = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID!;
const CLIENT_SECRET = process.env.NEXT_PUBLIC_SPOTIFY_SECRET!;
const REDIRECT_URI = process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI!;

export function useSpotifyAuth() {
  const [oauthCode, setOauthCode] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loadingToken, setLoadingToken] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const code = localStorage.getItem("spotify_oauth_code");
    setOauthCode(code);
  }, []);

  useEffect(() => {
    if (oauthCode && !accessToken && !loadingToken) {
      fetchAccessToken();
    }
  }, [oauthCode]);

  const fetchAccessToken = useCallback(async () => {
    if (!oauthCode) return;
    setLoadingToken(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append("grant_type", "authorization_code");
      params.append("code", oauthCode);
      params.append("redirect_uri", REDIRECT_URI);

      const basicAuth = btoa(`${CLIENT_ID}:${CLIENT_SECRET}`);

      const res = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: {
          Authorization: `Basic ${basicAuth}`,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: params.toString(),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error_description || "Erreur token Spotify");
      }
      const data = await res.json();
      setAccessToken(data.access_token);
      localStorage.setItem("spotify_access_token", data.access_token);
    } catch (err: any) {
      setError(err.message || "Erreur lors de la récupération du token");
    } finally {
      setLoadingToken(false);
    }
  }, [oauthCode]);

  return {
    oauthCode,
    accessToken,
    loadingToken,
    error,
    fetchAccessToken,
  };
}