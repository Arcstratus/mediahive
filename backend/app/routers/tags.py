from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Tag, bookmark_tags, resource_tags
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
    resource_count_subq = (
        select(resource_tags.c.tag_id, func.count().label("cnt"))
        .group_by(resource_tags.c.tag_id)
        .subquery()
    )
    bookmark_count_subq = (
        select(bookmark_tags.c.tag_id, func.count().label("cnt"))
        .group_by(bookmark_tags.c.tag_id)
        .subquery()
    )
    result = await db.execute(
        select(
            Tag,
            (
                func.coalesce(resource_count_subq.c.cnt, 0)
                + func.coalesce(bookmark_count_subq.c.cnt, 0)
            ).label("resource_count"),
        )
        .outerjoin(resource_count_subq, Tag.id == resource_count_subq.c.tag_id)
        .outerjoin(bookmark_count_subq, Tag.id == bookmark_count_subq.c.tag_id)
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
