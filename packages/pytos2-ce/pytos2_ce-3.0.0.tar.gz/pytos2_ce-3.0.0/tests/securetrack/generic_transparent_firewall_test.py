import pytest
import json
import responses

from pytos2.securetrack.generic_transparent_firewall import GenericTransparentFirewall
from pytos2.utils import get_api_node


class TestGenericTransparentFirewall:
    device = json.load(
        open("tests/securetrack/json/generic_transparent_firewalls/device-9.json")
    )
    firewalls = device["TransparentFirewalls"]

    @responses.activate
    def test_add_generic_transparent_firewall_200(self, st):
        """Add one or multiple firewalls"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw",
            status=201,
        )

        """Add single firewall"""
        to_add = self.firewalls[0]
        newFirewall = st.add_generic_transparent_firewall(
            output_l3_device_id=to_add["outputL3DeviceId"],
            output_l3_is_generic_device=to_add["outputL3IsGenericDevice"],
            output_l3_interface_name=to_add["outputL3InterfaceName"],
            layer2_device_id=to_add["layer2DeviceId"],
            input_l2_interface_name=to_add["inputL2InterfaceName"],
            output_l2_interface_name=to_add["outputL2InterfaceName"],
            input_l3_device_id=to_add["inputL3DeviceId"],
            input_l3_is_generic_device=to_add["inputL3IsGenericDevice"],
            input_l3_interface_name=to_add["inputL3InterfaceName"],
        )
        assert newFirewall is None

    @responses.activate
    def test_add_generic_transparent_firewall_400(self, st):
        """Add one or multiple firewalls"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw",
            status=400,
        )

        """Add single firewall"""
        with pytest.raises(ValueError) as exception:
            to_add = self.firewalls[0]
            st.add_generic_transparent_firewall(
                output_l3_device_id=to_add["outputL3DeviceId"],
                output_l3_is_generic_device=to_add["outputL3IsGenericDevice"],
                output_l3_interface_name=to_add["outputL3InterfaceName"],
                layer2_device_id=to_add["layer2DeviceId"],
                input_l2_interface_name=to_add["inputL2InterfaceName"],
                output_l2_interface_name=to_add["outputL2InterfaceName"],
                input_l3_device_id=to_add["inputL3DeviceId"],
                input_l3_is_generic_device=to_add["inputL3IsGenericDevice"],
                input_l3_interface_name=to_add["inputL3InterfaceName"],
            )
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_add_generic_transparent_firewall_404(self, st):
        """Add one or multiple firewalls"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw",
            status=404,
        )

        """Add single firewall"""
        with pytest.raises(ValueError) as exception:
            to_add = self.firewalls[0]
            st.add_generic_transparent_firewall(
                output_l3_device_id=to_add["outputL3DeviceId"],
                output_l3_is_generic_device=to_add["outputL3IsGenericDevice"],
                output_l3_interface_name=to_add["outputL3InterfaceName"],
                layer2_device_id=to_add["layer2DeviceId"],
                input_l2_interface_name=to_add["inputL2InterfaceName"],
                output_l2_interface_name=to_add["outputL2InterfaceName"],
                input_l3_device_id=to_add["inputL3DeviceId"],
                input_l3_is_generic_device=to_add["inputL3IsGenericDevice"],
                input_l3_interface_name=to_add["inputL3InterfaceName"],
            )
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_generic_transparent_firewall(
        self, st, generic_transparent_firewall_mock
    ):
        """Get firewalls by device id"""
        firewalls = [
            GenericTransparentFirewall.kwargify(d)
            for d in get_api_node(self.device, "TransparentFirewalls", listify=True)
        ]
        firewallsByInt = st.get_generic_transparent_firewalls(9, False)
        assert firewallsByInt == firewalls

        with pytest.raises(ValueError) as exception:
            st.get_generic_transparent_firewalls(404, False)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_update_generic_transparent_firewalls_200(self, st):
        """Update one or multiple firewalls"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw",
            status=200,
        )

        """Update single firewall"""
        firewall_to_update = GenericTransparentFirewall.kwargify(self.firewalls[0])
        newFirewall = st.update_generic_transparent_firewalls([firewall_to_update])
        assert newFirewall is None

    @responses.activate
    def test_update_generic_transparent_firewalls_400(self, st):
        """PUT bad request"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw",
            status=400,
        )

        with pytest.raises(ValueError) as exception:
            firewall_to_update = GenericTransparentFirewall.kwargify(self.firewalls[0])
            st.update_generic_transparent_firewalls([firewall_to_update])
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_update_generic_transparent_firewalls_404(self, st):
        """PUT device id not found"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw",
            status=404,
        )

        with pytest.raises(ValueError) as exception:
            firewall_to_update = GenericTransparentFirewall.kwargify(self.firewalls[0])
            st.update_generic_transparent_firewalls([firewall_to_update])
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_transparent_firewall(
        self, st, generic_transparent_firewall_mock
    ):
        """Delete firewall by firewall id"""
        firewallByInt = st.delete_generic_transparent_firewall(23)
        assert firewallByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_transparent_firewall(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_transparent_firewalls(
        self, st, generic_transparent_firewall_mock
    ):
        """Delete firewalls by device id"""
        firewallsByInt = st.delete_generic_transparent_firewalls(9)
        assert firewallsByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_transparent_firewalls(404)
        assert "Not Found" in str(exception.value)
