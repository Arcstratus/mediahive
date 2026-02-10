"""Tests for the bookmarks router."""

from datetime import datetime, timezone

import httpx

from app.models import Bookmark


# -- helpers --


async def create_bookmark(client: httpx.AsyncClient, **overrides) -> dict:
    payload = {"url": "https://example.com", **overrides}
    resp = await client.post("/api/bookmarks", json=payload)
    assert resp.status_code == 201
    return resp.json()


# -- POST /api/bookmarks --


async def test_create_bookmark_minimal(client):
    data = await create_bookmark(client)

    assert data["url"] == "https://example.com"
    assert data["title"] is None
    assert data["description"] is None
    assert data["folder"] is None
    assert data["tags"] == []
    assert data["id"] is not None
    assert "created_at" in data


async def test_create_bookmark_full(client):
    data = await create_bookmark(
        client,
        title="Example",
        url="https://example.com",
        description="A site",
        folder="dev",
        tags=["python", "web"],
    )

    assert data["title"] == "Example"
    assert data["description"] == "A site"
    assert data["folder"] == "dev"
    assert len(data["tags"]) == 2
    assert {t["name"] for t in data["tags"]} == {"python", "web"}


async def test_create_bookmark_auto_creates_tags(client):
    await create_bookmark(client, tags=["new-tag"])

    resp = await client.get("/api/tags")
    assert any(t["name"] == "new-tag" for t in resp.json())


# -- GET /api/bookmarks --


async def test_list_bookmarks_empty(client):
    resp = await client.get("/api/bookmarks")
    data = resp.json()

    assert resp.status_code == 200
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["per_page"] == 20


async def test_list_bookmarks_pagination(client):
    for i in range(5):
        await create_bookmark(client, url=f"https://example.com/{i}")

    resp = await client.get("/api/bookmarks", params={"per_page": 2, "page": 1})
    data = resp.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5

    resp = await client.get("/api/bookmarks", params={"per_page": 2, "page": 3})
    data = resp.json()
    assert len(data["items"]) == 1


async def test_list_bookmarks_search_by_title(client):
    await create_bookmark(client, title="FastAPI guide", url="https://a.com")
    await create_bookmark(client, title="Django guide", url="https://b.com")

    resp = await client.get("/api/bookmarks", params={"search": "fastapi"})
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["title"] == "FastAPI guide"


async def test_list_bookmarks_search_by_url(client):
    await create_bookmark(client, url="https://github.com/foo")
    await create_bookmark(client, url="https://gitlab.com/bar")

    resp = await client.get("/api/bookmarks", params={"search": "github"})
    assert len(resp.json()["items"]) == 1


async def test_list_bookmarks_search_by_description(client):
    await create_bookmark(client, url="https://a.com", description="async tutorial")
    await create_bookmark(client, url="https://b.com", description="sync basics")

    resp = await client.get("/api/bookmarks", params={"search": "async"})
    assert len(resp.json()["items"]) == 1


async def test_list_bookmarks_filter_by_tag(client):
    await create_bookmark(client, url="https://a.com", tags=["python"])
    await create_bookmark(client, url="https://b.com", tags=["rust"])

    resp = await client.get("/api/bookmarks", params={"tag": "python"})
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["url"] == "https://a.com"


async def test_list_bookmarks_filter_by_multiple_tags(client):
    await create_bookmark(client, url="https://a.com", tags=["python", "web"])
    await create_bookmark(client, url="https://b.com", tags=["python"])
    await create_bookmark(client, url="https://c.com", tags=["web"])

    resp = await client.get("/api/bookmarks", params={"tag": ["python", "web"]})
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["url"] == "https://a.com"


async def test_list_bookmarks_sort_by_title_asc(client):
    await create_bookmark(client, title="Zebra", url="https://a.com")
    await create_bookmark(client, title="Apple", url="https://b.com")

    resp = await client.get(
        "/api/bookmarks", params={"sort_by": "title", "sort_desc": False}
    )
    titles = [b["title"] for b in resp.json()["items"]]
    assert titles == ["Apple", "Zebra"]


async def test_list_bookmarks_sort_by_created_at_desc_by_default(client, db):
    old = Bookmark(
        url="https://first.com",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    new = Bookmark(
        url="https://second.com",
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    db.add_all([old, new])
    await db.commit()

    resp = await client.get("/api/bookmarks")
    urls = [b["url"] for b in resp.json()["items"]]
    assert urls == ["https://second.com", "https://first.com"]


# -- GET /api/bookmarks/{bookmark_id} --


async def test_get_bookmark(client):
    created = await create_bookmark(client, title="Test", url="https://t.com")

    resp = await client.get(f"/api/bookmarks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Test"


async def test_get_bookmark_not_found(client):
    resp = await client.get("/api/bookmarks/999")
    assert resp.status_code == 404


# -- PUT /api/bookmarks/{bookmark_id} --


async def test_update_bookmark_title(client):
    created = await create_bookmark(client, title="Old", url="https://a.com")

    resp = await client.put(f"/api/bookmarks/{created['id']}", json={"title": "New"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New"
    assert resp.json()["url"] == "https://a.com"


async def test_update_bookmark_tags(client):
    created = await create_bookmark(client, url="https://a.com", tags=["old"])

    resp = await client.put(
        f"/api/bookmarks/{created['id']}", json={"tags": ["new1", "new2"]}
    )
    tag_names = {t["name"] for t in resp.json()["tags"]}
    assert tag_names == {"new1", "new2"}


async def test_update_bookmark_partial(client):
    created = await create_bookmark(
        client, title="Keep", url="https://a.com", description="Keep too"
    )

    resp = await client.put(
        f"/api/bookmarks/{created['id']}", json={"url": "https://new.com"}
    )
    data = resp.json()
    assert data["url"] == "https://new.com"
    assert data["title"] == "Keep"
    assert data["description"] == "Keep too"


async def test_update_bookmark_not_found(client):
    resp = await client.put("/api/bookmarks/999", json={"title": "X"})
    assert resp.status_code == 404


# -- DELETE /api/bookmarks/{bookmark_id} --


async def test_delete_bookmark(client):
    created = await create_bookmark(client, url="https://a.com")

    resp = await client.delete(f"/api/bookmarks/{created['id']}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/bookmarks/{created['id']}")
    assert resp.status_code == 404


async def test_delete_bookmark_not_found(client):
    resp = await client.delete("/api/bookmarks/999")
    assert resp.status_code == 404


# -- POST /api/bookmarks/batch-delete --


async def test_batch_delete(client):
    b1 = await create_bookmark(client, url="https://a.com")
    b2 = await create_bookmark(client, url="https://b.com")
    b3 = await create_bookmark(client, url="https://c.com")

    resp = await client.post(
        "/api/bookmarks/batch-delete", json={"ids": [b1["id"], b3["id"]]}
    )
    assert resp.status_code == 200
    assert resp.json()["deleted"] == 2

    listing = await client.get("/api/bookmarks")
    assert listing.json()["total"] == 1
    assert listing.json()["items"][0]["id"] == b2["id"]


async def test_batch_delete_skips_nonexistent(client):
    b1 = await create_bookmark(client, url="https://a.com")

    resp = await client.post(
        "/api/bookmarks/batch-delete", json={"ids": [b1["id"], 999]}
    )
    assert resp.json()["deleted"] == 1


async def test_batch_delete_empty_list(client):
    resp = await client.post("/api/bookmarks/batch-delete", json={"ids": []})
    assert resp.json()["deleted"] == 0
