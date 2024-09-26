"use client";

import { useEffect } from "react";
import { fetchClient } from "@/lib/fetch";

export default function InvalidToken() {
  const handleLogout = async () => {
    try {
      const res = await fetchClient("/auth/logout", {
        method: "POST",
      });

      if (res.ok) {
        alert(
          "사용자 인증이 유효하지 않아 자동 로그아웃되었습니다. 다시 로그인해 주세요.",
        );
        window.location.href = "/";
      } else {
        throw new Error("Logout failed.");
      }
    } catch (error) {
      alert(
        "사용자 인증이 유효하지 않아 자동 로그아웃 처리 중 예기치 않은 오류가 발생했습니다. 관리자에게 문의하시거나 잠시 후 다시 시도해 주세요.",
      );
      console.error(`Unexpected error occurred while logging out: ${error}`);
    }
  };

  useEffect(() => {
    handleLogout();
  }, []);

  return (
    <div className="flex flex-center w-full h-full">
      <p className="font-semibold text-2xl">로그인 페이지로 이동중...</p>
    </div>
  );
}
