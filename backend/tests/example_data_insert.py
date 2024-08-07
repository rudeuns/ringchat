import json
import orjson
from sqlalchemy import func, insert
from sqlalchemy.orm import Session
from app.models.tables import Users, Folders, Links, Vectors, ChatRooms, Link_Chatrooms, Messages, Scores  


users_data = [
    {"email": "user1@example.com", "password": "password123", "user_name": "User1"},
    {"email": "user2@example.com", "password": "securepass", "user_name": "User2"},
    {"email": "user3@example.com", "password": "strongpass", "user_name": "User3"},
]

folder_data = [
    {'folder_name': 'Default', 'user_id': 1},
    {'folder_name': 'Default', 'user_id': 2},
    {'folder_name': 'Default', 'user_id': 3},
]

link_data = [
    {'url': 'https://docs.python.org/3/', 'last_updated': func.sysdate(), 'sum_bookmark': 0, 'avg_score': None, 'sum_used_num': 0},
    {'url': 'https://fastapi.tiangolo.com/ko/#_6', 'last_updated': func.sysdate(), 'sum_bookmark': 0, 'avg_score': None, 'sum_used_num': 0},
    {'url': 'https://pytorch.org/docs/stable/torch.html#optimizations', 'last_updated': func.sysdate(), 'sum_bookmark': 0, 'avg_score': None, 'sum_used_num': 0},
    {'url': 'https://www.tensorflow.org/api_docs', 'last_updated': func.sysdate(), 'sum_bookmark': 0, 'avg_score': None, 'sum_used_num': 0},
]


vector_data = [
    {'total_vector': [[0.1, 0.2, 0.3, 0.1, 0.2, 0.3],[0.2, 0.1, 0.4, 0.1, 0.2, 0.3]], 'summary_vector': [0.2, 0.1, 0.4, 0.1, 0.2, 0.3], 'created_time': func.sysdate(), 'link_id': 1},
    {'total_vector': [[0.1, 0.2, 0.3, 0.1, 0.2, 0.3],[0.2, 0.1, 0.4, 0.1, 0.2, 0.3]], 'summary_vector': [0.2, 0.1, 0.4, 0.1, 0.2, 0.3], 'created_time': func.sysdate(), 'link_id': 2},
    {'total_vector': [[0.1, 0.2, 0.3, 0.1, 0.2, 0.3],[0.2, 0.1, 0.4, 0.1, 0.2, 0.3]], 'summary_vector': [0.2, 0.1, 0.4, 0.1, 0.2, 0.3], 'created_time': func.sysdate(), 'link_id': 3},
    {'total_vector': [[0.1, 0.2, 0.3, 0.1, 0.2, 0.3],[0.2, 0.1, 0.4, 0.1, 0.2, 0.3]], 'summary_vector': [0.2, 0.1, 0.4, 0.1, 0.2, 0.3], 'created_time': func.sysdate(), 'link_id': 4},
    {'total_vector': [[0.1, 0.2, 0.3, 0.1, 0.2, 0.3],[0.2, 0.1, 0.4, 0.1, 0.2, 0.3]], 'summary_vector': [0.2, 0.1, 0.4, 0.1, 0.2, 0.3], 'created_time': func.sysdate(), 'link_id': 1}
]


chat_room_data = [
    {'room_name': '파이썬에 대한 질문', 'bookmark': 1, 'created_time': func.sysdate(), 'user_id': 1, 'folder_id':1},
    {'room_name': 'fastapi 사용법', 'bookmark': 0, 'created_time': func.sysdate(), 'user_id': 2, 'folder_id':2},
    {'room_name': '텐서플로우 vs 파이토치', 'bookmark': 1, 'created_time': func.sysdate(), 'user_id': 3, 'folder_id':3},
    {'room_name': '파이썬 공부법', 'bookmark': 1, 'created_time': func.sysdate(), 'user_id': 3, 'folder_id':3},
]

link_chat_room_data = [
    {'link_id': 1, 'room_id': 1},
    {'link_id': 2, 'room_id': 2},
    {'link_id': 3, 'room_id': 3},
    {'link_id': 4, 'room_id': 3},
    {'link_id': 1, 'room_id': 4},
]

message_data = [
    {'question': '파이썬 list, dictionary, set 사용법 알려줘', 'answer': '파이썬 list는 []을 사용하시구요, dictionary는 {}을 사용하시구요, set은 set()으로 사용하세요.', 'created_time': func.sysdate(), 'room_id': 1},
    {'question': 'fastapi를 활용해서 api를 만들고 싶어.', 'answer': 'fastapi quick start를 참고하세요.', 'created_time': func.sysdate(), 'room_id': 2},
    {'question': '텐서플로우랑 파이토치 비교해줘.', 'answer': '텐서플로우는 AI 서비스에 최적화 되어 있어서 기업이 많이 쓰고, 파이토치는 연구용으로 많이 사용되요.', 'created_time': func.sysdate(), 'room_id': 3},
    {'question': '파이썬 공부가 처음인데 어떻게 해?', 'answer': '기본서 책 사서 공부하세요.', 'created_time': func.sysdate(), 'room_id': 4},
    {'question': '어떤 책 사야되는데?', 'answer': '서점에서 베스트 셀러로 구매하세요.', 'created_time': func.sysdate(), 'room_id': 4},
]

scores_data = [
    {'score': 2, 'msg_id': 1},
    {'score': 3, 'msg_id': 3},
    {'score': 1, 'msg_id': 4},
    {'score': 1, 'msg_id': 5},
]

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
            vector_data['total_vector'] = orjson.dumps(vector_data['total_vector']).decode('utf-8')
            vector_data['summary_vector'] = orjson.dumps(vector_data['summary_vector']).decode('utf-8')

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
                link_id=data['link_id'],
                room_id=data['room_id']
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
    
    
