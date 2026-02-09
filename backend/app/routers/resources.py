from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Resource
from app.schemas import (
    PaginatedResponse,
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)

router = APIRouter(tags=["Resources"])


@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(body: ResourceCreate, db: AsyncSession = Depends(get_db)):
    resource = Resource(type=body.type.value, url=body.url, title=body.title)
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.get("/resources", response_model=PaginatedResponse)
async def list_resources(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    total = await db.scalar(select(func.count(Resource.id)))
    result = await db.execute(
        select(Resource)
        .order_by(Resource.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    items = result.scalars().all()
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
    for key, value in update_data.items():
        setattr(resource, key, value)
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
