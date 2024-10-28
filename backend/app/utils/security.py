import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Request, Response, HTTPException
from app.utils.config import get_env

JWT_SECRET_KEY = get_env("JWT_SECRET_KEY")
ALGORITHM = get_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = float(
    get_env("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
)
COOKIE_EXPIRE_SECOND = int(get_env("COOKIE_EXPIRE_SECOND", 86400))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def set_access_token_cookie(res: Response, access_token: str):
    secure = True if get_env("ENVIRONMENT") == "production" else False

    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=secure,
        max_age=COOKIE_EXPIRE_SECOND,
    )


def get_current_user_id(req: Request) -> int:
    try:
        access_token = req.cookies.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=401,
                detail="No access token provided.",
                headers={"X-Error": "UNAUTHORIZED"},
            )

        payload = jwt.decode(
            access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        return int(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access.",
            headers={"X-Error": "UNAUTHORIZED"},
        ) from e
