"use client";

import { memo } from "react";

type UserMessageProps = {
  content?: string;
};

const UserMessage: React.FC<UserMessageProps> = memo(({ content }) => {
  return (
    <div className="flex self-end max-w-[40rem] ms-10 px-4 py-2 bg-muted rounded-2xl break-all">
      <p>{content}</p>
    </div>
  );
});
UserMessage.displayName = "UserMessage";

export default UserMessage;
