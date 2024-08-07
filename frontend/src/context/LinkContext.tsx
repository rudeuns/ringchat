'use client'

import { createContext, ReactNode, useContext, useState } from 'react';

interface LinkContextType {
  inputLinks: string[];
  selectedLinks: string[];
  setInputLinks: (links: string[]) => void;
  setSelectedLinks: (links: string[]) => void;
  addLink: (link: string) => void;
  clearLinks: () => void
  limit: number;
}

const LinkContext = createContext<LinkContextType | undefined>(undefined);

export const LinkProvider = ({ children }: { children: ReactNode }) => {
  const [inputLinks, setInputLinks] = useState<string[]>([]);
  const [selectedLinks, setSelectedLinks] = useState<string[]>([]);
  const limit = 3

  const addLink = (link: string) => {
    if (inputLinks.length + selectedLinks.length < limit) {
      setSelectedLinks((prevLinks) => [...prevLinks, link]);
    }
  };

  const clearLinks = () => {
    setSelectedLinks([]);
  };

  return (
    <LinkContext.Provider value={{ inputLinks, setInputLinks, selectedLinks, setSelectedLinks, addLink, clearLinks, limit }}>
      {children}
    </LinkContext.Provider>
  );
};

export const useLink = () => {
  const context = useContext(LinkContext);
  if (context === undefined) {
    throw new Error('useLink must be used within a LinkProvider');
  }
  return context;
};