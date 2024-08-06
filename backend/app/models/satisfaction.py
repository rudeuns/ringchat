from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.database import Base


class Satisfaction(Base):
    __tablename__ = "Satisfaction"

    s_id = Column(NUMBER, primary_key=True)
    satisfaction = Column(NUMBER(1), nullable=False)  # Limited to a single digit (0-9)
    m_id = Column(NUMBER, ForeignKey("Message.m_id"), nullable=False)

    message = relationship("Message", back_populates="satisfactions")
