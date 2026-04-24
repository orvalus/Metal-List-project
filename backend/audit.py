"""
Audit: compare an artist's albums from DB with their discography on Sputnikmusic.

Implements rate limiting to avoid IP bans from Sputnikmusic.
"""

import httpx
import asyncio
import logging
from bs4 import BeautifulSoup
from typing import List, Optional
from dataclasses import dataclass
from rate_limiter import execute_with_rate_limit

logger = logging.getLogger(__name__)


@dataclass
class SputnikAlbum:
    title: str
    year: Optional[int]
    rating: Optional[float]


@dataclass
class AuditResult:
    artist_name: str
    sputnik_url: Optional[str]
    missing_albums: List[SputnikAlbum]       # albums on Sputnikmusic but not in DB
    extra_albums: List[str]                   # albums in DB but not on Sputnikmusic
    order_issues: List[str]                   # chronological order issues
    rating_diffs: List[dict]                  # rating differences
    sputnik_albums: List[SputnikAlbum]        # complete discography from Sputnikmusic


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


async def _search_artist_sputnik(artist_name: str) -> Optional[str]:
    """
    Search for the artist on Sputnikmusic and return the profile URL.
    
    Uses rate limiting to avoid IP bans.
    """
    search_url = f"https://www.sputnikmusic.com/search_results.php?genreid=0&search_in=Bands&search_text={artist_name.replace(' ', '+')}&x=0&y=0"

    async def _fetch_and_parse():
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=20) as client:
            logger.info(f"Searching for artist: {artist_name}")
            resp = await client.get(search_url)
            
            if resp.status_code != 200:
                logger.warning(f"Search failed for {artist_name} (status {resp.status_code})")
                return None

            soup = BeautifulSoup(resp.text, "html.parser")

            # Search for links to artist pages (/bands/...)
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/bands/" in href and artist_name.lower().replace(" ", "") in href.lower().replace("-", "").replace("_", ""):
                    if href.startswith("/"):
                        href = "https://www.sputnikmusic.com" + href
                    logger.info(f"Found artist URL: {href}")
                    return href

            # Fallback: first search result
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/bands/" in href:
                    if href.startswith("/"):
                        href = "https://www.sputnikmusic.com" + href
                    logger.info(f"Using first search result: {href}")
                    return href

        return None
    
    # Execute with rate limiting
    return await execute_with_rate_limit(_fetch_and_parse)


async def _get_discography_sputnik(artist_url: str) -> List[SputnikAlbum]:
    """
    Fetch an artist's discography from Sputnikmusic.
    
    Uses rate limiting to avoid IP bans.
    """
    
    async def _fetch_discography():
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=20) as client:
            logger.info(f"Fetching discography: {artist_url}")
            resp = await client.get(artist_url)
            
            if resp.status_code != 200:
                logger.warning(f"Failed to fetch {artist_url} (status {resp.status_code})")
                return []

            soup = BeautifulSoup(resp.text, "html.parser")
            albums = []

            # Sputnikmusic: albums are in tables with "album" class or in divs
            # Structure varies, try multiple selectors
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

            logger.info(f"Found {len(albums)} albums for {artist_url}")
            return albums
    
    # Execute with rate limiting
    result = await execute_with_rate_limit(_fetch_discography)
    return result or []


def _normalize(title: str) -> str:
    """Normalize the title for comparison."""
    import re
    return re.sub(r"[^a-z0-9]", "", title.lower())


async def audit_artist_sputnik(artist_name: str, db_albums: list) -> dict:
    """
    Compare DB albums with discography on Sputnikmusic.
    Return a dict with audit results.
    """
    # 1. Search for the artist
    artist_url = await _search_artist_sputnik(artist_name)
    if not artist_url:
        return {
            "artist": artist_name,
            "sputnik_url": None,
            "error": "Artist not found on Sputnikmusic.",
            "missing_albums": [],
            "extra_albums": [],
            "order_issues": [],
            "rating_diffs": [],
            "sputnik_albums": [],
        }

    # 2. Fetch discography
    sputnik_albums = await _get_discography_sputnik(artist_url)

    # 3. Normalize titles for comparison
    db_titles = {_normalize(a.title): a for a in db_albums}
    sputnik_titles = {_normalize(a.title): a for a in sputnik_albums}

    # 4. Missing albums (on Sputnikmusic but not in DB)
    missing = [
        {"title": a.title, "year": a.year, "rating": a.rating}
        for key, a in sputnik_titles.items()
        if key not in db_titles
    ]

    # 5. Extra albums (in DB but not on Sputnikmusic)
    extra = [
        a.title
        for key, a in db_titles.items()
        if key not in sputnik_titles
    ]

    # 6. Check chronological order (in DB)
    order_issues = []
    years = [(a.title, a.year) for a in db_albums if a.year is not None]
    for i in range(1, len(years)):
        if years[i][1] < years[i - 1][1]:
            order_issues.append(
                f"'{years[i][0]}' ({years[i][1]}) appears after '{years[i-1][0]}' ({years[i-1][1]})"
            )

    # 7. Rating differences
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
