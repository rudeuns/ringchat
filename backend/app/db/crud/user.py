from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.models import User
from app.schemas import UserCreate


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        return user
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading user.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    try:
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return user
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading user.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    try:
        new_user = User(**user_data.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing user.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e
