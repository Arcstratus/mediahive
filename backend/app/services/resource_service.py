import asyncio
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import httpx
from sqlalchemy import asc, desc, func, or_, select, type_coerce
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import String

from app.config import (
    IMAGE_EXTENSIONS,
    MEDIA_DIR,
    THUMBNAIL_DIR,
    VIDEO_EXTENSIONS,
)
from app.converters import remux_to_mp4
from app.database import async_session
from app.exceptions import ResourceNotFoundError, ResourceValidationError
from app.models import Resource, ResourceCategory, Tag, resource_tags
from app.schemas import (
    PaginatedResponse,
    ResourceCreate,
    ResourceUpdate,
)
from app.services.file_service import (
    delete_thumbnail,
    generate_thumbnail,
    move_file,
    move_to_trash,
    sha256_hash,
)
from app.services.tag_service import resolve_tags

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_ext_expr = type_coerce(
    func.substr(Resource.filename, func.instr(Resource.filename, ".")), String
)

SORTABLE_COLUMNS = {
    "title": Resource.title,
    "filename": Resource.filename,
    "ext": _ext_expr,
    "created_at": Resource.created_at,
}

ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | {".m3u8"}


# ---------------------------------------------------------------------------
# Resource CRUD
# ---------------------------------------------------------------------------


async def create_resource(db: AsyncSession, body: ResourceCreate) -> Resource:
    resource = Resource(
        category=body.category, filename=body.filename, title=body.title
    )
    if body.tags:
        resource.tags = await resolve_tags(db, body.tags)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


def _apply_filters(query, *, category, search, ext, tag, folder):
    if folder:
        query = query.where(Resource.folder == folder)
    if category:
        query = query.where(Resource.category == category)
    if search:
        condition = or_(
            Resource.title.icontains(search),
            Resource.filename.icontains(search),
        )
        query = query.where(condition)
    if ext:
        ext_cond = or_(*[Resource.filename.endswith(e) for e in ext])
        query = query.where(ext_cond)
    if tag:
        for t in tag:
            tag_subq = (
                select(resource_tags.c.resource_id)
                .join(Tag)
                .where(Tag.name.icontains(t))
            )
            query = query.where(Resource.id.in_(tag_subq))
    return query


async def list_resources(
    db: AsyncSession,
    *,
    page: int = 1,
    per_page: int = 20,
    category: str | None = None,
    search: str | None = None,
    ext: list[str] | None = None,
    tag: list[str] | None = None,
    folder: str | None = None,
    sort_by: str = "created_at",
    sort_desc: bool = True,
) -> PaginatedResponse:
    offset = (page - 1) * per_page

    base_query = select(Resource).where(Resource.deleted_at.is_(None))
    count_query = select(func.count(Resource.id)).where(Resource.deleted_at.is_(None))

    base_query = _apply_filters(
        base_query, category=category, search=search, ext=ext, tag=tag, folder=folder
    )
    count_query = _apply_filters(
        count_query, category=category, search=search, ext=ext, tag=tag, folder=folder
    )

    col = SORTABLE_COLUMNS.get(sort_by, Resource.created_at)
    order = desc(col) if sort_desc else asc(col)

    total = await db.scalar(count_query)
    result = await db.execute(base_query.order_by(order).offset(offset).limit(per_page))
    items = result.scalars().unique().all()
    return PaginatedResponse(items=items, total=total, page=page, per_page=per_page)


async def list_resource_ids(
    db: AsyncSession,
    *,
    category: str | None = None,
    search: str | None = None,
    ext: list[str] | None = None,
    tag: list[str] | None = None,
    folder: str | None = None,
    sort_by: str = "created_at",
    sort_desc: bool = True,
) -> list[int]:
    query = select(Resource.id).where(Resource.deleted_at.is_(None))
    query = _apply_filters(
        query, category=category, search=search, ext=ext, tag=tag, folder=folder
    )

    col = SORTABLE_COLUMNS.get(sort_by, Resource.created_at)
    order = desc(col) if sort_desc else asc(col)

    result = await db.execute(query.order_by(order))
    return list(result.scalars().all())


async def list_resource_folders(db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(Resource.folder, func.count(Resource.id))
        .where(Resource.folder.isnot(None))
        .where(Resource.deleted_at.is_(None))
        .group_by(Resource.folder)
        .order_by(Resource.folder)
    )
    return [{"folder": f, "count": c} for f, c in result.all()]


async def get_resource(db: AsyncSession, resource_id: int) -> Resource:
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise ResourceNotFoundError("Resource not found")
    return resource


async def update_resource(
    db: AsyncSession, resource_id: int, body: ResourceUpdate
) -> Resource:
    resource = await db.get(Resource, resource_id)
    if not resource:
        raise ResourceNotFoundError("Resource not found")
    update_data = body.model_dump(exclude_unset=True)
    tags_data = update_data.pop("tags", None)
    folder_data = update_data.pop("folder", ...)

    for key, value in update_data.items():
        setattr(resource, key, value)
    if tags_data is not None:
        resource.tags = await resolve_tags(db, tags_data)

    if folder_data is not ...:
        new_folder = folder_data.strip() if folder_data else None
        if new_folder == "":
            new_folder = None
        if new_folder and ".." in new_folder:
            raise ResourceValidationError("Invalid folder path")
        old_folder = resource.folder
        if new_folder != old_folder:
            if resource.filename:
                move_file(resource.filename, old_folder, new_folder)
            resource.folder = new_folder

    await db.commit()
    await db.refresh(resource)
    return resource


# ---------------------------------------------------------------------------
# Soft-delete / batch-delete
# ---------------------------------------------------------------------------


async def soft_delete_resource(db: AsyncSession, resource_id: int) -> None:
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise ResourceNotFoundError("Resource not found")
    delete_thumbnail(resource.thumbnail)
    if resource.filename:
        move_to_trash(resource.filename, resource.folder)
    resource.deleted_at = datetime.now(timezone.utc)
    await db.commit()


async def batch_soft_delete(db: AsyncSession, ids: list[int]) -> int:
    deleted = 0
    now = datetime.now(timezone.utc)
    for resource_id in ids:
        resource = await db.get(Resource, resource_id)
        if not resource or resource.deleted_at is not None:
            continue
        delete_thumbnail(resource.thumbnail)
        if resource.filename:
            move_to_trash(resource.filename, resource.folder)
        resource.deleted_at = now
        deleted += 1
    await db.commit()
    return deleted


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------


async def download_direct(url: str) -> bytes:
    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.content


async def download_m3u8(url: str) -> tuple[bytes, str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        playlist = resp.text

        segments: list[str] = []
        for line in playlist.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            segments.append(urljoin(url, line))

        chunks: list[bytes] = []
        for seg_url in segments:
            seg_resp = await client.get(seg_url)
            seg_resp.raise_for_status()
            chunks.append(seg_resp.content)

        return b"".join(chunks), ".ts"


async def bg_download(url: str, ext: str) -> None:
    if ext == ".m3u8":
        content, _ = await download_m3u8(url)
    else:
        content = await download_direct(url)

    sha = sha256_hash(content)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    if ext == ".m3u8":
        tmp_ts = MEDIA_DIR / f"{sha}.ts.tmp"
        with open(tmp_ts, "wb") as f:
            f.write(content)
        mp4_path = MEDIA_DIR / f"{sha}.mp4"
        ok = await remux_to_mp4(tmp_ts, mp4_path)
        tmp_ts.unlink(missing_ok=True)
        if not ok:
            return
        ext = ".mp4"
    else:
        dest = MEDIA_DIR / f"{sha}{ext}"
        if not dest.exists():
            with open(dest, "wb") as f:
                f.write(content)

    filename = f"{sha}{ext}"
    category = (
        ResourceCategory.video if ext in VIDEO_EXTENSIONS else ResourceCategory.image
    )

    thumbnail = None
    if category == ResourceCategory.video:
        thumbnail = await generate_thumbnail(MEDIA_DIR / filename, sha)

    async with async_session() as db:
        existing = await db.scalar(
            select(Resource).where(Resource.filename == filename)
        )
        if existing:
            return
        resource = Resource(
            category=category, title=filename, filename=filename, thumbnail=thumbnail
        )
        db.add(resource)
        await db.commit()


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------


async def upload_resource(
    db: AsyncSession,
    file_content: bytes,
    filename: str | None,
    title: str | None,
    tags_csv: str | None,
) -> Resource:
    sha = sha256_hash(file_content)
    ext = Path(filename or "").suffix.lower()
    new_name = f"{sha}{ext}"

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    dest = MEDIA_DIR / new_name
    if not dest.exists():
        with open(dest, "wb") as f:
            f.write(file_content)

    category = ResourceCategory.image
    if ext in VIDEO_EXTENSIONS:
        category = ResourceCategory.video
    elif ext not in IMAGE_EXTENSIONS:
        raise ResourceValidationError(f"Unsupported file extension: {ext}")

    thumbnail = None
    if category == ResourceCategory.video:
        thumbnail = await generate_thumbnail(dest, sha)

    resource = Resource(
        category=category,
        title=title or filename,
        filename=new_name,
        thumbnail=thumbnail,
    )
    if tags_csv:
        tag_names = [t.strip() for t in tags_csv.split(",") if t.strip()]
        resource.tags = await resolve_tags(db, tag_names)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


# ---------------------------------------------------------------------------
# Thumbnail management
# ---------------------------------------------------------------------------


async def set_thumbnail(
    db: AsyncSession, resource_id: int, timestamp: float
) -> Resource:
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise ResourceNotFoundError("Resource not found")
    if resource.category != ResourceCategory.video:
        raise ResourceValidationError("Resource is not a video")
    if not resource.filename:
        raise ResourceValidationError("Video file not found")

    video_path = MEDIA_DIR / (resource.folder or "") / resource.filename
    if not video_path.is_file():
        raise ResourceValidationError("Video file not found")

    # Delete old thumbnail if exists
    delete_thumbnail(resource.thumbnail)

    sha_prefix = resource.filename.rsplit(".", 1)[0]
    thumb_filename = f"{sha_prefix}_thumb.jpg"
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    thumb_path = THUMBNAIL_DIR / thumb_filename
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-ss",
        str(timestamp),
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(thumb_path),
        "-y",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    if proc.returncode != 0 or not thumb_path.is_file():
        raise ResourceValidationError("FFmpeg extraction failed")

    resource.thumbnail = thumb_filename
    await db.commit()
    await db.refresh(resource)
    return resource


async def remove_thumbnail(db: AsyncSession, resource_id: int) -> Resource:
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise ResourceNotFoundError("Resource not found")

    if resource.thumbnail:
        delete_thumbnail(resource.thumbnail)
        resource.thumbnail = None
        await db.commit()
        await db.refresh(resource)

    return resource
