from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import UserResponse
import app.db.crud as crud
from app.utils.security import get_current_user_id

router = APIRouter(tags=["me"])


@router.get("/me", response_model=UserResponse)
async def get_user(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await crud.get_user_by_id(db=db, user_id=user_id)
        return UserResponse(id=user.id, email=user.email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while fetching user info.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e
