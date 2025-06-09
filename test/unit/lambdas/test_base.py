import typing
import pytest
import aws_lambda_typing.context as context_
import aws_lambda_typing.events
import khc.lambdas.base


def test_cannot_instantiate_abstract_base_class():
    """Test that LambdaFunction cannot be instantiated directly."""
    with pytest.raises(TypeError) as excinfo:
        khc.lambdas.base.LambdaFunction()
    assert "Can't instantiate abstract class LambdaFunction" in str(excinfo.value)


class TestImplementation(khc.lambdas.base.LambdaFunction):
    """Concrete implementation for testing."""

    def handler(
        self,
        event: aws_lambda_typing.events.APIGatewayProxyEventV2,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        return {"success": True, "event": event, "context": str(context)}


class TestLambdaFunction:
    """Test suite for LambdaFunction class."""

    def test_can_instantiate_concrete_implementation(self):
        """Test that concrete implementation can be instantiated."""
        implementation = TestImplementation()
        assert isinstance(implementation, khc.lambdas.base.LambdaFunction)

    def test_concrete_implementation_handles_event(self):
        """Test that concrete implementation can handle events."""
        implementation = TestImplementation()

        # Properly typed event
        mock_event: aws_lambda_typing.events.APIGatewayProxyEventV2 = {
            "version": "2.0",
            "routeKey": "ANY /path",
            "rawPath": "/path",
            "rawQueryString": "",
            "headers": {},
            "cookies": [],
            "queryStringParameters": {},
            "pathParameters": {},
            "stageVariables": {},
            "body": "",
            "isBase64Encoded": False,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "api-id",
                "domainName": "id.execute-api.us-east-1.amazonaws.com",
                "domainPrefix": "id",
                "http": {
                    "method": "GET",
                    "path": "/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "IP",
                    "userAgent": "agent",
                },
                "requestId": "id",
                "routeKey": "ANY /path",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
        }

        # Cast the mock context to the correct type
        mock_context = typing.cast(
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

        result = implementation.handler(mock_event, mock_context)

        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["event"] == mock_event
        assert isinstance(result["context"], str)

    def test_concrete_implementation_maintains_contract(self):
        """Test that concrete implementation maintains the type contract."""
        implementation = TestImplementation()
        # Get type hints of the handler method
        handler_hints = typing.get_type_hints(implementation.handler)

        assert handler_hints["event"] == aws_lambda_typing.events.APIGatewayProxyEventV2
        assert handler_hints["context"] == context_.Context
        assert handler_hints["return"] == dict[str, typing.Any]
