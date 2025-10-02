"""
Tests for the health endpoint.
"""

import asyncio
import pytest
from datetime import datetime
from app.main import health_check, perform_health_checks


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_returns_ok_status(self):
        """Test that health check returns 'ok' status."""
        response = await health_check()

        assert response["status"] == "ok"
        assert "timestamp" in response
        assert "service" in response
        assert "version" in response
        assert "checks" in response
        assert "response_time_ms" in response

    @pytest.mark.asyncio 
    async def test_health_check_response_structure(self):
        """Test the structure of the health check response."""
        response = await health_check()

        # Check required fields
        required_fields = ["status", "timestamp", "service", "version", "checks", "response_time_ms"]
        for field in required_fields:
            assert field in response, f"Missing required field: {field}"

        # Check data types
        assert isinstance(response["status"], str)
        assert isinstance(response["timestamp"], str)
        assert isinstance(response["service"], str)
        assert isinstance(response["version"], str)
        assert isinstance(response["checks"], dict)
        assert isinstance(response["response_time_ms"], (int, float))

        # Verify timestamp format
        datetime.fromisoformat(response["timestamp"].replace('Z', '+00:00'))

    @pytest.mark.asyncio
    async def test_perform_health_checks(self):
        """Test the perform_health_checks function."""
        checks = await perform_health_checks()

        assert isinstance(checks, dict)
        assert "application" in checks
        assert "system" in checks
        assert checks["application"]["status"] == "healthy"
        assert checks["system"]["status"] == "healthy"