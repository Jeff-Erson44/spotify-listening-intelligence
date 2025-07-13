"use client"
import { useEffect, useState } from "react";
import { fetchProfileData, ProfileData } from "@/lib/api/profile";

export default function ProfilePage() {
  const [data, setData] = useState<ProfileData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const sessionId = localStorage.getItem('sessionId');
    if (!sessionId) {
      setError("Session ID not found in localStorage");
      return;
    }

    fetchProfileData(sessionId)
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return <div>Erreur : {error}</div>;
  }

  if (!data) {
    return <div>Chargement...</div>;
  }

  return (
    <main style={{ padding: "1rem" }}>
      <h1>Résultat</h1>

      <section>
        <h2>Nombre de titres écoutés : {data.nb_tracks}</h2>
        <p>Description : {data.description_auto}</p>
      </section>

      <section>
        <h3>Émotions principales :</h3>
        <ul>
          {data.top_3_emotions.map((emotion) => (
            <li key={emotion} style={{ color: data.emotion_colors[emotion] || 'black' }}>
              {emotion}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Genres dominants :</h3>
        <p>Genre dominant : {data.genre_dominant}</p>
        <ul>
          {data.top_3_genres.map((genre) => (
            <li key={genre}>{genre}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Moyennes :</h3>
        <p>Dansabilité moyenne : {(data.danse_moyenne * 100).toFixed(1)}%</p>
        <p>Énergie moyenne : {(data.energie_moyenne * 100).toFixed(1)}%</p>
      </section>
    </main>
  );
}