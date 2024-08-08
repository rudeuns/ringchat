import { NextRequest, NextResponse } from 'next/server';
import { fetchServer } from '@/lib/fetch';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);

  const userId = searchParams.get('userId');
  if (!userId) {
    return NextResponse.json({ message: 'User ID is required' }, { status: 400 });
  }

  const url = `${process.env.NEXT_PUBLIC_API_URL}/folders?userId=${userId}`
  
  return fetchServer(req, url, { method: 'GET' })
}