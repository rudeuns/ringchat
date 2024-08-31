from fastapi import APIRouter, Request, Response
import app.utils.security as security
import app.utils.response as response


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/email")
async def get_user_email(req: Request, res: Response):
    # 토큰 유효성 검사
    email = security.verify_access_token(req, res)

    res = response.handle_success(
        detail="Fetching user email successful.", data={"email": email}
    )
    return res
