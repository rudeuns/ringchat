'use client';

import { useState } from 'react';
import { ChevronDownIcon, ChevronRightIcon } from '@/components/common/Icons';
import ChatRoom from '@/components/ChatRoom';

interface ChatRoomFolderProps {
  name: string;
  // chatRoomList: ChatRoomProps[];
}

export default function ChatRoomFolder({ name }: ChatRoomFolderProps) {
  const [isOpen, setIsOpen] = useState(true);

  const toggleFolder = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chatroom-list">
      <div className="chatroom-folder">
        <button onClick={toggleFolder}>
          {isOpen ? <ChevronDownIcon /> : <ChevronRightIcon />}
        </button>
        <p className="chatroom-folder-text">{name}</p>
      </div>
      {isOpen && (
        <>
          <ChatRoom name="New Chat 1" id="1"/>
          <ChatRoom name="New Chat 2" id="2" />
        </>
      )}
    </div>
  );
}
