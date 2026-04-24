"""
Integration tests for importer.py - testing data import and validation.
Tests happy path, error cases, and cascade delete logic.
"""
import pytest
from sqlmodel import select
from models import Category, Artist, Album
from importer import import_parsed_data
from parser import ParsedCategory, ParsedArtist, ParsedAlbum


class TestImporterHappyPath:
    """Tests for successful import scenarios."""

    def test_import_single_category(self, test_session):
        """Test importing a single category."""
        cat = ParsedCategory(
            name="PROTO-METAL",
            description="Early metal sound",
            artists=[],
            sort_order=0,
        )
        import_parsed_data(test_session, [cat])
        
        saved = test_session.exec(select(Category)).all()
        assert len(saved) == 1
        assert saved[0].name == "PROTO-METAL"
        assert saved[0].description == "Early metal sound"

    def test_import_category_with_artist(self, test_session):
        """Test importing category with artist."""
        artist = ParsedArtist(
            name="Black Sabbath",
            description="Proto-metal pioneers",
            albums=[],
            sort_order=0,
        )
        cat = ParsedCategory(
            name="PROTO-METAL",
            description="",
            artists=[artist],
            sort_order=0,
        )
        import_parsed_data(test_session, [cat])
        
        cats = test_session.exec(select(Category)).all()
        artists = test_session.exec(select(Artist)).all()
        assert len(cats) == 1
        assert len(artists) == 1
        assert artists[0].category_id == cats[0].id

    def test_import_artist_with_album(self, test_session):
        """Test importing artist with complete album."""
        album = ParsedAlbum(
            title="Paranoid",
            year=1970,
            icon="🔥E",
            rating=4.7,
            description="Masterpiece",
            sort_order=0,
            sputnik_url="https://www.sputnikmusic.com/album/1/",
        )
        artist = ParsedArtist(
            name="Black Sabbath",
            description="",
            albums=[album],
            sort_order=0,
        )
        cat = ParsedCategory(
            name="PROTO-METAL",
            description="",
            artists=[artist],
            sort_order=0,
        )
        import_parsed_data(test_session, [cat])
        
        albums = test_session.exec(select(Album)).all()
        assert len(albums) == 1
        assert albums[0].title == "Paranoid"
        assert albums[0].year == 1970
        assert albums[0].rating == 4.7
        assert albums[0].sputnik_url == "https://www.sputnikmusic.com/album/1/"

    def test_import_multiple_artists_with_multiple_albums(self, test_session):
        """Test importing multiple artists and albums."""
        artists = [
            ParsedArtist(
                name="Black Sabbath",
                description="",
                albums=[
                    ParsedAlbum("Paranoid", 1970, "🔥E", 4.7, "d1", 0, None),
                    ParsedAlbum("Master of Reality", 1971, "🔥E", 4.6, "d2", 1, None),
                ],
                sort_order=0,
            ),
            ParsedArtist(
                name="Led Zeppelin",
                description="",
                albums=[
                    ParsedAlbum("IV", 1971, "🔥E", 4.7, "d3", 0, None),
                ],
                sort_order=1,
            ),
        ]
        cat = ParsedCategory(
            name="HARD ROCK",
            description="",
            artists=artists,
            sort_order=0,
        )
        import_parsed_data(test_session, [cat])
        
        albums = test_session.exec(select(Album)).all()
        assert len(albums) == 3
        assert all(a.artist_id is not None for a in albums)


class TestImporterReplace:
    """Tests for replace=True behavior."""

    def test_replace_true_clears_data(self, test_session):
        """Test that replace=True deletes existing data before import."""
        old_cat = ParsedCategory(name="OLD", description="", artists=[], sort_order=0)
        import_parsed_data(test_session, [old_cat])
        assert len(test_session.exec(select(Category)).all()) == 1
        
        new_cat = ParsedCategory(name="NEW", description="", artists=[], sort_order=0)
        import_parsed_data(test_session, [new_cat], replace=True)
        
        cats = test_session.exec(select(Category)).all()
        assert len(cats) == 1
        assert cats[0].name == "NEW"

    def test_replace_false_preserves_data(self, test_session):
        """Test that replace=False keeps existing data."""
        cat1 = ParsedCategory(name="CAT1", description="", artists=[], sort_order=0)
        import_parsed_data(test_session, [cat1])
        
        cat2 = ParsedCategory(name="CAT2", description="", artists=[], sort_order=1)
        import_parsed_data(test_session, [cat2], replace=False)
        
        cats = test_session.exec(select(Category)).all()
        assert len(cats) == 2


class TestImporterEdgeCases:
    """Tests for edge cases and unusual inputs."""

    def test_import_empty_list(self, test_session):
        """Test importing empty list."""
        import_parsed_data(test_session, [])
        assert len(test_session.exec(select(Category)).all()) == 0

    def test_import_album_without_url(self, test_session):
        """Test album without sputnik_url."""
        album = ParsedAlbum("Album", 2020, None, 4.5, "desc", 0, sputnik_url=None)
        artist = ParsedArtist("Artist", "", [album], 0)
        cat = ParsedCategory("CAT", "", [artist], 0)
        import_parsed_data(test_session, [cat])
        
        albums = test_session.exec(select(Album)).all()
        assert len(albums) == 1
        assert albums[0].sputnik_url is None

    def test_import_preserves_sort_order(self, test_session):
        """Test that sort_order is preserved."""
        artists = [
            ParsedArtist("Artist1", "", [], 0),
            ParsedArtist("Artist2", "", [], 1),
            ParsedArtist("Artist3", "", [], 2),
        ]
        cat = ParsedCategory("CAT", "", artists, 0)
        import_parsed_data(test_session, [cat])
        
        saved = test_session.exec(select(Artist).order_by(Artist.sort_order)).all()
        assert len(saved) == 3
        assert saved[0].sort_order == 0
        assert saved[1].sort_order == 1
        assert saved[2].sort_order == 2

    def test_import_maintains_relationships(self, test_session):
        """Test that FK relationships are correct."""
        album1 = ParsedAlbum("Album1", 2020, None, 4.5, "d1", 0, None)
        album2 = ParsedAlbum("Album2", 2021, None, 4.3, "d2", 1, None)
        artist = ParsedArtist("Artist", "", [album1, album2], 0)
        cat = ParsedCategory("CAT", "", [artist], 0)
        import_parsed_data(test_session, [cat])
        
        albums = test_session.exec(select(Album)).all()
        artist_db = test_session.exec(select(Artist)).first()
        cat_db = test_session.exec(select(Category)).first()
        
        assert all(a.artist_id == artist_db.id for a in albums)
        assert artist_db.category_id == cat_db.id


class TestDeleteOperations:
    """Tests for delete operations and cascade behavior."""

    def test_delete_album(self, test_session):
        """Test deleting an album."""
        album = ParsedAlbum("Album", 2020, None, 4.5, "desc", 0)
        artist = ParsedArtist("Artist", "", [album], 0)
        cat = ParsedCategory("CAT", "", [artist], 0)
        import_parsed_data(test_session, [cat])
        
        albums_before = test_session.exec(select(Album)).all()
        assert len(albums_before) == 1
        
        test_session.delete(albums_before[0])
        test_session.commit()
        
        albums_after = test_session.exec(select(Album)).all()
        assert len(albums_after) == 0

    def test_delete_artist(self, test_session):
        """Test deleting an artist."""
        album = ParsedAlbum("Album", 2020, None, 4.5, "desc", 0)
        artist = ParsedArtist("Artist", "", [album], 0)
        cat = ParsedCategory("CAT", "", [artist], 0)
        import_parsed_data(test_session, [cat])
        
        artists_before = test_session.exec(select(Artist)).all()
        assert len(artists_before) == 1
        
        test_session.delete(artists_before[0])
        test_session.commit()
        
        artists_after = test_session.exec(select(Artist)).all()
        assert len(artists_after) == 0

    def test_delete_category(self, test_session):
        """Test deleting a category."""
        artist = ParsedArtist("Artist", "", [], 0)
        cat = ParsedCategory("CAT", "", [artist], 0)
        import_parsed_data(test_session, [cat])
        
        cats_before = test_session.exec(select(Category)).all()
        assert len(cats_before) == 1
        
        test_session.delete(cats_before[0])
        test_session.commit()
        
        cats_after = test_session.exec(select(Category)).all()
        assert len(cats_after) == 0

    def test_multiple_albums_independent_delete(self, test_session):
        """Test deleting one album doesn't affect others."""
        albums = [
            ParsedAlbum("Album1", 2020, None, 4.5, "d1", 0),
            ParsedAlbum("Album2", 2021, None, 4.3, "d2", 1),
            ParsedAlbum("Album3", 2022, None, 4.1, "d3", 2),
        ]
        artist = ParsedArtist("Artist", "", albums, 0)
        cat = ParsedCategory("CAT", "", [artist], 0)
        import_parsed_data(test_session, [cat])
        
        all_albums = test_session.exec(select(Album)).all()
        assert len(all_albums) == 3
        
        test_session.delete(all_albums[1])
        test_session.commit()
        
        remaining = test_session.exec(select(Album)).all()
        assert len(remaining) == 2
        titles = {a.title for a in remaining}
        assert titles == {"Album1", "Album3"}
