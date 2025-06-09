import typing
import pytest
import aws_lambda_typing.context as context_
import aws_lambda_typing.events
import khc.base._lambda
import khc.base.event
import khc.events.alexa


def test_cannot_instantiate_abstract_base_class():
    """Test that LambdaFunction cannot be instantiated directly."""
    with pytest.raises(TypeError) as excinfo:
        khc.base._lambda.LambdaFunction()
    assert "Can't instantiate abstract class LambdaFunction" in str(excinfo.value)


class TestImplementation(khc.base._lambda.LambdaFunction):
    """Concrete implementation for testing."""

    def handler(
        self,
        event: khc.base.event.BaseEvent,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        return {"success": True, "event": event, "context": str(context)}


class TestLambdaFunction:
    """Test suite for LambdaFunction class."""

    def test_can_instantiate_concrete_implementation(self):
        """Test that concrete implementation can be instantiated."""
        implementation = TestImplementation()
        assert isinstance(implementation, khc.base._lambda.LambdaFunction)

    def test_concrete_implementation_handles_api_gateway_event(self):
        """Test that implementation can handle API Gateway events."""
        implementation = TestImplementation()

        # API Gateway event
        api_event = typing.cast(
            aws_lambda_typing.events.APIGatewayProxyEventV2,
            {
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
            },
        )

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

        result = implementation.handler(api_event, mock_context)

        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["event"] == api_event
        assert isinstance(result["context"], str)

    def test_concrete_implementation_handles_alexa_event(self):
        """Test that implementation can handle Alexa events."""
        implementation = TestImplementation()

        # Alexa event
        alexa_event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                "version": "1.0",
                "session": {},
                "request": {"type": "LaunchRequest"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "requestContext": {"requestId": "test-id"},
                "isBase64Encoded": False,
            },
        )

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

        result = implementation.handler(alexa_event, mock_context)

        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["event"] == alexa_event
        assert isinstance(result["context"], str)

    def test_concrete_implementation_maintains_contract(self):
        """Test that concrete implementation maintains the type contract."""
        implementation = TestImplementation()
        # Get type hints of the handler method
        handler_hints = typing.get_type_hints(implementation.handler)

        assert handler_hints["event"] == khc.base.event.BaseEvent
        assert handler_hints["context"] == context_.Context
        assert handler_hints["return"] == dict[str, typing.Any]
