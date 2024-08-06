from sqlalchemy import Column, Date, Table, Integer, ForeignKey
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2

from app.database import Base


link_chatroom = Table(
    "link_chatroom",
    Base.metadata,
    Column("lc_id", Integer, primary_key=True),
    Column("l_id", Integer, ForeignKey("link.l_id"), nullable=False),
    Column("r_id", Integer, ForeignKey("chatroom.r_id"), nullable=False),
)


class Link(Base):
    __tablename__ = "Link"

    l_id = Column(NUMBER, primary_key=True)
    url = Column(VARCHAR2(2048), nullable=False, unique=True) 
    last_updated = Column(Date, nullable=False)
    sum_bookmark = Column(NUMBER, default=0)
    avg_satisfaction = Column(NUMBER(3, 2), default=0.0)  # NUMBER(3, 2) for decimal precision
    sum_room_num = Column(NUMBER, default=0)
