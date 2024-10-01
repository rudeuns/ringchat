from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRoomCreate(BaseModel):
    folder_id: Optional[int] = None
    link_ids: List[int]


class ChatRoomUpdate(BaseModel):
    name: Optional[str]
    is_favorite: Optional[bool]


class ChatRoomResponse(BaseModel):
    id: int
    folder_id: Optional[int] = None
    name: str
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRoomListResponse(BaseModel):
    chat_rooms: List[ChatRoomResponse]

    class Config:
        from_attributes = True
