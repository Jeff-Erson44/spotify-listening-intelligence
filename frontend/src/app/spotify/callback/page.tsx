"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function SpotifyCallback() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [message, setMessage] = useState("Chargement...");

  useEffect(() => {
    const code = searchParams.get("code");
    const error = searchParams.get("error");

    if (error) {
      setMessage(`Erreur OAuth : ${error}`);
      return;
    }

    if (code) {
      localStorage.setItem("spotify_oauth_code", code);
      setMessage(`Code OAuth reçu et stocké. Redirection en cours...`);
      setTimeout(() => {
        router.push("/spotify"); 
      }, 2000);
    } else {
      setMessage("Code OAuth non trouvé dans l'URL.");
    }
  }, [searchParams, router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <h1 className="text-2xl font-bold mb-6">Callback Spotify</h1>
      <p className="break-all">{message}</p>
    </div>
  );
}