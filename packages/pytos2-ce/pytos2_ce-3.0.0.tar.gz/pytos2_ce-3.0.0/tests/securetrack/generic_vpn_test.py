import pytest
import json
import responses

from pytos2.securetrack.generic_vpn import GenericVpn
from pytos2.utils import get_api_node


class TestGenericVpn:
    device = json.load(open("tests/securetrack/json/generic_vpns/device-3.json"))
    vpns = device["GenericVpns"]

    vpn24 = json.load(open("tests/securetrack/json/generic_vpns/vpn-24.json"))
    vpn = vpn24["GenericVpn"]

    @responses.activate
    def test_add_generic_vpns_200(self, st):
        """Add one or multiple vpns"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/vpn",
            status=201,
        )

        """Add single vpn"""
        newVpn = st.add_generic_vpn(
            generic=True,
            device=1,
            interface_name="new33",
            vpn_name=None,
            tunnel_source_ip_addr="3.3.3.33",
            tunnel_dest_ip_addr="1.1.1.11",
        )
        assert newVpn is None

    @responses.activate
    def test_add_generic_vpns_400(self, st):
        """Add one or multiple vpns"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/vpn",
            status=400,
        )

        """Add single vpn"""
        with pytest.raises(ValueError) as exception:
            st.add_generic_vpn(
                generic=True,
                device=1,
                interface_name="new33",
                vpn_name=None,
                tunnel_source_ip_addr="3.3.3.33",
                tunnel_dest_ip_addr="1.1.1.11",
            )
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_add_generic_vpns_404(self, st):
        """Add one or multiple vpns"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/vpn",
            status=404,
        )

        """Add single vpn"""
        with pytest.raises(ValueError) as exception:
            st.add_generic_vpn(
                generic=True,
                device=1,
                interface_name="new33",
                vpn_name=None,
                tunnel_source_ip_addr="3.3.3.33",
                tunnel_dest_ip_addr="1.1.1.11",
            )
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_generic_vpn(self, st, generic_vpn_mock):
        """Get vpn by vpn id"""
        mockRes = get_api_node(self.vpn24, "GenericVpn")
        vpn = GenericVpn.kwargify(mockRes)
        vpnByInt = st.get_generic_vpn(24)
        vpnByStr = st.get_generic_vpn("24")
        assert vpnByInt == vpn
        assert vpnByStr == vpn

        with pytest.raises(ValueError) as exception:
            st.get_generic_vpn(404)
        assert "Not Found" in str(exception.value)

        with pytest.raises(ValueError) as exception:
            st.get_generic_vpn("404")
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_generic_vpns(self, st, generic_vpn_mock):
        """Get vpns by device id"""
        vpns = [
            GenericVpn.kwargify(d)
            for d in get_api_node(self.device, "GenericVpns", listify=True)
        ]
        vpnsByInt = st.get_generic_vpns(3, generic=True)
        vpnsByInt2 = st.get_generic_vpns(3, generic=False)
        assert vpnsByInt == vpns
        assert vpnsByInt2 == vpns

        with pytest.raises(ValueError) as exception:
            st.get_generic_vpns(404, generic=True)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_update_generic_vpns_200(self, st):
        """Update one or multiple vpns"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/vpn",
            status=200,
        )

        """Update single vpn"""
        vpn_to_update = GenericVpn.kwargify(self.vpn)
        newVpn = st.update_generic_vpn(vpn_to_update)
        assert newVpn is None

    @responses.activate
    def test_update_generic_vpns_400(self, st):
        """PUT bad request"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/vpn",
            status=400,
        )

        with pytest.raises(ValueError) as exception:
            vpn_to_update = GenericVpn.kwargify(self.vpn)
            st.update_generic_vpn(vpn_to_update)
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_update_generic_vpns_404(self, st):
        """PUT device id not found"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/vpn",
            status=404,
        )

        with pytest.raises(ValueError) as exception:
            vpn_to_update = GenericVpn.kwargify(self.vpn)
            st.update_generic_vpn(vpn_to_update)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_vpn(self, st, generic_vpn_mock):
        """Delete vpn by vpn id"""
        vpnByInt = st.delete_generic_vpn(24)
        assert vpnByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_vpn(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_vpns(self, st, generic_vpn_mock):
        """Delete vpns by device id"""
        vpnsByInt = st.delete_generic_vpns(1)
        assert vpnsByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_vpns(404)
        assert "Not Found" in str(exception.value)
