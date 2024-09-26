from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import RatingUpdate, RatingResponse
import app.db.crud as crud
from app.utils.security import get_current_user_id

router = APIRouter(tags=["rating"])


@router.post("/rating", response_model=RatingResponse)
async def rate_message(
    rating_data: RatingUpdate,
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        new_rating = await crud.create_or_update_rating(
            db=db, rating_data=rating_data
        )

        return RatingResponse(
            id=new_rating.id,
            message_id=new_rating.message_id,
            score=new_rating.score,
            create_at=new_rating.created_at,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while rating.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e
