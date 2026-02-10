from pydantic import BaseModel


class StatsResponse(BaseModel):
    images: int
    videos: int
    bookmarks: int
    tags: int
