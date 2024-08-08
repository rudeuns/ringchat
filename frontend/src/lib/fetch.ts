import { NextRequest, NextResponse } from 'next/server';

export async function fetchServer(req: NextRequest, url: string, options: RequestInit = {}) {
  const token = req.headers.get('authorization')?.split(' ')[1];
  if (!token) {
    return NextResponse.json({ message: 'No token found' }, { status: 401 });
  }

  const headers = {
    ...options.headers,
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const errorMessage = `Fetch response error: ${res.status} ${res.statusText}`;
      console.error(errorMessage);
      return NextResponse.json({ message: errorMessage }, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json(data, { status: 200 });
  } catch (error) {
    const errorMessage = `Error during fetch: ${error}`;
    console.error(errorMessage);
    return NextResponse.json({ message: errorMessage }, { status: 500 });
  }
}

export async function fetchClient(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token');
  if (!token) {
    console.error('No token found');
    throw new Error('No token found');
  }

  const headers = {
    ...options.headers,
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const errorMessage = `Fetch response error: ${res.status} ${res.statusText}`;
      console.error(errorMessage);
      throw new Error(errorMessage);
    }

    return await res.json();
  } catch (error) {
    console.error(`Error during fetch: ${error}`);
    throw error;
  }
}