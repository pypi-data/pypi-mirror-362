import pytest
import responses

from pytos2.securetrack.properties import Properties


class TestProperties:
    @responses.activate
    def test_get_properties(self, properties_mock, st):
        properties = st.get_properties()

        assert properties.secure_change_addresses[0].ip_address == "127.0.0.1"
        assert properties.secure_change_addresses[0].type == "external"
        assert properties.secure_change_addresses[1].ip_address == "127.0.0.1"
        assert properties.secure_change_addresses[1].type == "internal"

        assert (
            properties.general_properties[0].key == "LICENSE_ABOUT_TO_EXPIRE_THRESHOLD"
        )
        assert properties.general_properties[0].value == "45"

    @responses.activate
    def test_set_license_notification_days(self, properties_mock, st):
        st.set_license_notification_days(100)
