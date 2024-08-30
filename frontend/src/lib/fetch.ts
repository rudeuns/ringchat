import { NextResponse } from "next/server";

export async function fetchServer(path: string, options: RequestInit = {}) {
  const url = `${process.env.NEXT_PUBLIC_API_URL}${path}`;

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
    console.log(`Error occurred while processing API request: ${error}`);
    return NextResponse.json(
      {
        detail: "Error occurred while processing API request.",
        code: "NETWORK_ERROR",
      },
      { status: 500 },
    );
  }
}
