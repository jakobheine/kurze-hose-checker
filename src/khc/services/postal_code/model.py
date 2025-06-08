class PostalCodeResponse:
    """
    Data Transfer Object for Alexa Device Address API response.

    Args:
        country_code: The country code of the device, or None if not available.
        postal_code: The postal code of the device, or None if not available.
    """

    def __init__(self, country_code: str | None, postal_code: str | None) -> None:
        self.country_code = country_code
        self.postal_code = postal_code

    @classmethod
    def from_json(cls, data: dict[str, object]) -> "PostalCodeResponse":
        """
        Create an instance of PostalCodeResponse from JSON data.

        Args:
            data: Parsed JSON response from the Alexa API.

        Returns:
            PostalCodeResponse: An instance with country_code and postal_code.
        """
        country = data.get("countryCode")
        postal = data.get("postalCode")

        return cls(
            country_code=country if isinstance(country, str) else None,
            postal_code=postal if isinstance(postal, str) else None,
        )
