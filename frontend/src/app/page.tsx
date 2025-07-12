"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [tracks, setTracks] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);

  // 1. Créer la session
  useEffect(() => {
    async function createSession() {
      try {
        const res = await fetch("https://az96kjgo55.execute-api.eu-west-3.amazonaws.com/prod/create-session", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        });

        const data = await res.json();
        console.log("Session créée:", data);
        setSessionId(data.session_id || data.sessionId || null);
      } catch (error) {
        console.error("Erreur création session:", error);
      }
    }

    createSession();
  }, []);

  // 2. Une fois session créée, appeler extract-user sans mettre le sessionId dans les headers
  useEffect(() => {
    if (!sessionId) return;

    async function fetchRecentTracks() {
      try {
        const spotifyToken = "BQBGwd6z2tKZSehGosvzALSZtZGh12p2IB_3U-z5-Kd-jt8Y_yCg8Y2sd5-d1gSPKDXKby0sib4OCy0CbjoMJx7SrkwZdgGcLL05xaZQUFla8r96o4Qee9w7oL6LOyPMlbs7F9W0iLLo-hii2LXJe7px3qmioZjeftrm995TikDMDLjIlz5ogRtIciB6W6lqS8gqjNjr-raanrQy4PO4JxPh8Ygf22CUAoBrWddWvUAjQOClNTnIp7Vj57bqaAZ2VA"; // Remplace par un token valide ou gestion OAuth

        const res = await fetch("https://az96kjgo55.execute-api.eu-west-3.amazonaws.com/prod/extract-user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${spotifyToken}`, // token dans header, ok ici
          },
          body: JSON.stringify({ session_id: sessionId }),
        });

        const data = await res.json();
        console.log("Tracks extraits:", data);
        setTracks(data.recent_tracks_preview || []);
      } catch (error) {
        console.error("Erreur récupération tracks:", error);
      }
    }

    fetchRecentTracks();
  }, [sessionId]);

  // Fonction pour chercher les artistes
  async function searchArtists() {
    if (!searchQuery) return;
    try {
      const res = await fetch("https://az96kjgo55.execute-api.eu-west-3.amazonaws.com/prod/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery }),
      });
      const data = await res.json();
      setSearchResults(data.artists || []);
      console.log("Résultats recherche:", data);
    } catch (error) {
      console.error("Erreur recherche:", error);
    }
  }

  // Fonction pour appeler extract-simulated avec les artistes sélectionnés
  async function extractSimulated() {
    if (searchResults.length === 0) {
      alert("Aucun artiste sélectionné pour extraction simulée.");
      return;
    }

    // Préparer le body avec les champs attendus
    const artistsPayload = searchResults.map(artist => ({
      id: artist.id,
      name: artist.name,
      genres: artist.genres || [],
    }));

    try {
      const res = await fetch("https://az96kjgo55.execute-api.eu-west-3.amazonaws.com/prod/extract-simulated", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, artists: artistsPayload }),
      });
      const data = await res.json();
      console.log("Extraction simulée réussie:", data);
      alert("Extraction simulée lancée !");
    } catch (error) {
      console.error("Erreur extraction simulée:", error);
      alert("Erreur lors de l'extraction simulée.");
    }
  }

  return (
    <div>
      <h1>Bienvenue sur Spotify Listening Intelligence</h1>
      {sessionId ? (
        <>
          <h2>Session créée : {sessionId}</h2>
          <h3>50 derniers morceaux extraits :</h3>
          <ul>
            {tracks.map((track, idx) => (
              <li key={idx}>
                {track.track.name} — {track.track.artists[0].name}
              </li>
            ))}
          </ul>

          <hr />

          <div>
            <h3>Recherche artiste</h3>
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Tape un nom d'artiste"
            />
            <button onClick={searchArtists}>Rechercher</button>

            <ul>
              {searchResults.map(artist => (
                <li key={artist.id}>
                  {artist.name} — Genres: {artist.genres?.join(", ") || "N/A"}
                </li>
              ))}
            </ul>

            <button onClick={extractSimulated} disabled={searchResults.length === 0}>
              Extract Simulated
            </button>
          </div>
        </>
      ) : (
        <h2>Création de session en cours...</h2>
      )}
    </div>
  );
}