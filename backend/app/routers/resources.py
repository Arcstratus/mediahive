from pathlib import Path
from urllib.parse import urlparse

from fastapi import (
    BackgroundTasks,
    Depends,
    Query,
    UploadFile,
)
from fastapi_error_map import ErrorAwareRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import ResourceNotFoundError, ResourceValidationError
from app.schemas import (
    BatchDeleteRequest,
    BatchDeleteResponse,
    PaginatedResponse,
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from app.services import resource_service

router = ErrorAwareRouter(tags=["Resources"])


@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(body: ResourceCreate, db: AsyncSession = Depends(get_db)):
    return await resource_service.create_resource(db, body)


@router.get("/resources", response_model=PaginatedResponse)
async def list_resources(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    search: str | None = Query(None),
    ext: list[str] = Query(None),
    tag: list[str] = Query(None),
    folder: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    return await resource_service.list_resources(
        db,
        page=page,
        per_page=per_page,
        category=category,
        search=search,
        ext=ext,
        tag=tag,
        folder=folder,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


@router.get("/resources/ids", response_model=list[int])
async def list_resource_ids(
    category: str | None = Query(None),
    search: str | None = Query(None),
    ext: list[str] = Query(None),
    tag: list[str] = Query(None),
    folder: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    return await resource_service.list_resource_ids(
        db,
        category=category,
        search=search,
        ext=ext,
        tag=tag,
        folder=folder,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


@router.get("/resources/folders")
async def list_resource_folders(db: AsyncSession = Depends(get_db)):
    return await resource_service.list_resource_folders(db)


@router.post("/resources/batch-delete", response_model=BatchDeleteResponse)
async def batch_delete_resources(
    body: BatchDeleteRequest, db: AsyncSession = Depends(get_db)
):
    deleted = await resource_service.batch_soft_delete(db, body.ids)
    return BatchDeleteResponse(deleted=deleted)


@router.get(
    "/resources/{resource_id}",
    response_model=ResourceResponse,
    error_map={ResourceNotFoundError: 404},
)
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    return await resource_service.get_resource(db, resource_id)


@router.put(
    "/resources/{resource_id}",
    response_model=ResourceResponse,
    error_map={ResourceNotFoundError: 404, ResourceValidationError: 400},
)
async def update_resource(
    resource_id: int, body: ResourceUpdate, db: AsyncSession = Depends(get_db)
):
    return await resource_service.update_resource(db, resource_id, body)


@router.delete(
    "/resources/{resource_id}",
    status_code=204,
    error_map={ResourceNotFoundError: 404},
)
async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    await resource_service.soft_delete_resource(db, resource_id)


class DownloadRequest(BaseModel):
    url: str


@router.post(
    "/resources/download",
    status_code=202,
    error_map={ResourceValidationError: 400},
)
async def download_resource(body: DownloadRequest, bg: BackgroundTasks):
    parsed = urlparse(body.url)
    ext = Path(parsed.path).suffix.lower()

    if ext not in resource_service.ALLOWED_EXTENSIONS:
        raise ResourceValidationError(
            f"Unsupported URL extension: {ext or '(none)'}",
        )

    bg.add_task(resource_service.bg_download, body.url, ext)
    return {"status": "downloading"}


@router.post(
    "/resources/upload",
    response_model=ResourceResponse,
    status_code=201,
    error_map={ResourceValidationError: 400},
)
async def upload_resource(
    file: UploadFile,
    title: str | None = None,
    tags: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    return await resource_service.upload_resource(
        db, content, file.filename, title, tags
    )


class ThumbnailRequest(BaseModel):
    timestamp: float


@router.post(
    "/resources/{resource_id}/thumbnail",
    response_model=ResourceResponse,
    error_map={ResourceNotFoundError: 404, ResourceValidationError: 400},
)
async def set_thumbnail(
    resource_id: int, body: ThumbnailRequest, db: AsyncSession = Depends(get_db)
):
    return await resource_service.set_thumbnail(db, resource_id, body.timestamp)


@router.delete(
    "/resources/{resource_id}/thumbnail",
    response_model=ResourceResponse,
    error_map={ResourceNotFoundError: 404},
)
async def remove_thumbnail(resource_id: int, db: AsyncSession = Depends(get_db)):
    return await resource_service.remove_thumbnail(db, resource_id)
