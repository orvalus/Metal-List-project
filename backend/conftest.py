"""
Pytest configuration and fixtures for Metal List backend tests.
"""
import pytest
from sqlmodel import SQLModel, Session, create_engine


@pytest.fixture
def test_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture
def test_session(test_engine):
    """Provide a test database session with auto-cleanup."""
    with Session(test_engine) as session:
        yield session
        session.rollback()  # Ensure clean state
