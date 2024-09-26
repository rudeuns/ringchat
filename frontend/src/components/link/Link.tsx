"use client";

import { useState } from "react";
import { useLink } from "@/context/LinkContext";
import { LinkStatData } from "@/lib/interfaces";
import {
  HiOutlineCheck,
  HiOutlineStar,
  HiOutlineLink,
  HiOutlineBookmark,
  HiArrowTopRightOnSquare,
} from "react-icons/hi2";

interface LinkProps {
  id: number;
  url: string;
  title: string;
  link_stat: LinkStatData;
  selected: boolean;
}

export default function Link(props: LinkProps) {
  const { currentLinkNum, limit, setSelectedLinks } = useLink();
  const [isSelected, setIsSelected] = useState(props.selected);

  const formatNum = (num: number) => {
    if (num >= 1_000_000) {
      return (num / 1_000_000).toFixed(0) + "M";
    } else if (num >= 1_000) {
      return (num / 1_000).toFixed(0) + "K";
    } else {
      return num.toString();
    }
  };

  const handleClickCheckbox = () => {
    if (isSelected) {
      setSelectedLinks((prev) => prev.filter((link) => link !== props.url));
    } else {
      if (currentLinkNum() >= limit) {
        alert(`링크는 최대 ${limit}개까지 입력 가능합니다.`);
        return;
      }
      setSelectedLinks((prev) => [...prev, props.url]);
    }
    setIsSelected(!isSelected);
  };

  return (
    <div
      className={`flex-row flex-left-center space-x-4 p-2 ${isSelected && "bg-muted"}`}
    >
      <div
        className={`flex-center p-px border-2 rounded-sm ${isSelected ? "bg-primary border-primary" : "border-gray"}`}
      >
        <HiOutlineCheck
          className={`icon-base size-4 ${isSelected ? "text-white" : "text-transparent"}`}
          strokeWidth={3}
          onClick={() => handleClickCheckbox()}
        />
      </div>
      <div className="flex flex-col flex-1">
        <p className="text-xs text-primary-light break-all">{props.url}</p>
        <p className="break-words">{props.title}</p>
      </div>
      <div className="flex-row flex-left-center shrink-0 text-sm text-primary-light">
        <div className="container-stat">
          <HiOutlineStar className="icon-base hover:cursor-default" />
          <p>{props.link_stat.average_rating.toFixed(1)}</p>
        </div>
        <div className="container-stat">
          <HiOutlineLink className="icon-base hover:cursor-default" />
          <p>{formatNum(props.link_stat.attached_count)}</p>
        </div>
        <div className="container-stat">
          <HiOutlineBookmark className="icon-base hover:cursor-default" />
          <p>{formatNum(props.link_stat.favorite_count)}</p>
        </div>
      </div>
      <a href={props.url} target="_blank" rel="noopener noreferrer">
        <HiArrowTopRightOnSquare className="icon-base size-6 text-gray-hover" />
      </a>
    </div>
  );
}
