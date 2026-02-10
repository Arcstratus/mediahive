from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import TrashedResourceNotFoundError
from app.models import Resource
from app.services.file_service import permanently_delete_from_trash, restore_from_trash


async def list_trash(db: AsyncSession) -> list[Resource]:
    result = await db.execute(
        select(Resource)
        .where(Resource.deleted_at.isnot(None))
        .order_by(Resource.deleted_at.desc())
    )
    return list(result.scalars().all())


async def restore_resource(db: AsyncSession, resource_id: int) -> Resource:
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is None:
        raise TrashedResourceNotFoundError("Trashed resource not found")

    if resource.filename:
        restore_from_trash(resource.filename, resource.folder)

    resource.deleted_at = None
    await db.commit()
    await db.refresh(resource)
    return resource


async def permanently_delete(db: AsyncSession, resource_id: int) -> None:
    resource = await db.get(Resource, resource_id)
    if not resource or resource.deleted_at is None:
        raise TrashedResourceNotFoundError("Trashed resource not found")

    if resource.filename:
        permanently_delete_from_trash(resource.filename)

    await db.delete(resource)
    await db.commit()


async def empty_trash(db: AsyncSession) -> None:
    result = await db.execute(select(Resource).where(Resource.deleted_at.isnot(None)))
    resources = result.scalars().all()

    for resource in resources:
        if resource.filename:
            permanently_delete_from_trash(resource.filename)
        await db.delete(resource)

    await db.commit()
