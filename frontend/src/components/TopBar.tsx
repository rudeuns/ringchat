'use client'

import { useAuth } from "@/context/AuthContext"
import LogoutButton from "@/components/buttons/LogoutButton"

export default function TopBar() {
  const { user } = useAuth();

  return (
    <div className="topbar">
      <p className="text-lg">{user?.email}</p>
      <p className="text-lg">|</p>
      <LogoutButton />
    </div>
  )
}