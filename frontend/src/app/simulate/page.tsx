"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { searchArtists } from "@/lib/api/search";
import { extractSimulated } from "@/lib/api/extract-simulate";

interface Artist {
  id: string;
  name: string;
  genres: string[];
  images?: { url: string }[];
}

export default function SimulatePage() {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Artist[]>([]);
  const [selectedArtists, setSelectedArtists] = useState<Artist[]>([]);
  const router = useRouter(); 

  useEffect(() => {
    const stored = localStorage.getItem("selectedArtists");
    if (stored) {
      setSelectedArtists(JSON.parse(stored));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("selectedArtists", JSON.stringify(selectedArtists));
  }, [selectedArtists]);

  async function handleSearch() {
    if (!query.trim()) return;
    try {
      const results = await searchArtists(query.trim());
      setSearchResults(results);
    } catch (error) {
      console.error("Erreur recherche artistes", error);
    }
  }

  function addArtist(artist: Artist) {
    if (selectedArtists.find((a) => a.id === artist.id)) return;
    setSelectedArtists([...selectedArtists, artist]);
  }

  function removeArtist(id: string) {
    setSelectedArtists(selectedArtists.filter((a) => a.id !== id));
  }

  return (
    <main style={{ padding: "1rem" }}>
      <h1>Simulation - Recherche artistes</h1>

      <input
        type="text"
        placeholder="Chercher un artiste"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSearch();
        }}
        style={{ padding: "0.5rem", width: "300px" }}
      />
      <button onClick={handleSearch} style={{ marginLeft: 8 }}>
        Rechercher
      </button>

      <section style={{ marginTop: "1rem" }}>
        <h2>Résultats</h2>
        {searchResults.length === 0 && <p>Aucun résultat</p>}
        <ul>
          {searchResults.map((artist) => (
            <li key={artist.id} style={{ marginBottom: "0.5rem" }}>
              <strong>{artist.name}</strong> — Genres:{" "}
              {artist.genres.join(", ") || "N/A"}
              <button
                style={{ marginLeft: 8 }}
                onClick={() => addArtist(artist)}
              >
                Ajouter
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h2>Artistes sélectionnés</h2>
        {selectedArtists.length === 0 && <p>Aucun artiste sélectionné</p>}
        <ul>
          {selectedArtists.map((artist) => (
            <li key={artist.id} style={{ marginBottom: "0.5rem" }}>
              <strong>{artist.name}</strong> — Genres:{" "}
              {artist.genres.join(", ") || "N/A"}
              <button
                style={{ marginLeft: 8 }}
                onClick={() => removeArtist(artist.id)}
              >
                Supprimer
              </button>
            </li>
          ))}
        </ul>
      </section>

      <button
        disabled={selectedArtists.length < 5 || selectedArtists.length > 10}
        style={{ marginTop: "2rem", padding: "0.5rem 1rem", fontWeight: "bold" }}
        onClick={async () => {
          try {
            const sessionId = localStorage.getItem("sessionId");
            if (!sessionId) return;

            const result = await extractSimulated(selectedArtists, sessionId);
            console.log("Extract simulated result:", result);

            localStorage.removeItem("selectedArtists");
            setSelectedArtists([]);

            router.push("/profile");
          } catch (error) {
            console.error("Erreur extraction simulée", error);
          }
        }}
      >
        Générer l’extraction simulée
      </button>
    </main>
  );
}