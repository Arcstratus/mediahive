from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Resource, Tag, resource_tags
from app.schemas import (
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


@router.get("/resources", response_model=PaginatedResponse)
async def list_resources(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type: str | None = Query(None),
    tag: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page

    base_query = select(Resource)
    count_query = select(func.count(Resource.id))

    if type:
        base_query = base_query.where(Resource.type == type)
        count_query = count_query.where(Resource.type == type)

    if tag:
        base_query = base_query.join(resource_tags).join(Tag).where(Tag.name == tag)
        count_query = count_query.join(resource_tags).join(Tag).where(Tag.name == tag)

    total = await db.scalar(count_query)
    result = await db.execute(
        base_query.order_by(Resource.created_at.desc()).offset(offset).limit(per_page)
    )
    items = result.scalars().unique().all()
    return PaginatedResponse(items=items, total=total, page=page, per_page=per_page)


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
    for key, value in update_data.items():
        setattr(resource, key, value)
    if tags_data is not None:
        resource.tags = await _resolve_tags(db, tags_data)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}", status_code=204)
async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    resource = await db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    await db.delete(resource)
    await db.commit()
