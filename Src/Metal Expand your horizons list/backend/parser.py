"""
Parser pentru formatul de lista generat de promptul de muzica.

Format asteptat:
    CATEGORY NAME
    *italic description*

    ***Artist Name*** - short technical description

    - Album Name (Year) – ICON – ★Rating – short description
"""

import re
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class ParsedAlbum:
    title: str
    year: Optional[int]
    icon: Optional[str]
    rating: Optional[float]
    description: Optional[str]
    sort_order: int


@dataclass
class ParsedArtist:
    name: str
    description: Optional[str]
    albums: List[ParsedAlbum] = field(default_factory=list)
    sort_order: int = 0


@dataclass
class ParsedCategory:
    name: str
    description: Optional[str]
    artists: List[ParsedArtist] = field(default_factory=list)
    sort_order: int = 0


# Icon patterns recunoscute
ICONS = ["🔥E", "⭐R", "🌘D", "⚠️A", "🌀X"]

# Regex pentru linie de album:
# - Album Name (Year) – ICON – ★Rating – description
# Separatorul poate fi – (em dash) sau - (hyphen)
ALBUM_RE = re.compile(
    r"^[-•*]\s*"                          # bullet point
    r"(?P<title>.+?)"                      # titlu album
    r"\s*[\(\[](?P<year>\d{4})[\)\]]"      # (Year)
    r"\s*[–\-]+\s*"                        # separator
    r"(?P<icon>[🔥⭐🌘⚠️🌀][A-Z])?"         # icon optional
    r"\s*[–\-]+\s*"                        # separator
    r"[★*]?(?P<rating>[\d]+\.[\d]+)"       # rating ex: 4.5
    r"\s*[–\-]+\s*"                        # separator
    r"(?P<description>.+)?$",              # descriere
    re.UNICODE
)

# Regex pentru artist: ***Name*** - description  sau  **_Name_** - description
ARTIST_RE = re.compile(
    r"^\*{2,3}_?(?P<name>[^*_]+?)_?\*{2,3}"
    r"(?:\s*[-–]\s*(?P<description>.+))?$"
)

# Regex pentru categorie: ALL CAPS line (minim 3 cuvinte sau 5+ caractere majuscule)
CATEGORY_RE = re.compile(r"^[A-Z][A-Z\s/\-&]{4,}$")


def _strip_markdown(text: str) -> str:
    """Elimina formatare markdown simpla."""
    text = re.sub(r"\*{1,3}|_{1,3}", "", text)
    return text.strip()


def _parse_album_line(line: str, sort_order: int) -> Optional[ParsedAlbum]:
    """Parseaza o linie de album."""
    line = line.strip()
    m = ALBUM_RE.match(line)
    if not m:
        return None

    title = _strip_markdown(m.group("title")).strip()
    year_str = m.group("year")
    year = int(year_str) if year_str else None
    icon = m.group("icon")
    rating_str = m.group("rating")
    rating = float(rating_str) if rating_str else None
    description = m.group("description")
    if description:
        description = description.strip()

    return ParsedAlbum(
        title=title,
        year=year,
        icon=icon,
        rating=rating,
        description=description,
        sort_order=sort_order,
    )


def _parse_artist_line(line: str, sort_order: int) -> Optional[ParsedArtist]:
    """Parseaza o linie de artist."""
    line = line.strip()
    m = ARTIST_RE.match(line)
    if not m:
        return None

    name = m.group("name").strip()
    description = m.group("description")
    if description:
        description = description.strip()

    return ParsedArtist(name=name, description=description, sort_order=sort_order)


def parse_text(text: str) -> List[ParsedCategory]:
    """
    Parseaza textul complet si returneaza o lista de categorii cu artisti si albume.
    """
    lines = text.splitlines()
    categories: List[ParsedCategory] = []
    current_category: Optional[ParsedCategory] = None
    current_artist: Optional[ParsedArtist] = None
    pending_description: Optional[str] = None  # descriere categorie (linia urmatoare)

    cat_sort = 0
    artist_sort = 0
    album_sort = 0

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        # --- Incearca sa parseze ca album ---
        if line.startswith(("-", "•", "*")) and current_artist is not None:
            album = _parse_album_line(line, album_sort)
            if album:
                current_artist.albums.append(album)
                album_sort += 1
                continue

        # --- Incearca sa parseze ca artist ---
        artist = _parse_artist_line(line, artist_sort)
        if artist:
            if current_artist and current_category:
                current_category.artists.append(current_artist)
            current_artist = artist
            artist_sort += 1
            album_sort = 0
            continue

        # --- Incearca sa parseze ca categorie ---
        # Detectam categorii: linie ALL CAPS (fara bullet, fara **)
        clean_line = _strip_markdown(line)
        if CATEGORY_RE.match(clean_line) and not line.startswith(("*", "-", "•")):
            # Salveaza categoria curenta
            if current_artist and current_category:
                current_category.artists.append(current_artist)
                current_artist = None
            if current_category:
                categories.append(current_category)

            current_category = ParsedCategory(
                name=clean_line,
                description=None,
                sort_order=cat_sort,
            )
            cat_sort += 1
            artist_sort = 0
            pending_description = None
            continue

        # --- Descriere categorie (linia italica dupa categoria) ---
        italic_line = re.match(r"^\*(.+)\*$", line)
        if italic_line and current_category and not current_artist:
            current_category.description = italic_line.group(1).strip()
            continue

    # Salveaza ultimele elemente
    if current_artist and current_category:
        current_category.artists.append(current_artist)
    if current_category:
        categories.append(current_category)

    return categories
