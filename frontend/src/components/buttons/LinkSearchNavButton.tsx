import Link from "next/link"

export default function LinkSearchNavButton() {
  return (
    <Link href="/chat/link-search" className="btn-container flex-col">
      <div className="btn">
        <p className="btn-text">링크 검색하기</p>
      </div>
    </Link>
  )
}