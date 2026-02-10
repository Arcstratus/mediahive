from pathlib import Path

MEDIA_DIR = Path(__file__).resolve().parent.parent.parent / "media"
TRASH_DIR = MEDIA_DIR / ".trash"
THUMBNAIL_DIR = MEDIA_DIR / ".thumbnails"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"}
VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".ts",
}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | {".m3u8"}
