import logging
import requests
import ask_sdk_core.handler_input

import khc.services.postal_code.model

logger = logging.getLogger(__name__)


class PostalCodeProvider:
    @staticmethod
    def get_postal_code(handler_input: ask_sdk_core.handler_input.HandlerInput) -> str:
        """
        Retrieve the postal code from Alexa Device Address API.

        Args:
            handler_input: The Alexa SDK handler input containing the request envelope and context.

        Returns:
            str: The postal code of the Alexa device.

        Raises:
            PermissionError: If permissions are missing or postal code is not available.
        """
        device_id: str = handler_input.request_envelope.context.system.device.device_id
        api_endpoint: str = handler_input.request_envelope.context.system.api_endpoint
        api_access_token: str = (
            handler_input.request_envelope.context.system.api_access_token
        )

        url = f"{api_endpoint}/v1/devices/{device_id}/settings/address/countryAndPostalCode"
        headers = {"Authorization": f"Bearer {api_access_token}"}

        response: requests.Response = requests.get(url, headers=headers, timeout=3)

        if response.status_code == 200:
            data: dict[str, object] = response.json()
            postal_response = (
                khc.services.postal_code.model.PostalCodeResponse.from_json(data)
            )
            if postal_response.postal_code:
                logger.info(f"Postal code retrieved: {postal_response.postal_code}")
                return postal_response.postal_code
            else:
                logger.error("Postal code not found in response JSON.")
                raise PermissionError("Postal code not available.")
        elif response.status_code == 403:
            logger.error("Permission denied for device address API.")
            raise PermissionError("Missing permissions for device address.")
        else:
            logger.error(
                f"Failed to get postal code: {response.status_code} - {response.text}"
            )
            raise PermissionError(f"Failed to get postal code: {response.status_code}")
