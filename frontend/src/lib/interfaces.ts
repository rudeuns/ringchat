export interface FolderData {
  folderId: number;
  folderName: string;
}

export interface ChatRoomData {
  roomId: number;
  roomName: string;
  folderId: number;
}

export interface ChatMessageData {
  question: string;
  answer: string;
}

export interface LinkData {
  url: string;
  link_title: string;
  avgScore: number;
  sumUsedNum: number;
  sumBookmark: number;
}