"""
Integration tests for the health endpoint via HTTP.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestHealthEndpointIntegration:
    """Integration test cases for the health endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    def test_health_endpoint_returns_200(self, client):
        """Test that the health endpoint returns HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self, client):
        """Test that the health endpoint returns valid JSON."""
        response = client.get("/health")

        assert response.status_code == 200
        json_response = response.json()

        # Verify JSON structure
        assert isinstance(json_response, dict)
        assert json_response["status"] == "ok"

    def test_health_endpoint_response_content(self, client):
        """Test the content of the health endpoint response."""
        response = client.get("/health")
        json_response = response.json()

        # Check all expected fields are present
        expected_fields = ["status", "timestamp", "service", "version", "checks", "response_time_ms"]
        for field in expected_fields:
            assert field in json_response, f"Missing field: {field}"

        # Check specific values
        assert json_response["status"] == "ok"
        assert json_response["service"] == "Resume Tailor AI"
        assert json_response["version"] == "0.1.0"

        # Check checks structure
        assert isinstance(json_response["checks"], dict)
        assert "application" in json_response["checks"]
        assert "system" in json_response["checks"]