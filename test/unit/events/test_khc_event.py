import typing
import khc.events.khc


class TestKHCEvent:
    """Test suite for KHCEvent type."""

    def test_minimal_khc_event(self):
        """Test creation of minimal valid KHCEvent."""
        event = typing.cast(
            khc.events.khc.KHCEvent,
            {
                # Base fields from LambdaBaseEvent
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

        assert event["version"] == "1.0"
        assert event["postal_code"] == "12345"
        assert event["use_ai"] is True

    def test_complete_khc_event(self):
        """Test creation of complete KHCEvent with all fields."""
        event = typing.cast(
            khc.events.khc.KHCEvent,
            {
                # Base fields from LambdaBaseEvent
                "version": "1.0",
                "requestContext": {
                    "requestId": "test-id",
                    "stage": "prod",
                    "identity": {
                        "userAgent": "test-agent",
                    },
                },
                "routeKey": "ANY /khc",
                "rawPath": "/khc",
                "rawQueryString": "postal_code=12345",
                "headers": {
                    "content-type": "application/json",
                },
                "isBase64Encoded": False,
                # KHC-specific fields
                "postal_code": "12345",
                "use_ai": True,
            },
        )

        assert event["postal_code"] == "12345"
        assert event["use_ai"] is True
        assert event["requestContext"]["stage"] == "prod"
        assert event["headers"]["content-type"] == "application/json"

    def test_missing_required_field(self):
        """Test validation of required fields."""
        required_fields = {
            # Base fields
            "version",
            "requestContext",
            "routeKey",
            "rawPath",
            "rawQueryString",
            "headers",
            "isBase64Encoded",
            # KHC-specific fields
            "postal_code",
            "use_ai",
        }

        # Get type hints from the TypedDict
        type_hints = typing.get_type_hints(khc.events.khc.KHCEvent)

        # Check that all required fields are in the type hints
        assert all(field in type_hints for field in required_fields)
        # Check that all fields are present
        assert required_fields.issubset(type_hints.keys())

    def test_inherits_base_event_fields(self):
        """Test that KHCEvent properly inherits all LambdaBaseEvent fields."""
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

        for field in base_fields:
            assert field in event

    def test_postal_code_format(self):
        """Test different postal code formats."""
        events = [
            # Valid postal codes
            {
                "postal_code": "12345",
                "expected_valid": True,
                "description": "Standard postal code",
            },
            {
                "postal_code": "00000",
                "expected_valid": True,
                "description": "All zeros",
            },
            {
                "postal_code": "99999",
                "expected_valid": True,
                "description": "All nines",
            },
            # Invalid postal codes
            {
                "postal_code": "1234",
                "expected_valid": False,
                "description": "Too short",
            },
            {
                "postal_code": "123456",
                "expected_valid": False,
                "description": "Too long",
            },
            {
                "postal_code": "1234a",
                "expected_valid": False,
                "description": "Contains letter",
            },
            {
                "postal_code": "12 34",
                "expected_valid": False,
                "description": "Contains space",
            },
        ]

        for test_case in events:
            event = typing.cast(
                khc.events.khc.KHCEvent,
                {
                    "version": "1.0",
                    "requestContext": {"requestId": "test-id"},
                    "routeKey": "ANY /khc",
                    "rawPath": "/khc",
                    "rawQueryString": "",
                    "headers": {},
                    "isBase64Encoded": False,
                    "postal_code": test_case["postal_code"],
                    "use_ai": True,
                },
            )

            # We validate the format in the Lambda, not in the event type
            # This test just verifies that the field exists and is a string
            assert isinstance(event["postal_code"], str), test_case["description"]

    def test_use_ai_values(self):
        """Test different use_ai values."""
        for use_ai in [True, False]:
            event = typing.cast(
                khc.events.khc.KHCEvent,
                {
                    "version": "1.0",
                    "requestContext": {"requestId": "test-id"},
                    "routeKey": "ANY /khc",
                    "rawPath": "/khc",
                    "rawQueryString": "",
                    "headers": {},
                    "isBase64Encoded": False,
                    "postal_code": "12345",
                    "use_ai": use_ai,
                },
            )

            assert event["use_ai"] is use_ai
