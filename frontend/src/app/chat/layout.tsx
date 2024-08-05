import SideBar from "@/components/SideBar";
import TopBar from "@/components/TopBar";

export default function ChatLayout({
  children, modal
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <div className="full-container">
      <div className="sidebar-container">
        <SideBar />
      </div>
      <div className="main-container">
        <TopBar />
        {children}
        {modal}
      </div>
    </div>
  )
}