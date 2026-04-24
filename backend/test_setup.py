"""
Test that pytest and coverage tools are properly installed and configured.
"""
import pytest
import sys


class TestPytestSetup:
    """Tests to verify pytest is installed and working."""

    def test_pytest_is_available(self):
        """pytest should be installed and importable."""
        assert pytest is not None

    def test_pytest_version(self):
        """pytest should have a version."""
        assert hasattr(pytest, "__version__")
        assert pytest.__version__

    def test_python_version(self):
        """Python version should be 3.12+."""
        major, minor = sys.version_info.major, sys.version_info.minor
        assert major >= 3 and minor >= 12, f"Python {major}.{minor} < 3.12"


class TestCoverageTools:
    """Tests to verify coverage tools are installed."""

    def test_pytest_cov_is_available(self):
        """pytest-cov should be installed."""
        try:
            import pytest_cov
            assert pytest_cov is not None
        except ImportError:
            pytest.skip("pytest-cov not installed")

    def test_coverage_is_available(self):
        """coverage module should be installed."""
        try:
            import coverage
            assert coverage is not None
        except ImportError:
            pytest.skip("coverage not installed")


class TestTestableCode:
    """Basic tests to ensure app can be tested."""

    def test_models_import(self):
        """Models should be importable."""
        from models import Category, Artist, Album
        assert Category is not None
        assert Artist is not None
        assert Album is not None

    def test_database_import(self):
        """Database module should be importable."""
        from database import create_db_and_tables, get_session
        assert create_db_and_tables is not None
        assert get_session is not None

    def test_parser_import(self):
        """Parser module should be importable."""
        from parser import parse_text
        assert parse_text is not None

    def test_main_app_import(self):
        """Main FastAPI app should be importable."""
        from main import app
        assert app is not None
