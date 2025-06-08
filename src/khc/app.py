import os
import khc.handler.launch_request_handler
import khc.services.postal_code.provider
import khc.services.openrouter.client
import khc.services.weather.service
import ask_sdk_core.skill_builder


def create_skill():
    """
    Create and configure the Alexa skill with necessary handlers and services.

    Returns:
        ask_sdk_core.skill_builder.SkillBuilder: Configured SkillBuilder instance.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")

    postal_provider = khc.services.postal_code.provider.PostalCodeProvider()
    openrouter_client = khc.services.openrouter.client.OpenRouterClient(api_key=api_key)
    weather_service = khc.services.weather.service.WeatherService(
        openrouter_client=openrouter_client
    )
    launch_handler = khc.handler.launch_request_handler.LaunchRequestHandler(
        weather_service=weather_service, postal_provider=postal_provider
    )

    sb = ask_sdk_core.skill_builder.SkillBuilder()
    sb.add_request_handler(launch_handler)
    return sb


sb = create_skill()
lambda_handler = sb.lambda_handler()
