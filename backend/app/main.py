from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Depends

from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.tables import Users, Folders, Links, Vectors, ChatRooms, Link_Chatrooms, Messages, Scores
from app.database import get_db, engine, Base, SessionLocal, create_tables_if_not_exist

from tests.example_data_insert import example_insert

def start():
    # create_tables_if_not_exist(engine, Base)
   
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
    start()
    
    yield
    
    # When service is stopped.
    shutdown()

app = FastAPI(lifespan=lifespan)
# app = FastAPI()

# import os

# from dotenv import load_dotenv
# from fastapi import FastAPI, Request
# from langchain_openai import OpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain.prompts import PromptTemplate


# app = FastAPI()

# # OpenAI API key settings
# load_dotenv()
# llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Prompt template for creating text
# prompt_template = PromptTemplate(
#     input_variables=["question"],
#     template="Please answer the following questions: {question}"
# )

# # Create LLMChain
# prompt = PromptTemplate.from_template(prompt_template.template)
# llm_chain = prompt | llm | StrOutputParser()

# @app.post("/ask")
# async def ask_question(request: Request):
#     user_input = await request.json()
#     question = user_input.get("question")

#     if question:
#         response = llm_chain.invoke(question)
#         return {"answer": response}
#     else:
#         return {"error": "Please enter your question"}
# @app.get("/folders")
# def get_folders(user_id: int = Query(..., description='user id'), db: Session = Depends(get_db)):
#     try: 
#         with db as sess: 
#             folders = sess.query(Folder).filter(Folder.u_id == user_id).all()
#             if not folders: 
#                 return {'message': "찾을 수 없는 폴더 입니다."}
            
#             return {"folders": [folder.response_all() for folder in folders]}

#     except SQLAlchemyError as e:
#         # SQLAlchemy 관련 예외 발생 시 처리
#         print(f"Database error: {e}")
#         return {"error": "데이터베이스 오류가 발생했습니다."}, 500
#     except Exception as e:
#         # 기타 예외 발생 시 처리
#         print(f"Unexpected error: {e}")
#         return {"error": "예기치 않은 오류가 발생했습니다."}, 500
    
@app.get("/users")
def test(db: Session = Depends(get_db)):
    with db as sess: 
        users = sess.query(Users).all()
        print(users)
        for user in users:
            print(user.response_all())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
