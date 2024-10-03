"use client";

import { useState } from "react";
import { useFolder } from "@/context/FolderContext";
import { fetchClient } from "@/lib/fetch";
import { FolderData } from "@/lib/interfaces";
import { HiFolder } from "react-icons/hi2";
import Folder from "@/components/sidebar/Folder";

export default function FolderList() {
  const { folders, setFolders, isEntering, setIsEntering } = useFolder();
  const [folderName, setFolderName] = useState("");

  const handleChangeFolderName = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setFolderName(value);
  };

  const handleCreateFolder = async () => {
    setIsEntering(false);

    if (folderName.trim() !== "") {
      try {
        const res = await fetchClient("/folders", {
          method: "POST",
          body: JSON.stringify({
            name: folderName,
          }),
        });

        const result = await res.json();

        if (res.ok) {
          const newFolder: FolderData = {
            id: result.id,
            name: result.name,
            created_at: result.created_at,
            chat_rooms: result.chat_rooms,
          };

          setFolders((prev) => [...prev, newFolder]);
          setFolderName("");
        } else if (res.status == 401) {
          window.location.href = "/";
        } else {
          throw new Error(result.detail);
        }
      } catch (error) {
        alert("폴더 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
        console.error(error);
      }
    }

    setFolderName("");
  };

  const handleEnterFolderName = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleCreateFolder();
    }
  };

  return (
    <>
      {isEntering && (
        <div className="container-folder">
          <div className="container-sidebar-name">
            <HiFolder className="icon-base" />
            <input
              className="input-base grow px-2 py-1 rounded-md"
              type="text"
              value={folderName}
              onChange={handleChangeFolderName}
              onKeyDown={handleEnterFolderName}
              onBlur={() => handleCreateFolder()}
              autoFocus
            />
          </div>
        </div>
      )}
      {folders?.map((folder) => (
        <Folder
          key={folder.id}
          id={folder.id}
          name={folder.name}
          chatRooms={folder.chat_rooms}
        />
      ))}
    </>
  );
}
