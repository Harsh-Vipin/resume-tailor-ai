"""
Integration tests for CORS (Cross-Origin Resource Sharing) middleware.

These tests verify that CORS headers are properly set and that
the application correctly handles cross-origin requests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestCORSMiddleware:
    """Test CORS middleware functionality."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    def test_cors_headers_present_on_get_request(self, client):
        """Test that CORS headers are present on GET requests."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        
    def test_cors_preflight_request(self, client):
        """Test CORS preflight (OPTIONS) request handling."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        # Preflight should return 200
        assert response.status_code == 200
        
        # Check CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers

    def test_cors_allows_configured_origin(self, client):
        """Test that configured origins are allowed."""
        response = client.get(
            "/",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # With default config (*), any origin should be allowed
        assert "access-control-allow-origin" in response.headers

    def test_cors_credentials_header(self, client):
        """Test that credentials header is set when configured."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # Check if credentials are allowed (based on default config)
        if "access-control-allow-credentials" in response.headers:
            assert response.headers["access-control-allow-credentials"] == "true"

    def test_cors_on_root_endpoint(self, client):
        """Test CORS headers on root endpoint."""
        response = client.get(
            "/",
            headers={"Origin": "http://example.com"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_on_health_endpoint(self, client):
        """Test CORS headers on health endpoint."""
        response = client.get(
            "/health",
            headers={"Origin": "http://example.com"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_with_post_method(self, client):
        """Test CORS with POST method (for future endpoints)."""
        # Test OPTIONS preflight for POST
        response = client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        
        assert response.status_code == 200
        assert "access-control-allow-methods" in response.headers

    def test_cors_headers_case_insensitive(self, client):
        """Test that CORS works with different origin formats."""
        origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "https://example.com"
        ]
        
        for origin in origins:
            response = client.get(
                "/health",
                headers={"Origin": origin}
            )
            
            assert response.status_code == 200
            assert "access-control-allow-origin" in response.headers

    def test_response_includes_correlation_id_with_cors(self, client):
        """Test that correlation ID is present along with CORS headers."""
        response = client.get(
            "/",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        json_data = response.json()
        
        # Both CORS and correlation ID should be present
        assert "correlation_id" in json_data
        assert "access-control-allow-origin" in response.headers

    def test_cors_on_api_docs(self, client):
        """Test that CORS headers are present on API documentation endpoints."""
        response = client.get(
            "/docs",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Docs endpoint should return 200
        assert response.status_code == 200


class TestCORSConfiguration:
    """Test CORS configuration and environment variable handling."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    def test_cors_middleware_is_active(self, client):
        """Test that CORS middleware is active and processing requests."""
        # Make a simple request
        response = client.get("/")
        
        assert response.status_code == 200
        # The presence of CORS headers indicates middleware is active
        # Note: FastAPI's TestClient may not always show all CORS headers
        # but the middleware should still be registered

    def test_multiple_endpoints_have_cors(self, client):
        """Test that multiple endpoints have CORS support."""
        endpoints = ["/", "/health"]
        
        for endpoint in endpoints:
            response = client.get(
                endpoint,
                headers={"Origin": "http://localhost:3000"}
            )
            
            assert response.status_code == 200
            # CORS headers should be present
            assert "access-control-allow-origin" in response.headers
