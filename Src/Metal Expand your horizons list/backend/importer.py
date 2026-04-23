"""
Importa date din Google Docs URL sau din text direct in SQLite.
"""

import httpx
from sqlmodel import Session, select
from models import Category, Artist, Album
from parser import parse_text, ParsedCategory


def _google_docs_export_url(url: str) -> str:
    """
    Converteste un URL Google Docs intr-un URL de export plain text.
    Suporta formatul: https://docs.google.com/document/d/DOC_ID/edit
    """
    import re
    m = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        raise ValueError("URL invalid Google Docs. Format asteptat: https://docs.google.com/document/d/DOC_ID/edit")
    doc_id = m.group(1)
    return f"https://docs.google.com/document/d/{doc_id}/export?format=txt"


async def fetch_google_doc_text(url: str) -> str:
    """Preia textul din Google Docs via export URL."""
    export_url = _google_docs_export_url(url)
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        response = await client.get(export_url)
        response.raise_for_status()
        return response.text


def import_parsed_data(session: Session, categories: list[ParsedCategory], replace: bool = False):
    """
    Salveaza categoriile parsate in SQLite.
    Daca replace=True, sterge tot ce exista inainte.
    """
    if replace:
        # Sterge in ordine inversa (FK constraints)
        albums = session.exec(select(Album)).all()
        for a in albums:
            session.delete(a)
        artists = session.exec(select(Artist)).all()
        for a in artists:
            session.delete(a)
        cats = session.exec(select(Category)).all()
        for c in cats:
            session.delete(c)
        session.commit()

    for parsed_cat in categories:
        cat = Category(
            name=parsed_cat.name,
            description=parsed_cat.description,
            sort_order=parsed_cat.sort_order,
        )
        session.add(cat)
        session.flush()  # obtine cat.id

        for parsed_artist in parsed_cat.artists:
            artist = Artist(
                name=parsed_artist.name,
                description=parsed_artist.description,
                sort_order=parsed_artist.sort_order,
                category_id=cat.id,
            )
            session.add(artist)
            session.flush()

            for parsed_album in parsed_artist.albums:
                album = Album(
                    title=parsed_album.title,
                    year=parsed_album.year,
                    icon=parsed_album.icon,
                    rating=parsed_album.rating,
                    description=parsed_album.description,
                    sort_order=parsed_album.sort_order,
                    artist_id=artist.id,
                )
                session.add(album)

    session.commit()
