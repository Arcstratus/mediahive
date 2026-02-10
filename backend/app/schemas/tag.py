from datetime import datetime

from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    resource_count: int = 0

    model_config = {"from_attributes": True}
