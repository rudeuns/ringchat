from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import (
    FolderCreate,
    FolderUpdate,
    FolderResponse,
    FolderListResponse,
)
import app.db.crud as crud
from app.utils.security import get_current_user_id

router = APIRouter(tags=["folders"])


@router.get("/folders", response_model=FolderListResponse)
async def get_folders(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        folders = await crud.get_folders_by_user_id(db=db, user_id=user_id)
        return FolderListResponse(folders=folders)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while fetching folders.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.post("/folders", response_model=FolderResponse)
async def create_folder(
    folder_data: FolderCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        new_folder = await crud.create_folder(
            db=db, folder_data=folder_data, user_id=user_id
        )
        return FolderResponse(
            id=new_folder.id,
            name=new_folder.name,
            created_at=new_folder.created_at,
            chat_rooms=[],
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while creating folder.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.put("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: int,
    folder_data: FolderUpdate,
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        folder = await crud.get_folder_by_id(db=db, folder_id=folder_id)
        if not folder:
            raise HTTPException(
                status_code=404,
                detail="Folder not found.",
                headers={"X-Error": "NOT_FOUND"},
            )

        updated_folder = await crud.update_folder(
            db=db, folder=folder, folder_data=folder_data
        )

        return FolderResponse(
            id=updated_folder.id,
            name=updated_folder.name,
            created_at=updated_folder.created_at,
            chat_rooms=updated_folder.chat_rooms,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while updating folder.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.delete("/folders/{folder_id}")
async def delete_folder(
    folder_id: int,
    _=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        folder = await crud.get_folder_by_id(db=db, folder_id=folder_id)
        if not folder:
            raise HTTPException(
                status_code=404,
                detail="Folder not found.",
                headers={"X-Error": "NOT_FOUND"},
            )

        await crud.delete_folder(db=db, folder=folder)

        return {"detail": "Folder deleted successfully."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while deleting folder.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e
