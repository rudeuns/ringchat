"use client";

import { useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import { HiOutlineArrowUpCircle } from "react-icons/hi2";

interface MessageInputProps {
  onSendMessage: (message: string) => void;
}

export default function MessageInput({ onSendMessage }: MessageInputProps) {
  const [inputMessage, setInputMessage] = useState<string>("");
  const [isComposing, setIsComposing] = useState(false);

  const handleChangeInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = e.target;
    setInputMessage(value);
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() !== "") {
      onSendMessage(inputMessage.trim());
    }
    setInputMessage("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      if (isComposing) return;
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleCompositionStart = () => {
    setIsComposing(true);
  };

  const handleCompositionEnd = () => {
    setIsComposing(false);
  };

  return (
    <div className="flex flex-row items-end space-x-4 mx-10 mt-4 mb-6">
      <TextareaAutosize
        className="input-base grow min-h-12"
        placeholder="링챗에게 질문하기"
        cacheMeasurements
        maxRows={5}
        value={inputMessage}
        onChange={handleChangeInput}
        onKeyDown={handleKeyDown}
        onCompositionStart={handleCompositionStart}
        onCompositionEnd={handleCompositionEnd}
        autoFocus
      />
      <HiOutlineArrowUpCircle
        className="icon-base size-8 text-gray-hover"
        onClick={handleSendMessage}
      />
    </div>
  );
}
