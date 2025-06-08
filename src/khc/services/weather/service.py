import khc.services.openrouter.client


class WeatherService:
    """
    Service to provide weather-related answers based on postal code.

    Args:
        openrouter_client: Client instance to communicate with OpenRouter API.
    """

    def __init__(
        self, openrouter_client: khc.services.openrouter.client.OpenRouterClient
    ) -> None:
        self.openrouter_client = openrouter_client

    def get_short_answer(self, postal_code: str) -> str:
        """
        Generate a short answer about wearing shorts today for the given postal code.

        Args:
            postal_code (str): The postal code to query weather information for.

        Returns:
            str: A brief response indicating whether shorts are appropriate.
        """
        prompt = (
            f"Ich bin ein Alexa-Skill. Kann man heute in der Postleitzahl {postal_code} eine kurze Hose tragen? "
            "Antworte nach folgendem Schema: 'Ja/Nein, in [Ort] kann man heute (k)eine kurze Hose tragen. "
            "[Lass baumeln/Versteck die Waden.]'"
        )
        return self.openrouter_client.chat_completion(prompt)
