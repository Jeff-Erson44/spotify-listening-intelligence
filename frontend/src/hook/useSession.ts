import { useState, useEffect } from 'react';
import { createSession } from '@/lib/api/create-session';

const SESSION_KEY = 'sessionId';
const SESSION_TIMESTAMP_KEY = 'sessionTimestamp';
const SESSION_EXPIRATION_MS = 60 * 60 * 1000; // 1 heure

export function useSession() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedSessionId = localStorage.getItem(SESSION_KEY);
    const storedTimestamp = localStorage.getItem(SESSION_TIMESTAMP_KEY);
    const now = Date.now();

    if (storedSessionId && storedTimestamp) {
      const age = now - parseInt(storedTimestamp, 10);
      if (age < SESSION_EXPIRATION_MS) {
        setSessionId(storedSessionId);
        setLoading(false);
        return;
      }
      // session expirée
      localStorage.removeItem(SESSION_KEY);
      localStorage.removeItem(SESSION_TIMESTAMP_KEY);
    }

    createSession()
      .then(data => {
        localStorage.setItem(SESSION_KEY, data.sessionId);
        localStorage.setItem(SESSION_TIMESTAMP_KEY, now.toString());
        setSessionId(data.sessionId);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return sessionId;
}