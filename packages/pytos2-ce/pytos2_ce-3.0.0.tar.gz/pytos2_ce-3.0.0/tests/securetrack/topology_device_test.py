import pytest
import json
import responses
from responses import matchers

from pytos2.securetrack.topology_device import TopologyDevice
from pytos2.utils import get_api_node


class TestTopologyDevice:
    @responses.activate
    def test_get_topology_devices(self, st, topology_device_mock):
        """Test getting all topology devices"""
        devices = st.get_topology_devices()

        assert len(devices) == 229
        assert isinstance(devices[0], TopologyDevice)
        assert devices[0].id == 716
        assert devices[0].name == "V_OPM"
        assert devices[0].topology_enabled is True

        hub_dev = next(d for d in devices if d.name == "VirtualHub_West_US")
        assert hub_dev.id == 608
        assert hub_dev.vendor == "Azure"
        assert hub_dev.opm_id == "W-KeQN48tL-c2PXq2TuiYg=="
        assert hub_dev.opm_parent == "r2k5sreJHbdafBDqIQnACw=="
        assert hub_dev.parent == 606

        # Check that different types of devices are parsed correctly
        # Regular device without OPM properties
        asa_device = next(d for d in devices if d.name == "ASA_L2LFW")
        assert asa_device.id == 392
        assert asa_device.vendor == "Cisco"
        assert asa_device.opm_id is None

        # Azure device with OPM properties
        azure_device = next(
            d for d in devices if d.name == "Azure Testing Subscription"
        )
        assert azure_device.id == 508
        assert azure_device.vendor == "Azure"
        assert azure_device.opm_vendor == "MICROSOFT"
        assert azure_device.opm_model == "AZURE_ACCOUNT"
        assert azure_device.opm_system_id == "t7qaK8gDSbC-5tCF9DXy7Q=="

    @responses.activate
    def test_get_topology_device(self, st, topology_device_mock):
        """Test getting a single topology device by ID"""
        device = st.get_topology_device(716)

        assert isinstance(device, TopologyDevice)
        assert device.id == 716
        assert device.name == "V_OPM"
        assert device.model == ""
        assert device.domain == 1
        assert device.virtual_type == ""
        assert device.topology_enabled is True
        assert device.has_dynamic_topology == "enable"
        assert device.opm_id == "aNu2ebd5mhuDsBfm6v1Kog=="
        assert device.opm_system_id == "bvnfqz9aQq-qyAgdfJThVA=="
        assert device.opm_type == "MANAGEMENT"
        assert device.opm_vendor == "UNKNOWN"
        assert device.opm_model == "UNKNOWN"

    @responses.activate
    def test_get_topology_device_not_found(self, st, topology_device_mock):
        """Test getting a topology device that doesn't exist"""
        with pytest.raises(ValueError, match="Error Getting Topology Device 999"):
            st.get_topology_device(999)

    @responses.activate
    def test_topology_device_properties(self, topology_devices_data):
        """Test the TopologyDevice model properties and conversion"""
        device_data = topology_devices_data["TopologyDevices"][0]
        device = TopologyDevice.kwargify(device_data)

        assert device.id == 716
        assert device.name == "V_OPM"
        assert device.domain == 1
        assert device.topology_enabled is True
        assert device.opm_id == "aNu2ebd5mhuDsBfm6v1Kog=="
        assert device.opm_type == "MANAGEMENT"

        # Test conversion back to JSON/dict representation
        device_dict = device._json
        assert device_dict["device_id"] == 716
        assert device_dict["device_name"] == "V_OPM"
        assert device_dict["device_topology_enabled"] is True
        assert device_dict["opm_device_id"] == "aNu2ebd5mhuDsBfm6v1Kog=="
