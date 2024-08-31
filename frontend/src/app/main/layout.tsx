import { Suspense } from "react";
import LoadingSideBar from "@/components/loading/LoadingSideBar";
import SideBarServer from "@/components/server/SideBarServer";
import TopBarServer from "@/components/server/TopBarServer";
import { LinkProvider } from "@/context/LinkContext";

export default function MainLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <div className="flex flex-row h-full">
      <Suspense fallback={<LoadingSideBar />}>
        <SideBarServer />
      </Suspense>
      <div className="flex flex-col grow">
        <Suspense fallback={<p className="self-end">...</p>}>
          <TopBarServer />
        </Suspense>
        <LinkProvider>
          {children}
          {modal}
        </LinkProvider>
      </div>
    </div>
  );
}
