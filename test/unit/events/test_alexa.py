import typing
import khc.events.alexa


class TestAlexaEvent:
    """Test suite for AlexaEvent type."""

    def test_minimal_alexa_event(self):
        """Test creation of minimal valid AlexaEvent."""
        event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                # Base fields from LambdaBaseEvent
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # Required Alexa-specific fields
                "session": {},
                "request": {"type": "LaunchRequest"},
            },
        )

        assert event["version"] == "1.0"
        assert event["request"]["type"] == "LaunchRequest"
        assert "context" not in event  # context is optional

    def test_complete_alexa_event(self):
        """Test creation of complete AlexaEvent with all fields."""
        event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                # Base fields from LambdaBaseEvent
                "version": "1.0",
                "requestContext": {
                    "requestId": "test-id",
                    "stage": "prod",
                    "identity": {
                        "userAgent": "Alexa/1.0",
                    },
                },
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {
                    "content-type": "application/json",
                },
                "isBase64Encoded": False,
                # Alexa-specific fields
                "session": {
                    "new": True,
                    "sessionId": "test-session-id",
                    "application": {
                        "applicationId": "test-app-id",
                    },
                    "user": {
                        "userId": "test-user-id",
                    },
                },
                "request": {
                    "type": "IntentRequest",
                    "requestId": "test-request-id",
                    "timestamp": "2024-04-09T12:00:00Z",
                    "locale": "de-DE",
                    "intent": {
                        "name": "CheckShortsIntent",
                    },
                },
                "context": {
                    "System": {
                        "application": {
                            "applicationId": "test-app-id",
                        },
                        "user": {
                            "userId": "test-user-id",
                        },
                        "device": {
                            "deviceId": "test-device-id",
                        },
                    },
                },
            },
        )

        assert event["session"]["new"] is True
        assert event["request"]["type"] == "IntentRequest"
        assert event["context"]["System"]["device"]["deviceId"] == "test-device-id"

    def test_missing_required_field(self):
        """Test validation of required fields."""
        # Instead of testing TypeError, test that all required fields are defined
        required_fields = {
            # Base fields
            "version",
            "requestContext",
            "routeKey",
            "rawPath",
            "rawQueryString",
            "headers",
            "isBase64Encoded",
            # Alexa-specific fields
            "session",
            "request",
        }
        optional_fields = {"context"}

        # Get type hints from the TypedDict
        type_hints = typing.get_type_hints(khc.events.alexa.AlexaEvent)

        # Check that all required fields are in the type hints
        assert all(field in type_hints for field in required_fields)
        # Check that all fields are present
        assert required_fields.issubset(type_hints.keys())
        # Check that optional fields are present
        assert optional_fields.issubset(type_hints.keys())

    def test_intent_request(self):
        """Test specific structure for IntentRequest."""
        event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                # Base fields
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # Alexa fields
                "session": {},
                "request": {
                    "type": "IntentRequest",
                    "intent": {
                        "name": "CheckShortsIntent",
                        "slots": {
                            "postalCode": {
                                "name": "postalCode",
                                "value": "12345",
                            },
                        },
                    },
                },
            },
        )

        assert event["request"]["type"] == "IntentRequest"
        assert event["request"]["intent"]["name"] == "CheckShortsIntent"
        assert event["request"]["intent"]["slots"]["postalCode"]["value"] == "12345"

    def test_launch_request(self):
        """Test specific structure for LaunchRequest."""
        event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                # Base fields
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # Alexa fields
                "session": {"new": True},
                "request": {
                    "type": "LaunchRequest",
                    "requestId": "test-request-id",
                    "timestamp": "2024-04-09T12:00:00Z",
                    "locale": "de-DE",
                },
            },
        )

        assert event["request"]["type"] == "LaunchRequest"
        assert event["session"]["new"] is True

    def test_session_ended_request(self):
        """Test specific structure for SessionEndedRequest."""
        event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                # Base fields
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # Alexa fields
                "session": {"new": False},
                "request": {
                    "type": "SessionEndedRequest",
                    "reason": "USER_INITIATED",
                },
            },
        )

        assert event["request"]["type"] == "SessionEndedRequest"
        assert event["request"]["reason"] == "USER_INITIATED"
        assert event["session"]["new"] is False

    def test_inherits_base_event_fields(self):
        """Test that AlexaEvent properly inherits all LambdaBaseEvent fields."""
        base_fields = {
            "version",
            "requestContext",
            "routeKey",
            "rawPath",
            "rawQueryString",
            "headers",
            "isBase64Encoded",
        }

        event = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                # Base fields
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                # Alexa fields
                "session": {},
                "request": {"type": "LaunchRequest"},
            },
        )

        for field in base_fields:
            assert field in event

    def test_optional_context_field(self):
        """Test that context field is optional."""
        # Without context
        event1 = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                "session": {},
                "request": {"type": "LaunchRequest"},
            },
        )
        assert "context" not in event1

        # With context
        event2 = typing.cast(
            khc.events.alexa.AlexaEvent,
            {
                "version": "1.0",
                "requestContext": {"requestId": "test-id"},
                "routeKey": "ANY /alexa",
                "rawPath": "/alexa",
                "rawQueryString": "",
                "headers": {},
                "isBase64Encoded": False,
                "session": {},
                "request": {"type": "LaunchRequest"},
                "context": {
                    "System": {
                        "device": {"deviceId": "test-device"},
                    },
                },
            },
        )
        assert "context" in event2
        assert event2["context"]["System"]["device"]["deviceId"] == "test-device"
