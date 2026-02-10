from fastapi import Depends
from fastapi_error_map import ErrorAwareRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import TagAlreadyExistsError, TagNotFoundError
from app.schemas import TagCreate, TagResponse, TagUpdate
from app.services import tag_service

router = ErrorAwareRouter(tags=["Tags"])


@router.post("/tags", response_model=TagResponse, status_code=201, error_map={TagAlreadyExistsError: 409})
async def create_tag(body: TagCreate, db: AsyncSession = Depends(get_db)):
    return await tag_service.create_tag(db, body.name)


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    return await tag_service.list_tags_with_counts(db)


@router.patch(
    "/tags/{tag_id}",
    response_model=TagResponse,
    error_map={TagNotFoundError: 404, TagAlreadyExistsError: 409},
)
async def update_tag(tag_id: int, body: TagUpdate, db: AsyncSession = Depends(get_db)):
    return await tag_service.update_tag(db, tag_id, body.name)


@router.delete("/tags/{tag_id}", status_code=204, error_map={TagNotFoundError: 404})
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    await tag_service.delete_tag(db, tag_id)
