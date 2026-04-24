"""
Tests for the models module - Album sputnik_url field.
"""

import pytest
from models import AlbumCreate, AlbumRead, AlbumUpdate


def test_album_create_schema_has_sputnik_url():
    """Test that AlbumCreate schema includes sputnik_url."""
    album_data = AlbumCreate(
        title="Test Album",
        year=2020,
        icon="🔥E",
        rating=4.5,
        description="Test",
        sputnik_url="https://www.sputnikmusic.com/album/12345/",
        artist_id=1
    )
    assert album_data.sputnik_url == "https://www.sputnikmusic.com/album/12345/"


def test_album_create_schema_sputnik_url_optional():
    """Test that sputnik_url is optional in AlbumCreate schema."""
    album_data = AlbumCreate(
        title="Test Album",
        artist_id=1
    )
    assert album_data.sputnik_url is None


def test_album_update_schema_has_sputnik_url():
    """Test that AlbumUpdate schema includes sputnik_url."""
    album_update = AlbumUpdate(
        sputnik_url="https://www.sputnikmusic.com/album/54321/"
    )
    assert album_update.sputnik_url == "https://www.sputnikmusic.com/album/54321/"


def test_album_read_schema_has_sputnik_url():
    """Test that AlbumRead schema includes sputnik_url."""
    album_read = AlbumRead(
        id=1,
        title="Test Album",
        year=2020,
        icon="🔥E",
        rating=4.5,
        description="Test",
        sputnik_url="https://www.sputnikmusic.com/album/12345/",
        sort_order=0,
        artist_id=1
    )
    assert album_read.sputnik_url == "https://www.sputnikmusic.com/album/12345/"
