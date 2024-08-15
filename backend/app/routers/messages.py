from datetime import datetime
from datetime import timedelta
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from langchain_core.documents import Document
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tables import Link_Chatrooms
from app.models.tables import Links
from app.models.tables import Messages
from app.models.tables import Vectors
from app.utils.get_langchain_answer import get_langchain_answer

router = APIRouter()


class ChatMessageRequest(BaseModel):
    question: str


class ChatMessageResponse(BaseModel):
    answer: str


class ChatMessage(BaseModel):
    question: str
    answer: str


def format_messages_data(messages):
    messages_data = []
    for message in messages:
        messages_data.append(
            {"question": message.question, "answer": message.answer}
        )

    return messages_data


@router.get("/chatrooms/{roomId}/messages", response_model=List[ChatMessage])
async def get_chat_messages(roomId: int, db: Session = Depends(get_db)):
    messages = db.query(Messages).filter(Messages.room_id == roomId).all()
    if not messages:
        raise HTTPException(
            status_code=404, detail="Room not found or no messages available"
        )

    return messages


@router.post("/chatrooms/{roomId}/messages", response_model=ChatMessageResponse)
async def create_chat_answer(
    roomId: int, request: ChatMessageRequest, db: Session = Depends(get_db)
):
    link_chatrooms = (
        db.query(Link_Chatrooms).filter(Link_Chatrooms.room_id == roomId).all()
    )

    linked_documents = []
    for link_chatroom in link_chatrooms:
        link = (
            db.query(Links)
            .filter(Links.link_id == link_chatroom.link_id)
            .first()
        )
        if link and link.link_document:
            linked_documents.append(
                Document(page_content=link.link_document, title=link.link_title)
            )

    answer = get_langchain_answer(
        linked_documents, request.question, session_id=str(roomId)
    )
    # answer = f"Answer to '{request.question}'"

    now_utc = datetime.now()
    kst_offset = timedelta(hours=9)
    now_kst = now_utc + kst_offset

    new_message = Messages(
        room_id=roomId,
        question=request.question,
        answer=answer,
        created_time=now_kst,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return ChatMessageResponse(answer=answer)
