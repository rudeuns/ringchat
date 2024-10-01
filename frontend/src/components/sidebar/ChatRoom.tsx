"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter, usePathname } from "next/navigation";
import { HiOutlineDotsVertical } from "react-icons/hi";
import {
  HiOutlineChatBubbleOvalLeftEllipsis,
  HiChatBubbleOvalLeftEllipsis,
  HiBookmark,
  HiOutlineChatBubbleOvalLeft,
} from "react-icons/hi2";
import { fetchClient } from "@/lib/fetch";

interface ChatRoomProps {
  id: number;
  folder_id: number | null;
  name: string;
  isFavorite: boolean;
  onDelete: (chatRoomId: number, folderId: number | null) => void;
}

export default function ChatRoom(props: ChatRoomProps) {
  const [isFavorite, setIsFavorite] = useState(props.isFavorite);
  const [isOpen, setIsOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [chatRoomName, setChatRoomName] = useState<string>(props.name);
  const [prevChatRoomName, setPrevChatRoomName] = useState<string>(props.name);
  const [showMenu, setShowMenu] = useState(false);
  const [menuPos, setMenuPos] = useState({ x: 0, y: 0 });
  const dotIconRef = useRef<HTMLDivElement | null>(null);
  const menuRef = useRef<HTMLUListElement | null>(null);
  const router = useRouter();
  const pathname = usePathname();

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

  const handleOpenChatRoom = () => {
    if (props.folder_id) {
      router.push(`/main/chat/${props.id}?folderId=${props.folder_id}`);
    } else {
      router.push(`/main/chat/${props.id}`);
    }
  };

  const handleSetFavorite = async () => {
    setShowMenu(false);

    try {
      const res = await fetchClient(`/chatrooms/${props.id}`, {
        method: "PUT",
        body: JSON.stringify({
          name: null,
          is_favorite: !isFavorite,
        }),
      });

      const result = await res.json();

      if (res.ok) {
        setIsFavorite(!isFavorite);
      } else if (res.status == 401) {
        window.location.href = "/";
      } else {
        throw new Error(result.detail);
      }
    } catch (error) {
      alert(
        "즐겨찾기 설정 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
      );
      console.error(error);
    }
  };

  const handleClickRenameButton = () => {
    setShowMenu(false);
    setIsEditing(true);
    setPrevChatRoomName(chatRoomName);
  };

  const handleChangeChatRoomName = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setChatRoomName(value);
  };

  const handleEnterChatRoomName = (
    e: React.KeyboardEvent<HTMLInputElement>,
  ) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleRenameChatRoom();
    }
  };

  const handleRenameChatRoom = async () => {
    setIsEditing(false);

    if (chatRoomName.trim() !== "") {
      try {
        const res = await fetchClient(`/chatrooms/${props.id}`, {
          method: "PUT",
          body: JSON.stringify({
            name: chatRoomName,
            is_favorite: null,
          }),
        });

        const result = await res.json();

        if (res.status == 401) {
          window.location.href = "/";
        } else if (!res.ok) {
          setChatRoomName(prevChatRoomName);

          throw new Error(result.detail);
        }
      } catch (error) {
        alert(
          "채팅방 이름 수정 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
        );
        console.error(error);
      }
    } else {
      setChatRoomName(prevChatRoomName);
    }
  };

  const handleDeleteChatRoom = async () => {
    setShowMenu(false);

    const isConfirmed = confirm("채팅방을 정말 삭제하시겠습니까?");

    if (isConfirmed) {
      try {
        const res = await fetchClient(`/chatrooms/${props.id}`, {
          method: "DELETE",
        });

        const result = await res.json();

        if (res.ok) {
          props.onDelete(props.id, props.folder_id);
        } else if (res.status == 401) {
          window.location.href = "/";
        } else {
          throw new Error(result.detail);
        }
      } catch (error) {
        alert(
          "채팅방 삭제 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
        );
        console.error(error);
      }
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const match = pathname.match(/\/main\/chat\/(\d+)/);
    if (match && parseInt(match[1], 10) === props.id) {
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }
  }, [pathname]);

  return (
    <>
      <div
        className={`container-chatroom ${isOpen ? "font-medium shadow-md" : "hover:font-medium hover:shadow-md"}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <div className="container-sidebar-name" onClick={handleOpenChatRoom}>
          {isOpen ? (
            <HiChatBubbleOvalLeftEllipsis className="icon-base" />
          ) : (
            <HiOutlineChatBubbleOvalLeftEllipsis className="icon-base" />
          )}
          {isEditing ? (
            <input
              className="input-base  px-2 py-1 rounded-md"
              type="text"
              value={chatRoomName}
              onChange={handleChangeChatRoomName}
              onKeyDown={handleEnterChatRoomName}
              onBlur={() => handleRenameChatRoom()}
              autoFocus
            />
          ) : (
            <p className="text-overflow">{chatRoomName}</p>
          )}
        </div>
        {!isEditing && isFavorite && (
          <HiBookmark className="icon-base text-red hover:cursor-default" />
        )}
        {!isEditing && (
          <div
            className="flex-center"
            onClick={handleClickDotIcon}
            ref={dotIconRef}
          >
            <HiOutlineDotsVertical
              className={`icon-base ${showMenu || isHovered ? "text-black" : "text-gray-hover"}`}
              strokeWidth={1}
            />
          </div>
        )}
      </div>
      {showMenu && (
        <ul
          className="container-menu absolute text-sm "
          style={{
            top: `${menuPos.y}px`,
            left: `${menuPos.x}px`,
          }}
          ref={menuRef}
        >
          <li className="li-menu-default" onClick={handleSetFavorite}>
            즐겨찾기 설정/해제
          </li>
          <li className="li-menu-default" onClick={handleClickRenameButton}>
            채팅방 이름 수정
          </li>
          <li
            className="li-menu-base text-red-fill-hover"
            onClick={handleDeleteChatRoom}
          >
            채팅방 삭제
          </li>
        </ul>
      )}
    </>
  );
}

export function ChatRoomNotice() {
  return (
    <div className="container-chatroom font-medium shadow-md">
      <div className="container-sidebar-name hover:cursor-default">
        <HiOutlineChatBubbleOvalLeft className="icon-base hover:cursor-default" />
        <p className="font-medium">채팅을 시작해주세요</p>
      </div>
    </div>
  );
}
