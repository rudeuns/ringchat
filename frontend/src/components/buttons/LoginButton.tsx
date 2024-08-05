'use client'

import { useAuth } from "@/context/AuthContext"

export default function LoginButton() {
  const { testLogin } = useAuth();

  return (
    <div className="btn-container">
      <button className="btn" onClick={testLogin}>
        <p className="btn-text">로그인</p>
      </button>
    </div>
  )
}