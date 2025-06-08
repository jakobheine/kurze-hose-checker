import pytest
import unittest.mock
import khc.services.openrouter.client
import khc.services.weather.service


class TestWeatherService:
    @pytest.fixture
    def openrouter_client_mock(self):
        return unittest.mock.Mock(spec=khc.services.openrouter.client.OpenRouterClient)

    @pytest.fixture
    def weather_service(self, openrouter_client_mock):
        return khc.services.weather.service.WeatherService(
            openrouter_client=openrouter_client_mock
        )

    def test_get_short_answer_calls_openrouter_client(
        self, weather_service, openrouter_client_mock
    ):
        postal_code = "12345"
        expected_prompt = (
            f"Ich bin ein Alexa-Skill. Kann man heute in der Postleitzahl {postal_code} eine kurze Hose tragen? "
            "Antworte nach folgendem Schema: 'Ja/Nein, in [Ort] kann man heute (k)eine kurze Hose tragen. "
            "[Lass baumeln/Versteck die Waden.]'"
        )
        expected_response = (
            "Ja, in Musterstadt kann man heute eine kurze Hose tragen. Lass baumeln."
        )

        openrouter_client_mock.chat_completion.return_value = expected_response

        result = weather_service.get_short_answer(postal_code)

        openrouter_client_mock.chat_completion.assert_called_once_with(expected_prompt)
        assert result == expected_response
