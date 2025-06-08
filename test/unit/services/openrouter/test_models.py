import pytest
import typing
import khc.services.openrouter.models


class TestOpenRouterModels:
    def test_openrouter_request_to_dict(self):
        request = khc.services.openrouter.models.OpenRouterRequest(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hallo"}],
            max_tokens=42,
        )
        expected_dict = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hallo"}],
            "max_tokens": 42,
        }
        assert request.to_dict() == expected_dict

    def test_openrouter_response_from_json_valid(self):
        data = typing.cast(
            dict[str, object],
            {"choices": [{"message": {"content": "Hallo Welt"}}]},
        )
        response = khc.services.openrouter.models.OpenRouterResponse.from_json(data)
        assert isinstance(response, khc.services.openrouter.models.OpenRouterResponse)
        assert response.choices == typing.cast(list[dict[str, object]], data["choices"])

    def test_openrouter_response_from_json_invalid_raises(self):
        data = typing.cast(dict[str, object], {"choices": "invalid"})
        with pytest.raises(ValueError):
            khc.services.openrouter.models.OpenRouterResponse.from_json(data)

    def test_get_message_content_returns_content(self):
        choices = typing.cast(
            list[dict[str, object]],
            [{"message": {"content": "Hello from OpenRouter"}}],
        )
        response = khc.services.openrouter.models.OpenRouterResponse(choices=choices)
        content = response.get_message_content()
        assert content == "Hello from OpenRouter"

    def test_get_message_content_returns_none_for_invalid(self):
        choices = typing.cast(
            list[dict[str, object]],
            [{}],  # missing message key
        )
        response = khc.services.openrouter.models.OpenRouterResponse(choices=choices)
        content = response.get_message_content()
        assert content is None

        choices = typing.cast(
            list[dict[str, object]],
            [{"message": {}}],  # message without content
        )
        response = khc.services.openrouter.models.OpenRouterResponse(choices=choices)
        content = response.get_message_content()
        assert content is None

        response = khc.services.openrouter.models.OpenRouterResponse(choices=[])
        content = response.get_message_content()
        assert content is None
