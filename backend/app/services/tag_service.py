from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import TagAlreadyExistsError, TagNotFoundError
from app.models import Tag, bookmark_tags, resource_tags
from app.schemas import TagResponse


async def resolve_tags(db: AsyncSession, tag_names: list[str]) -> list[Tag]:
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


async def create_tag(db: AsyncSession, name: str) -> Tag:
    existing = await db.scalar(select(Tag).where(Tag.name == name))
    if existing:
        raise TagAlreadyExistsError("Tag already exists")
    tag = Tag(name=name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(db: AsyncSession, tag_id: int, name: str) -> Tag:
    tag = await db.get(Tag, tag_id)
    if not tag:
        raise TagNotFoundError("Tag not found")
    existing = await db.scalar(select(Tag).where(Tag.name == name, Tag.id != tag_id))
    if existing:
        raise TagAlreadyExistsError("Tag already exists")
    tag.name = name
    await db.commit()
    await db.refresh(tag)
    return tag


async def list_tags_with_counts(db: AsyncSession) -> list[TagResponse]:
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


async def delete_tag(db: AsyncSession, tag_id: int) -> None:
    tag = await db.get(Tag, tag_id)
    if not tag:
        raise TagNotFoundError("Tag not found")
    await db.delete(tag)
    await db.commit()
