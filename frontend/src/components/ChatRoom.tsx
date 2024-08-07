'use client';

import { useRouter } from "next/navigation";
import { ChatRoomData } from "@/lib/interfaces";

interface ChatRoomProps extends ChatRoomData {
  isSelected: boolean;
  onSelect: () => void;
}

export default function ChatRoom({ roomId, roomName, isSelected, onSelect }: ChatRoomProps) {
  const router = useRouter();

  const handleClick = () => {
    onSelect();
    router.push(`/chat/${roomId}`);
  };

  return (
    <button className="chatroom" onClick={handleClick}>
      <p className={isSelected ? "font-semibold" : ""}>{roomName}</p>
    </button>
  );
}
