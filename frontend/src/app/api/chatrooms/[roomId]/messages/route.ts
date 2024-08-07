import { NextRequest, NextResponse } from 'next/server';
import { fetchServer } from '@/lib/fetch';

interface Params {
  params: {
    roomId: string;
  };
}

export async function GET(req: NextRequest, { params }: Params) {
  const { roomId } = params;
  if (!roomId) {
    return NextResponse.json({ message: 'Room ID is required' }, { status: 400 });
  }

  const url = `${process.env.NEXT_PUBLIC_API_URL}/chatrooms/${roomId}/messages`;
  
  return fetchServer(req, url, { method: 'GET' })
}

export async function POST(req: NextRequest, { params }: Params) {
  const { roomId } = params;
  if (!roomId) {
    return NextResponse.json({ message: 'Room ID is required' }, { status: 400 });
  }
  
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chatrooms/${roomId}/messages`;
  
  const body = await req.json()

  return fetchServer(req, url, { 
    method: 'POST',
    body: JSON.stringify(body)
  })
}