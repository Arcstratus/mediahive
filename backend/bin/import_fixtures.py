import asyncio
import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database import Base, async_session, engine  # noqa: E402
from app.models import Resource  # noqa: E402

FIXTURES_PATH = BACKEND_DIR / "fixtures" / "resources.json"


async def main():
    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    data = json.loads(FIXTURES_PATH.read_text())
    print(f"Loading {len(data)} resources from {FIXTURES_PATH.name}")

    async with async_session() as session:
        for item in data:
            resource = Resource(
                type=item["type"],
                url=item.get("url"),
                title=item.get("title"),
            )
            session.add(resource)

        await session.commit()

    print(f"Imported {len(data)} resources.")
    await engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
