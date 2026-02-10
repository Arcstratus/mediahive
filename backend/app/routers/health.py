from fastapi_error_map import ErrorAwareRouter

router = ErrorAwareRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {"status": "ok"}
