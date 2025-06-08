import pytest
import unittest.mock
import khc.handler.launch_request_handler


class TestLaunchRequestHandler:
    @pytest.fixture
    def weather_service_mock(self):
        mock = unittest.mock.Mock()
        mock.get_short_answer.return_value = "Das Wetter ist schön."
        return mock

    @pytest.fixture
    def postal_provider_mock(self):
        mock = unittest.mock.Mock()
        mock.get_postal_code.return_value = "12345"
        return mock

    @pytest.fixture
    def handler_input_mock(self):
        mock = unittest.mock.Mock()
        mock.request_envelope.request.object_type = "LaunchRequest"
        mock.response_builder.speak.return_value = mock.response_builder
        mock.response_builder.set_should_end_session.return_value = (
            mock.response_builder
        )
        mock.response_builder.response = "response_object"
        return mock

    def test_can_handle_true(self, handler_input_mock):
        handler = khc.handler.launch_request_handler.LaunchRequestHandler(
            weather_service=unittest.mock.Mock(), postal_provider=unittest.mock.Mock()
        )
        result = handler.can_handle(handler_input_mock)
        assert result is True

    def test_handle_success(
        self, weather_service_mock, postal_provider_mock, handler_input_mock
    ):
        handler = khc.handler.launch_request_handler.LaunchRequestHandler(
            weather_service=weather_service_mock,
            postal_provider=postal_provider_mock,
        )

        response = handler.handle(handler_input_mock)

        postal_provider_mock.get_postal_code.assert_called_once_with(handler_input_mock)
        weather_service_mock.get_short_answer.assert_called_once_with("12345")
        handler_input_mock.response_builder.speak.assert_called_once_with(
            "Das Wetter ist schön."
        )
        assert response == handler_input_mock.response_builder.response

    def test_handle_permission_error(self, postal_provider_mock, handler_input_mock):
        postal_provider_mock.get_postal_code.side_effect = PermissionError
        handler = khc.handler.launch_request_handler.LaunchRequestHandler(
            weather_service=unittest.mock.Mock(),
            postal_provider=postal_provider_mock,
        )

        response = handler.handle(handler_input_mock)

        postal_provider_mock.get_postal_code.assert_called_once_with(handler_input_mock)
        handler_input_mock.response_builder.speak.assert_called_once()
        handler_input_mock.response_builder.set_should_end_session.assert_called_once_with(
            True
        )
        assert response == handler_input_mock.response_builder.response
