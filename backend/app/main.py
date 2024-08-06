from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Folder

from app.database import get_db

app = FastAPI()

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
@app.get("/folders")
def get_folders(user_id: int = Query(..., description='user id'), db: Session = Depends(get_db)):
    try: 
        with db as sess: 
            folders = sess.query(Folder).filter(Folder.u_id == user_id).all()
            if not folders: 
                return {'message': "찾을 수 없는 폴더 입니다."}
            
            return {"folders": [folder.response_all() for folder in folders]}

    except SQLAlchemyError as e:
        # SQLAlchemy 관련 예외 발생 시 처리
        print(f"Database error: {e}")
        return {"error": "데이터베이스 오류가 발생했습니다."}, 500
    except Exception as e:
        # 기타 예외 발생 시 처리
        print(f"Unexpected error: {e}")
        return {"error": "예기치 않은 오류가 발생했습니다."}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
