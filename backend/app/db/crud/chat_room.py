from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional
from app.db.models import ChatRoom, ChatRoomLink
from app.schemas import ChatRoomUpdate
from datetime import datetime, timedelta, timezone


async def get_chat_rooms_by_folder_id(
    db: AsyncSession, user_id: int, folder_id: Optional[int] = None
) -> List[ChatRoom]:
    try:
        query = select(ChatRoom).filter(ChatRoom.user_id == user_id)

        if folder_id is not None:
            if folder_id == 0:
                query = query.filter(ChatRoom.folder_id.is_(None))
            else:
                query = query.filter(ChatRoom.folder_id == folder_id)

        result = await db.execute(query.order_by(ChatRoom.created_at.desc()))
        chat_rooms = result.scalars().all()
        return chat_rooms
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading chat_room.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def create_chat_room(
    db: AsyncSession, user_id: int, folder_id: int, link_ids: List[int]
) -> ChatRoom:
    try:
        kst = timezone(timedelta(hours=9))
        now_in_kst = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

        new_chat_room = ChatRoom(
            user_id=user_id, folder_id=folder_id, name=now_in_kst
        )
        db.add(new_chat_room)
        await db.flush()

        for link_id in link_ids:
            new_chat_room_link = ChatRoomLink(
                chat_room_id=new_chat_room.id, link_id=link_id
            )
            db.add(new_chat_room_link)

        await db.commit()
        await db.refresh(new_chat_room)

        return new_chat_room

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing chat_room.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e


async def get_chat_room_links(
    db: AsyncSession, chat_room_id: int
) -> List[ChatRoomLink]:
    try:
        result = await db.execute(
            select(ChatRoomLink)
            .options(selectinload(ChatRoomLink.link))
            .filter(ChatRoomLink.chat_room_id == chat_room_id)
        )

        chat_room_links = result.scalars().all()
        return chat_room_links

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading chat_room_link.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def get_chat_room_by_id(db: AsyncSession, chat_room_id: int) -> ChatRoom:
    try:
        result = await db.execute(
            select(ChatRoom).filter(ChatRoom.id == chat_room_id)
        )

        chat_room = result.scalars().first()
        return chat_room

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading chat room.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def update_chat_room(
    db: AsyncSession, chat_room: ChatRoom, chat_room_data: ChatRoomUpdate
) -> ChatRoom:
    try:
        print(chat_room_data)
        if chat_room_data.name is not None:
            chat_room.name = chat_room_data.name

        if chat_room_data.is_favorite is not None:
            chat_room.is_favorite = chat_room_data.is_favorite

        await db.commit()
        await db.refresh(chat_room)

        return chat_room

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing chat room.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e


async def delete_chat_room(db: AsyncSession, chat_room: ChatRoom):
    try:
        await db.delete(chat_room)
        await db.commit()

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing chat room.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e
