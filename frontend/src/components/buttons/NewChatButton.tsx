'use client'

import { useRouter } from "next/navigation";

export default function NewChatButton() {
  const router = useRouter();

  return (
    <button className="btn-newchat" onClick={() => router.push('/chat')}>
      <p className="btn-text text-base">+ NEW</p>
    </button>
  );
}
