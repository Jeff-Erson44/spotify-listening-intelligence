'use client';
import { useRouter } from 'next/navigation';
import { createSession } from '@/lib/api/create-session';
import { useSessionContext } from '@/context/SessionContext';

export default function Home() {
  const { sessionId } = useSessionContext();
  const router = useRouter();

  return (
    <main>
      <div style={{ marginTop: 20 }}>
        <button
          onClick={async () => {
            localStorage.removeItem('sessionId');
            const { sessionId } = await createSession();
            console.log("New Spotify sessionId:", sessionId);
            localStorage.setItem('sessionId', sessionId);
            router.push('/spotify/login');
          }}
          style={{ marginRight: 10 }}
        >
          Connexion Spotify (compte)
        </button>

        <button
          onClick={async () => {
            localStorage.removeItem('sessionId');
            const { sessionId } = await createSession();
            console.log("New Simulated sessionId:", sessionId);
            localStorage.setItem('sessionId', sessionId);
            router.push('/simulate');
          }}
        >
          Version Simulée (sans compte)
        </button>
      </div>
    </main>
  );
}