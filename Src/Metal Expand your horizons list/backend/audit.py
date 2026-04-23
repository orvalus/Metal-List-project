"""
Audit: compara albumele unui artist din DB cu discografia de pe Sputnikmusic.
"""

import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class SputnikAlbum:
    title: str
    year: Optional[int]
    rating: Optional[float]


@dataclass
class AuditResult:
    artist_name: str
    sputnik_url: Optional[str]
    missing_albums: List[SputnikAlbum]       # albume pe Sputnikmusic, nu in DB
    extra_albums: List[str]                   # albume in DB, nu pe Sputnikmusic
    order_issues: List[str]                   # probleme de ordine cronologica
    rating_diffs: List[dict]                  # diferente de rating
    sputnik_albums: List[SputnikAlbum]        # discografia completa de pe Sputnikmusic


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


async def _search_artist_sputnik(artist_name: str) -> Optional[str]:
    """Cauta artistul pe Sputnikmusic si returneaza URL-ul profilului."""
    search_url = f"https://www.sputnikmusic.com/search/bands/{httpx.URL(artist_name)}"
    # Sputnikmusic search foloseste GET cu parametru
    search_url = f"https://www.sputnikmusic.com/search_results.php?genreid=0&search_in=Bands&search_text={artist_name.replace(' ', '+')}&x=0&y=0"

    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=20) as client:
        resp = await client.get(search_url)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Cauta link-uri catre pagini de artisti (/bands/...)
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/bands/" in href and artist_name.lower().replace(" ", "") in href.lower().replace("-", "").replace("_", ""):
                if href.startswith("/"):
                    href = "https://www.sputnikmusic.com" + href
                return href

        # Fallback: primul rezultat din search
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/bands/" in href:
                if href.startswith("/"):
                    href = "https://www.sputnikmusic.com" + href
                return href

    return None


async def _get_discography_sputnik(artist_url: str) -> List[SputnikAlbum]:
    """Preia discografia unui artist de pe Sputnikmusic."""
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=20) as client:
        resp = await client.get(artist_url)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        albums = []

        # Sputnikmusic: albumele sunt in tabele cu clasa "album" sau in div-uri
        # Structura variaza, incercam mai multe selectori
        for row in soup.select("table.discography tr, .albumblock, td.albuminfo"):
            title_el = row.select_one(".albumtitle, a[href*='/album/'], strong")
            year_el = row.select_one(".albumyear, .year")
            rating_el = row.select_one(".albumrating, .rating")

            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            if not title or len(title) < 2:
                continue

            year = None
            if year_el:
                import re
                m = re.search(r"\d{4}", year_el.get_text())
                if m:
                    year = int(m.group())

            rating = None
            if rating_el:
                import re
                m = re.search(r"[\d]+\.[\d]+", rating_el.get_text())
                if m:
                    rating = float(m.group())

            albums.append(SputnikAlbum(title=title, year=year, rating=rating))

        return albums


def _normalize(title: str) -> str:
    """Normalizeaza titlul pentru comparatie."""
    import re
    return re.sub(r"[^a-z0-9]", "", title.lower())


async def audit_artist_sputnik(artist_name: str, db_albums: list) -> dict:
    """
    Compara albumele din DB cu discografia de pe Sputnikmusic.
    Returneaza un dict cu rezultatele auditului.
    """
    # 1. Cauta artistul
    artist_url = await _search_artist_sputnik(artist_name)
    if not artist_url:
        return {
            "artist": artist_name,
            "sputnik_url": None,
            "error": "Artistul nu a fost gasit pe Sputnikmusic.",
            "missing_albums": [],
            "extra_albums": [],
            "order_issues": [],
            "rating_diffs": [],
            "sputnik_albums": [],
        }

    # 2. Preia discografia
    sputnik_albums = await _get_discography_sputnik(artist_url)

    # 3. Normalizeaza titlurile pentru comparatie
    db_titles = {_normalize(a.title): a for a in db_albums}
    sputnik_titles = {_normalize(a.title): a for a in sputnik_albums}

    # 4. Albume lipsa (pe Sputnikmusic dar nu in DB)
    missing = [
        {"title": a.title, "year": a.year, "rating": a.rating}
        for key, a in sputnik_titles.items()
        if key not in db_titles
    ]

    # 5. Albume extra (in DB dar nu pe Sputnikmusic)
    extra = [
        a.title
        for key, a in db_titles.items()
        if key not in sputnik_titles
    ]

    # 6. Verificare ordine cronologica (in DB)
    order_issues = []
    years = [(a.title, a.year) for a in db_albums if a.year is not None]
    for i in range(1, len(years)):
        if years[i][1] < years[i - 1][1]:
            order_issues.append(
                f"'{years[i][0]}' ({years[i][1]}) apare dupa '{years[i-1][0]}' ({years[i-1][1]})"
            )

    # 7. Diferente de rating
    rating_diffs = []
    for key, db_album in db_titles.items():
        if key in sputnik_titles:
            sp = sputnik_titles[key]
            if db_album.rating is not None and sp.rating is not None:
                diff = abs(db_album.rating - sp.rating)
                if diff >= 0.2:
                    rating_diffs.append({
                        "title": db_album.title,
                        "db_rating": db_album.rating,
                        "sputnik_rating": sp.rating,
                        "diff": round(diff, 2),
                    })

    return {
        "artist": artist_name,
        "sputnik_url": artist_url,
        "missing_albums": missing,
        "extra_albums": extra,
        "order_issues": order_issues,
        "rating_diffs": rating_diffs,
        "sputnik_albums": [
            {"title": a.title, "year": a.year, "rating": a.rating}
            for a in sputnik_albums
        ],
    }
