import { NextRequest, NextResponse } from 'next/server';
import { fetchServer } from '@/lib/fetch';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);

  const query = searchParams.get('query');
  if (!query) {
    return NextResponse.json({ message: 'Query is required' }, { status: 400 });
  }

  const url = `${process.env.NEXT_PUBLIC_API_URL}/links?query=${query}`
  
  return fetchServer(req, url, { method: 'GET' })
}