import typing
import aws_lambda_typing.context as context_
import khc.base._lambda
import khc.events.khc


class KHCLambda(khc.base._lambda.LambdaFunction):
    """Lambda function for Kurze Hosen Checker."""

    # type: ignore[override]
    def handler(
        self,
        event: khc.events.khc.KHCEvent,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        """
        Handle KHC request.

        Args:
            event: Event containing postal code and AI flag
            context: Lambda context

        Returns:
            Dict containing the response
        """
        # Validate postal code format
        if not (
            isinstance(event["postal_code"], str)
            and len(event["postal_code"]) == 5
            and event["postal_code"].isdigit()
        ):
            return {
                "statusCode": 400,
                "message": "Invalid postal code. Must be 5 digits.",
            }

        # For now, just return the input data
        return {
            "statusCode": 200,
            "postal_code": event["postal_code"],
            "use_ai": event["use_ai"],
            "message": "Request processed successfully",
        }
