import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { fetchEmail, fetchFolders, fetchNoFolderChatRooms } from "@/lib/api";
import { ErrorCode } from "@/lib/fetch";
import { FolderData, ChatRoomData } from "@/lib/interfaces";
import { LinkProvider } from "@/context/LinkContext";
import SideBar from "@/components/sidebar/SideBar";
import TopBar from "@/components/topbar/TopBar";
import InvalidToken from "@/components/common/InvalidToken";

export default async function MainLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  const accessToken = cookies().get("access_token");
  if (!accessToken) {
    redirect("/");
  }

  let email: string, folders: FolderData[], noFolderChatRooms: ChatRoomData[];

  try {
    [email, folders, noFolderChatRooms] = await Promise.all([
      fetchEmail({ accessToken: accessToken.value }),
      fetchFolders({ accessToken: accessToken.value }),
      fetchNoFolderChatRooms({ accessToken: accessToken.value }),
    ]);
  } catch (error) {
    if (error instanceof ErrorCode && error.code === "UNAUTHORIZED") {
      return <InvalidToken />;
    }
    throw new Error(
      `Unexpected error occurred while fetching data in MainLayout: ${error}`,
    );
  }

  return (
    <div className="flex flex-row h-full">
      <SideBar
        initFolders={folders}
        initNoFolderChatRooms={noFolderChatRooms}
      />
      <div className="flex flex-col grow">
        <TopBar email={email} />
        <LinkProvider>
          {children}
          {modal}
        </LinkProvider>
      </div>
    </div>
  );
}
