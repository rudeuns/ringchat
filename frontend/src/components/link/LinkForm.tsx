"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useLink } from "@/context/LinkContext";
import { fetchClient } from "@/lib/fetch";
import { HiOutlineBackspace } from "react-icons/hi2";
import { PiSpinnerGapBold } from "react-icons/pi";

export default function LinkForm() {
  const { inputLinks, setInputLinks, clearLink, currentLinkNum } = useLink();
  const [progress, setProgress] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const index = parseInt(name);

    setInputLinks((prev) => {
      const newLinks = [...prev];
      newLinks[index] = value;
      return newLinks;
    });
  };

  const handleClickBackspaceIcon = (index: number) => {
    setInputLinks((prev) => {
      const newLinks = [...prev];
      newLinks[index] = "";
      return newLinks;
    });
  };

  const parseLinks = async () => {
    try {
      setProgress(true);

      const res = await fetchClient("/links", {
        method: "POST",
        body: JSON.stringify({
          urls: inputLinks,
        }),
      });

      const result = await res.json();
      if (res.ok) {
        return result.link_ids;
      } else {
        throw new Error(result.detail);
      }
    } catch (error) {
      alert("링크 분석 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
      throw error;
    }
  };

  const createChatRoom = async (linkIds: number[]) => {
    try {
      const folderIdStr = searchParams.get("folderId");
      const folderId = folderIdStr ? parseInt(folderIdStr, 10) : null;

      const res = await fetchClient("/chatrooms", {
        method: "POST",
        body: JSON.stringify({
          folder_id: folderId,
          link_ids: linkIds,
        }),
      });

      const result = await res.json();
      if (res.ok) {
        clearLink();

        const href = `/main/chat/${result.id}?isNew=true&name=${result.name}`;

        if (result.folder_id) {
          router.push(href + `&folderId=${result.folder_id}`);
        } else {
          router.push(href);
        }
      } else if (res.status == 401) {
        window.location.href = "/";
      } else {
        throw new Error(result.detail);
      }
    } catch (error) {
      alert("채팅방 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
      throw error;
    }
  };

  const isValidUrls = () => {
    const hasInvalidUrl = inputLinks.some((url) => {
      if (url.trim() === "") {
        return false;
      }

      try {
        new URL(url);
        return false;
      } catch (error) {
        return true;
      }
    });

    if (hasInvalidUrl) {
      return false;
    } else {
      return true;
    }
  };

  const handleCreateChatRoom = async () => {
    if (currentLinkNum() === 0) {
      alert("최소 1개의 url을 입력해 주세요.");
      return;
    }

    if (!isValidUrls()) {
      alert("url 형식이 유효하지 않습니다. 다시 확인해 주세요.");
      return;
    }

    try {
      const linkIds = await parseLinks();
      await createChatRoom(linkIds);
    } catch (error) {
      setProgress(false);
      console.error(error);
    }
  };

  return (
    <>
      {inputLinks.map((link, index) => (
        <div className="relative mt-4" key={index}>
          <input
            className="input-base w-full pe-10"
            type="url"
            name={`${index}`}
            value={link}
            onChange={handleChangeInput}
            placeholder={`url을 입력해주세요 ${index === 0 ? "(필수)" : "(선택)"}`}
            autoComplete="off"
          />
          <HiOutlineBackspace
            className="icon-base icon-inside size-6 text-gray-hover"
            onClick={() => handleClickBackspaceIcon(index)}
          />
        </div>
      ))}
      <button
        className="btn-fill self-center mt-12"
        onClick={handleCreateChatRoom}
      >
        채팅 시작하기
      </button>

      {progress && (
        <div className="absolute inset-0 flex-center bg-white bg-opacity-50 z-10">
          <div className="flex flex-row items-center space-x-4 p-4 pe-8 bg-white border-muted-xl shadow-lg">
            <PiSpinnerGapBold className="icon-base text-primary animate-spin hover:cursor-default" />
            <p>링크 분석중...</p>
          </div>
        </div>
      )}
    </>
  );
}
