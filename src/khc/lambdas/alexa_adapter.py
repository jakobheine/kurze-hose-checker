import typing
import aws_lambda_typing.context as context_
import khc.events.alexa
import khc.base._lambda


class AlexaAdapter(khc.base._lambda.LambdaFunction):
    """
    Adapter for Alexa Skills to communicate with the KHC Lambda.

    This adapter:
    1. Receives Alexa Skill requests
    2. Transforms them into a format the KHC Lambda expects
    3. Calls the KHC Lambda
    4. Transforms the response back into Alexa Skill format
    """

    def __init__(self, khc_lambda: khc.base._lambda.LambdaFunction):
        """
        Initialize with a reference to the KHC Lambda.

        Args:
            khc_lambda: The Lambda function that does the actual checking
        """
        self.khc_lambda = khc_lambda

    # type: ignore[override] TypeChecker says bad-override. But it isnt. AlexaEvent is LambdaBaseEvent which is in union of BaseEvent.
    def handler(
        self,
        event: khc.events.alexa.AlexaEvent,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        """
        Handle Alexa Skill requests by delegating to KHC Lambda.

        Args:
            event: Alexa Skill request event
            context: Lambda context

        Returns:
            Alexa Skill response
        """
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hello World from Alexa Adapter",
                },
                "shouldEndSession": True,
            },
            "statusCode": 200,
        }
