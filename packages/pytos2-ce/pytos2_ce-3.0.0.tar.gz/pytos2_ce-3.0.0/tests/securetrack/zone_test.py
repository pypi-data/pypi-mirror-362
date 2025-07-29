import pytest
import json
import responses

from netaddr import IPAddress

from pytos2.securetrack.zone import Zone
from pytos2.utils import get_api_node


class TestZones:
    @responses.activate
    def test_get_zone(self, zones_mock, st):
        zone = st.get_zone(cache=False, identifier=69)
        assert isinstance(zone, Zone)
        assert zone.id == 69
        assert zone.name == "Corporate"
        assert zone.shared is False
        assert zone.internet is False
        assert zone.unassociated_networks is False
        assert zone.domain.id == 1
        zone = st.get_zone(cache=False, identifier="Corporate")
        print(f"Z: {zone}")
        assert zone.id == 69
        assert zone.name == "Corporate"
        assert zone.shared is False
        assert zone.internet is False
        assert zone.unassociated_networks is False
        assert zone.domain.id == 1
        assert isinstance(st.get_zone(cache=False, identifier=69), Zone)
        assert st._zones_cache.is_empty()
        zone_cache = st.get_zone(cache=True, identifier=69)
        assert isinstance(zone_cache, Zone)
        assert st._zones_cache.is_empty() is False
        zone_name = st.get_zone(cache=False, identifier="Corporate")
        assert isinstance(zone_name, Zone)

    @responses.activate
    def test_get_zones(self, zones_mock, st):
        zones = st.get_zones(cache=False)
        assert isinstance(st.get_zones(cache=False), list)
        assert st._zones_cache.is_empty()
        zones_cache = st.get_zones(cache=True)
        assert isinstance(zones_cache, list)
        assert st._zones_cache.is_empty() is False

    @responses.activate
    def test_internet_representing_address(self, zones_mock, st):
        ip_address = st.get_internet_representing_address()
        assert str(ip_address) == "8.8.4.4"

        response = st.set_internet_representing_address("8.8.8.8")
        assert response is None
