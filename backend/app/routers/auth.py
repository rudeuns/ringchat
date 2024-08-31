from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
import app.db.crud as crud
import app.schemas as schemas
import app.utils.security as security
import app.utils.response as response
import os
from dotenv import load_dotenv


load_dotenv(".env.local")

COOKIE_EXPIRE_SECOND = os.getenv("COOKIE_EXPIRE_SECOND")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup")
async def signup_for_access_token(
    user_info_data: schemas.UserInfoCreate, db: AsyncSession = Depends(get_db)
):
    # 이메일 중복 확인
    user_info = await crud.get_user_info_by_email(
        db=db, email=user_info_data.email
    )
    if user_info:
        response.handle_bad_request(
            detail="Email already registered.", code="EMAIL_EXISTS"
        )

    # 비밀번호 해싱
    hashed_password = security.get_password_hash(
        password=user_info_data.password
    )
    user_info_data.password = hashed_password

    # 새로운 사용자 정보 추가
    new_user_info = await crud.create_user_info(
        db=db, user_info_data=user_info_data
    )

    # JWT 토큰 발급
    access_token = security.create_access_token(
        data={"sub": new_user_info.email}
    )

    res = response.handle_success(detail="Signup and login successful.")
    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=int(COOKIE_EXPIRE_SECOND),
    )
    return res


@router.post("/login")
async def login_for_access_token(
    login_data: schemas.UserInfoLogin, db: AsyncSession = Depends(get_db)
):
    # 사용자 정보 조회
    user_info = await crud.get_user_info_by_email(db=db, email=login_data.email)
    if not user_info:
        response.handle_bad_request(
            detail="Incorrect email.", code="INVALID_EMAIL"
        )

    # 비밀번호 확인
    if not security.verify_password(
        plain_password=login_data.password, hashed_password=user_info.password
    ):
        response.handle_bad_request(
            detail="Incorrect password.", code="INVALID_PWD"
        )

    # JWT 토큰 발급
    access_token = security.create_access_token(data={"sub": user_info.email})

    res = response.handle_success(detail="Login successful.")
    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=int(COOKIE_EXPIRE_SECOND),
    )
    return res


@router.post("/logout")
async def logout():
    # 쿠키에서 토큰 삭제
    res = response.handle_success(detail="Logout successful.")
    res.delete_cookie(key="access_token")
    return res
