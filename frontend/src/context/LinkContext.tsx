"use client";

import { createContext, useContext, useState } from "react";

interface LinkContextProps {
  inputLinks: string[];
  setInputLinks: React.Dispatch<React.SetStateAction<string[]>>;
  selectedLinks: string[];
  setSelectedLinks: React.Dispatch<React.SetStateAction<string[]>>;
  limit: number;
  currentLinkNum: () => number;
  addLink: (link: string) => void;
  clearLink: () => void;
}

const LinkContext = createContext<LinkContextProps | undefined>(undefined);

export function LinkProvider({ children }: { children: React.ReactNode }) {
  const [inputLinks, setInputLinks] = useState<string[]>(["", "", ""]);
  const [selectedLinks, setSelectedLinks] = useState<string[]>([]);
  const limit = 3;

  const currentLinkNum = () => {
    return (
      inputLinks.filter((link) => link.trim() !== "").length +
      selectedLinks.length
    );
  };

  const addLink = (link: string) => {
    setInputLinks((prev) => {
      const newLinks = [...prev];
      const index = newLinks.findIndex((link) => link.trim() === "");
      if (index !== -1) {
        newLinks[index] = link;
      }
      return newLinks;
    });
  };

  const clearLink = () => {
    setInputLinks(["", "", ""]);
    setSelectedLinks([]);
  };

  return (
    <LinkContext.Provider
      value={{
        inputLinks,
        setInputLinks,
        selectedLinks,
        setSelectedLinks,
        limit,
        currentLinkNum,
        addLink,
        clearLink,
      }}
    >
      {children}
    </LinkContext.Provider>
  );
}

export const useLink = () => {
  const context = useContext(LinkContext);
  if (context === undefined) {
    throw new Error("useLink must be used within a LinkProvider");
  }
  return context;
};