import hashlib
import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import IMAGE_EXTENSIONS, MEDIA_DIR, VIDEO_EXTENSIONS
from app.database import get_db
from app.models import Resource
from app.schemas import (
    ImportRequest,
    ImportResponse,
    ScanRequest,
    ScanResponse,
    ScannedFile,
)

router = APIRouter(prefix="/imports", tags=["Imports"])

ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
EXCLUDED_DIRS = {"node_modules", ".venv", ".git"}


def _classify(ext: str) -> str | None:
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return None


@router.post("/scan", response_model=ScanResponse)
async def scan_folder(body: ScanRequest):
    folder = Path(body.path)
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(
            status_code=400, detail="Path does not exist or is not a directory"
        )

    files: list[ScannedFile] = []
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for fname in filenames:
            ext = Path(fname).suffix.lower()
            file_type = _classify(ext)
            if file_type is None:
                continue
            full_path = Path(dirpath) / fname
            files.append(
                ScannedFile(
                    path=str(full_path),
                    name=fname,
                    type=file_type,
                    size=full_path.stat().st_size,
                )
            )

    return ScanResponse(files=files)


@router.post("/execute", response_model=ImportResponse)
async def execute_import(body: ImportRequest, db: AsyncSession = Depends(get_db)):
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    imported = 0
    skipped = 0

    for item in body.files:
        src = Path(item.path)
        if not src.is_file():
            continue

        sha256 = hashlib.sha256(src.read_bytes()).hexdigest()
        ext = src.suffix.lower()
        new_name = f"{sha256}{ext}"
        dest = MEDIA_DIR / new_name

        # Check if resource with same url (hash filename) already exists
        existing = await db.scalar(
            select(Resource).where(Resource.filename == new_name)
        )
        if existing:
            skipped += 1
            continue

        if not dest.exists():
            shutil.copy2(src, dest)

        resource = Resource(category=item.type.value, title=src.name, filename=new_name)
        db.add(resource)
        imported += 1

    await db.commit()
    return ImportResponse(imported=imported, skipped=skipped)
