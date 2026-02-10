"""Tests for the trash router."""

from datetime import UTC, datetime, timedelta

import httpx

from app.models import Resource


# -- helpers --


def make_trashed_resource(
    *,
    category: str = "image",
    filename: str | None = None,
    title: str | None = None,
    folder: str | None = None,
    deleted_at: datetime | None = None,
) -> Resource:
    """Create a Resource instance with deleted_at set (i.e. in trash)."""
    return Resource(
        category=category,
        filename=filename,
        title=title,
        folder=folder,
        deleted_at=deleted_at or datetime.now(UTC),
    )


def make_active_resource(
    *,
    category: str = "image",
    filename: str | None = None,
    title: str | None = None,
    folder: str | None = None,
) -> Resource:
    """Create a Resource instance that is active (not trashed)."""
    return Resource(
        category=category,
        filename=filename,
        title=title,
        folder=folder,
    )


# -- GET /api/trash --


async def test_list_trash_empty(client: httpx.AsyncClient):
    resp = await client.get("/api/trash")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_list_trash_returns_only_soft_deleted_resources(client, db):
    trashed = make_trashed_resource(filename="trashed.png", title="Trashed")
    active = make_active_resource(filename="active.png", title="Active")
    db.add_all([trashed, active])
    await db.commit()

    resp = await client.get("/api/trash")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["title"] == "Trashed"
    assert items[0]["deleted_at"] is not None


async def test_list_trash_does_not_include_active_resources(client, db):
    active1 = make_active_resource(filename="a.png", title="A")
    active2 = make_active_resource(filename="b.png", title="B")
    db.add_all([active1, active2])
    await db.commit()

    resp = await client.get("/api/trash")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_list_trash_ordered_by_deleted_at_descending(client, db):
    now = datetime.now(UTC)
    older = make_trashed_resource(
        filename="older.png",
        title="Older",
        deleted_at=now - timedelta(hours=2),
    )
    newer = make_trashed_resource(
        filename="newer.png",
        title="Newer",
        deleted_at=now - timedelta(hours=1),
    )
    newest = make_trashed_resource(
        filename="newest.png",
        title="Newest",
        deleted_at=now,
    )
    # Add in non-sorted order to verify the endpoint sorts them
    db.add_all([older, newer, newest])
    await db.commit()

    resp = await client.get("/api/trash")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 3
    titles = [item["title"] for item in items]
    assert titles == ["Newest", "Newer", "Older"]


# -- POST /api/trash/{resource_id}/restore --


async def test_restore_trashed_resource(client, db):
    resource = make_trashed_resource(filename="restore_me.png", title="Restore Me")
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    resource_id = resource.id

    resp = await client.post(f"/api/trash/{resource_id}/restore")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == resource_id
    assert data["deleted_at"] is None
    assert data["title"] == "Restore Me"

    # Verify it no longer appears in trash
    resp = await client.get("/api/trash")
    assert resp.json() == []


async def test_restore_nonexistent_resource_returns_404(client):
    resp = await client.post("/api/trash/99999/restore")
    assert resp.status_code == 404
    assert resp.json()["error"] == "Trashed resource not found"


async def test_restore_active_resource_returns_404(client, db):
    resource = make_active_resource(filename="active.png", title="Active")
    db.add(resource)
    await db.commit()
    await db.refresh(resource)

    resp = await client.post(f"/api/trash/{resource.id}/restore")
    assert resp.status_code == 404
    assert resp.json()["error"] == "Trashed resource not found"


# -- DELETE /api/trash/{resource_id} --


async def test_permanently_delete_trashed_resource(client, db):
    resource = make_trashed_resource(filename="delete_me.png", title="Delete Me")
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    resource_id = resource.id

    resp = await client.delete(f"/api/trash/{resource_id}")
    assert resp.status_code == 204

    # Verify it is gone from both trash and the database
    resp = await client.get("/api/trash")
    assert resp.json() == []


async def test_permanently_delete_nonexistent_resource_returns_404(client):
    resp = await client.delete("/api/trash/99999")
    assert resp.status_code == 404
    assert resp.json()["error"] == "Trashed resource not found"


async def test_permanently_delete_active_resource_returns_404(client, db):
    resource = make_active_resource(filename="active.png", title="Active")
    db.add(resource)
    await db.commit()
    await db.refresh(resource)

    resp = await client.delete(f"/api/trash/{resource.id}")
    assert resp.status_code == 404
    assert resp.json()["error"] == "Trashed resource not found"


# -- DELETE /api/trash (empty trash) --


async def test_empty_trash_deletes_all_trashed_resources(client, db):
    trashed1 = make_trashed_resource(filename="t1.png", title="T1")
    trashed2 = make_trashed_resource(filename="t2.png", title="T2")
    db.add_all([trashed1, trashed2])
    await db.commit()

    resp = await client.delete("/api/trash")
    assert resp.status_code == 204

    # Verify trash is now empty
    resp = await client.get("/api/trash")
    assert resp.json() == []


async def test_empty_trash_does_nothing_when_trash_is_empty(client):
    resp = await client.delete("/api/trash")
    assert resp.status_code == 204

    resp = await client.get("/api/trash")
    assert resp.json() == []


async def test_empty_trash_does_not_affect_active_resources(client, db):
    trashed = make_trashed_resource(filename="trashed.png", title="Trashed")
    active = make_active_resource(filename="active.png", title="Active")
    db.add_all([trashed, active])
    await db.commit()
    await db.refresh(active)
    active_id = active.id

    resp = await client.delete("/api/trash")
    assert resp.status_code == 204

    # Trash is empty
    resp = await client.get("/api/trash")
    assert resp.json() == []

    # Active resource still exists (check via resources endpoint or DB)
    await db.refresh(active)
    assert active.id == active_id
    assert active.deleted_at is None
