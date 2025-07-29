import pytest
import json
import responses

from pytos2.securetrack.application import (
    ObjectReference,
    Application,
    SingleApplication,
    ApplicationGroup,
)
from pytos2.utils import get_api_node


class TestApplications:
    @responses.activate
    def test_get_applications(self, applications_mock, devices_mock, st):
        applications = st.get_device_applications(174)
        assert len(applications) == 3

        assert isinstance(applications[0], SingleApplication)
        assert applications[0].id == 742402
        assert applications[0].name == "Any"
        assert applications[0].display_name == "Any"
        assert applications[0].class_name == "any_object"
        assert applications[0].type == "any"
        assert applications[0].comment == ""
        assert applications[0].uid == "{bf62fdcf-e2c8-442e-a455-8bbc070e1cc3}"
        assert applications[0].overrides is False
        assert applications[0].management_domain == ""
        assert applications[0].global_device is None
        assert applications[0].device_id is None
        assert applications[0].application_id == ""
        assert applications[0].device_name == ""
        assert len(applications[0].services) == 0

        assert isinstance(applications[1], SingleApplication)
        assert applications[1].id == 742405
        assert applications[1].name == "104apci-unnumbered"
        assert applications[1].display_name == "104apci-unnumbered"
        assert applications[1].class_name == "application_object"
        assert applications[1].type == "single"
        assert applications[1].comment == ""
        assert applications[1].uid == "{286C3A6E-463C-5E3E-3427-4A98110EC5D6}"
        assert applications[1].overrides is False
        assert applications[1].management_domain == "Predefined"
        assert applications[1].global_device is None
        assert applications[1].device_id is None
        assert applications[1].application_id == ""
        assert applications[1].device_name == ""
        assert len(applications[1].services) == 1

        assert isinstance(applications[1].services[0], ObjectReference)
        assert applications[1].services[0].id == 6295334
        assert (
            applications[1].services[0].uid == "{3E95B1FB-7F0F-FE14-4DB7-CD54836E849B}"
        )
        assert applications[1].services[0].name == "st_implicit_app_100bao_2"
        assert applications[1].services[0].display_name == "st_implicit_app_100bao_2"
        assert applications[1].services[0].management_domain == "Predefined"
        assert applications[1].services[0].type == ""
        assert len(applications[1].services[0].ips) == 0
        assert applications[1].services[0].link == ""
        assert len(applications[1].services[0].members) == 0

        assert isinstance(applications[2], ApplicationGroup)
        assert applications[2].id == 744449
        assert applications[2].name == "meebo"
        assert applications[2].display_name == "meebo"
        assert applications[2].class_name == "application_group"
        assert applications[2].type == "group"
        assert applications[2].comment == ""
        assert applications[2].uid == "{69C3839D-B9F8-090D-2FB2-0B0A0672F761}"
        assert applications[2].overrides is False
        assert applications[2].management_domain == "Predefined"
        assert applications[2].global_device is None
        assert applications[2].device_id is None
        assert applications[2].application_id == ""
        assert applications[2].device_name == ""
        assert len(applications[2].applications) == 1

        assert isinstance(applications[2].applications[0], ObjectReference)
        assert applications[2].applications[0].id == 744451
        assert (
            applications[2].applications[0].uid
            == "{5C51B093-3B98-22BE-16B6-3A1F879699D1}"
        )
        assert applications[2].applications[0].name == "meebo-file-transfer"
        assert applications[2].applications[0].display_name == "meebo-file-transfer"
        assert applications[2].applications[0].management_domain == "Predefined"
        assert applications[2].applications[0].type == ""
        assert len(applications[2].applications[0].ips) == 0
        assert applications[2].applications[0].link == ""
        assert len(applications[2].applications[0].members) == 0

        applications = st.get_device_applications("SGW_200.237")
        assert applications == []

    @responses.activate
    def test_get_applications_failed(self, applications_failed_mock, devices_mock, st):
        with pytest.raises(ValueError) as e:
            st.get_device_applications(1337)

        assert "Failed to decode" in str(e.value)

        with pytest.raises(ValueError) as e:
            st.get_device_applications(1338)

        assert "Failed to get resource" in str(e.value)

        with pytest.raises(ValueError) as e:
            st.get_device_applications("NONEXISTENT")

        assert "Cannot find device" in str(e.value)
