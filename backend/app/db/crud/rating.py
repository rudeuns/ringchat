from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.models import Rating
from app.schemas import RatingUpdate


async def create_or_update_rating(
    db: AsyncSession, rating_data: RatingUpdate
) -> Rating:
    try:
        result = await db.execute(
            select(Rating).filter(Rating.message_id == rating_data.message_id)
        )
        existing_rating = result.scalars().first()

        if not existing_rating:
            new_rating = Rating(**rating_data.model_dump())
            db.add(new_rating)

            await db.commit()
            await db.refresh(new_rating)

            return new_rating
        else:
            existing_rating.score = rating_data.score
            db.add(existing_rating)

            await db.commit()
            await db.refresh(existing_rating)

            return existing_rating

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing rating.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e
