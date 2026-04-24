"""
Tests for audit endpoint - verify it's disabled.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_audit_endpoint_disabled():
    """Verify audit endpoint is disabled and returns 501."""
    response = client.get("/audit/1")
    assert response.status_code == 501
    assert "disabled" in response.json()["detail"].lower()
    assert "sputnikmusic" in response.json()["detail"].lower()


def test_audit_endpoint_returns_clear_error_message():
    """Verify error message clearly states no external connections allowed."""
    response = client.get("/audit/999")
    assert response.status_code == 501
    detail = response.json()["detail"]
    assert "Audit functionality is disabled" in detail
    assert "No external connections" in detail
    assert "Sputnikmusic" in detail
