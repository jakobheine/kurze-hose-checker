import logging
import ask_sdk_core.dispatch_components
import ask_sdk_core.utils
import khc.services.weather.service
import khc.services.postal_code.provider

logger = logging.getLogger(__name__)


class LaunchRequestHandler(ask_sdk_core.dispatch_components.AbstractRequestHandler):
    """
    Handler for Alexa skill launch requests.

    Args:
        weather_service: Service providing weather-related responses.
        postal_provider: Service to retrieve postal code from Alexa device.
    """

    def __init__(
        self,
        weather_service: khc.services.weather.service.WeatherService,
        postal_provider: khc.services.postal_code.provider.PostalCodeProvider,
    ) -> None:
        """
        Initialize the LaunchRequestHandler with required services.

        Args:
            weather_service (khc.services.weather.service.WeatherService): The weather service instance.
            postal_provider (khc.services.postal_code.provider.PostalCodeProvider): The postal code provider instance.
        """
        self.weather_service = weather_service
        self.postal_provider = postal_provider

    def can_handle(self, handler_input):
        """
        Determine if this handler can handle the incoming request.

        Args:
            handler_input: Input from Alexa service.

        Returns:
            bool: True if the request is a LaunchRequest, False otherwise.
        """
        return ask_sdk_core.utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        """
        Handle the LaunchRequest by retrieving postal code and returning weather advice.

        Args:
            handler_input: Input from Alexa service.

        Returns:
            Response: Alexa response object with speech output.
        """
        try:
            postal_code = self.postal_provider.get_postal_code(handler_input)
        except PermissionError:
            speak_output = (
                "Bitte erlaube in den Einstellungen der Alexa App den Zugriff auf deine Postleitzahl, "
                "damit ich dir Auskunft geben kann."
            )
            return (
                handler_input.response_builder.speak(speak_output)
                .set_should_end_session(True)
                .response
            )

        speak_output = self.weather_service.get_short_answer(postal_code)
        return handler_input.response_builder.speak(speak_output).response
