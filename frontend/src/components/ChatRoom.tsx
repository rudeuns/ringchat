'use client';

import { useRouter } from "next/navigation";

interface ChatRoomProps {
  name: string;
  id: string;
}

export default function ChatRoom({ name, id }: ChatRoomProps) {
  const router = useRouter();

  return (
    <button className="chatroom" onClick={() => router.push(`/chat/${id}`)}>
      <p>{name}</p>
    </button>
  );
}
