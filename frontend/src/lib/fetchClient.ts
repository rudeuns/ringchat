export async function fetchClient(path: string, options: RequestInit = {}) {
  const origin = typeof window !== "undefined" ? window.location.origin : "";

  const url =
    process.env.NODE_ENV === "production"
      ? `${origin}/api${path}`
      : `${process.env.NEXT_PUBLIC_API_URL}${path}`;

  const headers = new Headers({
    ...options.headers,
    "Content-Type": "application/json",
  });

  try {
    const res = await fetch(url, {
      ...options,
      headers,
      credentials: "include",
    });
    return res;
  } catch (error) {
    throw error;
  }
}
