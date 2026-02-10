from datetime import datetime

from pydantic import BaseModel

from .tag import TagResponse


class BookmarkCreate(BaseModel):
    title: str | None = None
    url: str
    description: str | None = None
    folder: str | None = None
    tags: list[str] = []


class BookmarkUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    description: str | None = None
    folder: str | None = None
    tags: list[str] | None = None


class BookmarkResponse(BaseModel):
    id: int
    title: str | None
    url: str
    description: str | None
    folder: str | None
    created_at: datetime
    tags: list[TagResponse] = []

    model_config = {"from_attributes": True}


class BatchCreateBookmarkResponse(BaseModel):
    created: int
    items: list[BookmarkResponse]


class PaginatedBookmarkResponse(BaseModel):
    items: list[BookmarkResponse]
    total: int
    page: int
    per_page: int
