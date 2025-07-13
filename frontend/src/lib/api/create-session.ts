const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export interface CreateSessionResponse {
  sessionId: string;
  createdAt: string;
}

export async function createSession(): Promise<CreateSessionResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}create-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = (await response.json()) as CreateSessionResponse;
    return data;
  } catch (error) {
    console.error('Error creating session:', error);
    throw error;
  }
}