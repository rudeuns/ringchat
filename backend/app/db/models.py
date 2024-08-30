from app.db.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    folders = relationship(
        "Folder", back_populates="user_info", cascade="all, delete-orphan"
    )


class Folder(Base):
    __tablename__ = "folder"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("user_info.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user_info = relationship("UserInfo", back_populates="folders")
    chat_rooms = relationship(
        "ChatRoom", back_populates="folder", cascade="all, delete-orphan"
    )


class ChatRoom(Base):
    __tablename__ = "chat_room"

    id = Column(Integer, primary_key=True)
    folder_id = Column(
        Integer, ForeignKey("folder.id", ondelete="CASCADE"), nullable=True
    )
    name = Column(String, default=lambda: datetime.now().strftime("%Y%m%d %H:%M:%S"))
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    folder = relationship("Folder", back_populates="chat_rooms")
    links = relationship(
        "ChatRoomLink", back_populates="chat_room", cascade="all, delete-orphan"
    )
    messages = relationship(
        "Message", back_populates="chat_room", cascade="all, delete-orphan"
    )


class Link(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    chat_rooms = relationship(
        "ChatRoomLink", back_populates="link", cascade="all, delete-orphan"
    )
    link_stat = relationship(
        "LinkStat", back_populates="link", uselist=False, cascade="all, delete-orphan"
    )
    summary_embedding = relationship(
        "LinkSummaryEmbedding",
        back_populates="link",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ChatRoomLink(Base):
    __tablename__ = "chat_room_link"

    id = Column(Integer, primary_key=True)
    chat_room_id = Column(
        Integer, ForeignKey("chat_room.id", ondelete="CASCADE"), nullable=False
    )
    link_id = Column(Integer, ForeignKey("link.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    chat_room = relationship("ChatRoom", back_populates="links")
    link = relationship("Link", back_populates="chat_rooms")


class LinkSummaryEmbedding(Base):
    __tablename__ = "link_summary_embedding"

    id = Column(Integer, primary_key=True)
    link_id = Column(
        Integer, ForeignKey("link.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    summary_vector = Column(Vector(dim=300), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    link = relationship("Link", back_populates="summary_embedding", uselist=False)


class LinkStat(Base):
    __tablename__ = "link_stat"

    id = Column(Integer, primary_key=True)
    link_id = Column(
        Integer, ForeignKey("link.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    average_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    attached_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    link = relationship("Link", back_populates="link_stat", uselist=False)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    chat_room_id = Column(
        Integer, ForeignKey("chat_room.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    is_user_message = Column(
        Boolean, default=True
    )  # True if user message, False if AI response
    created_at = Column(DateTime, default=datetime.now)

    chat_room = relationship("ChatRoom", back_populates="messages")
    rating = relationship(
        "Rating", back_populates="message", uselist=False, cascade="all, delete-orphan"
    )


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True)
    message_id = Column(
        Integer, ForeignKey("message.id", ondelete="CASCADE"), nullable=False
    )
    score = Column(Integer, nullable=False)  # Rating score (e.g., 1 to 5)
    created_at = Column(DateTime, default=datetime.now)

    message = relationship("Message", back_populates="rating", uselist=False)
