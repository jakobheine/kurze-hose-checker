import abc
import typing
import aws_lambda_typing.context as context_
import aws_lambda_typing.events


class LambdaFunction(abc.ABC):
    """Base class for AWS Lambda functions."""

    @abc.abstractmethod
    def handler(
        self,
        event: aws_lambda_typing.events.APIGatewayProxyEventV2,
        context: context_.Context,
    ) -> dict[str, typing.Any]:
        """
        Handle an AWS Lambda invocation.

        Args:
            event: Generic Lambda event
            context: Lambda context

        Returns:
            Dict containing the Lambda response
        """
