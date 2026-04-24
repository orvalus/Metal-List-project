"""
Tests for the parser module - sputnik_url extraction.
"""

import pytest
from parser import parse_text, ParsedAlbum


def test_parse_album_with_sputnik_url():
    """Test parsing an album line with a Sputnikmusic URL."""
    text = """
PROTO-METAL / HARD ROCK
*Early heavy sounds*

***Black Sabbath*** - Proto-metal pioneers
- Paranoid (1970) – 🔥E – ★4.7 – https://www.sputnikmusic.com/album/12345/ – Riff-bible, invented the genre
"""
    categories = parse_text(text)
    
    assert len(categories) == 1
    assert len(categories[0].artists) == 1
    assert len(categories[0].artists[0].albums) == 1
    
    album = categories[0].artists[0].albums[0]
    assert album.title == "Paranoid"
    assert album.year == 1970
    assert album.icon == "🔥E"
    assert album.rating == 4.7
    assert album.sputnik_url == "https://www.sputnikmusic.com/album/12345/"
    assert album.description == "Riff-bible, invented the genre"


def test_parse_album_without_sputnik_url():
    """Test parsing an album line without a URL (backward compatibility)."""
    text = """
PROTO-METAL / HARD ROCK
*Early heavy sounds*

***Black Sabbath*** - Proto-metal pioneers
- Paranoid (1970) – 🔥E – ★4.7 – Riff-bible, invented the genre
"""
    categories = parse_text(text)
    
    album = categories[0].artists[0].albums[0]
    assert album.title == "Paranoid"
    assert album.year == 1970
    assert album.rating == 4.7
    # URL should be None or empty when not provided
    assert album.sputnik_url is None or album.sputnik_url == ""


def test_parse_album_with_url_in_middle():
    """Test parsing album line where URL is between rating and description."""
    text = """
PROTO-METAL / HARD ROCK

***Led Zeppelin*** - Blues rock legend
- Led Zeppelin IV (1971) – ⭐R – ★4.5 – https://www.sputnikmusic.com/album/67890/ – Genre-defining masterpiece
"""
    categories = parse_text(text)
    
    album = categories[0].artists[0].albums[0]
    assert album.title == "Led Zeppelin IV"
    assert album.year == 1971
    assert album.icon == "⭐R"
    assert album.rating == 4.5
    assert album.sputnik_url == "https://www.sputnikmusic.com/album/67890/"
    assert "masterpiece" in album.description


def test_parse_multiple_albums_with_urls():
    """Test parsing multiple albums with URLs."""
    text = """
PROTO-METAL / HARD ROCK

***Black Sabbath*** - Proto-metal
- Paranoid (1970) – 🔥E – ★4.7 – https://www.sputnikmusic.com/album/1/ – First
- Master of Reality (1971) – 🔥E – ★4.6 – https://www.sputnikmusic.com/album/2/ – Second
"""
    categories = parse_text(text)
    
    artist = categories[0].artists[0]
    assert len(artist.albums) == 2
    
    assert artist.albums[0].sputnik_url == "https://www.sputnikmusic.com/album/1/"
    assert artist.albums[1].sputnik_url == "https://www.sputnikmusic.com/album/2/"


def test_parse_album_url_with_various_formats():
    """Test parsing URLs in different formats."""
    urls = [
        "https://www.sputnikmusic.com/album/12345/",
        "https://www.sputnikmusic.com/album/99999",
        "https://sputnikmusic.com/album/xyz/",
    ]
    
    for url in urls:
        text = f"""
PROTO-METAL / HARD ROCK

***Artist*** - Test
- Album (2000) – 🔥E – ★4.0 – {url} – Description
"""
        categories = parse_text(text)
        album = categories[0].artists[0].albums[0]
        assert album.sputnik_url == url, f"Failed to parse URL: {url}"
