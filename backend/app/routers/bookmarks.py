from fastapi import Depends, Query
from fastapi_error_map import ErrorAwareRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import BookmarkAlreadyExistsError, BookmarkNotFoundError
from app.schemas import (
    BatchCreateBookmarkResponse,
    BatchDeleteRequest,
    BookmarkCreate,
    BookmarkResponse,
    BookmarkUpdate,
    PaginatedBookmarkResponse,
)
from app.services import bookmark_service

router = ErrorAwareRouter(tags=["Bookmarks"])


@router.post(
    "/bookmarks",
    response_model=BatchCreateBookmarkResponse,
    status_code=201,
    error_map={BookmarkAlreadyExistsError: 409},
)
async def create_bookmarks(
    body: list[BookmarkCreate], db: AsyncSession = Depends(get_db)
):
    if len(body) == 1:
        item = await bookmark_service.create_bookmark(db, body[0])
        return BatchCreateBookmarkResponse(created=1, items=[item])
    items = await bookmark_service.batch_create_bookmarks(db, body)
    return BatchCreateBookmarkResponse(created=len(items), items=items)


@router.get("/bookmarks", response_model=PaginatedBookmarkResponse)
async def list_bookmarks(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    tag: list[str] = Query(None),
    folder: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    items, total = await bookmark_service.list_bookmarks(
        db,
        page=page,
        per_page=per_page,
        search=search,
        tag=tag,
        folder=folder,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )
    return PaginatedBookmarkResponse(
        items=items, total=total, page=page, per_page=per_page
    )


@router.get("/bookmarks/folders")
async def list_bookmark_folders(db: AsyncSession = Depends(get_db)):
    return await bookmark_service.list_bookmark_folders(db)


@router.get(
    "/bookmarks/{bookmark_id}",
    response_model=BookmarkResponse,
    error_map={BookmarkNotFoundError: 404},
)
async def get_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    return await bookmark_service.get_bookmark(db, bookmark_id)


@router.put(
    "/bookmarks/{bookmark_id}",
    response_model=BookmarkResponse,
    error_map={BookmarkNotFoundError: 404},
)
async def update_bookmark(
    bookmark_id: int, body: BookmarkUpdate, db: AsyncSession = Depends(get_db)
):
    return await bookmark_service.update_bookmark(db, bookmark_id, body)


@router.delete("/bookmarks", status_code=204)
async def batch_delete_bookmarks(
    body: BatchDeleteRequest, db: AsyncSession = Depends(get_db)
):
    await bookmark_service.batch_delete_bookmarks(db, body.ids)


@router.delete(
    "/bookmarks/{bookmark_id}", status_code=204, error_map={BookmarkNotFoundError: 404}
)
async def delete_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    await bookmark_service.delete_bookmark(db, bookmark_id)
