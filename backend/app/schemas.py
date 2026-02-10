from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ResourceCategory(str, Enum):
    image = "image"
    video = "video"


class TagCreate(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    resource_count: int = 0

    model_config = {"from_attributes": True}


class ResourceCreate(BaseModel):
    category: ResourceCategory
    filename: str | None = None
    title: str | None = None
    tags: list[str] = []


class ResourceUpdate(BaseModel):
    title: str | None = None
    folder: str | None = None
    tags: list[str] | None = None


class ResourceResponse(BaseModel):
    id: int
    category: ResourceCategory
    filename: str | None
    title: str | None
    folder: str | None = None
    created_at: datetime
    tags: list[TagResponse] = []

    model_config = {"from_attributes": True}


class TrashResponse(BaseModel):
    id: int
    category: ResourceCategory
    filename: str | None
    title: str | None
    folder: str | None = None
    created_at: datetime
    deleted_at: datetime | None = None

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    items: list[ResourceResponse]
    total: int
    page: int
    per_page: int


class ScanRequest(BaseModel):
    path: str


class ScannedFile(BaseModel):
    path: str
    name: str
    type: ResourceCategory
    size: int


class ScanResponse(BaseModel):
    files: list[ScannedFile]


class ImportFileItem(BaseModel):
    path: str
    type: ResourceCategory


class ImportRequest(BaseModel):
    files: list[ImportFileItem]


class ImportResponse(BaseModel):
    imported: int
    skipped: int


class StatsResponse(BaseModel):
    images: int
    videos: int
    bookmarks: int
    tags: int


class BatchDeleteRequest(BaseModel):
    ids: list[int]


class BatchDeleteResponse(BaseModel):
    deleted: int


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


class PaginatedBookmarkResponse(BaseModel):
    items: list[BookmarkResponse]
    total: int
    page: int
    per_page: int
