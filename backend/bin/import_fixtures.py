import asyncio
import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))


from sqlalchemy import select  # noqa: E402

from app.database import Base, async_session, engine  # noqa: E402
from app.models import Bookmark, Tag, bookmark_tags  # noqa: E402

FIXTURES_PATH = BACKEND_DIR / "fixtures" / "resources.json"


async def main():
    # Recreate all tables (wipe existing data)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    data = json.loads(FIXTURES_PATH.read_text())
    print(f"Loading {len(data)} bookmarks from {FIXTURES_PATH.name}")

    async with async_session() as session:
        # Build a tag cache so each unique name is created once
        tag_cache: dict[str, Tag] = {}

        # First pass: create all tags
        all_tag_names = {name for item in data for name in item.get("tags", [])}
        for tag_name in sorted(all_tag_names):
            tag = Tag(name=tag_name)
            session.add(tag)
        await session.flush()

        # Build tag cache
        for tag_name in all_tag_names:
            result = await session.execute(select(Tag).where(Tag.name == tag_name))
            tag_cache[tag_name] = result.scalar_one()

        # Second pass: create bookmarks and link tags
        for item in data:
            bookmark = Bookmark(
                title=item["title"],
                url=item["url"],
                description=item.get("description"),
            )
            session.add(bookmark)
            await session.flush()

            for tag_name in item.get("tags", []):
                await session.execute(
                    bookmark_tags.insert().values(
                        bookmark_id=bookmark.id,
                        tag_id=tag_cache[tag_name].id,
                    )
                )

        await session.commit()

    print(f"Imported {len(data)} bookmarks.")
    await engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
