import logging

logger = logging.getLogger(__name__)


class OpenRouterRequest:
    """
    Data Transfer Object for OpenRouter chat completion request.

    Args:
        model: Model name to use.
        messages: List of message dicts with roles and content.
        max_tokens: Maximum tokens to generate. Defaults to 80.
    """

    def __init__(
        self, model: str, messages: list[dict[str, str]], max_tokens: int = 80
    ) -> None:
        self.model = model
        self.messages = messages
        self.max_tokens = max_tokens

    def to_dict(self) -> dict[str, object]:
        """
        Convert the request DTO to a dictionary suitable for JSON serialization.

        Returns:
            Dictionary representation of the request.
        """
        return {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
        }


class OpenRouterResponse:
    """
    Data Transfer Object for OpenRouter chat completion response.

    Args:
        choices: List of choices from the API response.
    """

    def __init__(self, choices: list[dict[str, object]]) -> None:
        self.choices = choices

    @classmethod
    def from_json(cls, data: dict[str, object]) -> "OpenRouterResponse":
        """
        Instantiate OpenRouterResponse from JSON data.

        Args:
            data: Parsed JSON data from API response.

        Returns:
            Instance with parsed choices.
        """
        raw_choices = data.get("choices")
        if isinstance(raw_choices, list) and all(
            isinstance(c, dict) for c in raw_choices
        ):
            return cls(choices=raw_choices)
        else:
            raise ValueError("Invalid 'choices' structure in response")

    def get_message_content(self) -> str | None:
        """
        Extract the content of the first message in choices if available.

        Returns:
            Message content or None if not found.
        """
        if (
            isinstance(self.choices, list)
            and len(self.choices) > 0
            and isinstance(self.choices[0], dict)
        ):
            message = self.choices[0].get("message")
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str):
                    return content
        logger.error("Response JSON structure unexpected or empty.")
        return None
