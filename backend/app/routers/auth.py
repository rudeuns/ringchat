from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import UserCreate, UserLogin, UserResponse
import app.db.crud as crud
import app.utils.security as security

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=UserResponse)
async def signup(
    user_data: UserCreate, res: Response, db: AsyncSession = Depends(get_db)
):
    ERROR_CODE = None

    try:
        # 이메일 중복 확인
        user = await crud.get_user_by_email(db=db, email=user_data.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered.",
                headers={"X-Error": "EMAIL_EXISTS"},
            )

        # 비밀번호 해싱
        hashed_password = security.get_password_hash(user_data.password)
        user_data.password = hashed_password

        # 새로운 사용자 추가
        new_user = await crud.create_user(db=db, user_data=user_data)

        # JWT 토큰 발급
        ERROR_CODE = "TOKEN_CREATE_ERROR"
        access_token = security.create_access_token(
            data={"sub": str(new_user.id)}
        )
        security.set_access_token_cookie(res=res, access_token=access_token)

        return UserResponse(id=new_user.id, email=new_user.email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while signing up.",
            headers={"X-Error": ERROR_CODE or "SERVER_ERROR"},
        ) from e


@router.post("/login", response_model=UserResponse)
async def login(
    login_data: UserLogin,
    res: Response,
    db: AsyncSession = Depends(get_db),
):
    try:
        # 사용자 정보 조회
        user = await crud.get_user_by_email(db=db, email=login_data.email)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Incorrect email.",
                headers={"X-Error": "INVALID_EMAIL"},
            )

        # 비밀번호 확인
        if not security.verify_password(
            plain_password=login_data.password, hashed_password=user.password
        ):
            raise HTTPException(
                status_code=400,
                detail="Incorrect password.",
                headers={"X-Error": "INVALID_PWD"},
            )

        # JWT 토큰 발급
        access_token = security.create_access_token(data={"sub": str(user.id)})
        security.set_access_token_cookie(res=res, access_token=access_token)

        return UserResponse(id=user.id, email=user.email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while logging in.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.post("/logout")
async def logout(res: Response):
    try:
        # 토큰 삭제
        res.delete_cookie(key="access_token")
        return {"detail": "Logout successful."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while logging out.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e
