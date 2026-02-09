from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Bookmark, Resource, Tag
from app.schemas import StatsResponse

router = APIRouter(tags=["Stats"])


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    type_counts = await db.execute(
        select(Resource.category, func.count()).group_by(Resource.category)
    )
    counts = {row[0]: row[1] for row in type_counts.all()}

    bookmark_count = await db.scalar(select(func.count(Bookmark.id)))
    tag_count = await db.scalar(select(func.count(Tag.id)))

    return StatsResponse(
        images=counts.get("image", 0),
        videos=counts.get("video", 0),
        bookmarks=bookmark_count or 0,
        tags=tag_count or 0,
    )
