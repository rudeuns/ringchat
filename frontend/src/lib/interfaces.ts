export interface FolderData {
  folderId: number;
  folderName: string;
}

export interface ChatRoomData {
  roomId: number;
  roomName: string;
}

export interface ChatMessageData {
  question: string;
  answer: string;
}

export interface LinkData {
  url: string;
  avgScore: number;
  sumUsedNum: number;
  sumBookmark: number;
}