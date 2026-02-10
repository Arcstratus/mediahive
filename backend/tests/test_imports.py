import hashlib
from pathlib import Path
from unittest.mock import patch

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Resource


# ---------------------------------------------------------------------------
# POST /api/imports/scan
# ---------------------------------------------------------------------------


async def test_scan_folder_with_image_files(client: httpx.AsyncClient, tmp_path: Path):
    """Scan a folder containing image files returns them with correct type and size."""
    img1 = tmp_path / "photo.jpg"
    img1.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)  # 104 bytes

    img2 = tmp_path / "graphic.png"
    img2.write_bytes(b"\x89PNG" + b"\x00" * 50)  # 54 bytes

    resp = await client.post("/api/imports/scan", json={"path": str(tmp_path)})
    assert resp.status_code == 200

    data = resp.json()
    files = data["files"]
    assert len(files) == 2

    files_by_name = {f["name"]: f for f in files}

    assert files_by_name["photo.jpg"]["type"] == "image"
    assert files_by_name["photo.jpg"]["size"] == 104
    assert files_by_name["photo.jpg"]["path"] == str(img1)

    assert files_by_name["graphic.png"]["type"] == "image"
    assert files_by_name["graphic.png"]["size"] == 54
    assert files_by_name["graphic.png"]["path"] == str(img2)


async def test_scan_folder_with_video_files(client: httpx.AsyncClient, tmp_path: Path):
    """Scan a folder containing video files returns them with correct type."""
    vid = tmp_path / "clip.mp4"
    vid.write_bytes(b"\x00\x00\x00\x1c" + b"\x00" * 200)

    resp = await client.post("/api/imports/scan", json={"path": str(tmp_path)})
    assert resp.status_code == 200

    data = resp.json()
    assert len(data["files"]) == 1
    assert data["files"][0]["name"] == "clip.mp4"
    assert data["files"][0]["type"] == "video"


async def test_scan_folder_ignores_non_media_files(
    client: httpx.AsyncClient, tmp_path: Path
):
    """Scan a folder with mixed files ignores non-media files like .txt and .json."""
    (tmp_path / "readme.txt").write_text("hello")
    (tmp_path / "data.json").write_text("{}")
    (tmp_path / "script.py").write_text("print(1)")
    img = tmp_path / "photo.webp"
    img.write_bytes(b"RIFF" + b"\x00" * 20)

    resp = await client.post("/api/imports/scan", json={"path": str(tmp_path)})
    assert resp.status_code == 200

    data = resp.json()
    assert len(data["files"]) == 1
    assert data["files"][0]["name"] == "photo.webp"
    assert data["files"][0]["type"] == "image"


async def test_scan_nonexistent_path_returns_400(client: httpx.AsyncClient):
    """Scan a non-existent path returns 400."""
    resp = await client.post(
        "/api/imports/scan", json={"path": "/nonexistent/path/abc123"}
    )
    assert resp.status_code == 400
    assert "does not exist" in resp.json()["error"]


async def test_scan_excludes_excluded_directories(
    client: httpx.AsyncClient, tmp_path: Path
):
    """Scan excludes files inside node_modules, .git, and .venv directories."""
    # Create files in excluded directories
    for excluded in ("node_modules", ".git", ".venv"):
        excluded_dir = tmp_path / excluded
        excluded_dir.mkdir()
        (excluded_dir / "image.jpg").write_bytes(b"\xff" * 10)

    # Create a file in a normal subdirectory
    normal_dir = tmp_path / "photos"
    normal_dir.mkdir()
    (normal_dir / "valid.png").write_bytes(b"\x89" * 10)

    # Create a file at root level
    (tmp_path / "root.jpg").write_bytes(b"\xff" * 5)

    resp = await client.post("/api/imports/scan", json={"path": str(tmp_path)})
    assert resp.status_code == 200

    data = resp.json()
    names = {f["name"] for f in data["files"]}
    assert names == {"valid.png", "root.jpg"}


# ---------------------------------------------------------------------------
# POST /api/imports/execute
# ---------------------------------------------------------------------------


async def test_execute_import_creates_resources(
    client: httpx.AsyncClient, db: AsyncSession, tmp_path: Path
):
    """Import image files creates Resource records in DB and returns imported count."""
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    img1 = tmp_path / "a.jpg"
    img1.write_bytes(b"image-content-a")

    img2 = tmp_path / "b.png"
    img2.write_bytes(b"image-content-b")

    with patch("app.services.import_service.MEDIA_DIR", media_dir):
        resp = await client.post(
            "/api/imports/execute",
            json={
                "files": [
                    {"path": str(img1), "type": "image"},
                    {"path": str(img2), "type": "image"},
                ]
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["imported"] == 2
    assert data["skipped"] == 0

    # Verify DB records were created
    result = await db.execute(select(Resource))
    resources = result.scalars().all()
    assert len(resources) == 2

    filenames = {r.filename for r in resources}
    sha_a = hashlib.sha256(b"image-content-a").hexdigest()
    sha_b = hashlib.sha256(b"image-content-b").hexdigest()
    assert f"{sha_a}.jpg" in filenames
    assert f"{sha_b}.png" in filenames

    # Verify files were copied to media dir
    assert (media_dir / f"{sha_a}.jpg").exists()
    assert (media_dir / f"{sha_b}.png").exists()


async def test_execute_import_skips_existing_resources(
    client: httpx.AsyncClient, db: AsyncSession, tmp_path: Path
):
    """Import skips files that already exist in DB by hash filename."""
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    img = tmp_path / "photo.jpg"
    img.write_bytes(b"duplicate-content")

    sha = hashlib.sha256(b"duplicate-content").hexdigest()
    existing_filename = f"{sha}.jpg"

    # Pre-insert a resource with the same hash filename
    existing = Resource(
        category="image", title="old-photo.jpg", filename=existing_filename
    )
    db.add(existing)
    await db.commit()

    with patch("app.services.import_service.MEDIA_DIR", media_dir):
        resp = await client.post(
            "/api/imports/execute",
            json={"files": [{"path": str(img), "type": "image"}]},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["imported"] == 0
    assert data["skipped"] == 1

    # Verify no additional records were created
    result = await db.execute(select(Resource))
    resources = result.scalars().all()
    assert len(resources) == 1
    assert resources[0].title == "old-photo.jpg"


async def test_execute_import_skips_nonexistent_source_files(
    client: httpx.AsyncClient, db: AsyncSession, tmp_path: Path
):
    """Import skips files whose source paths do not exist."""
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    nonexistent = tmp_path / "does_not_exist.jpg"

    with patch("app.services.import_service.MEDIA_DIR", media_dir):
        resp = await client.post(
            "/api/imports/execute",
            json={"files": [{"path": str(nonexistent), "type": "image"}]},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["imported"] == 0
    assert data["skipped"] == 0

    # No records in DB
    result = await db.execute(select(Resource))
    resources = result.scalars().all()
    assert len(resources) == 0


async def test_execute_import_empty_file_list(
    client: httpx.AsyncClient, tmp_path: Path
):
    """Import with empty file list returns imported=0 and skipped=0."""
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    with patch("app.services.import_service.MEDIA_DIR", media_dir):
        resp = await client.post(
            "/api/imports/execute",
            json={"files": []},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["imported"] == 0
    assert data["skipped"] == 0
