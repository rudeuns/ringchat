import { FolderProvider } from "@/context/FolderContext";
import { ChatRoomData, FolderData } from "@/lib/interfaces";
import SideBarTop from "@/components/sidebar/SideBarTop";
import FolderList from "@/components/sidebar/FolderList";
import NoFolderList from "@/components/sidebar/NoFolderList";

interface SideBarProps {
  initFolders: FolderData[];
  initNoFolderChatRooms: ChatRoomData[];
}

export default function SideBar({
  initFolders,
  initNoFolderChatRooms,
}: SideBarProps) {
  return (
    <FolderProvider
      initFolders={initFolders}
      initNoFolderChatRooms={initNoFolderChatRooms}
    >
      <div className="container-sidebar">
        <SideBarTop />
        <div className="scroll-base">
          <FolderList />
          <NoFolderList />
        </div>
      </div>
    </FolderProvider>
  );
}
