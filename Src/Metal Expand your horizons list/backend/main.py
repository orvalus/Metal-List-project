from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional

from database import create_db_and_tables, get_session
from models import (
    Category, CategoryCreate, CategoryRead, CategoryUpdate, CategoryNested,
    Artist, ArtistCreate, ArtistRead, ArtistUpdate, ArtistNested,
    Album, AlbumCreate, AlbumRead, AlbumUpdate, AlbumNested,
)
from importer import fetch_google_doc_text, import_parsed_data
from parser import parse_text

app = FastAPI(title="Metal List API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ─────────────────────────────────────────────
# IMPORT ROUTES
# ─────────────────────────────────────────────

@app.post("/import/url", summary="Import from Google Docs URL")
async def import_from_url(
    url: str = Query(..., description="Public Google Docs URL"),
    replace: bool = Query(False, description="Delete existing data before import"),
    session: Session = Depends(get_session),
):
    try:
        text = await fetch_google_doc_text(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to access Google Docs: {str(e)}")

    categories = parse_text(text)
    if not categories:
        raise HTTPException(status_code=422, detail="No categories detected in document. Check the format.")

    import_parsed_data(session, categories, replace=replace)
    total_artists = sum(len(c.artists) for c in categories)
    total_albums = sum(len(a.albums) for c in categories for a in c.artists)

    return {
        "imported": {
            "categories": len(categories),
            "artists": total_artists,
            "albums": total_albums,
        }
    }


@app.post("/import/text", summary="Import from raw text")
async def import_from_text(
    body: dict,
    session: Session = Depends(get_session),
):
    text = body.get("text", "")
    replace = body.get("replace", False)
    if not text:
        raise HTTPException(status_code=400, detail="The 'text' field is empty.")

    categories = parse_text(text)
    if not categories:
        raise HTTPException(status_code=422, detail="No categories detected in text. Check the format.")

    import_parsed_data(session, categories, replace=replace)
    total_artists = sum(len(c.artists) for c in categories)
    total_albums = sum(len(a.albums) for c in categories for a in c.artists)

    return {
        "imported": {
            "categories": len(categories),
            "artists": total_artists,
            "albums": total_albums,
        }
    }


# ─────────────────────────────────────────────
# FULL LIST (nested)
# ─────────────────────────────────────────────

@app.get("/list", response_model=List[CategoryNested], summary="Lista completa (nested)")
def get_full_list(session: Session = Depends(get_session)):
    categories = session.exec(select(Category).order_by(Category.sort_order)).all()
    result = []
    for cat in categories:
        artists = session.exec(
            select(Artist).where(Artist.category_id == cat.id).order_by(Artist.sort_order)
        ).all()
        artists_nested = []
        for artist in artists:
            albums = session.exec(
                select(Album).where(Album.artist_id == artist.id).order_by(Album.sort_order)
            ).all()
            artists_nested.append(ArtistNested(
                id=artist.id,
                name=artist.name,
                description=artist.description,
                sort_order=artist.sort_order,
                albums=[AlbumNested(**a.model_dump()) for a in albums],
            ))
        result.append(CategoryNested(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            sort_order=cat.sort_order,
            artists=artists_nested,
        ))
    return result


# ─────────────────────────────────────────────
# CATEGORIES CRUD
# ─────────────────────────────────────────────

@app.get("/categories", response_model=List[CategoryRead])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category).order_by(Category.sort_order)).all()


@app.post("/categories", response_model=CategoryRead, status_code=201)
def create_category(data: CategoryCreate, session: Session = Depends(get_session)):
    cat = Category(**data.model_dump())
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@app.patch("/categories/{cat_id}", response_model=CategoryRead)
def update_category(cat_id: int, data: CategoryUpdate, session: Session = Depends(get_session)):
    cat = session.get(Category, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category does not exist")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@app.delete("/categories/{cat_id}", status_code=204)
def delete_category(cat_id: int, session: Session = Depends(get_session)):
    cat = session.get(Category, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category does not exist")
    # Delete artists and albums in cascade
    artists = session.exec(select(Artist).where(Artist.category_id == cat_id)).all()
    for artist in artists:
        albums = session.exec(select(Album).where(Album.artist_id == artist.id)).all()
        for album in albums:
            session.delete(album)
        session.delete(artist)
    session.delete(cat)
    session.commit()


# ─────────────────────────────────────────────
# ARTISTS CRUD
# ─────────────────────────────────────────────

@app.get("/artists", response_model=List[ArtistRead])
def get_artists(
    category_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    query = select(Artist).order_by(Artist.sort_order)
    if category_id is not None:
        query = query.where(Artist.category_id == category_id)
    return session.exec(query).all()


@app.post("/artists", response_model=ArtistRead, status_code=201)
def create_artist(data: ArtistCreate, session: Session = Depends(get_session)):
    if not session.get(Category, data.category_id):
        raise HTTPException(status_code=404, detail="Category does not exist")
    artist = Artist(**data.model_dump())
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


@app.patch("/artists/{artist_id}", response_model=ArtistRead)
def update_artist(artist_id: int, data: ArtistUpdate, session: Session = Depends(get_session)):
    artist = session.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist does not exist")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(artist, field, value)
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


@app.delete("/artists/{artist_id}", status_code=204)
def delete_artist(artist_id: int, session: Session = Depends(get_session)):
    artist = session.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist does not exist")
    albums = session.exec(select(Album).where(Album.artist_id == artist_id)).all()
    for album in albums:
        session.delete(album)
    session.delete(artist)
    session.commit()


# ─────────────────────────────────────────────
# ALBUMS CRUD
# ─────────────────────────────────────────────

@app.get("/albums", response_model=List[AlbumRead])
def get_albums(
    artist_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    query = select(Album).order_by(Album.sort_order)
    if artist_id is not None:
        query = query.where(Album.artist_id == artist_id)
    return session.exec(query).all()


@app.post("/albums", response_model=AlbumRead, status_code=201)
def create_album(data: AlbumCreate, session: Session = Depends(get_session)):
    if not session.get(Artist, data.artist_id):
        raise HTTPException(status_code=404, detail="Artist does not exist")
    album = Album(**data.model_dump())
    session.add(album)
    session.commit()
    session.refresh(album)
    return album


@app.patch("/albums/{album_id}", response_model=AlbumRead)
def update_album(album_id: int, data: AlbumUpdate, session: Session = Depends(get_session)):
    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album does not exist")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(album, field, value)
    session.add(album)
    session.commit()
    session.refresh(album)
    return album


@app.delete("/albums/{album_id}", status_code=204)
def delete_album(album_id: int, session: Session = Depends(get_session)):
    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album does not exist")
    session.delete(album)
    session.commit()


# ─────────────────────────────────────────────
# AUDIT
# ─────────────────────────────────────────────

@app.get("/audit/{artist_id}", summary="Audit an artist against Sputnikmusic")
async def audit_artist(artist_id: int, session: Session = Depends(get_session)):
    from audit import audit_artist_sputnik
    artist = session.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist does not exist")
    albums_in_db = session.exec(select(Album).where(Album.artist_id == artist_id).order_by(Album.sort_order)).all()
    result = await audit_artist_sputnik(artist.name, albums_in_db)
    return result
