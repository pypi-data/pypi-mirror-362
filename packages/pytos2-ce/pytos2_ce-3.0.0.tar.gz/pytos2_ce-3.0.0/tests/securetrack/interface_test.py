import pytest
import json

from netaddr import IPAddress, IPNetwork
from pytos2.securetrack.interface import Interface, BindableObject, TopologyInterface
from pytos2.utils import get_api_node


class TestInterface:
    @pytest.fixture
    def interface(self):
        j = json.load(open("tests/securetrack/json/interfaces/device8-interfaces.json"))
        interface_node = get_api_node(j, "interfaces.interface")[0]
        return Interface.kwargify(interface_node)


class TestBindableObject:
    @pytest.fixture
    def bindable(self):
        j = json.load(open("tests/securetrack/json/interfaces/device8-objects.json"))
        object_node = get_api_node(j, "bindable_objects")[1]
        return BindableObject.kwargify(object_node)


class TestTopologyInterface:
    @pytest.fixture
    def topointerface(self):
        j = json.load(
            open("tests/securetrack/json/interfaces/device8-topology-interfaces.json")
        )
        object_node = get_api_node(j, "interface")[0]
        return TopologyInterface.kwargify(object_node)

    def test_attributes(self, topointerface):
        assert topointerface.name == "Datacenter"
        assert topointerface.device_id == 8
        assert topointerface.ip.prefixlen == 24
        assert topointerface.ip.ip == IPAddress("10.3.3.1")
        assert isinstance(topointerface.ip, IPNetwork)


class TestAzureTopologyInterface:
    @pytest.fixture
    def topointerface(self):
        j = json.load(
            open(
                "tests/securetrack/json/interfaces/device784-azure-topology-interfaces.json"
            )
        )
        object_node = get_api_node(j, "interface")[3]
        return TopologyInterface.kwargify(object_node)

    def test_attributes(self, topointerface):
        assert (
            topointerface.name
            == "/subscriptions/44444444-xxxx-yyyy-zzzz-555555555555/resourceGroups/QA-RG/providers/Microsoft.Network/virtualHubs/Main-Hub-WE"
        )
        assert topointerface.device_id == 784
        assert topointerface.ip.prefixlen == 24
        assert topointerface.ip.ip == IPAddress("10.0.10.1")
        assert isinstance(topointerface.ip, IPNetwork)
