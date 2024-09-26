"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { HiOutlineSearch } from "react-icons/hi";
import { HiOutlineInformationCircle } from "react-icons/hi2";
import { LinkSearchDesc } from "@/components/common/Texts";

export default function LinkModalNav() {
  const [showInfo, setShowInfo] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleOpenModal = () => {
    if (searchParams.get("folderId")) {
      router.push(`/main/link?folderId=${searchParams.get("folderId")}`);
    } else {
      router.push("/main/link");
    }
  };

  return (
    <div className="flex-row flex-right-center space-x-1">
      <button className="btn-stroke" onClick={handleOpenModal}>
        <div className="flex-row flex-center space-x-2">
          <HiOutlineSearch className="icon-base" />
          <p>링크 검색하기</p>
        </div>
      </button>
      <div className="relative">
        <HiOutlineInformationCircle
          className={`icon-base size-6 text-gray hover:text-yellow ${showInfo && "text-yellow"}`}
          onMouseEnter={() => setShowInfo(true)}
          onMouseLeave={() => setShowInfo(false)}
        />
        {showInfo && (
          <div className="absolute left-full bottom-full w-[12rem] px-2 py-4 border-muted-lg shadow-md">
            <LinkSearchDesc />
          </div>
        )}
      </div>
    </div>
  );
}
