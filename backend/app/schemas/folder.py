from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.chat_room import ChatRoomResponse


class FolderCreate(BaseModel):
    name: str


class FolderUpdate(BaseModel):
    name: str


class FolderResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    chat_rooms: List[ChatRoomResponse]

    class Config:
        from_attributes = True


class FolderListResponse(BaseModel):
    folders: List[FolderResponse]

    class Config:
        from_attributes = True
