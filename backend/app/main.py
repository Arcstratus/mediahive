from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import MEDIA_DIR
from app.database import lifespan
from app.routers import health, imports, resources, stats, tags

app = FastAPI(title="MediaHive", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(resources.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(imports.router, prefix="/api")
app.include_router(stats.router, prefix="/api")

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/api/media", StaticFiles(directory=MEDIA_DIR), name="media")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
