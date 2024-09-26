from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import (
    MessageCreate,
    MessageStream,
    MessageResponse,
    MessageListResponse,
)
import app.db.crud as crud
from app.utils.security import get_current_user_id
from app.utils.langchain import get_langchain_response
from app.tasks.message_task import restore_link_content_and_chat_history
from typing import Optional
import asyncio

router = APIRouter(tags=["messages"])


@router.get(
    "/chatrooms/{chat_room_id}/messages", response_model=MessageListResponse
)
async def get_messages(
    chat_room_id: int,
    background_tasks: BackgroundTasks,
    restore: Optional[bool] = Query(None),
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        messages = await crud.get_messages_by_chat_room_id(
            db=db, chat_room_id=chat_room_id
        )

        if restore:
            background_tasks.add_task(
                restore_link_content_and_chat_history, chat_room_id
            )

        return MessageListResponse(messages=messages)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while fetching messages.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.post(
    "/chatrooms/{chat_room_id}/messages", response_model=MessageResponse
)
async def create_message(
    chat_room_id: int,
    message_data: MessageCreate,
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        new_message = await crud.create_message(
            db=db, message_data=message_data, chat_room_id=chat_room_id
        )

        return MessageResponse(
            id=new_message.id,
            content=new_message.content,
            is_user_message=new_message.is_user_message,
            created_at=new_message.created_at,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while creating message.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.post("/chatrooms/{chat_room_id}/messages/stream")
async def stream_message(chat_room_id: int, message_data: MessageStream):
    try:

        async def generate_ai_message():
            try:
                user_message = message_data.user_message

                for chunk in get_langchain_response(user_message, chat_room_id):
                    yield chunk
                    await asyncio.sleep(0.01)

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail="Unexpected error occurred while generating ai message.",
                    headers={"X-Error": "SERVER_ERROR"},
                ) from e

        return StreamingResponse(
            generate_ai_message(),
            media_type="text/event-stream",
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while streaming message.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e
