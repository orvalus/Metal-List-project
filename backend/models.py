from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    sort_order: int = Field(default=0)

    artists: Mapped[List["Artist"]] = Relationship(back_populates="category")


class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    sort_order: int = Field(default=0)

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Mapped[Optional["Category"]] = Relationship(back_populates="artists")

    albums: Mapped[List["Album"]] = Relationship(back_populates="artist")


class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: Optional[int] = None
    icon: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    sputnik_url: Optional[str] = None
    sort_order: int = Field(default=0)

    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    artist: Mapped[Optional["Artist"]] = Relationship(back_populates="albums")


# --- Response/Request schemas (without table=True) ---

class CategoryRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    sort_order: int


class CategoryCreate(SQLModel):
    name: str
    description: Optional[str] = None
    sort_order: int = 0


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None


class ArtistRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    sort_order: int
    category_id: Optional[int]


class ArtistCreate(SQLModel):
    name: str
    description: Optional[str] = None
    sort_order: int = 0
    category_id: int


class ArtistUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    category_id: Optional[int] = None


class AlbumRead(SQLModel):
    id: int
    title: str
    year: Optional[int]
    icon: Optional[str]
    rating: Optional[float]
    description: Optional[str]
    sputnik_url: Optional[str]
    sort_order: int
    artist_id: Optional[int]


class AlbumCreate(SQLModel):
    title: str
    year: Optional[int] = None
    icon: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    sputnik_url: Optional[str] = None
    sort_order: int = 0
    artist_id: int


class AlbumUpdate(SQLModel):
    title: Optional[str] = None
    year: Optional[int] = None
    icon: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    sputnik_url: Optional[str] = None
    sort_order: Optional[int] = None
    artist_id: Optional[int] = None


# --- Nested response schemas ---

class AlbumNested(AlbumRead):
    pass


class ArtistNested(ArtistRead):
    albums: List[AlbumNested] = []


class CategoryNested(CategoryRead):
    artists: List[ArtistNested] = []
