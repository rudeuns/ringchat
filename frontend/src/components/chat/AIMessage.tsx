"use client";

import { useState, memo } from "react";
import Image from "next/image";
import { HiOutlineStar } from "react-icons/hi2";
import Rating from "@/components/chat/Rating";
import Markdown from "@/components/common/Markdown";
import { fetchClient } from "@/lib/fetch";

type AIMessageProps = {
  id?: number;
  content?: string;
};

const AIMessage: React.FC<AIMessageProps> = memo(({ id, content }) => {
  const [isOpenRating, setIsOpenRating] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);
  const [rating, setRating] = useState<number>(0);

  const handleClickStarIcon = () => {
    setIsOpenRating(!isOpenRating);
  };

  const handleClickRating = async (rating: number) => {
    setRating(rating);
    setToastVisible(true);
    setTimeout(() => {
      setIsOpenRating(false);
    }, 500);
    setTimeout(() => {
      setToastVisible(false);
    }, 4000);

    if (id) {
      try {
        const res = await fetchClient(`/rating`, {
          method: "POST",
          body: JSON.stringify({
            message_id: id,
            score: rating,
          }),
        });

        const result = await res.json();
        if (res.status == 401) {
          window.location.href = "/";
        } else if (!res.ok) {
          throw new Error(result.detail);
        }
      } catch (error) {
        alert(
          "피드백 반영 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
        );
        console.error(error);
      }
    }
  };

  return (
    <div className="flex flex-row justify-start items-start space-x-2 me-10">
      <div className="flex flex-col items-center space-y-1 shrink-0">
        <Image src="/logo.svg" alt="LogoImage" width={30} height={30} />
        <div className="relative">
          <HiOutlineStar
            className={`icon-base size-6 ${isOpenRating ? "text-yellow" : "text-gray hover:text-yellow"}`}
            onClick={handleClickStarIcon}
          />
          {isOpenRating && <Rating onClick={handleClickRating} />}
        </div>
      </div>
      <Markdown content={content} />
      {toastVisible && (
        <div className="flex-row flex-center fixed top-2 right-1/2 translate-x-1/2 px-4 py-2 text-white bg-black bg-opacity-40 rounded-full shadow-md">
          {Array.from({ length: rating }, (_, index) => (
            <HiOutlineStar key={index} className="icon-base" />
          ))}
          <p className="ms-2">피드백 감사합니다!</p>
        </div>
      )}
    </div>
  );
});
AIMessage.displayName = "AIMessage";

export default AIMessage;
