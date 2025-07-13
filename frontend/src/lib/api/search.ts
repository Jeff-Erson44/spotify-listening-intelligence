const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function searchArtists(query: string) {
  try {
    const response = await fetch(
      `${API_BASE_URL}search`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.artists || [];
  } catch (error) {
    console.error("Failed to search artists:", error);
    throw error;
  }
}