from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Resource, Tag
from app.schemas import StatsResponse

router = APIRouter(tags=["Stats"])


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    type_counts = await db.execute(
        select(Resource.type, func.count()).group_by(Resource.type)
    )
    counts = {row[0]: row[1] for row in type_counts.all()}

    tag_count = await db.scalar(select(func.count(Tag.id)))

    return StatsResponse(
        images=counts.get("image", 0),
        videos=counts.get("video", 0),
        urls=counts.get("url", 0),
        tags=tag_count or 0,
    )
