import typing
import khc.services.postal_code.model


class TestPostalCodeResponse:
    def test_init_and_attributes(self):
        response = khc.services.postal_code.model.PostalCodeResponse(
            country_code="DE",
            postal_code="12345",
        )
        assert response.country_code == "DE"
        assert response.postal_code == "12345"

        response_none = khc.services.postal_code.model.PostalCodeResponse(
            country_code=None,
            postal_code=None,
        )
        assert response_none.country_code is None
        assert response_none.postal_code is None

    def test_from_json_valid_data(self):
        data = typing.cast(
            dict[str, object], {"countryCode": "US", "postalCode": "90210"}
        )
        response = khc.services.postal_code.model.PostalCodeResponse.from_json(data)
        assert response.country_code == "US"
        assert response.postal_code == "90210"

    def test_from_json_missing_keys(self):
        data = typing.cast(dict[str, object], {})
        response = khc.services.postal_code.model.PostalCodeResponse.from_json(data)
        assert response.country_code is None
        assert response.postal_code is None

    def test_from_json_invalid_types(self):
        data = typing.cast(
            dict[str, object], {"countryCode": 123, "postalCode": ["abc"]}
        )
        response = khc.services.postal_code.model.PostalCodeResponse.from_json(data)
        assert response.country_code is None
        assert response.postal_code is None
