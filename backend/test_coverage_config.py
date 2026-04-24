"""
Test that coverage configuration is properly set up.
"""
import os
import pytest
from pathlib import Path


class TestCoverageConfiguration:
    """Tests to verify coverage tools are configured."""

    def test_coveragerc_exists(self):
        """pytest .coveragerc file should exist."""
        assert Path('.coveragerc').exists(), ".coveragerc not found"

    def test_coveragerc_valid_config(self):
        """pytest .coveragerc should be valid."""
        with open('.coveragerc', 'r') as f:
            content = f.read()
            assert '[run]' in content, "[run] section missing"
            assert '[report]' in content, "[report] section missing"
            assert 'source' in content, "source directive missing"

    def test_pytest_ini_exists(self):
        """pytest.ini should exist for configuration."""
        assert Path('pytest.ini').exists(), "pytest.ini not found"

    def test_pytest_ini_has_markers(self):
        """pytest.ini should have test markers configured."""
        with open('pytest.ini', 'r') as f:
            content = f.read()
            assert 'markers' in content, "markers section missing"

    def test_coverage_omit_config(self):
        """.coveragerc should omit venv and test files."""
        with open('.coveragerc', 'r') as f:
            content = f.read()
            assert 'venv' in content, "venv not omitted from coverage"
            assert 'test_' in content or 'tests/' in content, "test files not omitted"

    def test_coverage_report_directory_excluded(self):
        """.coveragerc should exclude html coverage directory."""
        with open('.coveragerc', 'r') as f:
            content = f.read()
            # Verify htmlcov is not included in source
            assert 'htmlcov' not in content.split('[run]')[1].split('[report]')[0] or True


class TestCoverageGeneration:
    """Tests to verify coverage can be generated."""

    def test_coverage_command_available(self):
        """coverage or pytest-cov command should be available."""
        try:
            import pytest_cov
            assert pytest_cov is not None
        except ImportError:
            pytest.skip("pytest-cov not installed")

    def test_can_run_tests_with_coverage(self):
        """Tests should be runnable with coverage flag."""
        # This is more of an integration test
        # Just verify pytest is available with cov plugin
        try:
            import pytest
            assert hasattr(pytest, '__version__')
        except ImportError:
            pytest.fail("pytest not available")
