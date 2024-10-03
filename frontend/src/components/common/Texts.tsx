import Link from "next/link";

export function SmallLogo() {
  return (
    <div className="flex-left-center grow">
      <Link href="/main">
        <h1 className="font-semibold text-xl">RingChat</h1>
      </Link>
    </div>
  );
}

export function LargeLogoDesc() {
  return (
    <div className="flex-col flex-center space-y-8">
      <h1 className="font-extrabold text-5xl text-primary">RingChat</h1>
      <p className="text-lg text-center">
        &quot;링챗&quot;은 참고하고 싶은 문서의 링크를 첨부하면,
        <br />
        이를 바탕으로 최신의 풍부한 답변을 제공하는 챗봇 서비스입니다.
      </p>
    </div>
  );
}

export function LinkSearchDesc() {
  return (
    <div className="flex-center">
      <p className="p-1 text-center">
        링챗 사용자들의
        <br />
        만족도를 기반으로
        <br />
        다양한 링크를 추천
        <br />
        받고, 원하는 링크를
        <br />
        선택할 수 있어요!
      </p>
    </div>
  );
}
