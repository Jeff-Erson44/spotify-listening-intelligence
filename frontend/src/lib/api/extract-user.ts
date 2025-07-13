const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function extractUser(sessionId: string, token: string) {
  try {
    const response = await fetch(`${API_BASE_URL}extract-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ session_id: sessionId }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error in extractUser:', error);
    throw error;
  }
}