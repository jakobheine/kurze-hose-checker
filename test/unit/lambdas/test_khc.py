import typing
import pytest
import aws_lambda_typing.context as context_
import khc.events.khc
import khc.lambdas.khc


class TestKHCLambda:
    """Test suite for KHC Lambda."""

    @pytest.fixture
    def lambda_function(self) -> khc.lambdas.khc.KHCLambda:
        """Provide a KHCLambda instance."""
        return khc.lambdas.khc.KHCLambda()

    @pytest.fixture
    def mock_context(self) -> context_.Context:
        """Provide a mock Lambda context."""
        return typing.cast(
            context_.Context,
            {
                "function_name": "test",
                "function_version": "1",
                "invoked_function_arn": "arn:test",
                "memory_limit_in_mb": 128,
                "aws_request_id": "test-id",
                "log_group_name": "test-group",
                "log_stream_name": "test-stream",
            },
        )

    def test_handles_valid_request(self, lambda_function, mock_context):
        """Test handling of valid request."""
        event = typing.cast(
            khc.events.khc.KHCEvent,
            {
                # Base fields
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /khc",
                "rawPath": "/khc",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # KHC-specific fields
                "postal_code": "12345",
                "use_ai": True,
            },
        )

        response = lambda_function.handler(event, mock_context)

        assert response["statusCode"] == 200
        assert response["postal_code"] == "12345"
        assert response["use_ai"] is True

    def test_rejects_invalid_postal_code(self, lambda_function, mock_context):
        """Test rejection of invalid postal code."""
        event = typing.cast(
            khc.events.khc.KHCEvent,
            {
                # Base fields
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /khc",
                "rawPath": "/khc",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # KHC-specific fields with invalid postal code
                "postal_code": "1234",  # Too short
                "use_ai": True,
            },
        )

        response = lambda_function.handler(event, mock_context)

        assert response["statusCode"] == 400
        assert "Invalid postal code" in response["message"]
