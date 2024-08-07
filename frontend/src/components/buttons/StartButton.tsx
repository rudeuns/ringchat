interface StartButtonProps {
  onClick: () => void;
}

export default function StartButton({ onClick }: StartButtonProps) {
  return (
    <div className="btn-container mb-10">
      <button className="btn" onClick={onClick}>
        <p className="btn-text">대화 시작하기</p>
      </button>
    </div>
  )
}