"use client";

export default function ErrorRootPage() {
  return (
    <div className="flex-col flex-center space-y-2 mt-20">
      <p className="font-semibold text-2xl">예기치 못한 오류가 발생했습니다.</p>
      <p className="text-lg">
        문제가 지속될 시, 아래의 이메일로 문제 발생 상황을 보고해주시면 신속히
        조치를 취하겠습니다.
      </p>
      <a>email</a>
    </div>
  );
}
