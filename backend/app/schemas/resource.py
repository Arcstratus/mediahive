from datetime import datetime

from pydantic import BaseModel

from app.models import ResourceCategory
from .tag import TagResponse


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
    thumbnail: str | None = None
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
