'use client';

import Link from 'next/link';
import { useSession } from '@/hook/useSession';

export default function Home() {
  const sessionId = useSession();

  return (
    <main>
      <h1>Session ID :</h1>
      <p>{sessionId ?? 'Aucune session disponible'}</p>

      <div style={{ marginTop: 20 }}>
        <Link href="/spotify/login">
          <button style={{ marginRight: 10 }}>Connexion Spotify (compte)</button>
        </Link>

        <Link href="/simulate">
          <button>Version Simulée (sans compte)</button>
        </Link>
      </div>
    </main>
  );
}