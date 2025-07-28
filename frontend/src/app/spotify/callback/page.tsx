"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, Suspense } from "react";

function SpotifyCallbackContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const code = searchParams.get("code");
    const error = searchParams.get("error");

    if (error) return;

    if (code) {
      localStorage.setItem("spotify_oauth_code", code);
      setTimeout(() => {
        router.push("/spotify/login?code=" + code);
      }, 2000);
    }
  }, [searchParams, router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <h1 className="text-2xl font-bold mb-6">récupération de vos goûts musicaux</h1>
    </div>
  );
}

export default function SpotifyCallback() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen">Chargement...</div>}>
      <SpotifyCallbackContent />
    </Suspense>
  );
}