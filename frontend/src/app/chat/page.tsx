'use client'

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { LargeLogo } from "@/components/common/Logos";
import { ServiceDesc, LinkSearchDesc } from "@/components/common/Descriptions";
import InputField from "@/components/common/InputField";
import LinkSearchNavButton from "@/components/buttons/LinkSearchNavButton";
import StartButton from "@/components/buttons/StartButton";
import { fetchClient } from '@/lib/fetch';
import { useRouter } from 'next/navigation';
import { useLink } from '@/context/LinkContext';

export default function ChatPage() {
  const [urls, setUrls] = useState({ url1: '', url2: '', url3: '' });
  const { setInputLinks, selectedLinks, clearLinks, limit } = useLink();
  const { user } = useAuth(); 
  const router = useRouter();

  useEffect(() => {
    setInputLinks(Object.values(urls).filter(url => url !== ''));
  }, [urls]);

  useEffect(() => {
    if (selectedLinks.length > 0) {
      setUrls((prevUrls) => {
        const newUrls = { ...prevUrls };
        let index = 0;

        for (let i = 0; i < limit; i++) {
          const key = `url${i + 1}` as keyof typeof urls;
          if (!newUrls[key] && index < selectedLinks.length) {
            newUrls[key] = selectedLinks[index];
            index++;
          }
        }

        return newUrls;
      });
      clearLinks();
    }
  }, [selectedLinks]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUrls((prevState) => ({ 
      ...prevState, 
      [name]: value 
    }));
  };

  const handleSubmit = async () => {
    try {
      const url = `/api/chatrooms`;
      const data = await fetchClient(url, {
        method: 'POST',
        body: JSON.stringify({
          userId: user?.id,
          urls: Object.values(urls).filter(url => url !== ''),
        }),
      });
      
      const roomId = data.roomId;
      if (Number.isInteger(roomId)) {
        router.push(`/chat/${roomId}`);
      } else {
        console.error(`Invalid chatroomId: ${roomId}`);
      }
    } catch (error) {
      console.error(`Error during fetch: ${error}`);
    }
  };

  return (
    <div className="chat-main-scroll">
      <div className="chat-main-container">
        <div className="logo-desc">
          <LargeLogo />
          <ServiceDesc />
        </div>
        <div className="chat-main-sub-container">
          <div className="link-search-nav">
            <LinkSearchDesc />
            <LinkSearchNavButton />
          </div>
          <div className="link-input-container">
            <div className="link-input-notice">
              <p>링크는 최대 3개까지 입력 가능합니다.</p>
            </div>
            <InputField 
              type="url" 
              placeholder="url을 입력해주세요." 
              name="url1" 
              value={urls.url1} 
              handleChange={handleChange} 
            />
            <InputField 
              type="url" 
              placeholder="url을 입력해주세요." 
              name="url2" 
              value={urls.url2} 
              handleChange={handleChange} 
            />
            <InputField 
              type="url" 
              placeholder="url을 입력해주세요." 
              name="url3" 
              value={urls.url3} 
              handleChange={handleChange} 
            />
          </div>
        </div>
        <StartButton onClick={handleSubmit} />
      </div>
    </div>
  )
}