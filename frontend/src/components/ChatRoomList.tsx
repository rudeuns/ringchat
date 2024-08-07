'use client'

import { useEffect, useState } from "react"
import { useAuth } from "@/context/AuthContext";
import ChatRoomFolder from "@/components/ChatRoomFolder"
import { fetchClient } from "@/lib/fetch";
import { FolderData } from "@/lib/interfaces";

export default function ChatRoomList() {
  const { user } = useAuth();
  const [folders, setFolders] = useState<FolderData[]>([]);

  useEffect(() => {
    const getFolders = async () => {
      try {
        const url = `/api/folders?userId=${user?.id}`
        const data = await fetchClient(url, { method: 'GET'})
        setFolders(data)
      } catch (error) {
        console.error(`Error during fetch: ${error}`);
      }
    }
    
    if (user) {
      getFolders()
    }
  }, [user]);

  return (
    <div className="sidebar-mid">
      {folders.map((folder) => (
        <ChatRoomFolder key={folder.folderId} folderId={folder.folderId} folderName={folder.folderName} />
      ))}
    </div>
  )
}