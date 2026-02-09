import hashlib
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy import asc, desc, func, or_, select, type_coerce
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import String

import shutil

from app.config import IMAGE_EXTENSIONS, MEDIA_DIR, TRASH_DIR, VIDEO_EXTENSIONS
from app.database import get_db
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
    resource = Resource(type=body.type.value, url=body.url, title=body.title)
    if body.tags:
        resource.tags = await _resolve_tags(db, body.tags)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


_ext_expr = type_coerce(
    func.substr(Resource.url, func.instr(Resource.url, ".")), String
)

SORTABLE_COLUMNS = {
    "title": Resource.title,
    "url": Resource.url,
    "ext": _ext_expr,
    "created_at": Resource.created_at,
}


@router.get("/resources", response_model=PaginatedResponse)
async def list_resources(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type: str | None = Query(None),
    search: str | None = Query(None),
    ext: list[str] = Query(None),
    tag: list[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page

    base_query = select(Resource)
    count_query = select(func.count(Resource.id))

    if type:
        base_query = base_query.where(Resource.type == type)
        count_query = count_query.where(Resource.type == type)

    if search:
        condition = or_(
            Resource.title.icontains(search),
            Resource.url.icontains(search),
        )
        base_query = base_query.where(condition)
        count_query = count_query.where(condition)

    if ext:
        ext_cond = or_(*[Resource.url.endswith(e) for e in ext])
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
    type: str | None = Query(None),
    search: str | None = Query(None),
    ext: list[str] = Query(None),
    tag: list[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    query = select(Resource.id)

    if type:
        query = query.where(Resource.type == type)
    if search:
        query = query.where(
            or_(Resource.title.icontains(search), Resource.url.icontains(search))
        )
    if ext:
        query = query.where(or_(*[Resource.url.endswith(e) for e in ext]))
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


@router.post("/resources/batch-delete", response_model=BatchDeleteResponse)
async def batch_delete_resources(
    body: BatchDeleteRequest, db: AsyncSession = Depends(get_db)
):
    deleted = 0
    for resource_id in body.ids:
        resource = await db.get(Resource, resource_id)
        if not resource:
            continue
        if resource.url and resource.type in ("image", "video"):
            src = MEDIA_DIR / (resource.folder or "") / resource.url
            if src.is_file():
                TRASH_DIR.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(TRASH_DIR / resource.url))
        await db.delete(resource)
        deleted += 1
    await db.commit()
    return BatchDeleteResponse(deleted=deleted)


@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource:
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
            if resource.url and resource.type in ("image", "video"):
                old_path = MEDIA_DIR / (old_folder or "") / resource.url
                new_path = MEDIA_DIR / (new_folder or "") / resource.url
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
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    if resource.url and resource.type in ("image", "video"):
        src = MEDIA_DIR / (resource.folder or "") / resource.url
        if src.is_file():
            TRASH_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(TRASH_DIR / resource.url))
    await db.delete(resource)
    await db.commit()


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

    resource_type = "image"
    if ext in VIDEO_EXTENSIONS:
        resource_type = "video"
    elif ext not in IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"Unsupported file extension: {ext}"
        )

    resource = Resource(
        type=resource_type,
        title=title or file.filename,
        url=new_name,
    )
    if tags:
        tag_names = [t.strip() for t in tags.split(",") if t.strip()]
        resource.tags = await _resolve_tags(db, tag_names)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource
