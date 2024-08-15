from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tables import Folders

router = APIRouter()

class Folder(BaseModel):
    folderId: int
    folderName: str

def format_folders_data(folders):
    folders_data = []
    for folder in folders:
        if(1 == int(folder.folder_id)):
            folders_data.append({
                "folderId": int(folder.folder_id), 
                "folderName": folder.folder_name
            })

    return folders_data

@router.get("/folders", response_model=List[Folder])
async def get_folders(userId: int, db: Session = Depends(get_db)):
    folders = db.query(Folders).filter(Folders.user_id == userId).all()
    if not folders:
        raise HTTPException(status_code=404, detail="User not found or no folders available")
    
    return format_folders_data(folders)
