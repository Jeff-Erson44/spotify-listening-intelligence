"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { searchArtists } from "@/lib/api/search";
import ArtistSearchInput from "@/components/ArtistSearchInput/ArtistSearchInput";
import ArtistSearchSelect from "@/components/ArtistSearchSelect";

interface Artist {
  id: string;
  name: string;
  genres: string[];
  image?: { url: string }[];
}

export default function SimulatePage() {
  const router = useRouter();

  const [results, setResults] = useState<Artist[]>([]);
  const [query, setQuery] = useState("");
  const [selectedArtists, setSelectedArtists] = useState<Artist[]>([]);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("selectedArtists") || "[]");
    setSelectedArtists(stored);
  }, []);

  const handleSearch = async (value: string) => {
    try {
      const data = await searchArtists(value);
      console.log("Résultats de la recherche :", data);
      setResults(data);
    } catch (error) {
      console.error("Erreur de recherche :", error);
    }
  };

  const handleSelect = (artist: Artist) => {
    if (selectedArtists.find((a) => a.id === artist.id)) return;
    if (selectedArtists.length >= 10) return;

    const selected = {
      id: artist.id,
      name: artist.name,
      genres: artist.genres,
      image: artist.image
    };

    const stored = JSON.parse(localStorage.getItem("selectedArtists") || "[]");
    const updated = [...stored, selected];
    localStorage.setItem("selectedArtists", JSON.stringify(updated));

    console.log("Artiste ajouté au localStorage :", selected);

    setSelectedArtists((prev) => [...prev, artist]);
    setQuery("");
    setResults([]); 
  };

  return (
    <main className="">
      <h1 className="sm:text-5xl text-[24px] Sfpro-medium text-center mt-[100px] mb-4">Ton profil, à partir de tes artistes.</h1>
      <h2 className="sm:text-xl text-sm text-center text-gray-666 px-[32px]">Ajoute quelques artistes que tu écoutes régulièrement. On s'occupe du reste</h2>

      <div className="flex items-center gap-4 my-8 justify-center px-8">
        <ArtistSearchInput
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={() => handleSearch(query)}
          className="px-6 py-4 bg-black text-white rounded-xl hover:bg-gray-800 transition"
        >
          Rechercher
        </button>
      </div>
      {selectedArtists.length < 5 ? (
        <p className="text-[8px] text-red-500 text-center mt-1">Ajoute au moins 5 artistes pour continuer</p>
      ) : selectedArtists.length >= 10 ? (
        <p className="text-[8px] text-red-500 text-center mt-1">Tu ne peux pas ajouter plus de 10 artistes</p>
      ) : null}
      <div className="sm:app-grid">
          <div className="flex col-start-4 col-end-10 flex-column justify-center px-4 flex-col gap-2">
            {results.map((artist) => (
            <ArtistSearchSelect key={artist.id} artist={artist} onSelect={handleSelect} className=""/>
          ))}
        </div>
      </div>
      

      <div className="mt-12 px-4">

        <div className="flex flex-wrap justify-center gap-4">
          {selectedArtists.map((artist) => (
            <div key={artist.id} className="flex flex-col items-center">
              {artist.image && typeof artist.image === "string" && (
                <img
                  src={artist.image}
                  alt={artist.name}
                  width={80}
                  height={80}
                  className="rounded-xl object-cover w-[80px] h-[80px]"
                />
              )}
              <p className="mt-2 text-sm text-center">{artist.name}</p>
              <button
                onClick={() => {
                  const updated = selectedArtists.filter((a) => a.id !== artist.id);
                  setSelectedArtists(updated);
                  localStorage.setItem("selectedArtists", JSON.stringify(updated));
                }}
                className="mt-1 text-xs text-red-500 hover:underline"
              >
                Supprimer
              </button>
            </div>
          ))}
        </div>
        <div className="text-center mt-8">
          <button
            disabled={selectedArtists.length < 5 || selectedArtists.length > 10}
            className={`px-6 py-4 rounded-xl transition ${
              selectedArtists.length >= 5 && selectedArtists.length <= 10
                ? "bg-black text-white hover:bg-gray-800"
                : "bg-gray-300 text-gray-500 cursor-not-allowed"
            }`}
            onClick={async () => {
              try {
                const sessionId = localStorage.getItem("sessionId");
                if (!sessionId) return;

                const { extractSimulated } = await import("@/lib/api/extract-simulate");
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
            Générer le profil
          </button>
        </div>
      </div>
    </main>
  );
}