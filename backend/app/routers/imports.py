from fastapi import Depends
from fastapi_error_map import ErrorAwareRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import ImportPathError
from app.schemas import ImportRequest, ImportResponse, ScanRequest, ScanResponse
from app.services import import_service

router = ErrorAwareRouter(prefix="/imports", tags=["Imports"])


@router.post("/scan", response_model=ScanResponse, error_map={ImportPathError: 400})
async def scan_folder(body: ScanRequest):
    files = import_service.scan_folder(body.path)
    return ScanResponse(files=files)


@router.post("/execute", response_model=ImportResponse)
async def execute_import(body: ImportRequest, db: AsyncSession = Depends(get_db)):
    imported, skipped = await import_service.execute_import(db, body.files)
    return ImportResponse(imported=imported, skipped=skipped)
