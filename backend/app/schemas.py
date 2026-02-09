from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ResourceType(str, Enum):
    url = "url"
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
    type: ResourceType
    url: str | None = None
    title: str | None = None
    tags: list[str] = []


class ResourceUpdate(BaseModel):
    url: str | None = None
    title: str | None = None
    folder: str | None = None
    tags: list[str] | None = None


class ResourceResponse(BaseModel):
    id: int
    type: ResourceType
    url: str | None
    title: str | None
    folder: str | None = None
    created_at: datetime
    tags: list[TagResponse] = []

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
    type: ResourceType
    size: int


class ScanResponse(BaseModel):
    files: list[ScannedFile]


class ImportFileItem(BaseModel):
    path: str
    type: ResourceType


class ImportRequest(BaseModel):
    files: list[ImportFileItem]


class ImportResponse(BaseModel):
    imported: int
    skipped: int


class StatsResponse(BaseModel):
    images: int
    videos: int
    urls: int
    tags: int
