"use client"
import { useEffect, useCallback, useState } from "react";
import { extractUser } from "@/lib/api/extract-user";
import { useSession } from "@/hook/useSession";
import { useSpotifyAuth } from "@/hook/useSpotifyAuth";
import { useRouter } from "next/navigation";


export default function SpotifyPage() {
  const router = useRouter();
  const { accessToken, loadingToken, error: authError, fetchAccessToken } = useSpotifyAuth();

  useEffect(() => {
    if (!accessToken && !loadingToken) {
      const timer = setTimeout(() => {
        router.push("/spotify/login");
      }, 1500);

      return () => clearTimeout(timer);
    }
  }, [accessToken, loadingToken, router]);

  useEffect(() => {
    const url = new URL(window.location.href);
    const code = url.searchParams.get("code");

    if (code) {
      console.log("Code OAuth récupéré depuis l’URL :", code);
      localStorage.setItem("spotify_oauth_code", code);
    }
  }, []);
  const sessionId = useSession();
  const [loadingExtract, setLoadingExtract] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    console.log("SessionID:", sessionId);
    console.log("AccessToken:", accessToken);
  }, [sessionId, accessToken]);

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

      {!accessToken && (
        <button onClick={fetchAccessToken} disabled={loadingToken}>
          {loadingToken ? "Récupération du token..." : "Obtenir Access Token"}
        </button>
      )}

      {authError && (
        <p style={{ color: "red", marginTop: "1rem" }}>Erreur Auth : {authError}</p>
      )}

      {authError?.includes("Authorization code expired") && (
        <div style={{ marginTop: "1rem", color: "red" }}>
          <p>Votre code Spotify a expiré. Veuillez recommencer la connexion.</p>
          <button onClick={() => router.push("/")}>Retour à l’accueil</button>
        </div>
      )}

      {accessToken && (
        <>
          <section>
            <details style={{ marginTop: "1rem" }}>
              <summary>Voir Access Token</summary>
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
            </details>
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

      {!accessToken && !loadingToken && (
        <p>Veuillez d'abord vous connecter via Spotify pour obtenir un code OAuth.</p>
      )}
    </main>
  );
}