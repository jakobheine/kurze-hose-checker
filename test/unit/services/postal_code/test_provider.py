import pytest
import unittest.mock
import requests
import khc.services.postal_code.model
import ask_sdk_core.handler_input
import khc.services.postal_code.provider


class TestPostalCodeProvider:
    @pytest.fixture
    def handler_input_mock(self):
        mock = unittest.mock.Mock(spec=ask_sdk_core.handler_input.HandlerInput)

        # Vorbereitung der verschachtelten Mocks
        device_mock = unittest.mock.Mock()
        device_mock.device_id = "device123"

        system_mock = unittest.mock.Mock()
        system_mock.device = device_mock
        system_mock.api_endpoint = "https://api.amazonalexa.com"
        system_mock.api_access_token = "token-abc"

        context_mock = unittest.mock.Mock()
        context_mock.system = system_mock

        request_envelope_mock = unittest.mock.Mock()
        request_envelope_mock.context = context_mock

        mock.request_envelope = request_envelope_mock

        return mock

    @pytest.fixture
    def requests_get_mock(self):
        with unittest.mock.patch("requests.get") as mock_get:
            yield mock_get

    def test_get_postal_code_success(self, handler_input_mock, requests_get_mock):
        response_mock = unittest.mock.Mock(spec=requests.Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"countryCode": "DE", "postalCode": "12345"}
        requests_get_mock.return_value = response_mock

        postal_code = (
            khc.services.postal_code.provider.PostalCodeProvider.get_postal_code(
                handler_input_mock
            )
        )

        requests_get_mock.assert_called_once_with(
            "https://api.amazonalexa.com/v1/devices/device123/settings/address/countryAndPostalCode",
            headers={"Authorization": "Bearer token-abc"},
            timeout=3,
        )
        assert postal_code == "12345"

    def test_get_postal_code_no_postal_code_in_response(
        self, handler_input_mock, requests_get_mock
    ):
        response_mock = unittest.mock.Mock(spec=requests.Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "countryCode": "DE",
        }
        requests_get_mock.return_value = response_mock

        with pytest.raises(PermissionError, match="Postal code not available."):
            khc.services.postal_code.provider.PostalCodeProvider.get_postal_code(
                handler_input_mock
            )

    def test_get_postal_code_permission_denied(
        self, handler_input_mock, requests_get_mock
    ):
        response_mock = unittest.mock.Mock(spec=requests.Response)
        response_mock.status_code = 403
        response_mock.text = "Forbidden"
        requests_get_mock.return_value = response_mock

        with pytest.raises(
            PermissionError, match="Missing permissions for device address."
        ):
            khc.services.postal_code.provider.PostalCodeProvider.get_postal_code(
                handler_input_mock
            )

    def test_get_postal_code_other_error(self, handler_input_mock, requests_get_mock):
        response_mock = unittest.mock.Mock(spec=requests.Response)
        response_mock.status_code = 500
        response_mock.text = "Internal Server Error"
        requests_get_mock.return_value = response_mock

        with pytest.raises(PermissionError, match="Failed to get postal code: 500"):
            khc.services.postal_code.provider.PostalCodeProvider.get_postal_code(
                handler_input_mock
            )
