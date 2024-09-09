from datetime import datetime
from datetime import timedelta
from typing import List
import logging

import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.database import SessionLocal
from app.models.tables import ChatRooms
from app.models.tables import Link_Chatrooms
from app.models.tables import Links
from app.utils.url_processor import is_valid_url
from app.utils.parser import document_parse

router = APIRouter()

logger = logging.getLogger(__name__)

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


def parse_urls_threads(urls):
    with ThreadPoolExecutor() as executor: 
        return list(executor.map(document_parse, urls))
    
    
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
    request: ChatRoomRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    now_utc = datetime.now()
    kst_offset = timedelta(hours=9)
    now_kst = now_utc + kst_offset

    def process_chatroom(): 
        """Links, Chatrooms, Link_Chatrooms 테이블 생성에 관한 트랜잭션 처리 

        Raises:
            HTTPException: 트랜잭션이 정상적으로 처리되지 않으면 rollback 되도록 함

        Returns:
            roomId, urls(dict): Chatrooms 테이블 생성 시 만들어진 roomId와 
                                Links 테이블에 저장할 urls 반환 
        """
        try: 
            # 트랜잭션 시작 
            with db.begin_nested():
                new_chatroom = ChatRooms(
                    user_id=request.userId,
                    created_time=now_kst,
                    folder_id=1,
                    room_name=f'New Chat',
                )
                db.add(new_chatroom)
                db.flush() # new_chatroom의 roomd_id를 얻기 위한 작업 (commit X)
                
                # url 유효성 검사 후 파싱 진행
                is_valid_list = [is_valid_url(url) for url in request.urls]
                
                # 유효하지 않은 url이 첨부된 경우 채팅방 생성 X 
                if not all(is_valid_list): 
                    raise HTTPException(status_code=400, detail="One or more URLs are invalid.")
                
                for url in is_valid_list:
                    try: 
                        link_id = _insert_urls(url, db)
                        link_chatroom = Link_Chatrooms(link_id=link_id, room_id=new_chatroom.room_id)
                        db.add(link_chatroom)
                    except Exception as e:
                        print(f"Failed to insert URL {url}: {e}")
                        raise
                db.commit()
                    
        except Exception as e: 
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        return {"roomId": new_chatroom.room_id, "urls": is_valid_list} 
    
    transaction_result = process_chatroom()
    room_id = transaction_result['roomId']
    urls = transaction_result['urls']
    
    # URL 파싱
    parsed_documents = parse_urls_threads(urls)
    
    # 백그라운드 업데이트(DB) 
    for doc in parsed_documents:
        # TODO: 채팅방 제목을 위해 문서 요약 함수 활용 generate_title(doc.page_content)
        room_name = doc.metadata['title']
        
        background_tasks.add_task(update_linkAndchatrooms_table, 
                                  doc.metadata['source'], doc.metadata['title'], doc.page_content, 
                                  room_id, room_name,
                                  db)
    
    return {"roomId": room_id}

def _insert_urls(url: List[str], db: Session):
    link = db.query(Links).filter(Links.url == url).first()

    # 첨부된적 없는 링크 일 때 저장 
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
        db.flush()

    else: 
        print("This is a URL that has already been attached.")
    
    return link.link_id

def _update_link_table(url, title, content, db: Session): 
    link = db.query(Links).filter(Links.url == url).first()
    if link: 
        link.link_document = content
        link.link_title = title
        db.commit()

def _update_chatrooms_table(room_id, room_name, db: Session): 
    chatrooms = db.query(ChatRooms).filter(ChatRooms.room_id == room_id).first()
    
    if chatrooms: 
        chatrooms.room_name = room_name
        db.commit()
        

async def update_linkAndchatrooms_table(url, titile, content, room_id, room_name, db: Session): 
    try:
        with SessionLocal() as db: 
            _update_link_table(url, titile, content, db) 
            _update_chatrooms_table(room_id, room_name, db)
    except Exception as e: 
        logger.error(f"Failed to update link document for URL {url}: {e}", exc_info=True)
        