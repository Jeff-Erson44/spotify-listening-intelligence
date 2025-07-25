"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSpotifyAuth } from "@/hook/useSpotifyAuth";
import { useSession } from "@/hook/useSession";
import { extractUser } from "@/lib/api/extract-user";
import Loading from "@/components/Loading";

const clientId = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID;
const redirectUri = process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI;
const scopes = [
  "user-read-recently-played",
  "user-read-private",
];

export default function SpotifyLogin() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const code = searchParams.get("code");
  const { accessToken, fetchAccessToken, error: authError, loadingToken } = useSpotifyAuth();
  const [loadingExtract, setLoadingExtract] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const sessionId = useSession();

  useEffect(() => {
    if (code && !accessToken) {
      fetchAccessToken(code);
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
    } catch (err: any) {
      setError(err.message || "Erreur inconnue lors de l'extraction");
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
          <button
            onClick={handleLogin}
            className="px-6 py-4 bg-black text-white rounded-xl hover:bg-gray-800 transition w-[250px]"
          >
            Se connecter avec Spotify
          </button>
        </>
      ) : (
        <>
          <h3 className="text-center text-gray-500 mb-6">Vous êtes connecté !</h3>
          <button
            onClick={handleExtractUser}
            disabled={loadingExtract}
            className="px-6 py-4 text-white bg-black rounded-xl hover:bg-gray-800 transition w-[250px]"
          >
            {loadingExtract ? "Extraction en cours..." : "Générer mon profil"}
          </button>
          {error && (
            <p className="text-red-500 text-sm mt-4">{error}</p>
          )}
        </>
      )}
    </div>
  );
}