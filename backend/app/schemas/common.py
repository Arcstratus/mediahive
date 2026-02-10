from enum import Enum

from pydantic import BaseModel


class ResourceCategory(str, Enum):
    image = "image"
    video = "video"


class BatchDeleteRequest(BaseModel):
    ids: list[int]


class BatchDeleteResponse(BaseModel):
    deleted: int
