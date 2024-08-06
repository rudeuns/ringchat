from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
from sqlalchemy.orm import relationship

from app.models.users import Users
from app.database import Base


class Folder(Base):
    __tablename__ = "Folder"

    f_id = Column(NUMBER, primary_key=True)
    folder_name = Column(VARCHAR2(255)) 
    u_id = Column(NUMBER, ForeignKey("Users.u_id", ondelete="CASCADE"), nullable=False)

    users = relationship(Users, back_populates="folder") 
    
    def response_all(self): 
        return {
            "f_id": self.f_id,
            "folder_name": self.folder_name,
            "u_id": self.u_id
        }
        