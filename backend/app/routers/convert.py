import asyncio
import hashlib
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import MEDIA_DIR
from app.converters.image_format import to_jpg, to_png, to_webp
from app.converters.image_ico import to_ico
from app.converters.image_resize import resize_image
from app.database import get_db
from app.models import Resource
from app.schemas import ResourceResponse

router = APIRouter(tags=["Convert"])


async def _get_image_resource(resource_id: int, db: AsyncSession) -> Resource:
    """Fetch a resource and validate it is an existing, non-deleted image with a filename."""
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Resource not found")
    if resource.category != "image":
        raise HTTPException(status_code=400, detail="Resource is not an image")
    if not resource.filename:
        raise HTTPException(status_code=400, detail="Resource has no file")
    return resource


def _build_source_path(resource: Resource) -> Path:
    """Build the source file path and validate it exists."""
    source_path = MEDIA_DIR / (resource.folder or "") / resource.filename
    if not source_path.is_file():
        raise HTTPException(status_code=400, detail="Source file not found")
    return source_path


async def _finalize_conversion(
    temp_path: Path,
    ext: str,
    resource: Resource,
    db: AsyncSession,
) -> Resource:
    """
    Read the converted file, compute SHA256, rename/dedup, create a new Resource,
    and return it.
    """
    content = temp_path.read_bytes()
    sha256 = hashlib.sha256(content).hexdigest()
    new_filename = f"{sha256}.{ext}"

    folder_path = MEDIA_DIR / (resource.folder or "")
    final_path = folder_path / new_filename

    if final_path.exists():
        temp_path.unlink(missing_ok=True)
    else:
        temp_path.rename(final_path)

    # Build new title: replace extension in original title
    original_title = resource.title or resource.filename
    title_stem = Path(original_title).stem
    new_title = f"{title_stem}.{ext}"

    new_resource = Resource(
        category="image",
        title=new_title,
        filename=new_filename,
        folder=resource.folder,
    )
    db.add(new_resource)
    await db.commit()
    await db.refresh(new_resource)
    return new_resource


class ResizeRequest(BaseModel):
    width: int | None = None
    height: int | None = None
    scale: float | None = None


@router.post("/convert/{resource_id}/resize", response_model=ResourceResponse)
async def convert_resize(
    resource_id: int, body: ResizeRequest, db: AsyncSession = Depends(get_db)
):
    resource = await _get_image_resource(resource_id, db)
    source_path = _build_source_path(resource)

    ext = source_path.suffix.lstrip(".")
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    ok = await asyncio.to_thread(
        resize_image,
        source_path,
        temp_path,
        width=body.width,
        height=body.height,
        scale=body.scale,
    )
    if not ok:
        temp_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Resize conversion failed")

    return await _finalize_conversion(temp_path, ext, resource, db)


class WebpRequest(BaseModel):
    quality: int = 80


@router.post("/convert/{resource_id}/webp", response_model=ResourceResponse)
async def convert_webp(
    resource_id: int, body: WebpRequest, db: AsyncSession = Depends(get_db)
):
    resource = await _get_image_resource(resource_id, db)
    source_path = _build_source_path(resource)

    ext = "webp"
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    ok = await asyncio.to_thread(to_webp, source_path, temp_path, body.quality)
    if not ok:
        temp_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="WebP conversion failed")

    return await _finalize_conversion(temp_path, ext, resource, db)


class JpgRequest(BaseModel):
    quality: int = 85


@router.post("/convert/{resource_id}/jpg", response_model=ResourceResponse)
async def convert_jpg(
    resource_id: int, body: JpgRequest, db: AsyncSession = Depends(get_db)
):
    resource = await _get_image_resource(resource_id, db)
    source_path = _build_source_path(resource)

    ext = "jpg"
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    ok = await asyncio.to_thread(to_jpg, source_path, temp_path, body.quality)
    if not ok:
        temp_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="JPEG conversion failed")

    return await _finalize_conversion(temp_path, ext, resource, db)


@router.post("/convert/{resource_id}/png", response_model=ResourceResponse)
async def convert_png(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await _get_image_resource(resource_id, db)
    source_path = _build_source_path(resource)

    ext = "png"
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    ok = await asyncio.to_thread(to_png, source_path, temp_path)
    if not ok:
        temp_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="PNG conversion failed")

    return await _finalize_conversion(temp_path, ext, resource, db)


class IcoRequest(BaseModel):
    sizes: list[int] | None = None


@router.post("/convert/{resource_id}/ico", response_model=ResourceResponse)
async def convert_ico(
    resource_id: int, body: IcoRequest, db: AsyncSession = Depends(get_db)
):
    resource = await _get_image_resource(resource_id, db)
    source_path = _build_source_path(resource)

    ext = "ico"
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    ok = await asyncio.to_thread(to_ico, source_path, temp_path, body.sizes)
    if not ok:
        temp_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="ICO conversion failed")

    return await _finalize_conversion(temp_path, ext, resource, db)
