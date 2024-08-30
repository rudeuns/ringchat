from pydantic import BaseModel


class UserInfoCreate(BaseModel):
    email: str
    password: str


class UserInfoLogin(BaseModel):
    email: str
    password: str
