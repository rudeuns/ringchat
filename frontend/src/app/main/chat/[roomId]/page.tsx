"use client";

import { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";
import { fetchClient } from "@/lib/fetch";
import { MessageData } from "@/lib/interfaces";
import UserMessage from "@/components/chat/UserMessage";
import AIMessage from "@/components/chat/AIMessage";
import MessageInput from "@/components/chat/MessageInput";

export default function ChatPage() {
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [tempAIMessage, setTempAIMessage] = useState<string | null>(null);
  const messageEndRef = useRef<HTMLDivElement | null>(null);
  const pathname = usePathname();

  const chatRoomId = parseInt(pathname.split("/")[3], 10);

  const fetchMessages = async () => {
    try {
      const res = await fetchClient(
        `/chatrooms/${chatRoomId}/messages?restore=true`,
        {
          method: "GET",
        },
      );

      const result = await res.json();
      if (res.ok) {
        setMessages(result.messages);
      } else if (res.status == 401) {
        window.location.href = "/";
      } else {
        throw new Error(result.detail);
      }
    } catch (error) {
      alert(
        "대화 내용을 가져오는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
      );
      console.error(error);
    }
  };

  const createMessage = async (message: string, is_user_message: boolean) => {
    try {
      const res = await fetchClient(`/chatrooms/${chatRoomId}/messages`, {
        method: "POST",
        body: JSON.stringify({
          content: message,
          is_user_message: is_user_message,
        }),
      });

      const result = await res.json();
      if (res.ok) {
        const newMessage: MessageData = {
          id: result.id,
          content: result.content,
          is_user_message: result.is_user_message,
          created_at: result.created_at,
        };
        setMessages((prev) => [...prev, newMessage]);
      } else if (res.status == 401) {
        window.location.href = "/";
      } else {
        throw new Error(result.detail);
      }
    } catch (error) {
      throw error;
    }
  };

  const handleSendMessage = async (userMessage: string) => {
    try {
      await createMessage(userMessage, true);

      setTempAIMessage("");

      const res = await fetchClient(
        `/chatrooms/${chatRoomId}/messages/stream`,
        {
          method: "POST",
          body: JSON.stringify({
            user_message: userMessage,
          }),
        },
      );

      if (!res.ok || !res.body) {
        throw new Error();
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      let aiMessage = "";
      let done = false;

      while (!done) {
        messageEndRef.current?.scrollIntoView({ behavior: "smooth" });

        const { value, done: readerDone } = await reader.read();
        if (readerDone) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        aiMessage = aiMessage + chunk;
        setTempAIMessage((prev) => (prev ? prev + chunk : chunk));
      }

      await createMessage(aiMessage, false);
      setTempAIMessage(null);
    } catch (error) {
      alert("메세지 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
      console.error(error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <>
      <div className="scroll-base space-y-5 px-10 py-4 select-text">
        {messages.map((message) =>
          message.is_user_message ? (
            <UserMessage key={message.id} content={message.content} />
          ) : (
            <AIMessage
              key={message.id}
              id={message.id}
              content={message.content}
            />
          ),
        )}
        {tempAIMessage === "" ? (
          <AIMessage content="답변 생성중..." />
        ) : (
          tempAIMessage !== null && <AIMessage content={tempAIMessage} />
        )}
        <div ref={messageEndRef} />
      </div>
      <MessageInput onSendMessage={handleSendMessage} />
    </>
  );
}
