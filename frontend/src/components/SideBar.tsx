import { SmallLogo } from '@/components/common/Logos';
import NewChatButton from '@/components/buttons/NewChatButton';
import ChatRoomFolder from '@/components/ChatRoomFolder';
import NewFolderButton from '@/components/buttons/NewFolderButton';

export default function SideBar() {
  return (
    <>
      <div className="sidebar-top">
        <SmallLogo />
        <NewChatButton />
      </div>
      <div className="sidebar-mid">
        <ChatRoomFolder name="DEFAULT" />
      </div>
      <div className='sidebar-bottom'>
        <NewFolderButton />
      </div>
    </>
  );
}
