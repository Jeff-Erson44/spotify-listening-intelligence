const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

type Artist = { id: string; name: string; image?: { url: string }[]; genres?: string[] };
export async function extractSimulated(artists: Artist[]) {
  const session_id = localStorage.getItem("sessionId")

  if (!session_id) {
    throw new Error("Session ID not found in localStorage");
  }
  try {
    const response = await fetch(`${API_BASE_URL}extract-simulated`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ artists, session_id }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Failed to call extract simulated API:", error);
    throw error;
  }
}