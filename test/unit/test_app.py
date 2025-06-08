import pytest
import unittest.mock

import khc.handler.launch_request_handler
import khc.services.postal_code.provider
import khc.services.openrouter.client
import khc.services.weather.service
import ask_sdk_core.skill_builder

import khc.app  # Hier der Modulname deiner create_skill Funktion


class TestCreateSkill:
    @pytest.fixture(autouse=True)
    def patch_env(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-api-key")
        yield

    @pytest.fixture(autouse=True)
    def patch_dependencies(self, monkeypatch):
        # Mock PostalCodeProvider
        postal_mock = unittest.mock.Mock(
            spec=khc.services.postal_code.provider.PostalCodeProvider
        )
        monkeypatch.setattr(
            khc.services.postal_code.provider, "PostalCodeProvider", lambda: postal_mock
        )

        # Mock OpenRouterClient
        openrouter_mock = unittest.mock.Mock(
            spec=khc.services.openrouter.client.OpenRouterClient
        )

        def openrouter_init(api_key):
            assert api_key == "fake-api-key"
            return openrouter_mock

        monkeypatch.setattr(
            khc.services.openrouter.client, "OpenRouterClient", openrouter_init
        )

        # Mock WeatherService
        weather_mock = unittest.mock.Mock(
            spec=khc.services.weather.service.WeatherService
        )

        def weather_init(openrouter_client):
            assert openrouter_client == openrouter_mock
            return weather_mock

        monkeypatch.setattr(
            khc.services.weather.service, "WeatherService", weather_init
        )

        # Mock LaunchRequestHandler
        launch_handler_mock = unittest.mock.Mock(
            spec=khc.handler.launch_request_handler.LaunchRequestHandler
        )

        def launch_init(weather_service, postal_provider):
            assert weather_service == weather_mock
            assert postal_provider == postal_mock
            return launch_handler_mock

        monkeypatch.setattr(
            khc.handler.launch_request_handler, "LaunchRequestHandler", launch_init
        )

        # Mock SkillBuilder and its methods
        sb_mock = unittest.mock.Mock(spec=ask_sdk_core.skill_builder.SkillBuilder)
        sb_mock.add_request_handler.return_value = sb_mock
        sb_mock.lambda_handler.return_value = "lambda_handler_func"
        monkeypatch.setattr(ask_sdk_core.skill_builder, "SkillBuilder", lambda: sb_mock)

        yield

    def test_create_skill_returns_skillbuilder(self):
        sb = khc.app.create_skill()
        assert sb is not None
        assert hasattr(sb, "add_request_handler")
        assert hasattr(sb, "lambda_handler")

    def test_lambda_handler_is_created(self):
        sb = khc.app.create_skill()
        lambda_handler = sb.lambda_handler()
        assert lambda_handler == "lambda_handler_func"
