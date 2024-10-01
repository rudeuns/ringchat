"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useLink } from "@/context/LinkContext";
import { fetchClient } from "@/lib/fetch";
import { LinkData } from "@/lib/interfaces";
import { HiOutlineSearch } from "react-icons/hi";
import { HiOutlineXMark } from "react-icons/hi2";
import Select from "react-select";
import { selectOptions, selectStyles } from "@/components/link/LinkSortingMenu";
import Link from "@/components/link/Link";
import { PiSpinnerGapBold } from "react-icons/pi";

export default function LinkPage() {
  const [hasResult, setHasResult] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [links, setLinks] = useState<LinkData[]>([]);
  const { selectedLinks, setSelectedLinks, addLink } = useLink();
  const router = useRouter();

  const handleChangeQuery = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setQuery(value);
  };

  const handleSearchQuery = async () => {
    if (query.trim() === "") {
      setQuery("");
      setHasResult(null);
      return;
    }

    setHasResult(null);
    setIsLoading(true);

    try {
      const res = await fetchClient(`/links?query=${query}`, {
        method: "GET",
      });

      setIsLoading(false);

      const result = await res.json();
      if (res.ok) {
        const resultLinks: LinkData[] = result.links;

        if (resultLinks && resultLinks.length > 0) {
          const updatedLinks = resultLinks.map((link) => ({
            ...link,
            selected: false,
          }));
          setLinks(updatedLinks);
          setHasResult(true);
        } else {
          setHasResult(false);
        }
      } else {
        throw new Error(result.detail);
      }
    } catch (error) {
      setIsLoading(false);

      alert("링크 검색 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
      console.error(error);
    }
  };

  const handleEnterQuery = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSearchQuery();
    }
  };

  const handleSelectLink = () => {
    selectedLinks.forEach((link) => addLink(link));
    setSelectedLinks([]);
    router.back();
  };

  return (
    <div className="fixed inset-0 flex-center bg-black bg-opacity-80">
      <div className="flex flex-col w-3/5 h-4/5 space-y-2 p-4 bg-white rounded-lg overflow-scroll">
        <HiOutlineXMark
          className="icon-base self-end size-7 text-gray-hover"
          onClick={() => router.back()}
        />
        <div className="relative">
          <input
            className="input-base w-full"
            type="text"
            name="query"
            value={query}
            placeholder="어떤 주제의 링크를 검색하고 싶으신가요?"
            onChange={handleChangeQuery}
            onKeyDown={handleEnterQuery}
            autoComplete="off"
          />
          <HiOutlineSearch
            className="icon-base icon-inside size-6 text-gray-hover"
            onClick={handleSearchQuery}
          />
        </div>
        {isLoading && (
          <PiSpinnerGapBold className="icon-base size-8 self-center text-primary animate-spin" />
        )}
        {hasResult === false && (
          <p className="flex self-center">일치하는 검색 결과가 없습니다.</p>
        )}
        {hasResult === true && (
          <>
            <div className="flex-right-center">
              <Select
                options={selectOptions}
                defaultValue={selectOptions[0]}
                styles={selectStyles}
                isSearchable={false}
                components={{ IndicatorSeparator: () => null }}
              />
            </div>
            <div className="scroll-base divide-y-2 divide-muted border-muted-lg select-text">
              {links.map((link) => (
                <Link
                  key={link.id}
                  id={link.id}
                  url={link.url}
                  title={link.title}
                  link_stat={link.link_stat}
                  selected={link.selected}
                />
              ))}
            </div>
            <button className="btn-fill self-center" onClick={handleSelectLink}>
              선택 완료
            </button>
          </>
        )}
      </div>
    </div>
  );
}
