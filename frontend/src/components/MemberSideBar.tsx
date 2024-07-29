import { LogoSmall } from '@/components/Logo';
import NewChatButton from '@/components/NewChatButton';
import NewFolderButton from '@/components/NewFolderButton';
import { ChatListFolder } from '@/components/ChatList';

export default function MemberSideBar() {
  return (
    <>
      <div className="sb-logo-container-m">
        <LogoSmall />
        <NewChatButton />
      </div>
      <div className="chatlist-container">
        <ChatListFolder name="DEFAULT" />
      </div>
      <NewFolderButton />
    </>
  );
}
