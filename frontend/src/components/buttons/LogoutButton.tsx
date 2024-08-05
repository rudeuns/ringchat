'use client'

import { useAuth } from "@/context/AuthContext"

export default function LogoutButton() {
  const { logout } = useAuth();

  return (
    <button className="btn-container" onClick={logout}>
      <p className="text-lg">로그아웃</p>
    </button>
  )
}