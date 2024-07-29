'use client';

import { useAuth } from '@/context/AuthContext';
import MemberSideBar from '@/components/MemberSideBar';
import GuestSideBar from '@/components/GuestSideBar';

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <div className="sidebar-container">
      {user ? <MemberSideBar /> : <GuestSideBar />}
    </div>
  );
}
