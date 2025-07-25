"use client";

import { useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function SpotifyCallback() {
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const code = searchParams.get("code");
    const error = searchParams.get("error");

    if (error) {
      return;
    }

    if (code) {
      localStorage.setItem("spotify_oauth_code", code);
      setTimeout(() => {
        router.push("/spotify/login?code=" + code);
      }, 2000);
    }
  }, [searchParams, router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <h1 className="text-2xl font-bold mb-6">récupération de vos gout musicaux</h1>
    </div>
  );
}