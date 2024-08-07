import { NextRequest, NextResponse } from 'next/server';
import { fetchServer } from '@/lib/fetch';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);

  const folderId = searchParams.get('folderId');
  if (!folderId) {
    return NextResponse.json({ message: 'Folder ID is required' }, { status: 400 });
  }
 
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chatrooms?folderId=${folderId}`
  
  return fetchServer(req, url, { method: 'GET' })
}

export async function POST(req: NextRequest) {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chatrooms`

  const body = await req.json()

  return fetchServer(req, url, { 
    method: 'POST',
    body: JSON.stringify(body)
  })
}