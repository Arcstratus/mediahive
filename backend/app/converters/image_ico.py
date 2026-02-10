from pathlib import Path

from PIL import Image, ImageOps


def to_ico(
    input_path: Path,
    output_path: Path,
    sizes: list[int] | None = None,
) -> bool:
    """
    Convert an image to ICO (favicon) format with multiple sizes.

    Args:
        input_path: Source image file.
        output_path: Destination .ico file.
        sizes: List of icon sizes in pixels (square).
               Defaults to [16, 32, 48, 256] which covers standard favicon needs.

    Returns True on success, False on failure.
    """
    if sizes is None:
        sizes = [16, 32, 48, 256]

    try:
        img = Image.open(input_path)
        img = ImageOps.exif_transpose(img)

        if img.mode != "RGBA":
            img = img.convert("RGBA")

        img.save(output_path, format="ICO", sizes=[(s, s) for s in sizes])
        return True
    except Exception:
        return False
