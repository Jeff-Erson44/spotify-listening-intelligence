const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function extractUser(sessionId: string) {
  try {
    const res = await fetch(`${BASE_URL}/extract-user-lambda`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-session-id": sessionId,
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error("Erreur HTTP:", res.status, errorText);
      throw new Error(`Échec de l'extraction: ${res.status} - ${errorText}`);
    }

    return res.json();
  } catch (error) {
    console.error("Erreur réseau ou fetch:", error);
    throw new Error("Impossible d'appeler la fonction extract-user.");
  }
}