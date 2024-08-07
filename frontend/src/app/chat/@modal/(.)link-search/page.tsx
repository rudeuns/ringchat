"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { XMarkIcon } from "@/components/common/Icons";
import InputField from "@/components/common/InputField";
import LinkSearchButton from "@/components/buttons/LinkSearchButton";
import { fetchClient } from "@/lib/fetch";
import { LinkData } from "@/lib/interfaces";
import { useLink } from "@/context/LinkContext";

export default function ModalPage() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [links, setLinks] = useState<LinkData[]>([]);
  const [selectedLinks, setSelectedLinks] = useState<string[]>([]);
  const { inputLinks, addLink, limit } = useLink();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setQuery(value);
  };

  const handleSubmit = async () => {
    try {
      const url = `/api/links?query=${query}`;
      const data = await fetchClient(url, { method: 'GET' });
      setLinks(data);
    } catch (error) {
      console.error(`Error during fetch: ${error}`);
    }
  };

  const handleCheckboxChange = (link: string) => {
    setSelectedLinks((prevSelectedLinks) => {
      const totalLinks = prevSelectedLinks.length + inputLinks.length;

      if (prevSelectedLinks.includes(link)) {
        return prevSelectedLinks.filter((selectedLink) => selectedLink !== link);
      } else if (totalLinks < limit) {
        return [...prevSelectedLinks, link];
      } else {
        alert(`링크는 최대 3개까지 입력 가능합니다.`);
        return prevSelectedLinks;
      }
    });
  };

  const handleSelect = () => {
    selectedLinks.forEach((link) => addLink(link));
    router.back();
  };

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
              name='query'
              value={query}
              handleChange={handleChange}
            />
            <LinkSearchButton onClick={handleSubmit} />
          </div>
          <div className="select-container">
            <select className="select">
              <option value="">별점 높은 순</option>
              <option value="option1">첨부 많은 순</option>
              <option value="option2">저장 많은 순</option>
            </select>
          </div>
          <div className="link-list-container">
            {links.map((link, index) => (
              <div key={index} className="link-item">
                <input
                  type="checkbox"
                  checked={selectedLinks.includes(link.url)}
                  onChange={() => handleCheckboxChange(link.url)}
                  className="link-checkbox"
                />
                <a href={link.url} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="flex"
                >
                  {link.url}
                </a>
                <div className="link-score-container">
                  <div className="link-score-sub-container">
                    <p>별점: {link.avgScore}</p>  
                  </div>
                  <div className="link-score-sub-container">
                    <p>첨부: {link.sumUsedNum}</p>
                  </div>
                  <div className="link-score-sub-container">
                    <p>저장: {link.sumBookmark}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="btn-container">
            <button className="btn" onClick={handleSelect}>
              <p className="btn-text">선택 완료</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
