"use client"
import { useSessionId } from "@/hook/useSessionId";
import Link from "next/link";


export default function Home() {
  const sessionId = useSessionId();

  return (
    <main className="h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600 mb-4">Page d'accueil</h1>
      {sessionId ? (
        <p className="text-xl text-gray-800">Session ID : {sessionId}</p>
      ) : (
        <p className="text-xl text-gray-500">Chargement du Session ID...</p>
      )}
      <div>
        <Link href={'/spotify'}>
          <button>
            Se connecter avec spotify
          </button>
        </Link>
        <Link href={'/simulate'}>
          <button>
            Sans Spotify 
          </button>
        </Link>
      </div>
    </main>
  );
}