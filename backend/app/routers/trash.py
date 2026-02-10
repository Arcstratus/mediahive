from fastapi import Depends
from fastapi_error_map import ErrorAwareRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import TrashedResourceNotFoundError
from app.schemas import TrashResponse
from app.services import resource_service

router = ErrorAwareRouter(tags=["Trash"])


@router.get("/trash", response_model=list[TrashResponse])
async def list_trash(db: AsyncSession = Depends(get_db)):
    return await resource_service.list_trash(db)


@router.post(
    "/trash/{resource_id}/restore",
    response_model=TrashResponse,
    error_map={TrashedResourceNotFoundError: 404},
)
async def restore_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    return await resource_service.restore_resource(db, resource_id)


@router.delete(
    "/trash/{resource_id}",
    status_code=204,
    error_map={TrashedResourceNotFoundError: 404},
)
async def permanently_delete(resource_id: int, db: AsyncSession = Depends(get_db)):
    await resource_service.permanently_delete(db, resource_id)


@router.delete("/trash", status_code=204)
async def empty_trash(db: AsyncSession = Depends(get_db)):
    await resource_service.empty_trash(db)
