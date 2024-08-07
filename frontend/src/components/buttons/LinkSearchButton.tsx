interface LinkSearchButtonProps {
  onClick: () => void;
}

export default function LinkSearchButton({ onClick }: LinkSearchButtonProps) {
  return (
    <div className="btn-container ms-5">
      <button className="btn" onClick={onClick}>
        <p className="btn-text">검색</p>
      </button>
    </div>
  )
}