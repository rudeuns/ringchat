"use client";

import { useRouter } from "next/navigation";
import { XMarkIcon } from "@/components/common/Icons";
import InputField from "@/components/common/InputField";
import LinkSearchButton from "@/components/buttons/LinkSearchButton";

export default function ModalPage() {
  const router = useRouter();

  return (
    <div className="modal-container">
      <div className="modal-sub-container">
        <div className="btn-close-container">
          <button onClick={() => router.back()}>
            <XMarkIcon />
          </button>
        </div>
        <div className="modal-link-container">
          <div className="link-search-nav">
            <InputField 
              type="text" 
              placeholder="어떤 주제의 링크를 검색하고 싶으신가요?"
            />
            <LinkSearchButton />
          </div>
          <div className="select-container">
            <select className="select">
              <option value="">별점 높은 순</option>
              <option value="option1">첨부 많은 순</option>
              <option value="option2">저장 많은 순</option>
            </select>
          </div>
          <div className="link-list-container">
            
          </div>
        </div>
      </div>
    </div>
  );
}
