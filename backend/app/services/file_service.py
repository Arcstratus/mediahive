import asyncio
import hashlib
import shutil
from pathlib import Path

from app.config import (
    IMAGE_EXTENSIONS,
    MEDIA_DIR,
    THUMBNAIL_DIR,
    TRASH_DIR,
    VIDEO_EXTENSIONS,
)


def sha256_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def classify_extension(ext: str) -> str | None:
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return None


async def generate_thumbnail(video_path: Path, sha_prefix: str) -> str | None:
    """Extract a frame at 1s from a video and save as a JPEG thumbnail."""
    thumb_filename = f"{sha_prefix}_thumb.jpg"
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    thumb_path = THUMBNAIL_DIR / thumb_filename
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-ss",
            "1",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(thumb_path),
            "-y",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if proc.returncode == 0 and thumb_path.is_file():
            return thumb_filename
    except Exception:
        pass
    return None


def delete_thumbnail(thumb_filename: str | None) -> None:
    if not thumb_filename:
        return
    thumb_path = THUMBNAIL_DIR / thumb_filename
    if thumb_path.is_file():
        thumb_path.unlink()


def move_to_trash(filename: str, folder: str | None) -> None:
    src = MEDIA_DIR / (folder or "") / filename
    if src.is_file():
        TRASH_DIR.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(TRASH_DIR / filename))


def restore_from_trash(filename: str, folder: str | None) -> None:
    src = TRASH_DIR / filename
    dest = MEDIA_DIR / (folder or "") / filename
    if src.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))


def move_file(filename: str, old_folder: str | None, new_folder: str | None) -> None:
    old_path = MEDIA_DIR / (old_folder or "") / filename
    new_path = MEDIA_DIR / (new_folder or "") / filename
    if old_path.is_file():
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old_path), str(new_path))


def permanently_delete_from_trash(filename: str) -> None:
    trash_file = TRASH_DIR / filename
    if trash_file.is_file():
        trash_file.unlink()
