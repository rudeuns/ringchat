from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models.tables import Users, Folders, Links, Vectors, ChatRooms, Link_Chatrooms, Messages, Scores
from app.database import get_db, engine, Base, SessionLocal

from tests.example_data_insert import example_insert

def start():   
    Base.metadata.create_all(bind=engine, tables=[Users.__table__, Folders.__table__,
                                                    Links.__table__, Vectors.__table__, 
                                                    ChatRooms.__table__, Link_Chatrooms.__table__,
                                                    Messages.__table__, Scores.__table__])  # 테이블 생성
    # Base.metadata.drop_all(engine)

    with SessionLocal() as db:
        # 초기 데이터 삽입 (예시)
        example_insert(db)
            
def shutdown():
    print("service is stopped.")    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    
    # Base.metadata.drop_all(engine)
    # start()
    
    yield
    
    # When service is stopped.
    shutdown()

app = FastAPI(lifespan=lifespan)

from app.routers import folders, chatrooms, messages, links

app.include_router(folders.router, prefix='/api/v0')
app.include_router(chatrooms.router, prefix='/api/v0')
app.include_router(messages.router, prefix='/api/v0')
app.include_router(links.router, prefix='/api/v0')


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
