"use client";

import { useState, useEffect } from "react";
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
  const [sortBy, setSortBy] = useState<string>('avgScore');
    
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

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortBy(e.target.value);
    // 정렬 함수 호출
    sortLinks(e.target.value);
  };

  const sortLinks = (sortBy: string) => {
    const sortedLinks = [...links].sort((a, b) => {
      if (sortBy === 'avgScore') return b.avgScore - a.avgScore;
      if (sortBy === 'sumUsedNum') return b.sumUsedNum - a.sumUsedNum;
      if (sortBy === 'sumBookmark') return b.sumBookmark - a.sumBookmark;
      return 0;
    });
    setLinks(sortedLinks);
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
            <select className="select" onChange={handleSortChange} value={sortBy}>
              <option value="avgScore">별점 높은 순</option>
              <option value="sumUsedNum">첨부 많은 순</option>
              <option value="sumBookmark">저장 많은 순</option>
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
                <div>
                  <p className="flex">
                    제목: {link.link_title}
                  </p>
                  <br></br>
                  <a href={link.url} 
                    target="_blank" 
                      rel="noopener noreferrer" 
                      className="flex">
                      URL: {link.url}
                  </a>
                </div>
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
          <div className="flex flex-row justify-center space-x-5">
            <p>더 많은 링크가 필요하신가요?</p>
            <button className="underline underline-offset-2">웹 검색 요청</button>
          </div>
        </div>
      </div>
    </div>
  );
}
