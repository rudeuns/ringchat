interface SubmitChatButtonProps {
  onClick: () => void;
}

export default function SubmitChatButton({ onClick }: SubmitChatButtonProps) {
  return (
    <div className="btn-container flex-col justify-end">
      <button className="btn" onClick={onClick}>
        <p className="btn-text">전송</p>
      </button>
    </div>
  )
}