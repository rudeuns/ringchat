'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { ChevronDownIcon, ChevronRightIcon } from '@/components/common/Icons';
import ChatRoom from '@/components/ChatRoom';
import { fetchClient } from '@/lib/fetch';
import { FolderData, ChatRoomData } from '@/lib/interfaces';

export default function ChatRoomFolder({ folderId, folderName }: FolderData) {
  const [isOpen, setIsOpen] = useState(true);
  const [chatRooms, setChatRooms] = useState<ChatRoomData[]>([]);
  const [selectedRoomId, setSelectedRoomId] = useState<number | null>(null)
  const pathname = usePathname();

  const toggleFolder = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    const getChatRooms = async () => {
      try {
        const url = `/api/chatrooms?folderId=${folderId}`
        const data = await fetchClient(url, { method: 'GET'})
        setChatRooms(data);
      } catch (error) {
        console.error(`Error during fetch: ${error}`);
      }
    }
    if (!isOpen) {
      return;
    }
    getChatRooms()
  }, [isOpen, pathname])

  useEffect(() => {
    const match = pathname.match(/\/chat\/(\d+)/);
    if (match) {
      const roomId = parseInt(match[1], 10);
      setSelectedRoomId(roomId);
    } else {
      setSelectedRoomId(null)
    }
  }, [pathname])

  return (
    <div className="chatroom-list">
      <div className="chatroom-folder">
        <button onClick={toggleFolder}>
          {isOpen ? <ChevronDownIcon /> : <ChevronRightIcon />}
        </button>
        <p className="chatroom-folder-text">{folderName}</p>
      </div>
      {isOpen && (
        chatRooms.map((chatRoom) => (
          <ChatRoom 
            key={chatRoom.roomId} 
            roomId={chatRoom.roomId} 
            roomName={chatRoom.roomName} 
            isSelected={selectedRoomId === chatRoom.roomId}
            onSelect={() => setSelectedRoomId(chatRoom.roomId)}
          />
        ))
      )}
    </div>
  );
}
