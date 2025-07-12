"use client"
import { useEffect, useState, useCallback } from "react";
import { extractUser } from "@/lib/api/extract-user";
import { useSession } from "@/hook/useSession";
import { useRouter } from "next/navigation";

const CLIENT_ID = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID!;
const CLIENT_SECRET = process.env.NEXT_PUBLIC_SPOTIFY_SECRET!;
const REDIRECT_URI = process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI!;

export default function SpotifyPage() {
  const router = useRouter();
  const sessionId = useSession();
  const [oauthCode, setOauthCode] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loadingToken, setLoadingToken] = useState(false);
  const [loadingExtract, setLoadingExtract] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  // Récupérer le code OAuth dans localStorage
  useEffect(() => {
    const code = localStorage.getItem("spotify_oauth_code");
    setOauthCode(code);
  }, []);

  // Auto call fetchAccessToken dès que oauthCode est défini
  useEffect(() => {
    if (oauthCode && !accessToken && !loadingToken) {
      fetchAccessToken();
    }
  }, [oauthCode]);

  // suppression du useEffect auto extractUser

  // Échange code OAuth contre token
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

  // Appel lambda extractUser
  const handleExtractUser = useCallback(async () => {
    if (!accessToken || !sessionId) {
      setError("Token Spotify ou sessionId manquant");
      return;
    }
    setLoadingExtract(true);
    setError(null);
    setResult(null);
    try {
      const data = await extractUser(sessionId, accessToken);
      setResult(data);
      router.push("/profile");
    } catch (err: any) {
      setError(err.message || "Erreur inconnue lors de l'extraction");
    } finally {
      setLoadingExtract(false);
    }
  }, [accessToken, sessionId, router]);

  return (
    <main style={{ padding: "2rem" }}>
      <h1>Page Spotify</h1>

      {!accessToken && oauthCode && (
        <button onClick={fetchAccessToken} disabled={loadingToken}>
          {loadingToken ? "Récupération du token..." : "Obtenir Access Token"}
        </button>
      )}

      {accessToken && (
        <>
          <section>
            <h2>Access Token Spotify</h2>
            <pre
              style={{
                backgroundColor: "#f0f0f0",
                padding: "1rem",
                borderRadius: "4px",
                wordBreak: "break-all",
              }}
            >
              {accessToken}
            </pre>
          </section>

          <section style={{ marginTop: "1rem" }}>
            <h2>Session ID</h2>
            {sessionId ? (
              <p>{sessionId}</p>
            ) : (
              <p>Aucun sessionId trouvé dans le localStorage.</p>
            )}
          </section>

          <button
            onClick={handleExtractUser}
            disabled={loadingExtract || !sessionId}
            style={{ marginTop: "2rem", padding: "0.5rem 1rem", fontSize: "1rem" }}
          >
            {loadingExtract ? "Extraction en cours..." : "Générer Extraction"}
          </button>

          {error && (
            <p style={{ color: "red", marginTop: "1rem" }}>Erreur : {error}</p>
          )}

          {result && (
            <section style={{ marginTop: "2rem" }}>
              <h2>Résultat Extraction</h2>
              <pre
                style={{
                  backgroundColor: "#e0ffe0",
                  padding: "1rem",
                  borderRadius: "4px",
                  maxHeight: "300px",
                  overflow: "auto",
                  wordBreak: "break-word",
                }}
              >
                {JSON.stringify(result, null, 2)}
              </pre>
            </section>
          )}
        </>
      )}

      {!oauthCode && <p>Veuillez d'abord vous connecter via Spotify pour obtenir un code OAuth.</p>}
    </main>
  );
}