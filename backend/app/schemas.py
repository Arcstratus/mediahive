from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ResourceType(str, Enum):
    url = "url"
    image = "image"
    video = "video"


class ResourceCreate(BaseModel):
    type: ResourceType
    url: str | None = None
    title: str | None = None


class ResourceUpdate(BaseModel):
    url: str | None = None
    title: str | None = None


class ResourceResponse(BaseModel):
    id: int
    type: ResourceType
    url: str | None
    title: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    items: list[ResourceResponse]
    total: int
    page: int
    per_page: int
