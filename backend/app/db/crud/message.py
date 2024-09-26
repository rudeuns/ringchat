from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional
from app.db.models import Message
from app.schemas import MessageCreate


async def get_messages_by_chat_room_id(
    db: AsyncSession, chat_room_id: int, message_num: Optional[int] = None
) -> List[Message]:
    try:
        query = select(Message).filter(Message.chat_room_id == chat_room_id)

        if message_num:
            query = query.order_by(Message.created_at.desc()).limit(message_num)
        else:
            query.order_by(Message.created_at.asc())

        result = await db.execute(query)

        messages = result.scalars().all()

        if message_num:
            messages.reverse()

        return messages

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading message.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def create_message(
    db: AsyncSession, message_data: MessageCreate, chat_room_id: int
) -> Message:
    try:
        new_message = Message(
            **message_data.model_dump(), chat_room_id=chat_room_id
        )
        db.add(new_message)

        await db.commit()
        await db.refresh(new_message)

        return new_message

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing message.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e
