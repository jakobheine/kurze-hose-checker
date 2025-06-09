import abc
import typing
import aws_lambda_typing.context as context_
import khc.base.event


class LambdaFunction(abc.ABC):
    """Base class for AWS Lambda functions."""

    @abc.abstractmethod
    def handler(
        self,
        event: khc.base.event.BaseEvent,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        """
        Handle an AWS Lambda invocation.

        Args:
            event: Either an API Gateway event or an Alexa event
            context: Lambda context

        Returns:
            Dict containing the Lambda response
        """
