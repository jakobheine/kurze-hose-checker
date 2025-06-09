import typing
import pytest
import aws_lambda_typing.context as context_
import khc.lambdas.alexa_adapter
import khc.events.alexa
import khc.base._lambda
import khc.base.event


class MockKHCLambda(khc.base._lambda.LambdaFunction):
    """Mock implementation of the KHC Lambda."""

    def handler(
        self,
        event: khc.base.event.BaseEvent,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        return {"message": "Mock KHC Response"}


class TestAlexaAdapter:
    """Test suite for AlexaAdapter."""

    @pytest.fixture
    def mock_event(self) -> khc.events.alexa.AlexaEvent:
        """Provide a mock Alexa event."""
        return typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                "version": "1.0",
                "session": {
                    "new": True,
                    "sessionId": "test-session-id",
                    "application": {"applicationId": "test-app-id"},
                    "user": {"userId": "test-user-id"},
                },
                "request": {
                    "type": "IntentRequest",
                    "requestId": "test-request-id",
                    "timestamp": "2024-04-09T12:00:00Z",
                    "locale": "de-DE",
                    "intent": {"name": "CheckShortsIntent"},
                },
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "requestContext": {
                    "accountId": "123456789012",
                    "apiId": "api-id",
                    "domainName": "id.execute-api.us-east-1.amazonaws.com",
                    "domainPrefix": "id",
                    "http": {
                        "method": "POST",
                        "path": "/alexa",
                        "protocol": "HTTP/1.1",
                        "sourceIp": "IP",
                        "userAgent": "agent",
                    },
                    "requestId": "id",
                    "routeKey": "ANY /alexa",
                    "stage": "$default",
                    "time": "12/Mar/2020:19:03:58 +0000",
                    "timeEpoch": 1583348638390,
                },
                "isBase64Encoded": False,
            },
        )

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

    @pytest.fixture
    def adapter(self) -> khc.base._lambda.LambdaFunction:
        """Provide an AlexaAdapter instance with mock KHC Lambda."""
        mock_khc = MockKHCLambda()
        return khc.lambdas.alexa_adapter.AlexaAdapter(mock_khc)

    def test_initialization(self):
        """Test that adapter is properly initialized with KHC Lambda."""
        mock_khc = MockKHCLambda()
        adapter = khc.lambdas.alexa_adapter.AlexaAdapter(mock_khc)

        assert adapter.khc_lambda == mock_khc

    def test_handler_returns_correct_structure(self, adapter, mock_event, mock_context):
        """Test that handler returns correctly structured response."""
        response = adapter.handler(mock_event, mock_context)

        assert isinstance(response, dict)
        assert response["version"] == "1.0"
        assert "response" in response
        assert "statusCode" in response
        assert response["statusCode"] == 200

    def test_response_contains_output_speech(self, adapter, mock_event, mock_context):
        """Test that response contains proper output speech structure."""
        response = adapter.handler(mock_event, mock_context)

        assert "outputSpeech" in response["response"]
        assert response["response"]["outputSpeech"]["type"] == "PlainText"
        assert isinstance(response["response"]["outputSpeech"]["text"], str)
        assert (
            "Hello World from Alexa Adapter"
            in response["response"]["outputSpeech"]["text"]
        )

    def test_response_includes_session_end(self, adapter, mock_event, mock_context):
        """Test that response correctly sets session end."""
        response = adapter.handler(mock_event, mock_context)

        assert "shouldEndSession" in response["response"]
        assert response["response"]["shouldEndSession"] is True

    def test_handles_different_event_types(self, adapter, mock_context):
        """Test that adapter handles different Alexa event types."""
        launch_event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                "version": "1.0",
                "session": {},
                "request": {
                    "type": "LaunchRequest",
                    "requestId": "test-request-id",
                    "timestamp": "2024-04-09T12:00:00Z",
                    "locale": "de-DE",
                },
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "requestContext": {
                    "accountId": "123456789012",
                    "apiId": "api-id",
                    "domainName": "id.execute-api.us-east-1.amazonaws.com",
                    "domainPrefix": "id",
                    "http": {
                        "method": "POST",
                        "path": "/alexa",
                        "protocol": "HTTP/1.1",
                        "sourceIp": "IP",
                        "userAgent": "agent",
                    },
                    "requestId": "id",
                    "routeKey": "ANY /alexa",
                    "stage": "$default",
                    "time": "12/Mar/2020:19:03:58 +0000",
                    "timeEpoch": 1583348638390,
                },
                "isBase64Encoded": False,
            },
        )

        response = adapter.handler(launch_event, mock_context)

        assert response["statusCode"] == 200
        assert "response" in response
        assert "outputSpeech" in response["response"]

    def test_response_type_hints(self, adapter, mock_event, mock_context):
        """Test that handler maintains correct return type hints."""
        hints = typing.get_type_hints(adapter.handler)

        assert hints["return"] == dict[str, typing.Any]
        assert hints["event"] == khc.events.alexa.AlexaEvent
        assert hints["context"] == context_.Context

    def test_minimal_event_handling(self, adapter, mock_context):
        """Test that adapter can handle minimal valid event structure."""
        minimal_event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                "version": "1.0",
                "session": {},
                "request": {"type": "IntentRequest"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "requestContext": {
                    "accountId": "123456789012",
                    "apiId": "api-id",
                    "domainName": "id.execute-api.us-east-1.amazonaws.com",
                    "domainPrefix": "id",
                    "http": {
                        "method": "POST",
                        "path": "/alexa",
                        "protocol": "HTTP/1.1",
                        "sourceIp": "IP",
                        "userAgent": "agent",
                    },
                    "requestId": "id",
                    "routeKey": "ANY /alexa",
                    "stage": "$default",
                    "time": "12/Mar/2020:19:03:58 +0000",
                    "timeEpoch": 1583348638390,
                },
                "isBase64Encoded": False,
            },
        )

        response = adapter.handler(minimal_event, mock_context)

        assert response["statusCode"] == 200
        assert "response" in response
        assert "outputSpeech" in response["response"]
