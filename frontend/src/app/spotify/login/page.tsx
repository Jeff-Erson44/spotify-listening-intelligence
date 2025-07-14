"use client";

const clientId = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID;
const redirectUri = process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI; 
const scopes = [
  "user-read-recently-played",
  "user-read-private",
];

export default function SpotifyLogin() {
  const handleLogin = () => {
    const authUrl = 
      `https://accounts.spotify.com/authorize?response_type=code` +
      `&client_id=${encodeURIComponent(clientId!)}` +
      `&scope=${encodeURIComponent(scopes.join(" "))}` +
      `&redirect_uri=${encodeURIComponent(redirectUri!)}`;
    window.location.href = authUrl;
  };

  return (
    <div>
      <h1>Connexion Spotify</h1>
      <button onClick={handleLogin}>Se connecter avec Spotify</button>
    </div>
  );
}