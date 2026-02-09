from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Bookmark, Tag, bookmark_tags
from app.schemas import (
    BatchDeleteRequest,
    BatchDeleteResponse,
    BookmarkCreate,
    BookmarkResponse,
    BookmarkUpdate,
    PaginatedBookmarkResponse,
)

router = APIRouter(tags=["Bookmarks"])


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


SORTABLE_COLUMNS = {
    "title": Bookmark.title,
    "url": Bookmark.url,
    "created_at": Bookmark.created_at,
}


@router.post("/bookmarks", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(body: BookmarkCreate, db: AsyncSession = Depends(get_db)):
    bookmark = Bookmark(
        title=body.title,
        url=body.url,
        description=body.description,
        folder=body.folder,
    )
    if body.tags:
        bookmark.tags = await _resolve_tags(db, body.tags)
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return bookmark


@router.get("/bookmarks", response_model=PaginatedBookmarkResponse)
async def list_bookmarks(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    tag: list[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page

    base_query = select(Bookmark)
    count_query = select(func.count(Bookmark.id))

    if search:
        condition = or_(
            Bookmark.title.icontains(search),
            Bookmark.url.icontains(search),
            Bookmark.description.icontains(search),
        )
        base_query = base_query.where(condition)
        count_query = count_query.where(condition)

    if tag:
        for t in tag:
            tag_subq = (
                select(bookmark_tags.c.bookmark_id)
                .join(Tag)
                .where(Tag.name.icontains(t))
            )
            base_query = base_query.where(Bookmark.id.in_(tag_subq))
            count_query = count_query.where(Bookmark.id.in_(tag_subq))

    col = SORTABLE_COLUMNS.get(sort_by, Bookmark.created_at)
    order = desc(col) if sort_desc else asc(col)

    total = await db.scalar(count_query)
    result = await db.execute(base_query.order_by(order).offset(offset).limit(per_page))
    items = result.scalars().unique().all()
    return PaginatedBookmarkResponse(
        items=items, total=total, page=page, per_page=per_page
    )


@router.get("/bookmarks/{bookmark_id}", response_model=BookmarkResponse)
async def get_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    bookmark = await db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.put("/bookmarks/{bookmark_id}", response_model=BookmarkResponse)
async def update_bookmark(
    bookmark_id: int, body: BookmarkUpdate, db: AsyncSession = Depends(get_db)
):
    bookmark = await db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    update_data = body.model_dump(exclude_unset=True)
    tags_data = update_data.pop("tags", None)

    for key, value in update_data.items():
        setattr(bookmark, key, value)
    if tags_data is not None:
        bookmark.tags = await _resolve_tags(db, tags_data)

    await db.commit()
    await db.refresh(bookmark)
    return bookmark


@router.delete("/bookmarks/{bookmark_id}", status_code=204)
async def delete_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    bookmark = await db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await db.delete(bookmark)
    await db.commit()


@router.post("/bookmarks/batch-delete", response_model=BatchDeleteResponse)
async def batch_delete_bookmarks(
    body: BatchDeleteRequest, db: AsyncSession = Depends(get_db)
):
    deleted = 0
    for bookmark_id in body.ids:
        bookmark = await db.get(Bookmark, bookmark_id)
        if not bookmark:
            continue
        await db.delete(bookmark)
        deleted += 1
    await db.commit()
    return BatchDeleteResponse(deleted=deleted)
