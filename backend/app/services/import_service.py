import os
import shutil
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import MEDIA_DIR
from app.exceptions import ImportPathError
from app.models import Resource
from app.schemas import ImportFileItem, ScannedFile
from app.services.file_service import classify_extension, sha256_hash

EXCLUDED_DIRS = {"node_modules", ".venv", ".git"}


def scan_folder(path: str) -> list[ScannedFile]:
    folder = Path(path)
    if not folder.exists() or not folder.is_dir():
        raise ImportPathError("Path does not exist or is not a directory")

    files: list[ScannedFile] = []
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for fname in filenames:
            ext = Path(fname).suffix.lower()
            file_type = classify_extension(ext)
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

    return files


async def execute_import(
    db: AsyncSession, files: list[ImportFileItem]
) -> tuple[int, int]:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    imported = 0
    skipped = 0

    for item in files:
        src = Path(item.path)
        if not src.is_file():
            continue

        sha256 = sha256_hash(src.read_bytes())
        ext = src.suffix.lower()
        new_name = f"{sha256}{ext}"
        dest = MEDIA_DIR / new_name

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
    return imported, skipped
