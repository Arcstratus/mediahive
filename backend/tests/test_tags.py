"""Tests for the tags router."""

import httpx

from app.models import Bookmark, Resource, Tag


# -- helpers --


async def create_tag(client: httpx.AsyncClient, name: str) -> dict:
    resp = await client.post("/api/tags", json={"name": name})
    assert resp.status_code == 201
    return resp.json()


# -- POST /api/tags --


async def test_create_tag(client):
    data = await create_tag(client, "landscape")

    assert data["name"] == "landscape"
    assert data["id"] is not None
    assert "created_at" in data


async def test_create_tag_duplicate_returns_409(client):
    await create_tag(client, "nature")

    resp = await client.post("/api/tags", json={"name": "nature"})
    assert resp.status_code == 409


# -- GET /api/tags --


async def test_list_tags_empty(client):
    resp = await client.get("/api/tags")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_list_tags_ordered_by_name(client):
    await create_tag(client, "zebra")
    await create_tag(client, "apple")
    await create_tag(client, "mango")

    resp = await client.get("/api/tags")
    names = [t["name"] for t in resp.json()]
    assert names == ["apple", "mango", "zebra"]


async def test_list_tags_resource_count_zero_by_default(client):
    await create_tag(client, "unused")

    resp = await client.get("/api/tags")
    assert resp.json()[0]["resource_count"] == 0


async def test_list_tags_resource_count_includes_resources(client, db):
    tag = Tag(name="art")
    resource = Resource(category="image", filename="a.png", title="A")
    resource.tags.append(tag)
    db.add(resource)
    await db.commit()

    resp = await client.get("/api/tags")
    assert resp.json()[0]["resource_count"] == 1


async def test_list_tags_resource_count_includes_bookmarks(client, db):
    tag = Tag(name="ref")
    bookmark = Bookmark(title="B", url="https://example.com")
    bookmark.tags.append(tag)
    db.add(bookmark)
    await db.commit()

    resp = await client.get("/api/tags")
    assert resp.json()[0]["resource_count"] == 1


async def test_list_tags_resource_count_sums_resources_and_bookmarks(client, db):
    tag = Tag(name="mixed")
    resource = Resource(category="image", filename="b.png", title="B")
    resource.tags.append(tag)
    bookmark = Bookmark(title="C", url="https://example.com")
    bookmark.tags.append(tag)
    db.add_all([resource, bookmark])
    await db.commit()

    resp = await client.get("/api/tags")
    assert resp.json()[0]["resource_count"] == 2


# -- PATCH /api/tags/{tag_id} --


async def test_update_tag(client):
    tag = await create_tag(client, "old-name")

    resp = await client.patch(f"/api/tags/{tag['id']}", json={"name": "new-name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "new-name"
    assert resp.json()["id"] == tag["id"]


async def test_update_tag_not_found_returns_404(client):
    resp = await client.patch("/api/tags/999", json={"name": "x"})
    assert resp.status_code == 404


async def test_update_tag_duplicate_name_returns_409(client):
    await create_tag(client, "alpha")
    tag_b = await create_tag(client, "beta")

    resp = await client.patch(f"/api/tags/{tag_b['id']}", json={"name": "alpha"})
    assert resp.status_code == 409


# -- DELETE /api/tags/{tag_id} --


async def test_delete_tag(client):
    tag = await create_tag(client, "temp")

    resp = await client.delete(f"/api/tags/{tag['id']}")
    assert resp.status_code == 204

    resp = await client.get("/api/tags")
    assert resp.json() == []


async def test_delete_tag_not_found_returns_404(client):
    resp = await client.delete("/api/tags/999")
    assert resp.status_code == 404
