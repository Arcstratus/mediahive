from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

from app.exceptions import BookmarkAlreadyExistsError, BookmarkNotFoundError
from app.models import Bookmark, Tag, bookmark_tags
from app.schemas import BookmarkCreate, BookmarkUpdate
from app.services import tag_service

SORTABLE_COLUMNS = {
    "title": Bookmark.title,
    "url": Bookmark.url,
    "created_at": Bookmark.created_at,
}


async def create_bookmark(db: AsyncSession, body: BookmarkCreate) -> Bookmark:
    bookmark = Bookmark(
        title=body.title,
        url=body.url,
        description=body.description,
        folder=body.folder,
    )
    if body.tags:
        bookmark.tags = await tag_service.resolve_tags(db, body.tags)
    db.add(bookmark)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise BookmarkAlreadyExistsError("Bookmark with this URL already exists")
    await db.refresh(bookmark)
    return bookmark


async def batch_create_bookmarks(
    db: AsyncSession, items: list[BookmarkCreate]
) -> list[Bookmark]:
    existing_urls = set(
        (await db.scalars(
            select(Bookmark.url).where(
                Bookmark.url.in_([b.url for b in items])
            )
        )).all()
    )
    seen_urls: set[str] = set()
    bookmarks = []
    for body in items:
        if body.url in existing_urls or body.url in seen_urls:
            continue
        seen_urls.add(body.url)
        bookmark = Bookmark(
            title=body.title,
            url=body.url,
            description=body.description,
            folder=body.folder,
        )
        if body.tags:
            bookmark.tags = await tag_service.resolve_tags(db, body.tags)
        db.add(bookmark)
        bookmarks.append(bookmark)
    await db.commit()
    for bm in bookmarks:
        await db.refresh(bm)
    return bookmarks


async def list_bookmarks(
    db: AsyncSession,
    *,
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    tag: list[str] | None = None,
    sort_by: str = "created_at",
    sort_desc: bool = True,
) -> tuple[list[Bookmark], int]:
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
    items = list(result.scalars().unique().all())
    return items, total


async def get_bookmark(db: AsyncSession, bookmark_id: int) -> Bookmark:
    bookmark = await db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise BookmarkNotFoundError("Bookmark not found")
    return bookmark


async def update_bookmark(
    db: AsyncSession, bookmark_id: int, body: BookmarkUpdate
) -> Bookmark:
    bookmark = await db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise BookmarkNotFoundError("Bookmark not found")
    update_data = body.model_dump(exclude_unset=True)
    tags_data = update_data.pop("tags", None)

    for key, value in update_data.items():
        setattr(bookmark, key, value)
    if tags_data is not None:
        bookmark.tags = await tag_service.resolve_tags(db, tags_data)

    await db.commit()
    await db.refresh(bookmark)
    return bookmark


async def delete_bookmark(db: AsyncSession, bookmark_id: int) -> None:
    bookmark = await db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise BookmarkNotFoundError("Bookmark not found")
    await db.delete(bookmark)
    await db.commit()


async def batch_delete_bookmarks(db: AsyncSession, ids: list[int]) -> int:
    deleted = 0
    for bookmark_id in ids:
        bookmark = await db.get(Bookmark, bookmark_id)
        if not bookmark:
            continue
        await db.delete(bookmark)
        deleted += 1
    await db.commit()
    return deleted
