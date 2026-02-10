"""Tests for the resources router."""

from unittest.mock import AsyncMock, patch

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Resource, Tag


async def _create_resource(
    client: httpx.AsyncClient,
    category: str = "image",
    filename: str | None = None,
    title: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Helper to create a resource via the API and return the JSON response."""
    body: dict = {"category": category}
    if filename is not None:
        body["filename"] = filename
    if title is not None:
        body["title"] = title
    if tags is not None:
        body["tags"] = tags
    resp = await client.post("/api/resources", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# POST /api/resources
# ---------------------------------------------------------------------------


class TestCreateResource:
    async def test_create_with_minimal_fields(self, client: httpx.AsyncClient):
        data = await _create_resource(client, category="image")
        assert data["category"] == "image"
        assert data["filename"] is None
        assert data["title"] is None
        assert data["tags"] == []
        assert "id" in data
        assert "created_at" in data

    async def test_create_with_all_fields(self, client: httpx.AsyncClient):
        data = await _create_resource(
            client,
            category="video",
            filename="test.mp4",
            title="My Video",
            tags=["nature", "travel"],
        )
        assert data["category"] == "video"
        assert data["filename"] == "test.mp4"
        assert data["title"] == "My Video"
        assert len(data["tags"]) == 2
        tag_names = {t["name"] for t in data["tags"]}
        assert tag_names == {"nature", "travel"}

    async def test_auto_creates_tags(self, client: httpx.AsyncClient, db: AsyncSession):
        data = await _create_resource(
            client, category="image", tags=["new-tag-1", "new-tag-2"]
        )
        tag_names = {t["name"] for t in data["tags"]}
        assert tag_names == {"new-tag-1", "new-tag-2"}

        # Verify tags exist in the database
        from sqlalchemy import select

        result = await db.execute(
            select(Tag).where(Tag.name.in_(["new-tag-1", "new-tag-2"]))
        )
        tags = result.scalars().all()
        assert len(tags) == 2


# ---------------------------------------------------------------------------
# GET /api/resources
# ---------------------------------------------------------------------------


class TestListResources:
    async def test_empty_list(self, client: httpx.AsyncClient):
        resp = await client.get("/api/resources")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["per_page"] == 20

    async def test_pagination(self, client: httpx.AsyncClient):
        # Create 5 resources with unique filenames
        for i in range(5):
            await _create_resource(client, filename=f"file{i}.jpg", title=f"Res {i}")

        # Request page 1 with per_page=2
        resp = await client.get("/api/resources", params={"per_page": 2, "page": 1})
        data = resp.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["per_page"] == 2

        # Request page 3 with per_page=2 (should have 1 item)
        resp = await client.get("/api/resources", params={"per_page": 2, "page": 3})
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["total"] == 5

    async def test_filter_by_category(self, client: httpx.AsyncClient):
        await _create_resource(client, category="image", filename="a.jpg", title="img")
        await _create_resource(client, category="video", filename="b.mp4", title="vid")

        resp = await client.get("/api/resources", params={"category": "image"})
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["category"] == "image"

    async def test_search_by_title(self, client: httpx.AsyncClient):
        await _create_resource(client, title="sunset photo", filename="a.jpg")
        await _create_resource(client, title="city lights", filename="b.jpg")

        resp = await client.get("/api/resources", params={"search": "sunset"})
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "sunset photo"

    async def test_search_by_filename(self, client: httpx.AsyncClient):
        await _create_resource(client, filename="beach_sunset.jpg", title="A")
        await _create_resource(client, filename="mountain.png", title="B")

        resp = await client.get("/api/resources", params={"search": "beach"})
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["filename"] == "beach_sunset.jpg"

    async def test_filter_by_extension(self, client: httpx.AsyncClient):
        await _create_resource(client, filename="photo.jpg", title="A")
        await _create_resource(client, filename="image.png", title="B")
        await _create_resource(client, filename="clip.mp4", category="video", title="C")

        resp = await client.get("/api/resources", params={"ext": [".jpg", ".png"]})
        data = resp.json()
        assert data["total"] == 2
        filenames = {item["filename"] for item in data["items"]}
        assert filenames == {"photo.jpg", "image.png"}

    async def test_filter_by_tag(self, client: httpx.AsyncClient):
        await _create_resource(client, filename="a.jpg", tags=["nature"])
        await _create_resource(client, filename="b.jpg", tags=["urban"])

        resp = await client.get("/api/resources", params={"tag": ["nature"]})
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["filename"] == "a.jpg"

    async def test_filter_by_multiple_tags_intersection(
        self, client: httpx.AsyncClient
    ):
        await _create_resource(client, filename="a.jpg", tags=["nature", "sunset"])
        await _create_resource(client, filename="b.jpg", tags=["nature"])
        await _create_resource(client, filename="c.jpg", tags=["sunset"])

        # Both tags required (intersection)
        resp = await client.get("/api/resources", params={"tag": ["nature", "sunset"]})
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["filename"] == "a.jpg"

    async def test_filter_by_folder(self, client: httpx.AsyncClient, db: AsyncSession):
        # Create resources and set folder directly in DB
        r1 = await _create_resource(client, filename="a.jpg", title="A")
        r2 = await _create_resource(client, filename="b.jpg", title="B")

        # Set folder via update endpoint
        await client.put(f"/api/resources/{r1['id']}", json={"folder": "vacation"})
        await client.put(f"/api/resources/{r2['id']}", json={"folder": "work"})

        resp = await client.get("/api/resources", params={"folder": "vacation"})
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "A"

    async def test_excludes_soft_deleted(
        self, client: httpx.AsyncClient, db: AsyncSession
    ):
        await _create_resource(client, filename="keep.jpg", title="Keep")
        r2 = await _create_resource(client, filename="del.jpg", title="Delete")

        # Soft-delete r2
        await client.delete(f"/api/resources/{r2['id']}")

        resp = await client.get("/api/resources")
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Keep"

    async def test_sort_by_title_ascending(self, client: httpx.AsyncClient):
        await _create_resource(client, filename="c.jpg", title="Charlie")
        await _create_resource(client, filename="a.jpg", title="Alpha")
        await _create_resource(client, filename="b.jpg", title="Bravo")

        resp = await client.get(
            "/api/resources", params={"sort_by": "title", "sort_desc": False}
        )
        data = resp.json()
        titles = [item["title"] for item in data["items"]]
        assert titles == ["Alpha", "Bravo", "Charlie"]


# ---------------------------------------------------------------------------
# GET /api/resources/ids
# ---------------------------------------------------------------------------


class TestListResourceIds:
    async def test_returns_list_of_ids(self, client: httpx.AsyncClient):
        r1 = await _create_resource(client, filename="a.jpg")
        r2 = await _create_resource(client, filename="b.jpg")

        resp = await client.get("/api/resources/ids")
        assert resp.status_code == 200
        ids = resp.json()
        assert isinstance(ids, list)
        assert set(ids) == {r1["id"], r2["id"]}

    async def test_respects_category_filter(self, client: httpx.AsyncClient):
        r_img = await _create_resource(client, category="image", filename="a.jpg")
        await _create_resource(client, category="video", filename="b.mp4")

        resp = await client.get("/api/resources/ids", params={"category": "image"})
        ids = resp.json()
        assert ids == [r_img["id"]]

    async def test_excludes_soft_deleted(self, client: httpx.AsyncClient):
        r1 = await _create_resource(client, filename="keep.jpg")
        r2 = await _create_resource(client, filename="del.jpg")

        await client.delete(f"/api/resources/{r2['id']}")

        resp = await client.get("/api/resources/ids")
        ids = resp.json()
        assert ids == [r1["id"]]


# ---------------------------------------------------------------------------
# GET /api/resources/folders
# ---------------------------------------------------------------------------


class TestListResourceFolders:
    async def test_returns_folder_names_with_counts(self, client: httpx.AsyncClient):
        r1 = await _create_resource(client, filename="a.jpg")
        r2 = await _create_resource(client, filename="b.jpg")
        r3 = await _create_resource(client, filename="c.jpg")

        await client.put(f"/api/resources/{r1['id']}", json={"folder": "photos"})
        await client.put(f"/api/resources/{r2['id']}", json={"folder": "photos"})
        await client.put(f"/api/resources/{r3['id']}", json={"folder": "docs"})

        resp = await client.get("/api/resources/folders")
        assert resp.status_code == 200
        folders = resp.json()
        folder_map = {f["folder"]: f["count"] for f in folders}
        assert folder_map == {"docs": 1, "photos": 2}

    async def test_excludes_resources_without_folder(self, client: httpx.AsyncClient):
        r1 = await _create_resource(client, filename="a.jpg")
        await _create_resource(client, filename="b.jpg")  # no folder

        await client.put(f"/api/resources/{r1['id']}", json={"folder": "myfolder"})

        resp = await client.get("/api/resources/folders")
        folders = resp.json()
        assert len(folders) == 1
        assert folders[0]["folder"] == "myfolder"

    async def test_excludes_soft_deleted(self, client: httpx.AsyncClient):
        r1 = await _create_resource(client, filename="a.jpg")
        r2 = await _create_resource(client, filename="b.jpg")

        await client.put(f"/api/resources/{r1['id']}", json={"folder": "alive"})
        await client.put(f"/api/resources/{r2['id']}", json={"folder": "dead"})

        await client.delete(f"/api/resources/{r2['id']}")

        resp = await client.get("/api/resources/folders")
        folders = resp.json()
        assert len(folders) == 1
        assert folders[0]["folder"] == "alive"


# ---------------------------------------------------------------------------
# GET /api/resources/{resource_id}
# ---------------------------------------------------------------------------


class TestGetResource:
    async def test_returns_resource(self, client: httpx.AsyncClient):
        created = await _create_resource(client, filename="test.jpg", title="Test")

        resp = await client.get(f"/api/resources/{created['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == created["id"]
        assert data["filename"] == "test.jpg"
        assert data["title"] == "Test"

    async def test_returns_404_for_nonexistent(self, client: httpx.AsyncClient):
        resp = await client.get("/api/resources/99999")
        assert resp.status_code == 404

    async def test_returns_404_for_soft_deleted(self, client: httpx.AsyncClient):
        created = await _create_resource(client, filename="del.jpg")
        await client.delete(f"/api/resources/{created['id']}")

        resp = await client.get(f"/api/resources/{created['id']}")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PUT /api/resources/{resource_id}
# ---------------------------------------------------------------------------


class TestUpdateResource:
    async def test_update_title(self, client: httpx.AsyncClient):
        created = await _create_resource(client, filename="a.jpg", title="Old")

        resp = await client.put(
            f"/api/resources/{created['id']}", json={"title": "New Title"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "New Title"

    async def test_update_tags(self, client: httpx.AsyncClient):
        created = await _create_resource(client, filename="a.jpg", tags=["old"])

        resp = await client.put(
            f"/api/resources/{created['id']}", json={"tags": ["new1", "new2"]}
        )
        assert resp.status_code == 200
        data = resp.json()
        tag_names = {t["name"] for t in data["tags"]}
        assert tag_names == {"new1", "new2"}

    async def test_partial_update_preserves_fields(self, client: httpx.AsyncClient):
        created = await _create_resource(
            client, filename="a.jpg", title="Original", tags=["tag1"]
        )

        # Update only title, tags should remain
        resp = await client.put(
            f"/api/resources/{created['id']}", json={"title": "Updated"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated"
        assert data["filename"] == "a.jpg"
        # tags should be preserved since we didn't send them
        tag_names = {t["name"] for t in data["tags"]}
        assert tag_names == {"tag1"}

    async def test_returns_404_for_nonexistent(self, client: httpx.AsyncClient):
        resp = await client.put("/api/resources/99999", json={"title": "X"})
        assert resp.status_code == 404

    async def test_rejects_folder_with_dotdot(self, client: httpx.AsyncClient):
        created = await _create_resource(client, filename="a.jpg")

        resp = await client.put(
            f"/api/resources/{created['id']}", json={"folder": "../escape"}
        )
        assert resp.status_code == 400
        assert "Invalid folder path" in resp.json()["error"]


# ---------------------------------------------------------------------------
# DELETE /api/resources/{resource_id}
# ---------------------------------------------------------------------------


class TestDeleteResource:
    async def test_soft_deletes(self, client: httpx.AsyncClient, db: AsyncSession):
        created = await _create_resource(client, filename="a.jpg")

        resp = await client.delete(f"/api/resources/{created['id']}")
        assert resp.status_code == 204

        # Confirm deleted_at is set in DB
        resource = await db.get(Resource, created["id"])
        assert resource is not None
        assert resource.deleted_at is not None

    async def test_returns_404_for_nonexistent(self, client: httpx.AsyncClient):
        resp = await client.delete("/api/resources/99999")
        assert resp.status_code == 404

    async def test_returns_404_for_already_soft_deleted(
        self, client: httpx.AsyncClient
    ):
        created = await _create_resource(client, filename="a.jpg")

        resp1 = await client.delete(f"/api/resources/{created['id']}")
        assert resp1.status_code == 204

        resp2 = await client.delete(f"/api/resources/{created['id']}")
        assert resp2.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/resources/batch-delete
# ---------------------------------------------------------------------------


class TestBatchDelete:
    async def test_soft_deletes_multiple(
        self, client: httpx.AsyncClient, db: AsyncSession
    ):
        r1 = await _create_resource(client, filename="a.jpg")
        r2 = await _create_resource(client, filename="b.jpg")
        r3 = await _create_resource(client, filename="c.jpg")

        resp = await client.post(
            "/api/resources/batch-delete",
            json={"ids": [r1["id"], r2["id"]]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["deleted"] == 2

        # r3 should still be accessible
        resp_get = await client.get(f"/api/resources/{r3['id']}")
        assert resp_get.status_code == 200

        # r1 and r2 should be soft-deleted
        for rid in [r1["id"], r2["id"]]:
            resp_get = await client.get(f"/api/resources/{rid}")
            assert resp_get.status_code == 404

    async def test_skips_nonexistent_and_already_deleted(
        self, client: httpx.AsyncClient
    ):
        r1 = await _create_resource(client, filename="a.jpg")

        # Soft-delete r1 first
        await client.delete(f"/api/resources/{r1['id']}")

        resp = await client.post(
            "/api/resources/batch-delete",
            json={"ids": [r1["id"], 99999]},
        )
        data = resp.json()
        assert data["deleted"] == 0

    async def test_empty_list_returns_zero(self, client: httpx.AsyncClient):
        resp = await client.post("/api/resources/batch-delete", json={"ids": []})
        assert resp.status_code == 200
        data = resp.json()
        assert data["deleted"] == 0


# ---------------------------------------------------------------------------
# POST /api/resources/download
# ---------------------------------------------------------------------------


class TestDownloadResource:
    @patch("app.services.resource_service.bg_download", new_callable=AsyncMock)
    async def test_returns_202_for_valid_image_url(
        self, mock_bg: AsyncMock, client: httpx.AsyncClient
    ):
        resp = await client.post(
            "/api/resources/download",
            json={"url": "https://example.com/photo.jpg"},
        )
        assert resp.status_code == 202
        assert resp.json()["status"] == "downloading"
        mock_bg.assert_awaited_once_with("https://example.com/photo.jpg", ".jpg")

    async def test_returns_400_for_unsupported_extension(
        self, client: httpx.AsyncClient
    ):
        resp = await client.post(
            "/api/resources/download",
            json={"url": "https://example.com/file.txt"},
        )
        assert resp.status_code == 400
        assert "Unsupported URL extension" in resp.json()["error"]
