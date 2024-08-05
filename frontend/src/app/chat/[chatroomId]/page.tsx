'use client'

import Image from "next/image"
import TextareaAutosize from 'react-textarea-autosize';
import SubmitChatButton from '@/components/buttons/SubmitChatButton';

export default function ChatMessagePage() {
  return (
    <>
      <div className="chat-msg-container">
        <div className="chat-question-container">
          <div className="chat-question">question</div>
        </div>
        <div className="chat-answer-container">
          <div className="chat-answer-logo">
            <Image src="/logo.svg" alt="LogoImage" width={40} height={40} />
          </div>
          <div className="chat-answer">answer</div>
        </div>
      </div>
      <div className="chat-input-container">
        <TextareaAutosize 
          className="input-field" 
          placeholder="메세지를 입력해주세요." 
          cacheMeasurements
          maxRows={5}
        />
        <SubmitChatButton />
      </div>
    </>
  )
}