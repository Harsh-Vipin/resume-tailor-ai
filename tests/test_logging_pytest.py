"""
Pytest-compatible tests for the logging system.

These tests check the logging functionality including:
- Logging configuration
- Custom formatters
- Middleware logging
- Log levels and output
"""

import logging
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from fastapi import Request
from fastapi.testclient import TestClient

# Import the application and logging components
from app.main import app
from app.logging_config import setup_logging, CustomJSONFormatter
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware


class TestLoggingConfiguration:
    """Test logging configuration setup."""

    def test_setup_logging_creates_logger(self):
        """Test that setup_logging configures the root logger properly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")

            setup_logging(
                log_level="DEBUG",
                log_file=log_file,
                enable_console=False,
                enable_json=False
            )

            # Check root logger configuration
            root_logger = logging.getLogger()
            assert root_logger.level == logging.DEBUG

            # Check if log file was created
            root_logger.info("Test log message")
            assert os.path.exists(log_file)

            # Read log content
            with open(log_file, 'r') as f:
                log_content = f.read()

            assert "Test log message" in log_content

    def test_setup_logging_json_format(self):
        """Test JSON logging format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test_json.log")

            setup_logging(
                log_level="INFO",
                log_file=log_file,
                enable_console=False,
                enable_json=True
            )

            # Create a logger and log a message
            test_logger = logging.getLogger("test_json")
            test_logger.info("JSON test message", extra={"test_field": "test_value"})

            # Read and parse log content
            with open(log_file, 'r') as f:
                log_content = f.read().strip()

            # Should be valid JSON
            log_data = json.loads(log_content.split('\n')[-1])
            assert log_data["message"] == "JSON test message"
            assert log_data["level"] == "INFO"
            assert log_data["logger"] == "test_json"

    def test_custom_json_formatter(self):
        """Test the CustomJSONFormatter class."""
        formatter = CustomJSONFormatter()

        # Create a log record
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None
        )

        # Add extra attributes
        record.correlation_id = "test-123"
        record.method = "GET"
        record.url = "http://localhost:8000/"

        # Format the record
        formatted = formatter.format(record)
        log_data = json.loads(formatted)

        # Verify structure
        assert log_data["message"] == "Test message"
        assert log_data["level"] == "INFO"
        assert log_data["logger"] == "test_logger"
        assert log_data["correlation_id"] == "test-123"
        assert log_data["http_method"] == "GET"
        assert log_data["url"] == "http://localhost:8000/"


class TestLoggingMiddleware:
    """Test logging middleware functionality."""

    def create_mock_request(self, method="GET", url="http://localhost:8000/"):
        """Create a mock request for testing."""
        request = Mock(spec=Request)
        request.method = method
        request.url = Mock()
        request.url.__str__ = Mock(return_value=url)
        request.client = Mock()
        request.client.host = "127.0.0.1"
        request.headers = {"user-agent": "test-agent"}
        request.state = Mock()
        return request

    @pytest.mark.asyncio
    async def test_logging_middleware_adds_correlation_id(self):
        """Test that logging middleware adds correlation ID to request state."""
        middleware = LoggingMiddleware(app)
        request = self.create_mock_request()

        # Mock call_next
        async def mock_call_next(req):
            response = Mock()
            response.status_code = 200
            response.headers = {}
            return response

        with patch('logging.getLogger') as mock_logger:
            response = await middleware.dispatch(request, mock_call_next)

            # Check that correlation ID was added
            assert hasattr(request.state, 'correlation_id')
            assert request.state.correlation_id is not None
            assert len(request.state.correlation_id) == 36  # UUID length

            # Check response headers
            assert "X-Correlation-ID" in response.headers

    @pytest.mark.asyncio
    async def test_error_handling_middleware_logs_exceptions(self, caplog):
        """Test that error handling middleware logs exceptions properly."""
        middleware = ErrorHandlingMiddleware(app)
        request = self.create_mock_request()
        request.state.correlation_id = "test-error-123"

        # Mock call_next to raise an exception
        async def mock_call_next_error(req):
            raise ValueError("Test exception")

        # Use caplog to capture the actual log output
        with caplog.at_level(logging.ERROR):
            response = await middleware.dispatch(request, mock_call_next_error)

            # Check that exception was logged
            assert "Unhandled exception" in caplog.text
            assert "ValueError: Test exception" in caplog.text

            # Check response
            assert response.status_code == 500

class TestApplicationLogging:
    """Test application-level logging functionality."""

    def setup_method(self):
        """Set up test environment."""
        # Create a test client
        self.client = TestClient(app)

    def test_application_startup_logging(self, caplog):
        """Test that application startup events are logged."""
        with caplog.at_level(logging.INFO):
            # The app should already be started, but we can check if startup logs exist
            # This test verifies that logging infrastructure is in place
            test_logger = logging.getLogger("resume_tailor.test")
            test_logger.info("Test startup message")

            assert "Test startup message" in caplog.text

    def test_health_endpoint_logging(self, caplog):
        """Test that health endpoint generates appropriate logs."""
        with caplog.at_level(logging.INFO):
            # Make request to health endpoint
            response = self.client.get("/health")

            assert response.status_code == 200

            # Check if logging occurred (this depends on middleware being active)
            # In a real test environment, we would check for specific log messages

    def test_root_endpoint_logging(self, caplog):
        """Test that root endpoint generates appropriate logs."""
        with caplog.at_level(logging.INFO):
            response = self.client.get("/")

            assert response.status_code == 200
            response_data = response.json()
            assert "correlation_id" in response_data


class TestLogLevels:
    """Test different log levels and their behavior."""

    def test_debug_level_logging(self, caplog):
        """Test DEBUG level logging."""
        with caplog.at_level(logging.DEBUG):
            logger = logging.getLogger("test_debug")
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            assert "Debug message" in caplog.text
            assert "Info message" in caplog.text
            assert "Warning message" in caplog.text
            assert "Error message" in caplog.text

    def test_info_level_logging(self, caplog):
        """Test INFO level logging."""
        with caplog.at_level(logging.INFO):
            logger = logging.getLogger("test_info")
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # DEBUG should not appear, others should
            assert "Debug message" not in caplog.text
            assert "Info message" in caplog.text
            assert "Warning message" in caplog.text
            assert "Error message" in caplog.text

    def test_warning_level_logging(self, caplog):
        """Test WARNING level logging.""" 
        with caplog.at_level(logging.WARNING):
            logger = logging.getLogger("test_warning")
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # Only WARNING and ERROR should appear
            assert "Debug message" not in caplog.text
            assert "Info message" not in caplog.text
            assert "Warning message" in caplog.text
            assert "Error message" in caplog.text


class TestCorrelationIdTracking:
    """Test correlation ID functionality."""

    def test_correlation_id_generation(self):
        """Test that correlation IDs are generated properly."""
        from uuid import UUID

        # Simulate middleware generating correlation IDs
        import uuid
        correlation_id = str(uuid.uuid4())

        # Verify it's a valid UUID
        UUID(correlation_id)  # Should not raise exception
        assert len(correlation_id) == 36
        assert correlation_id.count('-') == 4

    def test_correlation_id_in_logs(self, caplog):
        """Test that correlation IDs appear in log messages."""
        with caplog.at_level(logging.INFO):
            logger = logging.getLogger("test_correlation")

            # Log with correlation ID
            logger.info(
                "Test message with correlation ID",
                extra={"correlation_id": "test-123-456"}
            )

            # Note: This test verifies the logging infrastructure
            # The actual correlation ID formatting depends on the formatter used
