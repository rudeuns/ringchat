import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Request, Response
from fastapi.security import OAuth2PasswordBearer
import app.utils.response as response
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    try:
        hashed_password = pwd_context.hash(password)
    except Exception as e:
        response.handle_server_error(
            detail_while="hashing password",
            code="PWD_HASH_ERROR",
            exception=e,
        )

    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    try:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        response.handle_server_error(
            detail="creating access token",
            code="TOKEN_CREATE_ERROR",
            exception=e,
        )

    return encoded_jwt


def verify_access_token(req: Request, res: Response) -> str:
    access_token = req.cookies.get("access_token")
    if not access_token:
        response.handle_unauthorized_error(detail="No access token provided.")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            res.delete_cookie("access_token")
            response.handle_unauthorized_error(
                detail="Unauthorized access. Email not found."
            )
    except Exception as e:
        res.delete_cookie("access_token")
        response.handle_server_error(
            detail_while="verifying access token",
            code="TOKEN_VERIFY_ERROR",
            exception=e,
        )

    return email
