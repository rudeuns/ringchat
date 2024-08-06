from sqlalchemy import Column
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2

from app.database import Base


class Users(Base):
    __tablename__ = "Users"

    u_id = Column(NUMBER, primary_key=True)
    email = Column(VARCHAR2(64), nullable=False, unique=True, index=True) 
    password = Column(VARCHAR2(32), nullable=False)
    name = Column(VARCHAR2(18), nullable=False)
    