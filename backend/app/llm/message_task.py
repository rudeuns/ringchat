from app.db.database import create_db_session
import app.db.crud as crud
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict

store: Dict[int, Dict[str, ChatMessageHistory]] = {}


async def restore_link_content_and_chat_history(chat_room_id: int):
    try:
        db = await create_db_session()

        chat_room_links = await crud.get_chat_room_links(
            db=db, chat_room_id=chat_room_id
        )

        document_text = "".join(
            [
                chat_room_link.link.content or ""
                for chat_room_link in chat_room_links
            ]
        )

        messages = await crud.get_messages_by_chat_room_id(
            db=db, chat_room_id=chat_room_id, message_num=10
        )

        memory = ChatMessageHistory()

        for message in messages:
            if message.is_user_message:
                memory.add_user_message(message.content)
            else:
                memory.add_ai_message(message.content)

        store[chat_room_id] = {
            "document_text": document_text,
            "chat_history": memory,
        }

    except Exception as e:
        raise RuntimeError(f"Error restoring chat room data: {e}")

    finally:
        await db.close()
