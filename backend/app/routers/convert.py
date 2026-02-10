from fastapi import Depends
from fastapi_error_map import ErrorAwareRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.converters.image_format import to_jpg, to_png, to_webp
from app.converters.image_ico import to_ico
from app.converters.image_resize import resize_image
from app.database import get_db
from app.exceptions import (
    ConversionError,
    ConversionNotNeededError,
    ResourceNotFoundError,
    ResourceValidationError,
)
from app.schemas import ResourceResponse
from app.services import conversion_service

router = ErrorAwareRouter(tags=["Convert"])

_convert_error_map = {
    ResourceNotFoundError: 404,
    ResourceValidationError: 400,
    ConversionError: 400,
    ConversionNotNeededError: 400,
}


class ResizeRequest(BaseModel):
    width: int | None = None
    height: int | None = None
    scale: float | None = None


@router.post(
    "/convert/{resource_id}/resize",
    response_model=ResourceResponse,
    error_map=_convert_error_map,
)
async def convert_resize(
    resource_id: int, body: ResizeRequest, db: AsyncSession = Depends(get_db)
):
    return await conversion_service.convert_image(
        db,
        resource_id,
        resize_image,
        ext=None,
        converter_kwargs={
            "width": body.width,
            "height": body.height,
            "scale": body.scale,
        },
    )


class WebpRequest(BaseModel):
    quality: int = 80


@router.post(
    "/convert/{resource_id}/webp",
    response_model=ResourceResponse,
    error_map=_convert_error_map,
)
async def convert_webp(
    resource_id: int, body: WebpRequest, db: AsyncSession = Depends(get_db)
):
    return await conversion_service.convert_image(
        db, resource_id, to_webp, "webp", converter_args=(body.quality,)
    )


class JpgRequest(BaseModel):
    quality: int = 85


@router.post(
    "/convert/{resource_id}/jpg",
    response_model=ResourceResponse,
    error_map=_convert_error_map,
)
async def convert_jpg(
    resource_id: int, body: JpgRequest, db: AsyncSession = Depends(get_db)
):
    return await conversion_service.convert_image(
        db, resource_id, to_jpg, "jpg", converter_args=(body.quality,)
    )


@router.post(
    "/convert/{resource_id}/png",
    response_model=ResourceResponse,
    error_map=_convert_error_map,
)
async def convert_png(resource_id: int, db: AsyncSession = Depends(get_db)):
    return await conversion_service.convert_image(db, resource_id, to_png, "png")


class IcoRequest(BaseModel):
    sizes: list[int] | None = None


@router.post(
    "/convert/{resource_id}/ico",
    response_model=ResourceResponse,
    error_map=_convert_error_map,
)
async def convert_ico(
    resource_id: int, body: IcoRequest, db: AsyncSession = Depends(get_db)
):
    return await conversion_service.convert_image(
        db, resource_id, to_ico, "ico", converter_args=(body.sizes,)
    )


class Mp4Request(BaseModel):
    crf: int = 23


@router.post(
    "/convert/{resource_id}/mp4",
    response_model=ResourceResponse,
    error_map=_convert_error_map,
)
async def convert_mp4(
    resource_id: int, body: Mp4Request, db: AsyncSession = Depends(get_db)
):
    return await conversion_service.convert_to_mp4(db, resource_id, crf=body.crf)
