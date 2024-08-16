from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base
from app.database import engine
from app.database import SessionLocal
from app.models.tables import ChatRooms
from app.models.tables import Folders
from app.models.tables import Link_Chatrooms
from app.models.tables import Links
from app.models.tables import Messages
from app.models.tables import Scores
from app.models.tables import Users
from app.models.tables import Vectors
from app.routers import chatrooms
from app.routers import folders
from app.routers import links
from app.routers import messages
from tests.example_data_insert import example_insert


def start():
    Base.metadata.create_all(
        bind=engine,
        tables=[
            Users.__table__,
            Folders.__table__,
            Links.__table__,
            Vectors.__table__,
            ChatRooms.__table__,
            Link_Chatrooms.__table__,
            Messages.__table__,
            Scores.__table__,
        ],
    )  # 테이블 생성
    # Base.metadata.drop_all(engine)

    with SessionLocal() as db:
        # 초기 데이터 삽입 (예시)
        example_insert(db)


def shutdown():
    print("service is stopped.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.

    # start()

    yield

    # When service is stopped.
    shutdown()


app = FastAPI(lifespan=lifespan)


app.include_router(folders.router, prefix="/api/v0")
app.include_router(chatrooms.router, prefix="/api/v0")
app.include_router(messages.router, prefix="/api/v0")
app.include_router(links.router, prefix="/api/v0")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
