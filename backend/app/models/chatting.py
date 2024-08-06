from sqlalchemy import Column, ForeignKey, TIMESTAMP, CLOB
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
from sqlalchemy.orm import relationship

from app.database import Base


class ChatRoom(Base):
    __tablename__ = "ChatRoom"

    r_id = Column(NUMBER, primary_key=True)
    room_name = Column(VARCHAR2(255), nullable=False)
    bookmark = Column(NUMBER, default=0)
    created_date = Column(TIMESTAMP, nullable=False)
    u_id = Column(NUMBER, ForeignKey("Users.u_id"), nullable=False)

    users = relationship("Users", back_populates="chat_rooms")
    messages = relationship("Message", back_populates="chat_room")
    links = relationship("Link", secondary="Link_ChatRoom", back_populates="chat_rooms") 


class Message(Base):
    __tablename__ = "Message"

    m_id = Column(NUMBER, primary_key=True)
    question = Column(CLOB)
    answer = Column(CLOB)
    created_date = Column(TIMESTAMP)
    r_id = Column(NUMBER, ForeignKey("ChatRoom.r_id"), nullable=False)

    chat_room = relationship("ChatRoom", back_populates="messages")
    satisfactions = relationship("Satisfaction", back_populates="message")

