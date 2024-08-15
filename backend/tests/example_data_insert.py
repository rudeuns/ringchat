import orjson
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models.tables import ChatRooms
from app.models.tables import Folders
from app.models.tables import Link_Chatrooms
from app.models.tables import Links
from app.models.tables import Messages
from app.models.tables import Scores
from app.models.tables import Users
from app.models.tables import Vectors


def read_doc(file):
    with open(file, "r", encoding="utf-8") as f:
        docs = f.read()
    return docs


users_data = [
    {
        "email": "user1@example.com",
        "password": "password123",
        "user_name": "User1",
    }
]

folder_data = [{"folder_name": "Default", "user_id": 1}]

link_data = [
    {
        "url": "https://yooloo.tistory.com/60",
        "last_updated": func.sysdate(),
        "sum_bookmark": 0,
        "avg_score": None,
        "sum_used_num": 0,
        "link_title": "파이썬 __main__ 이란",
    },
    {
        "url": "https://sean-j.tistory.com/37",
        "last_updated": func.sysdate(),
        "sum_bookmark": 0,
        "avg_score": None,
        "sum_used_num": 0,
        "link_title": "Document loaders",
    },
]

documents = ["doc1.txt", "doc2.txt"]
for i, doc in enumerate(documents):
    data = read_doc("tests/text_files/" + doc)
    link_data[i]["link_document"] = data


vector_data = [
    {
        "total_vector": [
            [0.1, 0.2, 0.3, 0.1, 0.2, 0.3],
            [0.2, 0.1, 0.4, 0.1, 0.2, 0.3],
        ],
        "summary_vector": [0.2, 0.1, 0.4, 0.1, 0.2, 0.3],
        "created_time": func.sysdate(),
        "link_id": 1,
    },
    {
        "total_vector": [
            [0.1, 0.2, 0.3, 0.1, 0.2, 0.3],
            [0.2, 0.1, 0.4, 0.1, 0.2, 0.3],
        ],
        "summary_vector": [0.2, 0.1, 0.4, 0.1, 0.2, 0.3],
        "created_time": func.sysdate(),
        "link_id": 2,
    },
]


chat_room_data = [
    {
        "room_name": "파이썬에 대한 질문",
        "bookmark": 1,
        "created_time": func.sysdate(),
        "user_id": 1,
        "folder_id": 1,
    },
    {
        "room_name": "Document loaders 사용법",
        "bookmark": 0,
        "created_time": func.sysdate(),
        "user_id": 1,
        "folder_id": 1,
    },
]

link_chat_room_data = [
    {"link_id": 1, "room_id": 1},
    {"link_id": 2, "room_id": 2},
]

message_data = [
    {
        "question": "파이썬에서 __main__가 무슨 역할을 해?",
        "answer": '파이썬에서 __main__은 최상위 코드 환경을 나타내는 특별한 문자열입니다. 즉, 특정 파이썬 파일이 직접 실행될 때, 해당 파일의 __name__ 변수에는 "__main__"이라는 값이 할당됩니다. 반면, 해당 파일이 다른 파일에서 import 될 때에는 __name__ 변수에는 파일 자체의 이름이 할당됩니다.',
        "created_time": func.sysdate(),
        "room_id": 1,
    },
    {
        "question": "실제로 사용하는 예시 들어줘.",
        "answer": 'calculator.py라는 파일을 만들어 덧셈, 뺄셈 기능을 제공하는 계산기 모듈을 만들고, 이 모듈을 다른 곳에서 import 하거나 직접 실행할 수 있도록 __main__을 활용하는 예시입니다. def subtract(x, y): """두 숫자를 빼는 함수""" return x - y if __name__ == "__main__": subtract(3, 5)',
        "created_time": func.sysdate(),
        "room_id": 1,
    },
    {
        "question": "lanchain에서 document loader가 뭐야?",
        "answer": "LangChain에서 Document Loader는 외부 데이터 소스에서 텍스트 데이터를 가져와 LangChain이 처리할 수 있는 형식으로 변환하는 핵심 구성 요소",
        "created_time": func.sysdate(),
        "room_id": 2,
    },
    {
        "question": "예시 코드 작성해줘.",
        "answer": 'from langchain.document_loaders import WebBaseLoader loader = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence") documents = loader.load()',
        "created_time": func.sysdate(),
        "room_id": 2,
    },
]

scores_data = [{"score": 2, "msg_id": 1}, {"score": 3, "msg_id": 3}]


def add_users(db: Session, users_data: list[dict]):
    """여러 사용자 데이터를 Users 테이블에 추가하는 함수

    Args:
        db (Session): 데이터베이스 세션
        users_data (list[dict]): 추가할 사용자 데이터 리스트 (딕셔너리 형태)
    """
    try:
        # users_data 리스트의 각 딕셔너리를 Users 객체로 변환하여 추가
        for user_data in users_data:
            user = Users(**user_data)
            db.add(user)

        db.commit()  # 변경 사항을 데이터베이스에 커밋
        print("사용자 추가 성공")
    except Exception as e:
        db.rollback()  # 예외 발생 시 롤백
        print(f"사용자 추가 실패: {e}")


def add_folders(db: Session, folders_data: list[dict]):
    """여러 폴더 데이터를 Folder 테이블에 추가하는 함수"""
    try:
        for folder_data in folders_data:
            folder = Folders(**folder_data)
            db.add(folder)
        db.commit()
        print("폴더 추가 성공")
    except Exception as e:
        db.rollback()
        print(f"폴더 추가 실패: {e}")


def add_links(db: Session, links_data: list[dict]):
    """여러 링크 데이터를 Link 테이블에 추가하는 함수"""
    try:
        for link_data in links_data:
            link = Links(**link_data)
            db.add(link)
        db.commit()
        print("링크 추가 성공")
    except Exception as e:
        db.rollback()
        print(f"링크 추가 실패: {e}")


def vector_insert(db: Session, vectors_data: list[dict]):
    try:
        for vector_data in vectors_data:
            # JSON 변환 (orjson 사용)
            vector_data["total_vector"] = orjson.dumps(
                vector_data["total_vector"]
            ).decode("utf-8")
            vector_data["summary_vector"] = orjson.dumps(
                vector_data["summary_vector"]
            ).decode("utf-8")

            stmt = insert(Vectors).values(**vector_data)
            db.execute(stmt)
        db.commit()
        print("벡터 추가 성공")
    except Exception as e:
        db.rollback()
        print(f"벡터 추가 실패: {e}")


def add_chat_rooms(db: Session, chat_rooms_data: list[dict]):
    """여러 채팅방 데이터를 ChatRoom 테이블에 추가하는 함수"""
    try:
        for chat_room_data in chat_rooms_data:
            chat_room = ChatRooms(**chat_room_data)
            db.add(chat_room)
        db.commit()
        print("채팅방 추가 성공")
    except Exception as e:
        db.rollback()
        print(f"채팅방 추가 실패: {e}")


def add_link_chatroom(db: Session, link_chatroom_data: list[dict]):
    try:
        for data in link_chatroom_data:
            stmt = insert(Link_Chatrooms).values(
                link_id=data["link_id"], room_id=data["room_id"]
            )
            db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"링크-채팅방 연결 실패: {e}")


def add_messages(db: Session, messages_data: list[dict]):
    """여러 메시지 데이터를 Message 테이블에 추가하는 함수"""
    try:
        for message_data in messages_data:
            message = Messages(**message_data)
            db.add(message)
        db.commit()
        print("메시지 추가 성공")
    except Exception as e:
        db.rollback()
        print(f"메시지 추가 실패: {e}")


def add_scores(db: Session, scores_data: list[dict]):
    """여러 만족도 데이터를 Scores 테이블에 추가하는 함수"""
    try:
        for score_data in scores_data:
            score = Scores(**score_data)
            db.add(score)
        db.commit()
        print("만족도 추가 성공")
    except Exception as e:
        db.rollback()
        print(f"만족도 추가 실패: {e}")


def example_insert(db):
    add_users(db, users_data)
    add_links(db, link_data)
    add_folders(db, folder_data)
    add_chat_rooms(db, chat_room_data)
    vector_insert(db, vector_data)
    add_link_chatroom(db, link_chat_room_data)
    add_messages(db, message_data)
    add_scores(db, scores_data)
