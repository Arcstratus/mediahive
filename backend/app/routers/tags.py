from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Tag, resource_tags
from app.schemas import TagCreate, TagResponse

router = APIRouter(tags=["Tags"])


@router.post("/tags", response_model=TagResponse, status_code=201)
async def create_tag(body: TagCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(Tag).where(Tag.name == body.name))
    if existing:
        raise HTTPException(status_code=409, detail="Tag already exists")
    tag = Tag(name=body.name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    count_subq = (
        select(resource_tags.c.tag_id, func.count().label("resource_count"))
        .group_by(resource_tags.c.tag_id)
        .subquery()
    )
    result = await db.execute(
        select(
            Tag,
            func.coalesce(count_subq.c.resource_count, 0).label("resource_count"),
        )
        .outerjoin(count_subq, Tag.id == count_subq.c.tag_id)
        .order_by(Tag.name)
    )
    return [
        TagResponse.model_validate(
            {**row.Tag.__dict__, "resource_count": row.resource_count}
        )
        for row in result.all()
    ]


@router.delete("/tags/{tag_id}", status_code=204)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await db.delete(tag)
    await db.commit()
