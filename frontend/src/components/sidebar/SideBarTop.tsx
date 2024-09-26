"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useFolder } from "@/context/FolderContext";
import { SmallLogo } from "@/components/common/Texts";
import {
  HiOutlinePencilSquare,
  HiPencilSquare,
  HiOutlineFolderPlus,
  HiFolderPlus,
} from "react-icons/hi2";

export default function SideBarTop() {
  const { setIsEntering } = useFolder();
  const [isHoveredFolderIcon, setIsHoveredFolderIcon] = useState(false);
  const [isHoveredPencilIcon, setIsHoveredPencilIcon] = useState(false);
  const router = useRouter();

  const handleClickFolderIcon = () => {
    setIsEntering(true);
  };

  const handleClickPencilIcon = () => {
    router.push("/main");
  };

  return (
    <div className="container-sidebar-top">
      <SmallLogo />
      <div
        className="flex-center"
        onMouseEnter={() => setIsHoveredFolderIcon(true)}
        onMouseLeave={() => setIsHoveredFolderIcon(false)}
        onClick={handleClickFolderIcon}
      >
        {isHoveredFolderIcon ? (
          <HiFolderPlus className="icon-base size-6" />
        ) : (
          <HiOutlineFolderPlus className="icon-base size-6" />
        )}
      </div>
      <div
        className="flex-center"
        onMouseEnter={() => setIsHoveredPencilIcon(true)}
        onMouseLeave={() => setIsHoveredPencilIcon(false)}
        onClick={handleClickPencilIcon}
      >
        {isHoveredPencilIcon ? (
          <HiPencilSquare className="icon-base size-6" />
        ) : (
          <HiOutlinePencilSquare className="icon-base size-6" />
        )}
      </div>
    </div>
  );
}
