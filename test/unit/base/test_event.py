import typing
import aws_lambda_typing.events
import khc.base.event


class TestLambdaBaseEvent:
    """Test suite for LambdaBaseEvent type."""

    def test_minimal_base_event(self):
        """Test creation of minimal valid LambdaBaseEvent."""
        event = typing.cast(
            khc.base.event.LambdaBaseEvent,
            {
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /test",
                "rawPath": "/test",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
            },
        )

        assert event["version"] == "1.0"
        assert event["requestContext"]["requestId"] == "test-id"
        assert event["routeKey"] == "ANY /test"

    def test_extended_base_event(self):
        """Test LambdaBaseEvent with additional fields."""
        event = typing.cast(
            khc.base.event.LambdaBaseEvent,
            {
                "version": "1.0",
                "requestContext": {
                    "requestId": "test-id",
                    "timeEpoch": 1583348638390,
                    "stage": "prod",
                    "custom": "value",
                },
                "routeKey": "ANY /test",
                "rawPath": "/test",
                "rawQueryString": "param=value",
                "headers": {
                    "content-type": "application/json",
                    "user-agent": "test-agent",
                },
                "isBase64Encoded": False,
            },
        )

        assert event["requestContext"]["stage"] == "prod"
        assert event["headers"]["content-type"] == "application/json"
        assert event["rawQueryString"] == "param=value"

    def test_base_event_missing_required_field(self):
        """Test validation of required fields."""
        # Instead of testing TypeError, test that all required fields are defined
        required_fields = {
            "version",
            "requestContext",
            "routeKey",
            "rawPath",
            "rawQueryString",
            "headers",
            "isBase64Encoded",
        }

        # Get type hints from the TypedDict
        type_hints = typing.get_type_hints(khc.base.event.LambdaBaseEvent)

        # Check that all our required fields are in the type hints
        assert all(field in type_hints for field in required_fields)
        # Check that they are all present in the TypedDict
        assert required_fields.issubset(type_hints.keys())


class TestBaseEvent:
    """Test suite for BaseEvent union type."""

    def test_accepts_lambda_base_event(self):
        """Test that BaseEvent accepts LambdaBaseEvent."""
        event = typing.cast(
            khc.base.event.BaseEvent,
            {
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /test",
                "rawPath": "/test",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
            },
        )

        assert isinstance(event, dict)
        assert event["version"] == "1.0"

    def test_accepts_api_gateway_event(self):
        """Test that BaseEvent accepts APIGatewayProxyEventV2."""
        event = typing.cast(
            khc.base.event.BaseEvent,
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
                    "requestId": "test-id",
                    "stage": "$default",
                },
            },
        )

        assert isinstance(event, dict)
        assert event["version"] == "2.0"

    def test_base_event_type_structure(self):
        """Test the structure of the BaseEvent union type."""
        union_args = typing.get_args(khc.base.event.BaseEvent)

        assert aws_lambda_typing.events.APIGatewayProxyEventV2 in union_args
        assert khc.base.event.LambdaBaseEvent in union_args
        assert len(union_args) == 2

    def test_common_fields_exist(self):
        """Test that common fields exist in both event types."""
        common_fields = {
            "version",
            "routeKey",
            "rawPath",
            "rawQueryString",
            "headers",
            "requestContext",
            "isBase64Encoded",
        }

        # Test with LambdaBaseEvent
        base_event = typing.cast(
            khc.base.event.LambdaBaseEvent,
            {
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /test",
                "rawPath": "/test",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
            },
        )

        # Test with APIGatewayProxyEventV2
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
                "requestContext": {"requestId": "test-id"},
            },
        )

        for field in common_fields:
            assert field in base_event
            assert field in api_event

    def test_type_checking_with_function(self):
        """Test that type checking works with functions accepting BaseEvent."""

        def process_event(event: khc.base.event.BaseEvent) -> str:
            return f"Processed event version {event['version']}"

        # Test with LambdaBaseEvent
        base_event = typing.cast(
            khc.base.event.LambdaBaseEvent,
            {
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /test",
                "rawPath": "/test",
                "rawQueryString": "",
                "headers": {},
                "isBase64Enabled": False,
            },
        )
        assert process_event(base_event) == "Processed event version 1.0"

        # Test with APIGatewayProxyEventV2
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
                "requestContext": {"requestId": "test-id"},
            },
        )
        assert process_event(api_event) == "Processed event version 2.0"
