import asyncio
import uuid
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import MEDIA_DIR
from app.converters.probe import probe_video
from app.converters.remux import remux_to_mp4
from app.converters.transcode import transcode_to_mp4
from app.exceptions import (
    ConversionError,
    ConversionNotNeededError,
    ResourceNotFoundError,
    ResourceValidationError,
)
from app.models import Resource, ResourceCategory
from app.services.file_service import sha256_hash


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def validate_resource(
    db: AsyncSession, resource_id: int, category: ResourceCategory
) -> Resource:
    """Fetch a resource and validate it exists, is not deleted, matches category, and has a file."""
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise ResourceNotFoundError("Resource not found")
    if resource.category != category:
        raise ResourceValidationError(f"Resource is not a {category}")
    if not resource.filename:
        raise ResourceValidationError("Resource has no file")
    return resource


def build_source_path(resource: Resource) -> Path:
    """Build the source file path and validate it exists."""
    source_path = MEDIA_DIR / (resource.folder or "") / resource.filename
    if not source_path.is_file():
        raise ResourceValidationError("Source file not found")
    return source_path


async def finalize_conversion(
    temp_path: Path,
    ext: str,
    resource: Resource,
    db: AsyncSession,
    category: ResourceCategory | None = None,
) -> Resource:
    """
    Read the converted file, compute SHA256, rename/dedup, create a new Resource,
    and return it.
    """
    content = temp_path.read_bytes()
    sha256 = sha256_hash(content)
    new_filename = f"{sha256}.{ext}"

    folder_path = MEDIA_DIR / (resource.folder or "")
    final_path = folder_path / new_filename

    if final_path.exists():
        temp_path.unlink(missing_ok=True)
    else:
        temp_path.rename(final_path)

    original_title = resource.title or resource.filename
    title_stem = Path(original_title).stem
    new_title = f"{title_stem}.{ext}"

    new_resource = Resource(
        category=category or resource.category,
        title=new_title,
        filename=new_filename,
        folder=resource.folder,
    )
    db.add(new_resource)
    await db.commit()
    await db.refresh(new_resource)
    return new_resource


# ---------------------------------------------------------------------------
# Converters
# ---------------------------------------------------------------------------


async def convert_image(
    db: AsyncSession,
    resource_id: int,
    converter_fn,
    ext: str,
    *,
    converter_args: tuple = (),
    converter_kwargs: dict | None = None,
) -> Resource:
    """Generic pipeline: validate -> build path -> temp file -> call converter -> finalize."""
    resource = await validate_resource(db, resource_id, ResourceCategory.image)
    source_path = build_source_path(resource)

    if ext is None:
        ext = source_path.suffix.lstrip(".")
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    kwargs = converter_kwargs or {}
    ok = await asyncio.to_thread(
        converter_fn, source_path, temp_path, *converter_args, **kwargs
    )
    if not ok:
        temp_path.unlink(missing_ok=True)
        raise ConversionError(f"{ext.upper()} conversion failed")

    return await finalize_conversion(temp_path, ext, resource, db)


async def convert_to_mp4(db: AsyncSession, resource_id: int, crf: int = 23) -> Resource:
    resource = await validate_resource(db, resource_id, ResourceCategory.video)
    source_path = build_source_path(resource)

    if source_path.suffix.lower() == ".mp4":
        raise ConversionNotNeededError("Resource is already MP4")

    ext = "mp4"
    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = MEDIA_DIR / (resource.folder or "") / temp_name

    probe = await probe_video(source_path)
    if probe and probe.is_mp4_ready:
        ok = await remux_to_mp4(source_path, temp_path)
    else:
        ok = await transcode_to_mp4(source_path, temp_path, crf=crf)

    if not ok:
        temp_path.unlink(missing_ok=True)
        raise ConversionError("MP4 conversion failed")

    return await finalize_conversion(
        temp_path, ext, resource, db, category=ResourceCategory.video
    )
