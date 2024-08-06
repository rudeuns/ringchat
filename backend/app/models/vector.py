from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.oracle import VECTOR  
from sqlalchemy.orm import relationship

from app.database import Base


class Vector(Base):
    __tablename__ = "vector"

    v_id = Column(Integer, primary_key=True)  
    total_vector = Column(VECTOR, nullable=False)
    summary_vector = Column(VECTOR, nullable=False)
    created_date = Column(DateTime)  
    l_id = Column(Integer, ForeignKey("link.l_id"), nullable=False)

    link = relationship("Link", back_populates="vectors")
