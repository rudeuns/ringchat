'use client';

import { useState } from 'react';
import { ChevronDownIcon, ChevronRightIcon } from '@/components/Icons';

interface ChatListFolderProps {
  name: string;
  // chatList: string[];
}

export function ChatListFolder({ name }: ChatListFolderProps) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleFolder = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex flex-col">
      <div className="chatlist-folder">
        <button onClick={toggleFolder}>
          {isOpen ? <ChevronDownIcon /> : <ChevronRightIcon />}
        </button>
        <p className="mx-2 text-lg">{name}</p>
      </div>
      {isOpen && (
        <>
          <ChatListItem />
          <ChatListItem />
        </>
      )}
    </div>
  );
}

export function ChatListItem() {
  return (
    <div className="chatlist-item">
      <p className="text-base">New Chat</p>
    </div>
  );
}
