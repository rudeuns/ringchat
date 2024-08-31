"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { HiChevronUp, HiChevronDown } from "react-icons/hi2";
import { fetchClient } from "@/lib/fetch";

export default function TopBar({ email }: { email: string }) {
  const [showMenu, setShowMenu] = useState(false);
  const router = useRouter();

  const handleToggleMenu = () => {
    setShowMenu(!showMenu);
  };

  const handleLogout = async () => {
    try {
      const res = await fetchClient("/auth/logout", {
        method: "POST",
      });

      if (res.ok) {
        router.push("/");
        return;
      }
    } catch (error) {
      alert(
        "로그아웃 중 예기치 않은 오류가 발생했습니다. 관리자에게 문의하시거나 잠시 후 다시 시도해 주세요.",
      );
      console.log(`Unexpected error occurred while logging out: ${error}`);
    }
  };

  return (
    <div className="relative">
      <div className="flex justify-end items-start h-topbar px-4 py-2">
        <div className="flex-row flex-right-center">
          <p className="p-1">{email}</p>
          {showMenu ? (
            <HiChevronUp className="icon-base" onClick={handleToggleMenu} />
          ) : (
            <HiChevronDown className="icon-base" onClick={handleToggleMenu} />
          )}
        </div>
      </div>
      {showMenu && (
        <ul className="container-menu absolute top-full right-4 shadow-sm">
          <li className="li-menu-base text-gray hover:cursor-not-allowed">
            마이페이지
          </li>
          <li
            className="li-menu-base text-red-fill-hover"
            onClick={handleLogout}
          >
            로그아웃
          </li>
        </ul>
      )}
    </div>
  );
}
