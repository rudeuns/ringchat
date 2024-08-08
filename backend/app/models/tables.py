import json
from sqlalchemy.types import TypeDecorator
from sqlalchemy import Column, Sequence, ForeignKey, Date, JSON, DateTime, CLOB, TIMESTAMP, Table
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
from sqlalchemy.orm import relationship

from app.database import Base, DB_USER

db_user = DB_USER.lower()

class JsonType(TypeDecorator):
    impl = VARCHAR2(4000)  # 적절한 VARCHAR2 크기 설정
    cache_ok = True  # 캐싱 활성화 (성능 향상)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return

class Users(Base):
    __tablename__ = "Users"
    __table_args__ = {'schema': DB_USER}
    
    user_id = Column(NUMBER, Sequence(db_user+'.user_id_seq'), primary_key=True)
    email = Column(VARCHAR2(64), nullable=False, unique=True, index=True)
    password = Column(VARCHAR2(32), nullable=False)
    user_name = Column(VARCHAR2(18), nullable=False)
    
    folders = relationship("Folders", back_populates="users")
    chatrooms = relationship("ChatRooms", back_populates="users")
    
    def response_all(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password,
            "user_name": self.user_name
        }
        
        
class Folders(Base):
    __tablename__ = "Folders"
    __table_args__ = {'schema': DB_USER}

    folder_id = Column(NUMBER, Sequence(db_user+'.folder_id_seq'), primary_key=True)
    folder_name = Column(VARCHAR2(255))
    user_id = Column(NUMBER, ForeignKey(DB_USER+".Users.user_id", ondelete="CASCADE"), nullable=False)
    
    users = relationship("Users", back_populates="folders")
    chatrooms = relationship("ChatRooms", back_populates="folders")
    
    def response_all(self):
        return {
            "folder_id": self.folder_id,
            "folder_name": self.folder_name,
            "user_id": self.user_id
        }

class Links(Base):
    __tablename__ = "Links"
    __table_args__ = {'schema': DB_USER}

    link_id = Column(NUMBER, Sequence(db_user+'.link_id_seq'), primary_key=True)
    url = Column(VARCHAR2(2048), nullable=False, unique=True) 
    link_title = Column(VARCHAR2(255), nullable=False)
    link_document = Column(CLOB)
    last_updated = Column(Date, nullable=False)
    sum_bookmark = Column(NUMBER, default=0)
    avg_score = Column(NUMBER(3, 2), default=0.0)  
    sum_used_num = Column(NUMBER, default=0)
    
    vectors = relationship("Vectors", back_populates="links")
    link_chatrooms = relationship("Link_Chatrooms", back_populates="links")
    
    def response_all(self):
        return {
            "link_id": self.link_id,
            "url": self.url,
            "last_updated": self.last_updated,
            "sum_bookmark": self.sum_bookmark,
            "avg_score": self.avg_score,
            "sum_used_num": self.sum_used_num
        }
        

class Vectors(Base):
    __tablename__ = "Vectors"
    __table_args__ = {'schema': DB_USER}

    vector_id = Column(NUMBER, Sequence(db_user+'.vector_id_seq'), primary_key=True)  
    total_vector = Column(JsonType, nullable=False)
    summary_vector = Column(JsonType, nullable=False)
    created_time = Column(DateTime)  
    link_id = Column(NUMBER, ForeignKey(DB_USER+".Links.link_id", ondelete="CASCADE"), nullable=False)

    links = relationship("Links", back_populates="vectors")
    
    def response_all(self):
        return {
            "vector_id": self.vector_id,
            "total_vector": self.total_vector,
            "summary_vector": self.summary_vector,
            "created_time": self.created_time,
            "link_id": self.link_id
        }
    

class ChatRooms(Base):
    __tablename__ = "ChatRooms"
    __table_args__ = {'schema': DB_USER}

    room_id = Column(NUMBER, Sequence(db_user+'.room_id_seq'), primary_key=True)
    room_name = Column(VARCHAR2(255), nullable=False)
    bookmark = Column(NUMBER, default=0)
    created_time = Column(TIMESTAMP, nullable=False)
    user_id = Column(NUMBER, ForeignKey(DB_USER+".Users.user_id", ondelete="CASCADE"), nullable=False)
    folder_id = Column(NUMBER, ForeignKey(DB_USER+".Folders.folder_id", ondelete="CASCADE"), nullable=False)
    
    users = relationship("Users", back_populates="chatrooms")
    folders = relationship("Folders", back_populates="chatrooms") 
    link_chatrooms = relationship("Link_Chatrooms", back_populates="chatrooms")
    messages = relationship("Messages", back_populates="chatrooms")

    def response_all(self):
        return {
            "room_id": self.room_id,
            "room_name": self.room_name,
            "bookmark": self.bookmark,
            "created_time": self.created_time,
            "user_id": self.user_id,
            "folder_id": self.folder_id
        }

class Link_Chatrooms(Base):
    __tablename__ = "Link_Chatrooms"
    __table_args__ = {'schema': DB_USER}

    link_room_id = Column(NUMBER, Sequence(db_user+'.link_room_id_seq'), primary_key=True)
    link_id = Column(NUMBER, ForeignKey(DB_USER+".Links.link_id", ondelete="CASCADE"), nullable=False)
    room_id = Column(NUMBER, ForeignKey(DB_USER+".ChatRooms.room_id", ondelete="CASCADE"), nullable=False)

    links = relationship("Links", back_populates="link_chatrooms")
    chatrooms = relationship("ChatRooms", back_populates="link_chatrooms")
    
    def response_all(self):
        return {
            "link_room_id": self.link_room_id,
            "link_id": self.link_id,
            "room_id": self.room_id
        }

class Messages(Base):
    __tablename__ = "Messages"
    __table_args__ = {'schema': DB_USER}

    msg_id = Column(NUMBER, Sequence(db_user+'.msg_id_seq'), primary_key=True)
    question = Column(CLOB)
    answer = Column(CLOB)
    created_time = Column(TIMESTAMP)
    room_id = Column(NUMBER, ForeignKey(DB_USER+".ChatRooms.room_id"), nullable=False)

    chatrooms = relationship("ChatRooms", back_populates="messages")
    scores = relationship("Scores", back_populates="messages")
    
    def response_all(self):
        return {
            "msg_id": self.msg_id,
            "question": self.question,
            "answer": self.answer,
            "created_time": self.created_time,
            "room_id": self.room_id
        }

class Scores(Base):
    __tablename__ = "Scores"
    __table_args__ = {'schema': DB_USER}

    score_id = Column(NUMBER, Sequence(db_user+'.score_id_seq'), primary_key=True)
    score = Column(NUMBER(1), nullable=False)  # Limited to a single digit (0-9)
    msg_id = Column(NUMBER, ForeignKey(DB_USER+".Messages.msg_id"), nullable=False)

    messages = relationship("Messages", back_populates="scores")
    
    def response_all(self):
        return {
            "score_id": self.score_id,
            "score": self.score,
            "msg_id": self.msg_id
        }
