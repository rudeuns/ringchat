from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import app.db.models as models
import app.schemas as schemas
import app.utils.response as response


async def get_user_info_by_email(db: AsyncSession, email: str) -> models.UserInfo:
    try:
        result = await db.execute(
            select(models.UserInfo).filter(models.UserInfo.email == email)
        )
        user_info = result.scalars().first()
    except SQLAlchemyError as e:
        response.handle_db_access_error(
            detail_while="reading user_info", code="DB_READ_ERROR", exception=e
        )

    return user_info


async def create_user_info(
    db: AsyncSession, user_info_data: schemas.UserInfoCreate
) -> models.UserInfo:
    try:
        new_user_info = models.UserInfo(**user_info_data.model_dump())
        db.add(new_user_info)
        await db.commit()
        await db.refresh(new_user_info)
    except SQLAlchemyError as e:
        await db.rollback()
        response.handle_db_access_error(
            detail_while="creating user_info", code="DB_WRITE_ERROR", exception=e
        )

    return new_user_info
