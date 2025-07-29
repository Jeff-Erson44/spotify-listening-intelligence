"use client";

import { useEffect, useState, useCallback, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSpotifyAuth } from "@/hook/useSpotifyAuth";
import { useSession } from "@/hook/useSession";
import { extractUser } from "@/lib/api/extract-user";

const clientId = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID;
const redirectUri = process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI;
const scopes = [
  "user-read-recently-played",
  "user-read-private",
];

function SpotifyLoginInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const code = searchParams.get("code");
  const { accessToken, fetchAccessToken } = useSpotifyAuth();
  const [loadingExtract, setLoadingExtract] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const sessionId = useSession();

  useEffect(() => {
    if (code && !accessToken) {
      fetchAccessToken();
    }
  }, [code, accessToken, fetchAccessToken]);

  const handleLogin = () => {
    const authUrl =
      `https://accounts.spotify.com/authorize?response_type=code` +
      `&client_id=${encodeURIComponent(clientId!)}` +
      `&scope=${encodeURIComponent(scopes.join(" "))}` +
      `&redirect_uri=${encodeURIComponent(redirectUri!)}`;
    window.location.href = authUrl;
  };

  const handleExtractUser = useCallback(async () => {
    if (!accessToken || !sessionId) {
      setError("Token Spotify ou sessionId manquant");
      return;
    }
    setLoadingExtract(true);
    setError(null);
    try {
      await extractUser(sessionId, accessToken);
      router.push("/profile");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Erreur inconnue lors de l'extraction");
      }
    } finally {
      setLoadingExtract(false);
    }
  }, [accessToken, sessionId, router]);

  return (
    <div className="app-grid px-4">
      <h1 className="sm:text-5xl text-[24px] Sfpro-medium text-center mt-[100px] mb-4 col-span-12">
        Connexion Spotify
      </h1>

      {!accessToken ? (
        <>
          <h2 className="sm:text-xl text-sm text-center text-gray-666 px-[32px] mb-8 col-span-12">
            Connexion 100 % sécurisée via Spotify. Aucune donnée n’est stockée, aucun mot de passe requis.
          </h2>
          <div className="col-span-12 flex justify-center items-center mt-4">
            <button
              onClick={handleLogin}
              className="px-6 py-4 bg-black text-white rounded-xl hover:bg-gray-800 transition w-[250px]"
            >
              Se connecter avec Spotify
            </button>
          </div>
        </>
      ) : (
        <>
          <div className="col-span-12 flex justify-center items-center mt-4">
            <button
              onClick={handleExtractUser}
              disabled={loadingExtract}
              className="px-6 py-4 text-white bg-black rounded-xl hover:bg-gray-800 transition w-[250px]"
            >
              {loadingExtract ? "Début de l'extraction..." : "Générer mon profil"}
            </button>
          </div>
          {error && (
            <p className="text-red-500 text-sm mt-4">{error}</p>
          )}
        </>
      )}
    </div>
  );
}

export default function SpotifyLogin() {
  return (
    <Suspense fallback={<div>Chargement...</div>}>
      <SpotifyLoginInner />
    </Suspense>
  );
}