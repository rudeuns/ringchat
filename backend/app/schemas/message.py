from pydantic import BaseModel
from typing import List
from datetime import datetime


class MessageCreate(BaseModel):
    content: str
    is_user_message: bool


class MessageStream(BaseModel):
    user_message: str


class MessageResponse(BaseModel):
    id: int
    content: str
    is_user_message: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
