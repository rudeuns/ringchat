'use client'

import { useRouter } from "next/navigation"

export default function StartButton() {
  const router = useRouter();

  return (
    <div className="btn-container mb-10">
      <button className="btn" onClick={() => router.push('/chat/0')}>
        <p className="btn-text">대화 시작하기</p>
      </button>
    </div>
  )
}