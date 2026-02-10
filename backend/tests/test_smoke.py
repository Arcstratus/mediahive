"""Smoke test to verify the test infrastructure works."""

from app.models import Tag


async def test_db_read_write(db):
    """Verify we can write to and read from the test database."""
    tag = Tag(name="test-tag")
    db.add(tag)
    await db.commit()
    await db.refresh(tag)

    assert tag.id is not None
    assert tag.name == "test-tag"


async def test_health_endpoint(client):
    """Verify the async test client can reach the API."""
    resp = await client.get("/api/health")
    assert resp.status_code == 200
