from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)          # ex: "PROTO-METAL / HARD ROCK"
    description: Optional[str] = None      # ex: "Early heavy sounds before metal crystallized"
    sort_order: int = Field(default=0)

    artists: List["Artist"] = Relationship(back_populates="category")


class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)          # ex: "Black Sabbath"
    description: Optional[str] = None      # ex: "definitive proto-metal, dark riffs, occult atmosphere"
    sort_order: int = Field(default=0)

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="artists")

    albums: List["Album"] = Relationship(back_populates="artist")


class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: Optional[int] = None
    icon: Optional[str] = None             # ex: "🔥E", "⭐R", "🌘D", "⚠️A", "🌀X"
    rating: Optional[float] = None         # ex: 4.7
    description: Optional[str] = None      # ex: "riff-bible, invented the genre"
    sort_order: int = Field(default=0)

    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    artist: Optional[Artist] = Relationship(back_populates="albums")


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
    sort_order: int
    artist_id: Optional[int]


class AlbumCreate(SQLModel):
    title: str
    year: Optional[int] = None
    icon: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    sort_order: int = 0
    artist_id: int


class AlbumUpdate(SQLModel):
    title: Optional[str] = None
    year: Optional[int] = None
    icon: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    artist_id: Optional[int] = None


# --- Full nested read (for complete display) ---

class AlbumNested(SQLModel):
    id: int
    title: str
    year: Optional[int]
    icon: Optional[str]
    rating: Optional[float]
    description: Optional[str]
    sort_order: int


class ArtistNested(SQLModel):
    id: int
    name: str
    description: Optional[str]
    sort_order: int
    albums: List[AlbumNested] = []


class CategoryNested(SQLModel):
    id: int
    name: str
    description: Optional[str]
    sort_order: int
    artists: List[ArtistNested] = []
