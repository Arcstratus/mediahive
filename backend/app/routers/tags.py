from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import TagCreate, TagResponse
from app.services import tag_service

router = APIRouter(tags=["Tags"])


@router.post("/tags", response_model=TagResponse, status_code=201)
async def create_tag(body: TagCreate, db: AsyncSession = Depends(get_db)):
    return await tag_service.create_tag(db, body.name)


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    return await tag_service.list_tags_with_counts(db)


@router.delete("/tags/{tag_id}", status_code=204)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    await tag_service.delete_tag(db, tag_id)
