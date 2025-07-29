import pytest
import json
from typing import List
from netaddr import IPAddress
import responses
from . import conftest

from pytos2.api import Pager
from pytos2.securetrack.topology import (
    TopologyMode,
    TopologySyncStatus,
    TopologySubnet,
    TopologySubnetDetailed,
    SubnetDevice,
)


class TestTopology:
    @responses.activate
    def test_topology_subnets(self, topology_subnets_mock, st):
        pager: Pager = st.get_topology_subnets()
        subnets: List[TopologySubnet] = pager.fetch_all()
        for sub in subnets:
            assert isinstance(sub.id, int)
            assert isinstance(sub.name, str)
            assert isinstance(sub.ip, IPAddress)
            assert isinstance(sub.mask, IPAddress)
            if sub.domain_id_tag:
                assert isinstance(sub.domain_id_tag, int)

        sub = subnets[0]
        assert sub.id == 6
        assert sub.name == "10.1.1.0/30"
        assert sub.ip == IPAddress("10.1.1.0")
        assert sub.mask == IPAddress("255.255.255.252")
        assert sub.domain_id_tag == 1

        sub: TopologySubnetDetailed = st.get_topology_subnet(6)
        assert sub.id == 6
        assert sub.name == "10.1.1.0/30"
        assert sub.ip == IPAddress("10.1.1.0")
        assert sub.mask == IPAddress("255.255.255.252")
        if sub.domain_id_tag:
            assert sub.domain_id_tag == 1

        device = sub.attached_devices[0]
        assert isinstance(device, SubnetDevice)
        assert device.id == 1
        assert device.is_generic is False
        assert device.name == "RTR1"
        assert device.interface_id == 1
        assert device.interface_name == "GigabitEthernet2"
        assert device.interface_ip == IPAddress("10.1.1.2")

        assert isinstance(sub.join_candidates, List)
