export function ServiceDesc() {
  return (
    <div className="flex flex-col">
      <Description desc="링챗은 기존 LLM 챗봇에 원하는 문서의 링크를 추가로 제공하여" />
      <Description desc="더 높은 정확도와 신뢰도를 가진 답변을 제공하는 챗봇 서비스입니다." />
    </div>
  )
}

export function LinkSearchDesc() {
  return (
    <div className="flex flex-col">
      <Description desc="원하는 문서의 링크가 없으신가요?" />
      <Description desc="링챗만의 데이터로 선별된 링크를 추천해드려요." />
    </div>
  )
}

export function Description({ desc }: { desc: string}) {
  return (
    <div className="flex place-content-center">
      <p className="text-lg">{desc}</p>
    </div>
  )
}

