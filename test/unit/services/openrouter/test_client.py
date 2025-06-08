import pytest
import unittest.mock
import requests
import khc.services.openrouter.client
import khc.services.openrouter.models


class TestOpenRouterClient:
    @pytest.fixture
    def client_with_key(self):
        return khc.services.openrouter.client.OpenRouterClient(api_key="test_api_key")

    @pytest.fixture
    def client_without_key(self):
        return khc.services.openrouter.client.OpenRouterClient(api_key=None)

    def test_chat_completion_no_api_key(self, client_without_key):
        result = client_without_key.chat_completion("Hello")
        assert result == "Der Skill ist aktuell nicht richtig konfiguriert."

    def test_chat_completion_success(self, client_with_key):
        with (
            unittest.mock.patch(
                "khc.services.openrouter.client.requests.post"
            ) as mock_post,
            unittest.mock.patch(
                "khc.services.openrouter.models.OpenRouterResponse.from_json"
            ) as mock_from_json,
        ):
            mock_response = unittest.mock.Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "Hallo, wie kann ich helfen?"}}]
            }
            mock_post.return_value = mock_response

            mock_instance = unittest.mock.Mock()
            mock_instance.get_message_content.return_value = (
                "Hallo, wie kann ich helfen?"
            )
            mock_from_json.return_value = mock_instance

            result = client_with_key.chat_completion("Hallo")

            mock_post.assert_called_once()
            mock_from_json.assert_called_once()
            assert result == "Hallo, wie kann ich helfen?"

    def test_chat_completion_no_content(self, client_with_key):
        with (
            unittest.mock.patch(
                "khc.services.openrouter.client.requests.post"
            ) as mock_post,
            unittest.mock.patch(
                "khc.services.openrouter.models.OpenRouterResponse.from_json"
            ) as mock_from_json,
        ):
            mock_response = unittest.mock.Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {}
            mock_post.return_value = mock_response

            mock_instance = unittest.mock.Mock()
            mock_instance.get_message_content.return_value = None
            mock_from_json.return_value = mock_instance

            result = client_with_key.chat_completion("Hallo")

            assert (
                result == "Tut mir leid, ich konnte die Antwort gerade nicht erhalten."
            )

    def test_chat_completion_request_exception(self, client_with_key):
        with unittest.mock.patch(
            "khc.services.openrouter.client.requests.post"
        ) as mock_post:
            mock_post.side_effect = requests.RequestException("Connection error")

            result = client_with_key.chat_completion("Hallo")

            assert (
                result == "Tut mir leid, ich konnte die Antwort gerade nicht erhalten."
            )

    def test_chat_completion_value_error(self, client_with_key):
        with unittest.mock.patch(
            "khc.services.openrouter.client.requests.post"
        ) as mock_post:
            mock_response = unittest.mock.Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.side_effect = ValueError("JSON error")
            mock_post.return_value = mock_response

            result = client_with_key.chat_completion("Hallo")

            assert (
                result == "Tut mir leid, ich konnte die Antwort gerade nicht erhalten."
            )
