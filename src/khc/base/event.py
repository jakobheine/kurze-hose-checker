import aws_lambda_typing.events
import typing


class LambdaBaseEvent(typing.TypedDict):
    """Base TypedDict for all Lambda events with common fields."""

    version: str
    requestContext: dict[str, typing.Any]
    # Common API Gateway fields that are also useful for other events
    routeKey: str
    rawPath: str
    rawQueryString: str
    headers: dict[str, str]
    isBase64Encoded: bool


BaseEvent = aws_lambda_typing.events.APIGatewayProxyEventV2 | LambdaBaseEvent
