from pydantic import BaseModel

from app.models import ResourceCategory


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
