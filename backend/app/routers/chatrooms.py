from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import (
    ChatRoomListResponse,
    ChatRoomResponse,
    ChatRoomCreate,
    ChatRoomUpdate,
)
import app.db.crud as crud
from app.utils.security import get_current_user_id
from typing import Optional

router = APIRouter(tags=["chatrooms"])


@router.get("/chatrooms", response_model=ChatRoomListResponse)
async def get_chatrooms(
    folder_id: Optional[int] = Query(None, alias="folderId"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        chat_rooms = await crud.get_chat_rooms_by_folder_id(
            db=db, user_id=user_id, folder_id=folder_id
        )

        return ChatRoomListResponse(chat_rooms=chat_rooms)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while fetching chat rooms.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.post("/chatrooms", response_model=ChatRoomResponse)
async def create_chat_room(
    chat_room_data: ChatRoomCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        new_chat_room = await crud.create_chat_room(
            db=db,
            user_id=user_id,
            folder_id=chat_room_data.folder_id,
            link_ids=chat_room_data.link_ids,
        )

        return ChatRoomResponse(
            id=new_chat_room.id,
            folder_id=new_chat_room.folder_id,
            name=new_chat_room.name,
            created_at=new_chat_room.created_at,
            is_favorite=new_chat_room.is_favorite,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while creating chat room.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.put("/chatrooms/{chat_room_id}", response_model=ChatRoomResponse)
async def update_chat_room(
    chat_room_id: int,
    chat_room_data: ChatRoomUpdate,
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        chat_room = await crud.get_chat_room_by_id(
            db=db, chat_room_id=chat_room_id
        )
        if not chat_room:
            raise HTTPException(
                status_code=404,
                detail="Chat room not found.",
                headers={"X-Error": "NOT_FOUND"},
            )

        updated_chat_room = await crud.update_chat_room(
            db=db, chat_room=chat_room, chat_room_data=chat_room_data
        )

        return ChatRoomResponse(
            id=updated_chat_room.id,
            folder_id=updated_chat_room.folder_id,
            name=updated_chat_room.name,
            created_at=updated_chat_room.created_at,
            is_favorite=updated_chat_room.is_favorite,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while updating chat room.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.delete("/chatrooms/{chat_room_id}")
async def delete_chat_room(
    chat_room_id: int,
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        chat_room = await crud.get_chat_room_by_id(
            db=db, chat_room_id=chat_room_id
        )
        if not chat_room:
            raise HTTPException(
                status_code=404,
                detail="Chat room not found.",
                headers={"X-Error": "NOT_FOUND"},
            )

        await crud.delete_chat_room(db=db, chat_room=chat_room)

        return {"detail": "Chat room deleted successfully."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while deleting chat room.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e
