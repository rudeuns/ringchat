'use client';

import { useAuth } from '@/context/AuthContext';
import { LogoSmall } from '@/components/Logo';
import NewChatButton from '@/components/NewChatButton';
import NewFolderButton from '@/components/NewFolderButton';
import { ChatListFolder } from '@/components/ChatList';

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <div className="sidebar-container">
      {!user ? (
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
      ) : (
        <>
          <div className="sb-logo-container-g">
            <LogoSmall />
            <p className="text-base">로그인이 필요한 서비스입니다.</p>
          </div>
        </>
      )}
    </div>
  );
}
