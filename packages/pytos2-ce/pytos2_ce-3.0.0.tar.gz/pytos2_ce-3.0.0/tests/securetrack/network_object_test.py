import json
from pathlib import Path

from pytos2.api import Pager
import responses
import pytest
from netaddr import IPAddress, IPNetwork, IPRange

from pytos2.securetrack.network_object import (
    NetworkObject,
    RangeNetworkObject,
    classify_network_object,
)
from pytos2.utils import get_api_node


class TestDevice:
    @pytest.fixture
    def device(self):
        j = json.load(open("tests/securetrack/json/devices/devices.json"))
        device_node = get_api_node(j, "devices.device")[0]
        return classify_network_object(device_node)


class TestLoadNetworkObjects:
    def test_all_objects(self):
        for path in Path("tests/securetrack/json/network_objects/").glob("*.json"):
            network_objects_node = get_api_node(
                json.load(path.open()), "network_objects.network_object"
            )
            if network_objects_node:
                for network_object in network_objects_node:
                    classify_network_object(network_object)


class TestSearchNetworkObjects:
    @responses.activate
    def test_search_network_objects(self, st, network_objects_mock2):
        pgr = st.search_network_objects(device=20)
        assert len(pgr) == 4

        pgr = st.search_network_objects(device=10000)
        assert isinstance(pgr, Pager)
        assert len(pgr) == 0

        netobjs = st.search_network_objects(name="https")
        for obj in netobjs:
            assert isinstance(obj, NetworkObject)

        with pytest.raises(ValueError):
            st.search_network_objects(name="https", ip="1.1.1.1")


class TestCheckpointObject:
    @responses.activate
    def test_nat_object(self, st, network_objects_mock):
        # this should be refactored when get_network_object returns an object
        obj = st.get_network_object(
            device=20, name="CP_default_Office_Mode_addresses_pool"
        )
        assert obj.nat_info.mapped_to_ip == "Hide Behind Gateway"
        obj = st.get_network_object(device=20, name="Net_172.16.40.0")
        assert isinstance(obj.nat_info.mapped_to_ip, IPAddress)


class TestFortigateObject:
    @responses.activate
    def test_nat_object(self, st, network_objects_mock):
        # this should be refactored when get_network_object returns an object
        obj = st.get_network_object(device=157, name="VIP to HQ")
        assert isinstance(obj.nat_info.mapped_ip, IPAddress)
        assert isinstance(obj.nat_info.mapped_ip_max, IPAddress)


class TestHostObject:
    # this class covers host object with interfaces as well
    @responses.activate
    def test_host_object(self, st, network_objects_mock):
        # this should be refactored when get_network_object returns an object
        obj = st.get_network_object(device=184, name="SGW_200.237")
        assert isinstance(obj.ip, IPAddress)
        assert isinstance(obj.interfaces[0].interface_ips[0].ip, IPAddress)


class TestSubnetObject:
    @responses.activate
    def test_subnet_object(self, st, network_objects_mock):
        # this should be refactored when get_network_object returns an object
        obj = st.get_network_object(device=184, name="Sales_1")
        assert isinstance(obj.subnet, IPNetwork)


class TestRangeObject:
    ip_one = IPAddress("172.16.200.0")
    ip_two = IPAddress("172.16.200.255")
    ip_three = IPAddress("78.23.45.200")
    ip_four = IPAddress("78.32.45.10")

    @responses.activate
    def test_range_object(self, st, network_objects_mock):
        # this should be refactored when get_network_object returns an object
        obj = st.get_network_object(device=184, name="my_range")
        first = int(self.ip_one)
        last = int(self.ip_two)
        assert isinstance(obj.range, IPRange)
        assert obj.reverse_range is False
        assert obj.range.first == first
        assert obj.range.last == last
        assert obj.first == first
        assert obj.last == last

    @responses.activate
    def test_fortinet_range_object(self, st, network_objects_mock):
        obj = st.get_network_object(device=184, name="fortinet_reverse_range")
        first = int(self.ip_one)
        last = int(self.ip_two)
        assert isinstance(obj.range, IPRange)
        assert obj.range.first == first
        assert obj.range.last == last
        assert obj.reverse_range
        assert obj.first == last
        assert obj.last == first

    @responses.activate
    def test_real_worl_fortinet_range_object(self, st, network_objects_mock):
        obj = st.get_network_object(device=184, name="fortinet_real_world")
        first = int(self.ip_three)
        last = int(self.ip_four)
        assert isinstance(obj.range, IPRange)
        assert obj.range.first == first
        assert obj.range.last == last
        assert obj.reverse_range
        assert obj.first == last
        assert obj.last == first

    @responses.activate
    def test_classify_error(self):
        bad_obj = {"first_ip": "Not IP", "last_ip": "172.16.200.0"}

        with pytest.raises(ValueError):
            RangeNetworkObject.kwargify(bad_obj)


class TestNetworkObjects:
    @responses.activate
    def test_network_objects(self, st, network_objects_mock):
        pager = st.get_network_objects(revision=24522)
        assert isinstance(pager, Pager)
        network_objects = pager.fetch_all()
        obj = network_objects[0]
        assert obj.id == 450118
        assert obj.name == "Admin_server_02"

        network_objects = st.get_network_objects(revision=24522, object_ids=[450118])
        assert isinstance(network_objects, list)
        assert len(network_objects) == 1

        network_objects = st.get_network_objects(device=10, object_ids=[80681])
        assert isinstance(network_objects, list)
        assert len(network_objects) == 1

        groups = st.get_network_object_groups(15)
        assert len(groups) == 1
        assert groups[0].name == "Panorama-G-1"

        pager = st.get_network_object_rules(12)
        assert isinstance(pager, Pager)
        rules = pager.fetch_all()
        assert len(rules) == 3
        assert rules[0].id == 26
        assert rules[0].name == "HQ access"
