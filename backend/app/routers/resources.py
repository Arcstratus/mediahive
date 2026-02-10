import asyncio
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
    UploadFile,
)
from pydantic import BaseModel
from sqlalchemy import asc, desc, func, or_, select, type_coerce
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import String

from app.config import IMAGE_EXTENSIONS, MEDIA_DIR, THUMBNAIL_DIR, TRASH_DIR, VIDEO_EXTENSIONS
from app.database import async_session, get_db
from app.models import Resource, Tag, resource_tags
from app.schemas import (
    BatchDeleteRequest,
    BatchDeleteResponse,
    PaginatedResponse,
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)

router = APIRouter(tags=["Resources"])


async def _generate_thumbnail(video_path: Path, sha_prefix: str) -> str | None:
    """Extract a frame at 1s from a video and save as a JPEG thumbnail."""
    thumb_filename = f"{sha_prefix}_thumb.jpg"
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    thumb_path = THUMBNAIL_DIR / thumb_filename
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-ss", "1",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(thumb_path),
            "-y",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if proc.returncode == 0 and thumb_path.is_file():
            return thumb_filename
    except Exception:
        pass
    return None


async def _remux_ts_to_mp4(ts_path: Path, mp4_path: Path) -> bool:
    """Remux a .ts file to .mp4 using FFmpeg (copy streams, fix timestamps)."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-fflags", "+genpts+discardcorrupt",
            "-i", str(ts_path),
            "-c", "copy",
            "-movflags", "+faststart",
            "-avoid_negative_ts", "make_zero",
            str(mp4_path),
            "-y",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0 and mp4_path.is_file()
    except Exception:
        return False


async def _resolve_tags(db: AsyncSession, tag_names: list[str]) -> list[Tag]:
    """Resolve tag names to Tag objects, creating missing ones."""
    tags: list[Tag] = []
    for name in tag_names:
        tag = await db.scalar(select(Tag).where(Tag.name == name))
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
            await db.flush()
        tags.append(tag)
    return tags


@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(body: ResourceCreate, db: AsyncSession = Depends(get_db)):
    resource = Resource(
        category=body.category.value, filename=body.filename, title=body.title
    )
    if body.tags:
        resource.tags = await _resolve_tags(db, body.tags)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


_ext_expr = type_coerce(
    func.substr(Resource.filename, func.instr(Resource.filename, ".")), String
)

SORTABLE_COLUMNS = {
    "title": Resource.title,
    "filename": Resource.filename,
    "ext": _ext_expr,
    "created_at": Resource.created_at,
}


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
    offset = (page - 1) * per_page

    base_query = select(Resource).where(Resource.deleted_at.is_(None))
    count_query = select(func.count(Resource.id)).where(Resource.deleted_at.is_(None))

    if folder:
        base_query = base_query.where(Resource.folder == folder)
        count_query = count_query.where(Resource.folder == folder)

    if category:
        base_query = base_query.where(Resource.category == category)
        count_query = count_query.where(Resource.category == category)

    if search:
        condition = or_(
            Resource.title.icontains(search),
            Resource.filename.icontains(search),
        )
        base_query = base_query.where(condition)
        count_query = count_query.where(condition)

    if ext:
        ext_cond = or_(*[Resource.filename.endswith(e) for e in ext])
        base_query = base_query.where(ext_cond)
        count_query = count_query.where(ext_cond)

    if tag:
        for t in tag:
            tag_subq = (
                select(resource_tags.c.resource_id)
                .join(Tag)
                .where(Tag.name.icontains(t))
            )
            base_query = base_query.where(Resource.id.in_(tag_subq))
            count_query = count_query.where(Resource.id.in_(tag_subq))

    col = SORTABLE_COLUMNS.get(sort_by, Resource.created_at)
    order = desc(col) if sort_desc else asc(col)

    total = await db.scalar(count_query)
    result = await db.execute(base_query.order_by(order).offset(offset).limit(per_page))
    items = result.scalars().unique().all()
    return PaginatedResponse(items=items, total=total, page=page, per_page=per_page)


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
    query = select(Resource.id).where(Resource.deleted_at.is_(None))

    if folder:
        query = query.where(Resource.folder == folder)
    if category:
        query = query.where(Resource.category == category)
    if search:
        query = query.where(
            or_(Resource.title.icontains(search), Resource.filename.icontains(search))
        )
    if ext:
        query = query.where(or_(*[Resource.filename.endswith(e) for e in ext]))
    if tag:
        for t in tag:
            tag_subq = (
                select(resource_tags.c.resource_id)
                .join(Tag)
                .where(Tag.name.icontains(t))
            )
            query = query.where(Resource.id.in_(tag_subq))

    col = SORTABLE_COLUMNS.get(sort_by, Resource.created_at)
    order = desc(col) if sort_desc else asc(col)

    result = await db.execute(query.order_by(order))
    return list(result.scalars().all())


@router.get("/resources/folders")
async def list_resource_folders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Resource.folder, func.count(Resource.id))
        .where(Resource.folder.isnot(None))
        .where(Resource.deleted_at.is_(None))
        .group_by(Resource.folder)
        .order_by(Resource.folder)
    )
    return [{"folder": f, "count": c} for f, c in result.all()]


@router.post("/resources/batch-delete", response_model=BatchDeleteResponse)
async def batch_delete_resources(
    body: BatchDeleteRequest, db: AsyncSession = Depends(get_db)
):
    deleted = 0
    now = datetime.now(timezone.utc)
    for resource_id in body.ids:
        resource = await db.get(Resource, resource_id)
        if not resource or resource.deleted_at is not None:
            continue
        if resource.thumbnail:
            thumb_path = THUMBNAIL_DIR / resource.thumbnail
            if thumb_path.is_file():
                thumb_path.unlink()
        if resource.filename:
            src = MEDIA_DIR / (resource.folder or "") / resource.filename
            if src.is_file():
                TRASH_DIR.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(TRASH_DIR / resource.filename))
        resource.deleted_at = now
        deleted += 1
    await db.commit()
    return BatchDeleteResponse(deleted=deleted)


@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int, body: ResourceUpdate, db: AsyncSession = Depends(get_db)
):
    resource = await db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    update_data = body.model_dump(exclude_unset=True)
    tags_data = update_data.pop("tags", None)
    folder_data = update_data.pop("folder", ...)

    for key, value in update_data.items():
        setattr(resource, key, value)
    if tags_data is not None:
        resource.tags = await _resolve_tags(db, tags_data)

    if folder_data is not ...:
        new_folder = folder_data.strip() if folder_data else None
        if new_folder == "":
            new_folder = None
        if new_folder and ".." in new_folder:
            raise HTTPException(status_code=400, detail="Invalid folder path")
        old_folder = resource.folder
        if new_folder != old_folder:
            if resource.filename:
                old_path = MEDIA_DIR / (old_folder or "") / resource.filename
                new_path = MEDIA_DIR / (new_folder or "") / resource.filename
                if old_path.is_file():
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(old_path), str(new_path))
            resource.folder = new_folder

    await db.commit()
    await db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}", status_code=204)
async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Resource not found")
    if resource.thumbnail:
        thumb_path = THUMBNAIL_DIR / resource.thumbnail
        if thumb_path.is_file():
            thumb_path.unlink()
    if resource.filename:
        src = MEDIA_DIR / (resource.folder or "") / resource.filename
        if src.is_file():
            TRASH_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(TRASH_DIR / resource.filename))
    resource.deleted_at = datetime.now(timezone.utc)
    await db.commit()


class DownloadRequest(BaseModel):
    url: str


async def _download_direct(url: str) -> bytes:
    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.content


async def _download_m3u8(url: str) -> tuple[bytes, str]:
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


_ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | {".m3u8"}


async def _bg_download(url: str, ext: str) -> None:
    if ext == ".m3u8":
        content, _ = await _download_m3u8(url)
    else:
        content = await _download_direct(url)

    sha = hashlib.sha256(content).hexdigest()
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    if ext == ".m3u8":
        # Write TS to a temp file, remux to MP4, then delete the temp
        tmp_ts = MEDIA_DIR / f"{sha}.ts.tmp"
        with open(tmp_ts, "wb") as f:
            f.write(content)
        mp4_path = MEDIA_DIR / f"{sha}.mp4"
        ok = await _remux_ts_to_mp4(tmp_ts, mp4_path)
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
    category = "video" if ext in VIDEO_EXTENSIONS else "image"

    thumbnail = None
    if category == "video":
        thumbnail = await _generate_thumbnail(MEDIA_DIR / filename, sha)

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


@router.post("/resources/download", status_code=202)
async def download_resource(body: DownloadRequest, bg: BackgroundTasks):
    parsed = urlparse(body.url)
    ext = Path(parsed.path).suffix.lower()

    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported URL extension: {ext or '(none)'}",
        )

    bg.add_task(_bg_download, body.url, ext)
    return {"status": "downloading"}


@router.post("/resources/upload", response_model=ResourceResponse, status_code=201)
async def upload_resource(
    file: UploadFile,
    title: str | None = None,
    tags: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    sha256 = hashlib.sha256(content).hexdigest()
    ext = Path(file.filename or "").suffix.lower()
    new_name = f"{sha256}{ext}"

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    dest = MEDIA_DIR / new_name
    if not dest.exists():
        with open(dest, "wb") as f:
            f.write(content)

    category = "image"
    if ext in VIDEO_EXTENSIONS:
        category = "video"
    elif ext not in IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"Unsupported file extension: {ext}"
        )

    thumbnail = None
    if category == "video":
        sha_prefix = sha256
        thumbnail = await _generate_thumbnail(dest, sha_prefix)

    resource = Resource(
        category=category,
        title=title or file.filename,
        filename=new_name,
        thumbnail=thumbnail,
    )
    if tags:
        tag_names = [t.strip() for t in tags.split(",") if t.strip()]
        resource.tags = await _resolve_tags(db, tag_names)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


class ThumbnailRequest(BaseModel):
    timestamp: float


@router.post("/resources/{resource_id}/thumbnail", response_model=ResourceResponse)
async def set_thumbnail(
    resource_id: int, body: ThumbnailRequest, db: AsyncSession = Depends(get_db)
):
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Resource not found")
    if resource.category != "video":
        raise HTTPException(status_code=400, detail="Resource is not a video")
    if not resource.filename:
        raise HTTPException(status_code=400, detail="Video file not found")

    video_path = MEDIA_DIR / (resource.folder or "") / resource.filename
    if not video_path.is_file():
        raise HTTPException(status_code=400, detail="Video file not found")

    # Delete old thumbnail if exists
    if resource.thumbnail:
        old_thumb = THUMBNAIL_DIR / resource.thumbnail
        if old_thumb.is_file():
            old_thumb.unlink()

    sha_prefix = resource.filename.rsplit(".", 1)[0]

    # For manual set_thumbnail, use the user-specified timestamp
    thumb_filename = f"{sha_prefix}_thumb.jpg"
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    thumb_path = THUMBNAIL_DIR / thumb_filename
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-ss", str(body.timestamp),
        "-i", str(video_path),
        "-frames:v", "1",
        "-q:v", "2",
        str(thumb_path),
        "-y",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    if proc.returncode != 0 or not thumb_path.is_file():
        raise HTTPException(status_code=400, detail="FFmpeg extraction failed")

    resource.thumbnail = thumb_filename
    await db.commit()
    await db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}/thumbnail", response_model=ResourceResponse)
async def remove_thumbnail(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource.thumbnail:
        thumb_path = THUMBNAIL_DIR / resource.thumbnail
        if thumb_path.is_file():
            thumb_path.unlink()
        resource.thumbnail = None
        await db.commit()
        await db.refresh(resource)

    return resource
