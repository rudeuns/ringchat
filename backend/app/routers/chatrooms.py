from datetime import datetime
from datetime import timedelta
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tables import ChatRooms
from app.models.tables import Link_Chatrooms
from app.models.tables import Links
from app.models.tables import Vectors

router = APIRouter()


class ChatRoom(BaseModel):
    roomId: int
    roomName: str
    folderId: int


class ChatRoomRequest(BaseModel):
    userId: int
    urls: List[str]


class ChatRoomResponse(BaseModel):
    roomId: int


def format_chatrooms_data(chatrooms):
    chatrooms_data = []
    for chatroom in chatrooms:
        chatrooms_data.append(
            {
                "roomId": int(chatroom.room_id),
                "roomName": chatroom.room_name,
                "folderId": int(chatroom.folder_id),
            }
        )

    return chatrooms_data


@router.get("/chatrooms", response_model=List[ChatRoom])
async def get_chatrooms(folderId: int, db: Session = Depends(get_db)):
    chatrooms = (
        db.query(ChatRooms).filter(ChatRooms.folder_id == folderId).all()
    )
    if not chatrooms:
        raise HTTPException(status_code=404, detail="Chatrooms not found")

    return format_chatrooms_data(chatrooms)


@router.post("/chatrooms", response_model=ChatRoomResponse)
async def create_chatroom(
    request: ChatRoomRequest, db: Session = Depends(get_db)
):
    now_utc = datetime.now()
    kst_offset = timedelta(hours=9)
    now_kst = now_utc + kst_offset

    new_chatroom = ChatRooms(
        user_id=request.userId,
        created_time=now_kst,
        folder_id=1,
        room_name=f'New Chat\n{now_kst.strftime("%Y-%m-%d %H:%M:%S")}',
    )
    db.add(new_chatroom)
    db.commit()
    db.refresh(new_chatroom)

    # TODO: URL 파싱 및 저장을 백그라운드 작업으로 추가
    # background_tasks.add_task(parse_and_save_urls, request.urls, db)

    parse_and_save_urls(request.urls, new_chatroom.room_id, db)

    return {"roomId": new_chatroom.room_id}


def parse_and_save_urls(urls: List[str], room_id: int, db: Session):
    for url in urls:
        link = db.query(Links).filter(Links.url == url).first()

        if not link:
            link = Links(
                url=url,
                link_title="Title Placeholder",
                last_updated=datetime.now(),
                sum_bookmark=0,
                avg_score=0.0,
                sum_used_num=0,
            )
            db.add(link)
            db.commit()
            db.refresh(link)

        link_chatroom = Link_Chatrooms(link_id=link.link_id, room_id=room_id)

        db.add(link_chatroom)
        db.commit()
        db.refresh(link_chatroom)
