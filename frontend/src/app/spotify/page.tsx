"use client";
import { useEffect, useState } from "react";
import { extractUser } from "@/lib/api/extract-user";

export default function Spotify() {
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("sessionId");
    if (stored) {
      setSessionId(stored);
    }
  }, []);

  const handleGenerateProfile = async () => {
    if (!sessionId) {
      console.error("Aucun ID de session trouvé.");
      return;
    }

    setLoading(true);
    try {
      const result = await extractUser(sessionId);
      console.log("Résultat Lambda extract-user-lambda :", result);
    } catch (error) {
      console.error("Erreur lors de l'extraction :", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Page Spotify</h1>

      <button
        onClick={handleGenerateProfile}
        disabled={loading || !sessionId}
        className="px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700"
      >
        {loading ? "Génération en cours..." : "Générer mon profil"}
      </button>

      <p className="mt-4 text-sm text-gray-500">
        Nous n'enregistrons aucune donnée personnelle. La génération est anonyme et temporaire.
      </p>
    </div>
  );
}