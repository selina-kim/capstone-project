type MethodType = "GET" | "POST" | "DELETE" | "PUT";

const request = async (
  method: MethodType,
  endpoint: string,
  body: BodyInit | null | undefined = null,
) => {
  const url = `${process.env.EXPO_PUBLIC_API_URL}${endpoint}`;
  try {
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        // 'Authorization': `Bearer ${token}`,
      },
      body: body,
    });

    if (!response.ok) {
      throw new Error(
        `HTTP Error Status: ${response.status} - ${response.statusText}`,
      );
    }

    // 204 No Content (common for deletes) has no body to parse
    if (response.status === 204) {
      return { data: null, error: null };
    }

    const data = await response.json();
    return { data, error: null };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : error;
    return {
      data: null,
      error: `Error fetching from ${url}. ${errorMessage}`,
    };
  }
};

const client = {
  get: (endpoint: string) => request("GET", endpoint),
  post: (endpoint: string, body: BodyInit | null | undefined) =>
    request("POST", endpoint, body),
  delete: (endpoint: string) => request("DELETE", endpoint),
  put: (endpoint: string, body: BodyInit | null | undefined) =>
    request("PUT", endpoint, body),
};

export default client;
