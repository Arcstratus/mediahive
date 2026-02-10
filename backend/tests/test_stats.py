import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Bookmark, Resource, Tag


async def test_empty_database_returns_all_zeros(client: httpx.AsyncClient):
    """GET /stats on an empty database should return zeros for all fields."""
    resp = await client.get("/api/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data == {"images": 0, "videos": 0, "bookmarks": 0, "tags": 0}


async def test_counts_images_correctly(db: AsyncSession, client: httpx.AsyncClient):
    """GET /stats should count resources with category='image'."""
    db.add_all(
        [
            Resource(category="image", filename="a.png"),
            Resource(category="image", filename="b.jpg"),
            Resource(category="image", filename="c.webp"),
        ]
    )
    await db.commit()

    resp = await client.get("/api/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data["images"] == 3
    assert data["videos"] == 0


async def test_counts_videos_correctly(db: AsyncSession, client: httpx.AsyncClient):
    """GET /stats should count resources with category='video'."""
    db.add_all(
        [
            Resource(category="video", filename="a.mp4"),
            Resource(category="video", filename="b.mkv"),
        ]
    )
    await db.commit()

    resp = await client.get("/api/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data["videos"] == 2
    assert data["images"] == 0


async def test_counts_bookmarks_correctly(db: AsyncSession, client: httpx.AsyncClient):
    """GET /stats should count all bookmarks."""
    db.add_all(
        [
            Bookmark(url="https://example.com/1"),
            Bookmark(url="https://example.com/2"),
            Bookmark(url="https://example.com/3"),
            Bookmark(url="https://example.com/4"),
        ]
    )
    await db.commit()

    resp = await client.get("/api/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data["bookmarks"] == 4


async def test_counts_tags_correctly(db: AsyncSession, client: httpx.AsyncClient):
    """GET /stats should count all tags."""
    db.add_all(
        [
            Tag(name="nature"),
            Tag(name="travel"),
        ]
    )
    await db.commit()

    resp = await client.get("/api/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data["tags"] == 2


async def test_mixed_data_returns_correct_counts(
    db: AsyncSession, client: httpx.AsyncClient
):
    """GET /stats with mixed data should return accurate counts for every field."""
    db.add_all(
        [
            # 2 images
            Resource(category="image", filename="photo1.png"),
            Resource(category="image", filename="photo2.jpg"),
            # 3 videos
            Resource(category="video", filename="clip1.mp4"),
            Resource(category="video", filename="clip2.mkv"),
            Resource(category="video", filename="clip3.webm"),
            # 4 bookmarks
            Bookmark(url="https://example.com/1"),
            Bookmark(url="https://example.com/2"),
            Bookmark(url="https://example.com/3"),
            Bookmark(url="https://example.com/4"),
            # 5 tags
            Tag(name="nature"),
            Tag(name="travel"),
            Tag(name="food"),
            Tag(name="tech"),
            Tag(name="music"),
        ]
    )
    await db.commit()

    resp = await client.get("/api/stats")

    assert resp.status_code == 200
    data = resp.json()
    assert data["images"] == 2
    assert data["videos"] == 3
    assert data["bookmarks"] == 4
    assert data["tags"] == 5
