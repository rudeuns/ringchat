from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List
from app.db.models import Folder
from app.schemas import FolderCreate, FolderUpdate


async def get_folders_by_user_id(
    db: AsyncSession, user_id: int
) -> List[Folder]:
    try:
        result = await db.execute(
            select(Folder)
            .options(selectinload(Folder.chat_rooms))
            .filter(Folder.user_id == user_id)
            .order_by(Folder.created_at.asc())
        )

        folders = result.scalars().all()

        for folder in folders:
            folder.chat_rooms.sort(
                key=lambda chat_room: chat_room.created_at, reverse=True
            )

        return folders

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading folder.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def get_folder_by_id(db: AsyncSession, folder_id: int) -> Folder:
    try:
        result = await db.execute(
            select(Folder)
            .options(selectinload(Folder.chat_rooms))
            .filter(Folder.id == folder_id)
        )

        folder = result.scalars().first()
        folder.chat_rooms.sort(
            key=lambda chat_room: chat_room.created_at, reverse=True
        )

        return folder

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading folder.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def create_folder(
    db: AsyncSession, folder_data: FolderCreate, user_id: int
) -> Folder:
    try:
        new_folder = Folder(**folder_data.model_dump(), user_id=user_id)
        db.add(new_folder)

        await db.commit()
        await db.refresh(new_folder)

        return new_folder

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing folder.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e


async def update_folder(
    db: AsyncSession, folder: Folder, folder_data: FolderUpdate
) -> Folder:
    try:
        folder.name = folder_data.name

        await db.commit()
        await db.refresh(folder)

        return folder

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing folder.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e


async def delete_folder(db: AsyncSession, folder: Folder):
    try:
        await db.delete(folder)
        await db.commit()

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing folder.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e
