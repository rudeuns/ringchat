"use client";

import { useState, useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { useFolder } from "@/context/FolderContext";
import { ChatRoomData } from "@/lib/interfaces";
import ChatRoom, { ChatRoomNotice } from "@/components/sidebar/ChatRoom";

export default function NoFolderList() {
  const { noFolderChatRooms, setNoFolderChatRooms } = useFolder();
  const [isMainPage, setIsMainPage] = useState(true);
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const handleDeleteChatRoom = (
    chatRoomId: number,
    folderId: number | null,
  ) => {
    if (folderId === null) {
      setNoFolderChatRooms((prev) =>
        prev.filter((chatRoom) => chatRoom.id !== chatRoomId),
      );
    }
  };

  useEffect(() => {
    if (searchParams.get("folderId")) {
      setIsMainPage(false);
      return;
    }

    const match = pathname.match(/\/main\/chat\/(\d+)/);
    if (match) {
      setIsMainPage(false);

      if (searchParams.get("isNew")) {
        const chatRoomId = parseInt(match[1], 10);
        const name = searchParams.get("name") || "New Chat";
        const createdAt = new Date().toISOString();

        const newChatRoom: ChatRoomData = {
          id: chatRoomId,
          folder_id: null,
          name: name,
          is_favorite: false,
          created_at: createdAt,
        };

        setNoFolderChatRooms((prev) => [newChatRoom, ...prev]);
      }
    } else {
      setIsMainPage(true);
    }
  }, [pathname, searchParams]);

  return (
    <>
      {isMainPage && <ChatRoomNotice />}
      {noFolderChatRooms?.map((chatRooms) => (
        <ChatRoom
          key={chatRooms.id}
          id={chatRooms.id}
          folder_id={chatRooms.folder_id}
          name={chatRooms.name}
          isFavorite={chatRooms.is_favorite}
          onDelete={handleDeleteChatRoom}
        />
      ))}
    </>
  );
}
