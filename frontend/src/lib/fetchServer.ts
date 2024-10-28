import { headers as nextHeaders } from "next/headers";

export class ErrorCode extends Error {
  code: string | undefined;

  constructor(message?: string | undefined, code?: string | undefined) {
    super(message);
    this.code = code;
  }
}

export async function fetchServer(path: string, options: RequestInit = {}) {
  const host = nextHeaders().get("host");
  const origin = host ? `https://${host}` : "";

  const url =
    process.env.NODE_ENV === "production"
      ? `${origin}/api${path}`
      : `${process.env.NEXT_PUBLIC_SERVER_API_URL}${path}`;

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
