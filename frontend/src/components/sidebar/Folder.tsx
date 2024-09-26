"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";
import { useFolder } from "@/context/FolderContext";
import { ChatRoomData } from "@/lib/interfaces";
import { HiFolder } from "react-icons/hi2";
import { FaFolderOpen } from "react-icons/fa6";
import { HiOutlineDotsVertical } from "react-icons/hi";
import ChatRoom, { ChatRoomNotice } from "@/components/sidebar/ChatRoom";
import { fetchClient } from "@/lib/fetch";

interface FolderProps {
  id: number;
  name: string;
  chatRooms: ChatRoomData[];
}

export default function Folder(props: FolderProps) {
  const { addChatRoomToFolder, setFolders } = useFolder();
  const [isOpen, setIsOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [isMainPage, setIsMainPage] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [folderName, setFolderName] = useState<string>(props.name);
  const [prevFolderName, setPrevFolderName] = useState<string>(props.name);
  const [showMenu, setShowMenu] = useState(false);
  const [menuPos, setMenuPos] = useState({ x: 0, y: 0 });
  const dotIconRef = useRef<HTMLDivElement | null>(null);
  const menuRef = useRef<HTMLUListElement | null>(null);
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const handleToggleFolder = () => {
    setIsOpen(!isOpen);
  };

  const handleClickDotIcon = () => {
    if (dotIconRef.current) {
      if (!showMenu) {
        const pos = dotIconRef.current.getBoundingClientRect();
        setMenuPos({ x: pos.x + 30, y: pos.y - 5 });
        setShowMenu(true);
      } else {
        setShowMenu(false);
      }
    }
  };

  const handleClickOutside = (e: MouseEvent) => {
    if (
      menuRef.current &&
      !menuRef.current.contains(e.target as Node) &&
      dotIconRef.current &&
      !dotIconRef.current.contains(e.target as Node)
    ) {
      setShowMenu(false);
    }
  };

  const handleAddChatRoom = () => {
    router.push(`/main?folderId=${props.id}`);
    setShowMenu(false);
  };

  const handleClickRenameButton = () => {
    setShowMenu(false);
    setIsEditing(true);
    setPrevFolderName(folderName);
  };

  const handleChangeFolderName = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setFolderName(value);
  };

  const handleEnterFolderName = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleRenameFolder();
    }
  };

  const handleRenameFolder = async () => {
    setIsEditing(false);

    if (folderName.trim() !== "") {
      try {
        const res = await fetchClient(`/folders/${props.id}`, {
          method: "PUT",
          body: JSON.stringify({
            name: folderName,
          }),
        });

        const result = await res.json();

        if (res.status == 401) {
          window.location.href = "/";
        } else if (!res.ok) {
          setFolderName(prevFolderName);

          throw new Error(result.detail);
        }
      } catch (error) {
        alert(
          "폴더 이름 수정 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
        );
        console.error(error);
      }
    } else {
      setFolderName(prevFolderName);
    }
  };

  const handleDeleteFolder = async () => {
    setShowMenu(false);

    const isConfirmed = confirm("폴더를 정말 삭제하시겠습니까?");

    if (isConfirmed) {
      try {
        const res = await fetchClient(`/folders/${props.id}`, {
          method: "DELETE",
        });

        const result = await res.json();

        if (res.ok) {
          window.location.reload();
        } else if (res.status == 401) {
          window.location.href = "/";
        } else {
          throw new Error(result.detail);
        }
      } catch (error) {
        alert("폴더 삭제 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
        console.error(error);
      }
    }
  };

  const handleDeleteChatRoom = (
    chatRoomId: number,
    folderId: number | null,
  ) => {
    if (folderId && folderId === props.id) {
      const updatedChatRooms = props.chatRooms.filter(
        (chatRoom) => chatRoom.id !== chatRoomId,
      );

      setFolders((prev) =>
        prev.map((folder) =>
          folder.id === props.id
            ? { ...folder, chat_rooms: updatedChatRooms }
            : folder,
        ),
      );
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const folderIdStr = searchParams.get("folderId");
    if (!folderIdStr || folderIdStr !== props.id.toString()) {
      setIsOpen(false);
      setIsMainPage(false);
      return;
    }

    const match = pathname.match(/\/main\/chat\/(\d+)/);
    if (match) {
      setIsMainPage(false);
      setIsOpen(true);

      if (searchParams.get("isNew")) {
        const folderId = parseInt(folderIdStr, 10);
        const chatRoomId = parseInt(match[1], 10);
        const name = searchParams.get("name") || "New Chat";
        const createdAt = new Date().toISOString();

        const newChatRoom: ChatRoomData = {
          id: chatRoomId,
          folder_id: folderId,
          name: name,
          is_favorite: false,
          created_at: createdAt,
        };

        addChatRoomToFolder(folderId, newChatRoom);
      }
    } else {
      setIsMainPage(true);
      setIsOpen(true);
    }
  }, [pathname, searchParams]);

  return (
    <>
      <div
        className="container-folder"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <div className="container-sidebar-name" onClick={handleToggleFolder}>
          {isOpen ? (
            <FaFolderOpen className="icon-base" />
          ) : (
            <HiFolder className="icon-base" />
          )}
          {isEditing ? (
            <input
              className="input-base  px-2 py-1 rounded-md"
              type="text"
              value={folderName}
              onChange={handleChangeFolderName}
              onKeyDown={handleEnterFolderName}
              onBlur={() => handleRenameFolder()}
              autoFocus
            />
          ) : (
            <p className="text-overflow">{folderName}</p>
          )}
        </div>
        {!isEditing && (
          <div
            className="flex-center"
            onClick={handleClickDotIcon}
            ref={dotIconRef}
          >
            <HiOutlineDotsVertical
              className={`icon-base ${showMenu || isHovered ? "text-primary" : "text-gray-hover"}`}
              strokeWidth={1}
            />
          </div>
        )}
      </div>
      {isOpen && (
        <div className="flex flex-col ms-4">
          {isMainPage && <ChatRoomNotice />}
          {props.chatRooms?.map((chatRoom) => (
            <ChatRoom
              key={chatRoom.id}
              id={chatRoom.id}
              folder_id={chatRoom.folder_id}
              name={chatRoom.name}
              isFavorite={chatRoom.is_favorite}
              onDelete={handleDeleteChatRoom}
            />
          ))}
        </div>
      )}
      {showMenu && (
        <ul
          className="container-menu absolute text-sm "
          style={{
            top: `${menuPos.y}px`,
            left: `${menuPos.x}px`,
          }}
          ref={menuRef}
        >
          <li className="li-menu-default" onClick={handleAddChatRoom}>
            새 채팅방 추가
          </li>
          <li className="li-menu-default" onClick={handleClickRenameButton}>
            폴더 이름 수정
          </li>
          <li
            className="li-menu-base text-red-fill-hover"
            onClick={handleDeleteFolder}
          >
            폴더 삭제
          </li>
        </ul>
      )}
    </>
  );
}
