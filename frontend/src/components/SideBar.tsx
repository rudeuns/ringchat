import { SmallLogo } from '@/components/common/Logos';
import NewChatButton from '@/components/buttons/NewChatButton';
import ChatRoomList from '@/components/ChatRoomList';
import NewFolderButton from '@/components/buttons/NewFolderButton';

export default function SideBar() {
  return (
    <>
      <div className="sidebar-top">
        <SmallLogo />
        <NewChatButton />
      </div>
      <ChatRoomList />
      <div className='sidebar-bottom'>
        <NewFolderButton />
      </div>
    </>
  );
}
