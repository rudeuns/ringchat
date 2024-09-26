"use client";

import { createContext, useContext, useState } from "react";
import { FolderData, ChatRoomData } from "@/lib/interfaces";

interface FolderContextProps {
  folders: FolderData[];
  setFolders: React.Dispatch<React.SetStateAction<FolderData[]>>;
  noFolderChatRooms: ChatRoomData[];
  setNoFolderChatRooms: React.Dispatch<React.SetStateAction<ChatRoomData[]>>;
  isEntering: boolean;
  setIsEntering: React.Dispatch<React.SetStateAction<boolean>>;
  addChatRoomToFolder: (folderId: number, newChatRoom: ChatRoomData) => void;
}

interface FolderProviderProps {
  initFolders: FolderData[];
  initNoFolderChatRooms: ChatRoomData[];
  children: React.ReactNode;
}

const FolderContext = createContext<FolderContextProps | undefined>(undefined);

export function FolderProvider({
  initFolders,
  initNoFolderChatRooms,
  children,
}: FolderProviderProps) {
  const [folders, setFolders] = useState<FolderData[]>(initFolders);
  const [noFolderChatRooms, setNoFolderChatRooms] = useState<ChatRoomData[]>(
    initNoFolderChatRooms,
  );
  const [isEntering, setIsEntering] = useState(false);

  const addChatRoomToFolder = (folderId: number, newChatRoom: ChatRoomData) => {
    setFolders((prev) =>
      prev.map((folder) => {
        if (folder.id === folderId) {
          const updatedChatRooms = folder.chat_rooms
            ? [newChatRoom, ...folder.chat_rooms]
            : [newChatRoom];
          return { ...folder, chat_rooms: updatedChatRooms };
        }
        return folder;
      }),
    );
  };

  return (
    <FolderContext.Provider
      value={{
        folders,
        setFolders,
        noFolderChatRooms,
        setNoFolderChatRooms,
        isEntering,
        setIsEntering,
        addChatRoomToFolder,
      }}
    >
      {children}
    </FolderContext.Provider>
  );
}

export function useFolder() {
  const context = useContext(FolderContext);
  if (context === undefined) {
    throw new Error("useFolder must be used within a FolderProvider");
  }
  return context;
}
