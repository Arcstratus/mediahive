import shutil

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import MEDIA_DIR, TRASH_DIR
from app.database import get_db
from app.models import Resource
from app.schemas import TrashResponse

router = APIRouter(tags=["Trash"])


@router.get("/trash", response_model=list[TrashResponse])
async def list_trash(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Resource)
        .where(Resource.deleted_at.isnot(None))
        .order_by(Resource.deleted_at.desc())
    )
    return result.scalars().all()


@router.post("/trash/{resource_id}/restore", response_model=TrashResponse)
async def restore_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is None:
        raise HTTPException(status_code=404, detail="Trashed resource not found")

    if resource.filename:
        src = TRASH_DIR / resource.filename
        dest = MEDIA_DIR / (resource.folder or "") / resource.filename
        if src.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))

    resource.deleted_at = None
    await db.commit()
    await db.refresh(resource)
    return resource


@router.delete("/trash/{resource_id}", status_code=204)
async def permanently_delete(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is None:
        raise HTTPException(status_code=404, detail="Trashed resource not found")

    if resource.filename:
        trash_file = TRASH_DIR / resource.filename
        if trash_file.is_file():
            trash_file.unlink()

    await db.delete(resource)
    await db.commit()


@router.delete("/trash", status_code=204)
async def empty_trash(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Resource).where(Resource.deleted_at.isnot(None))
    )
    resources = result.scalars().all()

    for resource in resources:
        if resource.filename:
            trash_file = TRASH_DIR / resource.filename
            if trash_file.is_file():
                trash_file.unlink()
        await db.delete(resource)

    await db.commit()
