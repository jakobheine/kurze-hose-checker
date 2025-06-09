import typing
import khc.base.event


class AlexaEvent(khc.base.event.LambdaBaseEvent):
    """Type definition for Alexa Skill events."""

    # Alexa-specific fields
    session: dict[str, typing.Any]
    request: dict[str, typing.Any]
    context: typing.NotRequired[dict[str, typing.Any]]
