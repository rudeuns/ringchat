export interface FolderData {
  id: number;
  name: string;
  created_at: string;
  chat_rooms: ChatRoomData[];
}

export interface ChatRoomData {
  id: number;
  name: string;
  is_favorite: boolean;
  created_at: string;
  folder_id: number | null;
}

export interface LinkData {
  id: number;
  url: string;
  title: string;
  link_stat: LinkStatData;
  selected: boolean;
}

export interface LinkStatData {
  average_rating: number;
  rating_count: number;
  attached_count: number;
  favorite_count: number;
}

export interface MessageData {
  id: number;
  content: string;
  is_user_message: boolean;
  created_at: string;
}
