const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function createSession() {
  try {
    const res = await fetch(`${BASE_URL}/create-session-lambda`, {
      method: "POST",
      credentials: "include",
    });
    if (!res.ok) {
      console.error("Erreur lors de la création de session:", res.statusText);
      return { sessionId: null };
    }
    const sessionId = res.headers.get("x-session-id");
    return { sessionId: sessionId ?? null };
  } catch (error) {
    console.error("Erreur réseau:", error);
    return { sessionId: null };
  }
}