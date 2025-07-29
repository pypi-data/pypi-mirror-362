import pytest
import json
import responses
from . import conftest

from pytos2.securetrack.security_policy import (
    SecurityPolicy,
    SecurityPolicyDeviceMapping,
    SecurityPolicyInterface,
    SecurityPolicyMatrixType,
    SecurityZoneMatrix,
    CSVData,
    InterfacesManualMappings,
    InterfaceUserMapping,
    ZoneUserAction,
)


class TestSecurityPolicy:
    @responses.activate
    def test_get_security_policies(self, security_policy_mock, st):
        security_policies = st.get_usp_policies()
        first = security_policies[0]
        assert first.id == 7131354762492230143
        assert first.name == "27001"
        assert first.domain_id == "1"
        assert first.domain_name == "Default"
        assert first.description is None
        assert first.type == SecurityPolicyMatrixType.SECURITY_ZONE_MATRIX
        assert (
            security_policies[13].description
            == "Aligning trust and networks to the Trusted Internet Connections Model"
        )

        security_policies = st.get_usp_policies(get_global=True)
        first = security_policies[0]
        assert first.id == 7131354762492230143
        assert first.name == "27001"
        assert first.domain_id == "1"
        assert first.domain_name == "Default"
        assert first.type == SecurityPolicyMatrixType.SECURITY_ZONE_MATRIX

    @responses.activate
    def test_get_security_policies_ignoreSecureTrack2Data(
        self, security_policy_mock, st
    ):
        security_policies = st.get_usp_policies(aurora_data=False)
        first = security_policies[0]
        assert first.id == 1
        assert first.name == "Corporate Matrix (Physical + AWS)"
        assert first.domain_id == "1"
        assert first.domain_name == "Default"
        assert first.description == ""

    @responses.activate
    def test_export_security_policy(self, security_policy_mock, st):
        csv_string = st.export_usp_policy(7131354762492230143)
        assert isinstance(csv_string, str)

        with pytest.raises(ValueError) as exception:
            st.export_usp_policy(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_usp_map(self, security_policy_mock, st):
        security_policy_device_mapping = st.get_usp_map(5)
        assert security_policy_device_mapping.device_id == 5
        assert isinstance(security_policy_device_mapping.affiliated_interfaces, list)
        assert isinstance(security_policy_device_mapping.interfaces, list)
        interf = security_policy_device_mapping.interfaces[1]
        assert interf.name == "ge-0/0/1.1"
        assert interf.zones[0] == "Virtual_DC-04"

    @responses.activate
    def test_delete_security_policy(self, security_policy_mock, st):
        deleted = st.delete_usp_policy(7131354762492230143)
        assert deleted is None

        with pytest.raises(ValueError) as exception:
            st.delete_usp_policy(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_add_usp_map(self, security_policy_mock, st, zones_mock):
        resp = st.add_usp_map(device=5, interface_name="ge-0/0/0.0", zone=147)
        assert resp is None

        with pytest.raises(ValueError) as exception:
            st.add_usp_map(404, "", -1)
        assert "Not Found" in str(exception.value)

        resp = st.add_usp_map(
            device=5, interface_name="ge-0/0/0.0", zone="SomeTestZone"
        )
        assert resp is None

        with pytest.raises(ValueError) as e:
            st.add_usp_map(
                device=5, interface_name="ge-0/0/0.0", zone="SomeNonexistentZone"
            )
        assert "No matching zones" in str(e.value)

    @responses.activate
    def test_delete_usp_map(self, security_policy_mock, st):
        resp = st.delete_usp_map(device=5, interface_name="ge-0/0/0.0", zone=147)
        assert resp is None

        with pytest.raises(ValueError) as exception:
            st.delete_usp_map(404, "", -1)
        assert "Not Found" in str(exception.value)
