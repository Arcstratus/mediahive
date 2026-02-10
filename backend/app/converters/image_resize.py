from pathlib import Path

from PIL import Image, ImageOps


def resize_image(
    input_path: Path,
    output_path: Path,
    *,
    width: int | None = None,
    height: int | None = None,
    scale: float | None = None,
) -> bool:
    """
    Resize an image file.

    Exactly one sizing strategy must be provided:
    - width + height: resize to exact dimensions (maintains aspect ratio, fits within box)
    - width only: resize to width, auto-calculate height maintaining aspect ratio
    - height only: resize to height, auto-calculate width maintaining aspect ratio
    - scale: resize by scale factor (e.g. 0.5 = half size)

    Uses LANCZOS resampling for quality.
    Output format is inferred from output_path extension.
    Returns True on success, False on failure.
    """
    try:
        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)

        orig_w, orig_h = img.size

        if scale is not None:
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        elif width is not None and height is not None:
            img.thumbnail((width, height), Image.Resampling.LANCZOS)
        elif width is not None:
            new_h = int(orig_h * width / orig_w)
            img = img.resize((width, new_h), Image.Resampling.LANCZOS)
        elif height is not None:
            new_w = int(orig_w * height / orig_h)
            img = img.resize((new_w, height), Image.Resampling.LANCZOS)
        else:
            return False

        # Convert RGBA to RGB for formats that don't support alpha (e.g. JPEG)
        if img.mode == "RGBA" and output_path.suffix.lower() in (".jpg", ".jpeg"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        save_kwargs: dict = {}
        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            save_kwargs["quality"] = 85
        elif ext == ".webp":
            save_kwargs["quality"] = 85
        elif ext == ".png":
            save_kwargs["optimize"] = True

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, **save_kwargs)
        return True
    except Exception:
        return False
