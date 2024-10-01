from pydantic import BaseModel
from datetime import datetime


class RatingUpdate(BaseModel):
    message_id: int
    score: int


class RatingResponse(BaseModel):
    id: int
    message_id: int
    score: int
    create_at: datetime

    class Config:
        from_attributes = True
