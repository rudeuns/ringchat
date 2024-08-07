'use client'

import { useState, useEffect, useRef } from "react";
import Image from "next/image"
import TextareaAutosize from 'react-textarea-autosize';
import SubmitChatButton from '@/components/buttons/SubmitChatButton';
import { ChatMessageData } from "@/lib/interfaces";
import { fetchClient } from "@/lib/fetch";
import { usePathname } from "next/navigation";

export default function ChatMessagePage() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [roomId, setRoomId] = useState<number | null>(null);
  const pathname = usePathname();
  const messageEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const match = pathname.match(/\/chat\/(\d+)/);
    if (match) {
      setRoomId(parseInt(match[1], 10));
    } else {
      console.error('Invalid roomId in URL');
    }
  }, [pathname])

  useEffect(() => {
    if (roomId) {
      getChatMessages();
    }
  }, [roomId]);

  useEffect(() => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages])

  const getChatMessages = async () => {
    try {
      const url = `/api/chatrooms/${roomId}/messages`
      const data: ChatMessageData[] = await fetchClient(url, { method: 'GET' });

      const storedMessages = data.map(({ question, answer}) => ({ question, answer }))

      setMessages(storedMessages);
    } catch (error) {
      console.error(`Error during fetch: ${error}`);
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = e.target;
    setQuestion(value);
  };

  const handleSubmit = async () => {
    if (!roomId) return;

    try {
      const url = `/api/chatrooms/${roomId}/messages`
      const data = await fetchClient(url, {
        method: 'POST',
        body: JSON.stringify({ question }),
      });

      if (data) {
        setMessages([...messages, { question, answer: data.answer }]);
        setQuestion('');
      }
    } catch (error) {
      console.error(`Error during fetch: ${error}`);
    }
  };

  return (
    <>
      <div className="chat-msg-container">
        {messages.map((msg, index) => (
          <div key={index} className="chat-msg-sub-container" >
            <div className="chat-question-container">
              <div className="chat-question">
                <p className="chat-msg-text">{msg.question}</p>
              </div>
            </div>
            <div className="chat-answer-container">
              <div className="chat-answer-logo">
                <Image src="/logo.svg" alt="LogoImage" width={40} height={40} />
              </div>
              <div className="chat-answer">
                <p className="chat-msg-text">{msg.answer}</p>
              </div>
            </div>
          </div>
        ))}
        <div ref={messageEndRef} />
      </div>
      <div className="chat-input-container">
        <TextareaAutosize 
          className="input-field" 
          placeholder="메세지를 입력해주세요." 
          cacheMeasurements
          maxRows={5}
          value={question}
          onChange={handleChange}
        />
        <SubmitChatButton onClick={handleSubmit}/>
      </div>
    </>
  )
}