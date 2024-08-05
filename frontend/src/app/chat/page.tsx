import { LargeLogo } from "@/components/common/Logos"
import { ServiceDesc, LinkSearchDesc } from "@/components/common/Descriptions"
import InputField from "@/components/common/InputField";
import LinkSearchNavButton from "@/components/buttons/LinkSearchNavButton";
import StartButton from "@/components/buttons/StartButton";

export default function ChatPage() {
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
            <InputField type="url" placeholder="url을 입력해주세요." />
            <InputField type="url" placeholder="url을 입력해주세요." />
            <InputField type="url" placeholder="url을 입력해주세요." />
          </div>
        </div>
        <StartButton />
      </div>
    </div>
  )
}