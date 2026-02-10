from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

resource_tags = Table(
    "resource_tags",
    Base.metadata,
    Column("resource_id", Integer, ForeignKey("resources.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

bookmark_tags = Table(
    "bookmark_tags",
    Base.metadata,
    Column("bookmark_id", Integer, ForeignKey("bookmarks.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    resources: Mapped[list["Resource"]] = relationship(
        secondary=resource_tags, back_populates="tags"
    )
    bookmarks: Mapped[list["Bookmark"]] = relationship(
        secondary=bookmark_tags, back_populates="tags"
    )


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    folder: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    thumbnail: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=resource_tags, back_populates="resources", lazy="selectin"
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    folder: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=bookmark_tags, back_populates="bookmarks", lazy="selectin"
    )
