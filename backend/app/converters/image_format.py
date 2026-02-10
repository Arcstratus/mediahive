from pathlib import Path

from PIL import Image, ImageOps


def to_webp(input_path: Path, output_path: Path, quality: int = 80) -> bool:
    """Convert an image to WebP format. Returns True on success."""
    try:
        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)
        img.save(output_path, format="WEBP", quality=quality, method=4)
        return True
    except Exception:
        return False


def to_jpg(input_path: Path, output_path: Path, quality: int = 85) -> bool:
    """Convert an image to JPEG format. Returns True on success."""
    try:
        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)

        if img.mode == "RGBA" or (img.mode == "P" and "transparency" in img.info):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.convert("RGBA").split()[3])
            img = background

        img.save(output_path, format="JPEG", quality=quality, optimize=True)
        return True
    except Exception:
        return False


def to_png(input_path: Path, output_path: Path) -> bool:
    """Convert an image to PNG format. Returns True on success."""
    try:
        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)
        img.save(output_path, format="PNG", optimize=True)
        return True
    except Exception:
        return False
