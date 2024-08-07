import Link from "next/link";

export default function NewChatButton() {
  return (
    <Link href="/chat" className="btn-newchat">
      <p className="btn-text text-base">+ NEW</p>
    </Link>
  );
}
