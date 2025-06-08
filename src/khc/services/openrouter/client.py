import logging
import requests
import khc.services.openrouter.models

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """
    Client to interact with the OpenRouter chat completion API.

    Args:
        api_key (str | None): The API key for authorization.
    """

    def __init__(self, api_key: str | None) -> None:
        """
        Initialize the OpenRouterClient.

        Args:
            api_key (str | None): The API key for the OpenRouter API.
        """
        self.api_key = api_key

    def chat_completion(self, prompt: str, max_tokens: int = 80) -> str:
        """
        Send a chat completion request to OpenRouter API with a prompt.

        Args:
            prompt (str): The user prompt for the chat completion.
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 80.

        Returns:
            str: The content of the chat completion or an error message.
        """
        if not self.api_key:
            logger.error("API key is not set.")
            return "Der Skill ist aktuell nicht richtig konfiguriert."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        request_body = khc.services.openrouter.models.OpenRouterRequest(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        ).to_dict()

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=request_body,
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            openrouter_response = (
                khc.services.openrouter.models.OpenRouterResponse.from_json(data)
            )
            content = openrouter_response.get_message_content()
            if content:
                return content
            else:
                return "Tut mir leid, ich konnte die Antwort gerade nicht erhalten."
        except requests.RequestException as e:
            logger.error(f"HTTP request error: {e}")
            return "Tut mir leid, ich konnte die Antwort gerade nicht erhalten."
        except ValueError as e:
            logger.error(f"JSON decode error: {e}")
            return "Tut mir leid, ich konnte die Antwort gerade nicht erhalten."
